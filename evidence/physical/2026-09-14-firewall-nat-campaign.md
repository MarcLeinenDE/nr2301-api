# Firewall/NAT physical campaign — 2026-09-14

Device/firmware: dedicated NR2301 test router, ACIY.3, normal administrator session via `http://zyxel.home`.

This file records sanitized physical evidence only. No credentials, device identifiers, client inventory, real WAN/LAN addresses, or other sensitive values are included.

## Confirmed write contracts

### VPN passthrough

`firewall/fw_set_vpn_passthrough` requires native JSON integers for the three protocol states:

```json
{
  "pptp": 0,
  "l2tp": 1,
  "ipsec": 1
}
```

Each value is `0` or `1` as a JSON integer, not a string.

Physical round-2 evidence:

```text
VPN_INT_SAME_STATE_RESULT = 0
VPN_INT_WRITE_RESULT = 0
VPN_INT_READBACK = True
VPN_INT_RESTORE_RESULT = 0
VPN_INT_RESTORED = True
```

The earlier stringified-value candidate returned `result=-3` and did not change the getter state.

### Other confirmed campaign writes

The first campaign physically confirmed reversible mutation/read-back/restore for:

- `firewall/fw_set_disable_info` (`dmz_disable`)
- `firewall/ww_upnp_open_close`
- `firewall/ww_fw_set_disable_info` (IP-filter switch)
- `firewall/ww_fw_set_port_disable_info` (port-filter switch)
- `firewall/set_port_forward`

`firewall/set_port_trigger` also accepted the getter-shaped same-state object containing `enable` and `items`, but the tested router had an empty item list, so the rule-item schema remains unresolved.

## Full-list read selector for IP/port filters

Historical NR2301 project artifacts from 2026-08-24 use the following requests to retrieve the complete lists:

```json
{
  "ww_ip_filter": {
    "list": ["all"]
  }
}
```

and:

```json
{
  "ww_port_filter": {
    "list": ["all"]
  }
}
```

A 2026-09-08 probe also established that `list: []` is accepted by both endpoints, but that only proves an accepted request body; it must not be documented as the complete-list selector.

On 2026-09-14, a post-campaign residue check using `list: ["all"]` returned zero IP-filter entries and zero port-filter entries:

```text
IP_FILTER_ALL_READ_COUNT = 0
IP_FILTER_NONEMPTY_COUNT_BEFORE = 0
IP_FILTER_SYNTHETIC_MATCH_COUNT = 0
IP_FILTER_CLEANUP = NOT_NEEDED
PORT_FILTER_ALL_READ_COUNT = 0
PORT_FILTER_NONEMPTY_COUNT_BEFORE = 0
PORT_FILTER_SYNTHETIC_MATCH_COUNT = 0
PORT_FILTER_CLEANUP = NOT_NEEDED
FIREWALL_FILTER_RESIDUE_CLEANUP = PASS
```

## Unresolved / contradictory writes

### IP and port filter rule lists

Two source-backed simple-list candidates were tested while the respective filter switch was enabled. The firmware returned `setting_response='OK'`, but subsequent full-list read-back did not contain the synthetic test rule. A later `list: ["all"]` residue check also returned zero entries.

Therefore `setting_response='OK'` alone is not sufficient success evidence for `ww_edit_ip_filter` or `ww_edit_port_filter`, and the exact non-empty rule write schema remains unresolved. Earlier documentation claiming a temporary rule had been live-added/read back cannot currently be tied to an exact retained request body and should not be used as protocol truth.

### Remote administration and WAN ping

For both `firewall/set_admin_from_wan` and `firewall/set_ping_from_wan`, the following same-state candidates were physically rejected with `setting_response='ERROR'`:

- string `"0"` / `"1"`
- native integer `0` / `1`

The exact write value/schema therefore remains unresolved even though the field names are statically known from the shipped frontend. Resolve by retained historical evidence or targeted NR2301 WebUI capture rather than additional guessing.

### DMZ destination clear/delete

A synthetic DMZ destination could be written and read back. Restoring the originally empty/no-destination state was not achieved through the tested guessed delete transports. DMZ itself was restored to `dmz_disable='1'` (disabled). The destination-clear contract is quarantined for targeted NR2301 WebUI capture; hardware reset remains the final recovery path.

### Port trigger item schema

The tested router reported:

```text
PORT_TRIGGER_ENABLE = 0
PORT_TRIGGER_ITEM_COUNT = 0
```

No NR2301 item schema could therefore be learned from read-back. This is quarantined for targeted WebUI capture.

## WebUI quarantine list

At the end of the larger test campaign, capture the real NR2301 WebUI requests for:

1. DMZ destination clear/delete
2. remote administration from WAN write
3. WAN ping write
4. IP-filter non-empty rule create/edit/delete
5. port-filter non-empty rule create/edit/delete
6. port-trigger rule create/edit/delete

Cross-device Zyxel/OEM findings may be used to formulate test hypotheses, but only NR2301 physical behavior is canonical.
