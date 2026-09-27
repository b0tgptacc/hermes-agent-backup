---
name: messaging-gateway-operations
description: "Use when connecting chat platforms to an agent gateway."
version: 1.0.0
author: MASTER
license: MIT
metadata:
  hermes:
    tags: [messaging, gateway, telegram, discord, slack, operations]
---

# Messaging Gateway Operations

## When to Use

Use this skill when a user wants messages from Telegram, Discord, Slack, or another chat platform to reach an agent and receive executed results. It also applies when a request incorrectly describes inbound chat routing as an MCP or skill installation.

## Core distinction

Do not confuse three different extension mechanisms:

- **Messaging gateway adapter:** receives inbound chat messages and routes them into agent sessions. This is the correct layer for Telegram/Discord/Slack ingress.
- **MCP server:** exposes tools that the agent can call. It does not normally provide inbound chat routing.
- **Skill:** procedural guidance loaded into the prompt. A skill by itself does not open a network connection or receive messages.

When the real objective is inbound messaging, prefer the platform's built-in gateway adapter over adding a third-party MCP or a narrow platform skill. Explain the correction briefly, then implement the correct layer.

## Workflow

1. Resolve every named component before acting. Inspect the active profile and authoritative platform documentation; when the user says a generic adjacent name such as “dashboard,” check the live path/service and relevant recent session context before assuming they mean Hermes’ built-in surface. Prefer the user’s existing custom service when evidence identifies one, and avoid launching a same-named extra service by mistake.
2. Check gateway status, adapter dependencies, and whether credentials are already configured without printing secret values.
3. Install only the platform dependency required by the active Hermes environment.
4. Configure durable gateway startup appropriate to the operating system, but do not invent or request secrets in normal chat.
5. Leave token and owner-ID entry to a local interactive setup wizard or credential store.
6. Use an explicit user allowlist. Never enable global public access by default when the agent has terminal, file, browser, or automation tools.
7. Start the gateway only after credentials are present.
8. Set and verify per-platform output policy separately from tool capability. For a final-answer-only Telegram bot, explicitly disable both `tool_progress` and `interim_assistant_messages`; global display values override built-in platform defaults unless a platform override is present. When users need a visible long-task signal, keep technical surfaces disabled and add one editable, delayed, semantic progress status instead; see `references/telegram-user-progress.md`.
9. When administrator telemetry must be isolated, use a second outbound-only bot with a distinct profile secret, no fallback to the conversational bot, and an explicit admin destination. Require the admin to send `/start`, then verify the complete hook-to-dedicated-bot path; see `references/admin-conversation-monitoring.md`.
10. For product-level Telegram progress, prefer a gateway lifecycle hook (`agent:start`, `agent:step`, `agent:end`) that edits one semantic status bubble. Delay the first bubble for fast turns, use monotonic explicitly-conditional stages, cap at 95% before final delivery, suppress technical tool/reasoning/interim surfaces with per-platform display overrides, rate-limit edits, and make all Telegram failures best-effort. Guard the `agent:end`/in-flight `sendMessage` race: cancelling an `asyncio.to_thread` await does not stop the worker; retain the task until it captures `message_id`, then delete any late bubble.
11. Verify dependency import/version, gateway status, adapter connection, resolved display values, hook load, race regression tests, and a real inbound test message.
12. Run E2E checks in a fresh or deliberately isolated platform session. Before sending a trivial probe into a long-lived production conversation, inspect its size/state; if it is near context compaction, start a clean session (`/new`) or use a dedicated test chat. Otherwise a harmless probe can trigger expensive compaction or revive stale in-flight context, making the gateway look slow or incorrect. Verify four distinct facts separately: inbound receipt, agent final-response creation, platform send attempt/success, and actual user-visible delivery. Process status or an outbound-only `send` command is not full E2E proof.
13. Explain session semantics: a platform usually creates a separate session under the same profile; use the platform handoff feature if the user wants the current CLI conversation transferred.

## Verification standard

Do not claim the integration is complete until a real message sent through the platform receives an agent response. If credentials are intentionally left for the user, report the state as "prerequisites installed; credential binding and end-to-end test pending."

## Security

- Keep bot tokens and signing secrets in the platform credential store or Hermes `.env`, never in skills, memory, generated documents, or normal responses.
- Prefer numeric user IDs and explicit chat/user allowlists over usernames or public access.
- If group privacy settings are changed, verify the platform-specific rejoin/admin requirements.
- Treat third-party MCP servers that request a bot token as untrusted until their code, permissions, and data flow have been reviewed.

## References

- `references/telegram-hermes-windows.md` — verified Telegram setup sequence for Hermes on Windows, including dependency installation, login-start fallback, allowlisting, and session handoff.
- `references/telegram-user-progress.md` — one-message, nontechnical, conditional progress stages for long Telegram tasks, with privacy, failure-handling, and verification rules.
- `references/admin-conversation-monitoring.md` — private administrator visibility into gateway conversations using observer hooks, summaries, delivery controls, privacy, and verification.
