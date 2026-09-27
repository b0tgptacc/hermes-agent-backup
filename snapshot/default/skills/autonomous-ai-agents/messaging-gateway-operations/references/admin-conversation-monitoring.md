# Administrator conversation monitoring for messaging gateways

Use this reference when an operator wants private visibility into user messages and model replies for quality improvement. Keep monitoring read-only and fail-open: telemetry must never delay, modify, or block the user-facing turn.

## Preferred architecture

Use Hermes observer hooks rather than patching the gateway core:

- `pre_llm_call` exposes turn-level input context, including `session_id`, `turn_id`, `user_message`, `platform`, and commonly `sender_id`.
- `post_llm_call` fires once after the completed turn and exposes `user_message`, `assistant_response`, `session_id`, `turn_id`, `model`, and `platform`.
- Correlate input and output by `turn_id`; cache sender metadata from the pre-hook when the post-hook does not carry it.
- Filter by platform and exclude the administrator's own chat to avoid feedback loops.
- Enqueue completed records and perform summarization/delivery asynchronously. Hook callbacks should stay fast and return no behavior-changing value.
- Use `turn_id` as an idempotency key, persist pending delivery locally, and retry boundedly so network failures do not lose or duplicate reports.

A practical report contains sender name/ID, timestamp, request text or summary, short response summary, duration/status, and session/turn IDs. Display short inputs verbatim; summarize only over a configured character threshold. A cheaper auxiliary model is usually sufficient for summaries.

## Delivery patterns

1. **Real-time private admin feed:** one report after each completed turn. Best for immediate oversight.
2. **Scheduled digest:** periodically read new completed turns from the canonical session store, group by user/topic, and highlight errors, repeated reformulations, latency, and likely quality gaps.
3. **Hybrid:** real-time alerts for every turn or only anomalies, plus a daily quality digest. This is the default recommendation.
4. **External observability backend:** use hook-based integrations such as Langfuse when full traces, token usage, tools, evaluations, and dashboards justify the privacy and operational cost.

Prefer a separate private admin chat or dedicated monitoring bot. If the same bot delivers reports, ensure outbound admin reports cannot re-enter the monitored inbound path.

### Dedicated send-only Telegram bot pattern

For strong separation from the conversational bot, use a second Telegram bot only as an outbound report transport. Do not register it as another inbound gateway adapter unless commands or replies to the monitoring bot are an explicit requirement.

1. Validate the supplied credential with Telegram `getMe` without printing the token; record only safe bot metadata such as bot ID and username.
2. Store it under a distinct profile-scoped secret such as `TELEGRAM_QUALITY_MONITOR_BOT_TOKEN` in `%HERMES_HOME%/.env`. Never reuse or replace the primary adapter token.
3. Have the administrator open the new bot and send `/start` before testing private delivery. A valid token can still return `Chat not found` until this happens.
4. Make the observer's sender read only the dedicated secret and call the Telegram sender with the explicit `(token, admin_chat_id, message)` tuple. Remove imports of the primary Telegram adapter's standalone sender.
5. Do **not** fall back to the primary bot when the dedicated credential is missing or delivery fails. Keep the report retryable while allowing the user's main response to complete normally.
6. Unit-test both negative and positive routing: missing dedicated token raises/retries, and a mocked sender receives the dedicated token. Search the plugin afterward for primary token names and adapter sender imports.
7. Restart the gateway so the updated `.env` is loaded, then run a real hook-to-delivery E2E through the queue, summarizer, and dedicated bot. Verify terminal status `sent`, empty pending/retry queues, and remove synthetic records.

This pattern isolates admin telemetry without creating a second conversational surface, preserves fail-open behavior for users, and makes accidental regression to the primary bot detectable.

## Telegram delivery and output hygiene

For a single private administrator feed, configure both the report destination and the excluded administrator identity explicitly. Prefer numeric Telegram IDs. If a plugin schema is under your control and `hermes config set` coerces numeric input to an integer, declare ID settings as `int` (zero meaning unset/fallback) and cast to `str` at the Bot API boundary. Do not try to force a string by shell-embedding quotes unless you have verified the parser: some Hermes CLI paths preserve those quotes as part of the value.

To show Telegram users only the model's clean answer while preserving tool capability, use explicit per-platform display overrides:

```yaml
display:
  platforms:
    telegram:
      streaming: true
      tool_progress: off
      interim_assistant_messages: false
      long_running_notifications: false
      busy_ack_detail: false
      show_reasoning: false
      cleanup_progress: true
```

`tool_progress` and `interim_assistant_messages` are independent channels. Disabling only one can still expose lines such as file writes, terminal commands, reads, task updates, or Codex commentary. `streaming: true` may remain enabled because it edits the clean model response rather than exposing tool execution.

Always verify the resolved values through `gateway.display_config.resolve_display_setting()` after saving. Resolution order is per-platform override, global display value, built-in platform default, then global default; therefore a global `display.tool_progress: all` can override Telegram's quieter built-in default unless an explicit Telegram override is present.

## Durable delivery details

- Keep the synchronous hook free of SQLite/network/LLM work. A bounded in-memory handoff to a gateway worker avoids delaying the user response; persist promptly and document the small hard-crash window before persistence.
- Persist `claimed_at` (or an equivalent lease timestamp) when a worker claims a row. Recover only expired claims, not rows whose original creation time is old.
- Track daily-digest inclusion per row (`digested_at` or equivalent), not only with a timestamp cursor; otherwise an older retry that succeeds after a newer row can be omitted forever.
- Make retention absolute for terminal rows. Do not require `digested_at` for deletion: disabling the digest or receiving more rows than the daily batch cap must not bypass retention.
- Treat Telegram sender responses as success only when the contract explicitly says so (for example `result.get("success") is True`). Error-only or unknown dictionary shapes must remain retryable.
- Telegram does not provide a general idempotency key. A crash after Telegram accepts a report but before the local commit can still duplicate delivery; include a stable Turn ID and document this at-least-once edge.
- Neutralize HTML/Markdown control characters in untrusted request text and model-generated summaries before privileged admin delivery to prevent formatted-link or report-label spoofing.

## Avoid weak implementations

- Ordinary gateway logs are not a transcript contract: input may be preview-truncated and response logs may contain only length/status. Do not build durable monitoring from log scraping alone.
- Polling the internal session database can support digests, but bind to stable store APIs/schema and track a durable high-water mark; avoid fragile joins based on timestamps.
- Do not patch `gateway/run.py` when observer hooks satisfy the requirement; core patches create update conflicts and a larger blast radius.
- Gateway health OTLP monitoring is intentionally content-free and is not a conversation-audit channel.

## Privacy and security

- Treat prompts and responses as confidential content. Notify users or establish an appropriate policy/legal basis before monitoring.
- Independently redact secrets and configured PII before admin delivery; do not assume turn-level hook payloads are safe to forward verbatim.
- Restrict the admin destination with an explicit allowlist and use numeric IDs.
- Define retention, deletion, access control, and whether summaries may be sent to an external model provider.
- Keep full raw transcripts local by default; send the minimum useful content to the admin channel.

## Verification

Before declaring the monitor complete, exercise real turns from an allowed non-admin user and verify:

1. a short input appears verbatim;
2. a long input is summarized at the configured threshold;
3. the final assistant response is summarized and correlated to the correct turn;
4. admin-originated messages do not loop;
5. duplicate hook delivery does not duplicate the report;
6. Telegram/API delivery failure queues and later retries the report;
7. redaction removes representative secrets and PII;
8. monitoring failure does not affect the user's response;
9. a restart preserves the delivery high-water mark and pending queue.
