---
name: operational-spreadsheet-dashboards
description: Use when building auditable operational Excel dashboards.
version: 1.0.0
metadata:
  hermes:
    tags: [excel, dashboard, operations, timeline, plan-fact, audit]
    category: productivity
---

# Operational Spreadsheet Dashboards

Build decision-ready `.xlsx` dashboards from operational tables while preserving traceability to the source rows. Use this skill for production, logistics, procurement, inventory, milestone, plan/fact, and readiness reporting.

## Principles

- Treat source labels, prefixes, formulas, dates, and row hierarchy as data contracts; inspect them before designing the dashboard.
- Derive business entities and event boundaries explicitly. Do not infer that every repeated identifier is a top-level object.
- Separate **plan**, **fact**, and **operational fallback**. Never present a plan date as fact.
- Fail closed on placeholders, text tokens, anonymized formulas, and unparseable dates. Surface them in a dedicated problems view.
- Keep calculations auditable: expose source row, quantity source, date source, and any fallback used.
- Prefer one continuous chronological event table over decorative summary-only sheets.

## Workflow

1. **Inspect the workbook**
   - Inventory sheets, dimensions, merged cells, hidden sheets, tables, formulas, date formats, and row prefixes.
   - Dump representative header rows and every hierarchy/header row.
   - Count identifier reuse and inspect immediate child rows; repeated order identifiers often represent batches rather than parent objects.

2. **Define the semantic model**
   - Identify parent entities, component rows, batch/event rows, quantity fields, milestone dates, and plan/fact pairs.
   - Write the rules down before calculation: entity boundary, quantity precedence, date precedence, capping, and missing-data behavior.
   - If a single-child batch stores values on the parent row while the child is blank, inherit only for that child and record the source cell.

3. **Normalize events**
   - Convert each batch into component-level events with explicit fields: parent ID, batch ID, component ID, milestone, plan/fact, date, quantity, source row/cell.
   - Keep unusable values as issues; do not coerce formula placeholders or arbitrary strings to numbers/dates.

4. **Calculate readiness**
   - For ratio-based kits/BOMs, derive the per-unit requirement from the authoritative total quantities.
   - Accumulate component quantities chronologically.
   - At each date calculate the minimum component coverage; emit a readiness event only when complete-unit count increases.
   - Cap completion at the authoritative total and reconcile every increment to the cumulative value.
   - For the validated GCD method and its constraints, see `references/gcd-kit-readiness.md`.

5. **Design the workbook**
   - Provide, when applicable:
     - a continuous party/event timeline;
     - a complete-unit readiness timeline;
     - a calendar view;
     - a problems/data-quality view;
     - a methodology sheet;
     - a hidden normalized audit base.
   - Use native Excel tables, filters, frozen panes, consistent date formats, conditional formatting, and internal navigation links.
   - Put operational KPIs above tables, not instead of them.

6. **Verify**
   - Reopen the generated workbook and validate ZIP integrity.
   - Confirm sheet names, dimensions, table refs, hidden/visible state, filters, freeze panes, charts, and navigation links.
   - Programmatically assert chronological sorting, cumulative reconciliation, and completion caps.
   - Open in an installed spreadsheet application for visual inspection when available; check titles, widths, clipped charts, calendar labels, and plan/fact status colors.

## Plan/Fact Rules

- Prefer actual date and actual quantity when both are usable.
- When fact is absent, a plan fallback may be used only in a clearly named operational scenario such as `План — факт отсутствует`.
- Keep a separate pure-plan scenario when comparisons are useful.
- Record quantity precedence in the workbook methodology and expose the chosen source on event rows.
- Never silently fill a missing date from another milestone.

## Data-Quality View

Create one row per actionable issue with:

- severity;
- parent and batch identifiers;
- component identifier;
- source row/cell;
- affected field;
- problem description;
- raw value;
- recommended correction.

Avoid flagging parent/master rows merely because their child-owned fields are blank. Flag missing values only when the corresponding stage or quantity makes the field materially expected.

## Pitfalls

- A unique order ID is not sufficient to identify a parent; combine identifier frequency with child-row quantity patterns.
- Summing all delivered pieces does not measure kit readiness. Use the bottleneck component after applying per-kit ratios.
- A batch date based on multiple components should normally be the latest usable component date for that milestone.
- Spreadsheet libraries do not evaluate formulas. If formulas were anonymized into tokens, their values are unknown and must remain unknown.
- Calendar month names can inherit an English process locale; use an explicit localized month mapping for user-facing workbooks.
- Do not call a workbook complete after saving it. Reopen, validate arithmetic, and inspect it visually.

## Acceptance Criteria

- Every visible figure traces to source data or a disclosed fallback.
- Chronological tables are actually sorted.
- Readiness increments reconcile to cumulative readiness and never exceed the authoritative total.
- Missing or unusable dates are discoverable in the problems sheet.
- The workbook opens without repair warnings and remains usable with filters and frozen headers.
