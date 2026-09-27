---
name: remote-agent-workstation-operations
description: "Use when a client UI drives an agent on another host."
version: 1.0.0
author: MASTER Curator
license: MIT
metadata:
  hermes:
    tags: [remote-agent, desktop, backend, files, vpn, workstation]
---

# Remote Agent Workstation Operations

## When to use

Use this skill when a desktop/TUI/web client should drive an agent runtime on another machine while sharing sessions, models, tools, or files. It covers LAN, VPN, SSH, and internet-reachable deployments, plus the split-filesystem problem where the agent executes on the backend but source files originate on the client.

## Core model

Keep four planes distinct:

1. **Client UI** — renders chat and selects local files.
2. **Agent backend** — owns sessions, profiles, models, memory, skills, approvals, and tool execution.
3. **Messaging gateway** — Telegram/Discord/etc.; normally a separate process from the desktop backend.
4. **File plane** — attachments, synchronized workspaces, Git, or network shares.

Never imply that connecting a remote UI automatically gives the backend transparent access to the client's filesystem, clipboard, applications, or screen.

## Workflow

1. Inspect the live product version and authoritative documentation before naming commands, flags, ports, auth methods, or UI labels.
2. Identify which host owns the runtime and which host owns the files. State where terminal/file/computer-use actions will execute.
3. Inspect current backend listeners, bind address, authentication readiness, firewall scope, and VPN availability without printing secrets.
4. Choose the narrowest safe transport:
   - trusted LAN only: bind to a specific LAN address, require authentication, and firewall to the private subnet;
   - LAN plus roaming: prefer a private overlay network such as Tailscale and bind to the overlay address;
   - SSH-capable hosts: use the product's managed SSH/tunnel mode when suitable;
   - public internet: require HTTPS plus OAuth/OIDC and a correctly configured reverse proxy; never expose an agent-control port with password-only auth.
5. Keep the backend durable under the host's service manager. Verify it survives logout/restart when persistence is part of the requirement.
6. Configure the client connection and test both HTTP readiness and the authenticated WebSocket/control channel. A public status endpoint alone is not proof that chat works.
7. Choose the file-plane pattern by workload:
   - one-off documents/images: client attachment upload;
   - persistent document workspace: a dedicated synchronized folder, with versioning;
   - source code: Git clone/commit/push/pull;
   - live single-copy files: a least-privilege network share over VPN only.
8. Isolate each user/customer/project into a dedicated folder and, when identity/state must differ, a dedicated profile. Never expose an entire user home or system drive by default.
9. Verify a real round trip: create or select a harmless client file, confirm the backend can read it, have the agent produce a small change/artifact, and confirm the expected result reaches the client.

## File-plane decision rules

### Attachment upload

Use for small, explicit inputs. Confirm that the client transfers bytes across the remote boundary and that the backend stages a copy in the session workspace. Explain that changes to the staged copy do not mutate the original client file automatically; output must be downloaded or returned as an attachment.

### Synchronized workspace

Default recommendation for recurring non-code work. Use a dedicated folder on both machines, bidirectional sync only when backend edits must return to the client, and enable file versioning. Avoid simultaneous editing of lock-sensitive Office files. Keep secrets and credential directories excluded.

### Git workspace

Default for code and text-based projects. Preserve history, review diffs, and use branches/commits rather than generic bidirectional file synchronization when concurrent edits are likely.

### Network share

Use only when one physical copy must remain on the client. Restrict the share to a dedicated folder and account. Prefer read-only access for analysis. Permit write access only when required. Carry SMB/NFS over LAN or VPN, never directly over the public internet. On Windows, mapped drive letters may be invisible to scheduled tasks or services; prefer a stable UNC path only if the runtime and shell support it, otherwise use synchronization.

## Security invariants

- The remote backend can execute tools with the backend host's privileges; access control must reflect that impact.
- Keep secrets on the backend. A remote client authenticates to the backend but should not receive provider tokens.
- Bind to a specific trusted interface where practical rather than every interface.
- Require authentication on every non-loopback bind.
- Use least-privilege file roots, allowlists, backups, and versioning.
- Do not open SMB or an unauthenticated agent-control port to the internet.
- Computer-use controls the backend host's interactive desktop unless a separate client-side worker is explicitly deployed.

## Verification checklist

- Backend process is running under the intended profile and user.
- Listener is bound only where intended.
- Authentication is required and the configured provider is advertised.
- Firewall/VPN policy allows the client and rejects unintended networks.
- Client passes the product's HTTP and WebSocket connection tests.
- A real chat turn completes against the remote backend.
- A client-originated file is staged/synchronized/mounted as designed.
- The backend reads it and returns or synchronizes a verified result.
- Messaging gateway status is checked separately when messaging is in scope.

## Product-specific references

- Hermes Desktop/backend and client-file details: `references/hermes-remote-desktop-files.md`.
