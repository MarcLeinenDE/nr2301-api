# Administrator direct-IP login recheck — 2026-09-21

Device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

## Context

An earlier controlled A/B test on 2026-08-31 observed administrator pre-auth
failure when the same router was addressed as `http://192.168.1.1`, while
`http://zyxel.home` succeeded. That remains valid historical evidence for that
runtime state.

During the 2026-09-21 LAN/router physical campaign, `zyxel.home` did not resolve
on the test PC. The test session therefore explicitly used:

```text
NR2301_URL=http://192.168.1.1
```

## Observed result

Two independent SDK programs then completed authenticated work through the
direct IP:

1. guarded static-DHCP residue cleanup;
2. the complete destructive LAN/router write/read-back/restore lifecycle.

Both programs instantiate `NR2301Client` with `NR2301_URL`, call
`client.login()`, and only proceed to the authenticated router operations after
the login succeeds.

The cleanup completed:

```text
DHCP_STATIC_RESIDUE count=1 synthetic_present=True
DHCP_STATIC_RESIDUE_CLEANUP = PASS
```

The subsequent lifecycle completed:

```text
LAN_DHCP_WRITE field=leasetime changed=True readback=True
LAN_STATIC_RESERVATION_WRITE original_count=0 synthetic_count=1 readback=True
LAN_LEGACY_ADDRESS_WRITE force_same_state=True readback=True
ROUTER_WORK_MODE_WRITE force_same_state=True mode_preserved=True
LAN_ROUTER_FINAL dhcp_restored=True reservations_restored=True address_preserved=True work_mode_preserved=True
PASSED
```

## Conclusion

The 2026-08-31 direct-IP `result=4` observation must not be generalized into a
permanent firmware rule.

On the same ACIY.3 device, direct-IP administrator challenge/login was usable on
2026-09-21. Host/authority sensitivity is therefore runtime/environment/state
dependent in the current evidence set.

Clients may continue to use `http://zyxel.home` as a convenient default, but
must not reject `http://192.168.1.1` pre-emptively. If one authority returns a
pre-auth failure, trying the alternative known authority is a recovery option;
the raw endpoint-specific result remains authoritative.

No credentials, session cookies, or private identifiers are recorded here.
