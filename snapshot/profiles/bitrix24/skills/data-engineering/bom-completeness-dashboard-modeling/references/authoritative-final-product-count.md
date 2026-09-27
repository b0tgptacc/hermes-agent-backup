# Authoritative Final-Product Counts in BOM Dashboards

Use this pattern when a stakeholder supplies a confirmed total for the final product after an earlier dashboard inferred a different number from GCDs across ORD/assemblies.

## Decision hierarchy

1. Treat the confirmed final-product total as authoritative master data.
2. Do not continue presenting a cross-ORD GCD as the final-product count.
3. Identify the final-product BOM anchor using explicit product semantics, confirmed mapping, component names, and assembly-level GCD. State when the anchor is an inference rather than an explicit source key.
4. Treat all other ORD as related/supporting orders until an approved inclusion map proves that each is a required position of the final product.
5. Never sum ORD-level supported-set counts to obtain final-product output.

## Recalculation

For the selected final-product assembly `c` and authoritative target `T`:

```text
per_product[c,p] = BOM_sum[c,p] / assembly_GCD[c]
quantity_only_sets[p] = floor(quantity_only[p] / per_product[c,p])
dated_sets[p] = floor(dated_quantity[p] / per_product[c,p])
quantity_only_complete = min(T, min_p(quantity_only_sets[p]))
dated_complete = min(T, min_p(dated_sets[p]))
```

If the target and assembly GCD differ, do not silently rescale. Require an approved conversion rule or present the discrepancy as unresolved.

Undated components may support `quantity_only_complete`; they must force `dated_complete` down and must not receive synthetic dates.

## Superseding an earlier meta-kit hypothesis

A corrected dashboard must do more than change a KPI:

- remove superseded meta-kit and logistics pages from navigation and direct routing;
- mark retained compatibility fields as `SUPERSEDED`/archival;
- remove stale labels such as “out of 10” from tables and exports;
- replace dated event streams with final-product events;
- invalidate shipment plans built on the superseded denominator;
- retain the older artifact as a separate version rather than overwriting it.

If final-product readiness is blocked by undated components, do not reuse an old multi-shipment plan as a plan for finished goods. Show no final shipment date until the blockers have defensible dates. Component or supporting-order waves may remain only when explicitly labeled as such.

## Fail-closed checks

Validate both schema and executable invariants:

- authoritative target is a constant;
- final-product assembly ID and component count are fixed;
- component minima reconcile to quantity-only and dated KPIs;
- blocker list exactly equals components with zero dated support;
- the readiness event for an undated complete quantity has `date = null`;
- calendar contains no synthetic final-product completion event;
- mutations to target, assembly, component count, blockers, or dated completeness are rejected;
- embedded JSON equals the external package;
- desktop and mobile UI contain no visible stale denominator or accessible superseded route.

## Communication

Distinguish clearly:

- **Fact:** stakeholder-confirmed final-product total.
- **Inference:** which ORD is the final-product BOM anchor, if not explicitly keyed.
- **Quantity-only result:** known quantities can support the target.
- **Dated result:** only quantities with defensible dates support timeline readiness.
- **Unknown:** final assembly/shipment dates while blockers lack dates.
