---
name: verified-work-status-reporting
description: "Use when reporting status of long-running verified work."
version: 1.0.0
author: MASTER
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [status, progress, verification, delivery, orchestration]
    category: productivity
---

# Verified Work Status Reporting

Report the real state of long-running implementation, research, migration, deployment, or review work without confusing activity with completion. Use when the administrator asks “what is the status?”, when an external requester needs a progress update, or when a multi-stage task crosses implementation and acceptance gates.

## Core rule

Derive status from fresh evidence, not the last narrative. A worker saying “completed,” a targeted test passing, or a service being reachable proves only that scoped fact.

## Procedure

1. Inspect the active worker, reviewer, process, or durable task record.
2. Run or read the smallest deterministic check that grounds the current stage.
3. Separate evidence by scope:
   - targeted checks;
   - full regression suite;
   - runtime/container health;
   - browser/E2E acceptance;
   - independent review.
4. Classify the state:
   - **implementation** — core behavior is still being built;
   - **remediation** — review findings have failing tests and fixes underway;
   - **verification** — implementation is stable but release gates remain;
   - **accepted** — all required gates are green;
   - **blocked** — progress needs a human decision, access, or external dependency.
5. Report the current stage, verified delta, open blockers, and next gate.
6. If the requester is external, do not send “ready” until acceptance is verified.

## Scoped evidence language

Prefer:

- `security regression tests: 11/11 pass`;
- `latest full suite: 29 passed, 2 failed, 5 errors`;
- `database container healthy; application acceptance still pending`.

Avoid:

- `all blockers fixed` when only focused tests are green;
- `done` because the worker exited successfully;
- `Docker verified` when only `compose config` passed;
- percentages that imply precision not supported by acceptance criteria.

A newly strengthened invariant can make an old fixture invalid. State this as a regression being reconciled, not as a product defect or a completed fix, until the full suite passes again.

## Repeated status questions

Answer with the delta since the previous update. Lead with the current stage and changed evidence; do not repeat the full feature inventory unless requested. Keep the response decision-ready:

1. current state;
2. newly verified progress;
3. remaining blocker;
4. next gate.

## External progress updates

For end users, keep one unobtrusive, non-technical status message. Use semantic stages and only a conditional progress scale. Never expose tool names, paths, prompts, secrets, raw errors, or internal reasoning. Fast tasks should not create status flicker.

## Completion gate

Use “accepted” or “ready” only when the requested outcome exists and every named acceptance criterion has appropriate evidence. If verification is incomplete, say exactly which gate remains.

## Pitfalls

- Treating process activity as proof that useful progress is occurring.
- Reporting targeted and full-suite results as one undifferentiated count.
- Repeating stale status after the worker or files changed.
- Hiding a red full suite behind several green subsystem checks.
- Sending an external completion message before independent review.
- Overloading repeated updates with the whole project history.

## Reference

See `references/status-evidence-patterns.md` for reusable status shapes and acceptance-state examples.
