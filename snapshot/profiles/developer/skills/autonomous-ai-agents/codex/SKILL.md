---
name: codex
description: "Delegate an isolated coding task to Codex CLI safely."
version: 2.0.0-developer
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [coding-agent, codex, worktree, review]
    related_skills: [subagent-driven-development, requesting-code-review]
---

# Codex CLI Worker for DEVELOPER

## Purpose

Use the installed Codex CLI as one explicitly selected heterogeneous worker for a
bounded coding or detached review task. `subagent-driven-development` remains the
orchestration, isolation, verification, and integration owner. Never assign the
same implementation task to both Codex and a Hermes writer.

## Activation gate

Use only when:

- the task is large or isolated enough to benefit from a second implementation
  context, or the Administrator explicitly requests Codex;
- a Git repository, exact acceptance criteria, canonical commands, and allowed
  scope are known;
- the parent can verify the resulting worktree, diff, and tests.

For small cohesive changes, implement directly. For broad current-web research,
request a RESEARCHER handoff through MASTER rather than sending Codex to browse.

## Prerequisites

- `codex --version` succeeds.
- Codex OAuth is already configured; never copy auth files or tokens into prompts.
- The task runs inside a Git repository.
- Terminal calls use `pty=true`.
- Native Windows programs receive `C:/...` paths. Scratch paths come from
  `$LOCALAPPDATA/Temp`, converted to `C:/...` when passed as native argv.

Do not install or upgrade Codex automatically during a task.

## Safe writer workflow

1. Inspect `AGENTS.md`, Git state, base SHA, project commands, and existing user
   changes.
2. Create a dedicated branch/worktree for a writer. Never run concurrent writers
   in the same checkout. Example from a repository root:

```bash
git worktree add -b agent/codex-task "C:/Users/admin/AppData/Local/Temp/codex-task" HEAD
```

3. Launch with workspace-only write sandboxing and no automatic remote actions:

```text
terminal(
  command="codex exec --sandbox workspace-write '<self-contained brief>'",
  workdir="C:/Users/admin/AppData/Local/Temp/codex-task",
  background=true,
  notify_on_complete=true,
  pty=true
)
```

The brief must include allowed files, non-goals, required RED/GREEN checks,
canonical tests, no secret access, no package/global install, no commit/push/PR,
and the structured completion fields.

4. Do not poll repeatedly. On completion, inspect the actual worktree and require:

- changed files and diff;
- commands, exit codes, and bounded output summaries;
- assumptions and residual risks;
- sandbox/network mode;
- no commit or external side effect unless explicitly authorized.

5. The DEVELOPER parent reruns targeted tests, checks the complete diff and Git
state, and performs artifact-bound independent review. A Codex summary is not
proof.
6. Integrate only after verification. Clean up the worktree only after preserving
required evidence and confirming no uncommitted work would be lost.

## Detached review workflow

Use a dedicated review checkout/worktree and ask Codex for findings only. Bind the
review to an exact base/result SHA or patch hash. The reviewer must not edit,
commit, comment on GitHub, or push. The parent validates every finding against the
actual diff and reruns deterministic checks.

## Gateway and sandbox failures

If workspace sandboxing fails in a gateway/service context, stop and report the
observed error. Do not silently switch to an unsandboxed host mode. The shortest
safe alternatives are:

1. run the worker in a disposable container/VM with a dedicated worktree;
2. let DEVELOPER implement directly under normal Hermes approvals;
3. request explicit Administrator authorization for the exact isolation boundary
   and consequential capability.

A Git worktree is edit isolation, not a security sandbox.

## Parallel work

- Parallel read-only reviews are allowed when each is artifact-bound.
- Parallel writers require independent branches and worktrees with no shared
  generated outputs or migrations.
- The parent serializes integration and reruns integration tests.
- Codex workers never push, open PRs, merge, deploy, or edit another worktree by
  default.

## Completion contract

Return to the parent:

- worktree and branch;
- base SHA and result SHA or dirty-diff SHA-256;
- changed files;
- exact commands and exit codes;
- test/build summaries;
- sandbox and network mode;
- assumptions, blockers, and residual risks.

The parent accepts only after reproducing the relevant checks and confirming the
base checkout and unrelated user work are unchanged.
