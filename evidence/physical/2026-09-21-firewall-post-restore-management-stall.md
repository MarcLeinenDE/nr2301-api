# Firewall/NAT post-restore transient management stall — 2026-09-21

Device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

## Context

A public-SDK Firewall/NAT lifecycle exercised all reversible write helpers in one
authenticated session.

The run physically completed write + semantic read-back for:

- DMZ enable/disable;
- VPN passthrough;
- administrator access from WAN;
- ping from WAN;
- IP-filter list;
- IP-filter enable state;
- port-filter list;
- port-filter enable state;
- Port Forward;
- Port Trigger;
- URL Filter;
- UPnP.

The test then executed its `finally` restore path for the original Firewall/NAT
state.

## Observation

After restore calls completed, the final verification snapshot began reading the
Firewall/NAT getters again.

The final `firewall/get_admin_from_wan` request connected to the management
HTTP service at `zyxel.home`, but the server did not return an HTTP response
within the harness's explicit 5-second read timeout.

The SDK surfaced a transport read timeout.

This occurred after:

- URL Filter had already passed write + read-back in the same run;
- UPnP had already passed write + read-back;
- restore code had executed;
- the management host was still reachable at the TCP/HTTP connection level.

Therefore this failure cannot be attributed specifically to the URL-filter
contract.

## Relation to earlier evidence

Earlier ACIY.3 evidence already showed:

- 2026-09-18 full Firewall/NAT production-helper smoke completed without a router
  reboot; boot time only advanced during the test.
- 2026-09-21 one immediate `get_url_filter` after a successful URL-filter write
  hit a 5-second read timeout.
- other NR2301 disruptive-write lifecycles use recovery/re-login and delayed
  read-back because management availability can temporarily lag configuration
  writes.

The new run broadens the interpretation: the transient stall can affect a
different Firewall getter after the cumulative write/restore sequence.

## Interpretation

A single Firewall/NAT getter timeout immediately after a configuration-write or
restore sequence is an **inconclusive management-readiness condition**, not
evidence that the preceding setter failed or that the requested state was not
restored.

Physical verification should therefore use a shared Firewall/NAT recovery rule:

1. issue each intended write only once unless semantic read-back proves a retry
   is required;
2. after a transport/protocol failure, retry the getter rather than blindly
   repeating the write;
3. allow a less aggressive read timeout than the original 5-second harness;
4. re-login if the session was lost;
5. decide success from eventual semantic read-back;
6. verify the final full snapshot after management becomes ready.

The request contracts themselves are unchanged.

The current run proves successful write/read-back for all 12 reversible
Firewall/NAT writes before the final snapshot timeout. A further rerun is needed
only to close final post-restore snapshot equality under the generalized recovery
policy.

No real configured rule values, client identifiers, credentials or session
tokens are published here.
