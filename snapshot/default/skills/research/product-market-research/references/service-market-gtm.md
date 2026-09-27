# Service-market GTM research in under-documented markets

Use this workflow when evaluating demand and customer acquisition for an operational B2B service such as fulfillment, logistics, bookkeeping, or field services.

## Evidence model

Separate three layers:

1. **Observed market facts:** market size, channel growth, number or type of active merchants, platform availability, regulation, payment and delivery constraints. Prefer government country guides, ministries, industry associations, platform documentation, and first-party marketplace pages.
2. **Buyer hypotheses:** likely pain, minimum viable volume, categories to prioritize, and reasons to outsource. Label these as hypotheses until interviews or operating data confirm them.
3. **Execution targets:** outreach volume, meetings, pilots, conversion, CAC, and retention goals. These are management targets, not market statistics; never present them as benchmarks without evidence.

## Segmentation

Segment buyers by operational trigger rather than broad demographics:

- current monthly transaction or order volume;
- number of SKUs or process complexity;
- current channel mix;
- owner time consumed by the operation;
- error, delay, capacity, storage, or staffing pain;
- regulatory or special-handling requirements;
- readiness to run a paid pilot.

Prioritize customers with existing demand and a costly bottleneck. Deprioritize very small accounts, highly customized low-volume work, and regulated or special-handling categories until the operation is ready.

## Offer design

Translate capabilities into outcomes. For fulfillment, sell timely dispatch, accurate inventory, fewer picking errors, and growth without adding warehouse staff—not merely storage and packing.

Use a bounded paid pilot with:

- explicit volume or duration;
- full cost calculation before launch;
- acceptance criteria and SLA;
- measured baseline and after-state;
- a clear path to full rollout.

Avoid invented local prices. Build price from the operator's real unit economics and validate willingness to pay through interviews and pilots.

## Acquisition hierarchy

For a young B2B service, usually test in this order:

1. founder-led, personalized outbound to active buyers;
2. partnerships with adjacent providers who encounter the trigger first;
3. proof assets: process video, calculator, case study, sample report;
4. referrals from successful pilots;
5. targeted paid acquisition and retargeting after message-market fit.

For fulfillment, adjacent partners often include import/cargo firms, customs brokers, packaging suppliers, marketplace consultants, accountants, product studios, web agencies, and couriers.

## Sparse-web retrieval pattern

When local search results are weak, start from known authoritative country and platform pages rather than inferring the market from snippets. Retrieve the page body directly and inspect its server-rendered article text. A standard-library `html.parser.HTMLParser` that skips `script`, `style`, and `noscript` is a dependable fallback for extracting readable body text when a generic shell extraction returns mostly boilerplate. Preserve the source URL and register it in the citation ledger before drafting.

## TAM discipline

Do not convert adjacent-market GMV, internet penetration, marketplace sales growth, or merchant counts directly into a service TAM. These are demand signals, not evidence of outsourced-service spend. A defensible TAM requires credible data for addressable transaction volume, outsourcing penetration, and realized price or take rate. If those inputs are unavailable, say so plainly and use a paid pilot to establish bottom-up cost-to-serve, willingness to pay, and contribution margin instead of inventing a percentage.

## Geographic rollout for physical operations

For services with warehouses, depots, or field capacity, separate market interest from route or facility density. Launch the full operating node in the primary demand center. Test secondary cities with scheduled line-haul, mobile service days, or cross-dock first; commit to a permanent facility only after sustained volume and positive route-level unit economics are observed.

## Deliverable

A decision-ready brief should contain:

- strongest demand signals with citations;
- prioritized ICPs and explicit exclusions;
- pain-to-offer mapping;
- lead-source and partner map;
- outreach message and qualification questions;
- funnel stages and a 30-day experiment plan;
- operating and sales KPIs;
- assumptions, risks, and what must be validated next.
