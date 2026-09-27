# Autonomous OSS Pilot Portfolio Research

Use this workflow when curating demonstrable automation/AI pilots for an organization that cannot yet grant internal-system access and does not want replacements for working systems.

## Portfolio constraints

Treat these as hard gates:

- No replacement for established ERP, CRM, EDI/e-signature, TMS, HRM, banking, or BI systems unless replacement is explicitly requested.
- No dependency on internal APIs, databases, mailboxes, network shares, or production credentials.
- Inputs are manual uploads of synthetic, public, or sanitized files; outputs are advisory reports or downloadable artifacts.
- Confidential data stays local unless an approved data-processing route exists.
- Human approval remains mandatory for legal, financial, HR, compliance, and operational decisions.
- Prefer a thin domain layer over mature permissively licensed OSS rather than reimplementing OCR, RAG, analytics, optimization, or transcription engines.

## Research method

1. Map departments and recurring manual decisions, not just software categories.
2. Separate a business scenario from its reusable technical substrate. For example, document extraction can support both shipment-document reconciliation and supplier-quote normalization without becoming two unrelated platforms.
3. Search for mature repositories that own the expensive generic capability. Verify repository status, license SPDX identifier, maintenance recency, and whether the visible license has extra terms or mixed-license assets.
4. Prefer MIT, Apache-2.0, or BSD. Treat AGPL, source-available, `NOASSERTION`, custom/additional terms, and mixed datasets/models as explicit legal-review flags rather than silently accepting them.
5. Define the pilot as `manual input -> observable transformation -> human-reviewable output`.
6. Give every pilot a fixed evaluation set, baseline, success metric, failure boundary, and deletion path.
7. Rank the portfolio using explicit weighted criteria such as business value, demonstration clarity, isolation from internal infrastructure, OSS reuse, and implementation effort. Label the score as comparative judgment, not ROI.
8. Recommend a small first wave rather than building everything. A strong default is one document workflow, one file-based analytics workflow, and one cited local knowledge workflow.

## Acceptance criteria for each candidate

Record:

- departments and user;
- concrete problem and non-goals;
- exact OSS repositories and licenses;
- what the organization-specific thin layer must add;
- input and output;
- demonstration script;
- measurable baseline and target;
- data/privacy constraints;
- human-in-the-loop boundary;
- estimated complexity and the assumptions behind it;
- what production access would be needed only after the isolated pilot succeeds.

## High-value patterns

- Cross-document reconciliation with source-page evidence.
- Supplier-quote normalization using the same document pipeline.
- Reproducible KPI reports from CSV/XLSX snapshots with schema validation and reconciliation totals.
- Local knowledge search that must cite source passages and fail closed when evidence is absent.
- Local PII masking evaluated on a jurisdiction-specific labeled set.
- Public-site change detection with exact diffs and respect for terms/robots/rate limits.
- Route or capacity what-if simulation clearly labeled as non-TMS.
- Anomaly ranking as a review queue, never an accusation or automatic block.
- Forecasting only when backtested against a naive baseline.

## Common failure modes

- Proposing another system of record because it has an impressive open-source demo.
- Calling a generic chatbot a business result without a fixed question set and citation accuracy test.
- Counting GitHub stars as quality; stars are only a maturity signal and are dynamic.
- Omitting the custom thin layer, making the recommendation look like a list of repositories rather than an executable pilot.
- Promising time savings or financial benefit without a measured manual baseline.
- Using real confidential documents during a no-access proof of concept.
- Treating model output as a final legal, HR, finance, or operations decision.
- Building a shared platform before one narrow scenario has passed its acceptance test.

## Deliverable structure

Lead with the recommended first wave and why. Then provide a ranked table and short project cards. End with:

- isolated pilot architecture;
- 30-day or sprint sequence;
- explicit exclusions;
- license/date caveat;
- sources for every repository and external fact.
