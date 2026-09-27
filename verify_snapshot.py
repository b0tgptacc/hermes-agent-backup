#!/usr/bin/env python
from __future__ import annotations

import gzip
import hashlib
import json
import shutil
import sqlite3
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def payload_files() -> set[str]:
    actual = set()
    for root_name in ("snapshot", "source"):
        root = ROOT / root_name
        if root.exists():
            actual.update(path.relative_to(ROOT).as_posix() for path in root.rglob("*") if path.is_file())
    return actual


def database_archive(profile: str, info: dict, temp: Path) -> Path:
    relative = "default" if profile == "default" else f"profiles/{profile}"
    profile_root = ROOT / "snapshot" / relative
    parts = info.get("archive_parts") or []
    if not parts:
        return profile_root / "state.db.gz"
    archive = temp / f"{profile}-state.db.gz"
    with archive.open("wb") as output:
        for part in parts:
            path = profile_root / part["name"]
            if path.stat().st_size != part["bytes"] or digest(path) != part["sha256"]:
                raise RuntimeError(f"Database archive part mismatch: {path}")
            with path.open("rb") as source:
                shutil.copyfileobj(source, output)
    if archive.stat().st_size != info["archive_bytes"] or digest(archive) != info["archive_sha256"]:
        raise RuntimeError(f"Combined database archive mismatch: {profile}")
    return archive


def main() -> None:
    entries = MANIFEST["files"]
    declared = [item["path"] for item in entries]
    if len(declared) != len(set(declared)):
        raise RuntimeError("Manifest contains duplicate paths")
    declared_set = set(declared)
    actual_set = payload_files()
    missing = sorted(declared_set - actual_set)
    extra = sorted(actual_set - declared_set)
    if missing or extra:
        raise RuntimeError(f"Payload/manifest mismatch; missing={missing}, extra={extra}")

    for item in entries:
        path = ROOT / item["path"]
        if path.stat().st_size != item["bytes"]:
            raise RuntimeError(f"Size mismatch: {item['path']}")
        if digest(path) != item["sha256"]:
            raise RuntimeError(f"SHA-256 mismatch: {item['path']}")

    for profile, profile_info in MANIFEST["profiles"].items():
        info = profile_info.get("database")
        if not info:
            continue
        with tempfile.TemporaryDirectory() as directory:
            archive = database_archive(profile, info, Path(directory))
            database_path = Path(directory) / "state.db"
            with gzip.open(archive, "rb") as source, database_path.open("wb") as output:
                shutil.copyfileobj(source, output, 1024 * 1024)
            database = sqlite3.connect(database_path)
            try:
                integrity = database.execute("PRAGMA integrity_check").fetchone()[0]
            finally:
                database.close()
            if integrity != "ok":
                raise RuntimeError(f"SQLite integrity failed: {profile}: {integrity}")
    print(f"VERIFY_OK files={len(entries)} profiles={len(MANIFEST['profiles'])}")


if __name__ == "__main__":
    main()
