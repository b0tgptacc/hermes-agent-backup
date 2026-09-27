# Telegram progress hook lifecycle safety

Use this when implementing or reviewing a one-message Telegram progress hook. The hook is concurrent infrastructure even when it only edits one message: `agent:start`, `agent:step`, `agent:end`, replacement runs, stale expiry, cancellation, gateway shutdown, and Telegram network completion can interleave independently.

## Preferred architecture

Prefer one supervisor task per run when designing from scratch. If separate start, heartbeat, stale, and final tasks already exist, enforce every invariant below.

## Required invariants

- Store every lifecycle task on the run state; never create an untracked cleanup task.
- Publish or reject lifecycle tasks atomically under the same run-registry lock. Once retirement starts, no new task may be attached. Repeated `agent:end` reuses the existing final-cleanup task.
- Run retirement in one independently owned task/future. Callers await it through `asyncio.shield`, so cancellation of an event handler cannot strand half-retired state.
- Concurrent lifecycle callers share the same retirement completion. A sibling being cancelled by retirement must not await the retirement owner that is awaiting it; exclude the initiating lifecycle task from sibling cancellation.
- A cancelled replacement `agent:start` independently retires both the newly registered and previous states, including any late `sendMessage` result. Re-check the new state under the registry lock before spawning tasks.
- Never cancel a coroutine merely because it awaits `asyncio.to_thread`; the worker continues. Preserve it until it captures `message_id`, then delete any late bubble.
- Serialize edits and deletion per run. Render text only after acquiring the lock so a queued heartbeat cannot restore an older stage after the final edit.
- A failed initial `sendMessage` retires immediately. Deletion uses bounded retries, catches transport exceptions, and stale/final cleanup retires in `finally`.
- Keep percentages out unless progress has a real fixed denominator. Named stages (`Этап N/5`) plus a periodic liveness timestamp are honest; tool-iteration counts are not completion percentages.

## Deterministic regression matrix

Use events and barriers, not fixed sleeps. Cover:

1. Fast-turn suppression.
2. End during in-flight send, including late success and no `message_id`.
3. Ordinary and exceptional send failure.
4. Replacement during send, edit, and delete.
5. Cancellation at every await in replacement start.
6. Simultaneous stale and final cleanup.
7. Cancellation of the retirement caller before and after retirement-task publication.
8. Repeated `agent:end` and end queued against retirement on the registry lock.
9. Bounded delete failures and exceptional stale cleanup.
10. Monotonic edit ordering and zero pending tasks after every terminal path.

Stress the race tests repeatedly before the single final gateway restart. Keep the gateway running during iterative verification to avoid user-visible restart notifications.
