"""Best-effort, non-technical Telegram progress indicator.

The hook deliberately exposes no tool names, arguments, paths, prompts, errors,
or timing promises. Stages are semantic lifecycle markers, not time estimates.
"""

from __future__ import annotations

import asyncio
import json
import os
import secrets
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Any


_START_DELAY_SECONDS = 1.5
_FINAL_CLEANUP_SECONDS = 30.0
_STALE_CLEANUP_SECONDS = 30 * 60.0
_HEARTBEAT_SECONDS = 60.0
_DELETE_RETRY_ATTEMPTS = 3
_DELETE_RETRY_SECONDS = 1.0

_STAGE_TEXT = {
    1: "Задача принята",
    2: "Собираю необходимую информацию",
    3: "Готовлю решение",
    4: "Проверяю результат",
    5: "Завершаю работу",
}


def format_stage(stage: int, *, updated_at: str = "") -> str:
    normalized_stage = max(1, min(5, int(stage)))
    text = (
        f"{_STAGE_TEXT[normalized_stage]}\n"
        f"Этап {normalized_stage}/5\n"
        "Продолжительность зависит от задачи."
    )
    if updated_at:
        text += f"\nЗадача ещё выполняется · Обновлено: {updated_at}"
    return text


@dataclass
class RunState:
    run_id: str
    session_id: str
    chat_id: str
    thread_id: str = ""
    stage: int = 1
    message_id: str = ""
    ended: bool = False
    send_started: bool = False
    created_at: float = field(default_factory=time.monotonic)
    start_task: asyncio.Task | None = None
    stale_task: asyncio.Task | None = None
    heartbeat_task: asyncio.Task | None = None
    cleanup_task: asyncio.Task | None = None
    stop_event: asyncio.Event = field(default_factory=asyncio.Event)
    edit_lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    retire_lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    retirement_task: asyncio.Task | None = None


_RUNS: dict[str, RunState] = {}
_LOCK = asyncio.Lock()


def _telegram_token() -> str:
    return os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()


def _api_call_sync(method: str, payload: dict[str, Any]) -> dict[str, Any]:
    token = _telegram_token()
    if not token:
        return {}
    body = urllib.parse.urlencode(payload).encode("utf-8")
    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/{method}",
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            parsed = json.loads(response.read().decode("utf-8"))
    except Exception:
        # Progress is best-effort and must never interrupt the agent turn.
        return {}
    return parsed if isinstance(parsed, dict) and parsed.get("ok") else {}


async def _api_call(method: str, payload: dict[str, Any]) -> dict[str, Any]:
    return await asyncio.to_thread(_api_call_sync, method, payload)


async def _send(state: RunState) -> None:
    payload: dict[str, Any] = {
        "chat_id": state.chat_id,
        "text": format_stage(state.stage),
        "disable_notification": "true",
    }
    if state.thread_id:
        try:
            payload["message_thread_id"] = int(state.thread_id)
        except ValueError:
            pass
    result = await _api_call("sendMessage", payload)
    message = result.get("result") if isinstance(result, dict) else None
    if isinstance(message, dict) and message.get("message_id") is not None:
        state.message_id = str(message["message_id"])


async def _edit(state: RunState, *, updated_at: str = "") -> None:
    # All edits share one lock. The text is rendered only after acquiring it,
    # so a queued heartbeat sees the newest stage instead of replaying a stale
    # lower stage after the final edit.
    async with state.edit_lock:
        if not state.message_id:
            return
        await _api_call(
            "editMessageText",
            {
                "chat_id": state.chat_id,
                "message_id": state.message_id,
                "text": format_stage(state.stage, updated_at=updated_at),
            },
        )


async def _delete(state: RunState) -> bool:
    # Serialize delete behind any in-flight edit. Retry transient failures a
    # bounded number of times; progress cleanup must not live forever.
    async with state.edit_lock:
        if not state.message_id:
            return True
        for attempt in range(_DELETE_RETRY_ATTEMPTS):
            try:
                result = await _api_call(
                    "deleteMessage",
                    {"chat_id": state.chat_id, "message_id": state.message_id},
                )
            except Exception:
                result = {}
            if result:
                state.message_id = ""
                return True
            if attempt + 1 < _DELETE_RETRY_ATTEMPTS:
                await asyncio.sleep(_DELETE_RETRY_SECONDS)
        return False


async def _cancel_and_join(task: asyncio.Task | None) -> None:
    if task is None or task is asyncio.current_task() or task.done():
        return
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)


async def _join_heartbeat(state: RunState) -> None:
    task = state.heartbeat_task
    if task is None or task is asyncio.current_task() or task.done():
        return
    # stop_event wakes the ordinary sleep immediately. If a heartbeat edit is
    # already in flight, let it finish completely so no detached to_thread HTTP
    # request can arrive after the final stage. _api_call_sync is itself bounded.
    await asyncio.gather(task, return_exceptions=True)


async def _perform_retirement(
    state: RunState,
    preserve_inflight_start: bool,
    initiator: asyncio.Task | None,
) -> None:
    """Run the cancellation-safe retirement critical section once."""
    state.ended = True
    state.stop_event.set()

    if (
        not preserve_inflight_start
        and not state.send_started
        and state.start_task is not initiator
    ):
        await _cancel_and_join(state.start_task)
    if state.cleanup_task is not initiator:
        await _cancel_and_join(state.cleanup_task)
    if state.stale_task is not initiator:
        await _cancel_and_join(state.stale_task)

    async with _LOCK:
        if _RUNS.get(state.session_id) is state:
            _RUNS.pop(state.session_id, None)

    await _join_heartbeat(state)


async def _retire_state(
    state: RunState,
    *,
    preserve_inflight_start: bool = False,
) -> None:
    """Retire through one shielded task that survives caller cancellation."""
    created = False
    current = asyncio.current_task()
    async with state.retire_lock:
        task = state.retirement_task
        if task is None:
            task = asyncio.create_task(
                _perform_retirement(
                    state,
                    preserve_inflight_start or state.send_started,
                    current,
                )
            )
            state.retirement_task = task
            created = True

    lifecycle_tasks = {
        state.start_task,
        state.stale_task,
        state.cleanup_task,
        state.heartbeat_task,
    }
    # If retirement is already owned elsewhere, a lifecycle task entering from
    # its cancellation/finally path must not await the owner that is awaiting it.
    if not created and current in lifecycle_tasks:
        return
    await asyncio.shield(task)


async def _delayed_start(state: RunState) -> None:
    try:
        await asyncio.sleep(_START_DELAY_SECONDS)
        if state.ended:
            await _retire_state(state)
            return
        state.send_started = True
        await _send(state)
        # A failed ordinary send has no progress bubble to maintain. Retire
        # immediately instead of keeping stale/heartbeat tasks alive until end.
        if not state.message_id:
            await _retire_state(state, preserve_inflight_start=True)
            return
        # The turn may end or be replaced while Telegram accepts sendMessage.
        if state.ended:
            await _delete(state)
            await _retire_state(state, preserve_inflight_start=True)
    except asyncio.CancelledError:
        return
    except Exception:
        # A progress API failure must not leave lifecycle tasks registered or
        # surface as an unhandled background-task exception.
        await _retire_state(state, preserve_inflight_start=state.send_started)
        return


async def _stale_cleanup(state: RunState) -> None:
    try:
        await asyncio.sleep(_STALE_CLEANUP_SECONDS)
        state.ended = True
        state.stop_event.set()
        await _delete(state)
    except asyncio.CancelledError:
        return
    finally:
        await _retire_state(state, preserve_inflight_start=state.send_started)


async def _heartbeat(state: RunState) -> None:
    """Refresh the same status bubble so long turns visibly remain alive."""
    try:
        while not state.stop_event.is_set():
            try:
                await asyncio.wait_for(
                    state.stop_event.wait(),
                    timeout=_HEARTBEAT_SECONDS,
                )
                return
            except asyncio.TimeoutError:
                pass
            if state.message_id and not state.ended:
                await _edit(state, updated_at=time.strftime("%H:%M"))
    except asyncio.CancelledError:
        return


async def _finish_and_cleanup(state: RunState) -> None:
    try:
        state.stage = max(state.stage, 5)
        state.stop_event.set()
        await _join_heartbeat(state)
        if state.message_id:
            await _edit(state)
        await asyncio.sleep(_FINAL_CLEANUP_SECONDS)
        await _delete(state)
    finally:
        await _retire_state(state, preserve_inflight_start=state.send_started)


async def _abort_start_transaction(
    state: RunState,
    previous: RunState | None,
) -> None:
    """Independently retire both sides of a cancelled replacement start."""

    async def _cleanup(candidate: RunState) -> None:
        if candidate.message_id:
            await _delete(candidate)
        await _retire_state(
            candidate,
            preserve_inflight_start=candidate.send_started,
        )

    candidates = [state]
    if previous is not None:
        candidates.append(previous)
    await asyncio.gather(*(_cleanup(candidate) for candidate in candidates))


def _consume_detached_task(task: asyncio.Task) -> None:
    try:
        task.result()
    except asyncio.CancelledError:
        pass
    except Exception:
        pass


async def _on_start(context: dict[str, Any]) -> None:
    session_id = str(context.get("session_id") or "").strip()
    chat_id = str(context.get("chat_id") or "").strip()
    if not session_id or not chat_id:
        return
    state = RunState(
        run_id=secrets.token_hex(8),
        session_id=session_id,
        chat_id=chat_id,
        thread_id=str(context.get("thread_id") or "").strip(),
    )
    previous: RunState | None = None
    registered = False
    try:
        async with _LOCK:
            previous = _RUNS.get(session_id)
            _RUNS[session_id] = state
            registered = True

        if previous is not None:
            previous.ended = True
            previous.stop_event.set()
            if previous.message_id:
                await _delete(previous)
            await _retire_state(
                previous,
                preserve_inflight_start=previous.send_started,
            )

        # Cleanup of the previous run may await Telegram I/O. During that window
        # agent:end can retire the newly registered state, so re-check atomically
        # before creating any lifecycle tasks.
        async with _LOCK:
            if (
                _RUNS.get(session_id) is not state
                or state.ended
                or state.retirement_task is not None
            ):
                return
            state.start_task = asyncio.create_task(_delayed_start(state))
            state.stale_task = asyncio.create_task(_stale_cleanup(state))
            state.heartbeat_task = asyncio.create_task(_heartbeat(state))
    except asyncio.CancelledError:
        if registered:
            cleanup = asyncio.create_task(
                _abort_start_transaction(state, previous)
            )
            cleanup.add_done_callback(_consume_detached_task)
        raise


async def _on_step(context: dict[str, Any]) -> None:
    session_id = str(context.get("session_id") or "").strip()
    iteration = max(0, int(context.get("iteration") or 0))
    async with _LOCK:
        state = _RUNS.get(session_id)
        if state is None or state.ended:
            return
        # Iteration count is only a coarse activity signal used to advance
        # named semantic stages. No exact completion percentage is claimed.
        target = 2 if iteration <= 1 else 3 if iteration == 2 else 4
        if target <= state.stage:
            return
        state.stage = target
    await _edit(state)


async def _on_end(context: dict[str, Any]) -> None:
    session_id = str(context.get("session_id") or "").strip()
    should_retire = False
    preserve_inflight_start = False
    async with _LOCK:
        state = _RUNS.get(session_id)
        if state is None:
            return
        # Retirement and cleanup publication share this atomic invariant: once
        # retirement exists no new lifecycle task may be attached, and repeated
        # end events reuse the already-published cleanup task.
        if state.retirement_task is not None or state.cleanup_task is not None:
            return
        state.ended = True
        state.stop_event.set()

        if state.start_task and not state.start_task.done():
            should_retire = True
            preserve_inflight_start = state.send_started
        else:
            state.cleanup_task = asyncio.create_task(_finish_and_cleanup(state))
            state.cleanup_task.add_done_callback(_consume_detached_task)
            return

    if should_retire:
        await _retire_state(
            state,
            preserve_inflight_start=preserve_inflight_start,
        )


async def handle(event_type: str, context: dict[str, Any]) -> None:
    if str(context.get("platform") or "").lower() != "telegram":
        return
    try:
        if event_type == "agent:start":
            await _on_start(context)
        elif event_type == "agent:step":
            await _on_step(context)
        elif event_type == "agent:end":
            await _on_end(context)
    except Exception:
        # A progress failure must never affect the real response.
        return
