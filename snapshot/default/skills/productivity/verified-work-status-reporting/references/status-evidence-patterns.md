# Status Evidence Patterns

Use these shapes as adaptable patterns, not fixed prose.

## Remediation in progress

```text
Current stage: reviewer-blocker remediation.
Verified delta: focused security checks 11/11 pass; focused financial checks 12/12 pass.
Full suite: still red — 29 passed, 2 failed, 5 errors.
Next gate: reconcile regressions, rerun the full suite, then rebuild Docker and re-review.
```

## Verification in progress

```text
Current stage: release verification.
Verified: full suite and migration drift check pass.
Remaining: clean-volume container startup and browser smoke.
Not yet accepted for delivery.
```

## Accepted

```text
Current stage: accepted for delivery.
Verified: full suite, production checks, clean Docker startup, authenticated E2E, and independent review all pass.
Remaining limitations: <explicit bounded caveats or none>.
```

## Blocked

```text
Current stage: blocked.
Completed evidence: <what is genuinely green>.
Blocker: <human decision, access, credential, or external dependency>.
Shortest continuation path: <one concrete action>.
```

## Evidence hierarchy

From weakest to strongest:

1. Worker narrative or process activity.
2. Artifact/file existence.
3. Focused deterministic check.
4. Full regression suite.
5. Runtime or clean-environment verification.
6. Browser/E2E acceptance.
7. Independent fail-closed review.

Higher evidence does not erase a contradictory lower-stage failure; resolve discrepancies before claiming acceptance.
