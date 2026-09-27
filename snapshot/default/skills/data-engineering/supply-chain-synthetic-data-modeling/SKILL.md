---
name: supply-chain-synthetic-data-modeling
description: Use when creating synthetic supply-chain and BOM datasets.
version: 1.0.0
metadata:
  hermes:
    tags: [supply-chain, synthetic-data, bom, production-planning, logistics, xlsx]
    category: data-engineering
---

# Supply-Chain Synthetic Data Modeling

Create coherent, auditable synthetic datasets for products, bills of materials (BOMs), manufacturing batches, logistics milestones, and completeness/readiness reporting. Use this for demos, QA fixtures, analytics prototypes, planning simulations, and spreadsheet deliverables.

## Core principle

Model the operational chain rather than producing a flat random table:

`finished product → required BOM positions → uneven production lots → QA → shipment readiness → destination ETA → product readiness`

Synthetic values must be fictitious but internally consistent. A large row count is not useful if required quantities, dates, statuses, and summaries contradict each other.

## Recommended workbook/data model

Use separate normalized sheets or tables:

1. **Description / data dictionary** — snapshot date, horizon, formulas, assumptions, and an explicit synthetic-data notice.
2. **Products** — finished-good code, name, business segment, target quantity, priority, destination hub/DC, required date.
3. **BOM / Specification** — product code, component SKU, component name, unit, quantity per set, required total, category, supplier/source fields.
4. **Production lots** — one row per lot with component SKU, uneven quantity, manufacturing date, QA date, ship-ready date, mode, ETA, destination, handling class, and status.
5. **Component completeness** — required, planned, produced at snapshot, deficit, coverage ratio, full-production date, full-arrival date.
6. **Product summary** — buildable units at snapshot, product completeness, bottleneck dates, due-date variance, and schedule status.
7. **Control checks** — row counts, date bounds, plan coverage, lot heterogeneity, referential integrity, and result status.

Do not collapse production dates into comma-separated cells when the dataset is intended for filtering, BI, SQL, or simulation. One lot per row is the durable structure.

## Procedure

1. **Set the scenario boundary**
   - Establish an explicit snapshot date and planning horizon.
   - Define number of finished goods, BOM depth, volume scale, business segments, destination nodes, and whether shortages or delays should exist.
   - Use a fixed random seed so the fixture is reproducible.

2. **Create realistic master data**
   - Give finished goods and components stable, distinct codes.
   - Keep names plausible for the business domain without copying real confidential records.
   - Include logistics-relevant attributes: origin, supplier, transport mode, destination, dangerous-goods/temperature/fragility/oversize handling where applicable.

3. **Generate BOM requirements**
   - For each BOM row compute:
     `required_total = target_finished_qty × qty_per_set`
   - Use correct units; do not silently mix pieces, sets, kilograms, and meters.
   - Prefer component SKUs that are unique per actual item. If a component is shared by multiple products, model allocation explicitly rather than duplicating supply invisibly.

4. **Generate uneven production lots**
   - Split each component's planned amount into 3–6 unequal positive integer lots.
   - Use irregular date gaps rather than a uniform weekly cadence.
   - Ensure at least one clearly legible example such as `30, 4, 17, …` when demonstrating partial manufacture.
   - Keep manufacturing dates inside the requested horizon; downstream ETA may fall outside it if transit logically requires that.
   - Set statuses from dates relative to the snapshot rather than choosing statuses independently.

5. **Add logistics milestones**
   - Preserve causal order:
     `manufacturing_date ≤ QA_date ≤ ship_ready_date ≤ ETA`
   - Make transit ranges mode-sensitive; air should normally be faster than multimodal sea/rail.
   - Include destination hub/DC and handling constraints so the fixture represents a logistics operation, not only a factory plan.

6. **Calculate completeness**
   - Component coverage at the snapshot:
     `min(1, produced_to_date / required_total)`
   - Component deficit:
     `max(0, required_total - produced_to_date)`
   - Buildable finished units:
     `min(floor(produced_component_i / qty_per_set_i))` across all mandatory BOM positions.
   - Product completeness is the bottleneck coverage:
     `min(component_coverage_i)` across mandatory positions.
   - Full-production readiness is the latest date on which every component cumulatively reaches its requirement.
   - Full-DC readiness uses cumulative quantities ordered by ETA, then takes the latest component readiness date.
   - Due-date variance:
     `max(0, full_DC_readiness - required_date)` in days.

7. **Make the artifact usable**
   - Freeze headers, enable filters, use native Excel tables, set date/integer/percent formats, and size columns for operational review.
   - Use conditional formatting for shortages, completeness, and delays.
   - Add a summary visualization only when it has informative variation.
   - Put assumptions and the synthetic-data disclaimer in the workbook itself.

8. **Verify programmatically before delivery**
   - Check every BOM SKU has production lots.
   - Check planned total is at least required total unless intentional shortage scenarios are labeled.
   - Check every lot quantity is positive and each modeled SKU has the intended heterogeneity.
   - Check date horizon and milestone ordering.
   - Recompute summaries from detailed rows and compare them to exported summary values.
   - Check all control rows report success.
   - Re-open the workbook and inspect sheet dimensions, tables, filters, date formats, and charts.

## Pitfalls

- **All product completeness values become zero.** Because product completeness is the minimum across components, one unstarted component zeroes the product. If the goal is a useful dashboard fixture, deliberately give every component an initial lot or create a planned mix of zero/partial/complete products.
- **Formatting numeric controls as dates.** Apply date formats only to the actual date cells, not an entire mixed-type control column; otherwise counts such as `31` display as dates in 1900.
- **Random splits are not automatically heterogeneous.** Verify distinct lot quantities per SKU. A random generator can produce equal sizes.
- **Manufacturing horizon and arrival horizon are different.** Enforce the requested bound on manufacturing dates; do not falsify ETA merely to keep all downstream milestones inside the same window.
- **Planned quantity is not current availability.** Keep planned, manufactured-to-date, ship-ready, and arrived quantities separate.
- **A workbook save is not verification.** Re-open it and validate both structure and domain invariants.

## Supporting reference

See `references/completeness-fixture-pattern.md` for a compact schema, invariants, and deterministic generation pattern.
