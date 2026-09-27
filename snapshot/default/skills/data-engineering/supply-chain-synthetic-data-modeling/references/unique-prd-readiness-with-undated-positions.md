# Unique-PRD completeness with undated positions

Use this pattern when a logistics workbook mixes BOM summary rows, repeated component rows, lot/party detail, and incomplete dates.

## Separate roles before arithmetic

Do not sum every numeric occurrence of a component across the sheet. Classify rows first:

- **Master BOM**: required total per finished-product/ORD composition.
- **Party/lot detail**: allocation or fulfillment of that master amount.
- **Milestone snapshots**: the same material represented at production, ready, shipment, terminal, or customer stages.

Adding master, party, and milestone values double-counts one physical quantity. A valid parser must define the row/block role and use exactly one quantity source for each metric.

## Aggregate duplicate BOM positions first

For composition `c` and component `p`:

```text
BOM_sum[c,p] = sum(required B on master BOM rows for p)
G[c] = gcd(BOM_sum[c,p] for unique p)
per_set[c,p] = BOM_sum[c,p] / G[c]
```

Then calculate component-limited sets:

```text
sets[c,p] = floor(available[c,p] / per_set[c,p])
complete_sets[c] = min_p(sets[c,p]), capped at G[c]
```

The minimum must be taken over every mandatory unique component, including components without a date.

Dividing each component sum directly by the composition GCD is generally wrong: it returns component multiplicity relative to GCD, not buildable sets, whenever `per_set > 1`.

## Keep quantity completeness separate from date coverage

Maintain two explicit measures:

1. **Quantity-only completeness** — includes known component quantities even when dates are missing.
2. **Dated readiness** — includes only quantities that can be placed on a verified plan/fact timeline.

Undated components affect the quantity-only set count but must not receive fabricated dates or appear in a calendar bucket. Show both values side by side and label the distinction in KPI text.

If a source is confirmed to contain a master total plus party details of the same volume, avoid `master + parties`. Use an explicit allocation rule; a conservative quantity-only merge can use `max(master_total, allocated_party_total)` while preserving both fields and documenting the assumption. Do not generalize this rule without confirming the summary/detail relationship.

## Allocation boundaries

- Aggregate repeated PRD only inside its parent composition/ORD.
- If a PRD is shared by multiple compositions, require an explicit allocation table; do not let one supply quantity satisfy several products invisibly.
- Detect duplicate BOM rows and cross-composition component overlap programmatically.

## Chronological readiness

For each stage/scenario, accumulate component quantities by verified date and recompute the minimum set count only when the date advances. Record only positive deltas. Plan fallback must be labeled as calculated plan/fact, never as strict fact.

## Verification invariants

- Recomputed `per_set == BOM_sum / GCD` for every component.
- `available_sets == floor(quantity / per_set)`.
- `capped_sets == min(GCD, available_sets)`.
- Product total equals the minimum component total.
- Limiting flags exactly match the minimum components.
- Quantity-only and dated totals reconcile independently.
- Missing dates remain null.
- Master totals and party quantities are not added unless they are proven independent.
- Dashboard JSON rejects missing/extra fields, invalid dates/types, negative quantities, over-cap values, wrong summaries, and inconsistent limiting flags.

## UI guidance

Provide a component audit view with BOM sum, GCD, per-set norm, quantity including undated rows, dated quantity, sets per PRD, capped sets, and limiting status. Wide tables need an explicit horizontal-scroll affordance. Verify desktop and a real 390px mobile viewport.
