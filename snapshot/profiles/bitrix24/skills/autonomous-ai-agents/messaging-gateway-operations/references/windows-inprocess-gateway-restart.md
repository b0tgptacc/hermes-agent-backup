# Windows gateway restart from inside the gateway process

Use this when `hermes gateway restart` refuses because the caller is descended from the running gateway. The refusal is correct: an in-tree restart would kill its own command before it can start the replacement. A newly opened terminal can still inherit the same marker or relationship, so verify independence rather than assuming it.

## Validated fallback: one-shot Task Scheduler action

1. Discover the exact installed `hermes.exe` path.
2. Write a temporary `.cmd` that runs `hermes.exe gateway restart` and redirects output to a dedicated log.
3. Create and immediately run a one-shot task with `schtasks.exe`; Task Scheduler launches it outside the gateway process tree.
4. Under Git Bash, single-quote the `/TR` value so backslashes survive. An unquoted Windows path may be stored as `C:Users...` and fail.
5. Verify the task's last result is `0` and read the restart log.
6. Verify the old gateway drained cleanly, `hermes gateway status` reports a new PID, Telegram reconnects, and expected hooks load.
7. Delete the scheduled task and temporary script.

Example shape (substitute live paths):

```bash
schtasks.exe /Create /TN HermesGatewayRestartOnce \
  /TR 'cmd.exe /c C:\path\to\restart_gateway_once.cmd' \
  /SC ONCE /ST 23:59 /F
schtasks.exe /Run /TN HermesGatewayRestartOnce
schtasks.exe /Query /TN HermesGatewayRestartOnce /V /FO LIST
# verify restart log, new PID, Telegram connection, hooks
schtasks.exe /Delete /TN HermesGatewayRestartOnce /F
```

Do not claim success from `/Run` alone. The acceptance evidence is: task result `0`, clean gateway drain, new PID, Telegram connected, hooks loaded, and temporary artifacts removed.
