# Marketplace Retrieval Patterns

Use these patterns when a shopping page is dynamic, localized, or blocks normal extraction. They are recovery options, not reasons to skip live verification.

## Recovery Order

1. Open the exact product or search page in the managed browser.
2. Fetch the public page directly with a normal browser user agent.
3. Use a text-rendering proxy such as `https://r.jina.ai/http://<url>` for publicly accessible content.
4. Check the marketplace search-results page, which may expose title, item ID, price, visible sales, and rating even when the product page is sparse.
5. Use the manufacturer's sitemap to discover canonical product URLs when search engines miss them.
6. Search the exact item ID/SKU on other indexes only as a locator; verify facts on the original source.

## Extracting Search Result Cards

Marketplace result cards often contain several offers in long markdown lines. Parse mechanically rather than copying by eye:

- heading/title;
- displayed price and old price;
- sold count and visible rating;
- item URL and stable item ID;
- variant clues embedded in the title;
- search locale/currency.

Store the clean canonical item URL without volatile tracking parameters, but preserve the retrieved source page for evidence.

## Manufacturer Discovery via Sitemap

When a product family is known but the model is not:

1. Fetch `/robots.txt`.
2. Locate `/sitemap.xml` or sitemap indexes.
3. Search product sitemap URLs for distinctive tokens: sensor ID, fps, shutter type, interface, or codec.
4. Fetch the canonical product page and extract the mode table, SKU, public price, and variant names.

This is especially effective for catalog sites whose internal search is weak.

## Dynamic Price Rules

- Timestamp every observation.
- Record source currency and locale.
- Preserve price ranges and MOQ; do not replace them with only a midpoint.
- Mark shipping, tax, duty, coupon, and new-user discounts separately.
- If a page displays `$0.00` but offers inquiry/contact, record `quote required`, not zero price.
- If price is missing, keep it missing; do not infer it from similar items.

## Seller Identity Rules

If the public search view does not expose the store name, write `seller not exposed in retrieved view` and retain the platform plus item ID. Do not substitute a brand in the title for the merchant identity.

## Evidence Quality

A search result supports only what it visibly contains. Use it for current displayed price, title claims, item ID, and visible sales/rating. Use the exact product page or manufacturer documentation for technical specifications and terms.

## Verification

- Re-fetch at least the recommended offer before finalizing.
- Confirm title, price, and item ID stay paired.
- Check that canonical URLs open or are at least present in the retrieved source.
- Record any page that could not expose seller, stock, shipping, or exact variant as an uncertainty, not a fact.