# Completeness Fixture Pattern

## Compact relational schema

### products

| Field | Meaning |
|---|---|
| product_code | Finished-good identifier |
| product_name | Human-readable name |
| target_qty | Number of finished sets required |
| priority | Operational priority |
| destination | DC, hub, terminal, or warehouse |
| required_date | Business due date |

### bom

| Field | Meaning |
|---|---|
| product_code | Parent finished good |
| component_sku | Component identifier |
| qty_per_set | Required units per finished set |
| unit | Piece, set, kg, m, etc. |
| required_total | `target_qty × qty_per_set` |

### production_lots

| Field | Meaning |
|---|---|
| lot_id | Unique lot identifier |
| component_sku | Produced component |
| lot_qty | Positive lot quantity |
| manufacturing_date | Production completion date |
| qa_date | Quality-control completion |
| ship_ready_date | Ready for pickup/export |
| transport_mode | Air, road, rail, multimodal, etc. |
| eta_destination | Forecast destination arrival |
| status | Derived from dates and snapshot |

## Deterministic uneven split

Given required total `R`:

1. Add a documented surplus or shortage policy to obtain planned total `P`.
2. Choose a lot count `n` in a bounded range such as 3–6.
3. Sample `n-1` unique cut points from `1..P-1`.
4. Sort cut points and convert adjacent differences into positive quantities.
5. Optionally shuffle quantities independently of dates.
6. Verify `sum(lots) == P`, every quantity is positive, and the set of quantities has more than one distinct value.

For a demonstration fixture, it is acceptable to pin one legible sequence such as `30, 4, 17, 21, 16` and randomize the remainder with a fixed seed.

## Readiness calculation

For each component, sort lots by manufacturing date and accumulate quantity. The first date where cumulative quantity reaches the BOM requirement is the component's full-production date. Repeat by destination ETA for full-arrival date.

For each product:

- `buildable_units = min(floor(produced_i / qty_per_set_i))`
- `completeness = min(min(1, produced_i / required_i))`
- `full_production_date = max(component_full_production_date_i)`
- `full_arrival_date = max(component_full_arrival_date_i)`

These are bottleneck metrics; averaging component percentages overstates readiness and should not be labeled product completeness.

## Required invariants

- Every product referenced by BOM exists.
- Every production lot references an existing component SKU.
- `required_total == target_qty × qty_per_set`.
- Lot quantities are positive.
- Manufacturing dates satisfy the requested horizon.
- `manufacturing_date ≤ qa_date ≤ ship_ready_date ≤ eta_destination`.
- Planned totals cover requirements unless shortages are intentional and labeled.
- Summary values can be recomputed exactly from detailed rows.
- Control/report columns preserve semantic types; mixed count/date columns must not receive a whole-column date format.

## Scenario-quality checklist

A useful synthetic logistics fixture should include:

- multiple finished goods from different operating segments;
- different BOM sizes and quantities per set;
- uneven production lots and irregular intervals;
- multiple suppliers, countries, transport modes, and destination nodes;
- logistics handling constraints;
- a mix of on-time and delayed readiness;
- enough current production across all components to avoid an accidentally all-zero product dashboard, unless that is the intended test case;
- an explicit statement that all entities and values are fictitious.
