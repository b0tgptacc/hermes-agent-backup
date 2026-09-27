# Russian company registry workflow

Use this note when researching a Russian legal entity from public sources.

## Identity first: FNS EGRUL

The public FNS search at `https://egrul.nalog.ru/` is the primary source for legal identity. Query by exact INN when available; name-only searches can return many same-name entities.

The public web flow may expose read-only JSON used by the frontend:

1. POST a form query to `https://egrul.nalog.ru/` with the INN in `query`.
2. The response returns a temporary search token `t`.
3. GET `https://egrul.nalog.ru/search-result/{t}`.
4. Validate the returned INN, OGRN, region, registration date, exact legal name, status, and director.

Tokens are ephemeral. Cite the stable EGRUL landing page and state “lookup by INN …” rather than publishing a token URL. Do not automate around a CAPTCHA if one is required.

## Aggregator cross-checks

Russian corporate aggregators such as Checko, Rusprofile, and ЗаЧестныйБизнес can expose normalized data sourced from FNS, Rosstat, courts, procurement, enforcement, and other public registers. Use them to:

- discover ownership percentages and related entities;
- inspect filed financial statements and ratios;
- check staff counts, tax payments, court cases, enforcement, procurement, and vacancies;
- cross-check that the exact INN/OGRN matches.

Treat proprietary reliability scores as the service’s opinion, not an official fact.

## Financial reconciliation

Two services may both be correct while showing different headline numbers. Check labels and filing rows:

- `выручка` is sales revenue;
- `доходы` may include other income;
- `чистая прибыль` is not operating profit;
- taxes and insurance contributions may be separate or combined.

Prefer the figure directly tied to the filed accounting row. State both only when the distinction is useful. Never average the values.

Derived checks should be calculated deterministically:

- net margin = net profit / revenue;
- equity ratio = equity / assets;
- estimated liabilities = assets - equity.

## Operational interpretation

A newly registered company with a large staff and immediate material revenue may indicate a transfer of an existing team or contracts. This is an inference until supported by a merger, asset-transfer disclosure, employee history, project announcement, or predecessor-company evidence.

Registered OKVED codes establish permitted/declared scope, not proven delivery capability. Verify active work through projects, named customers, SRO membership, licenses, vacancies, procurement, and filed operating evidence.

## Relationship checks

When comparing a Russian firm with a foreign engineering group, separate:

- equity ownership or shared parent;
- disclosed joint venture;
- documented EPC/subcontract relationship;
- same-project participation;
- mere sector similarity.

Absence of a foreign shareholder in EGRUL disproves direct disclosed equity ownership, but does not disprove contracts, consortiums, or subcontracts.
