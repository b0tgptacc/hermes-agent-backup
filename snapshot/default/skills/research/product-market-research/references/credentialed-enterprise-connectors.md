# Credentialed enterprise connector curation

Use this reference when selecting or designing MCP/agent access to a CRM, ERP, task system, document store, chat archive, or other confidential business platform.

## Separate documentation from operations

Treat these as different capability classes:

- **Documentation MCP:** searches vendor API documentation and never receives tenant credentials or business records.
- **Operational connector:** authenticates to a tenant and reads or changes real records.

An official hosted documentation MCP can be a safe default only after a live handshake and tool-schema inspection. Disable server-initiated sampling unless it is explicitly required. Assume the hosted service sees every documentation query, so queries must contain method/domain terminology only—never client names, message text, filenames, IDs, or other tenant data.

## Operational connector default

Do not select a broad community connector merely because it advertises many domains. For confidential analysis, prefer a thin local stdio connector built after the approved scope is known. A vendor SDK or official server template may be useful as implementation material without being safe to deploy as-is.

Required production properties:

1. Static allowlist of exact read-only API method names.
2. Unknown methods fail closed; suffixes such as `.get` or `.list` are not authorization evidence.
3. No arbitrary/raw REST call, generic endpoint, or user-supplied method name.
4. No unrestricted batch endpoint; each outbound method is validated individually.
5. No write tools or write code in the read-only production build.
6. Fixed HTTPS tenant hostname and SSRF protection.
7. Pagination, response-size, runtime, and file-size limits.
8. Download/auth/token/webhook URLs are consumed internally or redacted before model-visible output.
9. Logs contain tool name, duration, count, and error class only—not query text, chat content, CRM fields, filenames, credentials, or signed download URLs.
10. File-content access is a separate opt-in capability from file metadata listing.

A prompt or README saying “read-only by default” is not a security boundary. Verify enforcement in code and tests.

## Authentication and access reality

- Prefer a dedicated service identity with the minimum module scopes and revocable credentials.
- A long-lived incoming webhook is a bearer secret even when embedded in a URL; never place it in config, logs, prompts, reports, or command arguments.
- Module scopes do not prove method-level read-only behavior. The connector's exact allowlist is the primary barrier.
- Administrator status does not necessarily bypass object-level permissions or expose all private chats, closed groups, files, or deleted records. Inventory and reconcile accessible objects before claiming completeness.
- For multi-user or multi-tenant access, OAuth may be necessary, but token storage/refresh and per-user identity materially increase the attack surface.

## Profile creation rule

For isolated enterprise work, create a blank profile. If the Administrator explicitly requires cloning a base profile, treat cloning as a migration, not a shortcut: immediately inventory inherited `.env` credentials, gateways, MCP servers, plugins, memory, and toolsets; remove unrelated access; keep secret and PII redaction enabled; and verify the target profile—not the source profile—end to end.

## Acceptance tests

Require deterministic evidence:

- documentation MCP handshake, discovered tools, sampling state, and one representative call;
- exact runtime tool allowlist, not upstream discovery count;
- an allowed read method succeeds or reaches the expected auth boundary;
- a known write method is rejected even with legacy confirmation/override flags;
- an unknown method whose name looks read-only (for example `evil.fake.list`) is rejected;
- generic batch/raw methods are absent or reject non-allowlisted calls;
- signed download/auth URLs are redacted from model-visible output;
- source inventory totals reconcile with extracted/empty/out-of-scope/unsupported/access-denied/failed terminal states;
- no completeness claim while unexplained gaps remain.

## Selection labels

- **default:** verified documentation-only MCP, or audited thin operational connector meeting every required property.
- **optional/pilot:** narrow connector with strong controls but incomplete domain coverage or low maturity.
- **implementation source only:** official SDK/template containing useful auth, throttling, or tenant-guard patterns but also write tools.
- **exclude:** raw API, broad mixed read/write surface, fail-open method classification, secret-bearing per-call parameters, unbounded file access, missing license, or no meaningful tests.
