# Firewall filter empty-list read evidence — 2026-09-08

Target: Zyxel NR2301, tested firmware family `V1.00(ACIY.3)C0`, normal administrator session.

A sanitized read-only probe exercised the two lower-level firewall filter list getters through direct authenticated POST calls.

## IP filter

Request body:

```json
{
  "ww_ip_filter": {
    "list": []
  }
}
```

Method: `firewall/ww_read_ip_filter`.

Observed structure:

- top-level response: JSON object
- `firewall`: JSON object
- `firewall.list`: JSON list
- `firewall.setting_response`: string
- configured entry count on the tested router at probe time: `0`

## Port filter

Request body:

```json
{
  "ww_port_filter": {
    "list": []
  }
}
```

Method: `firewall/ww_read_port_filter`.

Observed structure:

- top-level response: JSON object
- `firewall`: JSON object
- `firewall.list`: JSON list
- `firewall.setting_response`: string
- configured entry count on the tested router at probe time: `0`

## Interpretation boundary

This evidence establishes that an empty list is a valid minimal read request body for both methods on the tested firmware and that direct authenticated POST dispatch succeeds under the normal administrator account.

It does **not** establish the item schema for non-empty IP/port filter lists. The public SDK must therefore preserve rule items raw rather than inventing a higher-level rule model until separate evidence normalizes those structures.

No firewall rule was added, edited, removed, enabled or disabled during this probe. No private IP addresses, ports or rule contents were printed or committed.