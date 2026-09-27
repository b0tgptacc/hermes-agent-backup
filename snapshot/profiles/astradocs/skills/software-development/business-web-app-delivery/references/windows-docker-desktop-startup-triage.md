# Windows Docker Desktop startup triage

Use this when a local CRM/ERP stack is already implemented but `docker compose up` cannot reach Docker Desktop on Windows.

## Separate platform failure from application failure

Before changing Compose files, images, volumes, or application data:

1. Run `docker version` or `docker info`.
2. If the client works but the daemon endpoint is unavailable, treat the incident as a Docker/WSL platform-startup failure—not a CRM failure.
3. Confirm the selected context with `docker context ls`.
4. Inspect WSL state with `wsl.exe --status` and `wsl.exe --list --verbose`.
5. Read the newest Docker Desktop backend log under `%LOCALAPPDATA%\Docker\log\host\` and identify the first engine-start failure, not later `_ping` timeouts.

Typical evidence includes a missing `dockerDesktopLinuxEngine` named pipe or Docker reporting that Desktop is unable to start. These symptoms prove that Compose has not yet reached the application stack.

## Safe response

- Do not run `docker compose down -v`, delete VHDX files, unregister WSL distributions, rebuild images, or edit the application merely because the daemon is unavailable.
- A non-destructive WSL shutdown/restart may be attempted, but verify success with `docker info`; do not present it as a universal fix.
- If recovery requires restarting `WslService` and the current session lacks elevation, stop at that boundary. Ask the operator to restart Windows or restart the service from an elevated terminal.
- After Docker reports a working server, run `docker compose up -d` and independently verify Compose health plus the application HTTP endpoint.

## Reporting

State clearly:

- the project path was found;
- whether the failure occurred before Compose contacted the daemon;
- the exact diagnosed subsystem (Docker Desktop/WSL versus the application);
- that volumes and application data were left untouched;
- the shortest operator action needed to continue.

Never claim the CRM is running until container state and the application health endpoint have both been read back successfully.
