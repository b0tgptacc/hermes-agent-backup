---
name: local-place-recommendations
description: "Use when ranking restaurants, hotels, or local venues."
version: 1.0.0
metadata:
  hermes:
    tags: [research, local, restaurants, hotels, ratings, maps, recommendations]
    related_skills: [maps, grounded-citations, blocked-page-recovery]
---

# Local Place Recommendations

Recommend the strongest local restaurant, hotel, cafe, venue, or service using current, cross-platform evidence rather than a single directory rank. Use for “best restaurant in…”, “where should I stay?”, “top venue for a business dinner”, and similar local-choice questions.

## Decision model

Treat “best” as a decision under uncertainty, not the maximum displayed star value. Evaluate:

1. **Fit for purpose** — cuisine/service, business dinner, family meal, nightlife, budget, location.
2. **Rating strength** — rating level plus rating/review volume.
3. **Cross-platform agreement** — compare at least two independent map/review sources when practical.
4. **Current viability** — open status, recent activity, hours, functioning contacts.
5. **Operational fit** — price, reservation, parking, noise, accessibility, distance.

If the user gives no use case, choose the best general-purpose option and name one clear winner. Add one alternative only when it serves a materially different purpose.

## Workflow

### 1. Discover candidates broadly

- Geocode the city or location with the `maps` skill.
- Query nearby POIs by the relevant category to avoid relying on search-engine popularity alone.
- Supplement OpenStreetMap candidates with local map directories because OSM usually lacks ratings and review volume.
- Resolve duplicate spellings and branches by exact address and coordinates.

### 2. Collect comparable evidence

For each serious candidate, capture:

- exact name and category;
- current status and address;
- rating value;
- number of ratings and number of written reviews;
- opening hours;
- price/average check when available;
- cuisine or service type;
- reservation/contact link.

Prefer current Yandex Maps and 2GIS data for Russian cities. Their public place/search pages may contain server-rendered structured state. Extract only public, unauthenticated fields; do not bypass CAPTCHAs, login, or paid boundaries.

### 3. Weight rating confidence

Do not rank a 5.0 score from 20 ratings above a 4.9 score from 1,000 ratings without explanation. Use rating volume as confidence, not as proof of quality.

A practical qualitative hierarchy:

- **Strong:** high rating with hundreds of written reviews and broad cross-platform agreement.
- **Moderate:** high rating with dozens to low hundreds of reviews.
- **Weak:** perfect rating with a very small sample, stale activity, or only one platform.

Do not average platform ratings blindly: platforms use different scales, moderation, and aggregation. Compare direction and strength instead.

### 4. Read the use case

Separate categories that users often conflate:

- best food vs best atmosphere;
- restaurant vs karaoke/banquet hall;
- fine dining vs casual cafe;
- central location vs destination venue;
- business dinner vs family gathering;
- overall reputation vs novelty.

A venue can lead the citywide rating yet be wrong for a quiet business meal. State the winner for the requested use case.

### 5. Deliver the answer

Lead with one sentence:

> Best overall: **Name** — why in one clause.

Then give 3–5 decision-critical facts: cross-platform ratings with sample sizes, cuisine/category, address, hours, price, and map link. State the rating snapshot as current at research time. Avoid a long unranked list.

## Evidence and citations

- Cite each platform next to the metric it supports.
- Distinguish `ratings` from written `reviews`; never swap the labels.
- Prefer a stable place/search URL rather than an ephemeral API or state URL.
- If hours or prices conflict, identify the platform and recommend confirming by phone.
- Use the `grounded-citations` workflow for externally sourced claims.

## Pitfalls

- **Raw-star ranking:** ignoring sample size.
- **Category mismatch:** naming a nightclub, karaoke club, or banquet hall as the best restaurant without qualification.
- **Platform monoculture:** trusting one directory when another major source disagrees.
- **Popularity substitution:** treating chain familiarity as quality.
- **Stale status:** recommending a closed or moved venue.
- **False precision:** inventing a universal score from incompatible platforms.
- **List dumping:** presenting ten options when the user asked for the best one.
- **Unverified operational details:** quoting hours or average check without platform attribution.

## Verification checklist

- Exact venue and branch match across sources.
- At least two current sources were checked when practical.
- Rating and sample size are paired correctly.
- Venue category matches the requested experience.
- Address, hours, and map link are current.
- One winner is clearly identified, with limitations disclosed.

## References

- `references/public-map-page-extraction.md` — public structured fields commonly exposed by Yandex Maps and 2GIS pages.
