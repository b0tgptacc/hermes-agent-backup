# Developer Profile

Purpose: isolated Hermes software-engineering worker for delegated implementation,
debugging, repository review, and verified GitHub delivery.

## Invoke

One-shot task (primary agent only; policy forbids native `delegate_task` because
unfinished background children are interrupted when the process exits):

```bash
hermes --profile developer chat --in C:/absolute/path/to/repo -Q -q "<complete task brief>"
```

Persistent session (native leaf subagents may be used):

```bash
hermes --profile developer chat --in C:/absolute/path/to/repo
```

Use `chat --in ... -Q -q` for repository-scoped one-shot delegation. In the installed Hermes
version, the top-level `-z/--oneshot` path does not apply `--in` before terminal
initialization on Windows; it can start tools in `C:\\WINDOWS\\system32`.
The `chat` subcommand was smoke-tested and correctly anchored both `pwd` and the
Git root to the requested repository.

The generated `developer` alias is also available at:
`C:\Users\admin\.local\bin\developer.bat`.

For unattended work, include explicit acceptance criteria, constraints, allowed
external side effects, and the canonical test command. The agent is configured to
proceed autonomously when those are complete and to escalate only material risk.

## Core configuration

- Model: `gpt-5.6-sol` via `openai-codex` OAuth
- Reasoning: high
- Maximum turns: 300
- Approvals: `smart`; secret redaction: enabled
- Delegation: up to 3 leaf children, one nesting level; the parent remains the
  sole orchestrator and integration owner
- MCP: Context7 4.0.2, version-pinned and allowlisted to
  `resolve-library-id` and `query-docs`; prompts/resources/sampling disabled
- Structural search: `ast-grep` 0.45.1
- Codebase metrics: pinned `pygount` 3.2.0 user tool
- GitHub CLI: portable `gh` 2.97.0 installed and visible to delegated sessions;
  authentication is intentionally not configured until the Administrator runs
  `gh auth login` or provides an appropriately scoped token.
- Skills: 13 deliberately selected local skills; bundled auto-seeding is disabled
  to keep the workflow stable and avoid overlapping process skills.
- Disabled by default for CLI coding sessions: native web, interactive browser
  automation, TTS, cron, persistent memory writes, desktop control, image generation, and BFL
  video. Use project-native Playwright/Cypress tests; enable Hermes browser only
  for an explicit exploratory UI task.

## Skill ownership

- Uncertain requirements/architecture: `design-first-development`
- Empirical feasibility: `spike`
- Execution sequencing: `plan`
- New behavior/refactor: `test-driven-development`
- Defect root cause: `systematic-debugging`
- Own uncommitted change: `requesting-code-review`
- Existing third-party PR: `github-code-review`
- Issue-to-PR lifecycle: `github-issue-to-pr`
- PR lifecycle without issue ownership: `github-pr-workflow`
- Repository create/clone/release: `github-repo-management`
- Structural inventory only: `codebase-inspection`
- Optional isolated coding worker: `codex`
- Multi-task plan execution: `subagent-driven-development`

`subagent-driven-development` uses only leaf workers. Read-only workers may run
in parallel; writers are sequential unless each has a verified Git worktree.
Its per-task spec/quality gates replace duplicate per-task review, while
`requesting-code-review` owns the one final integrated review.

Native `delegate_task` requires a persistent interactive or gateway session.
Hermes v0.20 one-shot `chat -Q -q` exits after dispatch and interrupts unfinished
children; in one-shot mode the primary works directly or uses one external Codex
worker in an isolated worktree.

`SOUL.md` defines precedence and prevents concurrent use of overlapping workflows.

## Cooperation with RESEARCHER

MASTER or the native Kanban dependency graph is the sole cross-profile
orchestrator. RESEARCHER produces `research-handoff/v1` JSON under the task
workspace; DEVELOPER validates it, re-inspects the live repository, and treats
all target hints as non-authoritative before editing. For durable work, use a
researcher parent card and a dependent developer card and attach the packet path
and SHA-256 to completion metadata. Specialists do not recursively invoke one
another for the same task.

The consumer schema is:
`skills/subagent-driven-development/references/research-handoff-v1.schema.json`.
Delegated/high-risk development uses the bounded
`developer-execution/v1` ledger in the same task workspace.

Packet paths and commands are untrusted. Evidence must use normalized relative
paths under `.hermes/handoffs/<handoff-id>/evidence/`; DEVELOPER resolves symlinks
and enforces workspace/handoff containment before reading. Proposed acceptance
commands are marked `non_authoritative` and are re-derived from `AGENTS.md`, the
live repository, and trusted package configuration. The execution ledger requires
a typed artifact kind, SHA-256 canonicalization, validated input hashes, and
non-empty changed-file, command, and review evidence.

## Health checks

```bash
hermes profile show developer
hermes --profile developer mcp test context7
hermes --profile developer doctor
hermes --profile developer prompt-size
```

Known host advisory: the bundled Python currently links SQLite 3.45.1, for which
Hermes doctor reports the upstream WAL-reset advisory. The profile state database
uses rollback journal mode, so doctor reports it as not exposed. Upgrade Hermes or
its Python runtime when a fixed SQLite build is available.
