# Bitrix24 REST audit reference

Use this as a Bitrix24-specific companion to the class-level work-management audit workflow. Verify methods against the official Bitrix24 documentation MCP before relying on this snapshot because on-premise module versions can differ.

## Preferred architecture

- Hosted official documentation MCP: `https://mcp-dev.bitrix24.com/mcp`.
- Documentation MCP is for method discovery only; do not put company data in search prompts.
- Disable MCP sampling.
- Portal data access uses a dedicated incoming webhook or OAuth identity with the smallest module scopes.
- Module scopes do not provide method-level read-only enforcement. The client must enforce an exact method allowlist.

Useful read scopes for task/project/file audits commonly include:

```text
task, tasks, tasks_extended, im, disk,
user, department, sonet_group, socialnetwork
```

Select only what the approved scope needs.

## Method map

| Purpose | Preferred method | Notes |
|---|---|---|
| Current identity | `user.current` | Connectivity and effective identity check. |
| Tasks | `tasks.task.list` | Paginate all pages; request date/project/participant fields explicitly. |
| Task details | `tasks.task.get` | Use `select[]=*` plus `UF_TASK_WEBDAV_FILES` when supported. |
| Task history | `tasks.task.history.list` | Optional; can be expensive and is not required for every audit. |
| Task results | `tasks.task.result.list` | Check its `files` field separately. |
| Current task conversation | `im.dialog.messages.get` | Use task `chatId`, not task ID. Maximum page is typically 50; continue with `LAST_ID`. |
| Legacy comments | `task.commentitem.getlist` | Deprecated in newer tasks modules; use only as fallback/cross-check. |
| Direct attachment metadata | `disk.attachedObject.get` | Attachment ID is not always the same as a disk file ID. |
| Disk file metadata | `disk.file.get` | May return `ACCESS_DENIED` even when the task message is readable. |
| Chat file download | `im.v2.File.download` | One-time URL; may return `FILE_ACCESS_ERROR`. Do not retry permanently. |
| Project details | `socialnetwork.api.workgroup.get` | Object-level visibility still applies. |
| Legacy workgroups | `sonet_group.get` | Useful fallback on older/on-premise installations. |

## Active-during-period filtering

For a task active at any point in 2026:

1. Query candidates with `CREATED_DATE <= 2026-12-31T23:59:59`.
2. Client-side include when `closedDate` is missing or `closedDate >= 2026-01-01T00:00:00`.
3. Include missing-date records with an explicit warning rather than dropping them silently.

Do not filter only by creation date if the user intends to include older tasks that remained open.

## Task chat pagination

1. Read `chatId` from `tasks.task.get`.
2. Call `im.dialog.messages.get` with `DIALOG_ID=chat<chatId>` and `LIMIT=50`.
3. Collect messages by stable message ID.
4. For older pages, set `LAST_ID` to the smallest numeric ID from the prior page.
5. Stop on a short page, no IDs, or a non-decreasing boundary.
6. Deduplicate `(task_id, message_id)` after resumed runs.

System messages often have `author_id=0`. Keep them in the evidence corpus when relevant, but exclude them from semantic clustering to avoid labels dominated by timestamps, formatting keys, and status-change boilerplate.

## File recovery ladder

Check in this order:

1. `tasks.task.get` → `ufTaskWebdavFiles` for direct task attachments.
2. `im.dialog.messages.get` → message `params.FILE_ID` and response `files` map.
3. `im.v2.File.download` for a bounded chat-file download.
4. If chat-file resolution fails, call legacy `task.commentitem.getlist` and inspect `ATTACHED_OBJECTS`.
5. `tasks.task.result.list` → `files`; resolve these as attachment objects.

Keep these namespaces separate:

```text
task_id != chat_id != message_file_id != attachment_id != disk_file_id
```

`FILE_ACCESS_ERROR` and `ACCESS_DENIED` are terminal access outcomes. Record them once, then continue. They may reflect ACL gaps rather than missing files.

## Error handling

Retry:

- `QUERY_LIMIT_EXCEEDED`;
- operation-time limits explicitly documented as transient;
- network timeouts and temporary connection failures.

Do not retry:

- HTTP 400 with a parsed permanent API error;
- `ACCESS_DENIED`;
- `FILE_ACCESS_ERROR`;
- invalid method/parameter;
- insufficient scope.

Parse `HTTPError` bodies before the generic `URLError` branch; `HTTPError` is a subclass of `URLError`. Otherwise every permanent 400 can accidentally enter the transient retry loop.

## Resumable export notes

- Write task/message/file JSONL incrementally.
- Commit task terminal state atomically after all its subrecords.
- A killed run can append records before state commit, so normalized totals must dedupe.
- Task results are a separate file source; do not forget them.
- Record both raw attempt counts and deduplicated logical counts.

## Reporting limitations precisely

Say:

- “N unique files were downloaded and verified on disk.”
- “M file-reference attempts returned access errors.”

Do not convert M into “M unique missing physical files” unless identifiers were reconciled across current chat, legacy comment, attachment, and disk namespaces.
