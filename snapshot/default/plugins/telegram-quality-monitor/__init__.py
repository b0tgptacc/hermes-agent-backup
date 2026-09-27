"""Telegram quality monitor plugin entry point."""
from .monitor import register

__all__ = ["register"]
