---
name: talent-sourcing-research
description: Use when sourcing job candidates across public platforms.
version: 1.0.0
author: MASTER
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [recruiting, sourcing, candidates, resumes, research]
    category: research
---

# Talent sourcing research

Find and verify potential job candidates across public resume boards, professional networks, career profiles, and specialist communities. Produce an actionable shortlist grounded in visible professional evidence.

## When to use

Use when the user asks to:

- find candidates for a vacancy;
- source passive or active talent across multiple platforms;
- search resume boards and return individual profile links;
- compare public profiles with a job specification;
- treat experience with AI or another technology as a hiring advantage.

Do not use this skill merely to analyze resumes the user already supplied; use the relevant document-reading workflow for that.

## Core workflow

1. **Parse the vacancy.** Separate mandatory requirements, strong advantages, and interview-only verification points.
2. **Resolve material ambiguity.** For office roles, determine the city before searching. Confirm other facts only when they materially change the search.
3. **Plan evidence classes.** Use ordinary web research for indexed profiles and route platform-native or authenticated social research through the appropriate profile/tool.
4. **Search broadly, retain narrowly.** Search multiple source classes, but retain only individual profiles with stable URLs and job-relevant evidence.
5. **Open and verify.** Read each retained profile where access permits. Do not convert a search snippet or job title into a confirmed skill.
6. **Deduplicate.** Compare name, URL, career history, employer, and location.
7. **Score transparently.** Rank mandatory role fit before optional advantages. State the rubric and missing evidence.
8. **Deliver an actionable shortlist.** Include links, confirmed matches, gaps, availability/work-format conflicts, and contact priority.
9. **State access limits.** If a board hides profiles behind an employer login, distinguish verified profiles from leads that the user must open.

See `references/candidate-sourcing.md` for evidence rules, resume-board constraints, AI evaluation, and the delivery checklist.

## Output standard

For each candidate provide:

- name or public profile title;
- individual profile URL and source;
- location and work-format evidence;
- current or most recent role;
- confirmed mandatory matches;
- optional advantages;
- missing or unconfirmed requirements;
- public availability and compensation conflicts, if shown;
- confidence and recommended contact priority.

Separate candidates into:

1. primary matches;
2. conditional or passive leads;
3. adjacent specialists or bonus-only profiles.

Do not hide a core mismatch inside a high percentage. A candidate with AI experience but no required infrastructure, finance, clinical, or operational background belongs in an adjacent section, not at the top of the main shortlist.

## Safety and fairness

- Evaluate only job-related professional evidence.
- Never rank by age, sex, family status, ethnicity, appearance, or other protected/non-job-related traits.
- Minimize personal data. Link to the profile instead of reproducing phone numbers, emails, birth dates, or home-area details.
- Do not bypass login walls, CAPTCHAs, paywalls, or platform restrictions.
- Never ask for or type the user's password. The user may authenticate in their own browser or provide an export.
- Treat public availability labels exactly as written; a public profile does not imply willingness to change jobs.

## Verification

Before finalizing:

- every listed URL resolves to the intended individual profile;
- every claimed match is supported by visible profile text;
- title-only or snippet-only results are marked as unverified leads;
- location, office readiness, salary, and availability are not inferred;
- declared totals equal the actual number of listed candidates;
- optional advantages did not override missing mandatory criteria.
