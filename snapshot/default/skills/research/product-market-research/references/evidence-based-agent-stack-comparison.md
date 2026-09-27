# Evidence-Based Agent Stack Comparison

Use this reference when comparing complete AI-agent stacks such as Hermes, OpenClaw, Codex, Claude Code, or a model-backed custom agent. Compare the working system, not model labels alone.

## Separate the layers

Evaluate four layers independently:

1. **Model** — reasoning, coding, context, modalities, latency, price, and availability.
2. **Harness/runtime** — agent loop, tool calling, approvals, sandbox, session lifecycle, compaction, retries, and native coding workflow.
3. **Configured instance** — enabled tools, skills, profiles, memory, channels, credentials, fallback providers, prompt/schema size, and actual dependency readiness.
4. **Operations** — service management, backups, monitoring, audit, trust boundaries, update policy, incident recovery, and total maintenance cost.

A provider route that calls a model through the host agent loop is not automatically equivalent to the vendor's native coding harness. State explicitly whether the comparison uses a shared loop, a native app-server/ACP runtime, or an external CLI worker.

## Resolve names before comparison

Search the exact product name first. If it is unverified, say so and record the interpreted product explicitly rather than silently correcting it. Pin current flagship model IDs from official provider documentation; do not infer “flagship” from community posts.

## Evidence hierarchy

For the local/current agent, collect live evidence where available:

- version, model/provider, authentication status without secrets;
- enabled toolsets and the tools actually present in the active prompt;
- installed skills and provenance;
- profiles, memory/session state, channels, schedules, and terminal backend;
- diagnostic warnings and optional dependencies;
- system-prompt and tool-schema overhead when supported.

For the comparator, prefer official docs, official repositories, provider model pages, and official pricing. Separate shipped capability from the user's configured and acceptance-tested state.

## Model-quality discipline

Never invent a head-to-head benchmark. If two frontier models lack a comparable independent test under the same harness, tools, data, budgets, and acceptance criteria:

- score the model layer as parity or “not established”;
- mark confidence low;
- move the decision to harness fit, configuration, operations, and scenario-specific acceptance tests.

Provider marketing claims support positioning, not superiority.

## Scenario-weighted matrix

Avoid one universal winner. Build at least two matrices when relevant:

- general-purpose / chief-of-staff work;
- software development with the intended native coding harness.

Use an exposed scale and formula, for example `weighted points = weight × rating / max rating`. Keep weights editable, include a confidence column, and label the output “expert fit assessment — not a model benchmark.” Treat differences smaller than the uncertainty of the evidence as practical parity.

Useful criteria include model fit, tool breadth, memory/recall, procedural skills, multi-agent routing, channels/nodes, security, interfaces, extensibility, operational complexity, native coding harness, repository context, worktree isolation, verification gates, and IDE/CI integration.

## Decision-ready deliverable

A strong report should contain:

- executive conclusion and explicit naming assumptions;
- verified snapshot of the current configured agent;
- capabilities, strengths, weaknesses, and operational debt;
- general and development comparisons;
- scenario-by-scenario recommendations;
- methodology, uncertainty, and source ledger;
- a clear conclusion that at roughly equal model capability, context, tools, permissions, skills, memory hygiene, orchestration, evals, observability, and recovery loops usually determine the real outcome.

## Spreadsheet-specific verification

For XLSX delivery:

- keep formulas and weights visible;
- provide literal chart-source summary values when a writer library cannot create cached formula results, or recalculate with a spreadsheet application;
- verify archive integrity, sheet/table/chart/hyperlink counts, formulas, and key cells;
- visually inspect at least the executive sheet in a real spreadsheet application;
- if the workbook is open and locked, save the corrected artifact under an unambiguous final filename rather than claiming the locked draft was updated.

Do not describe a workbook as visually verified when only ZIP/XML structure was checked.
