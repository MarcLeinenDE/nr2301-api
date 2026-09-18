<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Physical Firewall WebUI contract verification — 2026-09-14

Firmware: `V1.00(ACIY.3)C0` on the dedicated non-production NR2301.

This focused write/read-back/restore campaign used only request shapes recovered from the shipped NR2301 WebUI source. USB/management mode and DMZ clear/delete were not touched.

## Live-confirmed contracts

### WAN ping

`firewall/set_ping_from_wan` with the nested WebUI body was physically verified end to end:

```json
{"ping_from_wan":{"ping_from_wan_enable":"0"}}
```

or `"1"`.

Observed lifecycle:

- same-state write: `firewall.setting_response="OK"`
- mutation: `firewall.setting_response="OK"`
- getter read-back matched the target
- restore: `firewall.setting_response="OK"`
- final getter matched the original state

### Remote administration from WAN

`firewall/set_admin_from_wan` with the nested WebUI body was physically verified end to end:

```json
{"admin_from_wan":{"admin_from_wan_enable":"0"}}
```

or `"1"`.

Observed lifecycle:

- same-state write: `firewall.setting_response="OK"`
- mutation: `firewall.setting_response="OK"`
- getter read-back matched the target
- restore: `firewall.setting_response="OK"`
- final getter matched the original state

The separate WebUI follow-up action `router/restart_web_server` was deliberately **not** invoked by this verification harness, so only the firewall setter itself is live-verified here.

### IP filter non-empty rule lifecycle

The exact shipped 10-slot WebUI wire form is now live-verified:

- enable through `firewall/ww_fw_set_disable_info` returned `setting_response="OK"`
- mode read-back confirmed enabled
- `firewall/ww_edit_ip_filter` accepted a 10-slot list with string wire indices and a synthetic documentation address
- full-list read through `ww_read_ip_filter` + `list:["all"]` returned the synthetic rule
- restoring the original 10-slot list returned `setting_response="OK"` and exact semantic restore
- filter enable state was restored successfully

Final synthetic-IP residue check: **absent**.

### Port filter non-empty rule lifecycle

The exact shipped 10-slot WebUI wire form is now live-verified:

- enable through `firewall/ww_fw_set_port_disable_info` returned `setting_response="OK"`
- mode read-back confirmed enabled
- `firewall/ww_edit_port_filter` accepted the 10-slot `start:end` list with string wire indices
- full-list read through `ww_read_port_filter` + `list:["all"]` returned the synthetic rule
- restoring the original 10-slot list returned `setting_response="OK"` and exact semantic restore
- filter enable state was restored successfully

Final synthetic-port residue check: **absent**.

## Port Trigger: write confirmed, restore semantics refined

A non-empty `firewall/set_port_trigger` write using the exact shipped item schema returned `result=0`, and `get_port_trigger` read-back contained the synthetic rule. Therefore rule creation with the source-derived item schema is physically confirmed.

The first restore attempt used the disabled WebUI form:

```json
{"enable":0}
```

It returned `result=0` and restored the enable state, but the stored synthetic item remained present. Final residue check reported the synthetic trigger still stored.

Inspection of the physical NR2301 `firewall_pt.html` explains this behavior: when the UI switch is OFF, the page sends only `{"enable":0}` and does not send `items`. Consequently, disabling Port Trigger does **not** clear stored rules.

The UI only transmits its 10-slot `items` array while the switch is ON. A correct clear/restore sequence for a previously disabled clean state therefore requires:

1. submit `{"enable":1,"items":[...10 slots with the target slot emptied...]}` to update the stored list;
2. then submit `{"enable":0}` to restore the disabled state.

A focused recovery harness has been prepared downstream to verify this two-step cleanup and remove the synthetic residue. Until that succeeds, the Port Trigger lifecycle is `LIVE_VERIFIED` for non-empty creation/read-back but cleanup/restore remains pending.

## Campaign result

- WAN ping nested shape: PASS
- WAN admin nested shape: PASS
- IP-filter 10-slot non-empty lifecycle: PASS
- Port-filter 10-slot non-empty lifecycle: PASS
- Port-trigger non-empty creation/read-back: PASS
- Port-trigger exact restore: PENDING two-step cleanup verification
- final synthetic IP residue: absent
- final synthetic port residue: absent
- final synthetic trigger residue: present pending focused cleanup

No private deployment identifiers or secrets are included in this evidence file.
