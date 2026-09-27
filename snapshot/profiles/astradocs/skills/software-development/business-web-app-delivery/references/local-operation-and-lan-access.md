# Local operation and LAN-access runbook

Use this when an existing containerized business app must be brought back up or opened from another device on the same network.

## Bring-up sequence

1. Inspect the project README and Compose file before choosing a startup command.
2. Query `docker compose ps`. If the Docker engine is unavailable on a Windows desktop, start Docker Desktop, then poll `docker info` until it succeeds; do not repeatedly run Compose against a missing engine.
3. Run `docker compose up -d --build` (or the project-documented equivalent). If the shell runner classifies the command as long-lived, run it as a tracked background process and wait for its bounded completion.
4. Verify all required services with `docker compose ps`; require explicit healthy/running state.
5. Probe the health endpoint and representative unauthenticated routes. Treat an expected login redirect as success only when the redirect target is correct.

## LAN exposure checklist

A published container port alone is insufficient. Verify every layer:

1. Determine the host's active physical-LAN IPv4 address. Exclude VPN, Docker, WSL, Hyper-V, and tunnel adapters; prefer the adapter whose gateway belongs to the local router subnet.
2. Confirm Compose publishes the service on all host interfaces, e.g. `0.0.0.0:8000->8000/tcp`, rather than only `127.0.0.1`.
3. Add the exact LAN IP or an intentional subnet-aware host policy to the framework's allowed-host configuration. For Django, a LAN request returning HTTP 400 while localhost works is a strong signal to inspect `ALLOWED_HOSTS`.
4. Add the LAN origin (scheme, IP, and port) to trusted CSRF origins when the framework/application requires it for form submissions. Same-origin GET success does not prove POST/CSRF behavior.
5. Ensure an inbound firewall rule permits only the required TCP port. Prefer limiting profiles and remote subnet when practical; do not assume an unrelated existing rule is appropriate merely because it opens the same port.
6. Recreate/restart the web service so environment changes are loaded.
7. Probe the app through the LAN IP from the host, then, when possible, from a second device. Verify the expected status/redirect and a representative authenticated form submission.

## Secret-safe configuration inspection

Environment files often contain secrets. Never print or paste the whole file to inspect one host/origin setting. Parse and display only the specific non-secret keys needed. When editing, use a targeted replacement and ensure tooling/output does not echo neighboring secret-bearing lines. If a patch tool would expose context, use a secret-safe script that edits only the named key and reports the key name plus a boolean/change status, never the file contents.

## Operational caveats

- A DHCP-assigned IPv4 address may change. Recommend a router-side DHCP reservation for stable access.
- The host, Docker engine, and containers must remain running.
- Local HTTP is appropriate only for a trusted LAN. Do not present it as an Internet-exposure pattern; public access requires TLS, authentication review, reverse-proxy policy, and tighter firewall controls.
- A local curl to the LAN IP verifies host routing and application host policy, but not Wi-Fi client isolation or cross-device reachability. If a second device cannot connect, check AP/client isolation, guest-network separation, and subnet/firewall scope.
