# Firewall and NAT recipes

Detailed reference: [`firewall`](../../api/firewall.md).

Firewall changes can expose management services or internal clients to the WAN. Read the current state first and restore it if testing fails.

Physical campaign evidence:

- [`2026-09-14-firewall-nat-campaign.md`](../../evidence/physical/2026-09-14-firewall-nat-campaign.md)
- [`2026-09-14-webui-source-crawl.md`](../../evidence/physical/2026-09-14-webui-source-crawl.md)

## Remote administration from WAN

Read `firewall/get_admin_from_wan`.

The physical NR2301 WebUI source now establishes the exact shipped write shape:

```json
{
  "admin_from_wan": {
    "admin_from_wan_enable": "1"
  }
}
```

Use string `"1"` for enabled and `"0"` for disabled. The earlier physical flat string/integer candidates were rejected because they omitted the `admin_from_wan` wrapper object.

The frontend treats `firewall.setting_response="OK"` as success. When the admin-from-WAN value changes, the WebUI schedules `router/restart_web_server` after 600 ms, so a management interruption is expected.

This nested shape is source-confirmed from the shipped physical-device frontend but has not yet been physically mutated/read back after discovery. Preserve that distinction until the focused write test is complete.

> [!WARNING]
> Enabling WAN administration increases attack surface. Do not enable it merely for broad API coverage; use a deliberate reversible test and restore the original state.

## Respond to WAN ping

Read `firewall/get_ping_from_wan`.

The physical NR2301 WebUI source establishes:

```json
{
  "ping_from_wan": {
    "ping_from_wan_enable": "1"
  }
}
```

Use string `"1"` for enabled and `"0"` for disabled. The frontend treats `firewall.setting_response="OK"` as success.

As with WAN administration, this exact nested shape is source-confirmed; the earlier rejected physical candidates were flat values and therefore did not exercise the real WebUI request shape.

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

The later physical WebUI source crawl independently confirms the shipped page uses the same native integers with `toStringData:false`.

Preserve protocols you are not changing and verify with the getter.

## DMZ

- `firewall/fw_get_dmz_info` reads the stored DMZ destination.
- `firewall/fw_set_disable_info` controls DMZ enable state with top-level `dmz_disable`: string `"0"` means enabled and string `"1"` means disabled. This was physically mutated/read back/restored successfully.
- `firewall/fw_edit_dmz_entry` writes a changed destination as `{ "dmz_dest_ip": "<IPv4>" }`.

The physical NR2301 WebUI source explicitly comments that `fw_add_dmz_entry` is not implemented on the cpe.5g path and always uses `fw_edit_dmz_entry` for destination changes.

The no-destination clear/delete contract remains unresolved. The current NR2301 UI exposes no action that clears the stored destination: while DMZ is off the address input is disabled and restored to the current value; while it is on an empty value fails validation. Do not promote related-device delete behavior as canonical NR2301 behavior.

## Port forwarding

1. GET `firewall/get_port_forward`.
2. Preserve the current settings/list.
3. Use `firewall/set_port_forward` with the shipped object shape.
4. GET `get_port_forward` again and verify the rule/list state.

Disabled form:

```json
{
  "enable": 0
}
```

Enabled form uses native JSON values (`toStringData:false`) and up to 10 indexed slots:

```json
{
  "enable": 1,
  "items": [
    {
      "index": 0,
      "name": "example",
      "mac": "02-00-00-00-00-01",
      "local_port": "65500",
      "wan_port": "65500"
    }
  ]
}
```

A 2026-09-14 physical campaign successfully added a synthetic forwarding rule, read it back, cleared it and restored the initial state.

A notable response quirk from earlier live testing: `result=0` was observed while forwarding was enabled and `result=1` while disabled. Do not treat this field as a generic success/failure code without context.

## Port triggering

`get_port_trigger` returns a `settings` object containing at least `enable` and `items`.

Disabled form:

```json
{
  "enable": 0
}
```

The physical NR2301 WebUI source defines the previously missing rule-item schema. Enabled form uses `toStringData:false` and up to 10 indexed slots:

```json
{
  "enable": 1,
  "items": [
    {
      "index": 0,
      "name": "SDK-PT-WEBUI",
      "trigger_port": "65500",
      "start_port": "65501",
      "end_port": "65501"
    }
  ]
}
```

Each populated row requires all four textual fields. The frontend evaluates `result===0` as success.

A same-state `set_port_trigger` call using the getter-shaped empty object had already returned `result=0` and round-tripped successfully on 2026-09-14. The non-empty item schema above is source-confirmed and should be physically exercised with read-back/restore before being treated as live-verified rule creation.

## URL filter

Use `get_url_filter` / `set_url_filter`. The getter exposes mode plus black/white item collections.

The physical WebUI source confirms `set_url_filter` uses `toStringData:false`, for example:

```json
{
  "mode": "blacklist",
  "black_items": [
    {
      "value": "example.invalid",
      "index": 0
    }
  ]
}
```

Whitelist mode uses `white_items`; disabled mode is `"disable"`.

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

This request form is now directly confirmed by the shipped physical NR2301 WebUI source and was also used in the 2026-09-14 physical residue check. The router returned zero current entries for both lists.

A separate 2026-09-08 probe showed that minimal `list: []` requests are also accepted, but they are **not** the complete-list selector.

### IP-filter write shape

The WebUI enables/disables IP filtering with:

```json
{
  "ww_ip_filter": {
    "ip_filter_disable": "0"
  }
}
```

where string `"0"` means enabled and `"1"` means disabled.

When enabled, `ww_edit_ip_filter` receives 10 indexed slots. Empty UI slots are emitted as string `"0"`:

```json
{
  "ww_ip_filter": {
    "list": [
      {"ip": "203.0.113.77", "index": 0},
      {"ip": "0", "index": 1}
    ]
  }
}
```

This closes the source-level schema gap that caused earlier sparse/simple-list candidates to be inconclusive. A focused physical non-empty rule write/read-back/restore is still required before promoting that exact 10-slot non-empty lifecycle to live verification.

### Port-filter write shape

The WebUI enables/disables port filtering with a **native integer**:

```json
{
  "ww_port_filter": {
    "port_filter_disable": 0
  }
}
```

where `0` means enabled and `1` means disabled.

When enabled, `ww_edit_port_filter` receives 10 indexed slots. Populated entries use `"start:end"`; empty/incomplete slots use string `"0"`:

```json
{
  "ww_port_filter": {
    "list": [
      {"port": "65500:65500", "index": 0},
      {"port": "0", "index": 1}
    ]
  }
}
```

Again, the exact WebUI shape is source-confirmed; physically verify a non-empty rule lifecycle before relying on `setting_response="OK"` alone.

## UPnP

- read: `firewall/ww_upnp_open_close_state`
- write: `firewall/ww_upnp_open_close`

The shipped frontend writes:

```json
{
  "ww_upnp": {
    "upnp_enable": "1"
  }
}
```

or string `"0"`.

A 2026-09-14 physical campaign mutated UPnP, verified read-back and restored the original state. WPS and UPnP are separate controls on the tested firmware.

## Remaining focused live-verification work

The WebUI source crawl closed the request-shape gaps for WAN admin/ping, IP-filter list writes, port-filter list writes and port-trigger items. The following focused physical checks remain useful before production helper promotion:

1. nested `set_admin_from_wan` same-state/mutation/read-back/restore, including expected web-server restart behavior
2. nested `set_ping_from_wan` same-state/mutation/read-back/restore
3. one non-empty 10-slot `ww_edit_ip_filter` lifecycle
4. one non-empty 10-slot `ww_edit_port_filter` lifecycle
5. one non-empty `set_port_trigger` item lifecycle
6. DMZ destination clear/delete remains unresolved because the current NR2301 WebUI itself exposes no clear/delete action

Do not resume guessed payload probing for these now-source-defined contracts; use the exact shipped shapes above.
