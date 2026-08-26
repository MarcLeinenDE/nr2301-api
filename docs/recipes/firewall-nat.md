# Firewall and NAT recipes

Detailed reference: [`firewall`](../../api/firewall.md).

Firewall changes can expose management services or internal clients to the WAN. Read the current state first and restore it if testing fails.

## Remote administration from WAN

Read `firewall/get_admin_from_wan`.

Write `firewall/set_admin_from_wan` with the `admin_from_wan` field, then read the state back.

> [!WARNING]
> Enabling WAN administration increases attack surface. Do not enable it merely for API testing.

## Respond to WAN ping

Read `firewall/get_ping_from_wan`.

Write `firewall/set_ping_from_wan` with the `ping_from_wan` field, then read back.

## VPN passthrough

Read `firewall/fw_get_vpn_passthrough`, which reports PPTP, L2TP and IPsec state.

Write `firewall/fw_set_vpn_passthrough` with:

```json
{
  "pptp": "CURRENT_OR_NEW_VALUE",
  "l2tp": "CURRENT_OR_NEW_VALUE",
  "ipsec": "CURRENT_OR_NEW_VALUE"
}
```

Preserve protocols you are not changing and verify with the getter.

## DMZ

- `firewall/fw_get_dmz_info` reads DMZ state.
- `firewall/fw_set_disable_info` controls the DMZ disable state through `dmz_disable`.
- `firewall/fw_edit_dmz_entry` carries `dmz_dest_ip` but remains `STATIC_CONFIRMED` / `DO_NOT_TEST_FOR_COVERAGE` in the current catalog.

Do not present `fw_edit_dmz_entry` as a live-verified setup recipe yet.

## Port forwarding

1. GET `firewall/get_port_forward`.
2. Preserve the current settings/list.
3. Use `firewall/set_port_forward` with the exact frontend/current data structure.
4. GET `get_port_forward` again and verify the rule/list state.

The setter is live verified transactionally, but its request body is not yet normalized in the public method contract. Do not invent a rule schema from the response alone.

A notable response quirk from live testing: `result=0` was observed while forwarding was enabled and `result=1` while disabled. Do not treat this field as a generic success/failure code without context.

## Port triggering

Use `get_port_trigger` / `set_port_trigger` with the same read-preserve-write-read principle. The setter's full request schema is not yet normalized publicly.

## URL filter

Use `get_url_filter` / `set_url_filter`. The getter exposes mode plus black/white item collections. Preserve the current structure when writing because the setter's complete request schema remains unnormalized.

## IP and port filters

The `ww_*` methods expose the lower-level filter list controls:

- `ww_read_ip_filter`
- `ww_edit_ip_filter`
- `ww_fw_set_disable_info`
- `ww_read_port_filter`
- `ww_edit_port_filter`
- `ww_fw_set_port_disable_info`
- `ww_read_switch_mode_state`
- `ww_read_switch_port_mode_state`

Temporary IP/port rules were live-added, read back and removed. Use documentation/test addresses for development and require exact list read-back before claiming success.

## UPnP

- read: `firewall/ww_upnp_open_close_state`
- write: `firewall/ww_upnp_open_close`

Read the state after changing it. WPS and UPnP are separate controls on the tested firmware; enabling WPS did not automatically enable UPnP.

## Complete namespace coverage

The firewall namespace also contains the DMZ methods and firewall-disable helpers listed above. Methods marked `DO_NOT_TEST_FOR_COVERAGE` remain reference-only rather than being converted into copy-paste action recipes.