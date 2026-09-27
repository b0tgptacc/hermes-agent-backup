# Open-source project landscape research

Use this workflow when comparing GitHub/GitLab projects that implement the same capability, especially networking, media, remote-access, or protocol stacks.

## Evidence model

For each project verify separately:

1. **Capability** — README/docs explicitly describe the required direction (sender, receiver, bidirectional), supported platforms, transport, control/input, and offline/LAN operation.
2. **Protocol vs transport** — distinguish application protocol (AirPlay, Miracast, WebRTC, VNC, ADB, GameStream) from bearer/network (Wi-Fi LAN, Wi-Fi Direct, Internet, Bluetooth). Discovery over Bluetooth does not prove the media stream uses Bluetooth.
3. **Product class** — label screen mirroring, second display, low-latency streaming, remote desktop, browser gateway, and fleet-management tools separately. Do not rank them as interchangeable.
4. **Maturity** — inspect latest commit/release, archive state, current build instructions, issue activity, and platform assumptions. Popularity is secondary.
5. **License** — inspect the actual LICENSE/LICENCE/COPYING file. Public source without an explicit OSI-style license is source-visible, not safely reusable open source.
6. **Security** — verify pairing/authentication, encryption, direct-LAN behavior, exposed ports, and whether remote access requires a relay/VPN. Treat project marketing claims as claims, not audits.

## Retrieval workflow

1. Start with the canonical repository and official documentation.
2. Extract README plus focused protocol/security/connection pages.
3. Check current activity without relying only on GitHub API metadata. If API rate limits interfere, use the repository's `commits/<branch>.atom` feed and parse the first entry timestamp/title deterministically.
4. Inspect raw license files (`LICENSE`, `LICENCE`, `COPYING`) rather than inferring from badges or third-party catalogs.
5. For each candidate record: source device/OS, receiver device/OS, media path, discovery path, router/internet requirements, control channel, codec/hardware acceleration, security caveats, license, and maintenance signal.
6. Maintain a decision table and an explicit rejected/legacy tier; do not clutter the main shortlist with infrastructure that only indirectly satisfies the use case.

## Wireless-screen-specific checks

- Ordinary IP software can work over Wi-Fi even if it is not "Wi-Fi-specific"; state whether Internet is unnecessary.
- Miracast normally means Wi-Fi Direct, not Bluetooth.
- A Bluetooth beacon, HID channel, or pairing mechanism is not a Bluetooth video transport.
- When evaluating Bluetooth-only claims, cite primary radio/link-rate specifications and inspect the actual codec/streaming implementation. A demo using MJPEG at low rate is not evidence of production-grade full-screen mirroring.
- Distinguish mirror mode from an independent second desktop; the latter often requires a virtual display/EDID adapter.
- Do not invent latency figures. Quote only project measurements and label them as project claims unless independently benchmarked.

## Output

Lead with the strongest scenario recommendations, then provide:

- a matrix of source → receiver, protocol/transport, control, security, and maturity;
- a strict conclusion for constrained transports such as Bluetooth;
- conditional/legacy alternatives and why they rank lower;
- direct canonical repository/documentation links;
- a dated snapshot because maintenance and compatibility change.

## Pitfalls

- Calling every remote-desktop or browser gateway a screen-streaming solution.
- Equating GitHub presence or star count with maturity.
- Calling source-visible code open source without a license.
- Treating discovery/control traffic as proof the video uses the same transport.
- Claiming that Wi-Fi requires Internet.
- Comparing measured latency from one project against unsourced guesses for another.
- Using a shared default citation ledger while parallel workers may reset or mutate it. Use a task-specific explicit ledger path for the final synthesis.