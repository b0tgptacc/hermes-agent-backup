# Readiness Threshold Reporting

Use this pattern when a BOM plan must answer both “when can X complete kits be assembled?” and “what is missing at each delivery event?”.

## Independent supply schedules

Each component/SKU must have its own random or sourced delivery schedule. Do not generate one shared calendar and shift every component from it.

For reproducible synthetic data, derive a separate deterministic random stream per SKU, for example from `scenario_seed + SKU`. Let each SKU independently determine:

- number of lots;
- unequal positive lot quantities;
- delivery dates;
- supplier/logistics attributes when modeled.

Coincident dates are allowed when they occur naturally, but must not be forced by a shared cadence. Verify that date sequences are not all identical.

## Detailed delivery table

Keep one lot per row and include:

- finished-good code and name;
- component SKU and name;
- quantity per finished kit;
- total requirement;
- lot ID and lot quantity;
- delivery/ETA date;
- cumulative quantity for that SKU;
- component capacity in full kits: `floor(cumulative_qty / qty_per_kit)`;
- remaining component deficit;
- position-level issue/status.

A calendar must name every delivery line as `SKU/component — quantity`, not merely show a daily aggregate. If several lots arrive on one day, list each line in the same calendar cell.

## Event-by-event product readiness

For every unique delivery date:

1. Add arriving quantities to per-SKU cumulative balances.
2. Compute each component’s kit capacity.
3. Compute product-ready kits as the minimum component capacity, capped by target demand.
4. Compute newly ready kits as the increase from the previous event.
5. List all component shortages against the target.
6. Identify the bottleneck component(s) at the minimum capacity.
7. Flag deliveries that do not increase the number of complete kits.

A correct event report answers:

- what arrived on this date;
- how many complete kits can now be assembled;
- how many new kits this event unlocked;
- what is still missing;
- which position constrains readiness;
- whether the event solved or merely shifted the bottleneck.

## Parameterized X-kit readiness

Use one editable input only: `X = required complete kits`.

For each component:

- required quantity: `X × qty_per_kit`;
- planned total;
- earliest date cumulative supply reaches the required quantity;
- reserve after allocating X kits;
- deficit/problem when planned total is insufficient.

The overall readiness date for X kits is the latest component sufficiency date. Do not request a control date unless the user explicitly asks for an “as of” analysis.

In Excel, expose X through a validated input cell and calculate the component dates and overall maximum with formulas or a fully documented deterministic calculation. Configure recalculation on open and independently recompute the default X during verification.

## Milestone schedules

Support both views:

- round milestones: 10, 20, 30, … plus the non-round final target;
- unit milestones: every quantity from 1 through the final target.

For each milestone include:

- requested complete-kit quantity;
- readiness date;
- per-component sufficiency dates;
- limiting component(s);
- time from the prior milestone;
- note when several milestones are unlocked by the same lot.

Repeated dates are correct: one component lot may unlock many consecutive thresholds. Never invent distinct dates for each kit merely to make the table look varied.

## Verification

Programmatically verify:

- exactly one finished-good code when requested;
- every required SKU has supply lots;
- lot IDs are unique and quantities positive;
- per-SKU date sequences were generated independently;
- planned totals equal or intentionally exceed requirements;
- calendar contains every lot with SKU and quantity;
- event dates equal the unique delivery-date set;
- cumulative quantities and component capacities recompute exactly;
- newly ready kits sum to final ready kits;
- milestone quantities are complete and ordered;
- milestone dates are non-decreasing;
- each milestone date equals the maximum of independently recomputed component sufficiency dates;
- final target reaches zero shortage, unless an intentional uncovered scenario is labeled.
