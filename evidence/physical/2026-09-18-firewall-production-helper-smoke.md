# Firewall/NAT production-helper smoke — 2026-09-18

Physical device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

This sanitized record captures the final production-facing SDK smoke after the
2026-09-14 Firewall/NAT research campaign. No raw local identifiers, credentials
or unrelated configured rules are included.

## Full production smoke

The SDK production `FirewallNamespace` was exercised through its public helper
surface with read-back and restore.

Passed:

- DMZ enable same-state
- DMZ destination same-state (non-empty only; no clear/delete)
- VPN passthrough same-state
- WAN ping same-state
- WAN administration same-state; no implicit `router/restart_web_server`
- UPnP same-state
- IP filter synthetic non-empty lifecycle and restore
- port filter synthetic non-empty lifecycle and restore
- Port Trigger synthetic lifecycle, deletion and restore
- URL filter synthetic lifecycle and restore

The first Port Forward production smoke exposed a production-helper defect: the
helper emitted ten slots, while the already successful physical Port Forward
campaign used the NR2301 WebUI's five-slot representation. The attempted
synthetic rule was not visible. Restore completed and the final synthetic residue
check was false.

No router reboot occurred during the full smoke: `boot_time` advanced from
8282 to 8298.

## Focused Port Forward retest

After correcting the production helper to five slots and using the previously
live-working colon-separated locally administered test MAC representation, the
focused retest produced:

- original enable: 0
- synthetic slot: 0
- write result: 0
- synthetic read-back: true
- list restore result: 0
- disable restore result: 1 (endpoint-state-dependent; final state verified)
- final enable: 0
- final semantic state restored: true
- synthetic residue present: false
- `boot_time`: 9053 before and 9053 after
- reboot detected: false
- final result: PASS

Therefore the production Port Forward contract is five indexed slots
(`index=0..4`), with native integer `enable`/`index` values because the
stock page uses `toStringData:false`.

As previously documented, `set_port_forward.result` is endpoint-state-dependent:
`0` was observed for enabled writes and `1` for the final disabled state.
Do not interpret that field as a generic success/failure code without state
read-back.

## Remaining unresolved behavior

DMZ destination clear/delete remains unresolved. The stock NR2301 WebUI exposes
no clear/delete action for the stored destination, so no such production helper
is defined or inferred.
