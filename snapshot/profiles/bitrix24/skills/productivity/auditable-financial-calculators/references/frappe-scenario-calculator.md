# Frappe Scenario Calculator Pattern

Use this pattern when business users authorize a planning calculator but the normative production formula remains blocked.

## Separate scenario from FINAL

- Give the planning engine an explicit version such as `SCENARIO-0.1`.
- Keep normative finalize/publication commands fail-closed until the formal finance/customs evidence gate is closed.
- Put a visible non-statutory caveat in UI, saved revision and PDF.
- Never silently reinterpret a new scenario contract as approval of the legacy/production baseline.

## Canonical input and audit contract

- Require the FX-effective calculation date and enforce exact lexical `YYYY-MM-DD`; `date.fromisoformat()` alone accepts compact forms such as `YYYYMMDD`, which creates multiple hashes for the same date.
- Normalize accepted dates with `parsed.isoformat()` before hashing.
- HTTP clients must not supply the audit timestamp. Generate UTC server time inside calculate/save commands; deterministic domain helpers may still accept a timestamp for tests.
- Persist allow-listed inputs, named intermediates, ordered breakdown, outputs, formula version, server timestamp, actor, caveat and canonical SHA-256.
- Scenario/template allow-lists must reject unknown nested keys before persistence.

## Frappe command boundary

- Make calculation/save/template/export mutations `frappe.whitelist(methods=["POST"])`.
- Convert domain validation errors into named Frappe `ValidationError` 4xx responses rather than raw 500s.
- Keep DocTypes read-only through generic permissions; controlled commands insert with an internal flag only after role checks.
- Use a dedicated read/calculate role for sales users rather than granting generic write access.

## PDF contract

Create PDF only from an immutable saved revision. Pass both `snapshot_json` and `result_json` to one renderer. Include:

- quantity, weight/volume and calculation date;
- original amounts/currencies and all FX rates;
- duty mode/rate and every percentage base;
- normalized components and named section totals;
- formula/rounding policy (`Decimal`, quantizer, rounding mode);
- per-shipment/per-unit/pricing outputs;
- version, server timestamp, caveat and revision hash.

Escape every user-controlled string, store the file privately, hash the PDF bytes, and make repeated export idempotent. Parse the produced PDF to prove Cyrillic/text round-trip; inspect rendered pages when a rasterizer is available.

## Verification

- Two independent Decimal scripts that do not import the production engine must match exact named outputs.
- Add boundary tests for non-finite values, zero divisors, margin >=100%, missing/unused FX and half-cent rounding.
- Exercise real HTTP calculate -> save revision -> save template -> export/download PDF.
- Verify desktop/mobile UI with exact viewport metrics, no horizontal overflow, successful result state and matching CSRF token.
