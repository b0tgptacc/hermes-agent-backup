ПРОФИЛЬ: astradocs

Назначение:
  Senior fullstack-разработка на GPT-6 Astra: backend, frontend, product UI/UX,
  TDD, debugging, security review, GitHub delivery, Context7 и Playwright QA.
  Профиль также сохраняет полный документальный контур: OCR, анализ, перевод,
  создание и редактирование DOCX/XLSX/PPTX/PDF, сканов, изображений, legacy
  Office, ODF, RTF, EPUB и структурированных данных.

Запуск:
  hermes -p astradocs

Ключевые свойства:
  - модель: gpt-6-astra через отдельный OpenAI Codex OAuth профиля;
  - контекст: 1 050 000, operational output cap: 32 768;
  - reasoning: high;
  - Context7 MCP: актуальная version-aware документация библиотек и API;
  - Playwright MCP 0.0.82: изолированный headless Chrome, 21/25 tools;
  - unsafe Playwright tools evaluate/upload/drop/run-code отключены;
  - fullstack delivery: TDD, root-cause debugging, review, browser QA;
  - frontend: product UI redesign, frontend-design, design tokens, UI audit;
  - backend: бизнес-инварианты, auth/roles, транзакции, migrations, security;
  - GitHub: issues, repositories, PR lifecycle, code review и verified CI state;
  - локальные parsers и OCR до LLM-анализа;
  - OCR: Tesseract rus+eng, PDF/image, bbox + confidence;
  - LibreOffice: преобразование legacy Office/ODF и визуальный export;
  - форматные skills: DOCX, XLSX, PPTX, PDF;
  - fail-closed статусы PASS / PARTIAL / BLOCKED;
  - обязательные provenance, coverage accounting и read-back verification;
  - исходники не изменяются по умолчанию.

Основные команды проверки:
  hermes -p astradocs config check
  hermes -p astradocs doctor
  hermes -p astradocs skills list
  python "C:/Users/admin/AppData/Local/hermes/profiles/astradocs/skills/productivity/astra-document-operations/scripts/ocr_extract.py" --check

Рабочая папка:
  C:/Users/admin/AppData/Local/hermes/profiles/astradocs/workspace

Архитектура и результаты приёмки:
  C:/Users/admin/AppData/Local/hermes/profiles/astradocs/workspace/RESEARCH-AND-ARCHITECTURE.md
  C:/Users/admin/AppData/Local/hermes/profiles/astradocs/workspace/FULLSTACK-CAPABILITY-SELECTION.md
  C:/Users/admin/AppData/Local/hermes/profiles/astradocs/workspace/FULLSTACK-ACCEPTANCE.json
  C:/Users/admin/AppData/Local/hermes/profiles/astradocs/workspace/ACCEPTANCE.json
