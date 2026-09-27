# Cross-profile handoff security review

Use this checklist when a research/evidence agent emits a structured packet that an implementation agent will consume. Treat the packet as an untrusted boundary object even when both profiles belong to the same operator: retrieved web content can influence the producer.

## Boundary invariants

1. **Paths are capabilities.** Evidence and artifact paths must be normalized, workspace-relative, and contained under the task handoff directory. Reject absolute paths, drive-qualified paths, UNC paths, `..` traversal, symlink/junction escapes, and paths that resolve outside the approved root. Schema patterns help, but the consumer must canonicalize and verify containment before reading.
2. **Commands are proposals, not authority.** A producer may describe expected acceptance behavior, but the implementation owner must re-derive executable commands from the live repository and its project contract. Never execute command strings directly from a handoff. Prefer structured test intent (`kind`, `target`, `expected`) over shell text; if shell text is retained, mark it `non_authoritative: true`.
3. **Cross-references need semantic validation.** Verify every claim's evidence IDs exist, every evidence hash matches the contained file, quoted text occurs at the declared locator, timestamps/cutoffs are coherent, and target hints remain explicitly non-authoritative.
4. **Audit ledgers must prove work.** Require non-empty changed-file, command-result, and review arrays when the workflow claims execution. Use typed hash fields (`algorithm`, `artifact_kind`, full digest), bind review verdicts to the same artifact identity, and distinguish commit SHA from dirty-diff hash.
5. **Avoid self-referential hashes.** Hash the implementation artifact manifest, not a ledger that contains its own hash. State exactly which paths and separators are included in the digest algorithm.

## Negative fixtures

A schema or validator is incomplete unless these fixtures fail:

- evidence path is `C:/Users/.../.env`;
- evidence path is `../../private-file`;
- evidence path escapes through a symlink/junction;
- acceptance command is an environment dump, destructive shell command, or network write;
- claim references an unknown evidence ID;
- quote is absent from the hashed evidence body;
- ledger has empty `changed_files`, `commands`, or `review_verdicts`;
- result hash is a short placeholder rather than a full digest;
- an extra MCP server appears outside the approved server set;
- a stale tool example exists in a supporting reference or script rather than SKILL.md.

Run negative fixtures entirely in memory or against disposable fixtures; do not read real secret files or execute the malicious command strings.

## Validator coverage

Architecture validators should assert exact capability sets, not just selected members:

- exact MCP server names and enabled transports;
- exact tool allowlists plus prompts/resources/sampling state;
- isolation/headless flags where relevant;
- no competing native toolset owner;
- all policy surfaces: config, SOUL, PROFILE, SKILL.md, references, schemas, scripts, and tests;
- positive and negative schema fixtures;
- preserved acceptance artifacts for every stated gate.

A passing happy-path demo proves compatibility, not boundary safety. Pair it with adversarial fixtures and report missing live/network checks as residual risk rather than silently treating them as passed.
