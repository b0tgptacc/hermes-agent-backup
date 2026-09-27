# Worked anonymized logistics XLSX case

This reference records a validated reasoning pattern from an anonymized workbook. Identifiers are synthetic; values illustrate the checks, not a reusable business truth.

## Source shape

- One worksheet with master ORD rows, PRD component rows, later ORD party rows, plan/fact quantities, milestone dates, and anonymized `FML_`/`STR_` tokens.
- Seven inferred master assemblies.
- Immediate PRD rows after each master ORD were treated as BOM demand.
- Later ORD child rows were treated as party/delivery detail.

## Double-count proof

For one assembly/component:

```text
master requirement = 5,000
party quantities = 100 + 1,900 + 3,000 = 5,000
```

Adding master and parties produces 10,000, but this is the same volume represented twice. A second component showed the same conservation pattern:

```text
master = 10,000
parties = 4,000 + 6,000 = 10,000
```

Therefore master and detail must be modeled as different roles.

## Correct unique-component formula

```text
BOM_sum[p] = Σ master B for unique PRD p
G = gcd(BOM_sum[p])
per_set[p] = BOM_sum[p] / G
delivered[p] = Σ eligible party quantity for p
sets[p] = floor(delivered[p] / per_set[p])
complete = min_p(sets[p]), cap G
```

Literal `delivered[p] / G` was falsified by examples: it returned 1 instead of 5,200 for one assembly and 5 instead of 10 for another because it ignored component multiplicity.

## Positions without dates

A later requirement asked that every known position count toward kit quantity even when no date existed. The accepted model separated:

```text
all_positions_quantity[p] = max(BOM_sum[p], delivered_total[p])
quantity_only_sets[p] = floor(all_positions_quantity[p] / per_set[p])
dated_sets[p] = floor(dated_delivery[p] / per_set[p])
```

The `max` policy was valid only because party totals were confirmed as partitions of master totals. Missing dates stayed null and produced no calendar event.

## Meta-kit hypothesis

The seven assembly quantities were:

```text
5,200; 60,000; 60,200; 5,000; 10; 5,000; 1,000
```

Their GCD was 10, giving ORD norms:

```text
520; 6,000; 6,020; 500; 1; 500; 100
```

Each ORD supported 10 quantity-only meta-kits. Dated support was:

```text
10; 10; 10; 10; 10; 0; 0
```

so dated meta-kit completeness was zero. This was labeled a user business hypothesis because the XLSX had no explicit parent-kit relationship.

## Verified probes

The delivered dashboard package was required to reject mutations for:

- extra or missing component fields;
- negative quantities and bad IDs;
- incorrect per-set norm;
- incorrect floor/cap result;
- incorrect limiting flag;
- component-summary mismatch;
- meta-kit GCD, norm, minimum, or missing ORD position mismatch;
- impossible dates and readiness above 100%.

UI checks used real desktop and 390×844 mobile screenshots. The mobile probe asserted `scrollWidth == clientWidth`, while wide component tables retained intentional container-level horizontal scrolling with a visible hint.
