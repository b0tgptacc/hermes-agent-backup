---
name: design-first-development
description: Explore uncertain software design before planning or coding.
version: 1.0.0
author: Administrator, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, brainstorming, requirements, architecture, scoping]
    related_skills: [plan, spike, test-driven-development]
---

# Design-First Development

Turn an uncertain software request into a bounded, testable design. This is a
requirements-and-architecture skill, not an implementation plan and not a
mandatory ceremony for already-specified delegated work.

## When to Use

Use when a request has material uncertainty about behavior, scope, interfaces,
data flow, architecture, or acceptance criteria.

Do not use when:
- the delegated task already includes explicit acceptance criteria and constraints;
- the user asks for a pure mechanical change with one obvious reversible solution;
- diagnosing a defect (`systematic-debugging` owns that workflow);
- feasibility can only be learned by running an experiment (`spike` owns it);
- the solution is selected and only execution sequencing remains (`plan` owns it).

## Operating Modes

### Interactive mode

When the user is present and a material design choice is unresolved:

1. Inspect the project before asking questions.
2. Ask one question at a time, preferring concise choices.
3. Propose two or three credible approaches with trade-offs.
4. Lead with one recommendation.
5. Present a design scaled to the task and obtain approval before implementation.

Do not ask about information that can be established from files, tests, logs,
version control, or authoritative documentation.

### Delegated/autonomous mode

A delegation brief with explicit acceptance criteria counts as approval of the
requested outcome. Do not stall merely because no user is present.

- Inspect the project and record only material assumptions.
- Choose the simplest reversible design satisfying the brief.
- Escalate to the parent only if missing information changes a public contract,
  creates an irreversible migration, weakens security, or materially expands scope.
- Include the chosen design and assumptions in the completion report.

## Procedure

### 1. Inspect context

Use `search_files`, `read_file`, and read-only `terminal` commands to establish:
- repository structure and current behavior;
- project rules and architecture conventions;
- tests, build commands, and recent relevant changes;
- dependency versions and external contracts.

For version-sensitive library or framework behavior, query Context7 first. Use
web research only when Context7 lacks the library or the question is not API
documentation.

Completion criterion: every material question is classified as known, safely
assumed, or requiring a decision.

### 2. Bound the problem

State:
- user-visible outcome;
- in-scope and out-of-scope behavior;
- acceptance criteria;
- constraints and compatibility requirements.

If the request contains independent subsystems, decompose it and design only the
first coherent deliverable unless the brief explicitly authorizes the full scope.

Completion criterion: the work can be described as one coherent deliverable.

### 3. Compare approaches

When a meaningful choice exists, compare two or three options across:
- correctness and fit;
- operational complexity;
- security and failure behavior;
- testability and reversibility;
- maintenance cost.

Do not invent alternatives when only one sensible implementation exists.

Completion criterion: one recommended approach is selected with a concrete reason.

### 4. Produce the design

Cover only relevant sections:
- components and responsibilities;
- interfaces, inputs, outputs, and data flow;
- state and persistence;
- errors, validation, and recovery;
- security boundaries;
- test strategy and acceptance checks;
- rollout or migration when applicable.

For medium or large interactive work, save the approved design to
`docs/designs/YYYY-MM-DD-<topic>.md`. For small work, a short design note in the
response or plan is sufficient.

Completion criterion: an implementer can proceed without making a material design
decision not already captured.

### 5. Hand off without overlap

- If implementation spans multiple components, APIs, migrations, or more than
  roughly three files, load `plan` next and create the execution plan.
- If it is a small bounded feature, proceed directly with
  `test-driven-development`.
- If an empirical unknown blocks the design, use `spike`, discard the spike code,
  then return here and update the design.
- Never run `plan` and this skill as competing planning processes. This skill
  decides what to build; `plan` sequences how to build it.

## Overlap Contract

| Situation | Owning skill | This skill's role |
|---|---|---|
| Requirements or architecture unclear | `design-first-development` | Primary |
| Empirical feasibility unknown | `spike` | Define the question, consume verdict |
| Execution sequencing | `plan` | Provide approved design as input |
| New behavior implementation | `test-driven-development` | No concurrent process |
| Defect investigation | `systematic-debugging` | Only revisit design if root cause is architectural |
| Pre-commit quality gate | `requesting-code-review` | Supply acceptance criteria |
| Existing GitHub PR review | `github-code-review` | No role |

## Pitfalls

- Do not copy the original Brainstorming skill's universal approval gate into
  autonomous delegation; that deadlocks workers with complete briefs.
- Do not turn reversible, obvious changes into interview sessions.
- Do not let `spike` code enter production; rebuild through TDD after the verdict.
- Do not use Context7 as evidence for project-specific behavior; inspect the repo.
- Do not treat a design document as proof. Tests and runtime verification own proof.

## Verification

Before handing off:
- [ ] Current project context was inspected.
- [ ] Scope and acceptance criteria are explicit.
- [ ] Material assumptions are visible.
- [ ] Alternatives were compared only where a real choice existed.
- [ ] The selected design covers errors and tests.
- [ ] The next owning skill is unambiguous.
