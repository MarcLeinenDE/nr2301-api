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
