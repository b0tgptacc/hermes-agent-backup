# Conditional multi-shipment planning for authoritative finished-goods totals

Use this pattern when the business confirms a final-product target and requires several shipments, but one or more required components lack defensible readiness dates.

## Rules

1. The authoritative finished-goods target overrides a cross-ORD GCD used as a former headline count.
2. Anchor the target to a defensible final-product BOM. Disclose when the anchor is inferred rather than explicitly keyed.
3. Never reuse component-wave dates as finished-goods shipment dates.
4. Define `T` as the first business day after the later of an agreed control date or confirmation of the final undated blocker.
5. Express waves as `T`, `T+n` business days. Calendar dates are conditional targets only when the blocker deadline is explicit.
6. Reconcile shipment quantities and cumulative totals exactly to the authoritative target.
7. Every shipment object must include `explanation`, `why_this_date`, `release_condition`, and `reschedule_rule`.
8. If source shipment dates are intentionally ignored, enumerate their columns and label the output as simulation.

## Superseded-model cleanup

When an earlier meta-kit hypothesis is replaced:

- remove its navigation, direct route, DOM section, and render functions;
- remove stale denominator labels from tables and exports;
- mark retained compatibility fields `SUPERSEDED`;
- invalidate shipment plans built on the old denominator.

Hidden legacy UI is not sufficient.

## Fail-closed probes

Validate both JSON Schema and executable invariants. Reject mutations to:

- final-product target and assembly anchor;
- exact blocker names;
- undated readiness event (`date=null`, scenario `БЕЗ ДАТЫ`);
- wave count, IDs, dates, quantities, and cumulative totals;
- conditional-date flag and ignored source fields;
- any per-wave rationale or release condition.

Use negative tests that independently change quantity, date, wave count, conditional flag, blocker name, and rationale text. Verify that the active DOM contains no superseded routes, sections, or render functions.
