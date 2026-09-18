# Legacy DHCP multicall response envelope — 2026-09-18

Physical device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

A read-only SDK coverage test exercised `router/router_get_dhcp_settings`
through the frontend-verified one-member multicall transport.

Observed multicall member shape, sanitized:

```json
{
  "data": {
    "dhcp": {
      "disabled": "<string>",
      "start": "<string>",
      "limit": "<string>",
      "leasetime": "<string>",
      "mtu": "<string>",
      "dnsmode": "<string>",
      "dns1": "<string>",
      "dns2": "<string>",
      "ipv6dns1": "<string>",
      "ipv6dns2": "<string>"
    }
  }
}
```

The important contract correction is structural: the endpoint payload is nested
under `responses[0].data`. The earlier public schema incorrectly placed
`dhcp` directly at the multicall-member root.

No write was performed. Concrete LAN/DNS values from the physical device are
intentionally omitted.
