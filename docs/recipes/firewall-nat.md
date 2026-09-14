# Firewall and NAT recipes

Detailed reference: [`firewall`](../../api/firewall.md).

Firewall changes can expose management services or internal clients to the WAN. Read the current state first and restore it if testing fails.

Physical campaign evidence: [`2026-09-14-firewall-nat-campaign.md`](../../evidence/physical/2026-09-14-firewall-nat-campaign.md).

## Remote administration from WAN

Read `firewall/get_admin_from_wan`.

The shipped frontend identifies `firewall/set_admin_from_wan` and the `admin_from_wan` field, but the exact write value/schema is currently unresolved on ACIY.3. Physical same-state candidates using both string `"0"`/`"1"` and native integer `0`/`1` returned `setting_response='ERROR'`.

Do not invent additional value encodings. Resolve this contract from retained evidence or a targeted capture of the real NR2301 WebUI action.

> [!WARNING]
> Enabling WAN administration increases attack surface. Do not enable it merely for API testing.

## Respond to WAN ping

Read `firewall/get_ping_from_wan`.

The shipped frontend identifies `firewall/set_ping_from_wan` and the `ping_from_wan` field, but the exact write value/schema is currently unresolved on ACIY.3. Physical same-state candidates using both string `"0"`/`"1"` and native integer `0`/`1` returned `setting_response='ERROR'`.

Resolve the write contract by targeted NR2301 WebUI capture rather than further guessed payloads.

## VPN passthrough

Read `firewall/fw_get_vpn_passthrough`, which reports PPTP, L2TP and IPsec state.

Write `firewall/fw_set_vpn_passthrough` with native JSON integer values:

```json
{
  "pptp": 1,
  "l2tp": 1,
  "ipsec": 1
}
```

Each field is `0` or `1` as a JSON integer. A 2026-09-14 physical campaign confirmed same-state write, mutation, exact getter read-back and restore with native integers. The otherwise identical string-valued candidate returned `result=-3` and did not mutate the state.

Preserve protocols you are not changing and verify with the getter.

## DMZ

- `firewall/fw_get_dmz_info` reads the stored DMZ destination.
- `firewall/fw_set_disable_info` controls the DMZ disable state through `dmz_disable` and was physically mutated/read back/restored successfully.
- `firewall/fw_edit_dmz_entry` accepts a destination write on the tested router.

The no-destination clear/delete contract remains unresolved. A test destination was left stored while DMZ itself was restored to `dmz_disable='1'` (disabled). Several guessed delete transports had no read-back effect. Do not continue guessing; capture the real NR2301 WebUI clear/delete action and use the physical reset button as final recovery if required.

## Port forwarding

1. GET `firewall/get_port_forward`.
2. Preserve the current settings/list.
3. Use `firewall/set_port_forward` with the exact frontend/current data structure.
4. GET `get_port_forward` again and verify the rule/list state.

A 2026-09-14 physical campaign successfully added a synthetic forwarding rule, read it back, cleared it and restored the initial state.

A notable response quirk from earlier live testing: `result=0` was observed while forwarding was enabled and `result=1` while disabled. Do not treat this field as a generic success/failure code without context.

## Port triggering

`get_port_trigger` returns a `settings` object containing at least `enable` and `items`. A same-state `set_port_trigger` call using that getter-shaped object returned `result=0` and round-tripped successfully on 2026-09-14.

The tested router had zero trigger items, so this does **not** define the rule-item schema. Rule create/edit/delete remains quarantined for targeted NR2301 WebUI capture.

## URL filter

Use `get_url_filter` / `set_url_filter`. The getter exposes mode plus black/white item collections.

A 2026-09-14 physical campaign confirmed a synthetic blacklist item could be written and read back. Cleanup required a two-step sequence: clear the item slots while `mode="blacklist"`, then restore `mode="disable"`. Sending the old empty list together with disabled mode did not remove the stored item.

Always verify semantic item contents after cleanup rather than comparing only raw list shape.

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

The enable/disable switches were physically mutated, read back and restored successfully on 2026-09-14.

### Read the complete rule lists

Use the full-list selector:

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

This request form is retained in historical NR2301 project artifacts from 2026-08-24 and was used again in the 2026-09-14 physical residue check. The router returned zero current entries for both lists.

A separate 2026-09-08 probe showed that the following minimal requests are also accepted:

```json
{
  "ww_ip_filter": {
    "list": []
  }
}
```

and:

```json
{
  "ww_port_filter": {
    "list": []
  }
}
```

Do **not** interpret `list: []` as the complete-list selector. It proves only that an empty-list request body is accepted.

### Non-empty list writes remain unresolved

Current source-backed simple-list candidates for `ww_edit_ip_filter` and `ww_edit_port_filter` returned `setting_response='OK'`, but a subsequent `list: ["all"]` read did not contain the synthetic rules. A later residue check also found zero entries.

Therefore `setting_response='OK'` alone is not success evidence for these rule-list writes. Earlier prose claiming temporary IP/port rules had been added/read back cannot currently be tied to a retained exact request body and must not be used as a normalized contract.

Capture create/edit/delete through the real NR2301 WebUI before documenting a non-empty write schema.

## UPnP

- read: `firewall/ww_upnp_open_close_state`
- write: `firewall/ww_upnp_open_close`

A 2026-09-14 physical campaign mutated UPnP, verified read-back and restored the original state. WPS and UPnP are separate controls on the tested firmware.

## Quarantined WebUI contracts

The following functions are intentionally queued for a targeted NR2301 WebUI network capture rather than further guessed API payloads:

1. DMZ destination clear/delete
2. remote administration from WAN write
3. WAN ping write
4. IP-filter non-empty rule create/edit/delete
5. port-filter non-empty rule create/edit/delete
6. port-trigger rule create/edit/delete

For each capture, record the real HTTP verb, endpoint/query, JSON or form body, relevant non-secret headers/session behavior and exact API read-back. Cross-device Zyxel/OEM implementations may guide hypotheses but are not canonical until physically confirmed on the NR2301.
