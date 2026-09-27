# Optimistic concurrency and append-only financial history

Use this extension when saved calculator scenarios can be edited, finalized, quoted, exported, or audited later.

## Concurrency rule

A row lock alone does not prevent lost updates when the caller holds a stale model instance. Inside the save transaction:

1. lock the current database row;
2. compare the caller's expected revision to the locked revision;
3. reject a mismatch before recalculation, hashing, or finalization;
4. return a user-visible conflict error rather than refreshing stale inputs and overwriting the newer state.

Test with two separately loaded instances: save one to revision `N+1`, then attempt to finalize the stale `N` instance. The newer DRAFT, outputs, and history must remain unchanged.

## Full-chain integrity

Checking only the latest revision misses concealed lower-number inserts. Validate the complete ordered history:

- row count equals the main record's revision number;
- revision numbers are exactly contiguous `1..N`;
- every input and output snapshot matches its stored hash;
- every snapshot's formula version matches the revision metadata;
- the latest revision matches the main record's snapshots, hashes, and formula version.

Any history-chain damage must fail closed for both DRAFT and FINAL. Do not append a repair revision onto damaged history.

## Append-only enforcement

Layer the controls:

- model instance save/delete refusal;
- QuerySet update/delete refusal;
- `PROTECT` from revision to calculation so deleting a parent cannot erase history;
- production-database `BEFORE UPDATE` and `BEFORE DELETE` triggers;
- read-time full-chain validation before financial detail/PDF output.

Triggers permit INSERT because normal saves append revisions; the full-chain check detects extra, hidden, gapped, or malformed inserts. Ordinary hashes and triggers protect application/DML integrity, not a privileged database owner with DDL access. Use an external signed ledger if that stronger threat model is required.

## Migration safety

Vendor-specific trigger syntax differs. PostgreSQL reversal requires:

```sql
DROP TRIGGER IF EXISTS trigger_name ON table_name;
```

SQLite uses table-less `DROP TRIGGER IF EXISTS trigger_name`. Exercise migrations backward and forward on the real production database engine, not only by inspecting generated operations.

Backfilled history must use an explicit disabled system/unknown actor, never falsely attribute the migration to the calculation owner.

## Side-effect-free production probes

Wrap smoke probes in an outer transaction and force rollback after assertions. PostgreSQL foreign keys may be deferred, so after a raw parent DELETE execute `SET CONSTRAINTS ALL IMMEDIATE` inside the savepoint to test rejection before the outer rollback. Verify afterward that no QA calculations or users remain.

A production probe should cover stale save rejection, ORM/raw revision mutation rejection, protected parent deletion, hidden-insert detection, system migration actor, and zero residual QA state.
