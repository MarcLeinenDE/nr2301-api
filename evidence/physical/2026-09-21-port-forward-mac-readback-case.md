# Port Forward MAC read-back canonicalization — 2026-09-21

Device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

## Context

During the public-SDK Firewall/NAT physical lifecycle, the SDK wrote one
synthetic Port Forward rule through `firewall/set_port_forward`.

The request used a locally administered synthetic MAC containing uppercase hexadecimal letters. The concrete test value is intentionally omitted from the public repository.

The setter completed and the rule was present on immediate
`firewall/get_port_forward` read-back.

## Observed getter representation

The getter returned the same rule and the same MAC address bytes, but hexadecimal letters were rendered in lowercase.

All other tested fields matched:

- rule name;
- local port;
- WAN port;
- index;
- enabled state.

The physical test failed only because its first implementation compared the MAC
string case-sensitively.

## Conclusion

On ACIY.3, Port Forward MAC read-back may canonicalize hexadecimal letters to
lowercase.

For semantic write/read-back verification:

- compare MAC addresses case-insensitively after validating the address shape;
- do not require preservation of hexadecimal letter case;
- preserve the raw getter value when exposing raw API data.

This does not change the write contract or the five-slot Port Forward model.

The test's `finally` restore path executed after the comparison failure. A
subsequent full rerun remains required to prove the complete Firewall/NAT final
snapshot equality.

No real device/client MAC address is recorded in this evidence.
