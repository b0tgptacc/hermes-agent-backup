# GCD-Based Kit Readiness

Use this method when a parent order defines total required quantities for every component and those totals share a meaningful greatest common divisor (GCD).

## Model

For component `i`:

- authoritative total quantity: `T_i`;
- total number of kits: `K = gcd(T_1, T_2, ..., T_n)`;
- requirement per kit: `R_i = T_i / K`.

For cumulative usable quantity `Q_i(t)` received or ready by date `t`:

`Complete(t) = min_i floor(Q_i(t) / R_i)`

Cap the result at `K`.

Emit an event only when:

`Complete(t) > Complete(previous date)`

The increment is:

`New(t) = Complete(t) - Complete(previous date)`

## Event construction

1. Normalize every batch to component-level quantity/date records.
2. Group records by scenario and date.
3. Sort dates ascending.
4. Update cumulative quantities for all components represented on the date.
5. Recompute component coverage and the minimum.
6. Record date, increment, cumulative kits, contributing batches, limiting components, and quantity source.

When several components in the same batch have different dates, use component-level dates for readiness. For a party-level display date, use the latest applicable component date because the whole party is not available earlier.

## Plan/fact scenarios

Maintain two views when the source is incomplete:

- **Plan:** planned readiness date and planned readiness quantity; documented earlier-stage quantity fallback may be used.
- **Operational:** actual readiness date/quantity when usable, otherwise planned values with an explicit `plan — fact missing` status.

A fallback is disclosure, not fact reconstruction.

## Preconditions

The GCD method is valid only when:

- parent quantities describe one common BOM/kit population;
- quantities are integer-compatible;
- each total is an exact multiple of the per-kit requirement;
- the parent list is authoritative and complete;
- batches can be mapped unambiguously to parent components.

If these conditions are not supported by the workbook, require an explicit BOM or unit-ratio table instead of forcing a GCD interpretation.

## Verification

Assert programmatically that:

- every `R_i` is a positive integer;
- cumulative readiness is monotonic;
- `previous cumulative + increment = current cumulative`;
- readiness never exceeds `K`;
- no event uses a missing or unparseable date;
- components absent from the parent BOM are reported separately;
- every fallback exposes its source field.

## Example pattern

Totals `[5,000, 10,000, 30,000, 30,000, 5,000]` give `K = 5,000` and per-kit requirements `[1, 2, 6, 6, 1]`. A date produces new complete kits only when the cumulative quantities satisfy all five ratios; total delivered pieces alone are insufficient.
