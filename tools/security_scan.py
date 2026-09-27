#!/usr/bin/env python
"""Fail closed if current live credentials leak into the snapshot."""
from __future__ import annotations
import argparse, gzip, json, os, re, shutil, tempfile
from pathlib import Path

PATTERNS = [
    re.compile(rb"gh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(rb"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(rb"xox[baprs]-[A-Za-z0-9-]{20,}"),
    re.compile(rb"\b[0-9]{8,12}:[A-Za-z0-9_-]{30,}\b"),
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"https?://[^/\s]+/rest/\d+/[A-Za-z0-9_-]{8,}/?"),
    re.compile(rb"\bAIza[A-Za-z0-9_-]{30,}\b"),
    re.compile(rb"\bAKIA[A-Z0-9]{16}\b"),
    re.compile(rb"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"),
]
SENSITIVE_KEY = re.compile(
    r"(?:^|[_-])(?:api[_-]?key|token|secret|password|credential|private[_-]?key|oauth|webhook)(?:$|[_-])",
    re.I,
)


def credential_values(home: Path) -> set[bytes]:
    roots = [home]
    profiles = home / "profiles"
    if profiles.exists():
        roots += [p for p in profiles.iterdir() if p.is_dir()]
    values: set[bytes] = set()
    for root in roots:
        env = root / ".env"
        if env.exists():
            for line in env.read_text(encoding="utf-8-sig", errors="ignore").splitlines():
                if not line.strip() or line.lstrip().startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                value = value.strip().strip("'\"")
                if SENSITIVE_KEY.search(key) and len(value) >= 8:
                    values.add(value.encode())
        auth = root / "auth.json"
        if auth.exists():
            try:
                data = json.loads(auth.read_text(encoding="utf-8-sig"))
            except Exception:
                continue
            def walk(v, key=""):
                if isinstance(v, dict):
                    for k, x in v.items(): walk(x, str(k))
                elif isinstance(v, list):
                    for x in v: walk(x, key)
                elif isinstance(v, str) and SENSITIVE_KEY.search(key) and len(v) >= 8:
                    values.add(v.encode())
            walk(data)
    return values


def data_for(path: Path) -> bytes:
    if path.name.endswith(".gz"):
        with gzip.open(path, "rb") as f:
            return f.read()
    return path.read_bytes()


def scan_stream(stream, secrets: set[bytes]) -> tuple[int, int]:
    exact = pattern = 0
    carry = b""
    while chunk := stream.read(1024 * 1024):
        data = carry + chunk
        exact += sum(data.count(value) for value in secrets)
        pattern += sum(len(rx.findall(data)) for rx in PATTERNS)
        carry = data[-1024:]
    return exact, pattern


def scan_databases(repo: Path, secrets: set[bytes]) -> list[dict]:
    manifest = json.loads((repo / "manifest.json").read_text(encoding="utf-8"))
    findings = []
    for profile, profile_info in manifest.get("profiles", {}).items():
        info = profile_info.get("database")
        if not info:
            continue
        relative = "default" if profile == "default" else f"profiles/{profile}"
        root = repo / "snapshot" / relative
        parts = info.get("archive_parts") or []
        archives = [root / "state.db.gz"] if not parts else [root / part["name"] for part in parts]
        with tempfile.NamedTemporaryFile(suffix=".gz", delete=False) as combined:
            combined_path = Path(combined.name)
            for archive in archives:
                with archive.open("rb") as source:
                    shutil.copyfileobj(source, combined)
        try:
            with gzip.open(combined_path, "rb") as stream:
                exact, pattern = scan_stream(stream, secrets)
        finally:
            combined_path.unlink(missing_ok=True)
        if exact or pattern:
            findings.append({
                "path": f"snapshot/{relative}/state.db",
                "exact_live_secret_matches": exact,
                "credential_pattern_matches": pattern,
            })
    return findings


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--hermes-home", default=os.environ.get("HERMES_HOME"))
    args = ap.parse_args()
    repo, home = Path(args.repo).resolve(), Path(args.hermes_home).resolve()
    secrets = credential_values(home)
    findings = []
    max_file = ("", 0)
    for p in repo.rglob("*"):
        if not p.is_file() or ".git" in p.parts:
            continue
        size = p.stat().st_size
        if size > max_file[1]: max_file = (p.relative_to(repo).as_posix(), size)
        if p.name in {"security_scan.py"} or p.name.startswith("state.db.gz"):
            continue
        try: data = data_for(p)
        except Exception: continue
        exact = sum(1 for value in secrets if value in data)
        pattern = sum(len(rx.findall(data)) for rx in PATTERNS)
        critical_pattern = pattern if p.name.endswith("state.db.gz") or p.name in {"config.yaml", ".env.example"} else 0
        if exact or critical_pattern:
            findings.append({"path": p.relative_to(repo).as_posix(), "exact_live_secret_matches": exact, "credential_pattern_matches": pattern})
    findings.extend(scan_databases(repo, secrets))
    report = {"live_secret_values_checked": len(secrets), "findings": findings, "largest_file": {"path": max_file[0], "bytes": max_file[1]}, "github_100mb_limit_ok": max_file[1] < 100_000_000}
    print(json.dumps(report, indent=2))
    if findings or max_file[1] >= 100_000_000:
        raise SystemExit(2)

if __name__ == "__main__":
    main()
