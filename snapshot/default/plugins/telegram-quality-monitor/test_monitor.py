from __future__ import annotations

import asyncio
import os
import sqlite3
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

PLUGIN_DIR = Path(__file__).resolve().parent
if str(PLUGIN_DIR) not in sys.path:
    sys.path.insert(0, str(PLUGIN_DIR))

import monitor as qm  # noqa: E402


class TelegramQualityMonitorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old_home = os.environ.get("HERMES_HOME")
        self.old_channel = os.environ.get("TELEGRAM_HOME_CHANNEL")
        os.environ["HERMES_HOME"] = self.tmp.name
        os.environ["TELEGRAM_HOME_CHANNEL"] = "1001"
        qm._PRE_TURNS.clear()
        qm._discard_pending()

    def tearDown(self):
        if self.old_home is None:
            os.environ.pop("HERMES_HOME", None)
        else:
            os.environ["HERMES_HOME"] = self.old_home
        if self.old_channel is None:
            os.environ.pop("TELEGRAM_HOME_CHANNEL", None)
        else:
            os.environ["TELEGRAM_HOME_CHANNEL"] = self.old_channel
        self.tmp.cleanup()

    def settings(self, **overrides):
        values = qm.Settings(admin_chat_id="1001", admin_user_id="1001").__dict__.copy()
        values.update(overrides)
        return qm.Settings(**values)

    def test_redacts_common_secrets(self):
        bot = "123456789:abcdefghijklmnopqrstuvwxyzABCDE"
        openai = "sk-abcdefghijklmnopqrstuvwxyz"
        aws = "AKIAABCDEFGHIJKLMNOP"
        jwt = "eyJabcdefghijk.abcdefghijklmnop.qrstuvwxyzAB"
        text = f"token=abc1234567890 bot {bot} key {openai} aws {aws} jwt {jwt}"
        result = qm.redact(text)
        self.assertNotIn("abc1234567890", result)
        for secret in (bot, openai, aws, jwt):
            self.assertNotIn(secret, result)
        self.assertIn("[REDACTED]", result)

    def test_admin_turn_is_excluded(self):
        settings = self.settings(exclude_admin=True)
        qm.remember_pre_turn(platform="telegram", turn_id="t1", sender_id="1001", session_id="s1")
        with patch.object(qm, "ensure_worker"):
            qm.enqueue_completed_turn(
                platform="telegram",
                turn_id="t1",
                session_id="s1",
                user_message="hello",
                assistant_response="world",
            )
        conn = qm._connect()
        try:
            qm._persist_pending(conn, settings)
            count = conn.execute("SELECT COUNT(*) FROM turns").fetchone()[0]
        finally:
            conn.close()
        self.assertEqual(count, 0)

    def test_completed_turn_is_deduplicated(self):
        settings = self.settings(exclude_admin=True)
        with patch.object(qm, "ensure_worker"):
            for _ in range(2):
                qm.remember_pre_turn(platform="telegram", turn_id="t2", sender_id="2002", session_id="s2")
                qm.enqueue_completed_turn(
                    platform="telegram",
                    turn_id="t2",
                    session_id="s2",
                    user_message="question",
                    assistant_response="answer",
                )
        conn = qm._connect()
        try:
            qm._persist_pending(conn, settings)
            rows = conn.execute("SELECT * FROM turns").fetchall()
        finally:
            conn.close()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["sender_id"], "2002")

    def test_report_shows_short_request_and_summarizes_long_request(self):
        settings = self.settings(short_message_chars=20)
        row_short = {
            "turn_id": "a",
            "session_id": "s",
            "sender_id": "2",
            "user_message": "short request",
            "created_at": time.time(),
        }
        report_short = qm.format_realtime_report(row_short, settings, "summary", "reply", [])
        self.assertIn("Запрос полностью", report_short)
        self.assertIn("short request", report_short)

        row_long = dict(row_short, turn_id="b", user_message="x" * 50)
        report_long = qm.format_realtime_report(row_long, settings, "compressed request", "reply", [])
        self.assertIn("Выжимка длинного запроса", report_long)
        self.assertIn("compressed request", report_long)
        self.assertNotIn("x" * 30, report_long)

    def test_queue_processing_sends_once_and_marks_sent(self):
        settings = self.settings()
        conn = qm._connect()
        try:
            conn.execute(
                "INSERT INTO turns(turn_id,session_id,sender_id,user_message,assistant_response,created_at,status) "
                "VALUES('t3','s3','2002','question','answer',?,'queued')",
                (time.time(),),
            )
            conn.commit()
            sent = []
            with patch.object(qm, "_summarize_turn", return_value=("qsum", "asum", [])), patch.object(
                qm, "_send_telegram", side_effect=lambda chat, msg: sent.append((chat, msg))
            ):
                self.assertTrue(qm._process_one(conn, settings))
                self.assertFalse(qm._process_one(conn, settings))
            row = conn.execute("SELECT * FROM turns WHERE turn_id='t3'").fetchone()
        finally:
            conn.close()
        self.assertEqual(row["status"], "sent")
        self.assertEqual(len(sent), 1)
        self.assertEqual(sent[0][0], "1001")

    def test_delivery_failure_is_retried(self):
        settings = self.settings()
        conn = qm._connect()
        try:
            conn.execute(
                "INSERT INTO turns(turn_id,session_id,sender_id,user_message,assistant_response,created_at,status) "
                "VALUES('t4','s4','2002','question','answer',?,'queued')",
                (time.time(),),
            )
            conn.commit()
            with patch.object(qm, "_summarize_turn", return_value=("qsum", "asum", [])), patch.object(
                qm, "_send_telegram", side_effect=RuntimeError("offline")
            ):
                self.assertTrue(qm._process_one(conn, settings))
            row = conn.execute("SELECT * FROM turns WHERE turn_id='t4'").fetchone()
        finally:
            conn.close()
        self.assertEqual(row["status"], "retry")
        self.assertGreater(row["next_attempt_at"], time.time())

    def test_error_only_sender_result_is_failure(self):
        with patch.object(qm, "_send_telegram_async", return_value={"error": "offline"}):
            with self.assertRaises(RuntimeError):
                qm._send_telegram("1001", "report")

    def test_dedicated_bot_token_is_required(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("TELEGRAM_QUALITY_MONITOR_BOT_TOKEN", None)
            with self.assertRaises(RuntimeError):
                asyncio.run(qm._send_telegram_async("1001", "report"))

    def test_dedicated_bot_token_is_used_for_delivery(self):
        sender = AsyncMock(return_value={"success": True})
        with patch.dict(os.environ, {"TELEGRAM_QUALITY_MONITOR_BOT_TOKEN": "test-dedicated-token"}), patch(
            "tools.send_message_tool._send_telegram", sender
        ):
            result = asyncio.run(qm._send_telegram_async("1001", "report"))
        self.assertTrue(result["success"])
        sender.assert_awaited_once_with(
            "test-dedicated-token", "1001", "report", disable_link_previews=True
        )

    def test_html_and_markdown_are_neutralized(self):
        value = qm._telegram_plain('<a href="https://bad">click</a> *bold* [x](y)')
        self.assertNotIn("<a ", value)
        self.assertNotIn("*bold*", value)
        self.assertNotIn("[x]", value)

    def test_invalid_numeric_settings_use_safe_defaults(self):
        with patch.object(qm, "_plugin_settings", return_value={
            "daily_digest_hour": "bad", "retention_days": None,
            "short_message_chars": "NaN",
        }):
            settings = qm.load_settings()
        self.assertEqual(settings.daily_digest_hour, 20)
        self.assertEqual(settings.retention_days, 30)
        self.assertEqual(settings.short_message_chars, 1200)

    def test_gateway_registration_starts_recovery_worker(self):
        ctx = unittest.mock.MagicMock()
        old_ctx = qm._CTX
        try:
            with patch.dict(os.environ, {"_HERMES_GATEWAY": "1"}), patch.object(qm, "ensure_worker") as start:
                qm.register(ctx)
                start.assert_called_once_with()
            ctx.register_auxiliary_task.assert_called_once()
            self.assertEqual(ctx.register_hook.call_count, 2)
        finally:
            qm._CTX = old_ctx

    def test_non_gateway_registration_arms_bounded_bootstrap(self):
        ctx = unittest.mock.MagicMock()
        old_ctx = qm._CTX
        try:
            with patch.dict(os.environ, {}, clear=False):
                os.environ.pop("_HERMES_GATEWAY", None)
                with patch.object(qm, "ensure_gateway_bootstrap") as bootstrap:
                    qm.register(ctx)
                    bootstrap.assert_called_once_with()
        finally:
            qm._CTX = old_ctx

    def test_retention_deletes_old_undigested_sent_even_when_disabled(self):
        settings = self.settings(retention_days=30, enabled=False, daily_digest_enabled=False)
        conn = qm._connect()
        try:
            old = time.time() - 31 * 86400
            recent = time.time()
            conn.executemany(
                "INSERT INTO turns(turn_id,session_id,sender_id,user_message,assistant_response,created_at,status) "
                "VALUES(?,?,?,?,?,?,?)",
                [
                    ("old-sent", "s", "2", "q", "a", old, "sent"),
                    ("old-queued", "s", "2", "q", "a", old, "queued"),
                    ("new-sent", "s", "2", "q", "a", recent, "sent"),
                ],
            )
            conn.commit()
            qm._maybe_cleanup_retention(conn, settings)
            ids = {row[0] for row in conn.execute("SELECT turn_id FROM turns")}
        finally:
            conn.close()
        self.assertNotIn("old-sent", ids)
        self.assertIn("old-queued", ids)
        self.assertIn("new-sent", ids)

    def test_recent_claim_is_not_recovered_but_expired_claim_is(self):
        conn = qm._connect()
        try:
            old_created = time.time() - 86400
            conn.execute(
                "INSERT INTO turns(turn_id,session_id,sender_id,user_message,assistant_response,created_at,status,claimed_at) "
                "VALUES('lease','s','2','q','a',?,'processing',?)",
                (old_created, time.time()),
            )
            conn.commit()
            qm._recover_stale_claims(conn)
            self.assertEqual(conn.execute("SELECT status FROM turns WHERE turn_id='lease'").fetchone()[0], "processing")
            conn.execute("UPDATE turns SET claimed_at=? WHERE turn_id='lease'", (time.time() - 601,))
            conn.commit()
            qm._recover_stale_claims(conn)
            self.assertEqual(conn.execute("SELECT status FROM turns WHERE turn_id='lease'").fetchone()[0], "retry")
        finally:
            conn.close()

    def test_late_retry_is_included_in_later_digest(self):
        settings = self.settings(daily_digest_hour=0)
        conn = qm._connect()
        old_ctx = qm._CTX
        qm._CTX = None
        try:
            now = time.time()
            conn.executemany(
                "INSERT INTO turns(turn_id,session_id,sender_id,user_message,assistant_response,created_at,status,request_summary,response_summary) "
                "VALUES(?,?,?,?,?,?,?,?,?)",
                [
                    ("late", "s", "2", "q1", "a1", now - 60, "retry", "q1", "a1"),
                    ("ready", "s", "2", "q2", "a2", now, "sent", "q2", "a2"),
                ],
            )
            conn.commit()
            with patch.object(qm, "_send_telegram"):
                qm._maybe_daily_digest(conn, settings)
                self.assertIsNotNone(conn.execute("SELECT digested_at FROM turns WHERE turn_id='ready'").fetchone()[0])
                self.assertIsNone(conn.execute("SELECT digested_at FROM turns WHERE turn_id='late'").fetchone()[0])
                conn.execute("UPDATE turns SET status='sent' WHERE turn_id='late'")
                conn.execute("DELETE FROM meta WHERE key='last_digest_date'")
                conn.commit()
                qm._maybe_daily_digest(conn, settings)
            self.assertIsNotNone(conn.execute("SELECT digested_at FROM turns WHERE turn_id='late'").fetchone()[0])
        finally:
            qm._CTX = old_ctx
            conn.close()

    def test_post_hook_does_not_wait_on_locked_database(self):
        lock_conn = qm._connect()
        try:
            lock_conn.execute("BEGIN IMMEDIATE")
            qm.remember_pre_turn(platform="telegram", turn_id="fast", sender_id="2002", session_id="s")
            started = time.perf_counter()
            with patch.object(qm, "ensure_worker"):
                qm.enqueue_completed_turn(
                    platform="telegram", turn_id="fast", session_id="s",
                    user_message="q", assistant_response="a",
                )
            elapsed = time.perf_counter() - started
        finally:
            lock_conn.rollback()
            lock_conn.close()
        self.assertLess(elapsed, 0.1)

    def test_digest_fallback_groups_users(self):
        rows = [
            {
                "sender_id": "2002",
                "request_summary": "Q1",
                "response_summary": "A1",
                "quality_flags": "[]",
            },
            {
                "sender_id": "2002",
                "request_summary": "Q2",
                "response_summary": "A2",
                "quality_flags": "[]",
            },
        ]
        old_ctx = qm._CTX
        qm._CTX = None
        try:
            report = qm._format_digest(rows)
        finally:
            qm._CTX = old_ctx
        self.assertIn("Обработано обращений: 2", report)
        self.assertIn("Пользователь 2002: 2 обращений", report)


if __name__ == "__main__":
    unittest.main()
