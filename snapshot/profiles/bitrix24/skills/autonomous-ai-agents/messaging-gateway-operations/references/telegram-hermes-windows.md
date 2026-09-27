# Telegram ingress to Hermes on Windows

This reference captures a verified setup path for routing Telegram bot messages into the active Hermes profile. It is operational detail under the broader messaging-gateway workflow, not a standalone Telegram skill.

## Architecture

Telegram Bot API → Hermes Messaging Gateway → active Hermes profile/session → agent tools → Telegram response.

A Telegram MCP is unnecessary for inbound routing. Native MCP tools, if configured for unrelated capabilities, are automatically available to gateway sessions through the platform toolset.

## Prerequisites and checks

```bash
hermes --version
hermes gateway --help
hermes gateway status
hermes doctor
```

On Windows Git Bash, identify the Hermes venv before installing into it:

```bash
which hermes
which python
python -c "import sys; print(sys.executable)"
```

If `python-telegram-bot` is missing and the Hermes venv has no `pip`, use `uv` against the exact interpreter rather than the unrelated system `pip`:

```bash
uv pip install --python 'C:/Users/admin/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe' 'python-telegram-bot[webhooks]==22.8'
```

Match the package version to the active Hermes release or its `pyproject.toml`; do not assume `22.8` remains current.

Verify:

```bash
python -c "import telegram; print(telegram.__version__)"
hermes doctor
```

## Durable startup on Windows

Install login startup without starting an unconfigured gateway:

```bash
hermes gateway install --no-start-now --start-on-login
```

Windows may request UAC for a Scheduled Task. If elevation is declined, Hermes can install a Startup-folder fallback. Confirm with:

```bash
hermes gateway status
```

Do not describe a stopped gateway as failed when it was intentionally installed with `--no-start-now`.

## User-owned credential binding

The user should create a bot with official `@BotFather`, obtain their numeric Telegram user ID from a trusted ID bot, then run locally:

```bash
hermes gateway setup
```

Select Telegram and enter:

- Bot API token from BotFather.
- Numeric owner/user ID for the allowlist.

Do not ask the user to paste the token into normal agent chat. Do not enable `TELEGRAM_ALLOW_ALL_USERS` or `GATEWAY_ALLOW_ALL_USERS` for an agent with host tools.

## Start and verify

```bash
hermes gateway start
hermes gateway status
```

Then send a real Telegram message to the bot and verify a reply. Dependency import and gateway process status alone are not end-to-end proof.

### E2E test hygiene

Use `/new` first or a dedicated test chat when the existing Telegram conversation is long-lived, near the model context limit, or has prior interrupted work. A one-word probe in a very large session can spend minutes compacting history and may resume stale in-flight context, so it is a poor health check.

Treat these as separate evidence checkpoints:

1. gateway log records the inbound update;
2. the agent produces a final response for that same turn;
3. the Telegram adapter records a successful send, not merely “sending”;
4. the user confirms the expected reply is visible.

`hermes send --to telegram ...` is useful for outbound credential/network verification, but it bypasses the inbound agent loop and cannot establish full E2E health by itself. If a test turn begins doing unrelated historical work, stop that turn safely, start a clean session, and rerun the probe rather than accepting the misleading result.

Useful Telegram commands after connection:

```text
/sethome
```

To move the current CLI transcript, enter this in the CLI session after a Telegram home channel exists:

```text
/handoff telegram
```

Without handoff, Telegram normally uses a separate session under the same Hermes profile, with the same SOUL, skills, memory configuration, and platform toolset.

## Groups

For ordinary group messages, Telegram privacy mode must be disabled in BotFather or the bot must be an administrator. After changing privacy mode, remove and re-add the bot where required. Keep explicit user/chat allowlists and prefer mention-required behavior in shared groups.

## Completion states

- **Prepared:** dependency and durable startup installed.
- **Configured:** token and allowlist saved locally.
- **Running:** gateway process and Telegram adapter connected.
- **Verified:** a real Telegram message produced a correct agent response.

Report the exact achieved state rather than collapsing all four into “done.”
