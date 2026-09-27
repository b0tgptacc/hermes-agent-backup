# Public map-page extraction

Use this note when a Russian local-place task needs rating evidence beyond OpenStreetMap.

## Yandex Maps

A public search/place page can include server-rendered structured state for the selected venue. Useful fields observed in that state include:

- `shortTitle` and `fullAddress`;
- `status`;
- `ratingData.ratingValue`;
- `ratingData.ratingCount`;
- `ratingData.reviewCount`;
- `workingTimeText`;
- feature entries such as `average_bill2` and `price_category`;
- categories and public phone numbers.

Verify that the structured object’s title/address matches the intended branch. Search pages may also embed advertisements and nearby businesses with their own ratings; do not take the first `rating` field in the HTML. Anchor extraction on the selected venue’s `shortTitle`, `fullAddress`, or `ratingData` block.

## 2GIS

Public search pages may include structured organization objects with:

- `name_ex.primary`;
- `org.id` and branch count;
- `point` coordinates;
- `reviews.general_rating`;
- `reviews.general_review_count`;
- `reviews.general_review_count_with_stars`;
- category/rubric names.

2GIS may expose both `general_*` and `org_*` review aggregates plus Flamp-specific values. Report the platform’s general rating and label written-review count separately from star-rating count. Do not mix Flamp-only counts into the general sample.

## Cross-platform comparison

- Match exact branch by name, address, and coordinates.
- Record a timestamp or say “at the time of checking”; counts change.
- Compare rating direction and evidence volume, not a hand-made average.
- A public HTML field is evidence for what the platform displayed, not independent proof that every review is genuine.
- If the page requires CAPTCHA, authentication, or payment, stop and use another public source; do not bypass the control.
