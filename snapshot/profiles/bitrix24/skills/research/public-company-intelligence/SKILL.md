---
name: public-company-intelligence
description: "Use when profiling companies from public registry evidence."
version: 1.0.0
metadata:
  hermes:
    tags: [research, companies, registries, ownership, financials, due-diligence]
    related_skills: [grounded-citations, blocked-page-recovery, product-market-research]
---

# Public Company Intelligence

Build an evidence-based profile of a legal entity from authoritative registries, company disclosures, and corroborating public sources. Use for “tell me about this company,” ownership checks, relationship mapping, counterparty reconnaissance, and lightweight pre-diligence. This is not a legal, sanctions, or credit opinion.

## Required output model

Separate five layers explicitly:

1. **Legal identity** — exact name, registration identifiers, date, status, address, director.
2. **Ownership and control** — shareholders/participants, percentages, controlling person, related entities.
3. **Actual operating profile** — services, workforce, projects, customers, licenses/SRO, website claims.
4. **Financial condition** — revenue, profit, assets, equity, liabilities, liquidity, taxes, trend.
5. **Risk and relationship assessment** — established facts, calculated indicators, inferences, unknowns.

Never let a registered activity code stand in for proof that the company actually performs that work.

## Workflow

### 1. Resolve the exact entity

- Search by exact legal name plus city, then validate identifiers.
- Preserve INN/registration numbers exactly; do not normalize or repair them.
- Treat same-name entities as separate until identifiers match.
- Prefer the official national registry for identity, status, registration date, and director.

### 2. Establish ownership and control

- Record every disclosed owner and percentage.
- Identify the controlling owner rather than merely listing participants.
- Follow director and owner links to related companies in the same sector.
- Distinguish legal ownership from commercial relationships. Shared projects, email domains, or marketing references do not prove group control.

### 3. Test operational substance

Look for independent indicators of real activity:

- employee count and its year;
- revenue and tax payments;
- active vacancies;
- project references and named customers;
- licenses, SRO memberships, certificates;
- procurement records, court cases, inspections, and enforcement proceedings;
- functioning website and domain-linked business contacts.

A young entity with a large workforce and immediate revenue may reflect a team, contract, or business transfer. State this only as an inference unless the transfer is documented.

### 4. Reconcile financial fields

Do not average or silently choose between services. Check whether each number means:

- revenue from sales;
- total income;
- profit before tax;
- net profit;
- assets;
- equity;
- taxes plus insurance contributions.

Use deterministic calculations for margins and ratios. Label every derived value as calculated. Useful lightweight checks:

- net margin = net profit / revenue;
- equity ratio = equity / assets;
- estimated liabilities = assets - equity;
- current liquidity and autonomy when source fields support them.

A positive profit does not cancel weak liquidity or very low equity. Present both.

### 5. Recover data when the visible page is blocked

- Prefer a public official registry endpoint or the read-only JSON endpoint used by the site’s own frontend.
- For SPAs, inspect shipped JavaScript for endpoint paths and HTTP methods, then reproduce only public unauthenticated reads.
- Do not bypass authentication, CAPTCHAs, access controls, or paid boundaries.
- If an API URL contains an ephemeral token, cite the stable landing page and state the lookup key used.
- A company website outage is a verification limitation, not evidence that the company is inactive.

### 6. Write the assessment

Lead with a concise conclusion, then cover identity, activities, ownership, scale, financials, and risks. Mark:

- **Fact:** directly supported by a source.
- **Calculation:** derived deterministically from cited values.
- **Inference:** plausible interpretation of facts.
- **Unknown:** not established from public evidence.

For relationship questions, answer separately:

- ownership/control relationship;
- shared parent or shareholders;
- documented contract/project relationship;
- only sectoral similarity;
- no public evidence found.

## Source hierarchy

1. Official corporate/national registry.
2. Filed financial statements and regulator disclosures.
3. Official company or parent-group site.
4. Procurement, court, enforcement, licensing, and SRO registries.
5. Reputable aggregators that expose their upstream sources.
6. News, directories, and marketing pages.

Use aggregators for discovery and cross-checking, not as a substitute for official identity data when the registry is accessible.

## Pitfalls

- **Name collision:** profiling the wrong same-name company.
- **Activity-code inflation:** describing every registered code as an active capability.
- **Revenue/income confusion:** treating different accounting fields as inconsistent copies of one number.
- **Ownership leap:** inferring a parent/subsidiary relationship from collaboration or branding.
- **Current-state overclaim:** using stale archive data for current status.
- **Website overreliance:** accepting portfolio claims without projects, customers, or registry evidence.
- **Young-company narrative:** calling fast growth organic when a business transfer is equally plausible.
- **Risk-score laundering:** repeating a commercial aggregator’s score as an objective conclusion.

## Verification checklist

- Exact entity and identifiers match across sources.
- Registration status and director come from an authoritative source.
- Ownership percentages sum correctly or the unexplained remainder is stated.
- Financial period and metric semantics are explicit.
- Calculations reproduce from cited inputs.
- Relationship claims distinguish ownership from contracts.
- Material limitations are disclosed.
- Every external claim is cited using the `grounded-citations` workflow.

## References

- `references/russian-company-registry-workflow.md` — Russian EGRUL lookup, aggregator reconciliation, and reproducibility notes.
