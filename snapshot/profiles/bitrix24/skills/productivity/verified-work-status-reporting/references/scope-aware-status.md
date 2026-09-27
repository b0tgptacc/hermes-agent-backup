# Scope-Aware Status Updates

Use when a project has an accepted baseline and a later extension, redesign, migration, or hardening pass opens new gates.

## Reporting rule

Report both scopes explicitly:

- baseline status: accepted or still red for its original acceptance criteria;
- extension status: implementation, remediation, verification, accepted, or blocked.

A later fail-closed review supersedes an implementer's completion claim for the extension, but does not retroactively invalidate an unrelated accepted baseline. Conversely, a green baseline does not make the extension ready.

## Freshness rule

Before every repeated status answer, inspect the newest worker/reviewer stream and run or read the smallest current deterministic check. Newer reviews and newly added tests outrank earlier completion summaries.

## Concise shape

1. Current stage and scope.
2. Delta since the previous update.
3. Fresh evidence by gate.
4. Remaining blocker.
5. Next acceptance gate.

Avoid invented percentages. If a percentage is useful, label it explicitly as a rough communication estimate rather than measured completion.
