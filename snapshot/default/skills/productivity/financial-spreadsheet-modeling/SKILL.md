---
name: financial-spreadsheet-modeling
description: "Use when building auditable financial Excel models."
version: 1.0.0
author: MASTER
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [excel, finance, payroll, tax, auditability, reporting]
    category: productivity
    related_skills: [xlsx]
---

# Financial Spreadsheet Modeling

Build professional, auditable Excel workbooks for payroll, budgets, invoices, cash flow, pricing, and other financial calculations. Use the `xlsx` skill for file mechanics; this skill governs financial model structure, assumptions, controls, presentation, and verification.

## When to Use

Use when the user asks for a spreadsheet that calculates money, taxes, rates, payroll, budgets, forecasts, invoices, or management reporting—especially when the result will be reviewed by finance staff or reused as a template.

## Core Principles

1. **Separate inputs, calculations, and outputs.** Put editable rates and organization metadata on a visible `Настройки`/`Assumptions` sheet; transaction or employee inputs on a data sheet; totals and charts on a summary sheet.
2. **Make assumptions explicit.** Never silently choose a tax base, whether an amount is gross/net, or whether a rate is inclusive/exclusive. Put the adopted interpretation in the workbook and surface material legal/accounting caveats.
3. **Preserve auditability.** Prefer transparent row formulas and absolute references to hidden constants or opaque code. A reviewer should be able to trace every summary number to source rows.
4. **Distinguish inputs visually.** Use a restrained legend: one fill for editable inputs, another for calculated cells, and a third for warnings. Do not rely on color alone; add labels or notes.
5. **Treat templates as operational artifacts.** Include filters, frozen headers, print settings, number formats, validations, meaningful metadata, and enough blank rows for the requested scale.
6. **Verify structure and formula coverage.** A valid `.xlsx` archive is not sufficient; inspect first and last calculation rows, rates, ranges, tables, validations, and summary formulas.

## Workflow

### 1. Define the model contract

Identify:
- unit of analysis (employee, invoice, department, month);
- number of rows required;
- input fields;
- rate assumptions and their bases;
- expected outputs and summary metrics;
- currency, locale, and period;
- whether calculations are statutory, illustrative, or scenario-based.

When the requested accounting treatment appears unusual, proceed with a clearly labelled scenario if the request is otherwise safe and reversible, but add a prominent professional caveat rather than presenting it as universal law.

### 2. Design workbook layers

Recommended sheets:
- **Summary / Сводка:** key totals, counts, status breakdown, restrained chart.
- **Data / Расчёт:** one native Excel table with stable columns and row formulas.
- **Settings / Настройки:** editable rates, period, organization, responsible person, methodology note.
- **Lists / Справочники:** validation values; hide only if users do not need routine access.

### 3. Build robust formulas

- Store rates once on the settings sheet and use absolute references.
- Round monetary tax calculations explicitly to two decimal places when appropriate.
- Return blank output for blank input rows, e.g. `IF(Input="","",ROUND(...,2))`.
- Keep gross amount, tax base, tax, net amount, and total cost in distinct columns.
- Make summary formulas cover exactly the requested data rows.
- Set workbook recalculation flags (`calcMode=auto`, `fullCalcOnLoad`, `forceFullCalc`) because `openpyxl` does not evaluate formulas.

### 4. Add professional controls

- Native Excel table and autofilter.
- Freeze panes below the title/header area.
- Data validations for statuses, categories, dates/days, and non-negative amounts.
- Cell comments for ambiguous financial fields.
- Conditional formatting for operational statuses and exceptions.
- Currency, percentage, and date formats appropriate to the locale.
- Landscape/A3 or suitable print scaling for wide operational tables.
- Do not use worksheet protection as a security control; it is only an editing convenience.

### 5. Verify before delivery

At minimum verify programmatically:
- archive integrity (`zipfile.ZipFile(...).testzip()` returns `None`);
- expected sheet names and dimensions;
- exact requested row count;
- first and last identifiers;
- rate cells contain the requested numeric percentages;
- first and last calculation rows contain formulas;
- summary ranges reach the final data row;
- table, validation, and chart counts;
- recalculation flags are enabled.

Also calculate one deterministic sample independently (for example with `Decimal`) and report the expected gross/tax/net values. This checks the intended financial logic even when no spreadsheet calculation engine is installed. If LibreOffice or Excel is available, recalculate and inspect cached results; otherwise disclose only that live formula evaluation was unavailable, not that the workbook is unverified.

## Reusable Scenario References

- For payroll and tax models, see `references/payroll-tax-scenarios.md`. It documents a clean column architecture, scenario handling for unusual tax requests, and a compact verification checklist.
- For neighborhood retail viability and break-even analysis, see `references/retail-store-unit-economics.md`. It defines a three-scenario traffic/conversion model, startup cash needs, break-even thresholds, payback interpretation, compliance gates, and verification checks.

## Pitfalls

- **Do not embed rates in every formula.** Users must be able to change assumptions once.
- **Do not conflate tax base and gross amount.** They may match in a simplified scenario, but they remain conceptually separate.
- **Do not label scenario calculations as statutory truth.** Taxability and rates can depend on jurisdiction, date, worker classification, deductions, and thresholds.
- **Do not fill blank templates with invented personal data.** Use neutral IDs and blank names unless sample data is explicitly requested.
- **Do not claim formulas were calculated by `openpyxl`.** It writes and reads formulas but does not execute them.
- **Do not stop at file creation.** Inspect the resulting workbook and attach the verified artifact to the user-facing response.

## Delivery Standard

The final response should lead with the downloadable file, summarize included sheets and automation, state what was verified, and include only material accounting caveats. Avoid burying the artifact under a long explanation.
