# Social and regional acquisition profile pattern

Use this reference when a broad capability-router skill aggregates social networks, communities, video platforms, regional sites, browser sessions, and platform-specific CLIs. The objective is to isolate unstable/credentialed acquisition from a production evidence-first researcher without mistaking a Hermes profile for a security sandbox.

## Decision rule

Create a separate specialist profile when the candidate:

- has broad `MUST USE` triggers that would compete with an established research orchestrator;
- depends on fast-changing platform CLIs, cookies, proxies, browser extensions, or site-specific MCP servers;
- adds genuinely unique social/regional coverage but duplicates ordinary search, fetch, RSS, video, or browser capabilities;
- needs an independent upgrade and rollback cadence.

The profile should be an **acquisition specialist**, not a second general-purpose researcher. Route official/current/academic/document research to the evidence-first researcher; route social sentiment, community discussions, reviews, engagement signals, and regional platforms to the acquisition specialist. For hybrid tasks, a parent orchestrator runs both and the evidence-first researcher owns final synthesis.

## Profile isolation versus sandboxing

Hermes profiles isolate Hermes state through `HERMES_HOME`: config, `.env`, skills, memory, sessions, logs, MCP, cron, and state databases. They do not restrict the local process from reading the rest of the host filesystem.

External CLIs normally retain the real OS-user `HOME`, so their cookies, browser state, GitHub auth, npm config, and tool credentials can remain shared across profiles. For a credentialed acquisition profile, set `terminal.home_mode: profile` so subprocesses receive `HOME={HERMES_HOME}/home`. Verify every external CLI actually honors `HOME`; do not infer isolation from Hermes profile creation alone.

`terminal.home_mode: profile` still does not isolate an existing Chrome profile. Require one of:

- an explicitly selected dedicated browser profile with low-privilege accounts;
- a separate OS user for stronger browser/credential isolation;
- a profile-scoped cookie/MCP backend with an explicit export;
- exclusion of the backend when the browser profile cannot be selected reliably.

Profiles are routing and state boundaries. Use a container, remote host, cloud sandbox, or separate OS account when a real filesystem/process boundary is required. Browser-session backends may not work inside containers; test the intended trust boundary rather than assuming portability.

## Minimal role and ownership

A good role description is:

> Collects read-only evidence from social networks, communities, reviews, public video platforms, and regional web sources. Returns attributable evidence with dates, engagement metadata, quotes, access method, and limitations. Does not replace official, academic, or evidence-grade research.

Ownership:

1. Parent/MASTER: task routing and integration decision.
2. Social acquisition specialist: platform selection, retrieval, source metadata, verbatim evidence, engagement signals, and access limitations.
3. Evidence-first researcher: claim table, authority weighting, cross-source corroboration, final citation IDs, synthesis, and verdict.

Do not let the two profiles recursively invoke each other. Use a parent or durable task graph.

## Skill composition

Keep the default set small:

- a curator-managed, pinned, read-only copy of the capability router;
- one narrow human-signals/social-acquisition orchestration skill;
- a local evidence-packet validator or grounded citation layer when the profile delivers reports directly.

Remove or disable from the router copy:

- generic research ownership and broad synthesis instructions;
- automatic install/update/watch behavior;
- `--system`, install-all, global package mutations, and mutable-main update guidance;
- posting, commenting, liking, messaging, uploads, and other remote writes;
- duplicate generic web search/fetch, RSS, YouTube, GitHub, citation, and browser routes when another profile already owns them;
- instructions to reuse a personal browser profile or pass cookies in prompts/CLI arguments.

Treat recency/signal-synthesis skills (for example engagement-ranked “last N days” workflows) as alternative explicitly invoked modes, not simultaneous default orchestrators. Benchmark them against the router-based workflow before selection.

## MCP and browser policy

Start with no platform MCP by default. Add one only for a measured capability gap.

Possible controlled additions:

- one search/fetch MCP with a two-tool allowlist, while disabling the router's duplicate provider route;
- a platform MCP exposing only read/search/detail tools;
- one allowlisted Apify Actor for a specific missing platform;
- crawl/map-only tooling for a site-wide task, with generic search/fetch excluded.

Exclude by default:

- omnibus MCP catalogs;
- a second Exa/search transport;
- a second equal-precedence browser owner;
- unrestricted actor stores;
- MCP sampling from untrusted external servers;
- write tools.

If a router uses OpenCLI or an authenticated browser session, that is the browser owner for its platform. Do not silently treat isolated Playwright, native browser, and personal-session OpenCLI as interchangeable fallbacks; each has a different trust boundary.

## Social evidence packet

Return machine-readable acquisition evidence, not a final conclusion:

```json
{
  "query": "...",
  "platform": "...",
  "canonical_url": "...",
  "author": "...",
  "account_type": "official|community|unknown",
  "published_at": "...",
  "retrieved_at": "...",
  "engagement": {"likes": null, "comments": null, "views": null},
  "quote": "...",
  "locator": "post/comment/timestamp",
  "backend": "...",
  "access_mode": "public|credentialed",
  "content_hash": "...",
  "limitations": [],
  "contradiction_flags": [],
  "automation_risk": "low|medium|high"
}
```

Social popularity is not independent corroboration. Detect reposts, coordinated campaigns, bots, deleted/edited posts, sampled comment coverage, missing engagement fields, and platform ranking bias. An official social post may be first-party evidence; community reactions remain community evidence.

## Rollout sequence

1. Create a blank profile rather than cloning a broad existing skill library.
2. Configure smart approvals, secret redaction, explicit terminal cwd, profile-scoped HOME, and depth-1 leaf delegation.
3. Pilot public zero-auth channels first; no cookies, proxy, cron, or browser extensions.
4. Pin the router and every backend version/commit; prohibit automatic updates.
5. Add credentialed channels only with dedicated accounts and explicit account/ToS review.
6. Add recurring monitoring only after acquisition value is proven; use durable checkpoints, canonical URLs, and content hashes.
7. Keep external writes disabled throughout unless a separate profile and authorization model are designed for publishing.

## Benchmark and acceptance

Compare the specialist against the existing researcher and any alternative social-signal workflow using the same query set. Measure:

- unique relevant social/regional source coverage;
- full-body/thread/comment acquisition success;
- author/date/engagement correctness;
- verbatim evidence and locator completeness;
- latency, manual interventions, login/CAPTCHA failures, and reproducibility;
- account-ban/ToS exposure, data egress, retention, and cost;
- incremental decision value, not raw URL count.

Production acceptance requires:

1. ordinary general research does not activate the social router;
2. named social/regional tasks activate only the specialist;
3. a fresh session registers only expected MCP tools and no duplicate search/browser owner;
4. secrets never appear in stdout, logs, child output, artifacts, or command history;
5. personal browser sessions are not used without separate explicit authorization;
6. prompt injection cannot expand scope, permissions, providers, or install new backends;
7. write actions are rejected;
8. unavailable channels return bounded `unavailable` results rather than escalating into installs, proxies, or logins;
9. Windows PATH, subprocess startup, timeout, cleanup, and browser/service shutdown are exercised end to end;
10. final evidence packets pass schema validation and can be independently consumed by the evidence-first researcher.

## Market-claim discipline

A high star count, marketplace rating, audit badge, or install total can establish adoption and attention, not “best.” Separate:

- repository popularity;
- skill-registry installs;
- independent security findings;
- unique platform coverage;
- target-OS test results;
- evidence quality;
- production readiness.

Use-case-specific language: a router may be a leading low-friction option for no/low-API-cost social and regional acquisition while being inferior to browser automation for interaction, Firecrawl for site-wide crawl, Apify for specific hosted actors, or an evidence-first researcher for verified synthesis.