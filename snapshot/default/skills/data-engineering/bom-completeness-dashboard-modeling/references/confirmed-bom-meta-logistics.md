# Confirmed BOM, meta-kit normalization, and logistics simulation

## Promote explicit composition over inference

When a user supplies explicit `ORD → PRD` lists, use them as the authoritative BOM composition for those assemblies. Preserve a manifest containing raw/anonymized IDs, decoded display names, source rows, quantities, GCD, per-set norm, and provenance.

Reconcile component count and GCD to assembly summaries. A repeated paste of an identical long list is a duplicate copy, not additional BOM demand. Record the deduplication. Confirmed composition does not prove party allocation; keep that as a separate rule.

A validated case reconciled seven lists with counts `13, 1, 1, 5, 2, 69, 72` — 163 unique `ORD + PRD` pairs.

## Normalize assembly readiness to meta-kit units

For a user-approved higher-level kit with `H` meta-kits:

```text
meta_norm[ORD] = quantity_only_sets[ORD] / H
meta_cumulative[ORD,t] = floor(ORD_cumulative[t] / meta_norm[ORD])
meta_increment[ORD,t] = meta_cumulative[ORD,t] - previous_meta_cumulative[ORD]
```

Render readiness events in `0..H`, not raw thousands. Undated quantity-backed positions receive `БЕЗ ДАТЫ`, count toward quantity-only completeness, and stay out of the calendar.

## Logistics what-if plan

Only ignore source shipment dates when explicitly requested. List every ignored field prominently (for example `M/N`, `Q/R`, `S/T`). Optimize against readiness fill and make the output conditional:

1. Track dated-position fill and practical kit count by date.
2. Prefer a single consolidated shipment once all dated positions reach the target.
3. Treat undated required positions as hard release blockers.
4. Recommend a date only conditionally: release if blockers are physically confirmed by that date; otherwise first available day after confirmation.
5. Explain why earlier waves are suboptimal (partial kits, repeated handling, documents, and de-kitting risk).

A validated scenario reached 100% across five dated ORD positions on 30 September, while two undated positions remained blockers. The accepted recommendation was one conditional shipment of 10 kits on 30 September, not a factual source shipment date.

## Fail-closed probes

Reject mutations to:

- confirmed component count, GCD, raw ID, source row, or duplicate pair;
- normalized meta-kit norm, increment, cumulative value, or missing ORD position;
- ignore-dates flag, target kit count, recommendation date, or blocker set;
- embedded/external JSON mismatch.
