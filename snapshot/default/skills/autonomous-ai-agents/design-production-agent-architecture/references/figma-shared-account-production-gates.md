# Figma shared-account production gates

Use this reference when a centrally managed DESIGNER profile must retain real Figma Design/Slides creation capability while enforcing scope, attribution, concurrency, and document isolation.

## Capability model

A permanent read-only allowlist is not an acceptable end state when employees must create polished designs. Keep an exact reviewed surface that includes identity/context tools plus the vendor's new-file, canvas-mutation, and authorized asset-upload tools. Exclude unrelated code-integration, paid workflow, shader, diagram, capture, and future tools.

Govern risk around creative work rather than disabling composition, typography, imagery, component reuse, and iterative canvas editing.

## Governed shared-account dispatcher

Require every job to supply:

- authenticated/requester identifier;
- stable task ID;
- exact existing Figma target or explicit new Design/Slides declaration;
- employee brief and authorized inputs.

Hold a system-wide mutex for the complete job. A conservative global lock is acceptable and stronger than same-file locking when one shared account is used.

Write START/END records to a hash-chained ledger. Store a prompt SHA-256 rather than prompt plaintext. `fsync` records. Document that this is tamper-evident operational evidence, not vendor-native immutable attribution.

### Target validation

Do not validate Figma targets with a URL-prefix regex. Parse the entire value and require:

- HTTPS;
- exact `figma.com` or `www.figma.com` host;
- approved artifact kind (`design`, `slides`, or legacy `file`);
- nonempty ASCII-alphanumeric file key with reviewed length bounds;
- no userinfo, custom port, fragment, whitespace, control characters, hostile subdomain, or trailing junk.

For new artifacts, allow only explicit `NEW:DESIGN:<name>` or `NEW:SLIDES:<name>` values with a trimmed nonempty bounded name and no controls. Validate requester/task metadata with anchored safe-character expressions before embedding it into prompts.

Regression tests must include missing/short/oversized keys, hostile hosts, trailing junk with an otherwise valid key, literal and percent-encoded newline injection, fragments, empty/whitespace names, and positive Design, Slides, legacy File, and new-artifact cases.

## Effective Docker confinement

Use canonical Hermes keys and verify resolved runtime state:

- container cwd `/workspace`;
- `container_persistent: false`;
- cross-process reuse disabled;
- immutable image ID;
- non-root UID;
- network disabled;
- canonical CPU/memory/disk settings;
- no host environment forwarding;
- one explicit staging bind.

If supported, set `terminal.docker_auto_mount_profile_data: false` for document-ingestion profiles. Verify the config-to-environment bridge consumes it and that actual `/proc/self/mountinfo` exposes only `/workspace`, not profile skills, cache, media, attachments, credentials, or a persistent home.

After any image or confinement change, evict every old profile-labeled container and restart cached Hermes processes. Inspect current Docker inventory for stale image IDs, `/root` working directories, persistent home binds, extra mounts, or test-only dependencies.

A handcrafted `docker run` remains only a component test. Capture real Hermes terminal, file, and code-execution evidence and make the validator check that evidence plus current container inventory.

## OAuth and post-auth sequence

1. Confirm the organization contract permits the dedicated shared identity.
2. Start the official OAuth flow; the human administrator enters credentials. Never request or read passwords, callback codes, tokens, cookies, or recovery material.
3. Inventory newly created token filenames without reading contents.
4. Remove inherited ACLs from the token directory and every created/replaced token file; allow only the administrator and SYSTEM.
5. Run MCP connectivity and verify the local exact tool allowlist separately from the vendor's full discovered catalog.
6. Call `whoami`; mask identity in evidence and verify expected account, plan, and seat.
7. Treat a View/Dev/read-only seat as a hard write blocker. Do not attempt mutation until a Full seat and least-privilege edit access to a disposable non-sensitive project/file are confirmed.
8. Run the disposable task through the governed dispatcher, not a raw profile invocation.
9. Verify returned object IDs, structural metadata, layout checks, representative screenshots, final URL, audit START/END linkage, and lock behavior.
10. Conduct a post-authenticated independent review.

## Status discipline

Track separately:

- `CONFIGURED`: exact tools, dispatcher, sandbox, ACL policy installed;
- `AUTHENTICATED`: OAuth connected and masked identity verified;
- `OPERATIONAL`: Full seat/edit permission and disposable live read/write acceptance passed.

OAuth success alone is not operational acceptance. A successful MCP connection can discover many vendor tools while Hermes still registers only the reviewed allowlist; verify both facts independently.
