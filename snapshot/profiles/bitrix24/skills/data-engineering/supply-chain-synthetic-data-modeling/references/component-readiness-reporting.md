# Component-Level Delivery and Readiness Reporting

Use this pattern when a synthetic BOM plan must show when any requested number of complete finished goods becomes buildable.

## Independent delivery generation

- Give every BOM position its own deterministic random stream, e.g. seed derived from `scenario_seed + component_sku`.
- Randomize the lot count, lot quantities, and delivery dates independently per component.
- Do not derive all components from one shared date template or force synchronized final lots.
- Natural date collisions are allowed; artificial synchronization is not.
- Preserve exact component totals unless an intentional shortage scenario is labeled.

## Detailed supply table

Use one row per component lot. In addition to master and logistics fields, calculate after each row:

- cumulative quantity for that SKU;
- equivalent complete kits: `floor(cumulative_qty / qty_per_kit)`;
- remaining SKU deficit to the finished-goods plan;
- a readable position issue such as `Missing 120 pcs to plan` or `Position covered`.

Sort chronologically before calculating cumulative values.

## Event-by-event completeness analysis

For every distinct delivery date, calculate:

1. Component lots arriving that day, naming each SKU and quantity.
2. Cumulative quantity per mandatory SKU.
3. Kit capacity per SKU: `floor(cumulative_qty / qty_per_kit)`.
4. Complete kits available: minimum capacity across mandatory SKUs, capped at the plan.
5. New complete kits created on the date.
6. Remaining quantity by component.
7. Bottleneck component(s).
8. Operational diagnosis:
   - `Delivery did not increase complete-kit count`;
   - `Created +N complete kits; limited by ...`;
   - `Full plan covered`.

A calendar cell must list each arriving component and quantity, not only an aggregate daily total.

## Parameterized X-kit calculation

Use a single editable input: `Required kits (X)`. Do not require a control date unless the user explicitly asks for snapshot analysis.

For each mandatory component:

- required quantity: `X × qty_per_kit`;
- planned total;
- earliest date cumulative supply reaches the required quantity;
- remaining reserve after allocating X kits;
- shortage/problem if planned supply is insufficient.

Overall X-kit readiness is:

`max(component_readiness_date_i)`

The limiting component(s) are those whose readiness date equals this maximum. Make the final date prominent and force workbook recalculation on open if formulas are used.

## Milestone views

Offer two separate views when operational users need planning detail:

- **Round milestones:** 10, 20, 30, ... plus the non-round final plan quantity.
- **Unit-by-unit readiness:** one row for every quantity from 1 through the full plan.

Rows may legitimately share the same readiness date because one component lot can unlock many kits at once. Never invent distinct dates to make the table look progressive.

For each milestone include component-level readiness dates, the overall readiness date, the interval from the previous threshold, the bottleneck, and a comment explaining same-date thresholds.

## Verification

Programmatically verify:

- all quantities from 1 through the plan appear without gaps in a unit view;
- readiness dates are non-decreasing;
- each milestone date equals the independently recomputed maximum component threshold date;
- sum of new-kit increments equals the finished-goods plan;
- the final event has zero shortage;
- every detailed lot appears in the calendar annotation;
- every component schedule is generated independently;
- Excel table ranges, date formats, filters, freeze panes, and input validation are present.
