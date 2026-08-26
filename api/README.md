# API namespace index

The current catalog contains **157 methods across 16 namespaces**.

| Namespace | Methods | Documentation |
|---|---:|---|
| `account` | 6 | [account.md](account.md) |
| `aoc` | 3 | [aoc.md](aoc.md) |
| `cm` | 21 | [cm.md](cm.md) |
| `ddns` | 2 | [ddns.md](ddns.md) |
| `firewall` | 26 | [firewall.md](firewall.md) |
| `ota` | 7 | [ota.md](ota.md) |
| `package` | 4 | [package.md](package.md) |
| `phonebook` | 11 | [phonebook.md](phonebook.md) |
| `router` | 27 | [router.md](router.md) |
| `sim` | 7 | [sim.md](sim.md) |
| `sms` | 9 | [sms.md](sms.md) |
| `statistics` | 11 | [statistics.md](statistics.md) |
| `tr069` | 4 | [tr069.md](tr069.md) |
| `util_wan` | 3 | [util_wan.md](util_wan.md) |
| `version` | 2 | [version.md](version.md) |
| `wireless` | 14 | [wireless.md](wireless.md) |

Each namespace page is generated from the normalized public specification. The machine-readable source is [`../specification/methods.json`](../specification/methods.json).
## How to read a method entry

Each method entry separates four different questions:

- **Operation type** — whether the method behaves like a read, write/action, authentication operation, scan/export operation, or engineering read.
- **Verification** — how strongly the method itself was confirmed. See [`../docs/method-status.md`](../docs/method-status.md).
- **Auth evidence** — how well the privilege boundary was independently characterized. `UNTESTED` does not mean anonymous access.
- **Safety** — whether the method is low-impact, state-changing, disruptive, or intentionally not exercised for coverage.

Request and response schemas are intentionally conservative: fields are documented when they were observed or reconstructed with sufficient evidence. Missing fields should not be interpreted as proof that the firmware can never return additional data.

