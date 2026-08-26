# LAN, DHCP and DNS recipes

Detailed reference: [`router`](../../api/router.md).

The current frontend uses combined LAN/DHCP/DNS objects. These writes can reset the management connection, so the safe pattern is **read → copy → modify → multicall write → recover → read-back**.

## Read LAN/DHCP/DNS state

Call `router/router_get_dhcp_settings_comb`.

The `dhcp` object contains:

```text
disabled
lan_ip
lan_netmask
start
end
leasetime
mtu
dnsmode
dns1
dns2
ipv6dns1
ipv6dns2
```

Known field semantics:

- `disabled`: `0` = DHCP enabled, `1` = DHCP disabled
- `lan_ip`: router LAN IPv4 address
- `lan_netmask`: IPv4 netmask
- `start` / `end`: DHCP pool range
- `leasetime`: seconds; frontend validates 60..604800
- `mtu`: frontend validates 1280..1500
- `dnsmode`: `auto` or `manual`
- `dns1` / `dns2`: upstream IPv4 DNS resolvers
- `ipv6dns1` / `ipv6dns2`: upstream IPv6 DNS resolvers

## Safe combined write

The stock UI normally sends `router/router_set_dhcp_settings_comb` as a member of `/api.cgi?multicalls=1`.

Do not construct the complete object from defaults. Start with the exact `dhcp` object returned by `router_get_dhcp_settings_comb`, modify only the desired fields, and send that object as the member `data`.

Conceptually:

```json
{
  "requests": [
    {
      "path": "router",
      "method": "router_set_dhcp_settings_comb",
      "data": {
        "disabled": "CURRENT_VALUE",
        "lan_ip": "CURRENT_VALUE",
        "lan_netmask": "CURRENT_VALUE",
        "start": "CURRENT_VALUE",
        "end": "CURRENT_VALUE",
        "leasetime": "CURRENT_VALUE",
        "mtu": "CURRENT_VALUE",
        "dnsmode": "CURRENT_OR_NEW_VALUE",
        "dns1": "CURRENT_OR_NEW_VALUE",
        "dns2": "CURRENT_OR_NEW_VALUE",
        "ipv6dns1": "CURRENT_OR_NEW_VALUE",
        "ipv6dns2": "CURRENT_OR_NEW_VALUE"
      },
      "timeout": 30
    }
  ]
}
```

After the write, management TCP may reset. Reconnect, re-authenticate if necessary and read `router_get_dhcp_settings_comb` again.

## Change DNS to manual resolvers

A live-verified example used Cloudflare resolvers:

```text
dnsmode = manual
dns1 = 1.1.1.1
dns2 = 1.0.0.1
ipv6dns1 = 2606:4700:4700::1111
ipv6dns2 = 2606:4700:4700::1001
```

Workflow:

1. GET `router_get_dhcp_settings_comb`.
2. Copy its `dhcp` object unchanged.
3. Set `dnsmode` to `manual` and replace only the four DNS fields.
4. Send the full copied/modified object with `router_set_dhcp_settings_comb` through multicall.
5. Recover management connectivity.
6. GET the combined settings again and require the five DNS fields to match exactly.

Important behavior: the manual addresses are **upstream resolvers for the NR2301's DNS proxy**. Connected clients may still receive/use the router's LAN address as their DNS server rather than receiving `1.1.1.1` directly through DHCP option 6.

## Return DNS to automatic

Use the same read-copy-write pattern, then set:

```text
dnsmode = auto
dns1 = ""
dns2 = ""
ipv6dns1 = ""
ipv6dns2 = ""
```

Read the settings back after recovery.

## Change LAN address or DHCP pool

Use the same combined setter and change only `lan_ip`, `lan_netmask`, `start`, `end`, `disabled`, `leasetime` and/or `mtu` as needed.

A LAN-address change can make the old management URL unreachable. A client should know the target address before sending the write and should reconnect to the new address rather than repeatedly retrying the old one.

`router/router_set_lan_ip` also exists but is marked as a deprecated helper in the shipped frontend. Prefer the combined setter.

## Static DHCP reservations

Read `router/router_get_dhcp_static_ip`. The reservation setter is `router/router_set_dhcp_static_ip` and accepts:

```json
{
  "data": [
    {
      "index": "0",
      "mac": "02:00:00:00:00:01",
      "ip": "192.0.2.10"
    }
  ]
}
```

The UI supports ten visible slots (`0..9`). The MAC/IP shown above are documentation examples; replace them with the intended client and an address appropriate for the router LAN.

Use multicall/recovery handling and read the reservation list back after writing.

## Router vs bridge work mode

Read `router/router_get_work_mode`. Known values are `router` and `bridge`.

`router/router_set_work_mode` is live verified only with disruptive recovery handling. Changing work mode can fundamentally change addressing and management reachability; do not combine it casually with an unrelated DHCP/DNS change.