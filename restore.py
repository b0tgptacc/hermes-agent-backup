#!/usr/bin/env python
"""Restore the portable Hermes snapshot into HERMES_HOME."""
from __future__ import annotations

import argparse
import datetime as dt
import gzip
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import tempfile
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def target_home(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    if os.environ.get("HERMES_HOME"):
        return Path(os.environ["HERMES_HOME"]).resolve()
    if os.name == "nt":
        return Path(os.environ["LOCALAPPDATA"]) / "hermes"
    return Path.home() / ".hermes"


def verify(repo: Path, manifest: dict) -> None:
    errors = []
    declared = [item["path"] for item in manifest["files"]]
    if len(declared) != len(set(declared)):
        errors.append("manifest contains duplicate paths")
    declared_set = set(declared)
    actual_set = set()
    for root_name in ("snapshot", "source"):
        root = repo / root_name
        if root.exists():
            actual_set.update(path.relative_to(repo).as_posix() for path in root.rglob("*") if path.is_file())
    for path in sorted(declared_set - actual_set):
        errors.append(f"missing: {path}")
    for path in sorted(actual_set - declared_set):
        errors.append(f"undeclared payload file: {path}")
    for item in manifest["files"]:
        path = repo / item["path"]
        if not path.is_file():
            continue
        if path.stat().st_size != item["bytes"] or sha256(path) != item["sha256"]:
            errors.append(f"checksum mismatch: {item['path']}")
    if errors:
        raise SystemExit("Snapshot verification failed:\n" + "\n".join(errors))


def copy_profile(src: Path, dst: Path, backup: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if item.name == "state.db.gz" or item.name.startswith("state.db.gz.part"):
            continue
        if item.name == ".env.example":
            shutil.copy2(item, dst / ".env.restore-example")
            continue
        target = dst / item.name
        if target.exists():
            saved = backup / item.name
            saved.parent.mkdir(parents=True, exist_ok=True)
            if target.is_dir():
                shutil.copytree(target, saved, dirs_exist_ok=True)
                shutil.rmtree(target)
            else:
                shutil.copy2(target, saved)
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)
    archives = [src / "state.db.gz"] if (src / "state.db.gz").exists() else sorted(src.glob("state.db.gz.part*"))
    if archives:
        target_db = dst / "state.db"
        if target_db.exists():
            saved = backup / "state.db"
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target_db, saved)
        with tempfile.NamedTemporaryFile(suffix=".gz", delete=False) as combined:
            combined_path = Path(combined.name)
            for archive in archives:
                with archive.open("rb") as part:
                    shutil.copyfileobj(part, combined, 1024 * 1024)
        try:
            with gzip.open(combined_path, "rb") as f_in, target_db.open("wb") as f_out:
                shutil.copyfileobj(f_in, f_out, 1024 * 1024)
        finally:
            combined_path.unlink(missing_ok=True)
        conn = sqlite3.connect(target_db)
        try:
            integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        finally:
            conn.close()
        if integrity != "ok":
            raise RuntimeError(f"Restored database is invalid: {target_db}: {integrity}")


def rewrite_config_paths(config: Path, replacements: list[tuple[str, str]]) -> None:
    if not config.exists():
        return
    text = config.read_text(encoding="utf-8-sig")
    for source, target in replacements:
        for candidate in {source, source.replace("\\", "/")}:
            text = text.replace(candidate, target)
    config.write_text(text, encoding="utf-8")


def restore_source(repo: Path, home: Path, manifest: dict, backup: Path) -> None:
    meta = manifest.get("source", {})
    commit = meta.get("commit")
    source = home / "hermes-agent"
    if not commit:
        print("Source metadata has no Git commit; source restore skipped.")
        return
    if not (source / ".git").exists():
        raise SystemExit("Hermes source is absent. Install Hermes first, then rerun with --restore-source.")
    subprocess.run(["git", "-C", str(source), "fetch", "origin", commit], check=True)
    subprocess.run(["git", "-C", str(source), "checkout", "--detach", commit], check=True)
    patch = repo / "source" / "local-changes.patch"
    if patch.exists():
        check = subprocess.run(
            ["git", "-C", str(source), "apply", "--check", str(patch)],
            capture_output=True,
        )
        if check.returncode == 0:
            subprocess.run(["git", "-C", str(source), "apply", str(patch)], check=True)
        else:
            reverse = subprocess.run(
                ["git", "-C", str(source), "apply", "--reverse", "--check", str(patch)],
                capture_output=True,
            )
            if reverse.returncode != 0:
                raise SystemExit("Source patch neither applies cleanly nor is already applied; source restore stopped.")
    untracked = repo / "source" / "untracked"
    if untracked.exists():
        for p in untracked.rglob("*"):
            if p.is_file():
                dst = source / p.relative_to(untracked)
                dst.parent.mkdir(parents=True, exist_ok=True)
                if dst.exists() and sha256(dst) != sha256(p):
                    saved = backup / "source-overlay" / p.relative_to(untracked)
                    saved.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(dst, saved)
                shutil.copy2(p, dst)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", help="Hermes home; defaults to HERMES_HOME/platform default")
    ap.add_argument("--restore-source", action="store_true", help="Pin source commit and apply local source overlay")
    ap.add_argument("--force", action="store_true", help="Required when restoring into a non-empty Hermes home")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parent
    manifest = json.loads((repo / "manifest.json").read_text(encoding="utf-8"))
    verify(repo, manifest)
    home = target_home(args.target)
    if home.exists() and any(home.iterdir()) and not args.force:
        raise SystemExit(f"Target is non-empty: {home}\nStop Hermes and rerun with --force; existing profile data will be backed up.")
    home.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = home.parent / f"hermes-pre-restore-{stamp}"

    copy_profile(repo / "snapshot" / "default", home, backup / "default")
    profiles = repo / "snapshot" / "profiles"
    if profiles.exists():
        for src in sorted(p for p in profiles.iterdir() if p.is_dir()):
            copy_profile(src, home / "profiles" / src.name, backup / "profiles" / src.name)
    environment = manifest.get("source_environment", {})
    source_hermes = environment.get("hermes_home", "")
    source_user = environment.get("user_home", "")
    replacements = sorted(
        [
            (source_hermes, home.as_posix()),
            (source_user, Path.home().as_posix()),
        ],
        key=lambda pair: len(pair[0]),
        reverse=True,
    )
    replacements = [pair for pair in replacements if pair[0]]
    rewrite_config_paths(home / "config.yaml", replacements)
    for profile_home in (home / "profiles").iterdir() if (home / "profiles").exists() else []:
        if profile_home.is_dir():
            rewrite_config_paths(profile_home / "config.yaml", replacements)
    if args.restore_source:
        restore_source(repo, home, manifest, backup)
    print(f"RESTORE_OK target={home}")
    print(f"Previous files backup={backup}")
    print("Secrets were not restored. Configure .env/auth on this device, then run: hermes doctor")


if __name__ == "__main__":
    main()
