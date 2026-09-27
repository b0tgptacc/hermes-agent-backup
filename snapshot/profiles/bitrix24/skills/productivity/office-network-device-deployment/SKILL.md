---
name: office-network-device-deployment
description: "Use when deploying printers and office LAN devices."
version: 1.0.0
author: Hermes Curator
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [printers, scanners, ethernet, lan, office, deployment, security]
    category: productivity
---

# Office Network Device Deployment

Deploy printers, scanners, multifunction devices, and similar office appliances onto a shared LAN with verified addressing, secure administration, stable client configuration, and end-to-end functional tests.

## Core Principles

- Treat the exact model and regional manual as authoritative; closely related models can have different factory credentials and menus.
- Never infer or advertise a universal administrator password from another model family. Distinguish clearly between System Manager credentials, Remote UI access PINs, department/user credentials, and Wi-Fi credentials.
- A configured secret generally cannot be displayed in plaintext. Determine whether credentials are unset, user-configured, resettable from an authenticated panel, or service-only to recover.
- Prefer Ethernet to a router or managed switch for shared office use. A direct computer-to-device cable is appropriate only for an explicitly isolated single-host design.
- Prefer DHCP plus a router-side reservation. Use a manual device address only after checking the subnet, gateway, DHCP pool, exclusions, and conflicts.
- A successful web login is not a completed deployment. Verify printing, scanning, restart persistence, and access from the intended client population.

## Workflow

### 1. Establish scope and prerequisites

Identify:

- exact model and hardware/firmware variant;
- intended network segment or VLAN;
- router/switch port availability and whether the device should be isolated;
- client operating systems;
- required functions: print, duplex, color, scan-to-PC, scan-to-folder/email, fax, accounting;
- who owns router/DHCP and device-administrator credentials.

Do not ask the user for values that can be inspected safely from the host, device panel, router, or official documentation.

### 2. Inspect current state before changing anything

From an authorized client, record the active interface, subnet, gateway, routes, and neighbor/ARP table. Probe the local subnet only when authorized. Determine whether the device is already present and whether the expected Ethernet link exists.

If the device is absent, say so explicitly. Separate the physical prerequisite (connect cable, select wired mode, confirm link) from the later software configuration; do not claim remote configuration is possible before the device is reachable.

### 3. Research credentials precisely

Use the official manual for the exact series and region. Build a credential map:

| Credential | Purpose | Factory state | Recovery path |
|---|---|---|---|
| Administrator/System Manager ID and PIN | Protected settings | Verify exactly | Change/reset/service path |
| Web/Remote UI access PIN | Browser access | Verify exactly | Panel or authenticated admin path |
| Department/user credentials | Usage control | Usually user-created | Admin-managed |
| Wi-Fi key | Network association | External to device | Network owner |

Safe wording when documentation does not publish a fixed default: “No model-specific universal default was verified.” Do not substitute a common legacy value. If a manual says “if already set” or “if enabled,” treat that as evidence about optional configuration, not proof of a blank default unless the factory state is explicit.

Never expose a recovered secret in persistent memory, a reusable skill, or a normal report.

### 4. Establish wired connectivity

Typical sequence:

1. Connect CAT5e/CAT6 from the device to the intended router/switch port.
2. Select Wired LAN/Ethernet on the device panel if required.
3. Confirm link indication and wait for DHCP.
4. Read back IPv4 address, subnet mask, gateway, and wired MAC address from the panel or router.
5. Verify reachability from an intended client and open the exact device web interface.

If the address is `0.0.0.0`, link is absent or DHCP failed; diagnose cabling, switch/VLAN, and DHCP before touching client drivers.

### 5. Stabilize addressing

Recommended: create a DHCP reservation keyed to the wired MAC address, outside any conflicting static assignments. Then renew/restart the device and verify that the reserved address persists.

Manual static addressing is the fallback. Before setting it, verify the network prefix, gateway, DNS needs, DHCP pool, exclusions, and address vacancy. Never choose an address merely because it “looks free.”

Record a durable hostname where supported. Avoid client installations that depend only on transient discovery addresses.

### 6. Secure administration

- Set a unique administrator ID/PIN or password if the factory state is blank or weak.
- Set a separate Remote UI access control when the product supports one.
- Preserve credentials in the organization’s approved password manager, not in notes or chat.
- Enable TLS with a trusted or organization-managed certificate when practical.
- Update firmware from the official vendor channel.
- Disable unused services and wireless mode when wired-only operation is intended, but preserve protocols required by clients and scan workflows.
- Avoid factory reset unless its deletion scope is understood and backed up; initialization can remove address books, certificates, network settings, logs, and pending jobs.

### 7. Install clients predictably

Use the current official vendor driver and scan utility for the exact model and OS. For stable shared printing, prefer a vendor network port or Standard TCP/IP port bound to the reserved address/hostname over discovery-only WSD/AirPrint when the environment requires deterministic operation.

Configure defaults intentionally: paper size, duplex, color policy, accounting codes, and finishing options. For shared offices, consider centralized deployment through a print server, MDM, or Group Policy.

### 8. Verify end to end

Minimum acceptance tests:

- device responds at the reserved address;
- administrative web login works with the intended account;
- monochrome and color test pages print;
- duplex and paper-size defaults behave correctly;
- network scanning works in the required direction;
- the device remains reachable and clients still print after restart;
- another intended office client can use it;
- configuration or address-book backup is captured where supported.

Report each verified result separately from any untested recommendation.

## Failure Handling

- **Device not found:** verify power, cable, switch link, wired-mode selection, VLAN, DHCP lease, then subnet reachability—in that order.
- **Unknown administrator PIN:** do not brute-force or recycle defaults from other models. Use documented authenticated reset, vendor support, or an explicitly approved initialization after disclosing data loss.
- **Web UI works but printing fails:** inspect port type, firewall rules, driver/model mismatch, queue status, and supported print protocols.
- **Printing works but scanning fails:** verify the vendor scan utility, service discovery/firewall, destination permissions, and whether scan initiation is panel-to-PC or PC-to-device.
- **Address changes after restart:** fix DHCP reservation or correct the static configuration before reinstalling clients.

## References

- `references/canon-mf650-series.md` contains a model-specific Canon MF650-series example and official manual links. Use it only when that series matches; otherwise repeat the exact-model research.
