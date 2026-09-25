# Public-SDK Firewall/NAT reversible lifecycle — 2026-09-25

Device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

## Scope

This run closed the public-SDK physical lifecycle for the 12 Firewall/NAT write
methods that are fully reversible through their verified API contracts.

The test used:

`tests/integration/test_firewall_write_lifecycle.py`

with the authenticated administrator SDK surface and the canonical management
hostname.

## Physical result

Observed output:

```text
FIREWALL_DMZ_ENABLE_WRITE changed=True readback=True
FIREWALL_VPN_PASSTHROUGH_WRITE changed=True readback=True
FIREWALL_ADMIN_FROM_WAN_WRITE changed=True readback=True
FIREWALL_PING_FROM_WAN_WRITE changed=True readback=True
FIREWALL_IP_FILTER_RULE_WRITE changed=True readback=True
FIREWALL_IP_FILTER_MODE_WRITE changed=True readback=True
FIREWALL_PORT_FILTER_RULE_WRITE changed=True readback=True
FIREWALL_PORT_FILTER_MODE_WRITE changed=True readback=True
FIREWALL_PORT_FORWARD_WRITE changed=True readback=True
FIREWALL_PORT_TRIGGER_WRITE changed=True readback=True
FIREWALL_URL_FILTER_WRITE changed=True readback=True
FIREWALL_UPNP_WRITE changed=True readback=True
FIREWALL_FINAL dmz_restored=True vpn_restored=True wan_controls_restored=True filters_restored=True nat_rules_restored=True upnp_restored=True
PASSED
```

Pytest result:

```text
1 passed in 25.64s
```

## Verified write methods

The run physically exercised mutation/action, semantic read-back and exact final
restore for:

1. `firewall/fw_set_disable_info`
2. `firewall/fw_set_vpn_passthrough`
3. `firewall/set_admin_from_wan`
4. `firewall/set_ping_from_wan`
5. `firewall/ww_edit_ip_filter`
6. `firewall/ww_fw_set_disable_info`
7. `firewall/ww_edit_port_filter`
8. `firewall/ww_fw_set_port_disable_info`
9. `firewall/set_port_forward`
10. `firewall/set_port_trigger`
11. `firewall/set_url_filter`
12. `firewall/ww_upnp_open_close`

## Recovery behavior exercised by this campaign

Earlier runs of the same lifecycle discovered two additional physical behaviors
that are now part of the canonical verification model:

- Port Forward MAC read-back may lowercase hexadecimal letters. MAC verification
  is semantic/case-insensitive while raw getter values remain raw.
- after cumulative Firewall/NAT writes/restores, the management API can
  transiently stall. A single immediate getter timeout is inconclusive; the
  harness retries read-only snapshot verification with recovery/re-login rather
  than repeating writes blindly.

The final successful run completed without a recovery failure and proved the
complete semantic snapshot matched the original state.

## Remaining Firewall/NAT physical write gap

`firewall/fw_edit_dmz_entry` remains outside this 12-write lifecycle because
the stock NR2301 contract has no verified destination-clear/delete operation.

Its dedicated physical test uses an in-memory configuration backup as the
recovery path when the original DMZ destination is empty. That separate test is
still pending.

No real configured rule values, client identifiers, credentials, session
tokens, or private topology data are published here.
