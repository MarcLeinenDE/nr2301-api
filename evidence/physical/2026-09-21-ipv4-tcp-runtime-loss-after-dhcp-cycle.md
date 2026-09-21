# IPv4 TCP runtime loss observed after LAN/DHCP write cycle — 2026-09-21

Device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

Context:
- a physical SDK lifecycle had successfully changed `router_set_dhcp_settings_comb`
  by modifying only DHCP lease time;
- exact DHCP configuration was subsequently restored in the test cleanup path;
- the following network behavior was then observed from the attached Windows
  client on the NR2301 LAN.

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
- The exact restored DHCP configuration does not prove that all IPv4
  NAT/firewall/WAN runtime state recovered after the write.

Causality is **not yet established**. The observation occurred after a
`router_set_dhcp_settings_comb` mutation/restore cycle, but a reboot recovery
test is required before attributing the runtime failure to that setter.

Next verification:
1. reboot the router without changing configuration;
2. re-test IPv4 TCP to github.com:443, 1.1.1.1:80, 8.8.8.8:53 and IPv4 HTTPS;
3. compare with IPv6 TCP;
4. if IPv4 TCP returns after reboot, record the runtime recovery separately.

USB management-mode configuration was not changed.
