#!/usr/bin/env python
"""Build a portable, secret-minimized Hermes profile snapshot."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import re
import shutil
import sqlite3
import subprocess
from pathlib import Path

PROFILE_ITEMS = [
    "config.yaml", "profile.yaml", "SOUL.md", "PROFILE.md", ".no-bundled-skills",
    "README-FIRST.txt", "ACCEPTANCE.md", "MARKET-REVIEW.md", "terminal-env.sh",
    "memories", "skills", "plugins", "cron", "hooks", "desktop-plugins",
    "tui-widgets", "skins", "pets", "scripts", "assets",
]
SKIP_NAMES = {
    ".env", "auth.json", "auth.lock", "gateway.lock", "gateway.pid",
    "gateway_state.json", "pairing", "logs", "cache", "audio_cache", "image_cache",
    "pending_messages", "processes.json", "ticker_heartbeat", "ticker_last_success",
    "index-cache", "scan-cache", "audit.log", ".curator_backups", "__pycache__", ".pytest_cache", ".git", "node_modules",
}
SECRET_KEY = re.compile(
    r"(?:^|[_-])(?:api[_-]?key|token|secret|password|credential|private[_-]?key|oauth|webhook)(?:$|[_-])",
    re.I,
)
SAFE_NON_SECRET_KEYS = {"redact_secrets"}
TOKEN_PATTERNS = [
    re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
    re.compile(r"\b[0-9]{8,12}:[A-Za-z0-9_-]{30,}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"https?://[^/\s]+/rest/\d+/[A-Za-z0-9_-]{8,}/?"),
    re.compile(r"\bAIza[A-Za-z0-9_-]{30,}\b"),
    re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"),
]
LOCAL_MODEL_MARKERS = (
    "ollama", "llama.cpp", "llamacpp", "lmstudio", "lm studio",
    "localhost", "127.0.0.1", "custom:local",
)
ARCHIVE_CHUNK_BYTES = 64 * 1024 * 1024
GITHUB_SAFE_BLOB_BYTES = 90 * 1024 * 1024


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def ignore(_dir: str, names: list[str]) -> set[str]:
    return {n for n in names if n in SKIP_NAMES or n.endswith((".pyc", ".pyo", ".tmp", ".lock", "-wal", "-shm"))}


def copy_item(src: Path, dst: Path) -> None:
    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=True, ignore=ignore)
    elif src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def sanitized_config(src: Path, dst: Path) -> None:
    import yaml
    data = yaml.safe_load(src.read_text(encoding="utf-8-sig")) or {}

    def scrub(value, key=""):
        if (
            SECRET_KEY.search(str(key))
            and str(key) not in SAFE_NON_SECRET_KEYS
            and value not in (None, "", False, 0)
        ):
            return "<SET_ON_TARGET>"
        if isinstance(value, dict):
            return {k: scrub(v, str(k)) for k, v in value.items()}
        if isinstance(value, list):
            return [scrub(v, key) for v in value]
        return value

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(yaml.safe_dump(scrub(data), allow_unicode=True, sort_keys=False), encoding="utf-8")


def profile_uses_local_model(config: Path) -> bool:
    if not config.exists():
        return False
    import yaml
    data = yaml.safe_load(config.read_text(encoding="utf-8-sig")) or {}
    model = data.get("model", {}) if isinstance(data.get("model", {}), dict) else {}
    evidence = " ".join(
        str(model.get(key, "")) for key in ("provider", "default", "base_url")
    ).lower()
    return any(marker in evidence for marker in LOCAL_MODEL_MARKERS)


def env_example(src: Path, dst: Path) -> None:
    out = ["# Generated from the source profile. Live secrets are intentionally excluded.\n"]
    for raw in src.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#") or "=" not in raw:
            out.append(raw + "\n")
            continue
        key, value = raw.split("=", 1)
        if SECRET_KEY.search(key):
            value = "<SET_ON_TARGET>" if value.strip() else ""
        out.append(f"{key}={value}\n")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("".join(out), encoding="utf-8")


def credential_values(home: Path) -> set[str]:
    roots = [home]
    profiles = home / "profiles"
    if profiles.exists():
        roots += [p for p in profiles.iterdir() if p.is_dir()]
    values: set[str] = set()
    for root in roots:
        env = root / ".env"
        if env.exists():
            for line in env.read_text(encoding="utf-8-sig", errors="ignore").splitlines():
                if not line.strip() or line.lstrip().startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                value = value.strip().strip("'\"")
                if SECRET_KEY.search(key) and len(value) >= 8:
                    values.add(value)
        auth = root / "auth.json"
        if auth.exists():
            try:
                data = json.loads(auth.read_text(encoding="utf-8-sig"))
            except Exception:
                continue
            def walk(value, key=""):
                if isinstance(value, dict):
                    for k, v in value.items():
                        walk(v, str(k))
                elif isinstance(value, list):
                    for v in value:
                        walk(v, key)
                elif isinstance(value, str) and SECRET_KEY.search(key) and len(value) >= 8:
                    values.add(value)
            walk(data)
    return values


def redact_database(db_path: Path, live_values: set[str]) -> int:
    """Redact live and credential-shaped strings in base TEXT columns.

    Updating the messages base table intentionally lets Hermes' FTS triggers
    update both search indexes, so the removed value is not retained there.
    """
    conn = sqlite3.connect(db_path)
    changed = 0
    try:
        tables = conn.execute(
            "SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()
        for table, sql in tables:
            if not sql or "VIRTUAL TABLE" in sql.upper() or table.startswith("messages_fts"):
                continue
            columns = [r[1] for r in conn.execute(f"PRAGMA table_info({json.dumps(table)})")]
            if not columns:
                continue
            rows = conn.execute(
                f"SELECT rowid, {', '.join(json.dumps(c) for c in columns)} FROM {json.dumps(table)}"
            ).fetchall()
            for row in rows:
                rowid, values = row[0], list(row[1:])
                updates = {}
                for idx, value in enumerate(values):
                    if not isinstance(value, str):
                        continue
                    new = value
                    for secret in live_values:
                        if secret in new:
                            new = new.replace(secret, "[REDACTED_LIVE_SECRET]")
                    for pattern in TOKEN_PATTERNS:
                        new = pattern.sub("[REDACTED_CREDENTIAL]", new)
                    if new != value:
                        updates[columns[idx]] = new
                if updates:
                    assignments = ", ".join(f"{json.dumps(k)}=?" for k in updates)
                    conn.execute(
                        f"UPDATE {json.dumps(table)} SET {assignments} WHERE rowid=?",
                        [*updates.values(), rowid],
                    )
                    changed += 1
        conn.commit()
        # Rebuild external-content FTS indexes so removed strings cannot remain
        # in index segments, then VACUUM to discard freed SQLite pages.
        virtual_tables = {name for name, sql in tables if sql and "VIRTUAL TABLE" in sql.upper()}
        for fts in ("messages_fts", "messages_fts_trigram"):
            if fts in virtual_tables:
                conn.execute(f"INSERT INTO {fts}({fts}) VALUES('rebuild')")
        conn.commit()
        conn.execute("VACUUM")
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    finally:
        conn.close()
    return changed


def snapshot_db(src: Path, gz_dst: Path, live_values: set[str]) -> dict:
    gz_dst.parent.mkdir(parents=True, exist_ok=True)
    plain = gz_dst.with_suffix("")
    if plain.exists():
        plain.unlink()
    source = sqlite3.connect(f"file:{src.as_posix()}?mode=ro", uri=True)
    target = sqlite3.connect(plain)
    try:
        source.backup(target)
        integrity = target.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise RuntimeError(f"SQLite integrity check failed for {src}: {integrity}")
    finally:
        target.close()
        source.close()
    redacted_rows = redact_database(plain, live_values)
    check = sqlite3.connect(plain)
    try:
        integrity = check.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise RuntimeError(f"SQLite integrity check failed after redaction for {src}: {integrity}")
    finally:
        check.close()
    raw_hash = sha256(plain)
    raw_size = plain.stat().st_size
    with plain.open("rb") as f_in, gz_dst.open("wb") as raw_out:
        with gzip.GzipFile(filename="state.db", mode="wb", fileobj=raw_out, compresslevel=9, mtime=0) as f_out:
            shutil.copyfileobj(f_in, f_out, 1024 * 1024)
    plain.unlink()
    archive_size = gz_dst.stat().st_size
    archive_hash = sha256(gz_dst)
    archive_parts = []
    if archive_size >= GITHUB_SAFE_BLOB_BYTES:
        with gz_dst.open("rb") as source:
            index = 1
            while chunk := source.read(ARCHIVE_CHUNK_BYTES):
                part = gz_dst.with_name(f"{gz_dst.name}.part{index:03d}")
                part.write_bytes(chunk)
                archive_parts.append({
                    "name": part.name,
                    "bytes": part.stat().st_size,
                    "sha256": sha256(part),
                })
                index += 1
        gz_dst.unlink()
    return {
        "source": str(src), "raw_bytes": raw_size, "raw_sha256": raw_hash,
        "archive_bytes": archive_size, "archive_sha256": archive_hash,
        "archive_parts": archive_parts,
        "integrity": "ok", "redacted_rows": redacted_rows,
    }


def git_output(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def capture_source_overlay(home: Path, out: Path) -> dict:
    source = home / "hermes-agent"
    meta = {"version": subprocess.check_output(["hermes", "--version"], text=True).splitlines()[0].strip()}
    if not (source / ".git").exists():
        return meta
    meta.update({
        "repository": git_output(source, "remote", "get-url", "origin"),
        "commit": git_output(source, "rev-parse", "HEAD"),
        "describe": git_output(source, "describe", "--tags", "--always", "--dirty"),
    })
    patch = subprocess.check_output(["git", "-C", str(source), "diff", "--binary", "--", ":!bin"], text=False)
    if patch:
        (out / "source").mkdir(parents=True, exist_ok=True)
        (out / "source" / "local-changes.patch").write_bytes(patch)
    untracked = git_output(source, "ls-files", "--others", "--exclude-standard").splitlines()
    copied = []
    for rel in untracked:
        if rel == "bin" or rel.startswith("bin/"):
            continue
        src = source / rel
        if src.is_file():
            dst = out / "source" / "untracked" / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied.append(rel)
    meta["untracked_source_files"] = copied
    return meta


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hermes-home", default=os.environ.get("HERMES_HOME"))
    ap.add_argument("--output", required=True)
    ap.add_argument(
        "--exclude-profile", action="append", default=[],
        help="Named profile to exclude; may be repeated",
    )
    args = ap.parse_args()
    home = Path(args.hermes_home).resolve()
    out = Path(args.output).resolve()
    payload = out / "snapshot"
    if payload.exists():
        shutil.rmtree(payload)
    payload.mkdir(parents=True)
    source_payload = out / "source"
    if source_payload.exists():
        shutil.rmtree(source_payload)

    candidates = [("default", home)]
    profiles_root = home / "profiles"
    if profiles_root.exists():
        candidates += sorted((p.name, p) for p in profiles_root.iterdir() if p.is_dir())

    denylist = set(args.exclude_profile)
    profiles = []
    excluded_profiles = {}
    for name, profile_home in candidates:
        if name in denylist:
            excluded_profiles[name] = "explicitly excluded"
        elif profile_uses_local_model(profile_home / "config.yaml"):
            excluded_profiles[name] = "local model/provider configuration"
        else:
            profiles.append((name, profile_home))

    live_values = credential_values(home)
    manifest = {
        "format": 2,
        "profiles": {},
        "excluded_profiles": excluded_profiles,
        "source_environment": {
            "hermes_home": str(home),
            "user_home": str(Path.home()),
            "platform": os.name,
        },
        "source": capture_source_overlay(home, out),
    }
    for name, src_root in profiles:
        dst_root = payload / ("default" if name == "default" else f"profiles/{name}")
        dst_root.mkdir(parents=True, exist_ok=True)
        for item in PROFILE_ITEMS:
            src = src_root / item
            if not src.exists():
                continue
            if item == "config.yaml":
                sanitized_config(src, dst_root / item)
            else:
                copy_item(src, dst_root / item)
        if (src_root / ".env").exists():
            env_example(src_root / ".env", dst_root / ".env.example")
        db_info = None
        if (src_root / "state.db").exists():
            db_info = snapshot_db(src_root / "state.db", dst_root / "state.db.gz", live_values)
        manifest["profiles"][name] = {"database": db_info}

    files = []
    integrity_roots = [payload]
    if source_payload.exists():
        integrity_roots.append(source_payload)
    for integrity_root in integrity_roots:
        for p in sorted(integrity_root.rglob("*")):
            if p.is_file():
                files.append({"path": p.relative_to(out).as_posix(), "bytes": p.stat().st_size, "sha256": sha256(p)})
    manifest["files"] = files
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "profiles": list(manifest["profiles"]),
        "excluded_profiles": excluded_profiles,
        "files": len(files),
        "bytes": sum(f["bytes"] for f in files),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
