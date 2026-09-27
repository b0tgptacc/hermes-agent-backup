---
name: bom-completeness-dashboard-modeling
description: "Use for BOM kit completeness from logistics tables."
version: 1.0.0
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [bom, logistics, supply-chain, gcd, readiness, dashboard, data-quality]
    category: data-engineering
---

# BOM Completeness Dashboard Modeling

Build auditable kit-completeness calculations and operational dashboards from semi-structured logistics spreadsheets. Use this when rows mix assembly demand, component/SKU positions, production batches, shipments, plan/fact dates, formula placeholders, or missing dates.

## Core principle

A complete kit is constrained by the scarcest normalized component. Dates determine when a kit can appear in a timeline; dates must not decide whether a known quantity exists.

Never mix these concepts:

- master BOM demand versus delivery/batch detail;
- quantity-only completeness versus dated readiness;
- plan, fact, and mixed plan/fact fallbacks;
- mathematical inference versus confirmed business relationships.

## Procedure

### 1. Classify row roles before arithmetic

Identify, with source-row lineage:

- assembly/master header;
- immediate master component rows;
- later batch/party headers;
- child component rows of each batch;
- summary, formula, status, and separator rows.

Do not classify every positive quantity as BOM demand. A master quantity may be the total requirement while later positive quantities partition that same total.

Verify this with conservation checks. For a component `p`:

```text
master_total[p] ?= sum(batch_quantities[p])
```

If equal, adding master plus batches doubles the same business volume.

### 2. Aggregate duplicate components inside one assembly

For assembly `c`, aggregate only master BOM rows by unique component/SKU:

```text
BOM_sum[c,p] = Σ master_quantity[row]
               for rows belonging to component p in assembly c
```

Then calculate the assembly scale after aggregation:

```text
G[c] = gcd(BOM_sum[c,p] for all required p)
per_set[c,p] = BOM_sum[c,p] / G[c]
```

This avoids reusing one stock quantity against duplicate rows of the same SKU. Never compute a canonical GCD across unrelated assemblies.

If the business already supplies an authoritative BOM quantity per final kit, use it instead of inferring `per_set` from GCD.

### 3. Calculate supply-backed completeness

Aggregate deliveries/ready quantities for the same component inside the assembly allocation boundary:

```text
delivered[c,p,t] = Σ eligible batch quantities up to t
sets_from_component[c,p,t] = floor(delivered[c,p,t] / per_set[c,p])
complete_sets[c,t] = min_p(sets_from_component[c,p,t])
complete_sets[c,t] = min(complete_sets[c,t], G[c])
```

Record quantity source and fallback (`fact-ready`, `plan-ready`, production fact, production plan). A mixed fallback must be labeled “calculated plan/fact,” never “fact” or “operational fact.”

### 4. Handle positions without dates explicitly

Maintain two separate measures:

1. **Quantity-only completeness** — may include known quantities with no usable date.
2. **Dated readiness** — includes only quantities that can be placed on a defensible date.

Do not invent dates for undated quantities. They may affect the quantity-only KPI but not the calendar or dated event stream.

When the master total represents the total known/planned quantity and batches are a partition of it, a no-double-count quantity policy may be:

```text
all_positions_quantity[c,p] = max(BOM_sum[c,p], delivered_total[c,p])
```

Use this only after confirming the master-versus-detail relationship. Label the resulting measure as quantity-only/planned completeness, not actual readiness.

### 5. Model a higher-level kit only as an explicit hypothesis

If several ORD/assemblies are assumed to be required positions of one meta-kit:

```text
H = gcd(quantity_only_sets[ORD_i])
meta_norm[ORD_i] = quantity_only_sets[ORD_i] / H
supported_meta_kits[ORD_i] = floor(quantity_only_sets[ORD_i] / meta_norm[ORD_i])
meta_complete = min_i(supported_meta_kits[ORD_i])
```

Keep dated support separate. Mark the relationship as a user/business hypothesis unless the source contains an explicit parent-kit key or approved mapping.

### 6. Build an auditable data contract

Include:

- source file/hash/sheet/cell or row;
- assembly, party, and component IDs;
- master BOM total, GCD, per-set norm;
- summed plan/fact/calculated quantities;
- quantity-only and dated supported sets;
- limiting-component flags;
- assumptions and allocation method;
- problems/unresolved values.

Anonymous formula/status tokens are not reversible. Resolve them only through a trusted dictionary or source system; otherwise retain `unresolved`.

### 7. Fail-closed validation

Validate both shape and cross-row invariants:

- reject extra and missing nested fields;
- enforce real calendar dates, numeric ranges, and ID patterns;
- `per_set == BOM_sum / GCD`;
- `available_sets == floor(quantity / per_set)`;
- caps do not exceed GCD;
- limiting flags match the actual minima;
- component minima reconcile to assembly summaries;
- assembly summaries reconcile to any higher-level meta-kit;
- embedded dashboard JSON equals the external package.

JSON Schema cannot enforce every referential or aggregate invariant. Add an executable validator for cross-document IDs, hashes, dictionary lookups, and arithmetic reconciliation.

### 8. UI requirements

Provide distinct, plainly labeled surfaces for:

- all parties;
- dated complete-kit events;
- quantity-only completeness including undated positions;
- unique-component audit rows;
- calendar;
- data-quality problems;
- assumptions/methodology.

For wide component tables, keep a visible horizontal-scroll hint and test real mobile viewport width. Do not hide source/fallback columns that explain why a quantity was counted.

## Pitfalls

- Adding master BOM totals to their batch breakdown and doubling volume.
- Dividing component quantity directly by the assembly GCD instead of the component norm.
- Computing GCD before aggregating duplicate master components.
- Pooling the same component across assemblies without an allocation rule.
- Treating missing dates as missing quantities.
- Giving undated quantities synthetic calendar dates.
- Calling a plan/fact fallback “actual.”
- Assuming ORD rows form one meta-kit without an explicit business decision.
- Trusting JSON Schema alone for aggregate arithmetic.

## Verification checklist

- [ ] Row roles and assembly boundaries are explicit.
- [ ] Master totals and batch partitions are not added together.
- [ ] Duplicate master components are aggregated before GCD.
- [ ] Per-component norms and minima reconcile.
- [ ] Quantity-only and dated readiness are separate.
- [ ] Undated quantities receive no synthetic date.
- [ ] Plan/fact fallbacks are labeled honestly.
- [ ] Cross-assembly or meta-kit assumptions are disclosed.
- [ ] Schema and executable negative tests pass.
- [ ] Desktop and real mobile screenshots show no page overflow.

## Reference

See `references/anonymized-logistics-xlsx-case.md` for a worked anonymized case, alternative interpretations, failure examples, and verified acceptance probes.
