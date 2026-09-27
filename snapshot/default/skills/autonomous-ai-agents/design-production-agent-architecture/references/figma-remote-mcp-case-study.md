# Figma remote MCP case study (2026-08)

Use this as an implementation example, not a permanent statement of Figma's current product surface. Re-check official docs before deployment.

## Problem class

Employees needed to create Figma Slides and Design pages from PDF, DOCX, PPTX, XLSX/CSV, images, and briefs. Existing profiles already owned software delivery and evidence-first public research.

## Architecture result

A separate employee-facing design-production profile was justified because the workflow combined:

- a distinct user group;
- Figma OAuth and shared-file permissions;
- a general Plugin API write tool;
- document ingestion and creative output;
- independent write verification and same-file concurrency controls.

Figma remained absent from the coding and research profiles. A central orchestrator retained cross-profile ownership.

## Official remote server facts observed

Authoritative sources:

- https://developers.figma.com/docs/figma-mcp-server/
- https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/
- https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/
- https://developers.figma.com/docs/figma-mcp-server/write-to-canvas/
- https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/
- https://developers.figma.com/docs/figma-mcp-server/mcp-vs-agent/

The official hosted endpoint was `https://mcp.figma.com/mcp` with OAuth. Figma documented the remote server as recommended and the general `use_figma` tool as able to create, edit, delete, or inspect content in Figma Design, FigJam, and Slides.

Writes required a Full seat and edit permission. A Dev seat supported read-only workflows. Write-to-canvas was beta, free during beta, expected to become usage-based paid, and subject to manual-review limitations.

Figma limited remote MCP access to catalog-listed clients. The Hermes catalog used an OAuth client-name compatibility default. This is an integration dependency, not proof that Hermes is independently listed by Figma; re-test after either product changes.

## Phased allowlist and fail-closed write activation

Do not treat the desired end-state write list as the safe installation default. The case ultimately used two explicit phases.

### Pre-auth/read-only phase

Exactly eight read-oriented tools were selected:

- `whoami`
- `get_screenshot`
- `get_metadata`
- `get_design_context`
- `get_variable_defs`
- `get_libraries`
- `search_design_system`
- `download_assets`

The mutation tools `create_new_file`, `use_figma`, and `upload_assets` were technically absent. This mattered because the selected shared-account model did not yet have enforceable requester attribution and locking. Policy text and a session note were not accepted as substitutes.

### Reviewed write phase

Only after an authenticated single-worker dispatcher (immutable requester/task record plus enforced per-file or conservative global lock) or separate per-user OAuth identities are deployed may a new review consider adding:

- `create_new_file`
- `use_figma`
- `upload_assets`

The write list is therefore an activation candidate, not a default. However, do not turn this into a permanent read-only product when the approved use case requires high-quality creative production. Once dispatcher attribution and locking are technically proven, the reviewed 11-tool full-design allowlist may be configured before OAuth; configuration is not the same as permission to execute a live mutation. OAuth, seat, target-access, disposable acceptance, and post-auth review remain separate gates.

In both phases exclude Code Connect mutation/suggestions, shader tools, Weave/paid-credit tools, FigJam diagram generation, live UI capture, and all future tools not explicitly allowlisted. Keep MCP prompts, resources, and sampling disabled unless separately justified.

## Official execution skills

The upstream `figma/mcp-server-guide` repository supplied critical execution rules. Four skills covered the requested work:

- create a new file;
- general canvas execution;
- Slides-specific execution;
- full Design page/screen generation.

The implementation pinned one commit, copied full supporting references, and verified byte identity. Local security policy stayed outside the copied upstream skills.

## Document runtime pattern

Use structured tooling for PDF/DOCX/PPTX/XLSX inside a real execution boundary, not merely a profile-local virtualenv. A virtualenv isolates package versions; it does not isolate filesystem, credentials, process capabilities, or networking.

The hardened pattern used:

- a Docker image built from a digest-pinned base;
- direct and transitive Python distributions pinned with hashes;
- the configured backend pinned to the immutable built image ID rather than a mutable tag;
- non-root runtime UID;
- runtime network disabled;
- ephemeral containers and no cross-process reuse;
- no host environment forwarding;
- no arbitrary launch-cwd mount;
- one administrator-controlled staging directory mounted at `/workspace`;
- protected host ACLs on the staging directory;
- test frameworks kept in the maintenance venv but removed from the production image.

A practical runtime included PyMuPDF, pdfplumber, pypdf, python-docx, python-pptx, openpyxl, reportlab, and required crypto/table-extraction dependencies.

Run the actual skill tests. Import-only checks missed two PDF extras; the full PDF suite exposed missing table extraction and AES dependencies. After adding the required packages and regenerating the lock, all document suites passed. The durable lesson is to test helper behavior, then lock the proven environment—not to memorize one transient missing-package error.

Also exercise the actual Hermes paths, not only a handcrafted container command:

- terminal: confirm `/workspace`, non-root UID, blocked network, and no forbidden mounts;
- file: confirm an allowed staged file is readable and an outside sentinel is not;
- code execution: confirm it runs in the same confined backend;
- document behavior: create a benign fixture, extract its exact content through the agent, preserve evidence, then remove the fixture.

Do not preinstall multi-gigabyte OCR stacks without a real bulk-OCR need. Render selected scanned pages and use confined vision first.

## Shared dedicated-account model

The chosen target model used one centrally managed design profile and one dedicated Figma account. It reduced token sprawl but sacrificed native per-employee attribution.

The first design relied on policy requiring requester identity in the originating session and serialized same-file writes. Independent review correctly rejected that as insufficient: neither the session prose nor the agent policy technically authenticated the requester or acquired a lock.

A shared write identity therefore requires one of these enforceable controls before mutation tools are exposed:

1. an authenticated single-worker dispatcher that records immutable requester/task identity before dispatch and holds a per-file lock (or a more conservative global write lock); or
2. separate per-user OAuth identities when native attribution and revocation matter more than token consolidation.

While that decision is unresolved, keep the profile technically read-only even if the official mutation skills are installed. An installed skill cannot mutate through an MCP tool that is absent from the allowlist.

Additional controls remain mandatory:

- administrators retain credentials and complete OAuth;
- employees never receive passwords/tokens;
- least-privilege team/project membership;
- `whoami` before any future write;
- no deletion by default;
- upload as explicit disclosure;
- contract/licensing review for the account model;
- a new independent review before write activation.

Figma attributes writes to the dedicated account. Agent logs are compensating evidence, not native Figma authorship.

### OAuth storage and rollback archives

Protect the OAuth/client directory before authentication, not after token creation. Disable inherited ACLs and restrict the directory plus every existing file to the service identity/administrator and SYSTEM (or the platform-equivalent principals). After every OAuth or rotation, enumerate filenames and re-check ACL metadata without reading secret contents; atomically replaced files may not retain the intended ACL.

Exclude the entire credential directory—not just filenames that look like tokens—from backups, reports, fixtures, hashes, and independent-review inputs. A client metadata file may be non-secret today, but directory-level exclusion is the safer stable rule.

## Post-OAuth identity, seat, and admin diagnosis

Treat successful OAuth as authentication only. Immediately run three different checks and do not confuse them:

1. `mcp test` proves transport/auth and may enumerate the vendor's complete server catalog; it does **not** prove the agent's local allowlist.
2. the profile's MCP listing/config proves the selected local tool count;
3. `whoami` proves the account, plan, and seat returned by Figma.

For canvas writes, hard-stop when `whoami` reports `View`. Figma's seat model can change, so re-check official documentation, but in the observed 2026 flow a Full seat was required for Design creation/editing and design-mode Slides. A successful OAuth token and file-level invitation did not upgrade the seat.

If an operator cannot see Figma's Admin surface, diagnose the control plane instead of retrying OAuth:

- seat management was available on paid Professional, Organization, and Enterprise plans, not Starter;
- Professional team admins, Organization admins, and Enterprise organization/billing-group admins managed seats;
- the documented UI path was file browser → **Admin** → **People** → current **Seat type** → **Full**;
- absence of **Admin** usually meant the signed-in account was not an eligible admin or the team was not on a paid plan;
- keep the dedicated service account an ordinary member where possible. Use a separate owner/admin account to assign its Full seat and least-privilege project/file access.

Changing a seat can affect billing. Never click through a purchase or seat-cost confirmation without the user's explicit financial authorization. After an operator reports the change complete, re-run `whoami`; do not assume propagation or proceed while it still reports `View`.

OAuth may atomically create new files in the token directory. Re-harden and verify ACL metadata for **every** new file after login, without reading secret contents. Preserve only masked identity/plan/seat evidence.

## Dispatcher target validation

A governed dispatcher must validate the exact target as data before interpolating it into an agent prompt. Prefix-only regular expressions are insufficient.

For Figma URLs, use full URL parsing and require:

- HTTPS;
- exact `figma.com` or `www.figma.com` host;
- an approved artifact kind such as Design, Slides, or a reviewed legacy File route;
- a nonempty syntactically bounded file key;
- no userinfo, custom port, fragment, controls, embedded newline, or whitespace/trailing junk.

For new artifacts, accept only explicit `NEW:DESIGN:<name>` / `NEW:SLIDES:<name>` forms with a trimmed, nonempty, bounded visible name. Apply anchored safe-character validation to requester/task metadata as well.

Regression tests should include missing/short/overlong keys, hostile hosts/subdomains, HTTP, userinfo, ports, fragments, literal and percent-encoded newline injection, trailing junk, empty/whitespace new names, boundary lengths, and positive Design/Slides/legacy-file cases. Verify the global lock, hash-chain, and prompt-plaintext exclusion in the same deterministic suite.

## Strict Hermes mount mode and stale-runtime eviction

Hermes may add skills/cache/media/attachment/credential mounts beyond explicit `docker_volumes`. For a strict document-ingestion profile, use a verified profile option such as `terminal.docker_auto_mount_profile_data: false` when the installed Hermes build supports it, and test the **effective** mount inventory through terminal, file, and code-execution paths.

When changing image ID, cwd, persistence, or mount policy, terminate all profile-labeled old containers and restart processes that may cache environment construction. The deployment validator should inspect existing profile containers for image, UID, working directory, network mode, and exact mount targets, then record post-session cleanup. A correct YAML file does not evict an already-running stale container.

## Status discipline

The most important reporting pattern was:

```text
CONFIGURED != AUTHENTICATED != OPERATIONAL
```

When OAuth was canceled, the correct state was:

```text
profile/config/document runtime: PASS
OAuth: NOT AUTHENTICATED
live MCP/canvas acceptance: BLOCKED_PENDING_OAUTH
```

Do not flatten that into “connected.” Resume only when an administrator completes the official OAuth flow, then run `whoami`, tool enumeration, and a non-sensitive additive canvas smoke-test with screenshot/structure verification.

## Backup pattern

A useful rollback archive included policy, config, skills, source provenance, and dependency lock. It excluded:

- `.env`;
- OAuth/auth state;
- session/state databases;
- logs and caches;
- memories;
- the rebuildable virtual-environment binaries.

Verify every archived file hash against current source and record the archive SHA-256.
