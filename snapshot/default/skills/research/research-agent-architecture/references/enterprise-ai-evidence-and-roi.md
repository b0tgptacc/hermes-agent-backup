# Enterprise AI use-case research: evidence and ROI

Use this note when researching office copilots, knowledge-work automation, or departmental AI use cases.

## Evidence ladder

Keep these categories separate in the final report:

1. **Randomized/controlled task evidence** — supports causal claims for the tested task and population only.
2. **Field experiment with operational outcomes** — stronger external validity, but still process- and organization-specific.
3. **Large deployment with telemetry plus surveys** — useful for adoption and use-case discovery; self-reported time savings are not causal productivity gains.
4. **Case study or vendor/customer testimonial** — hypothesis-generating only.
5. **Product capability or marketing claim** — proves availability, not realized benefit.

Never transfer a percentage improvement from writing or customer support to meetings, spreadsheets, finance, HR, or legal work without direct evidence. State where domain-specific evidence is sparse.

## Practical prioritization

Score each use case on:

- frequency and baseline labor cost;
- reversibility of mistakes;
- output verifiability;
- data sensitivity and access complexity;
- integration depth;
- regulatory and decision-rights risk.

Default rollout order:

1. Frequent, reversible, human-reviewed drafts and summaries.
2. Citation-backed enterprise search and structured extraction.
3. Deterministic workflows with an LLM interface or explanation layer.
4. Tool-using agents with approvals and bounded permissions.
5. High-impact employment, finance, or legal decisions only as decision support, never an unsupervised first deployment.

## ROI measurement

Measure at the process level, not by prompts, generated tokens, or licenses assigned.

`Annual benefit = eligible volume × accepted net time saving × loaded labor cost + avoided error/outsourcing cost`

`Net ROI = (benefit - license - integration - training - review - incident cost) / total cost`

Use **net time saving**: generation time plus verification and correction. Track cycle time, throughput/FTE, backlog/SLA, first-pass yield, errors per 100 outputs, critical errors, acceptance without material edits, active use on eligible tasks, review burden, and cost per successful transaction.

Prefer a baseline plus randomized, stepped-wedge, or matched-control rollout. Treat self-reported time savings and satisfaction as supporting metrics, not booked financial value. Verify whether released time became throughput, lower backlog, fewer overtime hours, or avoided spend.

## Architecture patterns to recommend

- Embedded copilot with no automatic external send.
- ACL-aware RAG with citations and an explicit `not found` path.
- Deterministic calculation/record system plus LLM query and explanation shell.
- Document intelligence pipeline: OCR/layout, schema extraction, business validation, exception queue, approval, system write.
- Human-in-the-loop workflow: `draft -> validate -> approve -> execute`.
- Bounded agent: tool allowlist, read-only default, idempotency, transaction limits, audit log, rollback.
- AI control plane: model routing, DLP/PII controls, prompt and model versioning, eval sets, tracing, quotas, and incident handling.

## Reporting pattern

For every headline number, label:

- study design and sample;
- task and population;
- measured versus self-reported outcome;
- causal versus correlational status;
- transferability limitation;
- source funding or vendor involvement when material.

A useful final matrix is `use case | expected effect | complexity | evidence strength | risk | recommended autonomy level`.