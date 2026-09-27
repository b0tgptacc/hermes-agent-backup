# Multi-user gateway command approvals

Use this reference when a shared Telegram/Discord/Slack bot can execute shell commands or development workflows for multiple users.

## Verified default behavior

In an interactive gateway session, a shell command that reaches the approval gate is bound to the originating session and sent to that session's chat/thread. The agent execution blocks while waiting for a response.

For Telegram, the adapter renders inline choices such as:

- allow once;
- allow for the session;
- always allow;
- deny.

The callback handler verifies that the clicker is authorized for the platform/chat, then resolves the pending approval for that session. Authorization is not the same as administrative ownership: an allowlisted non-admin user can normally approve a command presented in their own chat.

The canonical approval timeout comes from `approvals.timeout` (commonly 300 seconds). No response is fail-closed: the command does not run. The agent may choose a lower-risk alternative or report the blocker.

Approval prompts are not automatically mirrored to the administrator. In a private DM, only the originating user normally sees the prompt. In a shared group/thread, another authorized participant who can see the buttons may be able to resolve it, depending on adapter authorization and chat policy.

## Scope differences that matter

- **Allow once** authorizes only that operation.
- **Session** affects the originating session.
- **Always** updates the profile-level command allowlist and can affect later sessions and other users sharing that profile.
- `approvals.mode: smart` is a risk classifier, not an admin-only approval policy.
- `approvals.mode: off`/YOLO removes prompts and is inappropriate for a shared host; hardline and explicit deny rules may still block catastrophic patterns.
- Shell-command approval does not imply that every file/tool action has the same approval path. Evaluate tool-specific side effects separately.

## Security conclusion

An explicit bot allowlist controls who may start sessions; it does not by itself create tenant isolation. If several users share one Hermes profile, OS identity, workspace, Docker daemon, command allowlist, and credentials, allowing each user to self-approve host commands lets them authorize effects on shared resources.

Treat the ability to approve as a privileged capability distinct from the ability to ask the bot questions.

## Recommended architecture

For ordinary users:

1. Execute development in a dedicated profile and isolated Docker/workspace with no unnecessary host mounts or shared credentials.
2. Auto-run only low-risk commands accepted by `smart` policy and explicit narrow allowlists.
3. Route uncertain or host-impacting approvals to a designated administrator, not the requester.
4. Show the requester only a neutral status such as “Требуется подтверждение администратора”. Do not expose raw commands, paths, secrets, or internal reasoning.
5. Restrict `Session` and especially `Always` decisions to administrators. Prefer one-time approval by default.
6. Keep timeout fail-closed and notify both requester and administrator of expiry without executing the command.
7. Record requester, session, redacted command, decision, approver, scope, and timestamp in an audit log.
8. Ensure an approval can resolve only the exact pending request/session; reject stale or already-resolved callbacks.

If the installed gateway has no built-in admin-only approver routing, do not imply that `smart` or an allowlist provides it. Implement a gateway adapter/plugin policy that separates `requester_id` from `approver_id`, or use separate user-facing and administrator approval bots. Verify the behavior end to end before enabling external users.

## Verification matrix

Test with one administrator and one ordinary allowlisted user:

1. Low-risk command runs without unnecessary prompting.
2. Risky command requested by the ordinary user is not self-approvable.
3. Approval appears only in the administrator destination.
4. Requester receives a nontechnical waiting status.
5. Admin allow-once executes exactly one pending command.
6. Admin deny blocks it and lets the agent adapt safely.
7. Timeout blocks execution.
8. A stale callback cannot execute anything.
9. Ordinary user cannot create profile-wide `Always` permission.
10. Approval for user A cannot resolve user B's session.
11. Shared group participants cannot approve merely because they can see the prompt.
12. Audit records contain redacted command metadata and no secrets.

## Operational reporting

When explaining current behavior, distinguish:

- observed configuration (`approvals.mode`, `approvals.timeout`);
- verified adapter/source behavior;
- deployment-specific assumptions (DM vs group, shared vs isolated profile);
- recommended target policy.

Do not claim administrator approval routing exists until a real non-admin request has been held, approved by the administrator, executed once, and read back from the intended target.