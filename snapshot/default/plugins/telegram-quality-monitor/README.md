# Telegram Quality Monitor

Private quality monitoring for Telegram turns handled by Hermes Gateway.

Administrative reports are sent by a dedicated send-only Telegram bot using
the profile secret `TELEGRAM_QUALITY_MONITOR_BOT_TOKEN`. They never use the
primary conversational bot token.

## Runtime behavior

- `pre_llm_call` remembers the Telegram sender ID for a turn.
- `post_llm_call` returns quickly after placing the completed turn in a bounded
  in-memory queue; it does not wait on SQLite, the summarizer, or Telegram.
- A gateway-owned daemon worker persists the turn, calls the auxiliary task
  `telegram_quality_summary`, and sends a realtime report to the configured
  admin chat.
- At 20:00 local gateway time, the worker sends one daily digest when there are
  undigested turns.
- The worker resumes queued/retry work after a gateway restart.

## Model routing

The auxiliary task is pinned in Hermes config to:

- provider: `openai-codex`
- model: `gpt-5.4-mini`

The primary agent model is not changed.

## Defaults

- Short request shown verbatim: up to 1,200 characters.
- Summarizer input cap: 12,000 request characters and 16,000 response
  characters (head+tail bounding).
- Realtime delivery retries: up to 8 attempts with exponential backoff.
- Daily digest: 20:00 local gateway time, up to 100 turns per digest.
- Local retention: an absolute 30 days for sent and terminally failed rows,
  regardless of daily-digest or plugin enablement state.
- The admin's own Telegram turns are excluded. `admin_user_id` defaults to the
  admin chat ID, which is correct for a private DM; configure it explicitly if
  the report destination changes to a group or channel.

## Data handling

The local database is:

`%HERMES_HOME%/quality-monitor/monitor.db`

Before persistence and submission to the auxiliary OpenAI model, common
credential formats are masked (OpenAI/GitHub/AWS keys, Telegram bot tokens,
JWTs, bearer tokens, and common token/password assignments). This is secret
redaction, not general PII anonymization: names, ordinary email addresses,
phone numbers, and business data remain visible because the feature is meant
for administrator quality review.

User-controlled HTML and Markdown control characters are neutralized before
Telegram delivery to prevent report-label or link spoofing.

The dedicated bot token lives only in `%HERMES_HOME%/.env`; do not place it in
`config.yaml`, logs, tests, or reports.

## Delivery semantics

SQLite claims and per-row digest markers prevent ordinary duplicate processing.
Telegram does not expose a general idempotency key, so a process crash after
Telegram accepts a message but before SQLite commits can still produce a
duplicate on retry. Every realtime report contains a stable Turn ID for manual
deduplication.

## Verification

```text
python -m unittest -q test_monitor.py
hermes plugins doctor C:/Users/admin/AppData/Local/hermes/plugins/telegram-quality-monitor --ci
hermes gateway status
```
