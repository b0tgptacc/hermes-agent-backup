# Evaluating Self-Hosted CRM/ERP for Domain-Specific Operations

Use this reference when selecting an open-source CRM for a company whose real workflow extends beyond sales into logistics, service delivery, finance, or another operational domain.

## 1. Start with the operating model, not the product list

Map the end-to-end flow before ranking products. For logistics/freight forwarding, a useful chain is:

`lead → rate request → quotation → customer order → logistics job → shipment/legs/events/documents → landed cost → invoice/payment → claim → analytics`

Separate capabilities into:

- **CRM:** parties, leads, opportunities, communication, tasks, pipeline.
- **ERP:** quotations, orders, purchases, inventory, invoices, payments.
- **TMS/domain operations:** jobs, cargo, route legs, containers/AWB, milestones, carriers, exceptions, claims, tracking portal.
- **Regulated accounting:** statutory invoices, payments, tax reporting, accounting FX, filings.

Do not award an ERP/CRM full logistics credit merely because it has a generic `Shipment` record. Verify multi-leg routing, cargo/consolidation, event history, documents, exceptions, carrier costs, and customer tracking separately.

## 2. Treat an existing verified custom module as an asset

If the company already has a tested domain module—especially a financial calculator with deterministic math, immutable revisions, hashes, or audit history—do not assume migration is beneficial.

Compare three trajectories:

1. strengthen the existing application;
2. integrate it as a bounded service with a packaged CRM/ERP;
3. rewrite it inside the candidate platform.

Default to preserving the verified module until a PoC proves that replacement reduces total cost without weakening correctness or auditability. Never duplicate financial formulas in low-code workflows, client scripts, or a second service.

## 3. Build a System-of-Record matrix before architecture approval

For every shared entity and material field, name exactly one writable owner. At minimum cover:

- Customer, Contact, Lead, Deal;
- Job, Shipment, Route Leg, Container, operational status;
- calculation inputs, calculation FX/source/date, formula version, revision, result, recommended price;
- customer-facing quotation number/version/currency/price/status;
- legal invoice, payment, accounting FX, tax status, receivables;
- calculation PDF, commercial proposal, regulated primary documents.

For each row state:

- authoritative system;
- what other systems may cache or mirror;
- whether the mirror is read-only;
- required external ID, revision, and hash;
- cutover rule for legacy records.

Distinguish calculation FX, quotation currency, and accounting FX. They may legitimately differ and must not overwrite one another.

## 4. Score fit and eligibility separately

A weighted score is useful for ranking, but it must not hide a must-have failure.

Recommended dimensions:

- daily CRM UX;
- ERP/operational baseline;
- domain extensibility;
- API/webhooks/integration;
- RBAC/audit/data control;
- upgrade safety;
- license/self-host freedom;
- maturity/ecosystem.

Publish weights, per-dimension 0–5 scores, and the formula:

`total = Σ((score / 5) × weight)`

Add an independent eligibility column. Examples of hard failures:

- audit or row-level permissions require an unacceptable paid tier;
- no supported extension boundary;
- regulated accounting localization is unverified;
- upgrade cannot preserve custom modules;
- export/restore is incomplete;
- candidate requires two writable financial sources of truth.

## 5. Audit open-source and open-core boundaries feature by feature

Do not infer freedom from the repository headline. Verify from official license files and documentation:

- core license;
- enterprise-marked files or packages;
- paid workflow/reporting/audit/SSO/row-permission features;
- proprietary marketplace modules;
- license effect of modifying the server versus integrating through APIs/SDKs;
- self-host restrictions and support boundaries.

Record the exact edition or package that provides each must-have capability.

## 6. Prefer a vertical-slice PoC over a broad demo

Run the same representative workflow on no more than three trajectories. For logistics:

1. deal → quotation;
2. create a logistics job without duplicating the customer;
3. shipment with multiple legs and status history;
4. multiple suppliers/carriers and actual costs;
5. call the existing calculator with an idempotency key;
6. finalize a revision and publish `calculation_id + revision + hash` into the quotation;
7. modifying the calculation creates a new quotation version and does not rewrite an accepted one;
8. role tests for sales/operations/finance;
9. backup → destroy → restore;
10. staging upgrade with all custom and integration tests;
11. reconciliation detects a missed webhook and revision/payment-status mismatch;
12. post-cutover writes to legacy invoice/payment stores are rejected.

Use fail-closed acceptance: one failed mandatory scenario makes the candidate ineligible regardless of score.

## 7. Architecture defaults

- Integrate through documented APIs/webhooks; never write directly into another product's database.
- Use idempotency keys, an outbox/event log, external-ID mappings, retries, and reconciliation jobs.
- Store immutable display snapshots only where historical documents require them; do not create a second editable master record.
- Keep statutory accounting in the validated accounting system until localization is independently verified.
- Require staging upgrade rehearsal, database backup, and restore verification before production.

## 8. Decision rule

Choose a packaged platform only if the PoC shows that standard features plus stable extension points materially reduce development and operational burden. If nearly every differentiating workflow still needs custom code, extending the existing modular application may be safer and cheaper than migrating for the sake of adopting a named CRM.
