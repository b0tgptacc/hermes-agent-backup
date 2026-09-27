---
name: evidence-based-local-venue-selection
description: "Use when ranking local venues with current review evidence."
version: 1.0.0
metadata:
  hermes:
    tags: [local, restaurants, venues, reviews, recommendations, maps]
    category: research
---

# Evidence-Based Local Venue Selection

Use this skill when the user asks for the **best** restaurant, café, hotel, bar, or similar local venue. This is a ranking task, not merely a nearby-POI lookup.

## Objective

Recommend one venue for the user’s actual purpose, supported by current ratings, meaningful review volume, recent review evidence, and verified operational details.

## Workflow

1. **Define the practical interpretation.** If the user gives no criteria, evaluate “best overall.” Avoid clarification unless cuisine, budget, accessibility, or occasion materially changes the answer.
2. **Build the candidate set.** Use the `maps` skill or current map/search sources to identify plausible venues and verify names, addresses, and categories.
3. **Cross-check current reputation.** Use at least two current review platforms when available. Capture rating, rating count, review count, and venue category.
4. **Weight sample size.** A 5.0 backed by hundreds of reviews is stronger evidence than a 5.0 backed by a few dozen. Never compare raw scores without their sample sizes.
5. **Inspect recent reviews.** Read both positive and low-rated reviews. Look for repeated operational themes: service at peak hours, food consistency, noise, seating, parking, accessibility, and price/value.
6. **Verify practical details.** Confirm current address, hours, price range, booking contact, cuisine, and relevant amenities.
7. **Rank by purpose.** Distinguish “best overall” from “best for a business dinner,” “best cuisine,” “best family option,” or “best nightlife.” Venue format can outweigh a small numerical rating difference.
8. **Report decisively.** Lead with one recommendation, give concise reasons, then at most two purpose-specific alternatives.

## Evidence Rules

- Treat venue-supplied descriptions and awards as attributed claims, not independent proof.
- Treat platform-generated summaries as orientation, then inspect underlying reviews when the decision matters.
- Do not infer stable service quality from one complaint or one compliment.
- Ratings, hours, menus, and prices are current-state facts; retrieve them live each time.
- Cite current source pages when the user may want to verify the recommendation.

## Corrections

If a later candidate proves better for the user’s purpose, explicitly correct the earlier ranking. Do not defend an inferior initial answer merely for consistency.

## Supporting Reference

See `references/map-platform-evidence.md` for a no-key extraction method and review-analysis checklist.

## Verification Checklist

Before finalizing:

- [ ] Candidate is open/current and in the requested city.
- [ ] Rating and sample size were checked live.
- [ ] At least one independent review source was inspected.
- [ ] Recent negative reviews were considered.
- [ ] Address, hours, price level, and booking details are current.
- [ ] Recommendation matches the occasion, not just the highest score.
