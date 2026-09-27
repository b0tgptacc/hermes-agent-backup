# Extending a cloned profile with a credentialed business system

Use this pattern when the Administrator explicitly wants a new domain profile to retain an existing profile's model, identity, tools, skills, and preferences while adding one enterprise system such as a CRM, ERP, service desk, or document platform.

## Build pattern

1. **Confirm the inheritance intent.** When the request is to “copy the base profile,” use `hermes profile create <name> --clone-from <source>` rather than an isolated blank profile. Do not use `--clone-all` unless session/state cloning is explicitly required.
2. **Inventory before adding.** Record the cloned model/provider, skills, MCP servers, privacy settings, approval mode, gateway state, and secret-redaction state. A clone can inherit unrelated credentials; never print them, and call out the inherited data boundary in the handoff.
3. **Separate knowledge from operations.** Prefer an official documentation-only MCP as the default knowledge layer. It can verify current API methods without holding tenant credentials or mutating data. Treat an operational MCP as a separate decision requiring tenant credentials, tool allowlists, and representative read/write tests.
4. **Curate, do not maximize.** Compare official templates and community connectors by maintenance, license, tool granularity, raw-API exposure, read-only support, authentication, and runtime allowlisting. Exclude broad connectors that combine reads, writes, deletes, and arbitrary raw API calls when a smaller direct client or audited wrapper covers the task.
5. **Inspect the complete installed artifact.** A hub scanner verdict is only one input. Read the skill contract and scripts, identify OS assumptions, secret handling, network destinations, batch behavior, and mutation classification. Never patch bundled, hub, pinned, external, or user-owned skills in the shared library; use a curator-managed local wrapper/overlay or recommend adoption. Profile-local user-authorized hardening is separate from curator library maintenance.
6. **Fail closed around mutations.** Unknown API methods must not default to read-only. Use an explicit read allowlist or classify unknown methods as writes. Batch helpers should be read-only unless they implement an auditable per-command approval boundary. Require a distinct confirmation for writes and a stronger one for destructive actions.
7. **Add a domain audit skill.** The profile should carry a class-level workflow for scope intake, privacy, deterministic inventory, coverage reconciliation, provenance, and `PASS/PARTIAL/BLOCKED` reporting. Keep tenant-specific endpoints, IDs, and credentials out of the skill.
8. **Surface the inference boundary.** Before sending chats, personnel records, customer data, or files to the configured model, state whether inference is cloud or local and obtain the required organizational decision. Cloning a profile also clones its model choice; that choice may be unsuitable for the new data class.

## MCP setup and verification

`hermes mcp add` may prompt first for authentication and then for which discovered tools to enable. Run it in a PTY and answer deliberately; a non-interactive call can hang without saving configuration.

For every selected MCP:

1. verify the publisher/repository and exact endpoint;
2. run `hermes -p <profile> mcp test <server>` and record the live discovered tools;
3. compare live discovery with README claims—live discovery can expose a newer or different tool set;
4. start the real profile and make one representative read-only MCP call;
5. independently validate the result against the returned official documentation or target system;
6. keep untrusted/community server sampling disabled unless it has a justified role.

A documentation MCP passing discovery is not evidence that tenant data access works. Tenant access remains `BLOCKED` until real scoped credentials are supplied and a read-only portal call succeeds.

## Enterprise access handoff

Request, without asking the user to paste secrets into chat:

- tenant URL and cloud/on-prem deployment type;
- dedicated integration identity and scoped webhook/OAuth path;
- approved entities, users/departments/projects, date range, and data classes;
- explicit decision on private/closed conversations and file contents;
- processing location, retention, redaction, and report recipients;
- expected output and one bounded pilot scope;
- cloud-versus-local inference decision.

Administrator status does not necessarily override object-level access or provide a global private-message export. Verify coverage empirically, reconcile counts, and report inaccessible areas as `PARTIAL` rather than claiming completeness.

## Acceptance gates

- profile creation and config check pass;
- selected skills are visible to the target profile;
- security-sensitive helper scripts pass syntax tests and mutation-rejection tests;
- MCP transport/discovery passes;
- a real profile session loads the domain skill and performs one representative MCP call;
- secret redaction, PII policy, and approval mode are explicit;
- no tenant write is performed during acceptance;
- missing tenant credentials and private-data authorization are reported as setup blockers, not tool failures.
