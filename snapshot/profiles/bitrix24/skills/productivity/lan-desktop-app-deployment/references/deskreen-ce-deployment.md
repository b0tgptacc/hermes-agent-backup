# Deskreen CE Windows deployment notes

Session-tested facts from the Deskreen CE rollout.

## Verified artifact
- Official release: pavlobu/deskreen v3.2.16 (published 2026-07-08).
- Windows x64 installer used: `deskreen-ce-3.2.16-x64.msi`.
- GitHub API release asset digest for the MSI: `sha256:de6052a0d5dc893e0d16da6a8da82aacae5803602a3efdde50037b536e3213f8`.

## Verified Windows install behavior
- MSI installs successfully with `msiexec.exe /i <path> /qn /norestart`.
- Installed executable path: `%LOCALAPPDATA%\Programs\deskreen-ce\Deskreen CE.exe`.
- Uninstall entry: `Deskreen CE` in standard Windows uninstall registry.
- Displayed version after install: `3.2.16.0`.

## Verified runtime behavior
- The app listens on TCP port `3131`.
- The local browser page is reachable at `http://<host-ip>:3131/`.
- The app responds to a launch argument that fixes the advertised local IP: `--ip <address>`.
- A Startup-folder shortcut works for per-user autostart.

## Operational caveats
- Community Edition is limited to one connected device at a time; do not promise one source simultaneously on two receivers.
- **Deskreen CE 3.2.16 has a localized-interface detection bug on Windows.** `isWifiConnected()` accepts only a hard-coded list/prefixes such as `Wi-Fi`, `WLAN`, and `Ethernet`. A real Russian Windows Wi-Fi alias such as `Беспроводная сеть` is rejected even while it has a valid IPv4 address, producing an endless `No WiFi and LAN connection` dialog. The `--ip` flag does not bypass this check because it is only consulted by the local-IP IPC handler, not by `isWifiConnected()`.
- Verified diagnostic: compare `os.networkInterfaces()`/`Get-NetIPAddress` aliases against the allowlist in `src/main/helpers/getMyLocalIpV4.ts`; a listening port 3131 does not prove the desktop UI passed the connectivity gate.
- Signed-build workaround: with explicit admin approval, rename the active physical Wi-Fi adapter to `Wi-Fi` (record interface GUID and old name first, and provide a restore path). Re-run the app and verify the modal closes. A custom source patch can remove the name allowlist but produces an unsigned build and should not silently replace the official artifact.
- Creating an inbound firewall rule on Windows requires elevation; without admin rights the script should warn and continue rather than pretending the rule was created.
- The source host's local IP should be recorded explicitly before generating the operator URL.

## Working file paths from the rollout
- `C:\Users\admin\Desktop\Deskreen-CE-Deployment\Files\deskreen-ce-3.2.16-x64.msi`
- `C:\Users\admin\Desktop\Deskreen-CE-Deployment\Scripts\install-deskreen-ce.ps1`
- `C:\Users\admin\Desktop\Deskreen-CE-Deployment\Scripts\check-deskreen-ce.ps1`
- `C:\Users\admin\Desktop\Deskreen-CE-Deployment\Scripts\start-deskreen-ce.ps1`
- `C:\Users\admin\Desktop\Deskreen-CE-Deployment\Scripts\uninstall-deskreen-ce.ps1`
- `C:\Users\admin\Desktop\Deskreen-CE-Deployment\Docs\README.md`
