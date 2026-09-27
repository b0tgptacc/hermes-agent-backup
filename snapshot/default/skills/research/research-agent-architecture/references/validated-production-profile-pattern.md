# Validated production research-profile pattern

This is a dated implementation reference derived from a successful Windows acceptance run on 2026-08-18. Re-check package versions and Hermes CLI behavior before reuse; preserve the architecture and verification method rather than copying volatile values blindly.

## Capability ownership

A compact, non-overlapping stack worked well:

- Search and clean public-page retrieval: one hosted search/fetch MCP.
- Interactive/JS-heavy public pages: official Playwright MCP in an isolated headless browser.
- Local documents and scans: native file/vision plus lightweight PDF extraction.
- Provenance: task-scoped local citation ledger with exact evidence quotes.
- Synthesis and ledger writes: one Primary.
- Verification: fresh read-only leaf or deterministic verifier.

Do not enable a native search provider beside an equivalent search MCP, or a native interactive browser beside Playwright, unless routing is explicit and a benchmark proves a distinct need.

## Working MCP composition

The validated profile used:

- local stdio Playwright: `npx -y @playwright/mcp@0.0.79 --headless --isolated --browser chrome`;
- hosted Exa endpoint limited in the URL to exactly two tools: `https://mcp.exa.ai/mcp?tools=web_search_exa,web_fetch_exa`;
- MCP sampling disabled for both servers.

The exact Playwright version is a historical tested value, not a perpetual recommendation. Query the package registry, pin the chosen version, and run the complete acceptance suite after upgrades.

Playwright was the only interactive browser owner. Exa owned discovery and clean retrieval. Their responsibilities did not overlap.

## Minimum Playwright surface

Start from the server catalog and allowlist only required tools. The validated profile excluded:

- `browser_evaluate`;
- `browser_file_upload`;
- `browser_drop`;
- `browser_drag`;
- `browser_run_code_unsafe`.

This retained navigation, snapshot/find, screenshots, bounded clicks, tabs, wait, ordinary form interaction, and network diagnostics while removing arbitrary page JavaScript and local-file transfer.

Treat form filling, clicks, downloads, login, payment, permission prompts, and personal-session use as separately gated actions even when a tool exists.

## Configuration procedure

1. Create a separate profile. Current Hermes profile names may require lowercase alphanumeric names; check `hermes profile create --help` instead of assuming hyphens are accepted.
2. Configure model/provider, `approvals.mode=smart`, `security.redact_secrets=true`, and depth-1 delegation with no child orchestrators.
3. Use `hermes tools enable|disable <toolset>` to curate the CLI surface. Avoid passing a JSON-looking list through `hermes config set platform_toolsets.cli`; scalar parsing can preserve it as a string rather than a YAML list.
4. Add Playwright MCP through the MCP CLI, not by hand-editing YAML. The discovery-first add/configure flow is interactive; use a PTY and explicitly select the allowlist.
5. Add only one complementary search/fetch server. Limit remote catalogs at the endpoint or through `tools.include`.
6. Disable MCP sampling.
7. Install or verify the browser engine. A connection-only MCP test does not prove that browser launch and page navigation work.
8. Adapt profile-local skills to the configured tool names. Scan the copied skill tree for stale references such as disabled native `web_search`, `web_extract`, or browser commands.

## Windows invocation

Use forward-slash native paths:

```bash
hermes --profile researcher chat \
  --in C:/Users/admin/research-workspace \
  -Q -q "<complete research brief>"
```

For interactive/fan-out work:

```bash
hermes --profile researcher chat \
  --in C:/Users/admin/research-workspace
```

Verify the actual cwd inside the acceptance task. Do not rely on a top-level one-shot shortcut when it has not been tested with `--in` on the installed Hermes version.

## Verification ladder

A production-ready profile needs all four levels.

### 1. Static configuration

Check:

- schema validation;
- pinned MCP package and arguments;
- isolated/headless browser flags;
- sampling disabled;
- exact search endpoint/tool list;
- approvals, redaction, child count, spawn depth;
- forbidden Playwright tools absent from `tools.include`;
- skill count and required local files.

### 2. Connection tests

Run:

```bash
hermes --profile researcher mcp test playwright
hermes --profile researcher mcp test exa
```

Important: `mcp test` reports the server's discoverable catalog. It can list tools that are excluded by the profile allowlist. Do not treat that display as proof that unsafe tools are exposed.

### 3. Fresh-session runtime test

Start a new agent session and require real calls to:

- search;
- clean fetch;
- browser navigation;
- browser snapshot.

Verify tool execution in the agent log or equivalent runtime trace. Also confirm the fresh session registered the configured allowlist count, not merely the full discoverable server catalog.

### 4. End-to-end evidence test

Use a current-fact task with official sources and require:

- task-scoped ledger;
- saved evidence text;
- exact verified quote per cited source;
- at least one cited URL opened through Playwright;
- claim table/evidence packets for non-trivial work;
- rendered source list;
- strict citation verification;
- read-only independent verdict;
- machine-readable final check.

A useful acceptance criterion is not a particular fact value, but that the real release/date/status is discovered at runtime and all claims are traceable.

## Citation CLI ordering

For the Grounded Citations script, `--ledger` is a global option and must precede the subcommand. The draft is positional:

```bash
python sources.py \
  --ledger C:/path/citations.json \
  verify C:/path/report.md \
  --strict --evidence --min-coverage 0.5
```

A connection test, rendered URL list, or non-strict low-coverage pass is insufficient. The production gate requires evidence quotes and a strict verifier exit code of zero, or explicit unresolved/unverified labeling.

## Doctor output interpretation

Separate blocking state from intentional design:

- A keyless MCP plus OAuth model can be fully operational even when doctor notes an empty profile `.env`.
- A native browser tool can be disabled or unavailable while the separately configured Playwright MCP is healthy.
- Do not dismiss warnings; validate the intended path with real execution and document why an advisory is non-blocking.

## Profile documentation

Record in the profile:

- ownership map;
- MCP transport, version, tool allowlist, and sampling policy;
- data sent to hosted services;
- browser isolation/auth/download policy;
- installed document/monitoring dependencies;
- invocation commands;
- acceptance artifacts and verifier status;
- known non-blocking advisories.

Keep popularity metrics, architectural recommendation, and actually installed/tested state clearly separated.
