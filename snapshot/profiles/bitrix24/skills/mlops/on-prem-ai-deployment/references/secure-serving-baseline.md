# Secure serving baseline

Use this reference while preparing a concrete deployment document. It is a control inventory, not a substitute for an organization-specific threat model.

## Deployment-class decision

| Condition | Default |
|---|---|
| One user, local files, no shared API | llama.cpp bound to localhost |
| Shared GPU server, one failure domain | vLLM-equivalent behind gateway; Docker/systemd |
| Multi-node HA or established platform team | Kubernetes with namespace/network policy controls |

## Required trust boundaries

1. User network → HTTPS gateway.
2. Gateway → private inference network.
3. Staging downloader → approved model sources.
4. Inference → read-only model storage.
5. Monitoring → metrics endpoints.
6. Administrators → bastion/PAM → management plane.

Default deny between boundaries. Inference has no Internet egress unless an approved use case proves it necessary.

## Role matrix

| Role | Required access | Explicit exclusions |
|---|---|---|
| Service owner | approve purpose, SLA, model | host administration |
| Security | policy, threat model, audit | routine prompt reading |
| Platform administrator | host, GPU, runtime, gateway | end-user impersonation |
| Model curator | stage/evaluate artifacts | unilateral production promotion |
| Auditor | read-only changes/access records | configuration mutation |
| User | allowed inference endpoints/models | administrative endpoints |
| Service identity | fixed scope and quota | interactive login/shared credentials |

Use separation of duties for production promotion and break-glass for emergencies only.

## Minimum control matrix

| Layer | Preventive controls | Detective/verification controls |
|---|---|---|
| Identity | OIDC/mTLS, MFA, RBAC/ABAC, short-lived credentials | denied-request metrics, quarterly review, revocation test |
| Network | gateway-only ingress, deny egress, isolated distributed ports | reachability tests from each trust zone |
| Host | supported LTS, disk encryption, SSH keys, bastion | patch/ECC/SMART/temperature alerts |
| Container | digest pin, read-only rootfs, no privilege/host namespaces/socket | image scan, SBOM, runtime config inspection |
| Model | immutable revision/hash, safe format, read-only mount | malware scan, hash drift alert, evaluation record |
| RAG | pre-retrieval ACL, tenant isolation, deletion propagation | cross-tenant negative tests, source traceability |
| Agents | minimal tools/identities, schema validation, human approval | tool audit, limit/rollback tests |
| Availability | rate/context/token/media limits, quotas | overload returns 429/503 without host OOM |
| Recovery | reproducible artifacts, protected backups | restore and rollback exercises |

## Runnable hardened-snippet pattern

Avoid shell angle-bracket placeholders. Use required variables:

```bash
: "${APPROVED_IMAGE:?set immutable image digest}"
: "${CONTEXT_LIMIT:?set tested context limit}"
```

For a read-only inference container, explicitly provide writable ephemeral caches, for example:

```text
/tmp
/var/cache/runtime
/var/cache/model-hub
```

Set runtime-specific cache environment variables to those mounts. Confirm permissions with the actual image because forcing an arbitrary UID can break GPU/runtime access.

## Logging baseline

Record:

- timestamp and correlation ID;
- user/service identity;
- policy decision and version;
- model name and immutable revision;
- endpoint, token counts, latency, result code;
- administrative changes and break-glass use.

Do not record full prompts, responses, source documents, secrets, system prompts, or chain-of-thought by default. Any temporary content logging needs approval, masking, restricted access, encryption, and automatic expiry.

## Diagram review checklist

- Every arrow starts and ends on the intended component.
- Direction matches data/control flow.
- User traffic cannot appear to bypass the gateway.
- IdP connects to the enforcement point, not directly to inference.
- Model registry and monitoring directions are understandable.
- RAG and bastion lines do not imply an unintended trust relationship.
- Zone labels, captions, arrows, and boxes do not overlap at desktop width.
- A headless or interactive browser render is visually inspected; HTML parsing alone is insufficient.

## Final evidence package

Attach or reference:

- approved architecture and data-flow diagram;
- model/runtime inventory with hashes and licenses;
- access matrix;
- load-test report and SLO decision;
- vulnerability/SBOM results;
- negative security-test results;
- restore and rollback evidence;
- signed GO/NO-GO checklist and accepted exceptions.
