---
name: candidate-sourcing-and-shortlisting
description: Use when sourcing and ranking candidates for a vacancy.
version: 1.0.0
metadata:
  hermes:
    tags: [recruiting, sourcing, candidates, resumes, hr]
    category: productivity
---

# Candidate sourcing and shortlisting

Source real candidates from lawful public or authorized recruiting sources, verify each profile against a vacancy, and produce an evidence-based shortlist. Use this for active search, passive-candidate discovery, multi-resume comparisons, and outreach preparation.

See `references/sourcing-packet.md` for the standard evidence schema, scoring model, and outreach checklist.

## Workflow

1. **Extract the vacancy.** Read the supplied document rather than asking the user to paste it. Separate:
   - mandatory professional requirements;
   - trainable/product-specific preferences;
   - working conditions such as city, office/remote format, schedule, and compensation;
   - non-job-related or discriminatory criteria, which must not affect ranking.
2. **Resolve only material gaps.** For office roles, city is mandatory. Ask for it if absent. Default to a first batch of 5–10 profiles unless the user specifies a count.
3. **Build a search profile.** Include role synonyms, seniority, core systems, donor companies, geography, and negative filters. Do not require every niche product when equivalent experience is likely transferable.
4. **Route sources intelligently.** Use ordinary web search for indexed public profiles and the social-research routing skill when platform-native profiles are central. Use authorized employer access for closed resume databases; never bypass login, CAPTCHA, paywalls, or privacy controls.
5. **Collect candidates as evidence packets.** Save batches to a durable JSON/CSV/Markdown file. For every candidate record the canonical URL, source, location evidence, current/last role, confirmed matches, missing/unconfirmed items, availability signal, and page state.
6. **Verify profiles.** Open the profile whenever possible. Search snippets are discovery evidence, not sufficient proof when a page is readable. Deduplicate by name, URL, employer history, and role chronology.
7. **Score conservatively.** Award points only for explicit evidence. Do not equate `1С` with `1С:Бухгалтерия`, `Битрикс` with `Битрикс24`, or platform exposure with hands-on administration. Keep job-fit score separate from contact priority and availability.
8. **Synthesize the shortlist.** Lead with the strongest actionable candidates. For each, state why they fit, what is unconfirmed, practical contact risks, and the first-screen questions. Separate active candidates, passive prospects, overqualified profiles, and reserves.
9. **Report constraints honestly.** State which platforms required authorization, which pages were blocked, and whether salary/office readiness is unknown. A public profile does not prove willingness to move.
10. **Prepare outreach only when requested.** Personalize from verified professional facts. Do not expose hidden contacts or sensitive personal data.

## Quality and legal safeguards

- Evaluate only business qualities connected to the role. Do not rank by age, sex, family status, nationality, appearance, health, or other protected/non-professional characteristics.
- Avoid collecting or reproducing personal phone numbers, private emails, dates of birth, or unrelated social content.
- Use neutral labels such as “not confirmed in the public profile,” not “does not know,” unless the source explicitly proves absence.
- Treat delegated/social-research output as unverified until the canonical pages or saved source captures are checked.
- Declared counts are hard assertions: deduplicate programmatically and verify the final count.

## Scoring guidance

Create a 100-point rubric from the vacancy before reviewing profiles. Weight mandatory capabilities most heavily, location/format modestly, and niche “nice-to-have” tools lightly. Never inflate a score because a candidate is senior. Explain that the score measures documented vacancy fit, not overall professional quality.

Also report:
- **availability:** active / passive / unknown;
- **contact priority:** high / medium / reserve;
- **confidence:** high / medium / low;
- **role-shape risk:** hands-on gap, overqualification, compensation risk, or narrow specialization.

## Pitfalls

- A vacancy may combine several jobs (for example CIO + system administrator + application administrator). Flag this and recommend a realistic must-have/learnable split.
- Product names can create an unrealistically narrow funnel. Search equivalents and adjacent experience, then list exact-product gaps for screening.
- Public social profiles often omit salary and office preference; never infer either.
- A polished profile can still be stale. Capture page date, last activity, or explicit job-seeking status when visible.
- Do not pass raw search results to the user. Remove vacancies, agencies, companies, duplicates, non-local profiles, and profiles without enough evidence.

## Verification checklist

- Every retained candidate is a real individual with a canonical public/authorized profile.
- Location evidence is explicit for office roles.
- Core claims are traceable to the source.
- Active/passive status is not guessed.
- No protected characteristics affected scoring.
- Shortlist order reflects both fit and practical contactability.
- Limitations and missing requirements are visible.
