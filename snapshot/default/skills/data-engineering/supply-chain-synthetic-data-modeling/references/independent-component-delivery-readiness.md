# Independent component delivery and X-kit readiness

Use this pattern when one finished product has multiple mandatory BOM positions whose shipment dates and lot sizes evolve independently.

## Modeling rules

- Give each component/SKU its own random stream or source schedule. Do not derive all component dates from one shared cadence.
- Lot count, lot quantity, and ETA are independently generated per component. Coincident dates are allowed only as a natural result, not forced synchronization.
- Keep one component lot per row. Required quantity is `target_kits × qty_per_kit`.
- For synthetic fixtures, use a fixed seed so results are reproducible while schedules remain independent by SKU (for example, seed material `scenario_seed:sku`).

## Direct columns on the detailed supply table

After sorting by ETA, add for every lot:

1. cumulative quantity for that SKU;
2. kit capacity after the lot: `floor(cumulative_qty / qty_per_kit)`;
3. remaining deficit to the product plan;
4. a human-readable position issue/status.

These fields make the readiness logic auditable from the detailed table rather than hiding it only in a summary.

## Event-level readiness table

Create one row for every unique delivery date, including dates that do not increase finished-kit readiness. For each date show:

- exact component/SKU and lot quantity arriving;
- cumulative quantity and kit capacity for every mandatory BOM position;
- complete kits available: `min(component kit capacities)` capped at target;
- newly enabled kits since the previous event;
- remaining shortages by component;
- bottleneck component(s);
- problem classification, especially “delivery does not increase complete kits”.

The sum of all positive `newly enabled kits` rows must equal final complete-kit readiness.

## Parameterized X-kit calculation

Use one editable input only: `required kits (X)`. A control date is unnecessary when the requested output is the earliest readiness date.

For every component compute:

- required for X: `X × qty_per_kit`;
- planned total;
- earliest ETA where cumulative quantity reaches required-for-X;
- reserve after allocating X;
- permanent plan deficit, if planned total is insufficient.

Product readiness for X is the latest component sufficiency date:

`X-kit readiness date = max(component sufficiency dates)`

Validate X against `1..target_kits`. If any component lacks total plan coverage, fail closed with an explicit “no coverage / missing N units” result instead of returning a misleading date.

## Calendar presentation

Mark every ETA on a calendar and label each marked cell with the specific component/SKU and lot quantity. Do not show only an aggregated daily total: users must be able to see that component X arrives in quantity Y on one date while component Z arrives in quantity I on another.

## Verification

- Every lot appears once in the detailed table and once on the calendar.
- Per-component cumulative quantities are monotonic by ETA.
- Final cumulative quantities match BOM requirements or explicitly labeled shortages.
- Event rows cover every unique ETA, including zero-readiness-change events.
- Recompute at least one sample X independently and compare its readiness date to the workbook formula/output.
- Confirm the only input in the X calculator is X and that no obsolete control-date input remains.
