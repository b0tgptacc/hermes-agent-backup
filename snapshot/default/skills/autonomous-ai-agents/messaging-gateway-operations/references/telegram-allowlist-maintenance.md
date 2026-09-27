# Telegram allowlist maintenance

Use explicit numeric IDs and fail closed. Before choosing the write target, inspect both the config-backed list and the legacy `TELEGRAM_ALLOWED_USERS` value (without printing unrelated `.env` secrets). In Hermes authorization, a non-empty environment allowlist is evaluated before the config-backed `allow_from`; adding an ID only to config can therefore leave the user unauthorized.

- If `TELEGRAM_ALLOWED_USERS` is absent/empty, prefer the config-backed platform allowlist:

```bash
hermes config set gateway.platforms.telegram.allow_from '["existing-id","new-id"]'
```

- If `TELEGRAM_ALLOWED_USERS` is already populated, update it as the active source of truth or deliberately migrate every existing ID to config and remove the legacy value. Never leave two divergent lists. Preserve the union of all intentionally authorized IDs during reconciliation.

`hermes config set` replaces the whole list, so first preserve every existing authorized ID; never write only the new ID. Avoid enabling `TELEGRAM_ALLOW_ALL_USERS` or `GATEWAY_ALLOW_ALL_USERS` for agents with host tools.

After changing the allowlist:

1. Read back both `gateway.platforms.telegram.allow_from` and the effective `TELEGRAM_ALLOWED_USERS` value; confirm the complete expected set and that the target ID is in the source actually used by authorization.
2. Restart/reload the gateway.
3. Load the resolved gateway configuration and verify `PlatformConfig.extra.allow_from` contains the new ID and `typing_indicator`/other adjacent settings were not lost.
4. Verify the Telegram adapter reconnects.
5. Send a benign outbound probe to the target chat. `Chat not found` means the bot has no DM relationship with that ID (typically wrong ID, wrong bot, or the user has not pressed Start); it does not disprove the allowlist fix.
6. Treat a real inbound message from the new user as final authorization proof; an outbound `hermes send` bypasses inbound authorization.

Do not expose bot tokens while inspecting authorization state. User IDs are identifiers, not credentials, but still minimize unnecessary disclosure in normal responses.
