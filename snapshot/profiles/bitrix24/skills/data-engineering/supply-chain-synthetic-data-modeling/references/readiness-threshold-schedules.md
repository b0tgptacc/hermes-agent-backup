# BOM readiness threshold schedules

Use this pattern when a supply-plan workbook must answer not only one `X`-kit query but a complete schedule of readiness thresholds.

## Threshold types

- **Round milestones:** `10, 20, …` through the largest round quantity, plus the non-round final target when applicable.
- **Unit-by-unit schedule:** exactly one row for every quantity `1…target_kits`, with no gaps.

## Calculation

For each threshold `X` and each mandatory component:

1. Compute `required_component_qty = X × qty_per_kit`.
2. Sort that component’s lots by ETA and find the first ETA where cumulative quantity reaches the requirement.
3. Set product readiness to the latest component sufficiency date.
4. Record the component(s) whose sufficiency date equals product readiness as the bottleneck.
5. Optionally record days since the previous threshold and each component’s own sufficiency date for auditability.

## Interpretation

Readiness dates must be non-decreasing. Multiple consecutive quantities can legitimately share one date because a single delivery lot may unlock many kits simultaneously. Label this as “same delivery as previous threshold”; never invent distinct dates merely to make each row look different.

## Workbook presentation

Use a separate filtered Excel table. Recommended columns:

- threshold quantity;
- readiness date;
- days since previous threshold;
- sufficiency date for every mandatory component;
- limiting component(s);
- explanatory comment.

Keep the user-entered `X` calculator separate: it answers one scenario interactively, while threshold sheets provide exhaustive schedules.

## Verification

- Confirm the row sequence is exactly the requested thresholds (`10,20,…` or `1…target`).
- Recompute every row independently from detailed lots.
- Confirm readiness dates are non-decreasing.
- Confirm every row equals `max(component sufficiency dates)`.
- Confirm the final threshold equals final product readiness.
