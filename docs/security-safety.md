# Security and safety notes

The API is a privileged local management interface. A client can encounter or modify sensitive information such as Wi-Fi credentials, subscriber identifiers, SMS content, VPN credentials, SIM/PIN state and router configuration.

## Client implementation guidance

- Never log passwords, PIN/PUK values, SMS bodies, VPN secrets or full configuration backups.
- Treat responses containing IMEI/IMSI/ICCID/MDN, MAC addresses or phonebook data as sensitive.
- Keep session cookies out of diagnostics and crash reports.
- Require explicit user intent before disruptive or destructive actions.
- Read state back after writes when possible.
- Assume management connectivity may disappear after LAN/Wi-Fi/work-mode/reboot changes.

This repository intentionally contains schemas for sensitive fields but no captured live subscriber identifiers, credentials or personal messages.
