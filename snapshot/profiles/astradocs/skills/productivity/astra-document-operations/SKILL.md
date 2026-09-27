---
name: astra-document-operations
description: "Use for end-to-end documents and OCR with GPT-6 Astra."
version: 1.0.0
author: MASTER
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [astra, documents, ocr, pdf, office, provenance, verification]
    category: productivity
    related_skills: [document-intelligence-pipelines, ocr-and-documents, docx, pdf, powerpoint, xlsx]
---

# Astra Document Operations

Оркестрирует проверяемую работу GPT-6 Astra с бизнес-документами всех практических типов. Skill не заменяет форматные skills; он выбирает маршрут, контролирует покрытие и объединяет результаты.

## Маршрутизация

| Вход | Первичный маршрут | Дополнительная проверка |
|---|---|---|
| DOCX/DOCM | `docx` + OOXML inventory | revisions/comments/text boxes/media |
| XLSX/XLSM | `xlsx` + formula/cache separation | hidden sheets, names, tables, charts |
| PPTX/PPTM | `powerpoint` | notes, hidden slides, SmartArt, images |
| Born-digital PDF | `pdf_read.py --meta/--text` | page count + page-level coverage |
| Scan PDF, PNG/JPEG/TIFF/BMP/WEBP | `scripts/ocr_extract.py` | Astra vision for low confidence/layout |
| DOC/XLS/PPT/ODT/ODS/ODP | LibreOffice copy-convert | process converted artifact again |
| CSV/TSV/JSON/XML/YAML/HTML/TXT/MD/RTF/EPUB | `read_file`/format parser | encoding, row/node counts, no type coercion |
| ZIP/OOXML/archive | inventory with size/ratio limits | never execute contents |
| Unknown | inspect signature; try `read_file`/anydoc | `BLOCKED` if reliable parser unavailable |

## Workflow

1. Preserve source; record absolute path, byte size and SHA-256.
2. Identify magic/container and inventory structural units.
3. Use a deterministic parser before Astra analysis.
4. For PDF, OCR only pages lacking reliable native text. For images, OCR at source resolution or 300 DPI equivalent.
5. Store canonical records with `ref`, method (`native|ocr|vlm`), text/value, bbox where available, confidence and warnings.
6. Validate coverage exactly. Missing or unsupported material cannot disappear from accounting.
7. Analyze only relevant records and cite coordinates.
8. Independently recalculate critical totals and dates.
9. When creating/editing, write a new artifact, read it back, run package validation and render-review visual output.
10. Report PASS/PARTIAL/BLOCKED.

## Local OCR and conversion

```bash
python scripts/ocr_extract.py input.pdf -o output.ocr.json --lang rus+eng --dpi 300
python scripts/ocr_extract.py scan.png -o output.ocr.json --lang rus+eng
python scripts/ocr_extract.py input.pdf -o output.ocr.json --force-ocr
python scripts/office_convert.py legacy.doc --to docx --outdir converted
python scripts/office_convert.py report.odt --to pdf --outdir converted
```

`office_convert.py` discovers LibreOffice on Windows even when `soffice` is not yet present in the current process PATH, always writes to a separate output directory, and verifies that the converted artifact exists.

The OCR script uses native PDF text first and Tesseract for scanned/empty pages. It returns page text, word boxes, confidence, language actually used, coverage and warnings. Confidence below the threshold is `PARTIAL`, not a guessed success.

## Astra-specific practice

- Audit active skills: Astra follows file instructions strongly, so remove conflicting/duplicate guidance.
- Keep a stable system prefix for prompt caching.
- Default to `high` reasoning. Escalate only for difficult review; do not use max reasoning for routine extraction.
- Avoid pushing whole binary packages or hundreds of thousands of raw tokens into context. Build an index and retrieve cited fragments.
- Inputs above 272K tokens have a pricing multiplier. The 1.05M context is available for exceptional cross-document synthesis, not routine extraction.
- Use image input for diagrams, layout and OCR verification; cite image/page crop and keep probabilistic findings marked.

## Fail-closed rules

- `PASS`: all required structural units accounted for and critical claims verified.
- `PARTIAL`: useful output exists but confidence, formula cache, unsupported objects or visual semantics remain incomplete.
- `BLOCKED`: corruption, encryption without password, failed pages, unknown format, unavailable parser/OCR, or material ambiguity.

Never claim universal perfect OCR. The target is no silent omission: uncertainty is visible and blocks unsupported conclusions.
