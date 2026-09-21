# Static DHCP reservation read-back format — 2026-09-21

Device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

## Context

The corrected LAN write lifecycle started from a bare hardware-factory state with
an empty static DHCP reservation table.

Before the write:

```text
DHCP_STATIC_RESIDUE count=0 synthetic_present=False
DHCP_STATIC_RESIDUE_CLEANUP = NOT_NEEDED
```

The combined DHCP lease-time mutation succeeded and verified by exact read-back.

The static reservation probe then used the corrected contract (the public MAC value below is a documentation-safe synthetic substitute for the local test value):
- numeric slot index `0`;
- locally administered unicast test MAC `02:00:00:00:00:01`;
- IPv4 `192.168.1.254`, inside the active `192.168.1.0/24` LAN and outside the
  DHCP pool chosen by the integration test.

## Observed read-back

The setter persisted the reservation. The subsequent
`router/router_get_dhcp_static_ip` response contained:

```json
{
  "index": 0,
  "mac": "02-00-00-00-00-01",
  "ip": "192.168.1.254"
}
```

The integration test failed only when the SDK normalization layer rejected the
getter's MAC string because it accepted colon-separated MACs exclusively.

## Conclusions

1. The corrected numeric-index/in-subnet setter request persists on ACIY.3.
2. Authenticated administrator write access is live verified.
3. The getter returns the tested MAC in uppercase hyphen-separated form.
4. SDK comparison logic must normalize equivalent colon- and hyphen-separated
   MAC representations before exact semantic comparison.
5. The failed test is not evidence of a setter failure.
6. Because cleanup used the same strict SDK parser, the synthetic reservation may
   remain present until a raw/format-tolerant cleanup is executed.

No secrets were recorded.
