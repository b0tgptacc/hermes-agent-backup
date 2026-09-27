# Controlled Completeness Scenarios

Use this pattern when a synthetic BOM/production fixture must contain known product-level completeness states rather than whatever random generation produces.

## Assign scenarios before lot generation

Partition finished goods into explicit groups such as:

- `complete_at_snapshot`
- `partial_at_snapshot`
- `unstarted_at_snapshot`

Keep the assignment deterministic and record it in the fixture description or generator configuration.

## Generate a 100% complete product

For every mandatory BOM component of the product:

1. Compute `required_total = target_qty × qty_per_set`.
2. Split exactly `required_total` into multiple unequal positive lots dated on or before the snapshot.
3. Put only surplus quantities after the snapshot and label those lots as reserve or safety stock.
4. Preserve the normal milestone order for each lot: manufacture, QA, ship-ready, ETA.

A pinned sequence may be used for legibility. Example for a requirement of 80 units: `30 + 4 + 17 + 29 = 80` by the snapshot, followed by an 8-unit future reserve lot.

## Generate partial and unstarted products

- Partial: every mandatory component may have an initial lot, but at least one bottleneck component remains below requirement.
- Unstarted: at least one mandatory component has zero produced quantity at the snapshot.
- Avoid accidentally making every product 0% unless that is an explicit test case; product completeness is the minimum component coverage.

## Required verification

Recompute from detailed lots, not from summary cells:

- `component_coverage = min(1, produced_to_date / required_total)`
- `product_completeness = min(component_coverage)`
- `buildable_units = min(floor(produced_i / qty_per_set_i))`

For each designated complete product assert:

- `product_completeness == 1`
- `buildable_units == target_qty`
- every mandatory component reaches its requirement by the snapshot
- later lots contain only reserve quantities

Also count designated versus actual complete products and expose that as a control-table check.

## Safe workbook output retry

If a spreadsheet destination is not writable because the workbook is open, do not retry the same overwrite blindly. Save a clearly versioned sibling such as `_expanded.xlsx`, verify that artifact, and report that the original was preserved.
