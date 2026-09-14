<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Physical NR2301 WebUI source crawl — 2026-09-14

Firmware: `V1.00(ACIY.3)C0` on the dedicated non-production NR2301.

Authenticated read-only source-driven crawl. Raw screenshots, rendered HTML and network logs remain private because they contain local device state. Raw evidence SHA-256: `09a7f72d942f6e0af2f49c9291072baa3b93fae65e30ac0f01e15ed59f60d942`.

Crawl summary:

- 39 routes discovered
- 36 routes browser-rendered
- 364 route/source links
- queue exhausted / complete
- no configuration mutation permitted by crawler

## Common WebUI transport rule

The shipped `ajaxHandler` defaults to `toStringData=true`. Its JSON serialization converts numeric values to strings unless a page explicitly passes `toStringData:false`.

This matters for exact wire modeling:

- IP-filter and port-filter pages use the default transport, so source numeric `index` values and the port-filter disable flag become strings on the wire.
- Port Forward, Port Trigger, URL Filter, and VPN Passthrough explicitly set `toStringData:false`; numeric fields on those pages remain native JSON integers.

The contracts below describe the **wire shape**, not merely the JavaScript source literal type.

## Remote administration and WAN ping

`html/firewall_remote.html` writes:

```json
{"ping_from_wan":{"ping_from_wan_enable":"0"}}
```

or `"1"` for `firewall/set_ping_from_wan`, and:

```json
{"admin_from_wan":{"admin_from_wan_enable":"0"}}
```

or `"1"` for `firewall/set_admin_from_wan`.

The earlier physical flat string/integer candidates were not the real WebUI body because they omitted the feature wrapper object. The frontend treats `firewall.setting_response == "OK"` as success. If admin-from-WAN changes, it schedules `router/restart_web_server` after 600 ms.

These exact nested shapes are source-confirmed but not yet physically mutated after discovery.

## IP filter

Complete read:

```json
{"ww_ip_filter":{"list":["all"]}}
```

Enable/disable:

```json
{"ww_ip_filter":{"ip_filter_disable":"0"}}
```

`"0"` = enabled, `"1"` = disabled.

`firewall/ww_edit_ip_filter` receives 10 indexed slots. Empty UI slots are `"0"`. Because the page uses default `toStringData=true`, `index` is a wire string:

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

This differs materially from the earlier sparse/simple-list guesses.

## Port filter

Complete read:

```json
{"ww_port_filter":{"list":["all"]}}
```

The source page constructs numeric `port_filter_disable`, but default `toStringData=true` makes the actual wire body:

```json
{"ww_port_filter":{"port_filter_disable":"0"}}
```

`"0"` = enabled, `"1"` = disabled.

`firewall/ww_edit_port_filter` receives 10 indexed slots. Populated values use `"start:end"`; empty/incomplete slots use `"0"`. `index` is also stringified on the wire:

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

## Port trigger

Getter: `firewall/get_port_trigger`.

Disabled:

```json
{"enable":0}
```

Enabled uses `toStringData:false`, so `enable` and `index` are native integers:

```json
{
  "enable":1,
  "items":[
    {"index":0,"name":"SDK-PT-WEBUI","trigger_port":"65500","start_port":"65501","end_port":"65501"}
  ]
}
```

The frontend iterates up to 10 slots, requires all textual fields for a populated row, and evaluates `result === 0` as success. Non-empty item shape is source-confirmed; earlier live same-state testing only proved the empty/getter-shaped form.

## Port forwarding

`firewall/set_port_forward` uses `toStringData:false`.

Disabled:

```json
{"enable":0}
```

Enabled:

```json
{
  "enable":1,
  "items":[
    {"index":0,"name":"example","mac":"02-00-00-00-00-01","local_port":"65500","wan_port":"65500"}
  ]
}
```

Port forwarding was already live-verified by the physical campaign.

## URL filter

`firewall/set_url_filter` uses `toStringData:false`, for example:

```json
{"mode":"blacklist","black_items":[{"value":"example.invalid","index":0}]}
```

Whitelist uses `white_items`; disabled mode is `"disable"`.

## UPnP

```json
{"ww_upnp":{"upnp_enable":"1"}}
```

or `"0"`. This matches the separately live-verified lifecycle.

## DMZ

Reads: `fw_get_disable_info`, `fw_get_dmz_info`, `router_get_lan_ip`.

Enable state:

```json
{"dmz_disable":"0"}
```

`"0"` = enabled, `"1"` = disabled.

Destination edit:

```json
{"dmz_dest_ip":"192.0.2.10"}
```

The current NR2301 frontend comments that `fw_add_dmz_entry` is not implemented on the cpe.5g path and always uses `fw_edit_dmz_entry`. The UI exposes no empty-destination clear/delete action, so DMZ clear/delete remains unresolved.

## VPN passthrough

The page uses `toStringData:false`, matching the already live-verified native-integer contract:

```json
{"pptp":1,"l2tp":1,"ipsec":1}
```

## Publication hygiene

No real password/session cookie, Wi-Fi key, subscriber identifier, local MAC/IP inventory, SMS content or other private runtime value from the raw crawl is included here.
