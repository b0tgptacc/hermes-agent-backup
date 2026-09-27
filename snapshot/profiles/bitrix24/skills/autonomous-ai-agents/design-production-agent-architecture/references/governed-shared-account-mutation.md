# Governed shared-account mutation dispatcher

Use this pattern when an Administrator deliberately chooses one centrally managed design-service identity but still needs real canvas creation/editing.

## Control shape

Require every invocation to carry:

- requester identifier;
- stable task ID;
- exact existing artifact URL, or an explicit new-artifact declaration such as `NEW:DESIGN:<name>` / `NEW:SLIDES:<name>`;
- task prompt or a prompt file constrained to the approved staging workspace.

Reject malformed targets before agent startup. Prefix the dispatched request with the validated identity/task/target and the external-write contract.

## Exact target validation

A URL-prefix regex is insufficient: it can accept an empty key, trailing junk, whitespace/control characters, or a hostile prompt suffix. Parse the complete URL with a standard URL parser and require:

- HTTPS and an exact approved hostname;
- no userinfo, password, custom port, or fragment;
- an approved artifact kind (`design`, `slides`, and legacy `file` only when required);
- a nonempty syntactically valid file key (the validated Figma deployment used 10–128 ASCII alphanumeric characters);
- no whitespace/control characters in decoded path suffixes or query text.

For `NEW:DESIGN:` / `NEW:SLIDES:`, require a trimmed, nonempty, bounded visible name while allowing ordinary internal spaces. Validate requester/task metadata separately so it cannot inject dispatcher fields.

Regression tests must reject missing and short keys, trailing whitespace/junk, hostile hosts, userinfo/port/fragment, newline/control injection, unsupported artifact kinds, and empty/whitespace NEW names. Include positive existing Design/Slides URLs and NEW names with normal spaces.

## Serialization

Hold one lock for the entire agent process, not merely for individual mutation calls. A global lock is conservative but avoids unknown-file/new-file races and is often preferable for a shared identity with modest throughput.

On Windows, use a named kernel mutex (`CreateMutexW` + `WaitForSingleObject`) rather than assuming a text-file byte lock is cross-process reliable. Treat `WAIT_OBJECT_0` and `WAIT_ABANDONED` as acquisition, `WAIT_TIMEOUT` as a blocked task, and always `ReleaseMutex`/`CloseHandle` in `finally`.

## Audit ledger

Append START and END records while holding the lock. Include timestamp, requester, task ID, exact target, local OS actor, prompt SHA-256, exit code, and previous-record hash. Compute each record hash from canonical sorted JSON before appending.

Do not store prompt plaintext, credentials, tokens, document contents, or screenshots in the ledger. Protect its directory with least-privilege ACLs and exclude it from broad employee modification.

A local hash chain is tamper-evident operational evidence. It is not vendor-native attribution or an immutable external audit service; an administrator with filesystem control can rewrite both records and hashes.

## Deterministic acceptance

Prove all of these:

1. malformed target is rejected before launch;
2. valid dry-run writes paired START/END records;
3. a second process times out while another process holds the named mutex;
4. every `previous_hash` and `record_hash` recomputes correctly;
5. plaintext prompts and secrets are absent;
6. the launcher invokes only the intended specialist profile;
7. mutation tools are present only after the dispatcher control is active;
8. OAuth/live mutation remains a separate human and disposable-file acceptance gate.

## Capability principle

Once the dispatcher passes and the Administrator accepts the residual attribution model, expose the minimum mutation set that can actually deliver the approved creative outcome. Do not remove canvas creation, iterative editing, typography/layout/image work, or authorized asset upload merely to make governance easier; govern those operations through target scope, locking, destructive confirmation, and post-write verification.
