# IPv4 TCP runtime loss observed after LAN/DHCP write cycle — 2026-09-21

Device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

Context:
- earlier in the same session a physical SDK lifecycle had successfully changed
  `router_set_dhcp_settings_comb` by modifying only DHCP lease time and then
  restored the exact DHCP configuration;
- immediately before the network diagnosis, the full factory-reset/config-restore
  production lifecycle was accidentally executed again by the user and completed
  with PASS, including final configuration restoration;
- after that PASS result, the following network behavior was observed from the
  attached Windows client on the NR2301 LAN.

Observed client path:
- interface: Ethernet 3
- IPv4 source: 192.168.1.100
- IPv6 source: global IPv6 address on the same interface

Observed results:

```text
github.com -> IPv4 140.82.121.4
  ICMP ping: success
  TCP/443: fail

1.1.1.1
  ICMP ping: success
  TCP/443: fail
  TCP/80: fail

8.8.8.8
  TCP/53: fail

google.com
  curl -4 HTTPS: timeout
  curl -6 HTTPS: HTTP 200

microsoft.com
  IPv6 TCP/443: success

WinHTTP proxy: DirectAccess / no proxy
curl.exe https://github.com: failed to connect to TCP/443
```

Interpretation:
- DNS resolution worked.
- IPv4 ICMP routing worked.
- IPv4 TCP failed across multiple unrelated destinations and ports.
- IPv6 TCP on the same client/interface remained functional.
- This is therefore not a GitHub-specific failure and not a generic loss of
  Internet access.
- A PASS result for factory-reset/config-restore plus exact configuration
  equality does **not** prove that IPv4 NAT/firewall/WAN runtime state is healthy.

Causality is **not yet established**. Because the failure was observed after a
fresh factory-reset/config-restore lifecycle as well as after earlier LAN/DHCP
writes, the evidence currently points more broadly at incomplete IPv4 runtime
recovery after disruptive reset/restore operations rather than specifically at
`router_set_dhcp_settings_comb`.

A plain reboot recovery test is required next. If IPv4 TCP returns after reboot
without any configuration change, that will strongly support a runtime-readiness
gap after reset/restore.

Next verification:
1. reboot the router without changing configuration;
2. re-test IPv4 TCP to github.com:443, 1.1.1.1:80, 8.8.8.8:53 and IPv4 HTTPS;
3. compare with IPv6 TCP;
4. if IPv4 TCP returns after reboot, record the runtime recovery separately and
   extend factory-reset/config-restore readiness checks beyond management/API
   recovery.

USB management-mode configuration was not changed.


## Plain reboot recovery observation

A subsequent plain production reboot was issued without changing configuration.

Observed reboot proof:

```text
boot_before=1311
boot_after=58
outage_observed=True
action_error=TransportError
recovery_attempt=31
```

Immediately after management/API recovery:

```text
1.1.1.1:80 TCP   -> success
8.8.8.8:53 TCP   -> success
github.com:443   -> name resolution failed
curl -4 google   -> DNS resolution timeout
curl -6 google   -> connection timeout
```

This is a strong readiness-ordering observation:

1. management/API recovery completed;
2. raw IPv4 TCP dataplane connectivity recovered;
3. DNS resolution was still unavailable;
4. IPv6 dataplane was still unavailable at that observation point.

Therefore a post-reset/reboot helper must not treat management/API recovery as
equivalent to full Internet/dataplane readiness. Readiness should be modeled as
separate stages and, where requested, verified independently.

Recommended recovery model:
- control-plane ready: authenticated API responds and boot evidence is valid;
- configuration ready: stable configuration read-back succeeds;
- IPv4 dataplane ready: at least one explicit IPv4 TCP probe succeeds;
- DNS ready: resolver successfully resolves a known hostname;
- IPv6 dataplane ready: optional/conditional IPv6 TCP probe succeeds.

The exact external probe targets should remain configurable rather than being
hard-coded as a universal product requirement.


## Manual hardware factory reset

After the plain software reboot, the user reported that the WebUI was still only
partially loading and general router behavior remained abnormal. Because remote
control was unreliable, a hardware factory reset was then performed using the
physical reset button.

This hardware reset is an important diagnostic boundary:
- it does not depend on the SDK factory-reset helper;
- it does not restore a saved configuration;
- it clears prior runtime/session state through the device's physical reset path.

No configuration restore should be performed until the bare factory state is
checked for:
- local WebUI readiness;
- local API/control-plane readiness;
- IPv4 TCP dataplane readiness;
- DNS readiness;
- IPv6 dataplane readiness.

If the bare factory state is healthy but the problem returns only after a saved
configuration is restored, the fault domain narrows substantially toward the
restore/post-restore path or restored configuration/runtime interaction.


## Bare hardware-factory state verification

After the manual hardware factory reset, **no saved configuration was restored**
before the following checks.

Client/network state:
- DHCP renewed successfully from `192.168.1.1`;
- client IPv4: `192.168.1.100/24`;
- IPv4 default gateway: `192.168.1.1`;
- global IPv6 address and IPv6 default gateway present;
- DNS servers included both router IPv4 and router-provided IPv6 addresses.

Observed checks:

```text
Resolve-DnsName zyxel.home
  -> 192.168.1.1

zyxel.home:80
  -> TCP success

192.168.1.1:80
  -> TCP success

1.1.1.1:80
  -> TCP success

8.8.8.8:53
  -> TCP success

Resolve-DnsName github.com
  -> 140.82.121.3

curl -4 https://www.google.com
  -> HTTP 200

curl -6 https://www.google.com
  -> HTTP 200
```

Conclusion:
- local management connectivity is healthy in bare factory state;
- IPv4 TCP dataplane is healthy;
- DNS is healthy;
- IPv6 dataplane is healthy.

This materially narrows the fault domain. The abnormal state observed after the
earlier automated factory-reset/config-restore lifecycle is **not reproduced by
a bare hardware factory reset**. The strongest current hypotheses are therefore:

1. a post-config-restore runtime/readiness defect;
2. a restored configuration value or combination that leaves one or more
   dataplane/runtime subsystems unhealthy;
3. interaction between config restore and subsystem startup ordering.

The evidence does not currently support a general hardware failure or a
persistent USB-management-path failure.

Next controlled experiment should capture a factory-state backup, then restore
the known baseline backup once, while continuously measuring:
- control-plane/API readiness;
- WebUI readiness;
- IPv4 TCP;
- DNS;
- IPv6 TCP.

Do not declare restore success solely from configuration equality.
