---
name: usage-analytics-data-correctness
description: "Use when auditing usage, quota, cost, or token dashboards."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [analytics, usage, quota, sqlite, security, data-correctness]
---

# Usage Analytics Data-Correctness Review

## When to Use

Use for security or correctness reviews of dashboards that report tokens, API calls, costs, credits, rate limits, or per-user usage. It is especially relevant when metrics combine cumulative database rows with provider account telemetry, when sessions can span reporting boundaries, or when messaging gateways supply identity.

Use this skill to review or design dashboards that combine local event/session data with provider account quotas, especially when the store is SQLite and identities come from messaging gateways.

## Review workflow

1. **Inventory semantics before writing SQL.** For every counter, record whether it is a cumulative aggregate, a per-event delta, a subset of another field, or a provider-specific estimate. Treat names such as `total`, `input`, `cached`, `reasoning`, and `aux` as untrusted until their write paths are inspected.
2. **Trace every write path.** Find the code and tests that populate aggregates, model/task breakdowns, timestamps, and identities. Verify migrations and the live schema read-only. Do not infer semantics from table names alone.
3. **Define one source of truth per view.** Never add a parent aggregate to its own breakdown. If legacy rows need fallback, compute non-negative residuals against only the dimensions represented by the parent aggregate.
4. **Audit identity granularity.** Distinguish account, credential, conversation, chat/thread, session, and individual sender. A mutable session-level `user_id` cannot support per-user attribution in a shared conversation.
5. **Audit time granularity.** Aggregate rows with `first_seen`/`last_seen` cannot be split precisely across day/week boundaries. Mark session-cohort approximations honestly; require timestamped usage deltas for exact period totals.
6. **Separate local accounting from provider quota.** Quota percentages are independent upstream telemetry unless the provider documents an absolute denominator and the local store carries the same account/credential identity.
7. **Review live SQLite access.** Use URI `mode=ro`, short transactions, bounded wait, parameterized queries, and a stale-cache/503 fallback. Test the actual journal mode. Never use `immutable=1` against a live store or copy only the main file when WAL may exist.
8. **Review secret and browser boundaries.** Resolve OAuth credentials server-side through the application's supported helper. Never return or log tokens. Loopback binding is not authentication; constrain Host/CORS, disable caching of sensitive responses, and add local auth when PII is exposed.
9. **Report certainty explicitly.** Separate verified facts, safe approximations, and values that cannot be inferred.
10. **Review a quiescent snapshot.** Do not edit code while an asynchronous reviewer is testing it. Record hashes or a revision before dispatch; if files change during review, treat that verdict as stale, finish the edits, rerun the complete suite, and request a fresh review of the final snapshot. Never report a stale FAIL as a current defect or a stale PASS as approval.

## Counting invariants

- If detailed rows partition an aggregate, use the detailed rows once; do not add the aggregate again.
- Auxiliary usage belongs in its own task dimension and may be merged for presentation only after deduplication.
- Cache buckets may be carved out of input totals by normalization; confirm before summing.
- Reasoning tokens are often a subset of output tokens; do not add them to total unless the provider contract proves they are disjoint.
- A safe legacy fallback is generally `max(0, aggregate - represented_main_detail)`. Do not subtract auxiliary rows from a main-loop-only aggregate.
- Cost, token volume, API-call count, and provider quota are different metrics and must not be used as proxies for one another.

## Time-window rules

- Store/query UTC instants; define reporting timezone explicitly with an IANA zone.
- Build local calendar boundaries first, convert them to UTC, and query half-open ranges `[start, end)`.
- Do not model a calendar day as a fixed 86,400 seconds across DST.
- State whether a week starts Monday, Sunday, or follows a provider reset window.
- Exact historical daily totals require timestamped per-call deltas. Session start/end timestamps are insufficient for sessions crossing a boundary.

## SQLite concurrency rules

- Open an existing database with `file:...?...mode=ro`; never let a dashboard create or migrate it.
- Use one short read transaction when multiple queries must share a snapshot. In rollback-journal mode, long reads can delay writer commits.
- Use bounded `busy_timeout` and return a cached result or explicit temporary-unavailable state on lock contention.
- Avoid sharing one connection concurrently across request threads. If pooling, enforce exclusive checkout.
- Use SQLite backup API for snapshots. A file copy can omit committed WAL content.

## Identity and privacy rules

- Prefer stable platform IDs over display names; names are mutable and non-unique.
- In shared chats, attribute usage to chat/thread/session unless each usage event records the initiating sender.
- Descendant jobs/subagents may be rolled up through `parent_session_id` only when the root identity is trustworthy (for example, a confirmed DM). Keep both total and delegated subtotals, detect parent cycles, and do not use lineage to manufacture per-user attribution for shared roots.
- Treat message content, user IDs, chat IDs, titles, paths, and model prompts as sensitive local data.
- For a web dashboard, bind loopback **and** validate Host, deny wildcard CORS, apply CSP and `Cache-Control: no-store`, and use a random local session token if sensitive data is shown.
- Keep quota-changing actions out of a read-only usage dashboard.

## Provider quota interpretation

A quota percentage normally does **not** establish token count, absolute capacity, remaining requests, cost, model split, user attribution, linear burn rate, or local day/week usage. With credential rotation, it may describe one selected account while the local database combines several. Display it as a separate upstream account-limit card with its own fetch time and reset time.

## Verification checklist

- [ ] Live schema and journal mode verified read-only
- [ ] Counter write paths and subset relationships inspected
- [ ] Main/aux/legacy reconciliation tested
- [ ] Shared-chat attribution limitations documented
- [ ] Descendant lineage roll-up tested for a confirmed DM and rejected for a shared/group root
- [ ] Timezone, week definition, and DST behavior explicit
- [ ] OAuth tokens remain server-side and absent from logs/API payloads
- [ ] Loopback bind and Host allowlist tested with valid hosts plus hostile lookalikes (for example `attacker.example` and `127.0.0.1.evil`)
- [ ] Quota telemetry is not converted into unsupported token/request estimates
- [ ] Every approximation is labeled in the UI
- [ ] Independent review was run against the final, unchanged file snapshot

## References

- `references/hermes-local-usage-dashboard.md` — Hermes-specific schema, OAuth quota, Telegram attribution, and SQLite findings.
