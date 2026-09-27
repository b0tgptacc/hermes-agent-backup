---
name: auditable-financial-calculators
description: "Use when building auditable financial calculators in apps."
version: 1.0.0
author: MASTER
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [finance, calculators, auditability, decimal, pricing, landed-cost, pdf, web-app]
    category: productivity
---

# Auditable Financial Calculators

Build production financial calculators inside operational applications—pricing,
landed cost, tax, commissions, unit economics, quotes, break-even, budgeting—so
that formulas are explicit, deterministic, reusable across UI/PDF/export, and
independently verifiable.

This skill governs the calculation contract and verification discipline. It is
not specific to spreadsheets or one framework.

## Core Standard

A calculator is complete only when:

1. Inputs, assumptions, calculations, and outputs are visibly separated.
2. Every percentage has an explicit base.
3. Currency normalization and rounding stages are documented.
4. One Decimal-only engine powers stored values, UI, charts, PDF, and exports.
5. Invalid combinations fail at named fields before arithmetic runs.
6. Saved scenarios preserve formula version and calculation timestamp.
7. Two independent reference scenarios match exact expected outputs.
8. PDF/export and responsive UI are exercised, not merely rendered in tests.
9. A fresh finance reviewer and a fresh technical reviewer both pass it.

## 1. Define the Calculation Contract First

Before modeling, resolve material ambiguities:

- jurisdiction and output currency;
- supported input currencies and source of exchange rates;
- whether rates are manual or fetched, and their effective date;
- fixed cost versus rate × driver modes;
- tax/duty bases;
- fee and commission bases;
- inclusive versus exclusive tax treatment;
- per-shipment versus per-unit outputs;
- markup versus margin semantics;
- rounding precision and rounding stage;
- whether calculations are statutory or illustrative scenarios.

Ask in one compact batch. Never silently guess a fee base or treat markup and
margin as synonyms.

## 2. Layer the Model

### Inputs

Keep source values and assumptions editable and typed:

- quantities and physical drivers;
- amount + currency pairs;
- exchange rates;
- percentage rates;
- fixed fees;
- mode selectors;
- calculation date and scenario identity.

### Calculated components

Store or expose every auditable intermediate—not only a final total. A reviewer
must be able to trace the total to normalized components, tax bases, fees and
rounding.

### Outputs

Separate:

- shipment/period total;
- per-unit cost;
- break-even price;
- target price before tax;
- target price after tax;
- warnings and assumptions.

Persist a formula version and calculation timestamp when scenarios are saved.

## 3. Decimal and Rounding Rules

- Use `Decimal` from input to output; never pass money through binary float.
- Define one money quantizer and explicit rounding mode, usually `0.01` with
  `ROUND_HALF_UP` when the business contract requires it.
- Keep FX and percentage inputs at higher precision than money outputs.
- Decide whether to round each converted component or only section totals; test
  the chosen staged behavior.
- Guard every divisor (`quantity > 0`, `margin < 100`).
- A zero-rate mode must not multiply by a missing optional rate; zero should
  deterministically produce zero when the corresponding cost is unused.

## 4. Validation Before Arithmetic

Validation must name the field that fixes the problem:

- missing FX rate for a used non-base currency;
- missing/zero weight for per-weight freight or duty;
- missing/zero volume for per-volume freight;
- negative amounts or percentages;
- margin at or above 100%;
- unsupported mode/currency;
- quantity at or below zero.

Do not continue into arithmetic after collecting validation errors: expressions
such as `price * quantity` can otherwise throw before the user sees the useful
field message.

Progressive disclosure in JavaScript is convenience only. Server/model
validation remains canonical.

## 5. One Calculation Engine

Centralize formulas in a service or model method with a stable contract:

- normalize inputs;
- compute named section totals;
- compute fees/taxes from explicit bases;
- compute overall and per-unit values;
- apply pricing mode;
- round and persist outputs;
- return an ordered breakdown for charts/reports.

Templates/scenarios store input fields only. Filter template payload keys
through an allow-list so calculated outputs, owner, formula version, and audit
fields cannot be injected.

Mutation endpoints such as clone/finalize/apply must be POST-only with CSRF.

## 6. Pricing Semantics

Given cost `C` and target `p` as a fraction:

- markup price: `C × (1 + p)`;
- margin price: `C ÷ (1 − p)`;
- break-even before tax: `C`;
- tax-inclusive price: before-tax price × `(1 + tax rate)` when that is the
  confirmed business contract.

Label outputs explicitly. Do not display a margin formula under a markup label.

## 7. Operational UI

Use the host application's design system. A strong calculator surface includes:

- numbered input sections matching the business checklist;
- visible assumptions/rates;
- mode-specific field disclosure;
- named field errors;
- dominant final cost and per-unit result;
- section breakdown and accessible chart legend;
- formula/audit panel stating every base;
- scenario/template actions;
- a visible methodological caveat when legal/tax values depend on external
  classification or date.

Localize labels and monetary formatting consistently. Search for mojibake and
mixed-language leftovers before browser acceptance.

## 8. PDF and Export

PDF must come from the same saved outputs, never a second implementation of the
formulas.

Requirements:

- Unicode font resolution fails clearly rather than emitting broken glyphs;
- user text is escaped before entering rich-text/markup APIs;
- inputs/rates, section totals, outputs, formulas, version/date, caveat and chart
  are included;
- page breaks avoid orphan headings;
- filename is sanitized;
- exported text round-trips through a PDF parser;
- pages are rasterized and visually inspected for clipping and glyph failures.

## 9. Verification Ladder

### Formula tests

Cover at least:

- percentage-base mode;
- unit-rate mode;
- fixed, per-weight and per-volume modes;
- every supported currency;
- markup and margin;
- zero/empty cost structure;
- invalid drivers, rates and percentages;
- stored-output recalculation after edit;
- safe template round-trip.

### Independent arithmetic

Write a separate small Decimal script that does not import the production
engine. Compare exact named outputs for two scenarios. This detects tests that
merely mirror the implementation.

### HTTP/security

- auth on every route;
- role boundaries;
- admin-only destructive actions;
- clone/apply/finalize POST + CSRF;
- no GET side effects;
- safe PDF user text.

### Browser/PDF

At desktop and mobile verify list, form, detail and templates; conditional
fields; no mojibake, overflow or console errors; touch targets; download the
PDF. Parse PDF text and render each page to image.

### Independent review

Use separate finance and technical reviewers. Finance checks formula contract,
bases and rounding. Technical review checks data integrity, roles, HTTP
semantics, export robustness and responsive UX.

## Pitfalls

- Reimplementing formulas in templates, JavaScript, and PDF separately.
- Citing a final total without intermediate bases.
- Applying percentage fees to an unstated base.
- Using rounded display text as an input to later calculations without declaring
  staged rounding.
- Allowing GET to clone or mutate scenarios.
- Treating tests that import the production engine as independent verification.
- Shipping PDF because `%PDF` exists without checking Cyrillic and page layout.
- Leaving English internal keys or mojibake visible in a localized product.
- Presenting scenario tax/customs treatment as statutory truth.

## Verification Checklist

- [ ] Calculation contract and assumptions are explicit.
- [ ] Decimal engine and rounding mode are centralized.
- [ ] Inputs/calculations/outputs are separated.
- [ ] Named validation covers every mode dependency.
- [ ] Templates contain allow-listed inputs only.
- [ ] Mutation routes are POST + CSRF.
- [ ] Two independent reference scenarios match.
- [ ] UI and PDF use the same saved outputs.
- [ ] PDF Cyrillic/text/layout are verified.
- [ ] Desktop/mobile E2E passed.
- [ ] Finance and technical reviews passed.

## References

- `references/import-landed-cost.md` — worked import/CIF/customs/pricing
  contract, formulas, validation matrix and verification scenarios.
