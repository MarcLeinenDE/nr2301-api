# Firewall and NAT recipes

Detailed reference: [`firewall`](../../api/firewall.md).

Firewall changes can expose management services or internal clients to the WAN. Read current state first, make the smallest evidenced change, read back, and restore.

Physical evidence:

- [`2026-09-14-firewall-nat-campaign.md`](../../evidence/physical/2026-09-14-firewall-nat-campaign.md)
- [`2026-09-14-webui-source-crawl.md`](../../evidence/physical/2026-09-14-webui-source-crawl.md)

## WebUI transport rule

The shipped common `ajaxHandler` defaults to `toStringData=true` and stringifies numeric values during JSON serialization. Only calls that explicitly pass `toStringData:false` retain native JSON numbers.

This distinction is part of the wire contract. In particular, IP-/port-filter indices and the port-filter disable value are strings on the wire even where the page source initially constructs numeric literals.

## Remote administration from WAN

Read `firewall/get_admin_from_wan`.

Shipped NR2301 WebUI write shape:

```json
{"admin_from_wan":{"admin_from_wan_enable":"1"}}
```

Use string `"1"` for enabled and `"0"` for disabled. The earlier physical flat candidates were rejected because they omitted the `admin_from_wan` wrapper.

The frontend treats `firewall.setting_response="OK"` as success. When this setting changes, the WebUI schedules `router/restart_web_server` after 600 ms, so management interruption is expected.

The nested shape is source-confirmed; complete a focused write/read-back/restore before treating that exact lifecycle as live verified.

> [!WARNING]
> Enabling WAN administration increases attack surface. Test only on the dedicated lab router and restore the original state.

## Respond to WAN ping

Read `firewall/get_ping_from_wan`.

WebUI write:

```json
{"ping_from_wan":{"ping_from_wan_enable":"1"}}
```

Use string `"1"` for enabled and `"0"` for disabled. Success is `firewall.setting_response="OK"`. The nested shape is source-confirmed and explains why earlier flat candidates failed.

## VPN passthrough

Read `firewall/fw_get_vpn_passthrough`.

Write with native JSON integers:

```json
{"pptp":1,"l2tp":1,"ipsec":1}
```

The WebUI explicitly uses `toStringData:false`. A physical campaign already confirmed same-state write, mutation, exact read-back, and restore with native integers; string-valued candidates returned `result=-3`.

## DMZ

- `firewall/fw_get_dmz_info` reads the stored destination.
- `firewall/fw_set_disable_info` uses `{ "dmz_disable": "0" }` for enabled and `"1"` for disabled; this lifecycle is live verified.
- `firewall/fw_edit_dmz_entry` writes `{ "dmz_dest_ip": "<IPv4>" }`.

The physical NR2301 WebUI comments that `fw_add_dmz_entry` is not implemented on the cpe.5g path and always uses `fw_edit_dmz_entry` for destination changes.

The current UI exposes no destination-clear/delete action: with DMZ off the field is disabled/restored to the stored value; with DMZ on an empty value fails validation. Keep clear/delete unresolved and do not promote related-device delete behavior.

## Port forwarding

Read `firewall/get_port_forward`, preserve current settings, write, read back, then restore.

Disabled:

```json
{"enable":0}
```

Enabled uses `toStringData:false`, so `enable` and `index` remain native integers:

```json
{
  "enable":1,
  "items":[
    {"index":0,"name":"example","mac":"02-00-00-00-00-01","local_port":"65500","wan_port":"65500"}
  ]
}
```

The WebUI iterates up to 10 slots. A 2026-09-14 physical campaign already confirmed a synthetic forwarding-rule lifecycle. Response `result` is endpoint-state-dependent; do not interpret it globally.

## Port triggering

Read `firewall/get_port_trigger`.

Disabled:

```json
{"enable":0}
```

Enabled uses `toStringData:false`; `enable` and `index` are native integers while port fields are strings:

```json
{
  "enable":1,
  "items":[
    {"index":0,"name":"SDK-PT-WEBUI","trigger_port":"65500","start_port":"65501","end_port":"65501"}
  ]
}
```

The page supports up to 10 slots, requires all textual fields for a populated row, and evaluates `result===0` as success. A prior same-state empty/getter-shaped write was live accepted; the non-empty item shape is source-confirmed and awaits focused physical lifecycle verification.

## URL filter

Use `get_url_filter` / `set_url_filter`. Setter uses `toStringData:false`:

```json
{"mode":"blacklist","black_items":[{"value":"example.invalid","index":0}]}
```

Whitelist uses `white_items`; disabled mode is `"disable"`.

A physical campaign confirmed a synthetic blacklist item and semantic cleanup. Verify item contents after restore instead of relying on raw list shape alone.

## IP and port filters

Available methods:

- `ww_read_ip_filter`
- `ww_edit_ip_filter`
- `ww_fw_set_disable_info`
- `ww_read_port_filter`
- `ww_edit_port_filter`
- `ww_fw_set_port_disable_info`
- `ww_read_switch_mode_state`
- `ww_read_switch_port_mode_state`

Enable/disable switches have already been physically mutated/read back/restored.

### Complete-list reads

IP:

```json
{"ww_ip_filter":{"list":["all"]}}
```

Port:

```json
{"ww_port_filter":{"list":["all"]}}
```

These are directly confirmed by the physical NR2301 WebUI source and were used by the residue check. Minimal `list: []` bodies are accepted too, but they are not the complete-list selector.

### IP-filter write shape

Switch:

```json
{"ww_ip_filter":{"ip_filter_disable":"0"}}
```

String `"0"` means enabled; `"1"` means disabled.

`ww_edit_ip_filter` receives 10 indexed slots. Because the page uses default `toStringData=true`, **index is a string on the wire**:

```json
{
  "ww_ip_filter": {
    "list": [
      {"ip":"203.0.113.77","index":"0"},
      {"ip":"0","index":"1"}
    ]
  }
}
```

Empty slots are string `"0"`. This closes the source-level schema gap; physically verify one non-empty lifecycle before promotion to live rule-write support.

### Port-filter write shape

The page source constructs `port_filter_disable` numerically, but default `toStringData=true` stringifies it. Actual wire form:

```json
{"ww_port_filter":{"port_filter_disable":"0"}}
```

String `"0"` means enabled; `"1"` means disabled.

`ww_edit_port_filter` receives 10 indexed slots. `index` is also a wire string:

```json
{
  "ww_port_filter": {
    "list": [
      {"port":"65500:65500","index":"0"},
      {"port":"0","index":"1"}
    ]
  }
}
```

Populated values use `"start:end"`; empty/incomplete slots use `"0"`. Again, physically verify one non-empty lifecycle before relying on `setting_response="OK"` alone.

## UPnP

Read: `firewall/ww_upnp_open_close_state`.

Write:

```json
{"ww_upnp":{"upnp_enable":"1"}}
```

or string `"0"`. A physical campaign already confirmed mutation, read-back, and restore. WPS and UPnP are independent controls on the tested firmware.

## Remaining focused live verification

The WebUI source crawl closed the shape gaps. The remaining useful physical checks are:

1. nested `set_admin_from_wan` same-state/mutation/read-back/restore, including expected web-server restart behavior
2. nested `set_ping_from_wan` same-state/mutation/read-back/restore
3. one non-empty 10-slot `ww_edit_ip_filter` lifecycle
4. one non-empty 10-slot `ww_edit_port_filter` lifecycle
5. one non-empty `set_port_trigger` lifecycle
6. DMZ destination clear/delete stays unresolved because the current NR2301 WebUI itself exposes no such action

Use these exact shipped wire shapes; do not resume speculative payload guessing.
