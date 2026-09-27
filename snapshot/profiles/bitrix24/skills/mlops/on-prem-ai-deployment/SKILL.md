---
name: on-prem-ai-deployment
description: "Use when designing or documenting on-prem AI serving."
version: 1.0.0
platforms: [linux, windows, macos]
metadata:
  hermes:
    tags: [on-prem, local-ai, llm-serving, security, access-control, runbook, vllm, llama-cpp]
---

# On-Prem AI Deployment

Use this skill to design, document, review, or prepare acceptance criteria for locally hosted generative-AI inference: a workstation, a dedicated GPU server, or a multi-node cluster.

## Default outcome

Unless the user specifies another format, produce a small documentation package rather than a single essay:

1. `README.md` — scope, architecture, deployment, security, operations, and decisions still required.
2. `acceptance-checklist.md` — binary GO/NO-GO checks with owners and exception handling.
3. An architecture diagram plus a rendered preview when diagram tooling is available.

State material assumptions. Do not pretend that a vendor-neutral template is ready for production before hardware, model revision, identity provider, data classes, SLOs, and regulatory requirements are supplied.

## Workflow

### 1. Define scope and trust boundaries

Capture or infer conservatively:

- use cases and prohibited decisions;
- users, applications, administrators, and service identities;
- data classes and retention;
- target hardware and operating system;
- concurrency, context length, output limits, and SLOs;
- whether RAG, multimodal input, or tools/agents are included;
- RPO/RTO and availability requirements.

For a generic request, use a clearly labeled baseline: Linux server, GPU-backed serving, corporate IdP, private network, HTTPS gateway, immutable model artifacts, and no outbound network from inference by default.

### 2. Choose the simplest fitting deployment class

- Workstation / single user: `llama.cpp` or equivalent local runtime, bound to localhost.
- Shared single server: vLLM or equivalent behind an authenticated gateway; Docker or systemd.
- Cluster: Kubernetes only when multi-node scaling, rolling updates, hard tenant separation, or established cluster operations justify it.

Do not introduce Kubernetes merely for hypothetical future growth.

### 3. Size with formulas, then benchmark

Use model weights only as a lower bound:

```text
weight_memory_GB ≈ parameter_billions × quantization_bits / 8
```

Add explicit runtime headroom and separately account for KV cache, context length, batching, concurrency, framework overhead, and multimodal components. Any numerical example must be calculated with a tool. Final procurement guidance must depend on a load test using the exact model, quantization, runtime, and traffic profile.

### 4. Design the access path

Recommended path:

```text
user/application -> HTTPS gateway -> policy/quotas -> private inference runtime
                                      |                 |
                                     IdP         read-only model registry
                                                        |
                                                 metrics/audit/SIEM
```

Apply Zero Trust principles:

- LAN membership or source IP is not authentication;
- validate token signature, issuer, audience, expiry, and groups;
- use RBAC/ABAC at the gateway;
- separate user, service, administrator, auditor, and break-glass identities;
- use short-lived credentials or mTLS for services;
- make inference ports unreachable from user networks;
- restrict administrative access through bastion/PAM/VPN with MFA and JIT access.

### 5. Secure the model and software supply chain

Record for every model and runtime artifact:

- immutable repository revision/commit;
- exact filenames and SHA-256 values;
- format, model card, license, and use restrictions;
- source and approval owner;
- malware/vulnerability scan results;
- quality, privacy, prompt-injection, and safety evaluation results;
- container digest and SBOM;
- previous approved rollback version.

Prefer `safetensors` or GGUF. Treat pickle deserialization and remote model code as code execution risks. Disable `trust_remote_code` by default; exceptions require source review, a fixed revision, an isolated build environment, and no secrets. Mount approved models read-only and forbid user-driven dynamic model loading.

### 6. Harden serving and containers

Baseline controls:

- gateway is the only published endpoint;
- deny-by-default firewall and outbound egress;
- immutable image by digest, read-only root filesystem, `no-new-privileges`;
- no privileged mode, host PID/IPC/network, or Docker socket;
- drop capabilities and add back only tested necessities;
- explicit writable cache/tmpfs mounts sized for the runtime;
- CPU, RAM, PID, context, body, rate, concurrency, media, and token limits;
- model directory read-only;
- secrets injected from a secret manager, never committed or placed in prompts;
- internal distributed ports isolated, especially for PyTorch/vLLM multi-node traffic.

A hardened command must still be runnable. If rootfs is read-only, provide writable cache locations and set runtime cache environment variables. Use shell variables with `: "${VAR:?message}"` for required deployment-specific values instead of angle-bracket placeholders that the shell interprets as redirection.

### 7. Cover LLM-specific controls

- System prompts are not security boundaries.
- Treat retrieved documents, web pages, email, and user uploads as untrusted data.
- Enforce data authorization outside the model.
- Apply source ACLs before RAG retrieval; propagate deletion to chunks and embeddings.
- Validate model output before SQL, shell, HTML, API, or workflow use.
- Give tools separate least-privilege identities.
- Require human approval for external, destructive, financial, publication, or messaging actions.
- Limit tool calls, execution time, object counts, and transaction value.
- Fail closed on ambiguous authorization or policy failures.

### 8. Make operations explicit

Document:

- metrics: availability, queue, p95/p99 latency, TTFT, tokens, GPU/VRAM/temperature/ECC, OOM, auth denials;
- privacy-preserving logs: identity, policy decision, model revision, correlation ID, latency, token counts, result code — not full prompts, responses, secrets, or source documents by default;
- alerting and escalation owners;
- backups by object type, RPO/RTO, and tested restoration;
- immutable promotion, staging evaluation, canary, observation window, and rollback;
- incident playbooks for credential compromise, prompt/response leakage, poisoned RAG, model/image compromise, and denial of service.

### 9. Build acceptance tests

Include checks for:

- unauthenticated, expired, wrong-issuer, and wrong-audience requests are denied;
- user cannot reach inference or administrative endpoints directly;
- service identity cannot exceed its model/endpoint scope;
- inference egress and distributed ports are blocked;
- oversized context/body/media and excessive parallelism are rejected before inference;
- indirect prompt injection cannot change policy;
- cross-tenant or unauthorized RAG retrieval fails;
- model output is not executed without validation;
- break-glass use alerts;
- restart, overload behavior, backup restoration, canary, and rollback are demonstrated.

## Evidence and citations

For claims about current runtime behavior or security limitations, use authoritative upstream documentation and the `grounded-citations` workflow. Prefer NIST for risk/Zero Trust, OWASP GenAI for LLM threats, official runtime documentation for endpoints and limitations, official container/orchestrator security guidance, and model-host security documentation for serialization risks.

Do not cite generic recommendations as if they were mandated standards. Distinguish sourced facts, architectural recommendations, assumptions, and organization-specific decisions.

## Artifact verification

Before delivery:

1. Verify all expected files exist and local links resolve.
2. Parse HTML structurally and check balanced Markdown code fences.
3. Run citation verification.
4. Render diagrams in a real browser and inspect the image for clipping, overlaps, orphaned arrows, wrong arrow direction, and logically false connections.
5. When an interactive browser cannot attach because approval/setup is required, use an installed browser's supported headless screenshot mode as a non-interactive fallback; verify the generated image rather than declaring the diagram good from HTML parsing alone.
6. Count checklist items and confirm every requested topic is present.

## Pitfalls

- Treating local hosting as proof of confidentiality.
- Exposing vLLM/llama.cpp directly because an API key exists.
- Logging prompts and responses by default.
- Using model file size as procurement sizing.
- Publishing `latest` images or mutable model revisions.
- Enabling remote code, dynamic LoRA/model loading, tools, or media URL fetching without a threat review.
- Producing a security checklist with no read-back, load test, restore test, or rollback test.
- Supplying shell snippets with `<PLACEHOLDER>` tokens that become redirections when copied.
- Applying `read_only: true` without writable runtime/Hugging Face/Triton caches.
- Creating a visually polished diagram without checking whether arrows actually connect the intended components.

## Supporting material

- `references/secure-serving-baseline.md` — concise control matrix, role matrix, and verification patterns for local LLM serving.
