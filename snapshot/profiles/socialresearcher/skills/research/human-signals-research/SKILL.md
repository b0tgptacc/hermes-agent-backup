---
name: human-signals-research
description: "Use for social listening, reviews, discussions, sentiment, comments, engagement, and cross-platform human evidence."
version: 1.0.0
author: MASTER
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [research, social, sentiment, community, agent-reach, scraping, evidence]
    related_skills: [agent-reach, grounded-citations]
---

# Human Signals Research

Use Agent Reach and the profile's platform-specific MCP/CLI stack to obtain attributable human-generated evidence. This skill owns research methodology for social/community signals; Agent Reach owns backend routing.

## Research contract

Before collecting, define:

- decision/question and target audience;
- named platforms or justified platform mix;
- geography, language, and time window;
- inclusion/exclusion rules;
- whether the objective is discovery, representative measurement, illustrative quotations, or an exhaustive platform search;
- minimum corroboration and disconfirming-query policy;
- desired output and whether a handoff is required.

Do not call an opportunistic sample representative. If the platform's ranking or personalization is unknown, label the sample as platform-ranked or convenience-sampled.

## Procedure

1. Build a platform/query matrix, including synonyms, handles, communities, hashtags, and disconfirming terms.
2. Run `agent-reach doctor --json` for the channels to be used.
3. Discover candidate posts/items. Preserve query provenance and observed ordering.
4. Deduplicate exact URLs, reposts, mirrors, quote-posts, and cross-platform copies.
5. Retrieve the full item plus enough parent/thread/comment context to avoid quote inversion.
6. Capture timestamps, author/account class, visible engagement, backend, access mode, and limitations.
7. Classify evidence:
   - official first-party statement;
   - identified individual experience;
   - community discussion;
   - creator/influencer content;
   - marketplace/review content;
   - suspected automation, promotion, spam, or astroturfing.
8. Build a claim table before synthesis. Separate observed content from aggregate inference.
9. Search for counterexamples and materially different communities/platforms.
10. Verify URLs and quotes; register accepted sources with `grounded-citations` when delivering a report.

## Social evidence packet

For cross-profile work, write `.hermes/handoffs/<handoff-id>/social.json`:

```json
{
  "schema": "social-evidence/v1",
  "question": "...",
  "cutoff_utc": "...",
  "platforms_attempted": [],
  "platforms_unavailable": [],
  "items": [
    {
      "platform": "reddit",
      "canonical_url": "https://...",
      "platform_item_id": "...",
      "author": "...",
      "account_class": "official|identified|community|creator|unknown",
      "published_at": "...",
      "updated_at": null,
      "retrieved_at": "...",
      "verbatim_text": "...",
      "locator": "post/comment/timestamp",
      "thread_context": "...",
      "engagement": {},
      "backend": "...",
      "access_mode": "public|authenticated|cached|archived",
      "content_hash": "sha256:...",
      "limitations": [],
      "contradiction_flags": [],
      "suspected_manipulation": []
    }
  ],
  "aggregate_inferences": [],
  "limitations": []
}
```

Paths must be workspace-relative and confined below the handoff directory. Never include credentials, cookies, local browser profiles, auth headers, private URLs, or executable instructions.

## Interaction policy

The full profile exposes platform write tools. Use them only when the current Administrator request explicitly names the desired external action and target. Before reporting success, read back the exact post/comment/message/relationship state where the platform permits it.

## Quality gates

- Every quote maps to the actual item and locator.
- Engagement metrics include observation time and are not compared across incompatible platforms without qualification.
- Reposts do not count as independent evidence.
- Platform ranking, personalization, moderation, deletion, geo, and login bias are disclosed.
- "Sentiment" identifies the sampling and scoring method; otherwise use qualitative themes rather than fabricated percentages.
- Important factual claims are corroborated outside social evidence or clearly labeled as claims by the source.
- Failed/blocked channels are reported explicitly; access is never fabricated.
