# Practical API recipes

The namespace pages under [`../../api/`](../../api/README.md) are the method-by-method reference. This directory adds a second, task-oriented layer for developers who start with a goal such as **change DNS**, **send an SMS**, **switch mobile network mode** or **rename a connected client**.

Recipes do not replace the method catalog. When a recipe and a method page differ, treat the current method page and machine-readable specification as the technical source of truth.

## Common rules

Before using a write/action method:

1. authenticate and preserve the `CGISID` session cookie;
2. read the current state first when a getter exists;
3. preserve fields you are not intentionally changing;
4. inspect the JSON result instead of trusting HTTP 200 alone;
5. for disruptive writes, reconnect/re-authenticate and read the affected state back;
6. never log credentials, SIM/subscriber identifiers, SMS content, Wi-Fi keys, VPN passwords/PSKs or configuration backups.

See [Authentication](../authentication.md), [Transport](../transport.md), [Multicall](../multicall.md) and [Security/safety](../security-safety.md).

## Find a task

| I want to… | Recipe |
|---|---|
| log in, keep a session alive, log out | [Authentication and session](authentication-session.md) |
| read hardware, firmware, battery, WAN, radio and diagnostics | [Device status and diagnostics](device-status-diagnostics.md) |
| change LTE/5G mode, roaming, reconnect mobile data or select an operator | [Mobile network](mobile-network.md) |
| manage the built-in VPN client profiles | [VPN client](vpn-client.md) |
| read/change Wi-Fi, Guest Wi-Fi, WPS or Wi-Fi extender state | [Wi-Fi, WPS and extender](wifi-wps-extender.md) |
| change LAN IP, DHCP, DNS or static DHCP reservations | [LAN, DHCP and DNS](lan-dhcp-dns.md) |
| configure WAN access, VPN passthrough, NAT/filters or UPnP | [Firewall and NAT](firewall-nat.md) |
| list clients, rename them or use MAC allow/block filtering | [Client management](client-management.md) |
| list, read, save, send or delete SMS | [SMS](sms.md) |
| manage local/SIM phonebook contacts and groups | [Phonebook](phonebook.md) |
| inspect SIM/PIN state and understand PIN/PUK operations | [SIM and PIN](sim-pin.md) |
| read/reset traffic counters or configure the data-package tracker | [Traffic and data package](traffic-data-package.md) |
| read or configure Dynamic DNS | [Dynamic DNS](ddns.md) |
| check OTA status and understand the update state machine | [Firmware/OTA](firmware-ota.md) |
| read or change TR-069 settings | [TR-069 and XMPP](tr069-xmpp.md) |
| reboot, schedule reboot, back up config, change UI language or power timeout | [System maintenance](system-maintenance.md) |

## Namespace coverage

Every current API namespace is represented by at least one recipe:

| Namespace | Primary recipe(s) |
|---|---|
| `account` | Authentication and session |
| `aoc` | Device status; System maintenance |
| `cm` | Mobile network; VPN client |
| `ddns` | Dynamic DNS |
| `firewall` | Firewall and NAT |
| `ota` | Firmware/OTA |
| `package` | Traffic and data package |
| `phonebook` | Phonebook |
| `router` | LAN/DHCP/DNS; Device status; System maintenance |
| `sim` | SIM and PIN |
| `sms` | SMS |
| `statistics` | Client management; Traffic and data package |
| `tr069` | TR-069 and XMPP |
| `util_wan` | Mobile network |
| `version` | Device status and diagnostics |
| `wireless` | Wi-Fi, WPS and extender |

Methods marked `STATIC_CONFIRMED`, `LIVE_REJECTED`, `NOT_IMPLEMENTED` or `DO_NOT_TEST_FOR_COVERAGE` are described as reference-only where appropriate; a recipe does not promote them to a verified safe workflow.