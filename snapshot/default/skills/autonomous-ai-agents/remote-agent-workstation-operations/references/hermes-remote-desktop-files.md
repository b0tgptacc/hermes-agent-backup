# Hermes remote Desktop and client files

This reference captures verified Hermes-specific behavior as of Hermes Agent 0.20.4 (August 2026). Re-check the live CLI and official docs before applying it to another version.

## Process boundaries

- `hermes serve` is the headless JSON-RPC/WebSocket backend used by Hermes Desktop and remote clients. Default: `127.0.0.1:9119`.
- `hermes dashboard` provides the same backend plus the web administration UI.
- `hermes gateway` is the separate messaging process for Telegram/Discord/etc. Desktop does not connect to the messaging gateway.
- One machine-level `serve` backend can expose the profiles installed on that host; profile selection remains backend-scoped.

Verify current flags with:

```text
hermes serve --help
hermes dashboard --help
```

Official docs:

- https://hermes-agent.nousresearch.com/docs/user-guide/desktop
- https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard
- https://hermes-agent.nousresearch.com/docs/user-guide/multi-connection-desktop

## Remote connection security

A non-loopback bind engages Hermes's authentication gate. The legacy `--insecure` flag is a no-op and must never be offered as a bypass.

- Trusted LAN or VPN: bundled username/password provider is acceptable. Store its username, password hash, and stable signing secret in the active Hermes `.env`; do not place secrets in `config.yaml`.
- Roaming clients: Tailscale is the simplest recommended transport. Bind `hermes serve` to the host's Tailscale IP and use that exact IP in Desktop so the listener and Host header agree.
- Public internet: HTTPS reverse proxy plus Nous Portal OAuth or self-hosted OIDC. Password-only public exposure is not acceptable.

A public `GET /api/status` response is only a readiness hint. Hermes Desktop chat also requires an authenticated WebSocket (`/api/ws`, and `/api/pty` where used). Use Desktop's connection test and complete a real turn.

## Desktop setup

In Hermes Desktop, open Settings -> Gateways -> Add connection -> Remote gateway. Enter the running `hermes serve` base URL, sign in using the backend's advertised provider, then Test and Save/Reconnect. UI wording may change, so prefer semantic labels rather than brittle click coordinates.

## Verified client attachment behavior

Hermes Desktop supports split filesystems. OS/Finder/Explorer drops are not left as absolute client paths that the remote host cannot read. The Desktop upload path transfers bytes and stages them in the session workspace:

- `uploadComposerAttachment()` chooses byte upload whenever the connection is remote.
- images use `image.attach_bytes`;
- ordinary files use `file.attach` with a data URL;
- the attachment is rewritten to a gateway-side reference before `prompt.submit`.

Implementation evidence in the 0.20.4 tree:

- `apps/desktop/src/app/chat/composer/hooks/use-composer-drop.ts`
- `apps/desktop/src/app/session/hooks/use-prompt-actions/index.ts`

Operational consequence: drag/drop is suitable for one-off files and images. It stages a copy on the backend. Editing that copy does not transparently update the original client file; return the result as a downloadable attachment or use a persistent file plane.

## Persistent client files

Choose one:

1. **Syncthing workspace (recommended for recurring documents):** client folder <-> dedicated backend folder. Enable versioning, exclude secrets, and avoid concurrent edits to Office files.
2. **Git (recommended for code):** clone on the backend, use branches/commits/push/pull, and review diffs.
3. **SMB/NFS over LAN or Tailscale (single-copy requirement):** expose only a dedicated folder through a dedicated least-privilege account. Prefer read-only for analysis. Never expose SMB publicly. Windows service/scheduled-task sessions may not see interactive mapped drive letters; synchronization is usually more reliable.

After synchronization, set the Hermes session/project cwd to the backend-side path, not the client path. File, terminal, and computer-use tools execute on the backend host.

## End-to-end verification

1. Attach or synchronize a harmless `test.txt` from the client.
2. Confirm the backend-side staged/synced path exists.
3. Ask the remote Hermes session to read it and append a unique test line.
4. For upload mode, download the resulting artifact and inspect it.
5. For sync/share mode, confirm the client-side file reflects the expected change.
6. Verify no unrelated client folders became visible.
