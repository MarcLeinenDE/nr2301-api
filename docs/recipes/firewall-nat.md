# Firewall and NAT recipes

Detailed reference: [`firewall`](../../api/firewall.md).

Firewall changes can expose management services or internal clients to the WAN. Read current state first, make the smallest evidenced change, read back, and restore.

Physical evidence:

- [`2026-09-14-firewall-nat-campaign.md`](../../evidence/physical/2026-09-14-firewall-nat-campaign.md)
- [`2026-09-14-webui-source-crawl.md`](../../evidence/physical/2026-09-14-webui-source-crawl.md)
- [`2026-09-14-firewall-webui-live-verification.md`](../../evidence/physical/2026-09-14-firewall-webui-live-verification.md)

Machine-readable live-contract overlay:

- [`specification/firewall-live-contracts-2026-09-14.json`](../../specification/firewall-live-contracts-2026-09-14.json)

## Public-SDK reversible lifecycle status

On 2026-09-25 the public SDK completed the full reversible Firewall/NAT lifecycle
for 12 write helpers in one run. All write/read-back stages passed and the final
semantic snapshot was identical to the original configuration.

Result: `1 passed in 25.64s`.

The only remaining Firewall/NAT write helper outside this lifecycle is the DMZ
destination setter. It remains a separate destructive/recovery test because an
empty original destination has no verified API-level clear operation.

## Management recovery after write/restore sequences

A single immediate Firewall/NAT getter timeout is not sufficient evidence that
the preceding write failed. The 2026-09-21 public-SDK lifecycle completed all
12 reversible write/read-back stages, including URL Filter and UPnP, then hit a
5-second read timeout on `get_admin_from_wan` while taking the final
post-restore snapshot.

For transactional verification:

1. send each intended write once;
2. on a transport/protocol failure, retry the getter rather than repeating the
   write blindly;
3. allow a longer read timeout during recovery;
4. re-login if needed;
5. decide success only from eventual semantic read-back;
6. verify the full final snapshot after management becomes ready.

This broadens the earlier URL-filter-specific timeout observation into a
namespace-level management-readiness rule. It does not change any Firewall/NAT
wire contract.

## WebUI transport rule

The shipped common `ajaxHandler` defaults to `toStringData=true` and stringifies numeric values during JSON serialization. Only calls that explicitly pass `toStringData:false` retain native JSON numbers.

This distinction is part of the wire contract. In particular, IP-/port-filter indices and the port-filter disable value are strings on the wire even where the page source initially constructs numeric literals.

## Remote administration from WAN

Read `firewall/get_admin_from_wan`.

Live-verified write shape:

```json
{"admin_from_wan":{"admin_from_wan_enable":"1"}}
```

Use string `"1"` for enabled and `"0"` for disabled. A 2026-09-14 physical verifier confirmed same-state write, mutation, getter read-back, restore write and final getter restore. The earlier flat candidates were rejected because they omitted the `admin_from_wan` wrapper.

The setter returns `firewall.setting_response="OK"` on the verified path.

The stock WebUI additionally schedules `router/restart_web_server` after 600 ms when this value changes. That extra action was not required to verify the setter contract itself and was deliberately not invoked by the focused verifier.

> [!WARNING]
> Enabling WAN administration increases attack surface. Test only on the dedicated lab router and restore the original state.

## Respond to WAN ping

Read `firewall/get_ping_from_wan`.

Live-verified write shape:

```json
{"ping_from_wan":{"ping_from_wan_enable":"1"}}
```

Use string `"1"` for enabled and `"0"` for disabled. The focused physical verifier confirmed same-state write, mutation, getter read-back and restore, with `firewall.setting_response="OK"` for each successful write.

## VPN passthrough

Read `firewall/fw_get_vpn_passthrough`.

Write with native JSON integers:

```json
{"pptp":1,"l2tp":1,"ipsec":1}
```

The WebUI explicitly uses `toStringData:false`. A physical campaign confirmed same-state write, mutation, exact read-back, and restore with native integers; string-valued candidates returned `result=-3`.

## DMZ

- `firewall/fw_get_dmz_info` reads the stored destination.
- `firewall/fw_set_disable_info` uses `{ "dmz_disable": "0" }` for enabled and `"1"` for disabled; this lifecycle is live verified.
- `firewall/fw_edit_dmz_entry` writes `{ "dmz_dest_ip": "<IPv4>" }`.

The physical NR2301 WebUI comments that `fw_add_dmz_entry` is not implemented on the cpe.5g path and always uses `fw_edit_dmz_entry` for destination changes.

The current UI exposes no destination-clear/delete action: with DMZ off the field is disabled/restored to the stored getter value; with DMZ on an empty value fails validation. Importantly, the getter value is not guaranteed to be a valid IPv4 address: `192.168.` was physically observed on 2026-08-25 and again as the 2026-09-25 pre-test state. Therefore classify the original with an IPv4 parser, not by empty/non-empty text. A valid IPv4 may be restored through the verified setter and must be read back. An empty or invalid/sentinel-like original requires full configuration-backup restore after the mutation. Keep clear/delete unresolved and do not promote related-device delete behavior.

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
    {"index":0,"name":"example","mac":"02:00:00:00:00:01","local_port":"65500","wan_port":"65500"}
  ]
}
```

The NR2301 WebUI exposes **5 Port Forward slots** (indices 0..4). A 2026-09-14 physical campaign confirmed a synthetic forwarding-rule lifecycle, and the 2026-09-18 production-helper smoke reconfirmed the five-slot form with write/read-back/restore and no residue. Response `result` is endpoint-state-dependent; do not interpret it globally. A 2026-09-21 public-SDK lifecycle additionally showed that the getter may lowercase hexadecimal letters in `mac`; semantic verification must therefore compare validated MAC addresses case-insensitively rather than requiring textual case preservation.

## Port triggering

Read `firewall/get_port_trigger`.

Disabled form:

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

The page supports up to 10 slots, requires all textual fields for a populated row, and evaluates `result===0` as success.

A 2026-09-14 physical run live-verified non-empty rule creation and getter read-back. It also established an important persistence rule:

> `{"enable":0}` disables Port Trigger but does **not** delete stored `items`.

To delete a stored rule in the verified WebUI workflow:

1. preserve the complete current item set and enable state;
2. send `enable=1` with the complete 10-slot list and the target slot emptied;
3. read back and verify the target item is gone;
4. restore the original enable state, for example with `{"enable":0}` if it was originally disabled;
5. read back again and verify both enable state and item semantics.

The dedicated recovery run verified this sequence: the synthetic item was removed, the original `enable=0` state restored, and the final non-empty item count was zero.

## URL filter

Use `get_url_filter` / `set_url_filter`. Setter uses `toStringData:false`:

```json
{"mode":"blacklist","black_items":[{"value":"example.invalid","index":0}]}
```

Whitelist uses `white_items`; disabled mode is `"disable"`.

A physical campaign confirmed a synthetic blacklist item and semantic cleanup. Verify item contents after restore instead of relying on raw list shape alone. A 2026-09-21 public-SDK lifecycle observed one immediate `get_url_filter` HTTP read timeout at an explicit 5-second harness timeout after a successful write; earlier URL-filter lifecycles passed without reboot. A single immediate post-write timeout is therefore inconclusive: retry read-back/re-login, do not blindly repeat the write, and decide success from eventual semantic state.

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

Enable/disable switches and non-empty rule lifecycles are live verified on ACIY.3.

### Complete-list reads

IP:

```json
{"ww_ip_filter":{"list":["all"]}}
```

Port:

```json
{"ww_port_filter":{"list":["all"]}}
```

These are directly confirmed by the physical NR2301 WebUI source and were used for physical rule read-back. Minimal `list: []` bodies are accepted too, but they are not the complete-list selector.

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

Empty slots are string `"0"`.

The focused physical verifier confirmed: enable → non-empty 10-slot write → full-list `list:["all"]` read-back → original list restore → original switch restore. The synthetic rule was absent at the final residue check.

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

Populated values use `"start:end"`; empty/incomplete slots use `"0"`.

The focused physical verifier confirmed: enable → non-empty 10-slot write → full-list `list:["all"]` read-back → original list restore → original switch restore. The synthetic port was absent at the final residue check.

## UPnP

Read: `firewall/ww_upnp_open_close_state`.

Write:

```json
{"ww_upnp":{"upnp_enable":"1"}}
```

or string `"0"`. A physical campaign confirmed mutation, read-back, and restore. WPS and UPnP are independent controls on the tested firmware.

## Remaining unresolved Firewall/NAT item

The focused WebUI-contract campaign is closed for WAN admin/ping, IP-filter rules, port-filter rules and Port Trigger items.

The remaining unresolved behavior is **DMZ destination clear/delete**. The current NR2301 WebUI itself exposes no clear/delete action, so related-device delete behavior must not be guessed or promoted as canonical NR2301 behavior without new direct evidence.
