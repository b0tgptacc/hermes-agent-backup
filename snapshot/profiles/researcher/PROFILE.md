# RESEARCHER Profile

Purpose: production-ready, evidence-first web research for current facts, market intelligence, news, academic literature, public web pages, PDFs/scans, video transcripts, and cited reports.

## Runtime

- Profile name: `researcher`
- Model: `gpt-5.6-sol`
- Provider: `openai-codex`
- Reasoning: high
- Maximum turns: 300
- Approvals: smart
- Secret redaction: enabled
- Delegation: maximum 3 leaf children, depth 1, full orchestrator mode disabled

## Process Architecture

`Primary → Discovery Scout(s) → Extraction Specialist → Primary synthesis → independent Verifier → Primary final gate`

The Primary is the only owner of the common ledger, claim table, synthesis, citation IDs, conflict resolution, and final verdict.

## MCP Stack

### Playwright MCP

- Required browser owner.
- Local stdio transport.
- Pinned npm package: `@playwright/mcp@0.0.79`.
- Starts isolated, headless Google Chrome.
- Sampling disabled.
- Default allowlist contains 12 navigation/extraction tools. Form filling,
  typing, clicking, key presses, option selection, hover, and dialog handling are
  absent; authenticated or state-changing browser interaction is not a default
  research capability.
- MCP prompts/resources disabled.
- Native Hermes browser and computer-use are disabled to prevent competing browser processes.

### Exa MCP

- Hosted endpoint with exactly two enabled tools: `web_search_exa` and `web_fetch_exa`.
- Used for discovery and clean full-page retrieval; Playwright remains the only dynamic browser/navigation owner.
- Anonymous, rate-limited access; no API key is stored in the profile.
- Sampling disabled.
- Explicit two-tool allowlist; MCP prompts/resources disabled.

Do not add Tavily, Firecrawl, Brave, Perplexity, Fetch, filesystem, PDF, citation, or omnibus MCP servers as parallel defaults. A provider may replace Exa after a benchmark, not coexist as a second default owner.

## Curated Skills

Core:

1. `research-orchestration`
2. `grounded-citations`
3. `blocked-page-recovery`
4. `ocr-and-documents`

Modes:

5. `product-market-research`
6. `arxiv`
7. `youtube-content`
8. `blogwatcher`
9. `competitor-news-monitor`

## Tool Surface

Enabled: clarification, code execution, cron jobs, delegation, file operations, session search, skills, terminal/processes, task planning, and vision.

Disabled by default: native browser, native web, computer-use, memory writes, media generation, TTS/STT, and X search. Cron is enabled only because monitoring is a defined research mode; every scheduled job still requires an explicit user request and scoped delivery target.

## Cooperation with DEVELOPER

MASTER or the native Kanban dependency graph is the sole cross-profile
orchestrator. For implementation-oriented research, RESEARCHER writes a
`research-handoff/v1` packet to
`.hermes/handoffs/<handoff-id>/research.json`, validates it against
`skills/research/research-orchestration/references/research-handoff-v1.schema.json`,
and attaches its path/hash to Kanban completion metadata. RESEARCHER does not
edit production code or claim implementation correctness; the dependent
DEVELOPER re-inspects the repository and owns engineering acceptance.

Evidence paths are normalized workspace-relative paths confined to
`.hermes/handoffs/<handoff-id>/evidence/`; absolute, traversal, backslash, and
unrelated local paths are schema-invalid. Proposed acceptance commands carry
`non_authoritative: true`; DEVELOPER independently re-derives commands instead of
executing packet text.

## Local Dependencies

- Google Chrome: installed at `C:/Program Files/Google/Chrome/Application/chrome.exe`.
- Playwright MCP: pinned to npm `@playwright/mcp@0.0.79`.
- PyMuPDF and PyMuPDF4LLM: `1.28.2`, installed in the Hermes Python 3.11 environment.
- `youtube-transcript-api`: installed in the Hermes Python environment.
- `blogwatcher-cli`: source pinned to `v0.2.1`, compiled as `C:/Users/admin/bin/blogwatcher-cli.exe` with upstream SSRF protection enabled by default.
- Marker/OCR heavyweight models are not preinstalled; scanned-page fallback uses page rendering plus vision, with Marker installed only when a real bulk-OCR task justifies its 3–5 GB footprint.

## Invocation

Quick sequential research:

```bash
hermes --profile researcher chat -Q -q "<complete research brief>"
```

Deep research with native leaf delegation:

```bash
hermes --profile researcher chat
```

Then submit the brief in the persistent session.

When a task workspace matters on Windows:

```bash
hermes --profile researcher chat --in C:/absolute/path/to/workspace -Q -q "<brief>"
```

Do not use top-level `-z/--oneshot` with `--in`; Hermes v0.20.0 could initialize terminal tools from `C:/WINDOWS/system32`.

## Verified Acceptance Baseline

Verified on 2026-08-18:

- `config check`: PASS; config schema v34.
- `mcp test playwright`: connected; official package pinned to `0.0.79`.
- `mcp test exa`: connected; anonymous two-tool endpoint.
- Previous baseline: 19 Playwright tools. Hardened baseline: 12 allowlisted
  navigation/extraction tools; evaluation, upload/drop/drag, unsafe code, form
  entry, typing, clicking, key presses, selection, hover, and dialogs absent.
- Real MCP smoke: Exa search plus Playwright navigation/snapshot against `https://example.com`: PASS.
- End-to-end research: Python 3.14.7/current Python 3.11 support status using three official sources, Exa discovery/fetch, Playwright browser evidence, three evidence packets, task-scoped citation ledger, and independent verifier: PASS.
- Grounded Citations: `verify --strict --evidence --min-coverage 0.5`: exit 0, 75% source-bearing sentence coverage.
- Playwright Chromium, PyMuPDF/PyMuPDF4LLM, youtube transcript support, and `blogwatcher-cli`: installed and exercised.

Acceptance artifacts are at `C:/Users/admin/researcher-agent-demo/`.

## Known Limitations

- Exa's anonymous hosted endpoint is externally operated, rate-limited, and receives search queries and fetched public URLs. Do not submit confidential queries or private URLs.
- Playwright operates a real isolated browser against public pages. The default profile cannot fill forms, click controls, type, press keys, select options, hover, or handle dialogs. Any authenticated or state-changing interaction requires a separately reviewed task-scoped allowlist change and explicit Administrator authorization; personal sessions remain out of scope.
- `hermes doctor` reports that no API key exists in the profile `.env`; this is expected because the model uses existing OpenAI Codex OAuth and both configured MCP servers are keyless.
- Hermes' embedded SQLite 3.45.1 triggers the upstream WAL-reset advisory. Hermes has automatically forced `journal_mode=DELETE`; doctor confirms the state databases are not exposed to the WAL bug. Upgrade the managed runtime when a compatible Hermes update is available.
- Native Tavily/Exa/Firecrawl web tools are intentionally disabled because no provider API key is configured. If a key is later added, benchmark and replace the anonymous Exa MCP instead of enabling both search surfaces.
- Recurring monitoring requires an explicitly created cron job and delivery target.
