# VPN active-index sentinel — 2026-09-18

Physical device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

During a reversible SDK VPN profile-write campaign, `cm/get_vpn_clients`
returned the following relevant state while the VPN client subsystem was
disabled:

```json
{
  "vpn_client_enable": "disable",
  "vpn_client_active_index": "disable"
}
```

The test had already successfully added and edited a synthetic VPN profile.
The campaign stopped before the active/inactive mutation because the SDK
incorrectly attempted to parse `"disable"` as a numeric profile index.

The integration test's `finally` cleanup path removed the synthetic profile
and restored the original global enable state; no additional cleanup failure
was reported.

Contract correction: `vpn_client_active_index="disable"` is a valid
no-active-profile sentinel on the tested firmware and must not be parsed
unconditionally as a numeric index.

Secret profile fields were used locally as part of the test but are not
included in this public evidence.
