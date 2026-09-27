# Candidate sourcing packet

Use this structure for every retained candidate. Keep facts traceable to the canonical profile and mark unknowns explicitly.

## Evidence record

```yaml
name: ""
canonical_url: ""
source: ""
retrieved_at: ""
page_state: public | authorized | snippet-only | blocked
location_evidence: ""
current_or_last_role: ""
availability: active | passive | unknown
confirmed_matches: []
missing_or_unconfirmed: []
strong_pluses: []
job_fit_score: 0
contact_priority: high | medium | reserve
confidence: high | medium | low
role_shape_risks: []
notes: ""
```

## Scoring model

Build weights from the vacancy; total must equal 100.

- Core professional must-haves: 55–70 points.
- Relevant scope/seniority and leadership: 10–20 points.
- Location and required work format: 5–10 points.
- Documentation, process, budget, or domain context: 5–15 points.
- Niche product preferences: no more than 5–10 points unless the user confirms they are genuinely non-trainable.

Score only explicit evidence. Use `0` for unknown, not a negative inference. Keep availability and contact priority outside the numerical fit score.

## Search packet prompt

Include:

1. role and synonyms;
2. city and work format;
3. mandatory evidence requirements;
4. trainable or adjacent skills;
5. target platforms and donor companies;
6. maximum number of candidates;
7. public/authorized access only;
8. required evidence record fields;
9. deduplication rule;
10. minimum verified-profile acceptance criterion.

## First-screen checklist

- Confirm current location and office/hybrid readiness.
- Confirm compensation range before a long interview when the role has a hard ceiling.
- Ask for one recent hands-on example per mandatory system.
- Distinguish personal execution from team/vendor oversight.
- Verify scale: users, servers, sites, budget, team, and uptime/SLA.
- Ask how results were measured and what failed.
- Confirm job-search status and notice period.

## Shortlist output

Lead with a compact table: priority, candidate, documented fit, availability, and recommendation. Then give per-candidate evidence, gaps, risks, and screening questions. End with source/access limitations and, when needed, a recommendation to simplify an over-combined vacancy.
