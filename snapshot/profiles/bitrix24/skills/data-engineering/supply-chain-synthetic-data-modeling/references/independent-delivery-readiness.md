# Independent delivery and kit-readiness planning

Use this pattern when a synthetic BOM plan must answer: “When can X complete kits be assembled, what is missing, and what blocks readiness?”

## Model

- Give every BOM position its own random stream, e.g. seed `scenario_seed:component_sku`.
- Randomize each component’s lot count, positive uneven quantities, and delivery dates independently. Do not synchronize components through one shared date template.
- Coincident dates are allowed only as natural random collisions.
- Keep one lot per row. Calendar cells must list each delivered SKU and quantity separately, not only aggregate daily totals.

## Detailed delivery table

For every lot, calculate after sorting by delivery date:

- cumulative quantity for that SKU;
- component kit capacity: `floor(cumulative_qty / qty_per_kit)`;
- component deficit against the overall plan;
- position status/problem text.

## Event-level readiness

For every unique delivery date:

1. Add all lots arriving that day to their SKU balances.
2. Compute every component’s kit capacity.
3. Compute complete kits as the minimum component capacity, capped by plan quantity.
4. Report new complete kits since the previous event.
5. List shortages by SKU and quantity.
6. Identify every bottleneck tied for the minimum capacity.
7. Flag deliveries that do not increase complete-kit availability.

## Parameterized X-kit query

Use one editable input only: `required kits (X)`. Do not require a control date unless the user explicitly asks for as-of analysis.

For each component:

- required quantity: `X × qty_per_kit`;
- planned quantity;
- earliest date cumulative deliveries reach required quantity;
- reserve after allocating X kits;
- uncovered-plan warning.

Overall X-kit readiness is the latest component readiness date. Validate `1 ≤ X ≤ plan_qty`.

## Readiness milestone sheets

Support both views when requested:

- round milestones: 10, 20, …, plus a non-round final plan value;
- unit milestones: 1, 2, …, plan quantity.

For every milestone include overall readiness date, each component’s readiness date, bottleneck, days since the previous threshold, and a note when several thresholds are reached by the same delivery. Repeated dates are correct: one large component lot can unlock many kit counts at once.

## Calendar

Render the entire planning horizon month by month. Highlight delivery dates and show one line per lot in the cell, e.g. `CMP-X: 120 шт.`. Verify programmatically that every detailed lot appears exactly once in the calendar.

## Verification

- Every component uses a distinct generated date sequence.
- Sum of lot quantities equals planned quantity for each SKU, unless an intentional shortage is labeled.
- All dates lie within the horizon.
- Cumulative fields reproduce from lot detail.
- Event rows equal the number of unique delivery dates.
- Sum of new complete kits equals final complete kits.
- X readiness equals the maximum of component threshold dates.
- Round and unit milestone sequences have no gaps and readiness dates never decrease.
- Calendar contains every lot’s SKU and quantity.
