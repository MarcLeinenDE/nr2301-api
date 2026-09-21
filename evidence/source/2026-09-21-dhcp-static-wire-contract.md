# Static DHCP setter source-contract correction — 2026-09-21

Firmware: `V1.00(ACIY.3)C0`.

A read-only capture of the shipped `html/set_dhcp.html` page was used after a
physical SDK test failed to verify a synthetic reservation.

The stock page constructs each populated reservation as:

```javascript
postData.data.push({
  index: i, mac: mac.macFormat(), ip: ip
})
```

Consequences:

- `index` is serialized as a JSON number;
- only populated slots are sent;
- slots are limited to `0..9`;
- before submission, each non-empty reservation IP is required to pass
  `checkIPGetewayMask(lanIP, submask, ip)`;
- duplicate MAC/IP values and invalid/multicast MACs are rejected;
- the resulting member is `router/router_set_dhcp_static_ip` with
  `data: {data: [...]}`;
- the enclosing call is `multicalls` with `toStringData=false`.

The failed SDK attempt had normalized `index` to string `"0"` and used
`192.0.2.254`, which was outside the router's active LAN subnet. Those inputs
did not match the shipped frontend contract.

No new write was performed during this source capture.
