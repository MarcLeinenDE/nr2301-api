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

Read `router/router_get_dhcp_static_ip`. The stock ACIY.3
`html/set_dhcp.html` page builds the setter member as:

```json
{
  "path": "router",
  "method": "router_set_dhcp_static_ip",
  "data": {
    "data": [
      {
        "index": 0,
        "mac": "02:00:00:00:00:01",
        "ip": "192.168.1.2"
      }
    ]
  }
}
```

Contract details:

- `index` is a **JSON number** in the wire payload, not a string.
- Only occupied rows are included; empty slots are omitted.
- The UI exposes exactly ten slots, indices `0..9`.
- Each reservation IP must be in the current LAN/subnet; the frontend checks
  this with `checkIPGetewayMask(lanIP, submask, ip)`.
- Duplicate MACs/IPs, multicast/invalid MACs and half-filled rows are rejected
  by the frontend.
- The page submits all changed LAN/DHCP members through one multicall with
  `toStringData=false`; SDK helpers should preserve the same JSON types.
- A write must be verified by `router_get_dhcp_static_ip` read-back. Tests
  should restore the complete original reservation table.

The 2026-09-21 SDK test that used string `"0"` plus `192.0.2.254` outside
the active LAN subnet was not frontend-equivalent and correctly failed to
verify. It is not evidence that the setter is unavailable.


## Router vs bridge work mode

Read `router/router_get_work_mode`. Known values are `router` and `bridge`.

`router/router_set_work_mode` is live verified only with disruptive recovery handling. Changing work mode can fundamentally change addressing and management reachability; do not combine it casually with an unrelated DHCP/DNS change.

## Physical SDK lifecycle closure — 2026-09-21

The complete LAN/router lifecycle has now been exercised through the public SDK
on ACIY.3:

- mutate DHCP lease time and verify exact read-back;
- add one synthetic static reservation and verify normalized exact read-back;
- execute the deprecated LAN-IP setter at the same original address with an
  explicit forced transport test;
- execute the work-mode setter at the same original mode with an explicit forced
  transport test;
- restore the complete original static reservation table and combined DHCP
  object;
- require final DHCP, reservation, LAN-address and work-mode snapshots to equal
  the originals.

The run passed, including exact final restoration. Disruptive writes should still
be treated as successful only after recovery/read-back, not merely from the HTTP
response.
