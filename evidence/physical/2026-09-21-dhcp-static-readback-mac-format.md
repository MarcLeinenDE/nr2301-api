# LAN/router SDK write/read-back/restore lifecycle — 2026-09-21

Device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

## Purpose

Close the complete production-SDK lifecycle for the remaining LAN/router write
contracts after the static-DHCP getter MAC-format correction.

This evidence is sanitized. No credentials, subscriber identifiers, real client
MAC addresses, or user phonebook data are recorded.

## Pre-run residue recovery

An earlier static-DHCP write had persisted successfully, but its cleanup was
blocked by the SDK parser rejecting the getter's uppercase hyphen-separated MAC
representation.

After the parser was corrected to normalize colon- and hyphen-separated MAC
representations, the guarded residue helper observed exactly one known synthetic
test reservation and removed it:

```text
DHCP_STATIC_RESIDUE count=1 synthetic_present=True
DHCP_STATIC_RESIDUE_CLEANUP = PASS
```

The cleanup helper only auto-clears when the synthetic reservation is the sole
table entry.

## Full physical lifecycle

The subsequent destructive integration test performed the following lifecycle:

1. snapshot the complete combined DHCP object;
2. snapshot the complete static-DHCP reservation table;
3. snapshot LAN address/netmask;
4. snapshot current router work mode;
5. change only DHCP lease time through
   `router/router_set_dhcp_settings_comb` and require exact read-back;
6. add one synthetic static reservation through
   `router/router_set_dhcp_static_ip` and require normalized exact read-back;
7. execute the deprecated `router/router_set_lan_ip` with the same original
   address using the SDK's explicit `force=True` transport-verification path;
8. execute `router/router_set_work_mode` with the same original mode using
   `force=True`;
9. restore the complete original static reservation table and combined DHCP
   object in `finally`;
10. require DHCP, reservations, LAN address and work mode to match the original
    snapshots exactly.

Observed test output:

```text
LAN_DHCP_WRITE field=leasetime changed=True readback=True
LAN_STATIC_RESERVATION_WRITE original_count=0 synthetic_count=1 readback=True
LAN_LEGACY_ADDRESS_WRITE force_same_state=True readback=True
ROUTER_WORK_MODE_WRITE force_same_state=True mode_preserved=True
LAN_ROUTER_FINAL dhcp_restored=True reservations_restored=True address_preserved=True work_mode_preserved=True
PASSED
```

Pytest result: `1 passed in 22.76s`.

## Static-DHCP getter representation

The live getter canonicalizes the tested reservation MAC to uppercase
hyphen-separated form, for example:

```json
{
  "index": 0,
  "mac": "02-00-00-00-00-01",
  "ip": "192.168.1.254"
}
```

The setter-side SDK accepts the frontend-equivalent colon-separated input and the
read path normalizes equivalent colon/hyphen representations to one stable SDK
form for semantic comparison.

## Conclusions

- `router_set_dhcp_settings_comb`: physical mutation + exact read-back + exact
  restore verified.
- `router_set_dhcp_static_ip`: physical add + normalized read-back + complete
  table restore verified.
- `router_set_lan_ip`: same-state forced transport execution + read-back
  verified; the method remains deprecated relative to the combined setter.
- `router_set_work_mode`: same-state forced transport execution + read-back
  verified; no router/bridge transition was required for this lifecycle.
- The complete cross-method lifecycle restored the initial LAN/router state
  exactly.
- A successful HTTP/write response alone is not the success criterion; recovered
  read-back remains authoritative for disruptive setters.
