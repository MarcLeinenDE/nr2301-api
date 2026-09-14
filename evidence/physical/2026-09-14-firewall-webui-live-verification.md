<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Physical NR2301 Firewall WebUI-contract verification — 2026-09-14

Firmware: `V1.00(ACIY.3)C0` on the dedicated non-production NR2301.

This run physically exercised the exact request shapes recovered from the shipped NR2301 WebUI source. Synthetic documentation-only values were used; no private deployment identifiers are published here.

## Summary

The following source-confirmed contracts were physically verified with write, getter read-back and restore:

- `firewall/set_ping_from_wan`
- `firewall/set_admin_from_wan`
- `firewall/ww_edit_ip_filter` using the complete 10-slot WebUI list representation
- `firewall/ww_edit_port_filter` using the complete 10-slot WebUI list representation
- `firewall/set_port_trigger` using a non-empty trigger item

IP-filter and port-filter synthetic rules were removed successfully and their switch state was restored. WAN ping and WAN admin were restored exactly.

Port Trigger required an additional recovery pass because the WebUI's disabled form (`{"enable":0}`) disables triggering but does **not** delete persisted rule items.

## WAN ping

Exact nested request shape:

```json
{"ping_from_wan":{"ping_from_wan_enable":"0"}}
```

or string `"1"`.

Physical result:

- same-state write: `firewall.setting_response = "OK"`
- mutation write: `"OK"`
- getter read-back matched target
- restore write: `"OK"`
- getter confirmed original state restored

This exact nested write contract is live verified on ACIY.3.

## WAN administration

Exact nested request shape:

```json
{"admin_from_wan":{"admin_from_wan_enable":"0"}}
```

or string `"1"`.

Physical result:

- same-state write: `firewall.setting_response = "OK"`
- mutation write: `"OK"`
- getter read-back matched target
- restore write: `"OK"`
- getter confirmed original state restored

The separate frontend-scheduled `router/restart_web_server` action was deliberately not invoked by this verifier. The setter itself is live verified; consumers that reproduce the full WebUI workflow should account for the additional web-server restart behavior when changing this setting.

## IP filter non-empty rule lifecycle

The verifier used the shipped WebUI wire representation:

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

with 10 indexed slots total and string indices because the common frontend transport stringifies numbers by default.

Physical result:

- filter enable response: `setting_response = "OK"`
- enable read-back succeeded
- non-empty list write response: `"OK"`
- full-list `list:["all"]` read-back contained the synthetic rule
- original list restore response: `"OK"`
- semantic list restore succeeded
- original switch state restore succeeded

The exact 10-slot non-empty write lifecycle is live verified.

## Port filter non-empty rule lifecycle

The verifier used the shipped WebUI wire representation:

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

with 10 indexed slots total. `index` and `port_filter_disable` are wire strings under the default frontend serializer.

Physical result:

- filter enable response: `setting_response = "OK"`
- enable read-back succeeded
- non-empty list write response: `"OK"`
- full-list `list:["all"]` read-back contained the synthetic rule
- original list restore response: `"OK"`
- semantic list restore succeeded
- original switch state restore succeeded

The exact 10-slot non-empty write lifecycle is live verified.

## Port Trigger non-empty lifecycle and delete semantics

The synthetic rule used the exact source-confirmed `toStringData:false` item shape:

```json
{
  "enable":1,
  "items":[
    {
      "index":0,
      "name":"SDK-PT-WEBUI",
      "trigger_port":"65500",
      "start_port":"65501",
      "end_port":"65501"
    }
  ]
}
```

Initial write returned `result = 0` and getter read-back matched the synthetic item exactly.

The first restore attempted the disabled WebUI form:

```json
{"enable":0}
```

That returned `result = 0` and restored `enable=0`, but the synthetic item remained stored. This establishes an important endpoint semantic: **disabling Port Trigger does not delete stored rule items**.

A dedicated recovery pass then reproduced the WebUI list-edit behavior:

1. verify current state was `enable=0` and the only non-empty trigger item was the synthetic test rule;
2. write `enable=1` with the complete 10-slot list and the synthetic slot cleared;
3. verify the synthetic item disappeared;
4. write `{"enable":0}` to restore the original enable state;
5. verify final `enable=0` and zero non-empty trigger items.

Recovery output:

- initial enable: `0`
- synthetic slots: `[0]`
- unrelated rule count: `0`
- clear write result: `0`
- clear-state enable: `1`
- synthetic cleared: `true`
- enable restore result: `0`
- final enable: `0`
- final non-empty count: `0`
- recovery restored: `true`

The Port Trigger item create/read/delete/disable lifecycle is therefore live verified. Implementations must not model `{"enable":0}` as rule deletion.

## Final state

After recovery:

- synthetic IP-filter rule absent
- synthetic port-filter rule absent
- synthetic Port Trigger rule absent
- original Port Trigger enable state restored (`0`)
- no unrelated Port Trigger entries were modified
- WAN ping and WAN administration restored to their original values

## Publication boundary

No real password, session cookie, MAC address, private LAN address, subscriber identifier or unrelated rule content is included in this evidence.
