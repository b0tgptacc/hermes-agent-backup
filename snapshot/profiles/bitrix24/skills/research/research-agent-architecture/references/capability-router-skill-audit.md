# Capability-router skill audit

Use this checklist when a candidate skill installs or routes multiple external tools.

1. Evaluate standalone quality and target-profile placement separately.
2. Map trigger scope and precedence against existing phase owners; broad `MUST USE` language can override a sound architecture.
3. Separate duplicated capabilities from genuinely unique channels; classify each as default, optional/on-demand, project-specific, or exclude.
4. Inspect installer profile-awareness: `$HERMES_HOME`, exact skill destination, global package/config writes, browser-profile reuse, cross-profile credential sharing, update behavior, and rollback.
5. Verify package identity across repository and registries. Same-name registry packages may be unrelated; prefer pinned tags/commits and hashes.
6. In an isolated temporary environment, perform static inspection, dependency audit, safe/dry-run install, and target-OS tests.
7. Treat global CLIs, browser extensions, containers, MCP entries, cookies, and account/ToS risk as part of the dependency surface.
8. If only a narrow source class is valuable, prefer a curator-managed adapter that keeps unique channels and defers orchestration, provenance, browser ownership, and citations to established owners.
