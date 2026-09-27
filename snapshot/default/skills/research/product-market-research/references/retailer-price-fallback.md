# Retailer Price Fallback

Use this only after the linked retailer remains inaccessible and the user still benefits from a current market-price reference. It does not recover or prove the blocked retailer's own price.

## Validated workflow

1. Preserve the original retailer URL as the purchase/reference link.
2. Query an accessible marketplace or price aggregator for the exact model, color, layout, region, and part number.
3. Prefer structured data embedded in the results page, such as JSON-LD `ItemList` entries containing `Product`, `Offer`, `price`, `priceCurrency`, `availability`, URL, and SKU.
4. Enumerate several candidates before selecting one. Match in this order: exact part number/SKU; exact model plus variant; closest documented substitute.
5. Record retrieval timestamp, region, availability, selected source URL, and a match-status field.
6. Label the value explicitly as `market price`, `market reference`, or the source marketplace's price. Never call it the blocked retailer's price.
7. If the original URL omits a decisive variant (switch type, layout, connector generation, color code), mark `requires variant confirmation` and explain which candidate was used.
8. In spreadsheets, keep separate clickable links for the original retailer and the price source, plus a methodology/limitations note.

## Verification

- Programmatically recount products, prices, images, and hyperlinks.
- Confirm every price maps to the chosen candidate URL and exact part number where available.
- Validate the XLSX archive, then render it through a spreadsheet engine and inspect every page.
- For wide sheets, set fit-to-width and inspect page breaks; remove overlapping chart data labels rather than accepting an unreadable chart.

## Pitfalls

- Do not silently replace a retailer price with an aggregator price.
- Do not choose the cheapest search result when its SKU or variant differs.
- Do not infer missing part numbers from a product photo alone.
- Do not present a dynamic marketplace price without timestamp and region.
