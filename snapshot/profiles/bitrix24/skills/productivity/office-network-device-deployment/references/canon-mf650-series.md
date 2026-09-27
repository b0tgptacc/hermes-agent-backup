# Canon i-SENSYS MF650 Series Wired Office Example

Applies to the MF657Cdw / MF655Cdw / MF651Cw manual family. Confirm the exact model and regional firmware before using these paths.

## Credential model

Canon documents two separate controls:

- **System Manager ID and PIN** protect administrative settings such as Network and Management Settings. The manual instructs an administrator to set them and says to contact the dealer or service representative if the PIN is forgotten.
- **Remote UI Access PIN** is a common PIN controlling browser access. It can be set from the panel when management access is available.

The official MF650-series pages reviewed do not publish a fixed universal administrator ID/PIN. Do not present legacy Canon values such as `7654321` as defaults for this series without exact-model documentation. A configured PIN is not a “viewable password”; use the documented change, authenticated reset, support, or approved initialization path.

System Manager configuration path:

`Menu → Management Settings → User Management → System Manager Information Settings → System Manager ID and PIN`

Remote UI PIN path:

`Menu → Management Settings → License/Other or Remote UI Settings/Update Firmware → Remote UI Settings → Restrict Access`

## Wired LAN procedure

1. Connect the printer to the router or switch with a LAN cable.
2. Select:
   `Menu → Preferences → Network → Select Wired/Wireless LAN → Wired LAN`
3. Wait several minutes for automatic IP assignment.
4. Read IPv4 information:
   `Status Monitor → Network Information → IPv4`
5. Read the wired MAC address:
   `Menu → Preferences → Network → Ethernet Driver Settings`
6. Open Remote UI at `http://<printer-ip>/`.
7. Prefer a router-side DHCP reservation for the wired MAC. If entering IPv4 manually, verify the subnet, mask, gateway, DHCP scope, and vacancy first; restart the printer after applying.
8. Install the current Canon driver and scan utility from the official regional support site.

If the panel shows `0.0.0.0`, troubleshoot physical link and DHCP before installing clients.

## Verification checklist

- Ethernet/Wired LAN icon is present.
- IPv4 address, mask, gateway, and wired MAC are recorded.
- Remote UI opens from an intended office client.
- Address persists after printer restart.
- Official MF650 driver prints monochrome, color, and duplex test pages.
- MF Scan Utility or the required network scan path succeeds.
- Administrator and Remote UI credentials are stored in the approved password manager.

## Destructive recovery caution

`Initialize All Data/Settings` restores factory defaults and can delete network configuration, address-book data, certificates, logs, and pending documents. Use only after explaining the scope, backing up recoverable data, and obtaining explicit approval.

## Official sources

- Wired LAN: https://oip.manual.canon/USRMA-6625-zz-SSM-650-enGB/contents/devu-setup-nw-wirelan.html
- Select wired/wireless mode: https://oip.manual.canon/USRMA-6625-zz-SSM-650-enGB/contents/devu-setup-nw-wirelan_wlesslan.html
- IPv4 configuration: https://oip.manual.canon/USRMA-6625-zz-SSM-650-enGB/contents/devu-setup-nw-ip-ipv4.html
- View network settings: https://oip.manual.canon/USRMA-6625-zz-SSM-650-enGB/contents/devu-setup-nw-view_nw.html
- System Manager ID/PIN: https://oip.manual.canon/USRMA-6625-zz-SSM-650-enGB/contents/devu-mcn_mng-set_privileges-sysmng_id_pin.html
- Remote UI PIN: https://oip.manual.canon/USRMA-6625-zz-SSM-650-enGB/contents/devu-mcn_mng-set_privileges-rui_pin.html
- Start Remote UI: https://oip.manual.canon/USRMA-6625-zz-SSM-650-enGB/contents/devu-mcn_mng-rui-strt.html
- Drivers: https://oip.manual.canon/USRMA-6625-zz-SSM-650-enGB/contents/devu-setup-drv.html
- Initialization scope: https://oip.manual.canon/USRMA-6625-zz-SSM-650-enGB/contents/devu-mcn_mng-initialize_set.html
