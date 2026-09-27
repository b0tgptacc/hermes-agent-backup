#!/usr/bin/env python
"""Safe LibreOffice copy-conversion with Windows path discovery."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path


def find_soffice() -> str | None:
    found = shutil.which("soffice") or shutil.which("libreoffice")
    if found:
        return found
    candidates = [
        Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "LibreOffice/program/soffice.exe",
        Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")) / "LibreOffice/program/soffice.exe",
    ]
    for p in candidates:
        if p.is_file():
            return str(p)
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", nargs="?")
    ap.add_argument("--to", default="pdf", help="LibreOffice output extension/filter, e.g. pdf, docx, xlsx, pptx")
    ap.add_argument("--outdir")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    exe = find_soffice()
    if args.check:
        print(json.dumps({"soffice": exe, "ready": bool(exe)}, ensure_ascii=False))
        return 0 if exe else 2
    if not args.input:
        ap.error("input is required unless --check is used")
    src = Path(args.input).resolve()
    if not src.is_file():
        print(json.dumps({"status": "BLOCKED", "error": f"File not found: {src}"}, ensure_ascii=False))
        return 2
    if not exe:
        print(json.dumps({"status": "BLOCKED", "error": "LibreOffice soffice not found"}, ensure_ascii=False))
        return 2
    outdir = Path(args.outdir).resolve() if args.outdir else src.parent / "converted"
    outdir.mkdir(parents=True, exist_ok=True)
    child_env = os.environ.copy()
    child_env.pop("PYTHONHOME", None)
    child_env.pop("PYTHONPATH", None)
    cp = subprocess.run([exe, "--headless", "--convert-to", args.to, "--outdir", str(outdir), str(src)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300, env=child_env)
    expected = outdir / f"{src.stem}.{args.to.split(':', 1)[0]}"
    result = {
        "status": "PASS" if cp.returncode == 0 and expected.is_file() else "BLOCKED",
        "source": str(src),
        "output": str(expected),
        "source_preserved": src.is_file(),
        "returncode": cp.returncode,
        "stdout": cp.stdout.strip(),
        "stderr": cp.stderr.strip(),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
