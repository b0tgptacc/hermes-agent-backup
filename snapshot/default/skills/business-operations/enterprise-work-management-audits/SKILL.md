---
name: enterprise-work-management-audits
description: "Use when auditing work-platform tasks, chats, and files."
version: 1.0.0
author: Hermes Curator
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [audit, tasks, chats, files, bitrix24, jira, evidence, export, coverage]
    category: business-operations
    related_skills: [document-intelligence-pipelines, xlsx, ocr-and-documents, grounded-citations]
---

# Enterprise Work-Management Audits

Build evidence-grade exports and analyses from systems such as Bitrix24, Jira, project portals, collaboration suites, and task trackers. Use this when the requested corpus spans tasks, project membership, task-internal conversations, attachments, results, and office documents.

## Core principle

A successful API call is not a complete audit. Separate and verify four layers:

1. **Authorization coverage** — which objects the service identity can actually see.
2. **Canonical extraction** — tasks, messages, file references, results, and project metadata.
3. **Artifact acquisition and document extraction** — downloaded bytes plus format-aware parsing.
4. **Reconciliation** — expected entities equal terminal extraction statuses, with retry duplicates removed.

Administrative role, module scope, and object-level access are different facts. Never interpret an empty list or access denial as proof that the underlying object does not exist.

## Intake and scope

Before extracting:

- define the portal, tenant, period, departments/projects, and included object types;
- define interval semantics explicitly (created in period, changed in period, or active at any time in period);
- distinguish task-internal chat from general/private chat;
- confirm whether source text and files may leave the local environment;
- choose a local workspace and check storage before downloading;
- preserve the user’s original files; conversions and OCR operate on copies.

For “active at any time in interval,” a robust default is:

```text
created_at <= interval_end
AND (closed_at is null OR closed_at >= interval_start)
```

Missing dates are coverage warnings, not invented values.

## Access architecture

Prefer a dedicated service identity and a revocable integration credential. Browser access is useful for initial setup and UI cross-checks, not for bulk extraction.

Security rules:

- store credentials only in a secret store or profile-local `.env`;
- never print webhook/token URLs or download URLs;
- use a static allowlist of exact read methods;
- unknown methods fail closed;
- do not infer read safety from suffixes such as `.get` or `.list`;
- exclude arbitrary REST, raw batch, write tools, and delete tools from the production surface;
- disable MCP sampling for documentation-only or untrusted MCP servers;
- use exact portal-host allowlists for API and file downloads;
- keep API logs to method, duration, count, and error code—never message text or credential-bearing URLs.

A user must personally enter passwords and approve browser/system permission prompts. Once an authenticated session exists, use it only for the authorized portal and avoid unrelated tabs.

## Extraction procedure

### 1. Inventory first

Perform read-only probes for:

- current identity;
- task listing;
- project/workgroup listing;
- task-chat listing/history;
- accessible file storages;
- representative task, comment, and attachment retrieval.

Record counts and schemas, not sensitive sample bodies, during the probe.

### 2. Use resumable append-only acquisition

For long exports:

- write canonical JSONL records incrementally;
- maintain an atomic state file with one terminal status per task;
- write downloads through `.part` files and rename only after success;
- preserve raw records even when normalized reports will deduplicate them;
- on resume, skip terminally completed task IDs;
- deduplicate normalized outputs by stable composite keys.

Recommended keys:

- task: `task_id`;
- message: `(task_id, message_id)`;
- file attempt: `(task_id, source, attachment_id/file_id, status, local_path)`.

Interrupted runs commonly append a record before state is committed. Therefore declared report totals must use deduplicated logical records, not raw JSONL line counts.

### 3. Retry selectively

Retry only transient failures such as rate limits, timeouts, and temporary connection errors. Do **not** exponentially retry permanent `400`, `ACCESS_DENIED`, `FILE_ACCESS_ERROR`, invalid-method, or insufficient-scope responses. Parse HTTP error bodies once, classify them, and move the unit to a terminal failure/access status.

A permanent error retried per file can turn a bounded audit into an hours-long apparent hang.

### 4. Extract task conversations correctly

Modern platforms may store task comments as task-chat messages rather than legacy comment entities. Prefer the current chat/message API, then use a legacy comment API as a coverage fallback when:

- the task has no current chat identifier;
- chat retrieval fails;
- message file IDs cannot be resolved;
- historical comments predate the current chat model.

Do not add current and legacy message totals together without deduplication; they may represent the same human interaction.

### 5. Acquire every file source

Check separately:

- files directly attached to the task;
- files attached to task-chat messages;
- files attached to task results;
- legacy comment attachment objects.

Task ID, chat ID, attachment ID, and underlying disk file ID are different namespaces. Keep each explicitly named. A message file reference that returns access denied is an access gap, not proof of a missing file.

Download only from allowlisted hosts. Record one terminal status per reference:

```text
downloaded | access_denied | missing_download_url |
unsupported | failed | intentionally_skipped
```

### 6. Parse documents safely

Route downloaded files through `document-intelligence-pipelines`:

- verify signatures, hashes, and sizes;
- enforce ZIP/OOXML expansion limits;
- never execute macros, embedded code, formulas, or OLE objects;
- parse DOCX/XLSX/PPTX natively;
- extract PDF text page by page and flag empty/scanned pages for OCR;
- convert legacy Office formats only on copies using a real office converter;
- index audio/video even when transcription is unavailable;
- keep `PASS`, `PARTIAL`, and `BLOCKED` explicit.

Tracked revisions, comments, text boxes, SmartArt, screenshot text, scans, and media transcription are separate coverage dimensions. Native body text alone does not prove full-document extraction.

## Reporting contract

Produce at minimum:

- project/section register;
- task register;
- task-message register;
- file index with local path, source, hash, acquisition status, and extraction status;
- evidence register linking each task to source URL/messages/files;
- semantic navigation layer;
- coverage and limitations report;
- deterministic verification report.

A useful workbook has separate sheets for `Projects`, `Tasks`, `Messages`, `Files`, `Topics`, and `Coverage`.

Semantic clustering is exploratory navigation, not business truth. Exclude system-generated messages from clustering, weight task titles/descriptions more heavily than comments, and label clusters as machine-derived until a business taxonomy is approved.

## Verification gates

Before claiming completion:

- every in-scope task has exactly one terminal state;
- normalized task/message/file counts match deduplicated source keys;
- every downloaded file path exists;
- unique downloaded paths equal the actual file inventory;
- every downloaded file has an extraction terminal status;
- workbook/CSV row counts match normalized records;
- access-denied references remain visible as limitations;
- final status is `PASS`, `PARTIAL`, or `BLOCKED` based on the real gaps.

Use `PARTIAL` when the task corpus is usable but files are access-denied, OCR is pending, tracked revisions are incomplete, or media is not transcribed. Never report `PASS` merely because no extractor crashed.

## Bitrix24 reference

For a tested Bitrix24-specific method map, task-chat/file fallbacks, and error classifications, read `references/bitrix24-rest-audit.md`.

## Pitfalls

- Treating administrator status as global visibility.
- Using browser scraping for hundreds of tasks when a scoped API exists.
- Exposing webhook URLs in screenshots, logs, commands, or reports.
- Allowing unknown REST methods because their names look read-only.
- Retrying permanent HTTP 400/access errors with exponential backoff.
- Counting resumed JSONL duplicates as new tasks or messages.
- Assuming task-chat `FILE_ID` is interchangeable with disk or attachment IDs.
- Ignoring files attached to task results.
- Calling an OCR/media-heavy corpus complete after native text extraction only.
- Presenting auto-cluster labels as an approved business taxonomy.

## Completion standard

The audit is complete when the authorized corpus is acquired, canonical records and downloaded artifacts are reconciled, every expected unit has a terminal status, source limitations are explicit, and the user has a verified evidence package suitable for the next decision stage.
