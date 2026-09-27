# Cross-border marketplace category research

Use this workflow when choosing product categories for importing into a country and selling through major marketplaces.

## Evidence stack

Do not equate a large import category with a good marketplace niche. Build two separate layers, then reconcile them:

1. **Macro supply dependence** — bilateral trade by HS chapter from an official customs source or UN Comtrade.
2. **Consumer and marketplace demand** — current national e-commerce reports plus first-party marketplace seller analytics.
3. **Regulatory feasibility** — tariff code, technical regulations, conformity documents, mandatory traceability/marking, and marketplace document rules.
4. **SKU economics** — dimensions, weight, breakage, returns, variant count, advertising, storage, and landed cost.

## Source hierarchy and useful primary sources

- UN Comtrade public API for bilateral HS data: `https://comtradeapi.un.org/public/v1/preview/C/A/HS`
  - Query exporter/reporter, importer/partner, annual frequency, export flow, and `cmdCode=AG2` for HS chapters.
  - If the requested year is unavailable, explicitly label the latest available detailed year as a structural benchmark. Never silently present it as current-year data.
- Russian e-commerce category context: AKIT analytics, `https://akit.ru/analytics/analyt-data`.
- Wildberries first-party niche validation: `https://seller.wildberries.ru/instructions/ru/ru/material/product-niche-analytics`.
- EAEU technical regulations: `https://eec.eaeunion.org/comission/department/deptexreg/tr/`.
- Russia mandatory marking calendar and code check: `https://честныйзнак.рф/marking_calendar/` and `https://честныйзнак.рф/checking_codes/`.
- Marketplace conformity-document guidance: `https://seller.wildberries.ru/instructions/ru/ru/material/certificates-and-conformity-declarations`.

URLs are entry points, not timeless proof of a deadline. Re-open them for every new report.

## Recommended output shape

Separate the deliverable into:

### A. Largest imports overall

- Rank broad HS groups only from retrieved data.
- State the reporting direction: importer-reported imports or exporter-reported exports.
- State the exact reference year and retrieval date.
- Explain why industrial equipment, vehicles, chemicals, or bulky goods may be poor choices for a small seller despite large trade value.

### B. Small/medium marketplace opportunities

For 10–15 candidate categories show:

- safe initial product scope and explicit exclusions;
- seasonality;
- relative competition (`low/medium/high`) labelled as analyst assessment unless measured;
- certification, declaration, state-registration, or marking risk;
- logistics/return risk;
- beginner verdict.

Prefer compact, low-breakage, non-electric, non-liquid goods with few size variants and bundle potential. Treat claims such as `children's`, `medical`, `protective`, or `food contact` as regulatory attributes that can change the applicable rules.

## Regulatory gate before recommendation

1. Determine intended use and likely EAEU tariff code; do not classify from the marketplace title alone.
2. Check applicable EAEU technical regulations.
3. Determine the required conformity route: certificate, declaration, state registration, or none.
4. Check mandatory marking by code and effective date, not by broad category name.
5. Verify that the importer/applicant and document ownership fit the intended supply chain.
6. Request composition/materials, Russian labels and instructions, manufacturer details, test reports, and production samples before a purchase order.
7. Exclude dangerous, controlled, illegal, safety-critical, or high-liability goods unless the task explicitly concerns a qualified operator.

## Common beginner red flags

- Apparel and footwear: variants, returns, light-industry conformity, and marking.
- Children's goods and toys: enhanced safety rules and age/material requirements.
- Cosmetics, household chemicals, supplements, food, and feed: composition, registration, expiry, and traceability.
- Batteries, chargers, radioelectronics, and appliances: multiple technical regulations, warranty, fire and transport risk.
- Safety-critical auto parts, PPE, medical goods, gas/fire products, and pyrotechnics: disproportionate liability.
- Bulky furniture, glass, ceramics, and large appliances: damage, storage, assembly, and expensive returns.

## Verification

Before delivery:

- Keep the macro year distinct from the market-demand year.
- Cite every external factual claim inline.
- Do not publish figures parsed from charts or PDFs unless extraction is reliable and the labels are visible.
- Label seasonality and competition as qualitative judgment unless backed by retrieved measurements.
- Validate a proposed niche at SKU/query level rather than category level.
