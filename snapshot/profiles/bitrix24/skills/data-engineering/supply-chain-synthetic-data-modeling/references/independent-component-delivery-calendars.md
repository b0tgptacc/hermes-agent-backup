# Independent component delivery schedules and calendars

Use this pattern when a synthetic BOM plan must model each component position independently.

## Generation

- Give each component SKU its own deterministic random generator, derived from a scenario seed and the SKU.
- Generate each SKU's lot count, positive unequal quantities, and delivery dates from that component-specific stream.
- Keep one lot per row and require the lot quantities for a SKU to sum to its planned requirement.
- Do not impose a shared cadence or synchronized date template across BOM positions.
- Independence permits chance collisions: two components may arrive on the same day, but their complete date sequences should not be identical unless intentional.

## Calendar presentation

A delivery-day cell must identify every arrival separately, for example:

- `CMP-X: 120 шт.`
- `CMP-Z: 45 шт.`

Do not replace these lines with only an aggregate such as `2 партии / 165 шт.`; the operator needs to know which BOM positions become available.

## Verification

1. Group lots by component SKU and verify planned totals.
2. Verify all delivery dates are inside the stated horizon.
3. Compare the complete ordered date sequence per SKU and flag unintended identical schedules.
4. Build a canonical delivery identity `(date, SKU, lot, quantity)` for every lot.
5. Confirm every canonical delivery appears once in the detail table and once in the calendar representation.
6. Recompute cumulative buildable finished units as the minimum component capacity after each delivery date.
