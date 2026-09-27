---
name: infrastructure-deployment-documentation
description: Use when turning infra notes into verified deployment docs.
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [documentation, infrastructure, deployment, architecture, security, runbook, acceptance]
---

# Infrastructure Deployment Documentation

Use this skill when a user provides a short outline, source document, diagram, or informal notes and expects a production-oriented deployment documentation package rather than a prose expansion.

## Deliverable standard

Default to a compact package in a new, clearly named directory:

- `README.md` — authoritative architecture and operating guide;
- `acceptance-checklist.md` — evidence-bearing GO/NO-GO checks;
- `architecture.html` — self-contained architecture diagram;
- `architecture-preview.png` — browser-rendered verification artifact when rendering is available.

Use the user's requested format when specified. If the source is a Word document, inspect the real document package for body text, tables, tracked changes, comments, and embedded media before drafting. Do not assume the visible paragraph extraction is complete.

## Workflow

1. **Inspect the source.** Extract its actual structure and identify every explicit stage, component, constraint, and omission. Preserve the source order as the backbone of the resulting guide.
2. **Define working assumptions.** State what is fixed by the source and what remains TBD. Do not invent hardware, domains, identities, model revisions, retention periods, SLOs, RPO/RTO, or regulatory applicability.
3. **Challenge unsafe shortcuts.** A direct connection that is acceptable for a pilot may be materially inferior for production. Distinguish the two and recommend a policy-enforcement gateway/backend when central authorization, audit, quotas, RAG ACLs, or tools are involved.
4. **Research current primary sources.** Prefer vendor documentation and standards. Register sources as they are retrieved, cite load-bearing claims inline, generate the source list mechanically, and run citation verification.
5. **Expand every source stage operationally.** For each stage cover prerequisites, configuration intent, network exposure, identity, secrets, validation, monitoring, rollback, owner, and acceptance evidence.
6. **Model trust boundaries.** Identify the single external entry point, management plane, application plane, inference plane, data plane, tool plane, and observability plane. Default internal services to no host publication and deny-by-default connectivity.
7. **Specify access, not just roles.** Include human roles, service identities, MFA/SSO, token audience and scope, break-glass, JIT administration, deprovisioning, and periodic access review.
8. **Make data controls explicit.** Cover classification, encryption, retention, log redaction, tenant boundaries, backup, restore, deletion propagation, and audit integrity.
9. **Treat AI tools as privileged execution.** Place RAG and tool calls behind deterministic policy. Require schema validation, least-privilege identities, sandboxing, bounded resources, and human approval for external, destructive, financial, or otherwise consequential actions.
10. **Build a real acceptance gate.** Tests must assert resulting state: blocked unauthenticated access, private internal ports, closed egress where required, cross-tenant isolation, recovery within RTO, rollback, alert delivery, and absence of prompts/secrets in routine logs.
11. **Render and inspect diagrams.** Syntax validation is not enough. Render in a real browser, inspect clipping, overlap, legibility, direction, and semantic correctness of every connector, fix defects, and render again.
12. **Verify the package.** Confirm every named file exists, local references resolve, code fences balance, required topics are present, citations pass, HTML parses, the PNG has valid dimensions, and checklist item counts are computed rather than estimated.

## Architecture diagram rules

- Draw connectors behind opaque component boxes.
- Define an intended edge list before drawing paths; compare it to the rendered result.
- Every arrow must terminate at a visible component and imply the correct direction.
- Route lines around unrelated nodes instead of through them.
- Do not add invisible or zero-sized placeholder elements to force layout.
- Use semantic colors consistently for edge/security, application, inference, data, tools, and operations.
- A second render is mandatory after any visual defect is corrected.

## Documentation content checklist

A production guide should normally include:

- purpose, scope, assumptions, and exclusions;
- recommended architecture and pilot-vs-production variants;
- sizing inputs and load-test requirement;
- host/container hardening and supply-chain controls;
- network flow matrix and published-port policy;
- authentication, authorization, service identities, and secrets;
- application/backend responsibilities;
- data/RAG lifecycle and tenant ACL enforcement;
- tool/MCP/SQL/file boundaries;
- monitoring, privacy-preserving logs, alerts, and SLOs;
- DoS/resource controls;
- backup, restore, update, canary, and rollback;
- incident response;
- phased implementation plan;
- GO/NO-GO acceptance tests;
- a table of unresolved decisions (`TBD`) with owners.

## Pitfalls

- **Merely rewriting bullets.** The user needs an executable operating standard, not longer prose.
- **Publishing internal APIs for convenience.** Bind inference, databases, vector stores, metrics, and tool servers only to private networks; expose a single authenticated gateway unless a documented exception exists.
- **Treating UI RBAC as the whole security model.** Downstream services and tools still require least-privilege identities and independent policy enforcement.
- **Using system prompts as security controls.** Authorization, ACLs, schemas, resource limits, and approvals must remain deterministic and external to the model.
- **Counting a successful file write as completion.** Verify structure and critical content; render visual artifacts.
- **Trusting the first diagram render.** Connector errors often survive syntax checks and materially misstate architecture.
- **Hand-writing citation lists.** Generate and verify them from the retrieval ledger.
- **Hard-coding unapproved versions or fake secrets.** Use clearly named required variables/TBDs and fail-closed examples.

## Supporting references

- `references/local-ai-stack-pattern.md` — condensed Ollama/Open WebUI/RAG/MCP production pattern and security boundaries.

## Completion report

Report the output directory, files created, major decisions encoded, and verification actually performed. Distinguish structural verification from live deployment verification. Never imply that documentation proves the infrastructure itself has been deployed or tested.
