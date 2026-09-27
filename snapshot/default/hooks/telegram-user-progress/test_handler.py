from __future__ import annotations

import asyncio
import gc
import importlib.util
import pathlib
import unittest
from unittest.mock import patch


PATH = pathlib.Path(__file__).with_name("handler.py")
SPEC = importlib.util.spec_from_file_location("telegram_progress_handler_tested", PATH)
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
import sys
sys.modules[SPEC.name] = MOD
SPEC.loader.exec_module(MOD)


class TelegramProgressTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        MOD._RUNS.clear()
        MOD._LOCK = asyncio.Lock()

    async def asyncTearDown(self):
        for state in list(MOD._RUNS.values()):
            for task in (
                state.start_task,
                state.stale_task,
                getattr(state, "heartbeat_task", None),
                getattr(state, "cleanup_task", None),
                getattr(state, "retirement_task", None),
            ):
                if task:
                    task.cancel()
        MOD._RUNS.clear()

    def test_text_contains_only_semantic_stage(self):
        text = MOD.format_stage(3)
        self.assertIn("Готовлю решение", text)
        self.assertIn("Этап 3/5", text)
        self.assertNotIn("%", text)
        self.assertNotIn("█", text)
        self.assertNotIn("░", text)
        for forbidden in ("terminal", "tool", "path", "token", "reasoning"):
            self.assertNotIn(forbidden, text.lower())

    async def test_heartbeat_refreshes_one_existing_message(self):
        calls = []

        async def fake(method, payload):
            calls.append((method, payload.copy()))
            if method == "sendMessage":
                return {"ok": True, "result": {"message_id": 91}}
            return {"ok": True, "result": {}}

        with (
            patch.object(MOD, "_api_call", fake),
            patch.object(MOD, "_START_DELAY_SECONDS", 0),
            patch.object(MOD, "_HEARTBEAT_SECONDS", 0.01),
        ):
            ctx = {"platform": "telegram", "session_id": "heartbeat", "chat_id": "400"}
            await MOD.handle("agent:start", ctx)
            await asyncio.sleep(0.045)

        methods = [method for method, _ in calls]
        self.assertEqual(methods.count("sendMessage"), 1)
        heartbeat_edits = [
            payload["text"]
            for method, payload in calls
            if method == "editMessageText" and "Обновлено:" in payload["text"]
        ]
        self.assertGreaterEqual(len(heartbeat_edits), 1)

    async def test_fast_turn_sends_no_progress(self):
        calls = []

        async def fake(method, payload):
            calls.append((method, payload))
            return {"ok": True, "result": {"message_id": 1}}

        with patch.object(MOD, "_api_call", fake), patch.object(MOD, "_START_DELAY_SECONDS", 0.2):
            ctx = {"platform": "telegram", "session_id": "s1", "chat_id": "100"}
            await MOD.handle("agent:start", ctx)
            await MOD.handle("agent:end", ctx)
            await asyncio.sleep(0.25)
        self.assertEqual(calls, [])

    async def test_long_turn_edits_one_message_monotonically(self):
        calls = []
        sent = asyncio.Event()

        async def fake(method, payload):
            calls.append((method, payload.copy()))
            if method == "sendMessage":
                sent.set()
                return {"ok": True, "result": {"message_id": 77}}
            return {"ok": True, "result": {}}

        with patch.object(MOD, "_api_call", fake), patch.object(MOD, "_START_DELAY_SECONDS", 0.01), patch.object(MOD, "_FINAL_CLEANUP_SECONDS", 0.01):
            base = {"platform": "telegram", "session_id": "s2", "chat_id": "200"}
            await MOD.handle("agent:start", base)
            await asyncio.wait_for(sent.wait(), timeout=1)
            await MOD.handle("agent:step", {**base, "iteration": 1})
            await MOD.handle("agent:step", {**base, "iteration": 2})
            await MOD.handle("agent:step", {**base, "iteration": 4})
            await MOD.handle("agent:end", base)
            await asyncio.sleep(0.04)

        methods = [method for method, _ in calls]
        self.assertEqual(methods.count("sendMessage"), 1)
        self.assertGreaterEqual(methods.count("editMessageText"), 4)
        self.assertEqual(methods.count("deleteMessage"), 1)
        edits = [payload["text"] for method, payload in calls if method == "editMessageText"]
        self.assertIn("Этап 2/5", edits[0])
        self.assertIn("Этап 3/5", edits[1])
        self.assertIn("Этап 4/5", edits[2])
        self.assertIn("Этап 5/5", edits[-1])

    async def test_cancelled_retirement_caller_cannot_strand_state(self):
        state = MOD.RunState(
            run_id="cancel-retire",
            session_id="cancel-retire",
            chat_id="312",
        )
        MOD._RUNS[state.session_id] = state

        await MOD._LOCK.acquire()
        try:
            caller = asyncio.create_task(MOD._retire_state(state))
            await asyncio.sleep(0)
            caller.cancel()
            await asyncio.gather(caller, return_exceptions=True)
        finally:
            MOD._LOCK.release()

        await MOD._retire_state(state)
        retirement_task = getattr(state, "retirement_task", None)
        if retirement_task is not None:
            await asyncio.shield(retirement_task)

        self.assertNotIn("cancel-retire", MOD._RUNS)

    async def test_concurrent_stale_and_final_cleanup_do_not_cancel_each_other_recursively(self):
        state = MOD.RunState(
            run_id="concurrent-cleanup",
            session_id="concurrent-cleanup",
            chat_id="307",
        )
        MOD._RUNS[state.session_id] = state

        with (
            patch.object(MOD, "_STALE_CLEANUP_SECONDS", 0),
            patch.object(MOD, "_FINAL_CLEANUP_SECONDS", 0),
        ):
            state.stale_task = asyncio.create_task(MOD._stale_cleanup(state))
            state.cleanup_task = asyncio.create_task(MOD._finish_and_cleanup(state))
            await asyncio.wait_for(
                asyncio.gather(
                    state.stale_task,
                    state.cleanup_task,
                    return_exceptions=True,
                ),
                timeout=1,
            )

        self.assertTrue(state.stale_task.done())
        self.assertTrue(state.cleanup_task.done())
        self.assertNotIn("concurrent-cleanup", MOD._RUNS)

    async def test_unexpected_send_exception_retires_state(self):
        async def fake(method, payload):
            if method == "sendMessage":
                raise RuntimeError("unexpected send failure")
            return {"ok": True, "result": {}}

        with patch.object(MOD, "_api_call", fake), patch.object(MOD, "_START_DELAY_SECONDS", 0):
            ctx = {"platform": "telegram", "session_id": "send-exception", "chat_id": "308"}
            await MOD.handle("agent:start", ctx)
            state = MOD._RUNS["send-exception"]
            await asyncio.gather(state.start_task, return_exceptions=True)
            await asyncio.sleep(0)

        self.assertNotIn("send-exception", MOD._RUNS)
        self.assertTrue(state.stale_task.done())
        self.assertTrue(state.heartbeat_task.done())

    async def test_on_end_cannot_publish_cleanup_after_retirement_started(self):
        state = MOD.RunState(
            run_id="end-retire-race",
            session_id="end-retire-race",
            chat_id="315",
        )
        MOD._RUNS[state.session_id] = state

        await MOD._LOCK.acquire()
        try:
            end_call = asyncio.create_task(
                MOD._on_end({"session_id": "end-retire-race"})
            )
            await asyncio.sleep(0)
            retire_call = asyncio.create_task(MOD._retire_state(state))
            await asyncio.sleep(0)
        finally:
            MOD._LOCK.release()

        await asyncio.gather(end_call, retire_call)
        if state.retirement_task is not None:
            await asyncio.shield(state.retirement_task)

        self.assertNotIn("end-retire-race", MOD._RUNS)
        self.assertTrue(state.cleanup_task is None or state.cleanup_task.done())

    async def test_cleanup_task_exception_is_consumed(self):
        state = MOD.RunState(
            run_id="cleanup-exception-consumed",
            session_id="cleanup-exception-consumed",
            chat_id="317",
            message_id="901",
        )
        MOD._RUNS[state.session_id] = state
        loop = asyncio.get_running_loop()
        reported = []
        previous_handler = loop.get_exception_handler()
        loop.set_exception_handler(lambda _loop, context: reported.append(context))

        async def fail_edit(*args, **kwargs):
            raise RuntimeError("forced final edit failure")

        try:
            with patch.object(MOD, "_edit", fail_edit):
                await MOD._on_end({"session_id": state.session_id})
                cleanup = state.cleanup_task
                self.assertIsNotNone(cleanup)
                done = asyncio.Event()
                cleanup.add_done_callback(lambda _task: done.set())
                await asyncio.wait_for(done.wait(), timeout=1)

            state.cleanup_task = None
            del cleanup
            gc.collect()
            await asyncio.sleep(0)
        finally:
            loop.set_exception_handler(previous_handler)

        unhandled = [
            context
            for context in reported
            if "exception was never retrieved" in str(context.get("message", "")).lower()
        ]
        self.assertEqual(unhandled, [])

    async def test_repeated_end_reuses_single_cleanup_task(self):
        state = MOD.RunState(
            run_id="repeat-end",
            session_id="repeat-end",
            chat_id="316",
        )
        MOD._RUNS[state.session_id] = state

        with patch.object(MOD, "_FINAL_CLEANUP_SECONDS", 60):
            ctx = {"session_id": "repeat-end"}
            await MOD._on_end(ctx)
            first_cleanup = state.cleanup_task
            self.assertIsNotNone(first_cleanup)
            await asyncio.sleep(0)
            await MOD._on_end(ctx)
            self.assertIs(state.cleanup_task, first_cleanup)

        await MOD._retire_state(state)
        if state.retirement_task is not None:
            await asyncio.shield(state.retirement_task)
        self.assertTrue(first_cleanup.done())

    async def test_final_cleanup_task_is_tracked_and_replacement_cancels_it(self):
        async def fake(method, payload):
            if method == "sendMessage":
                return {"ok": True, "result": {"message_id": 601}}
            return {"ok": True, "result": {}}

        with (
            patch.object(MOD, "_api_call", fake),
            patch.object(MOD, "_START_DELAY_SECONDS", 0),
            patch.object(MOD, "_FINAL_CLEANUP_SECONDS", 60),
        ):
            ctx = {"platform": "telegram", "session_id": "cleanup-track", "chat_id": "305"}
            await MOD.handle("agent:start", ctx)
            await asyncio.sleep(0.02)
            first_state = MOD._RUNS["cleanup-track"]
            await MOD.handle("agent:end", ctx)
            await asyncio.sleep(0.02)
            self.assertIsNotNone(first_state.cleanup_task)
            self.assertFalse(first_state.cleanup_task.done())

            await MOD.handle("agent:start", ctx)
            second_state = MOD._RUNS["cleanup-track"]
            await asyncio.sleep(0.02)

        self.assertIs(MOD._RUNS["cleanup-track"], second_state)
        self.assertTrue(first_state.cleanup_task.done())

    async def test_final_cleanup_exception_still_retires_state(self):
        state = MOD.RunState(
            run_id="cleanup-error",
            session_id="cleanup-error",
            chat_id="306",
            stage=4,
            message_id="602",
        )
        MOD._RUNS[state.session_id] = state
        state.stale_task = asyncio.create_task(asyncio.sleep(60))

        async def fail_edit(*args, **kwargs):
            raise RuntimeError("edit failed")

        with patch.object(MOD, "_edit", fail_edit):
            with self.assertRaisesRegex(RuntimeError, "edit failed"):
                await MOD._finish_and_cleanup(state)

        self.assertNotIn("cleanup-error", MOD._RUNS)
        self.assertTrue(state.stale_task.done())

    async def test_end_during_inflight_send_cleans_late_message(self):
        send_started = asyncio.Event()
        release_send = asyncio.Event()
        calls = []

        async def fake(method, payload):
            calls.append((method, payload.copy()))
            if method == "sendMessage":
                send_started.set()
                await release_send.wait()
                return {"ok": True, "result": {"message_id": 88}}
            return {"ok": True, "result": {}}

        with patch.object(MOD, "_api_call", fake), patch.object(MOD, "_START_DELAY_SECONDS", 0):
            ctx = {"platform": "telegram", "session_id": "race", "chat_id": "300"}
            await MOD.handle("agent:start", ctx)
            await asyncio.wait_for(send_started.wait(), timeout=1)
            state = MOD._RUNS["race"]
            await MOD.handle("agent:end", ctx)
            release_send.set()
            await asyncio.sleep(0.05)

        methods = [method for method, _ in calls]
        self.assertEqual(methods.count("sendMessage"), 1)
        self.assertEqual(methods.count("deleteMessage"), 1)
        self.assertNotIn("race", MOD._RUNS)
        self.assertTrue(state.stale_task.done())

    async def test_ordinary_failed_send_retires_without_waiting_for_end(self):
        async def fake(method, payload):
            if method == "sendMessage":
                return {}
            return {"ok": True, "result": {}}

        with patch.object(MOD, "_api_call", fake), patch.object(MOD, "_START_DELAY_SECONDS", 0):
            ctx = {"platform": "telegram", "session_id": "ordinary-fail", "chat_id": "304"}
            await MOD.handle("agent:start", ctx)
            state = MOD._RUNS["ordinary-fail"]
            await asyncio.sleep(0.05)

        self.assertNotIn("ordinary-fail", MOD._RUNS)
        self.assertTrue(state.start_task.done())
        self.assertTrue(state.stale_task.done())
        self.assertTrue(state.heartbeat_task.done())

    async def test_failed_inflight_send_retires_state_immediately(self):
        send_started = asyncio.Event()
        release_send = asyncio.Event()

        async def fake(method, payload):
            if method == "sendMessage":
                send_started.set()
                await release_send.wait()
                return {}
            return {"ok": True, "result": {}}

        with patch.object(MOD, "_api_call", fake), patch.object(MOD, "_START_DELAY_SECONDS", 0):
            ctx = {"platform": "telegram", "session_id": "failed-send", "chat_id": "301"}
            await MOD.handle("agent:start", ctx)
            await asyncio.wait_for(send_started.wait(), timeout=1)
            state = MOD._RUNS["failed-send"]
            await MOD.handle("agent:end", ctx)
            release_send.set()
            await asyncio.sleep(0.05)

        self.assertNotIn("failed-send", MOD._RUNS)
        self.assertTrue(state.stale_task.done())

    async def test_cancelled_replacement_during_previous_delete_retires_both_states(self):
        previous = MOD.RunState(
            run_id="cancel-delete-old",
            session_id="cancel-delete",
            chat_id="313",
            message_id="801",
        )
        MOD._RUNS[previous.session_id] = previous
        previous.stale_task = asyncio.create_task(asyncio.sleep(60))
        delete_started = asyncio.Event()
        block_delete = asyncio.Event()

        async def blocked_delete(state):
            if state is previous:
                delete_started.set()
                await block_delete.wait()

        with patch.object(MOD, "_delete", blocked_delete):
            ctx = {"platform": "telegram", "session_id": "cancel-delete", "chat_id": "313"}
            start_call = asyncio.create_task(MOD.handle("agent:start", ctx))
            await asyncio.wait_for(delete_started.wait(), timeout=1)
            new_state = MOD._RUNS["cancel-delete"]
            start_call.cancel()
            await asyncio.gather(start_call, return_exceptions=True)
            block_delete.set()
            await asyncio.sleep(0.05)

        for state in (previous, new_state):
            retirement = getattr(state, "retirement_task", None)
            if retirement is not None:
                await asyncio.shield(retirement)
        self.assertNotIn("cancel-delete", MOD._RUNS)
        self.assertTrue(previous.stale_task.done())

    async def test_cancelled_replacement_awaiting_previous_retirement_retires_new_state(self):
        previous = MOD.RunState(
            run_id="cancel-retire-old",
            session_id="cancel-retire-start",
            chat_id="314",
        )
        MOD._RUNS[previous.session_id] = previous
        retirement_started = asyncio.Event()
        release_retirement = asyncio.Event()
        original_perform = MOD._perform_retirement

        async def blocked_perform(state, preserve, initiator):
            if state is previous:
                retirement_started.set()
                await release_retirement.wait()
            await original_perform(state, preserve, initiator)

        with patch.object(MOD, "_perform_retirement", blocked_perform):
            ctx = {"platform": "telegram", "session_id": "cancel-retire-start", "chat_id": "314"}
            start_call = asyncio.create_task(MOD.handle("agent:start", ctx))
            await asyncio.wait_for(retirement_started.wait(), timeout=1)
            new_state = MOD._RUNS["cancel-retire-start"]
            start_call.cancel()
            await asyncio.gather(start_call, return_exceptions=True)
            release_retirement.set()
            await asyncio.sleep(0.05)

        for state in (previous, new_state):
            retirement = getattr(state, "retirement_task", None)
            if retirement is not None:
                await asyncio.shield(retirement)
        self.assertNotIn("cancel-retire-start", MOD._RUNS)

    async def test_replacement_start_does_not_spawn_tasks_after_new_state_ended(self):
        previous = MOD.RunState(
            run_id="previous",
            session_id="start-end-race",
            chat_id="309",
            message_id="701",
        )
        MOD._RUNS[previous.session_id] = previous
        delete_started = asyncio.Event()
        release_delete = asyncio.Event()

        async def blocked_delete(state):
            if state is previous:
                delete_started.set()
                await release_delete.wait()
                state.message_id = ""

        with (
            patch.object(MOD, "_delete", blocked_delete),
            patch.object(MOD, "_FINAL_CLEANUP_SECONDS", 0),
        ):
            ctx = {"platform": "telegram", "session_id": "start-end-race", "chat_id": "309"}
            start_call = asyncio.create_task(MOD.handle("agent:start", ctx))
            await asyncio.wait_for(delete_started.wait(), timeout=1)
            new_state = MOD._RUNS["start-end-race"]
            self.assertIsNot(new_state, previous)

            await MOD.handle("agent:end", ctx)
            await asyncio.sleep(0.02)
            release_delete.set()
            await start_call
            await asyncio.sleep(0.02)

        self.assertNotIn("start-end-race", MOD._RUNS)
        for task in (new_state.start_task, new_state.stale_task, new_state.heartbeat_task):
            self.assertTrue(task is None or task.done())

    async def test_delete_retries_transient_failures_before_retiring(self):
        delete_calls = 0

        async def fake(method, payload):
            nonlocal delete_calls
            if method == "deleteMessage":
                delete_calls += 1
                if delete_calls < 3:
                    return {}
                return {"ok": True, "result": True}
            return {"ok": True, "result": {}}

        state = MOD.RunState(
            run_id="delete-retry",
            session_id="delete-retry",
            chat_id="310",
            message_id="702",
        )
        MOD._RUNS[state.session_id] = state
        with (
            patch.object(MOD, "_api_call", fake),
            patch.object(MOD, "_DELETE_RETRY_SECONDS", 0),
            patch.object(MOD, "_FINAL_CLEANUP_SECONDS", 0),
        ):
            await MOD._finish_and_cleanup(state)

        self.assertEqual(delete_calls, 3)
        self.assertEqual(state.message_id, "")
        self.assertNotIn("delete-retry", MOD._RUNS)

    async def test_stale_cleanup_exception_always_retires_state(self):
        async def fake(method, payload):
            if method == "deleteMessage":
                raise RuntimeError("delete transport failed")
            return {"ok": True, "result": {}}

        state = MOD.RunState(
            run_id="stale-delete-error",
            session_id="stale-delete-error",
            chat_id="311",
            message_id="703",
        )
        MOD._RUNS[state.session_id] = state
        with (
            patch.object(MOD, "_api_call", fake),
            patch.object(MOD, "_DELETE_RETRY_SECONDS", 0),
            patch.object(MOD, "_STALE_CLEANUP_SECONDS", 0),
        ):
            state.stale_task = asyncio.create_task(MOD._stale_cleanup(state))
            await asyncio.gather(state.stale_task, return_exceptions=True)

        self.assertNotIn("stale-delete-error", MOD._RUNS)
        self.assertTrue(state.stale_task.done())

    async def test_replacement_does_not_orphan_inflight_start_message(self):
        first_started = asyncio.Event()
        release_first = asyncio.Event()
        calls = []
        send_count = 0

        async def fake(method, payload):
            nonlocal send_count
            calls.append((method, payload.copy()))
            if method == "sendMessage":
                send_count += 1
                if send_count == 1:
                    first_started.set()
                    await release_first.wait()
                    return {"ok": True, "result": {"message_id": 101}}
                return {"ok": True, "result": {"message_id": 102}}
            return {"ok": True, "result": {}}

        with patch.object(MOD, "_api_call", fake), patch.object(MOD, "_START_DELAY_SECONDS", 0):
            ctx = {"platform": "telegram", "session_id": "replace", "chat_id": "302"}
            await MOD.handle("agent:start", ctx)
            await asyncio.wait_for(first_started.wait(), timeout=1)
            first_state = MOD._RUNS["replace"]
            await MOD.handle("agent:start", ctx)
            second_state = MOD._RUNS["replace"]
            release_first.set()
            await asyncio.sleep(0.05)

        deleted_ids = [
            str(payload["message_id"])
            for method, payload in calls
            if method == "deleteMessage"
        ]
        self.assertIn("101", deleted_ids)
        self.assertIs(MOD._RUNS["replace"], second_state)
        self.assertTrue(first_state.stale_task.done())

    async def test_edits_are_serialized_and_final_stage_cannot_regress(self):
        first_edit_started = asyncio.Event()
        release_first_edit = asyncio.Event()
        edit_texts = []

        async def fake(method, payload):
            if method == "editMessageText":
                edit_texts.append(payload["text"])
                if len(edit_texts) == 1:
                    first_edit_started.set()
                    await release_first_edit.wait()
            return {"ok": True, "result": {}}

        state = MOD.RunState(run_id="r", session_id="serialize", chat_id="303", stage=4)
        state.message_id = "500"
        with patch.object(MOD, "_api_call", fake):
            heartbeat_edit = asyncio.create_task(MOD._edit(state, updated_at="12:00"))
            await asyncio.wait_for(first_edit_started.wait(), timeout=1)
            state.stage = 5
            final_edit = asyncio.create_task(MOD._edit(state))
            await asyncio.sleep(0.01)
            self.assertEqual(len(edit_texts), 1)
            release_first_edit.set()
            await asyncio.gather(heartbeat_edit, final_edit)

        self.assertIn("Этап 4/5", edit_texts[0])
        self.assertIn("Этап 5/5", edit_texts[-1])

    async def test_non_telegram_is_ignored(self):
        with patch.object(MOD, "_api_call") as api:
            await MOD.handle("agent:start", {"platform": "discord", "session_id": "s", "chat_id": "c"})
        api.assert_not_called()


if __name__ == "__main__":
    unittest.main()
