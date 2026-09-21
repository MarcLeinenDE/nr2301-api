# URL Filter post-write transient management timeout — 2026-09-21

Device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

## Context

During the public-SDK Firewall/NAT physical lifecycle, the following write/read-back stages had already completed successfully in one authenticated session:

- DMZ enable/disable;
- VPN passthrough;
- administrator access from WAN;
- ping from WAN;
- IP-filter list and enable state;
- port-filter list and enable state;
- Port Forward;
- Port Trigger.

The test then called `firewall/set_url_filter` with the already live-verified synthetic blacklist shape. The write call returned successfully.

## Observation

The immediately following `firewall/get_url_filter` request connected to the management HTTP service at `zyxel.home`, but no HTTP response arrived before the test's explicit 5-second read timeout.

The SDK surfaced this as a transport read timeout.

This was not:

- a DNS-resolution failure;
- a connection-refused failure;
- an authentication result/error response;
- a request-schema rejection.

The failure occurred only on the immediate getter read-back after the write.

## Prior evidence

This does not invalidate the URL Filter contract.

Earlier physical evidence already established:

- 2026-09-14: synthetic URL-filter write/read-back succeeded; cleanup semantics required an active empty blacklist write before returning to `mode=disable`, because disabling alone does not clear stored items.
- 2026-09-18: the production Firewall/NAT helper smoke completed URL-filter write/read-back/restore successfully and no router reboot occurred; `boot_time` advanced only from 8282 to 8298.
- earlier NR2301 disruptive-write work established that temporary management/API stalls can occur after configuration writes and should be handled as inconclusive until management recovery/read-back is attempted.

## Interpretation

The current evidence supports treating a single immediate post-write read timeout as a transient management-readiness condition, not as proof that the URL-filter write failed.

A robust physical verification sequence should therefore:

1. issue the already verified write once;
2. do not blindly repeat the write after a timeout;
3. retry the getter with a less aggressive timeout;
4. re-login if the management session was lost;
5. decide success only from eventual semantic read-back;
6. preserve the existing two-step cleanup rule for stored URL-filter items.

This recovery rule is evidence for the physical verification harness. It does not change the URL-filter request schema or success semantics.

A complete rerun is still required to prove the final Firewall/NAT snapshot restore after this transient timeout.
