# Local AI stack pattern: Ollama + Open WebUI + RAG + tools

Use this reference when a terse source outline names a local LLM runtime, chat UI, RAG, tools, and monitoring but does not define production trust boundaries.

## Recommended production path

```text
Users/apps -> VPN/LAN -> HTTPS gateway -> SSO/OIDC + policy
           -> Open WebUI -> AI backend/tool broker -> Ollama
AI backend -> PostgreSQL (history, ACL, audit metadata)
AI backend -> RAG service -> Qdrant
AI backend -> isolated MCP/SQL/file tools
Prometheus/Grafana/SIEM <- technical metrics and redacted events
```

Pilot may use `Open WebUI -> Ollama` on one private Docker network. Production should insert an AI backend/gateway when it needs central authorization, quotas, history, RAG ACL enforcement, or tool approvals.

## Non-negotiable boundaries

- Do not publish Ollama port 11434 to user or untrusted networks; its local API is not a complete production authentication boundary.
- Publish one HTTPS entry point. Keep PostgreSQL, Qdrant, Prometheus/exporters, Ollama, and MCP servers on private networks.
- Disable inference egress after approved model acquisition when local-only processing is required; verify this with network evidence while inference still succeeds.
- Pin container images by digest and model artifacts by immutable revision/hash; retain the previous compatible set for rollback.
- Open WebUI SSO/RBAC does not replace downstream least privilege. Service identities for backend, retrieval, and tools must be independently scoped.
- Keep `WEBUI_SECRET_KEY` stable across container recreation and source it from secrets management.
- Design Open WebUI groups as positive grants: additive permission systems cannot express a reliable deny by adding another group.
- Enforce RAG ACLs before retrieval from verified identity, never from user-supplied prompt metadata.
- Self-hosted vector stores need private binding plus authentication/TLS/audit where supported; query identities should be read-only or collection-scoped.
- PostgreSQL runtime identities must not own protected tables or hold `BYPASSRLS`; test cross-user and cross-tenant denial explicitly.
- MCP servers must validate token audience/scope and must not pass the client's token through to downstream APIs. Remote MCP uses HTTPS; stdio servers run sandboxed.
- SQL tools use read-only roles/views, allowlists, statement timeouts, and row limits. Do not execute arbitrary model-generated SQL.
- File tools receive a dedicated root, canonical-path validation, traversal/symlink defenses, and read-only access by default.
- Require human approval for write, delete, send, publish, payment, or other consequential actions.
- Routine logs and metrics exclude prompts, responses, retrieved chunks, document bodies, secrets, and sensitive tool results.

## Acceptance evidence

Collect evidence for:

1. unauthenticated/unauthorized requests rejected;
2. only gateway:443 reachable from the user segment;
3. Ollama inference succeeds with egress blocked;
4. cross-tenant chat/RAG access denied;
5. tool calls denied without required scope/approval;
6. overload returns controlled 429/503 rather than host OOM;
7. prompts and secrets absent from normal logs/metrics;
8. backup restore meets RPO/RTO;
9. rollback restores the previous runtime/model/policy set;
10. alerts actually reach and are acknowledged by on-call.

## Diagram review edge list

Define and visually verify at least these logical edges:

- Users/apps -> HTTPS gateway
- IdP -> gateway authorization
- Gateway -> Open WebUI/backend
- Open WebUI -> backend
- Backend -> Ollama
- Backend -> PostgreSQL
- Backend -> RAG service -> Qdrant
- Backend/tool broker -> each isolated tool
- Monitoring -> service metrics endpoints
- Backend/services -> redacted audit/log pipeline

An arrow that passes through a node can falsely imply the node is its source. Route connectors around unrelated boxes and re-render after correction.
