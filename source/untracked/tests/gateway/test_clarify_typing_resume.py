"""Regression coverage for typing around interactive clarify prompts."""

from unittest.mock import MagicMock

import pytest

from gateway.run import _typing_paused_for_interaction


def test_typing_resumes_after_clarify_answer():
    adapter = MagicMock()

    with _typing_paused_for_interaction(adapter, "chat-1"):
        adapter.pause_typing_for_chat.assert_called_once_with("chat-1")

    adapter.resume_typing_for_chat.assert_called_once_with("chat-1")


def test_typing_resumes_when_clarify_path_returns_or_raises():
    adapter = MagicMock()

    with pytest.raises(RuntimeError, match="prompt failed"):
        with _typing_paused_for_interaction(adapter, "chat-2"):
            raise RuntimeError("prompt failed")

    adapter.resume_typing_for_chat.assert_called_once_with("chat-2")
