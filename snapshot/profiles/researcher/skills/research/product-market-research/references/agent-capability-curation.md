# Agent Capability Curation

Use this reference when comparing AI-agent skills, MCP servers, coding CLIs, built-in tools, reviewers, or worker architectures. The objective is a coherent default capability set, not the largest install count.

## Evidence model

Do not call popularity a quality rating. Keep these columns separate:

- registry installs/downloads: adoption only;
- repository stars/forks/activity: ecosystem-level signal, not a per-skill score;
- source trust: official, maintained community, unknown, or archived;
- compatibility: current agent runtime, OS, tool contracts, and execution surface;
- security/side effects: secrets, network, filesystem, browser, database, and remote-write scope;
- operational cost: context/tool-schema size, dependencies, credentials, runtime, and review overhead;
- engineering utility: the concrete phase or failure mode it owns.

Timestamp dynamic metrics and link the stable detail/repository pages. If an API becomes authenticated or unavailable, preserve the last verified snapshot date instead of presenting it as live.

### Registry and repository evidence collection

For skills.sh market scans, prefer its public search endpoint for broad, reproducible discovery:

```text
https://skills.sh/api/search?q=<url-encoded query>&limit=100
```

Query several capability synonyms rather than one broad term, then deduplicate by the returned skill id. Use each stable detail page (`https://skills.sh/<owner>/<repo>/<skill>`) to verify the description, install display, repository link, first-seen date, organization verification, and security-audit badges. The search index and detail page can temporarily show different install totals; record both with the timestamp and label the discrepancy instead of choosing the larger value.

Repository activity is a separate signal. When unauthenticated GitHub API limits block metadata requests, the repository's public `https://github.com/<owner>/<repo>/commits.atom` feed provides a verifiable latest-commit timestamp. Keep repository stars explicitly labeled as repo-level: they are not attributable to one skill in a monorepo. Security badges are triage signals, not verdicts; any Warn/Fail requires reading the specific finding and the complete skill/install contract before selection.

Rank decision utility first, while retaining popularity as a separate adoption field. A low-install new or narrowly scoped skill may still be the default owner of a critical failure mode; a highly installed generic skill may be excluded when it duplicates native capabilities or has unresolved audit findings.

## Curate against the current library

Before recommending or installing anything:

1. Inventory installed skills, built-in tools, MCP servers, CLIs, credentials, model/provider, delegation limits, and project rules.
2. Build a phase map: intake, design, feasibility, planning, implementation, debugging, verification, review, Git/PR lifecycle, deployment.
3. Assign exactly one default owner to each phase.
4. Mark every candidate `default`, `optional/on-demand`, `project-specific`, or `exclude`.
5. Record the overlap it would create and the precedence rule needed if retained.

Common duplicate families:

- brainstorming/design vs planning;
- diagnosing/debugging workflows;
- own-change review vs third-party PR review;
- issue-to-PR vs generic PR lifecycle;
- native file/terminal/Git tools vs filesystem, shell, or Git MCP servers;
- native browser automation vs agent-browser/Playwright MCP;
- primary implementer vs external coding CLI worker;
- per-task review gates vs a second whole-diff review loop.

Popularity never overrides an unresolved overlap.

## Inspect before installation

Read the complete skill/tool contract, not only the registry description. Check for:

- unsupported parameters or stale tool names;
- assumptions that child agents can clarify, persist, commit, or access secrets;
- mandatory commits, pushes, installs, or browser logins;
- instructions to prefer itself over built-in tools;
- fixed concurrency or nesting assumptions;
- hidden dependencies and install scripts;
- platform-specific path/process behavior.

If an official or popular skill is nearly right, adapt only a curator-managed copy. Never silently edit bundled, hub-installed, pinned, external, or user-owned content.

## Architecture policy

Prefer a flat topology:

- parent: scope, decisions, integration, final verification;
- read-only research leaf;
- bounded implementer leaf;
- spec reviewer;
- quality/security reviewer;
- bounded fix worker.

Use nested orchestrators only when a durable queue or genuinely large program earns the added failure modes. Parallelize read-only work freely within the configured cap. Never run concurrent writers in one checkout; use verified worktrees/branches or serialize them.

Treat an external coding CLI as an alternative implementation owner, not a second agent editing the same task. Heterogeneous reviewers are optional only after their credentials, budget, sandbox, and output contract are configured.

## Execution-surface probe

Do not infer multi-agent behavior from API shape alone. Test both intended surfaces:

1. one-shot/headless invocation;
2. persistent interactive or gateway session.

A background child may outlive a turn but not the parent process. Acceptance testing must prove that results re-enter the session, the parent resumes, and the parent verifies artifacts. If one-shot cannot retain background children, route one-shot work to the parent or one bounded external worker; reserve native fan-out for a persistent surface. Phrase this as a tested routing rule for the current runtime, not a permanent claim that a tool is broken.

## Dependency tiers

- **Core:** version control, fast text search, structural search, language/runtime, package manager, repository CLI.
- **Project-specific:** tests, linter, type checker, browser/E2E framework, database client, security scanner; pin through the project lockfile/CI.
- **Optional credentialed workers:** alternative coding agents/providers; install only with a defined role, credentials, budget, and fallback value.
- **MCP:** default only when it adds a capability not already supplied by native tools/CLIs. Prefer the smallest server set and pin versions where reproducibility matters.

## Verification gates

After curation:

- validate configuration and prompt/tool-schema size;
- audit every newly installed skill;
- test each MCP connection and discovered tools;
- verify dependency versions and PATH visibility from the delegated profile;
- run a read-only one-shot policy smoke test;
- run a persistent multi-agent smoke test when native subagents are part of the design;
- run the canonical demo/project tests and inspect the real working tree;
- document limitations such as missing auth as setup state, not as permanent tool incapability.

Final reporting should distinguish: market leaders, selected defaults, optional candidates, explicit exclusions, overlap rules, actual installed state, and real acceptance-test evidence.