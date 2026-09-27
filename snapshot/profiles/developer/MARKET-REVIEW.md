# Developer Profile Market Review — 2026-08-18

## Method

There is no comparable five-star user rating across agent skill registries. The
market ordering below uses skills.sh deduplicated all-time installs as popularity,
repository stars/activity as ecosystem evidence, source trust, compatibility with
Hermes v0.20, and overlap/security cost. Popularity is not treated as proof of
quality.

The skills.sh measurements below were captured at 2026-08-18 05:39 UTC. Its API
now requires a Vercel OIDC bearer token, so stable detail pages are retained as
source URLs.

## Popular developer skills and profile decisions

| Skill | skills.sh installs | Decision | Reason |
|---|---:|---|---|
| mattpocock tdd | 702,558 | Exclude | Highest installs, but duplicates the deeper Hermes `test-driven-development` RED/GREEN contract and debugging integration. |
| vercel-labs/agent-browser | 691,811 | Do not enable by default | Strong browser executor, but overlaps Hermes browser/computer-use and project-native Playwright. Enable only for explicit exploratory UI work. |
| RigorPilot repo-intake-and-plan | 419,545 | Exclude | Overlaps `codebase-inspection` + `design-first-development` + `plan`; high installs contrast with only 469 repository stars. |
| mattpocock code-review | 353,212 | Exclude | Overlaps `requesting-code-review` and `github-code-review`. |
| obra brainstorming | 329,385 | Keep local adaptation | `design-first-development` preserves the mature design workflow while removing blocking approval loops from complete delegation briefs. |
| RigorPilot safe-debug | 280,015 | Exclude | Second, shorter competing debugging constitution. |
| obra systematic-debugging | 227,884 | Keep | Clear root-cause workflow and compatible with TDD. |
| obra writing-plans | 222,171 | Keep Hermes `plan` adaptation | One implementation-planning format. |
| mattpocock request-refactor-plan | 207,709 | Exclude | Current skills.sh page remains live but matching source is absent from the current repository tree; it also overlaps planning. |
| obra subagent-driven-development | 178,927 | Keep adapted Hermes version | Best complete orchestration pattern, adapted for Hermes background delivery, leaf limits, review ownership, and one-shot constraints. |
| obra using-git-worktrees | 166,070 | Exclude as standalone skill | Worktree rules are embedded as a subordinate isolation policy; a separate mandatory workflow would add consent/phase conflicts. |
| Anthropic webapp-testing | 134,450 | Project-specific | Use only when a web project supplies a pinned browser/E2E stack. |

Additional selected skills:

- `design-first-development`: local, autonomy-safe adaptation of brainstorming;
  it decides WHAT only when requirements/design are materially uncertain.
- `subagent-driven-development`: official Hermes optional skill, adapted for the
  profile and audited SAFE; it executes accepted multi-task plans only in a
  persistent session.
- `spike`: empirical feasibility only; output is disposable.
- GitHub lifecycle skills are retained with exclusive triggers rather than adding
  generic branch/PR skills.

Source pages:

- https://skills.sh/mattpocock/skills/tdd
- https://skills.sh/vercel-labs/agent-browser/agent-browser
- https://skills.sh/lllllllama/rigorpilot-skills/repo-intake-and-plan
- https://skills.sh/mattpocock/skills/code-review
- https://skills.sh/obra/superpowers/brainstorming
- https://skills.sh/lllllllama/rigorpilot-skills/safe-debug
- https://skills.sh/obra/superpowers/systematic-debugging
- https://skills.sh/obra/superpowers/writing-plans
- https://skills.sh/mattpocock/skills/request-refactor-plan
- https://skills.sh/obra/superpowers/subagent-driven-development
- https://skills.sh/obra/superpowers/using-git-worktrees
- https://skills.sh/anthropics/skills/webapp-testing

## Tools and MCP decisions

GitHub metrics captured through its public repository API on 2026-08-18:

| Tool | Repository stars | Profile decision |
|---|---:|---|
| OpenCode | 198,598 | Optional fallback/reviewer after separate provider setup; not installed. |
| Claude Code | 141,810 | Best optional heterogeneous reviewer after separate Anthropic auth; not installed. |
| Codex CLI | 106,554 | Installed implementation worker (`0.147.0`). |
| Context7 | 60,903 | Keep as the only default MCP; pinned to `4.0.2`. |
| agent-browser | 40,839 | Optional browser task only, not default. |
| Playwright MCP | 36,226 | Do not add globally; prefer the repository's Playwright/Cypress tests. |
| GitHub MCP | 32,322 | Do not add; `gh` plus Hermes GitHub skills already cover lifecycle operations. |
| Serena | 28,159 | Do not add by default; overlaps file search/edit and structural search. |
| ast-grep | 15,564 | Installed structural search (`0.45.1`). |
| DBHub | 3,372 | Database-project-only; never default because it expands data access. |
| Docker MCP Gateway | 1,535 | Optional only when several MCP servers require a common isolation/control plane. |

Native tools and installed dependencies:

- Git 2.54.0.windows.1
- ripgrep 15.2.0
- ast-grep 0.45.1
- Python 3.11.9
- Node 24.15.0 / npm 11.12.1
- uv 0.12.3
- GitHub CLI 2.97.0 (not authenticated)
- Codex CLI 0.147.0
- Docker 29.2.1

Claude Code, OpenCode, and Semgrep are intentionally not installed: the first two
need separate credentials and a defined role; Semgrep should be project/CI-pinned
rather than modifying the Hermes runtime environment.

Sources:

- https://github.com/openai/codex
- https://github.com/anthropics/claude-code
- https://github.com/anomalyco/opencode
- https://github.com/upstash/context7
- https://github.com/vercel-labs/agent-browser
- https://github.com/microsoft/playwright-mcp
- https://github.com/github/github-mcp-server
- https://github.com/oraios/serena
- https://github.com/ast-grep/ast-grep
- https://github.com/bytebase/dbhub
- https://github.com/docker/mcp-gateway

## Target architecture

1. **Parent DEVELOPER** owns scope, design, plan, integration, verification, and
   truth. It normally implements small cohesive changes directly.
2. **Research leaf** is read-only: repository reconnaissance, documentation,
   reproduction, or dependency/security research.
3. **Implementer leaf** owns one bounded plan task under TDD. It is available only
   in a persistent Hermes session; one-shot runs use the parent or one external
   Codex worker.
4. **Spec reviewer leaf** checks only acceptance criteria and scope.
5. **Quality reviewer leaf** checks correctness, security, maintainability, and
   tests after spec compliance.
6. **Fix leaf** addresses only enumerated findings; maximum two repair/review
   cycles.
7. **External Codex worker** is an alternative implementer, never a second owner
   of the same task. Use a dedicated worktree for parallel writing.
8. **Claude Code/OpenCode** are optional heterogeneous reviewers/fallbacks, not
   default workers.
9. Nested orchestrators remain disabled (`max_spawn_depth=1`,
   `orchestrator_enabled=false`). Read-only fan-out is capped at three.
10. Durable Kanban is an optional queue architecture for long-lived multi-worker
    services, not a default feature-task workflow.

## Exclusive workflow ownership

`intake → design-first OR spike → plan → direct/TDD OR subagent execution →
systematic debugging when a defect blocks progress → verification → one final
integrated review → exactly one GitHub lifecycle owner`

Precedence rules:

- Complete brief skips design approval loops.
- Design decides WHAT; plan sequences HOW.
- Systematic debugging owns root cause; TDD owns the regression fix.
- Subagent per-task gates replace duplicate per-task requesting-code-review.
- `github-issue-to-pr` supersedes `github-pr-workflow` when an issue is the
  starting artifact.
- `github-code-review` is only for someone else's existing PR.
- No GitHub/filesystem/git/shell MCP duplicates are enabled.

## Invocation constraint discovered by execution

- Repository one-shot: `hermes --profile developer chat --in C:/repo -Q -q ...`
  works, but must not dispatch native background subagents; the process exits
  before their result returns.
- Persistent multi-agent mode: `hermes --profile developer chat --in C:/repo`
  was tested with two parallel read-only leaves. Both completed, the parent
  independently reran 13 tests, and the integrated verdict was PASS.
- Top-level `-z/--oneshot` is not used on this Windows version because it can
  initialize terminal tools in `C:/WINDOWS/system32` before applying `--in`.
