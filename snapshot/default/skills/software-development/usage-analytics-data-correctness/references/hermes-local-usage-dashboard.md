# Hermes local usage dashboard: verified review notes

These notes apply to Hermes v0.20-era `state.db` and the built-in OpenAI Codex account-usage path. Re-check source and live schema after upgrades.

## Local accounting

- `sessions` stores cumulative session counters and routing identity.
- `session_model_usage` partitions usage by session, model, provider/base URL, billing mode, and `task`.
- `task = ''` represents main-loop accounting; non-empty tasks represent auxiliary calls such as vision, compression, and title generation.
- MoA advisor calls are intentionally excluded from auxiliary recording because conversation-loop accounting already folds them into the main delta.
- Do not add `sessions` token counters to all `session_model_usage` rows.
- For legacy fallback, reconcile session aggregates against represented **main** detail only. Auxiliary rows must remain additive and must not mask a missing main detail row.
- Canonical normalization separates cache read/write from input totals. Reasoning tokens are observability detail within output and should not be added again to total volume.

## Temporal limitation

`started_at`, `first_seen`, and `last_seen` are timestamps around cumulative rows, not a ledger of token deltas. A filter on session start produces a session-cohort metric, not exact usage during a calendar interval. Exact day/week history requires per-call delta rows with timestamps.

## Telegram attribution

Gateway peer refresh writes `source.user_id` into the session row and can update it on later turns. In a group or forum session this can become the latest sender, so assigning the full cumulative session usage to that ID is incorrect. `display_name` may be a chat presentation name rather than a stable person. Use chat/thread/session attribution for shared conversations; permit per-user attribution only for confirmed DMs unless an event ledger captures the initiating user per call.

For work spawned from a confirmed DM, descendant `subagent` sessions can be attributed to the DM user by walking `parent_session_id` to the trusted root. Resolve ancestry with memoization and cycle detection. Keep the actual source breakdown unchanged, expose delegated usage as a separate subtotal, and add two regression fixtures: a DM root whose descendant usage is included, and a group/shared root whose usage is not assigned to one person. Group usage should remain visible in the aggregate Telegram/source view.

## OpenAI Codex OAuth quota

The supported account-usage helper resolves OAuth credentials server-side and calls the Codex usage endpoint with the bearer token. Consume only its sanitized snapshot: windows, used percent, reset times, plan, and optional credit details. Never parse or expose `auth.json` in dashboard code.

The percentage is upstream rate-limit utilization, not a token denominator. It cannot establish absolute token capacity, remaining messages, cost, model/task/user split, or local calendar usage. With a credential pool, the snapshot may describe the selected credential while local rows combine calls made under several credentials; the usage schema has no credential/account dimension.

Do not expose reset-credit redemption in a read-only dashboard; it performs a quota-changing POST.

## Live SQLite

Observed deployments may use rollback-journal (`journal_mode=delete`) rather than WAL. Use URI `mode=ro`, a short timeout, and one brief read transaction for a consistent multi-query snapshot. A long rollback-journal read can delay writer commit. Do not use `immutable=1` for a live database. If a snapshot is needed, use SQLite backup API rather than copying only `state.db`, because a future/other deployment may use WAL.

## Local web boundary

Binding to `127.0.0.1` is necessary but insufficient when the dashboard contains PII or account telemetry. Validate Host, deny wildcard CORS, set CSP and `Cache-Control: no-store`, keep OAuth fetches server-side, and use a random local session/startup token for sensitive views. Cache sanitized quota snapshots briefly to avoid repeated refresh/API traffic.

Use an explicit Host allowlist rather than suffix matching. Regression probes should accept `127.0.0.1:<actual-port>` and `localhost:<actual-port>`, reject `attacker.example` and `127.0.0.1.evil:<port>`, and confirm non-loopback bind attempts fail.

## Review synchronization

Async reviewers can observe a mixed state when tests are added before implementation or files change mid-review. Before dispatch, finish edits and record hashes or a revision. If the reviewer reports that files changed externally, discard the verdict as stale, complete the implementation, rerun the full suite, and re-review the stable snapshot. A race-induced failure is useful evidence for a regression test, but not proof that the final artifact still fails.
