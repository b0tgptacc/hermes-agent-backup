#!/usr/bin/env python
"""Coverage-aware local OCR for image files and PDFs.

Native PDF text is preserved when reliable; only empty/weak pages are OCR'd
unless --force-ocr is supplied. Output contains page refs, word boxes,
confidence, extraction method and exact coverage accounting.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def find_tesseract() -> str | None:
    found = shutil.which("tesseract")
    if found:
        return found
    candidates = [
        Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Tesseract-OCR/tesseract.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/Tesseract-OCR/tesseract.exe",
    ]
    for p in candidates:
        if p.is_file():
            return str(p)
    return None


def tesseract_languages(exe: str, tessdata_dir: str | None = None) -> list[str]:
    cmd = [exe]
    if tessdata_dir:
        cmd += ["--tessdata-dir", tessdata_dir]
    cmd += ["--list-langs"]
    cp = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
    if cp.returncode:
        raise RuntimeError(cp.stderr.strip() or "tesseract --list-langs failed")
    return sorted(line.strip() for line in cp.stdout.splitlines()[1:] if line.strip())


def choose_languages(requested: str, available: list[str]) -> tuple[str, list[str]]:
    wanted = [x for x in requested.split("+") if x]
    selected = [x for x in wanted if x in available]
    warnings: list[str] = []
    missing = [x for x in wanted if x not in available]
    if missing:
        warnings.append("OCR language packs unavailable: " + ", ".join(missing))
    if not selected:
        if "eng" in available:
            selected = ["eng"]
        elif available:
            selected = [available[0]]
        else:
            raise RuntimeError("No Tesseract language packs are available")
    return "+".join(selected), warnings


def preprocess(image: Any) -> Any:
    from PIL import ImageOps

    image = ImageOps.exif_transpose(image).convert("RGB")
    gray = ImageOps.grayscale(image)
    return ImageOps.autocontrast(gray, cutoff=1)


def ocr_image(image: Any, page_no: int, lang: str, exe: str, tessdata_dir: str | None, psm: int) -> dict:
    import pytesseract
    from pytesseract import Output

    pytesseract.pytesseract.tesseract_cmd = exe
    image = preprocess(image)
    config_parts = [f"--psm {psm}"]
    old_tessdata = os.environ.get("TESSDATA_PREFIX")
    if tessdata_dir:
        os.environ["TESSDATA_PREFIX"] = tessdata_dir
    try:
        data = pytesseract.image_to_data(image, lang=lang, config=" ".join(config_parts), output_type=Output.DICT)
    finally:
        if tessdata_dir:
            if old_tessdata is None:
                os.environ.pop("TESSDATA_PREFIX", None)
            else:
                os.environ["TESSDATA_PREFIX"] = old_tessdata
    words = []
    confidences = []
    for i, raw in enumerate(data.get("text", [])):
        text = (raw or "").strip()
        try:
            conf = float(data["conf"][i])
        except (ValueError, TypeError, KeyError):
            conf = -1.0
        if not text:
            continue
        if conf >= 0:
            confidences.append(conf)
        words.append({
            "ref": f"page:{page_no}!word:{len(words)+1}",
            "text": text,
            "bbox": [int(data["left"][i]), int(data["top"][i]), int(data["width"][i]), int(data["height"][i])],
            "confidence": conf if conf >= 0 else None,
        })
    text = " ".join(w["text"] for w in words)
    mean = round(sum(confidences) / len(confidences), 2) if confidences else None
    return {
        "ref": f"page:{page_no}",
        "method": "ocr",
        "width_px": image.width,
        "height_px": image.height,
        "text": text,
        "words": words,
        "mean_confidence": mean,
    }


def extract_pdf(path: Path, args: argparse.Namespace, lang: str, exe: str) -> tuple[list[dict], list[str]]:
    import fitz
    from PIL import Image

    pages: list[dict] = []
    warnings: list[str] = []
    doc = fitz.open(path)
    scale = args.dpi / 72.0
    for idx, page in enumerate(doc, 1):
        native_words = page.get_text("words")
        native_text = page.get_text("text").strip()
        if not args.force_ocr and len(native_text) >= args.min_native_chars:
            words = []
            for n, w in enumerate(native_words, 1):
                words.append({
                    "ref": f"page:{idx}!word:{n}",
                    "text": str(w[4]),
                    "bbox": [round(float(w[0]), 2), round(float(w[1]), 2), round(float(w[2]), 2), round(float(w[3]), 2)],
                    "confidence": None,
                })
            pages.append({"ref": f"page:{idx}", "method": "native", "text": native_text, "words": words, "mean_confidence": None})
            continue
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        pages.append(ocr_image(image, idx, lang, exe, args.tessdata_dir, args.psm))
    doc.close()
    return pages, warnings


def extract_images(path: Path, args: argparse.Namespace, lang: str, exe: str) -> tuple[list[dict], list[str]]:
    from PIL import Image, ImageSequence

    pages: list[dict] = []
    warnings: list[str] = []
    with Image.open(path) as im:
        for idx, frame in enumerate(ImageSequence.Iterator(im), 1):
            if frame.width * frame.height > args.max_pixels:
                raise ValueError(f"Page {idx} exceeds --max-pixels={args.max_pixels}")
            pages.append(ocr_image(frame.copy(), idx, lang, exe, args.tessdata_dir, args.psm))
    return pages, warnings


def dependency_check(tessdata_dir: str | None) -> dict:
    checks: dict[str, Any] = {"python": sys.version.split()[0]}
    for module in ("PIL", "pytesseract", "fitz"):
        try:
            mod = __import__(module)
            checks[module] = getattr(mod, "__version__", "available")
        except Exception as exc:
            checks[module] = f"MISSING: {exc}"
    exe = find_tesseract()
    checks["tesseract_executable"] = exe
    if exe:
        try:
            cp = subprocess.run([exe, "--version"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
            checks["tesseract_version"] = (cp.stdout or cp.stderr).splitlines()[0]
            checks["languages"] = tesseract_languages(exe, tessdata_dir)
        except Exception as exc:
            checks["tesseract_error"] = str(exc)
    checks["ready"] = bool(exe and isinstance(checks.get("languages"), list) and checks["languages"])
    return checks


def default_tessdata() -> str | None:
    configured = os.environ.get("ASTRADOCS_TESSDATA")
    if configured:
        return configured
    profile_local = Path(__file__).resolve().parents[4] / "runtime" / "tessdata"
    return str(profile_local) if profile_local.is_dir() else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?")
    ap.add_argument("-o", "--output")
    ap.add_argument("--lang", default="rus+eng")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--psm", type=int, default=6)
    ap.add_argument("--min-confidence", type=float, default=70.0)
    ap.add_argument("--min-native-chars", type=int, default=20)
    ap.add_argument("--force-ocr", action="store_true")
    ap.add_argument("--max-pixels", type=int, default=120_000_000)
    ap.add_argument("--tessdata-dir", default=default_tessdata())
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.check:
        print(json.dumps(dependency_check(args.tessdata_dir), ensure_ascii=False, indent=2))
        return 0 if dependency_check(args.tessdata_dir).get("ready") else 2
    if not args.path:
        ap.error("path is required unless --check is used")

    path = Path(args.path)
    if not path.is_file():
        print(json.dumps({"status": "BLOCKED", "error": f"File not found: {path}"}, ensure_ascii=False), file=sys.stderr)
        return 2
    exe = find_tesseract()
    if not exe:
        print(json.dumps({"status": "BLOCKED", "error": "Tesseract executable not found"}, ensure_ascii=False), file=sys.stderr)
        return 2
    try:
        available = tesseract_languages(exe, args.tessdata_dir)
        lang, warnings = choose_languages(args.lang, available)
        ext = path.suffix.lower()
        if ext == ".pdf":
            pages, more = extract_pdf(path, args, lang, exe)
        elif ext in IMAGE_EXTS:
            pages, more = extract_images(path, args, lang, exe)
        else:
            raise ValueError(f"Unsupported OCR input format: {ext}")
        warnings.extend(more)
        low = [p["ref"] for p in pages if p["method"] == "ocr" and (p["mean_confidence"] is None or p["mean_confidence"] < args.min_confidence)]
        empty = [p["ref"] for p in pages if not p["text"].strip()]
        status = "PASS"
        if low or empty or any("unavailable" in x.lower() for x in warnings):
            status = "PARTIAL"
        if low:
            warnings.append("Low-confidence OCR pages require visual review: " + ", ".join(low))
        if empty:
            warnings.append("Pages with no extracted text: " + ", ".join(empty))
        result = {
            "schema_version": 1,
            "source": str(path.resolve()),
            "size_bytes": path.stat().st_size,
            "sha256": sha256(path),
            "status": status,
            "language_requested": args.lang,
            "language_used": lang,
            "warnings": warnings,
            "coverage": {
                "expected_pages": len(pages),
                "native_extracted": sum(p["method"] == "native" for p in pages),
                "ocr_extracted": sum(p["method"] == "ocr" and bool(p["text"].strip()) for p in pages),
                "failed": len(empty),
                "accounted": len(pages),
                "complete": len(pages) == sum(p["method"] == "native" for p in pages) + sum(p["method"] == "ocr" for p in pages),
            },
            "pages": pages,
        }
    except Exception as exc:
        result = {"status": "BLOCKED", "source": str(path.resolve()), "error": f"{type(exc).__name__}: {exc}"}
        text = json.dumps(result, ensure_ascii=False, indent=2)
        print(text, file=sys.stderr)
        if args.output:
            Path(args.output).write_text(text, encoding="utf-8")
        return 1

    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(text, encoding="utf-8")
        print(json.dumps({"status": result["status"], "output": str(Path(args.output).resolve()), "coverage": result["coverage"], "warnings": result["warnings"]}, ensure_ascii=False))
    else:
        print(text)
    return 0 if result["status"] == "PASS" else 3


if __name__ == "__main__":
    raise SystemExit(main())
