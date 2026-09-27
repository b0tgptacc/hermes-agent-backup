# Map-Platform Evidence Without an API Key

## Yandex Maps public HTML

A public organization page commonly embeds structured current business data in its HTML. Useful fields include:

- `ratingData.ratingValue`, `ratingCount`, `reviewCount`
- `fullAddress`, `workingTimeText`, status
- `features` entries such as `average_bill2`, cuisine, venue type, parking, terrace, accessibility, and delivery
- canonical organization URL `/maps/org/<slug>/<id>/`

The corresponding `/reviews/` page may embed review objects containing `reviewId`, `text`, `rating`, and `updatedTime`.

### Review analysis

1. Extract a bounded sample, preferably recent reviews.
2. Deduplicate by `reviewId`.
3. Count ratings by star value.
4. Read all low-rated reviews in the sample.
5. Separate repeated complaints from isolated incidents.
6. Quote or paraphrase fairly; do not convert one person’s experience into a universal claim.

## 2GIS public HTML

Search pages may embed organization objects with:

- `name_ex.primary`
- `reviews.general_rating`
- `general_review_count`
- `general_review_count_with_stars`
- category, coordinates, and address data

Use targeted searches for finalists, but keep a broad city/category search to avoid prematurely excluding strong candidates.

## Cross-platform comparison

Do not average platform scores mechanically. Compare:

- score;
- number of ratings;
- number and recency of written reviews;
- category/format fit;
- recurring positive and negative themes.

A practical ranking can favor a slightly lower score when it has a much larger, more recent sample or better matches the occasion.

## Source caveats

- Platform HTML structures can change; inspect fresh output rather than hard-coding a refusal.
- Venue descriptions, menus, and awards may originate from the venue owner.
- Current hours and prices require live verification on the day of recommendation.
