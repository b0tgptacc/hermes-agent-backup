# Telegram user-facing progress UX

Use this pattern when users need confidence that a long Telegram task is still running without seeing internal implementation details.

## Product contract

- Progress is a product-level abstraction, not a transcription of tool calls.
- Use one editable status message. Avoid one permanent message per tool or stage.
- Delay the first status by about 1–2 seconds so fast answers do not flicker.
- Keep stages monotonic. Never move backward when parallel tools complete out of order.
- Label percentages as conditional/stage-based; they are not time estimates.
- Never display 100% before the final answer is actually deliverable.
- After successful final delivery, delete the temporary status after a short grace period. On failure/cancellation, leave or replace it with a safe, nontechnical outcome.
- Treat every send/edit/delete as best-effort; progress failures must not abort the agent turn.

Recommended Russian stages:

1. «Задача принята» — «Этап 1/5»
2. «Собираю необходимую информацию» — «Этап 2/5»
3. «Готовлю решение» — «Этап 3/5»
4. «Проверяю результат» — «Этап 4/5»
5. «Завершаю работу» — «Этап 5/5»

Do not show numeric percentages unless completion is measured against a known, fixed workload. Tool iterations are not a valid denominator. Suggested note: «Продолжительность зависит от задачи.»

## Privacy and output policy

Never expose:

- tool names or arguments;
- terminal commands, URLs with credentials, or local paths;
- reasoning/scratch text;
- iteration numbers, stack traces, or raw exceptions;
- OAuth/configuration details.

Set explicit Telegram overrides because global display values take precedence over platform defaults:

```text
hermes config set display.platforms.telegram.tool_progress off
hermes config set display.platforms.telegram.interim_assistant_messages false
hermes config set display.platforms.telegram.thinking_progress false
hermes config set display.platforms.telegram.show_reasoning false
hermes config set display.platforms.telegram.long_running_notifications false
hermes config set display.platforms.telegram.busy_ack_detail false
```

Restart the gateway after configuration changes.

## Durable implementation option: gateway hook

A profile-scoped gateway hook under `$HERMES_HOME/hooks/<name>/` can subscribe to:

- `agent:start`: cache `session_id`, `chat_id`, `thread_id`; schedule delayed first status;
- `agent:step`: advance a monotonic semantic stage and edit the same message;
- `agent:end`: advance only to 95%, then schedule cleanup after final delivery has had time to land.

Use `session_id` (plus a per-run nonce/state object) to prevent parallel or stale cleanup tasks from editing a newer run. For Telegram forum topics, include `message_thread_id` on the initial send. Keep API errors fully suppressed or safely logged without token-bearing URLs.

Do not infer exact completion from tool count. Tool/iteration activity may be used only as a coarse monotonic signal because future work is unknown.

## Edge cases

- Fast turn: cancel delayed status and send nothing.
- Repeated/parallel events: ignore stage regressions and duplicate edits.
- New run for the same session: retire/delete the previous status before installing new state.
- Stop/cancel/timeout: ensure status eventually expires; do not leave a false «Готово».
- Gateway restart: in-memory cleanup cannot run after process death, so statuses must be self-limiting where the platform or architecture permits; never claim perfect cleanup across hard termination.
- Shared/group chats: key state by the real chat/thread/session, not only user ID.
- Interactive clarify/approval prompts may intentionally pause native Telegram typing. Every answer, timeout, send failure, and exception path must resume the existing typing refresh loop; use a `try/finally` or context manager and regression-test the pause→resume lifecycle.
- Stage-based progress can appear frozen during long research. Prefer five honest semantic stages over a fabricated fixed task count or percentage, and refresh the same status message periodically (for example once per minute) with a nontechnical liveness timestamp such as «Задача ещё выполняется · Обновлено: HH:MM». Do not create additional messages.

## Verification

1. Unit-test fast-turn suppression.
2. Unit-test exactly one initial `sendMessage` and subsequent `editMessageText` calls.
3. Assert displayed strings contain no technical vocabulary or dynamic tool data.
4. Test non-Telegram events are ignored.
5. Restart gateway and verify the hook loaded in gateway logs.
6. Verify resolved per-platform display settings.
7. Send a real multi-step Telegram request and observe one status bubble advancing before the final answer. Do not claim end-to-end completion without this final inbound test.
