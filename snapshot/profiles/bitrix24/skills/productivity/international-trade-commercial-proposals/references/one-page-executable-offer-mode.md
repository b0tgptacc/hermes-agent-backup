# One-page executable commercial proposal mode

Use this mode when the parties intend to begin cooperation directly on the basis of the commercial proposal rather than signing a separate contract first.

## Recommended output set

Produce 2–3 genuinely different one-page options when the user asks for variants:

1. **Strict offer:** strongest acceptance mechanics and essential terms; recommended when the signed proposal and advance are intended to bind the parties.
2. **Partnership proposal:** same commercial essentials, but framed around repeat orders, capacity reservation, and the relationship.
3. **Procurement format:** dense specification, total price, payment/delivery terms, and signatures for purchasing/accounting review.

Each option must remain independently usable; do not make one PDF depend on text located in another option.

## One-page content priority

Keep, in this order:

1. supplier and buyer legal placeholders/requisites;
2. offer number, issue date, and validity date;
3. goods, quantity, unit price, line totals, freight/packaging, and grand total;
4. currency of obligation and an exact conversion rule;
5. Incoterm, edition, and exact named place;
6. payment stages;
7. manufacturing start conditions and delivery range;
8. included/excluded customs, VAT, certification, and unloading costs;
9. warranty/claim window;
10. offer status, acceptance mechanism, signatures, and compliance condition.

Move explanatory prose, long force-majeure language, and detailed source commentary out before shrinking critical commercial text below readable size.

## Offer and acceptance language

Do not silently call an incomplete template a binding offer. Use a conditional formulation such as:

> После заполнения всех реквизитов и подписания Поставщиком настоящее коммерческое предложение является офертой. Полным и безоговорочным акцептом является подписание Покупателем и/или поступление предусмотренного аванса.

State what the acceptance confirms: specification, quantity, price, delivery basis, timeline, and payment terms. If legal review or the jurisdiction requires a separate contract, say so instead of overstating enforceability.

## Layout and verification

- Use one A4 page per option, not a multi-page PDF containing all options unless the user asks for a comparison pack.
- Keep signatures, source line, validity, and footer visible; a missing footer is an overflow signal.
- Render each option to an image and inspect it.
- Parse the final PDF and verify exactly one `/Page` object and a declared page count of one.
- If Chromium prints two pages, compact vertical spacing and local typography rather than hiding overflow with a fixed-height container.
- Prefer readable whitespace over filling the entire page; unused lower space is acceptable if all critical terms are legible.

## Pre-send warning

Tell the user to replace party details, bank data, manufacturer/SKU, HS/TN VED code, conformity requirements, and exact delivery address. Recommend legal review before relying on the document as the sole contractual basis.