# Supply-driven shipment waves

Use this pattern when shipment dates must be derived from planned or actual component receipts rather than chosen in advance.

## Source reconstruction

1. Identify one confirmed final-product BOM and its component norms.
2. Classify receipt rows by component and party with source-row lineage.
3. Apply an explicit quantity/date fallback, such as fact-ready then plan-ready.
4. Exclude outbound, terminal, and customer dates when the task asks for a readiness-based simulation.
5. Aggregate cumulative receipt quantity by component at each distinct date.

## Two separate completeness measures

```text
weighted_BOM_coverage[t] =
  Σ min(cumulative_supply[p,t], BOM_required[p])
  / Σ BOM_required[p]

strict_complete_kits[t] =
  min_p floor(cumulative_supply[p,t] / per_set[p])
```

Weighted coverage is useful for ranking incomplete component waves. It is not finished-product readiness. If strict completeness is zero, describe the shipment as a partial component set.

## Selecting waves

- Ship on the first workable business day after a material coverage jump.
- Consolidate a low-marginal arrival with the next major receipt when a separate trip adds little operational value.
- Move weekend arrivals to the next business day for receiving/inspection.
- Hold a late top-up for the final wave if it creates no additional strict kits.
- Keep the final date conditional when any required shortage has no defensible date.

## Worked anonymized pattern

A 69-component, 5,000-unit BOM produced planned milestones:

| Receipt date | Weighted coverage | Full positions | Zero positions | Decision |
|---|---:|---:|---:|---|
| 15 Sep | 80.98% | 46 | 4 | Ship next business day |
| 23 Sep | 81.61% | 47 | 4 | Hold; only +0.64 pp |
| 28 Sep | 92.60% | 57 | 2 | Combine 23+28 Sep and ship next day |
| 3 Oct (weekend) | 96.90% | 64 | 2 | Ship next business day |
| 13 Oct | 97.54% | 65 | 2 | Hold for final; no strict kits gained |

The fixed waves were partial component sets. Strict complete kits remained zero. The final wave stayed undated until all residual shortages were closed.

## Shipment object contract

Include:

- shipment ID and date/date rule;
- included receipt dates and party IDs;
- component rows/positions in the wave;
- cumulative weighted coverage;
- full, partial, and zero position counts;
- strict complete kits;
- explanation and date rationale;
- release condition and rescheduling rule.

## Verification

- Recompute the timeline directly from the source workbook.
- Assert exact milestone dates and metrics.
- Assert no component quantity is counted in more than one cumulative step.
- Reject changed shipment dates, coverage, shortages, or fabricated final dates.
- Verify desktop/mobile UI clearly distinguishes partial components from finished products.
