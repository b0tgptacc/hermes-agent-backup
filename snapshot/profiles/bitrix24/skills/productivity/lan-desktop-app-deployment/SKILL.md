---
name: lan-desktop-app-deployment
description: "Use when deploying LAN desktop apps."
version: 1.0.0
author: MASTER
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [deployment, lan, desktop-apps, office, screen-sharing, browser-receiver, windows, verification]
    category: productivity
---

# LAN Desktop App Deployment

Use this skill for rolling out lightweight desktop applications across office machines on a shared local network: screen-sharing tools, browser-based receivers, kiosk-style viewers, and similar utilities that are installed on some endpoints and opened from browsers on others.

This is not for printers, scanners, or traditional network appliances. It is for Windows/macOS/Linux desktop apps that need repeatable installation, local-network reachability, autostart, and end-to-end verification.

## When to use

- Deploy a screen-sharing receiver on one or more office PCs.
- Push a browser-accessible viewer app to laptop sources or central display hosts.
- Prepare a pilot package for manual installation on multiple machines.
- Verify that the app actually listens on the expected local port and is reachable from another machine.
- Build a repeatable uninstall path and a restart-safe launch path.

## Core principles

1. Prefer official installers and official release artifacts over third-party mirrors.
2. Treat the app's own runtime model as authoritative: per-user app, service, tray app, or browser server.
3. Separate installation from connectivity: a successful install is not a successful rollout.
4. Verify the exact local URL, port, and source/receiver roles before declaring success.
5. Capture limitations early, especially one-to-one vs one-to-many support.
6. Use local-network access only unless the user explicitly wants remote access.
7. If firewall changes are required, assume elevation may be needed and handle that as part of the deployment plan.

## Standard workflow

### 1. Pin the exact product and edition

Before writing scripts, confirm:

- product name and edition;
- OS family and architecture;
- installer type: MSI, EXE, DMG, AppImage, pkg, deb, rpm;
- whether the app installs per-user or system-wide;
- whether it needs an admin account or can run unelevated;
- the runtime port or local URL;
- whether the receiver side needs only a browser or also a client app;
- hard limits on concurrent connections.

If the product has a free/community tier, do not assume the community tier matches the paid tier's connection limits.

### 2. Collect the exact runtime facts

Record, from the official installer or docs when available:

- install path(s);
- executable name;
- uninstall method;
- startup mechanism;
- service vs tray vs user-session model;
- listening port(s);
- local URL format;
- firewall requirements;
- any required command-line flags (for example, fixed local IP or interface binding).

### 3. Build a repeatable deployment bundle

For Windows LAN rollouts, a useful bundle usually contains:

- the official installer artifact;
- a silent install script;
- a start script;
- a status/verification script;
- an uninstall script;
- a short operator README with the exact flow.

For each script, keep arguments explicit and log to a local file where possible.

### 4. Install safely

General Windows pattern:

- prefer `msiexec.exe /i <path> /qn /norestart` for MSI packages;
- quote file paths explicitly;
- if the app is installed per-user, expect the executable under `%LOCALAPPDATA%` rather than `Program Files`;
- if the app is launched with a local IP or interface flag, pass it explicitly so QR codes and links resolve correctly.

If the app is meant to auto-start for the current user, a Startup-folder shortcut is often the simplest reliable option.

### 5. Handle firewall and network access

- If the app listens on a fixed port, verify that the intended receiver network can reach it.
- Add an inbound rule only when needed and only for the intended profile/scope.
- If the user is not elevated, do not pretend the firewall rule was created; report that elevation is required.
- Prefer private/LAN scope over broad inbound exposure.

### 6. Verify end to end

Minimum verification for a screen-sharing or receiver app:

- installer completed successfully;
- executable exists in the expected path;
- app process is running;
- expected local port is listening;
- local URL opens in a browser on the same host;
- another machine on the LAN can reach the URL;
- the app shows the expected source/receiver role;
- the documented connection limit matches reality.

If the UI is browser-based, test the browser page itself, not just the service port.

## Common pitfalls

- Assuming the paid-tier limits are present in the free/community edition.
- Installing a receiver app on the wrong side of the workflow.
- Forgetting that the browser viewer may not work until the source app has launched first.
- Treating a listening port as proof that the stream works.
- Adding a firewall rule without elevation and assuming it succeeded.
- Launching with the wrong local IP, causing QR codes and URLs to point at an unreachable interface.
- Packaging a one-time pilot as if it were a general enterprise rollout.

## Verification commands and outputs

When possible, verify using the OS, not just the app UI:

- process list for the app name;
- port listen state;
- registry/uninstall entry on Windows;
- browser fetch of the local page;
- checksum for the installer artifact;
- a second-machine reachability test.

If the app advertises a local URL, record the actual URL produced on the machine where it runs.

## Example: browser-based screen sharing app

A common pattern for a browser-based receiver app is:

- source machine runs the desktop app;
- receiver machine uses only a browser;
- the source app listens on a fixed local port, such as 3131;
- the source app may offer a `--ip` or `--local-ip` flag to bind the advertised address;
- the source app may install per-user and place the executable under `%LOCALAPPDATA%`.

For a worked Windows example, see `references/deskreen-ce-deployment.md`.

## Notes on rollout style

For office deployments, prefer:

- a pilot on one source + one receiver first;
- then one standardized package per source machine;
- then a short operator instruction that states which side to open and what URL to use.

Keep source and receiver roles explicit in the documentation. In screen-sharing workflows, confusion usually comes from mixing up the machine that runs the stream with the machine that only opens the page.
