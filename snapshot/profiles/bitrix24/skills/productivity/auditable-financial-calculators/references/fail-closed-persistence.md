# Fail-closed persistence for financial calculators

Use this when saved calculations affect quotes, approvals, tax/customs scenarios, or historical reporting. Correct formulas alone are insufficient: persisted inputs and outputs must remain reconstructible and resistant to silent drift.

## Persistence contract

Store alongside the calculation:

- canonical input snapshot;
- canonical calculated-output snapshot;
- formula version and calculation timestamp;
- deterministic hashes of both snapshots;
- revision number and immutable revision rows;
- finalization timestamp;
- source-calculation lineage for clones;
- actual change actor, not merely the record owner.

Canonicalize Decimal values to each field’s declared precision, dates to ISO strings, and JSON with sorted compact keys before SHA-256 hashing. Hashes detect accidental/application-level drift; they are not signatures against a malicious database administrator.

## Save and revision behavior

1. Lock the current row in a transaction.
2. Validate inputs before arithmetic.
3. Recalculate through the single canonical engine.
4. Build canonical input/output snapshots and hashes.
5. Treat a no-op save as no new revision and preserve its original calculation timestamp.
6. For a changed state, increment the revision and append an immutable revision row in the same transaction.
7. Attribute the revision to the authenticated editor. Pass the actor through normal CRM forms, automatic repair paths, and admin saves; only fall back to owner for internal jobs that have no authenticated actor.

A revision should include calculation ID, revision number, actor, input/output snapshots, hashes, formula version, and timestamp. Prevent update/delete through model and admin APIs. If stronger evidence against privileged DB writers is required, use an external append-only ledger or signed/HMAC records; ordinary hashes are not enough.

## FINAL lifecycle

- DRAFT → FINAL is allowed and stamps `finalized_at`.
- A persisted FINAL record is immutable through normal model, form, view, and admin paths.
- Editing requires cloning; clones reset to DRAFT and retain source lineage.
- Do not silently repair a FINAL record whose inputs, outputs, snapshot, or hash differ. Block detail/export with a clear integrity response (for example HTTP 409).
- A drifted DRAFT may be recalculated and repaired, but the repair must create a new revision attributed to the user who triggered it.

## Database constraints

Application validation is necessary but not sufficient because bulk update, raw SQL, migrations, and administrative scripts can bypass `save()`.

Add database checks where expressible:

- quantity > 0;
- physical drivers and money inputs >= 0;
- FX rates NULL or > 0;
- bounded percentages (including exact upper-bound tests);
- conditional margin < 100;
- conditional duty bounds;
- weight/volume requirements for nonzero rate × driver modes.

Test direct `QuerySet.update()` or bulk writes and require `IntegrityError` for invalid values on the production database engine, not only SQLite.

## Read-time integrity

Before detail pages and financial exports:

1. Recompute expected outputs on a non-persisted copy.
2. Compare current inputs to the stored input snapshot/hash.
3. Compare stored outputs to recomputed outputs and output hash.
4. If valid, render.
5. If DRAFT drifted, repair transactionally, append a revision, and disclose that repair.
6. If FINAL drifted, fail closed and do not produce the report.

## Full source disclosure

HTML and PDF must disclose enough source data to reproduce the result independently: quantity/drivers; every amount and currency; all FX rates, source, reference, and effective date; freight/duty modes and rates; customs/broker fees; bank/agent/tax percentages and their bases; pricing mode/target; preparer; actual revision; formula version; finalization timestamp; and any legal/classification caveat.

## Migration caution

Do not irreversibly collapse lifecycle states. State-remapping migrations need a meaningful reverse function where possible. If a migration already ran in shared environments, do not edit history silently—add a corrective forward migration. Editing an unapplied migration is acceptable only when repository/deployment state is known and controlled.

## Deterministic verification

- Boundary tests: 100 accepted, 100.0001 rejected where 100 is the maximum.
- `quantity=None` returns a named ValidationError, never a TypeError from later arithmetic.
- No-op save creates no revision.
- Another manager editing an owner’s DRAFT is recorded as actor.
- Automatic DRAFT repair records the triggering user.
- Admin editing records the request user.
- Direct invalid DB writes fail.
- DRAFT input/output drift repairs and increments revision.
- FINAL input/output drift blocks both HTML and PDF.
- Two independent Decimal samples still match after hardening.
