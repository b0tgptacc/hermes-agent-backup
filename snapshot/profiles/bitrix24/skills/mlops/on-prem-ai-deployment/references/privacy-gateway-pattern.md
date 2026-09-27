# Privacy gateway pattern for local LLM → cloud LLM

Use this pattern when sensitive documents must be processed locally before a cloud model is called and later restored without silent corruption.

## Core decision

Do not use a generative model as an encryption, anonymization, or decryption primitive. The model may assist entity detection, but cryptography, policy, token integrity, egress checks, and restoration must be deterministic code outside the model.

Call the mechanism **reversible pseudonymization**, not encryption or irreversible anonymization:

```text
local parse
  -> deterministic recognizers + local NER/LLM detector
  -> validate/merge spans
  -> opaque integrity-protected tokens
  -> AEAD-encrypted local token vault
  -> outbound leak scan
  -> cloud LLM
  -> response schema/token validation
  -> deterministic restoration
  -> format-specific patch + new revision
```

The cloud must never receive the original binary, token map, vault key, or unsanitized observability traces.

## Fail-closed invariants

- Low-confidence, ambiguous, invalid, or overlapping spans block cloud processing or require human review.
- Model-provided offsets are untrusted. Prefer exact substring + occurrence; resolve positions in code.
- Any unknown, invented, malformed, translated, or split placeholder rejects the cloud response.
- Run an independent outbound DLP scan after all transformations and before egress.
- Prompts are guidance, not a security boundary; document content is untrusted and may contain indirect prompt injection.
- The local inference runtime has no outbound network. Only the policy gateway has allowlisted cloud egress.
- Prompt/response bodies, plaintext mappings, and vault material are excluded from logs, traces, crash reports, and metric labels.

## Token vault

Recommended properties:

- opaque random token per request, with an integrity tag;
- no cross-document stable identifiers unless explicitly required and risk-approved;
- AES-256-GCM or another approved AEAD;
- unique nonce and AAD binding tenant, request, and policy version;
- envelope key from KMS/HSM, rotation, and short TTL;
- vault deletion after success/expiry;
- immutable audit metadata without content.

## Document fidelity

Do not ask the cloud model to rewrite an entire office file. Parse locally, assign stable fragment IDs, and require schema-constrained patch operations such as `replace_text(fragment_id, expected_hash, new_text)`.

- Preserve the immutable original and write a new revision.
- A no-op path should preserve the original hash or use a documented deterministic normalization.
- Verify non-target XML parts, formulas, relationships, styles, comments, headers, and embedded objects.
- Render representative DOCX/PPTX/PDF outputs and perform visual diff.
- Treat OCR and PDF rewriting as potentially lossy. Low-confidence OCR should be local-only or human-reviewed.
- A modified document cannot be byte-for-byte identical to the original; define fidelity as unchanged non-target structures plus verified visual/semantic equivalence.

## Local model harness

For the detector role:

- temperature 0, thinking disabled;
- constrained JSON Schema output;
- model returns exact substring, entity type, occurrence, and confidence;
- code resolves and validates spans;
- union model output with deterministic recognizers and specialized NER;
- quantization is accepted only after per-entity recall regression tests.

The detector must not own KMS access, cloud credentials, or restoration privileges.

## Decision-only models (Laya/Jev class)

System-One/decision models are separate classifiers, not Qwen/LLM inference accelerators.

- They cannot replace arbitrary span extraction, cryptography, vaulting, or output integrity validation.
- A hosted decision model must not receive raw confidential data before the privacy boundary.
- A local decision model can be evaluated for risk routing or escalation, but it must not independently grant `safe_to_cloud` or bypass the primary detector.
- Benchmark on private, language- and format-representative data; measure per-class recall, calibration, p50/p95 latency, and end-to-end false negatives against a no-router baseline.

## GPU/runtime choice

For a 27B-class model, compute weight memory first (27B is about 54 GB at 16-bit, 27 GB at 8-bit, 13.5 GB at 4-bit), then add KV cache, batching, framework, and context overhead.

- Record exact GPU memory (for example A100 40 vs 80 GB) and topology (NVLink vs PCIe); two visible GPUs do not prove NVLink.
- Prefer TP=2 for models/long context that do not fit safely on one GPU.
- Prefer independent replicas for throughput when one replica fits and long context is not the bottleneck.
- Start with a bounded context and chunk documents with overlap/layout IDs. Enable very long context only after an exact-model load test.

## Acceptance tests

At minimum verify:

1. Unicode exact round-trip for all supported scripts.
2. Tampered vault, wrong key/AAD, and cross-tenant substitution fail.
3. Unknown or damaged placeholders fail.
4. Outbound captures contain zero known secrets on the acceptance corpus.
5. Credentials/private keys are blocked with no bypass.
6. No-op document paths preserve hash or documented normalization.
7. Targeted edits leave non-target structures unchanged and pass visual diff.
8. Encoded, multilingual, homoglyph, RTL, zero-width, and split prompt-injection fixtures cannot change policy or egress.
9. Overload/OOM returns a bounded failure and never falls back to unsanitized cloud processing.
10. Restore, rollback, key rotation, canary, and incident drills are demonstrated.

Status remains **pilot** until these gates pass on the exact model revision, runtime, VM/GPU topology, document formats, KMS, IdP, DLP, and contracted cloud data controls.