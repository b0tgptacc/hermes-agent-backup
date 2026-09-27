---
name: travel-destination-research
description: "Use for researching sights and remote travel destinations."
version: 1.0.0
metadata:
  hermes:
    tags: [travel, destinations, attractions, routes, maps, safety, seasonality]
    related_skills: [maps, grounded-citations, local-place-recommendations, blocked-page-recovery]
---

# Travel Destination Research

Research what a traveler should see and whether a specific destination is worth visiting, using current operational evidence rather than generic listicles. This skill covers regions, attractions, seasonal itineraries, and obscure natural features such as bays, volcanoes, trails, islands, and reserves.

## Decision model

Evaluate each candidate on:

1. **Traveler value** — scenery, uniqueness, wildlife, culture, or activity.
2. **Seasonal fit** — weather, snow, tides, wildlife timing, daylight, road and trail conditions.
3. **Access** — road, boat, helicopter, trail, permits, guide requirements, and realistic time cost.
4. **Current operability** — open/closed status, construction, volcanic or wildfire restrictions, transport availability.
5. **Risk and resilience** — evacuation difficulty, communications, wildlife, weather dependence, and need for reserve days.
6. **Fit for this trip** — first visit versus specialist expedition, trip length, fitness, and budget.

Rank; do not dump an unstructured bucket list. Separate essential first-trip sights from specialist or expedition-only options.

## Workflow

### 1. Resolve the exact place

Names of bays, rivers, mountains, and villages are frequently duplicated. Before describing an obscure feature:

- geocode the full name plus region with the `maps` skill;
- preserve the returned coordinates and feature type;
- cross-check against a topographic map or a second gazetteer;
- state the assumed feature explicitly when ambiguity remains;
- provide a map link so the user can confirm the target.

Never merge facts from identically named places.

### 2. Build the current operational picture

Prefer sources in this order:

1. park, reserve, tourism ministry, emergency-service, port, or municipal authority;
2. official route registry, permit page, or operator register;
3. current maps and topographic sources;
4. established operators for logistics and commercial availability;
5. traveler reports for qualitative experience only.

A nominal season (for example, “June–October”) does not override a live `closed` status. Quote the checked status and date it in the answer when material. Tell the traveler to recheck near departure when conditions are volatile.

### 3. Distinguish evidence from inference

Use calibrated language:

- **Verified:** exact coordinates, named neighboring features, official route status, permit rule.
- **Supported inference:** likely remote because maps show no settlement or mapped road and no official route was found.
- **Unknown:** landing conditions, current trail quality, operator availability, wildlife sightings.

Absence from one catalog is not proof that a place is inaccessible. Say “no official listed route was found,” not “there is no route.” Old topographic maps establish geography, not current infrastructure.

### 4. Handle blocked search without looping

If a general search backend is rate-limited or returns a bot challenge:

- stop repeating the same search;
- fetch known authoritative domains directly with `curl` or Python stdlib;
- inspect homepage links, route indexes, sitemaps, and site search endpoints;
- strip HTML with a small standard-library `HTMLParser` when no extractor is available;
- pivot to Nominatim/OSM APIs and public map objects for identity and location;
- use `blocked-page-recovery` only when the target page itself is blocked.

Validate body content; a search interstitial is not evidence.

### 5. Make the recommendation operational

For a regional “what to see” question, provide:

- a short ranked set of strongest sights;
- a sample itinerary sized to a reasonable default trip;
- reserve-day logic for weather-dependent transport;
- season-specific packing and safety points;
- explicit warnings for currently closed or expedition-grade options.

For one obscure destination, lead with a plain verdict: mainstream day trip, worthwhile specialist detour, or expedition-only. Then explain location, access, attraction, evidence gaps, and safer alternatives.

## Citations

Use `grounded-citations` for current claims and source each operational status inline. Direct map coordinates and calculated straight-line distances may share the map source, but identify calculated values as “по прямой.” Do not cite a search-result snippet when the underlying page can be fetched.

## Pitfalls

- Recommending a famous route from memory despite a live closure.
- Treating a tour operator’s sales page as proof of legal access.
- Calling a mapped feature developed because a photo or video exists.
- Treating no OSM road, POI, or campsite as proof none exists on the ground.
- Presenting wildlife sightings as guaranteed.
- Scheduling helicopters or sea excursions on the final day with no weather buffer.
- Giving precise travel times for unmapped or seasonal roads.
- Failing to say which same-named feature was researched.

## Verification checklist

- Exact feature and region resolved.
- Coordinates or map link supplied for obscure places.
- Official status checked where applicable.
- Seasonal conditions reflected in the recommendation.
- Access mode and uncertainty stated honestly.
- First-visit and expedition-grade options separated.
- Safety advice is specific to the terrain and sourced when consequential.
- Every current external claim is cited.

## References

- `references/remote-natural-feature-verification.md` — compact evidence pattern for obscure bays, trails, peaks, and similar destinations.
