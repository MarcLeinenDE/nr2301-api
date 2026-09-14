<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Physical NR2301 WebUI source crawl — 2026-09-14

Firmware under test: `V1.00(ACIY.3)C0` on the dedicated non-production NR2301.

This evidence was produced by an authenticated read-only source-driven WebUI crawl. Raw screenshots, rendered HTML and network logs remain private because they contain local device state. The sanitized raw-evidence bundle has SHA-256 `09a7f72d942f6e0af2f49c9291072baa3b93fae65e30ac0f01e15ed59f60d942`.

Crawl summary:

- 39 routes discovered
- 36 routes rendered in the browser
- 364 route/source links
- queue exhausted / complete crawl
- three engineering/missing routes retained as source-only/404 evidence
- no configuration mutation was permitted by the crawler

The shipped frontend source closes several previously quarantined Firewall/NAT request-shape gaps. These are **frontend/source-confirmed shapes** unless a separate physical write campaign already established live mutation/read-back/restore.

## Remote administration and WAN ping

`html/firewall_remote.html` uses:

```json
{
  "ping_from_wan": {
    "ping_from_wan_enable": "0"
  }
}
```

or `"1"` for `firewall/set_ping_from_wan`, and:

```json
{
  "admin_from_wan": {
    "admin_from_wan_enable": "0"
  }
}
```

or `"1"` for `firewall/set_admin_from_wan`.

This explains the earlier physical rejection of guessed flat string/integer payloads: the actual shipped frontend wraps each value in its feature object. The frontend treats `firewall.setting_response == "OK"` as success. If admin-from-WAN changes, it schedules `router/restart_web_server` after 600 ms.

The exact nested shapes above have not yet been physically mutated after discovery; retain the distinction between source confirmation and live write verification.

## IP filter

`html/firewall_ip.html` reads the complete list using a multicall member:

```json
{
  "ww_ip_filter": {
    "list": ["all"]
  }
}
```

The enable/disable write is:

```json
{
  "ww_ip_filter": {
    "ip_filter_disable": "0"
  }
}
```

where `"0"` means enabled and `"1"` means disabled.

When enabled, the frontend writes 10 indexed slots through `firewall/ww_edit_ip_filter`:

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

Empty UI slots are serialized as string `"0"`. This is materially different from the earlier sparse/synthetic list guesses and explains why `setting_response="OK"` alone did not establish a non-empty rule contract.

## Port filter

`html/firewall_port.html` reads the complete list with:

```json
{
  "ww_port_filter": {
    "list": ["all"]
  }
}
```

Enable/disable uses a native JSON integer:

```json
{
  "ww_port_filter": {
    "port_filter_disable": 0
  }
}
```

where `0` means enabled and `1` means disabled.

When enabled, `firewall/ww_edit_port_filter` receives 10 indexed slots. A populated slot is `"start:end"`; an empty/incomplete slot is `"0"`:

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

## Port trigger

`html/firewall_pt.html` confirms the item schema for `firewall/set_port_trigger`.

Disabled:

```json
{"enable": 0}
```

Enabled uses native JSON values (`toStringData:false`) and up to 10 indexed slots:

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

The frontend requires all four fields for a populated row and evaluates `result === 0` as success. The rule-item shape is source-confirmed; the earlier live same-state test only proved the getter-shaped empty-list form.

## Port forwarding

`html/firewall_pf.html` confirms the enabled object shape used by `firewall/set_port_forward` (`toStringData:false`):

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

Disabled form is `{ "enable": 0 }`. The frontend iterates 10 slots while enabled. Port forwarding itself was already live-verified by the physical campaign.

## URL filter

`html/firewall_url.html` confirms `firewall/set_url_filter` uses `toStringData:false` with mode plus the corresponding indexed item collection, for example:

```json
{
  "mode": "blacklist",
  "black_items": [
    {"value": "example.invalid", "index": 0}
  ]
}
```

Whitelist uses `white_items`; disabled mode is `"disable"`.

## UPnP

`html/firewall_upnp.html` writes:

```json
{
  "ww_upnp": {
    "upnp_enable": "1"
  }
}
```

or `"0"`. These are string values. This matches the separately live-verified UPnP lifecycle.

## DMZ

`html/firewall_dmz.html` reads `fw_get_disable_info`, `fw_get_dmz_info` and `router_get_lan_ip`.

Enable state write:

```json
{"dmz_disable": "0"}
```

where `"0"` means enabled and `"1"` means disabled.

A changed destination is written with `firewall/fw_edit_dmz_entry`:

```json
{"dmz_dest_ip": "192.0.2.10"}
```

The current NR2301 frontend contains a source comment that `fw_add_dmz_entry` is not implemented on the cpe.5g path and therefore always uses `fw_edit_dmz_entry`. The UI exposes no empty-destination clear/delete action. Consequently, the no-destination clear/delete contract remains unresolved and related-device delete behavior must not be promoted as canonical NR2301 behavior.

## VPN passthrough

`html/set_vpn_passthrough.html` confirms the already live-verified native-integer request and `toStringData:false`:

```json
{"pptp": 1, "l2tp": 1, "ipsec": 1}
```

## Publication hygiene

No real password/session cookie, Wi-Fi key, subscriber identifier, local MAC/IP inventory, SMS content or other private runtime value from the raw crawl is included in this evidence file.
