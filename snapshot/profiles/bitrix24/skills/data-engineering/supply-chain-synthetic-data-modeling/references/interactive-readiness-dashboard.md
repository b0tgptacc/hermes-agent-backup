# Interactive per-unit readiness dashboards

Use this pattern when a BOM or supply-plan fixture must drive an interactive timeline and calendar showing the readiness date of every finished set/unit.

## Data contract

Keep one canonical structured dataset and derive every presentation from it:

- `lots`: one row per component delivery with `(date, SKU, lot, quantity)`;
- `sets`: one row per finished set with `set_no`, `assembly_date`, per-component readiness dates, and bottleneck SKU(s);
- `milestones`: groups of consecutive sets that become ready on the same date;
- `components`: required quantity, lot count, first delivery, and full-delivery date.

For finished set `n`, compute each mandatory component's readiness date as the first delivery date on which cumulative quantity reaches `n × qty_per_set`. The set assembly date is the maximum of those component dates. Every component tied at that maximum is a bottleneck.

Never derive the dashboard separately from the workbook. Generate JSON and XLSX from the same in-memory model so they cannot drift by construction.

## Randomness that remains auditable

"More random" should mean visibly heterogeneous but reproducible:

1. Derive an independent RNG stream from a scenario seed plus SKU.
2. Give each component an independently sampled lot count and date sequence.
3. Split required quantity with skewed positive weights (for example, log-normal weights), then correct rounding so the lots sum exactly to requirement.
4. Sample irregular dates over a wide horizon rather than adding a fixed cadence.
5. Verify meaningful variation, not merely that a PRNG was called:
   - at least several distinct quantities per SKU;
   - minimum and maximum date gaps differ materially;
   - complete ordered schedules are not identical across SKUs;
   - every planned total reconciles exactly.

Report useful variability diagnostics such as lot-count range, min/max quantity, coefficient of variation, min/max date gap, and schedule span.

## Dashboard composition

A useful operational composition is:

- direct lookup for a finished-set number;
- timeline of readiness milestones with set ranges and cumulative total;
- month calendar combining component arrivals and new-ready-set events;
- component cards showing uneven lot volumes and date spans;
- a detail dialog listing the readiness date of every required component and highlighting the bottleneck.

Calendar cells should identify events through accessible labels. When a month opens, select its first event date automatically so the detail panel is informative rather than blank. On mobile, keep all primary view tabs simultaneously visible; do not rely on a clipped horizontal tab strip.

## Local standalone delivery

For a dependency-free local dashboard, serve static HTML/CSS/ES modules plus JSON through a loopback HTTP server. Do not instruct users to open the HTML directly because module imports and `fetch()` are commonly blocked under `file://`.

A launcher should bind the server first and only then open the browser. A small Python launcher using `ThreadingHTTPServer`, followed by `webbrowser.open()`, avoids the race caused by opening the URL before the server is listening. Bind to `127.0.0.1` unless LAN access is explicitly required.

## Verification gate

1. Unit-test uneven independent schedules, exact component totals, monotonic per-set readiness, milestone reconciliation, and export structure.
2. Re-open the XLSX and compare every normalized row against JSON—not only row counts. Normalize Excel `datetime` values to ISO dates before comparison to avoid false mismatches.
3. Run real-browser smoke tests at desktop and mobile widths:
   - page has no horizontal overflow;
   - no console or page errors;
   - search an interior set number and verify its dialog/date;
   - switch through timeline, calendar, and components;
   - verify the expected milestone/day/component counts.
4. Capture and visually inspect every primary view on both widths.
5. Have an independent reviewer verify calculations, exports, screenshots, and launcher behavior. Treat delegated findings as hypotheses until reproduced with a concrete differing record.

## Pitfalls

- Comparing XLSX tuples directly to JSON objects produces false mismatch reports because schemas and date types differ. Map columns explicitly and normalize dates first.
- A calendar with only dots but an empty detail panel looks unfinished. Auto-select the first event in the visible month.
- Removing runtime dependencies does not mean discarding reproducible QA. Keep the lockfile and smoke script; generated `node_modules` may be cleaned after verification.
- A successful HTTP response does not prove interaction quality. Exercise lookup, dialogs, tabs, month navigation, and representative event cells in a browser.
