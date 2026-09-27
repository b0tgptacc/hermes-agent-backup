# Telegram progress hook lifecycle and concurrency

Use this reference when implementing one editable Telegram progress message for long agent turns. The hook is networked concurrent lifecycle code, not a formatting helper.

## User-facing contract

- Show one nontechnical editable message.
- Use honest semantic stages such as `Этап 1/5` through `Этап 5/5`.
- Do not display percentages unless completion has a real fixed denominator; tool iteration count is not one.
- Add a low-rate liveness timestamp (for example once per minute) rather than creating new messages.
- Native `typing` may be paused during clarify/approval prompts, but every answer, timeout, scheduling failure, send failure, and exception path must resume it via `finally` or a context manager.

## Cancellation-safe lifecycle

Prefer one supervisor task per run. If start, heartbeat, stale, final-cleanup, and retirement tasks are separate, track every task explicitly and enforce these invariants:

1. Register a run atomically. If cleanup of a previous run awaits Telegram I/O, re-check under the registry lock that the replacement is still current, not ended, and not retiring before spawning lifecycle tasks.
2. Never cancel an `asyncio.to_thread` send/edit and assume its HTTP request stopped. Keep the task until it captures `message_id`, then delete any late bubble.
3. Serialize edit and delete operations per run so a delayed heartbeat cannot overwrite a newer or final stage.
4. Run retirement in one independently owned task/future stored on the run. Callers await it with `asyncio.shield`, so cancelling a caller cannot strand half-completed retirement.
5. Concurrent lifecycle callers share the retirement task. A lifecycle task entering from its cancellation `finally` must not await a retirement owner that is already awaiting that same task. Exclude the initiating lifecycle task from sibling cancellation.
6. Put stale and final retirement in `finally` blocks. Unexpected `sendMessage` failure or a result without `message_id` retires the cosmetic progress state immediately and never affects the agent turn.
7. Retry `deleteMessage` a small bounded number of times and catch transport exceptions. Do not keep internal state alive forever for cosmetic cleanup; disclose that a message can remain if all bounded attempts fail.
8. Identity-guard registry removal so an old cleanup cannot remove a replacement run.

## Required adversarial tests

Use events/barriers, not fixed sleeps. Test:

- fast-turn suppression;
- end while `sendMessage` is in flight, both success and no `message_id`;
- replacement while send/edit/delete is blocked;
- start/end overlap while previous-run deletion is blocked;
- ordinary and exceptional send failure;
- heartbeat/final edit completion reordered deliberately;
- stale and final cleanup expiring simultaneously;
- transient and exceptional delete failures with bounded retries;
- cleanup-task tracking and replacement cancellation;
- cancellation of the caller after retirement is created but while registry removal is blocked;
- repeated stress runs with no pending tasks, deadlocks, duplicate deletes, stage regressions, or orphaned registry entries.

After tests, restart the gateway, verify the hook name loaded, Telegram polling connected, resolved typing/display settings, and a real inbound multi-step turn. Process status or outbound-only delivery is not full E2E proof.
