# VPN production SDK lifecycle — 2026-09-18

Physical device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

The production-facing SDK VPN helpers were exercised end-to-end against the
dedicated test router after normalizing the ACIY.3
`vpn_client_active_index="disable"` sentinel.

Verified lifecycle:

- snapshot existing VPN profile/global/active state
- add a synthetic PPTP profile with local test credentials
- edit the same profile to L2TP/IPsec, including password and PSK fields
- enable the VPN client subsystem
- mark the synthetic profile active
- mark the synthetic profile inactive
- delete the synthetic profile
- exercise both global disable and global enable transitions
- restore the original active-profile selection
- restore the original global enable state
- verify the pre-existing public profile state is unchanged
- verify no router reboot occurred during the lifecycle

Final physical result: PASS.

Local test credentials were intentionally used because the device is a dedicated
non-production research target. Secret values are omitted from public evidence
and CI logs.
