---
name: international-trade-commercial-proposals
description: Use for cross-border offers with FX and production terms.
version: 1.0.0
metadata:
  hermes:
    tags: [commercial-offer, international-trade, foreign-exchange, incoterms, pdf]
    category: productivity
---

# International Trade Commercial Proposals

Create decision-ready commercial proposals for cross-border goods transactions. The output must make pricing, currency exposure, production capacity, logistics, customs allocation, and acceptance conditions explicit, then ship as a verified business artifact rather than prose alone.

## Trigger

Use for commercial offers, quotations, term sheets, or supplier proposals involving one or more of:

- foreign currency or an exchange-rate clause;
- international transport or Incoterms;
- production lead-time/capacity constraints;
- customs, import VAT, certifications, or export-control checks;
- a requested PDF or client-facing document.

For domestic quotes without these features, use a general document skill instead.

## Inputs and Assumptions

Gather seller/buyer, goods, quantity, technical specification, origin, destination, Incoterm and named place, contract/payment currency, payment milestones, production window, transit assumptions, quote validity, warranty, and required compliance documents.

If the user delegates choices, produce a clearly labeled preliminary project rather than fabricating real legal entities or regulatory facts. Use placeholders for party identities and banking details. Invented line items and prices may be used only as an illustrative commercial model and must be described as such.

## Procedure

1. **Define the commercial model.** Choose a plausible route, named Incoterm place, currencies, payment stages, production window, transit range, warranty, and offer validity. State assumptions that materially change cost or risk.
2. **Build the price table deterministically.** Show quantity, unit, unit price, line total, packaging/documentation, freight, and grand total. Calculate with `Decimal`; never hand-calculate totals or FX examples.
3. **Source the live rate.** Use an authoritative source appropriate to the payment jurisdiction (for Russia, Bank of Russia). Record currency, nominal, rate, and effective date. Cite the primary source in the document.
4. **Write an operational FX clause.** Distinguish currency of price/obligation, informational equivalent, conversion date/source, bank/conversion uplift, stale-invoice reissue rule, and correspondent-bank fees. Include the exact formula and one checked example. Do not present an informational RUB equivalent as a fixed RUB obligation.
5. **Allocate trade responsibilities.** State the Incoterm plus exact named place and version. Explicitly list what the price includes and excludes, especially import clearance, customs duty, import VAT, broker charges, unloading, certifications, and insurance. Incoterms do not replace the sales contract.
6. **Make production timing conditional.** Start the clock only after all prerequisites are satisfied (advance, approved specification, technical data). Separate manufacturing, booking, and transit. State capacity-reservation validity, effects of buyer delay/change orders, partial shipment, and whether dates are estimates or commitments.
7. **Cover acceptance and compliance.** Include document pack, visible/latent defect windows, warranty, export-control/end-use review, sanctions/banking feasibility, force majeure, and any liability cap suitable for legal review.
8. **Set acceptance mechanics.** Give quote validity and make clear that acceptance occurs through a separate contract/specification when appropriate. Add a pre-send checklist for party data, SKU/manufacturer, HS/TN VED code, conformity requirements, named delivery address, route, bank, and governing law.
9. **Draft with citations.** Cite authoritative FX and Incoterms sources inline and include a mechanically generated Sources block when the artifact relies on current external facts.
10. **Produce and verify the artifact.** Generate PDF with a document/PDF skill. Check page count, header/EOF, critical numbers, source dates, and visual layout page by page. An unexpected extra page is a failed layout gate, usually caused by overflow or print rounding; compact and re-export.

## Recommended Document Structure

1. Cover, parties, project status.
2. Specification and price summary.
3. Delivery basis and included/excluded costs.
4. Currency and FX clause.
5. Payment milestones.
6. Production and logistics timeline.
7. Quality, acceptance, documents, warranty.
8. Liability, compliance, force majeure.
9. Validity, acceptance, pre-signing checklist.
10. Sources and signatures.

## Quality Gates

- Every subtotal, total, percentage, and FX example recomputes exactly.
- Currency of obligation is unambiguous.
- Incoterm includes an exact named place and edition.
- Manufacturing lead time has explicit start conditions.
- Transit estimate is not misrepresented as guaranteed delivery.
- Import duties, VAT, broker charges, unloading, and conformity documents are allocated.
- No fictitious legal entity is presented as real.
- The PDF has the intended page count; no clipping, overflow, missing footer, or unreadable source URL.
- The user is warned which placeholders and regulatory fields must be completed before sending.

## Pitfalls

- **Ambiguous “price in RUB at the current rate.”** This leaves the conversion date and rate source undefined. Use an exact formula.
- **DAP described as duty paid.** Under DAP, import clearance and import charges normally remain with the buyer unless the contract reallocates them.
- **Lead time without prerequisites.** “35 days” is misleading if specification approval or advance is outstanding.
- **Fake completeness.** A polished PDF with invented party data, manufacturer, HS code, or certification status is more dangerous than an explicit project draft.
- **Visual-only verification.** A screenshot of HTML is not proof of final PDF page count. Verify both structure and layout.
- **A4 overflow.** Fixed A4 containers can still spill because content height, padding, and print rounding exceed one page. Treat extra pages or missing footers as a blocker.

## Supporting Reference

See `references/russian-ved-commercial-offer-checklist.md` for a concise Russia-focused checklist, example FX formula, and production-timing pattern. Treat it as a drafting aid, not legal advice.
