# Yandex Maps place verification

Use for current local-business recommendations when OpenStreetMap lacks ratings, review volume, hours, price range, cuisine, or review themes.

## Workflow

1. Fetch a targeted Yandex Maps search page with a normal desktop user agent and Russian `Accept-Language` header.
2. Confirm the exact business from the title, canonical link, `shortTitle`, and `fullAddress`. Search pages contain unrelated advertised businesses with their own ratings.
3. Extract the intended business fields from embedded SSR JSON: `ratingData.ratingValue`, `ratingCount`, `reviewCount`, `workingTimeText`, feature `average_bill2`, cuisine and institution features, phones, URLs, and address.
4. Prefer the canonical URL `https://yandex.ru/maps/org/<slug>/<business_id>/` in the answer.
5. Fetch `/maps/org/<slug>/<business_id>/reviews/` for review analysis. The rendered page can embed review objects with `reviewId`, author, text, rating, and timestamp. Deduplicate by review ID, count the visible rating distribution, inspect recent reviews, and read low-rated reviews for recurring failure modes.
6. A direct reviews API request may return only a CSRF token; the rendered reviews page is the reliable read-only fallback.
7. Compare score and sample size together. Separate “best overall” from “best for a business dinner”, “best cuisine”, and “best atmosphere”.
8. If new verification changes a prior recommendation, correct the ranking explicitly.

## Grounding

- Keep first-party history, awards, and positioning separate from independent map reviews.
- Do not treat one positive excerpt as consensus; summarize repeated themes and disclose meaningful recent complaints.
- Ratings and prices are dynamic; identify the platform and retrieval date when material.
- Judge the user’s use case, not only the directory category label (`restaurant`, `cafe`, `banquet hall`).
