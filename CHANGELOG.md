# Changelog

## Unreleased

Development metadata: `0.1.1.dev0`.

- documented the administrator pre-login lockout guard using `account/get_retrytimes_and_time`
- normalized the known live-working login `user_id` compatibility shape as eight lowercase alphanumeric characters (`[a-z0-9]{8}`), reused across `account/get_rand` and `account/login`
- recorded the 2026-08-31 physical USB smoke observation that the initial public SDK's 32-character hexadecimal `user_id` reproducibly received `account/get_rand result=4` before password submission; the exact causal relationship remains subject to the corrected physical retest
- clarified that the documented 0..6 login result table is scoped to `account/login` and must not be applied automatically to `account/get_rand.result`
- normalized the exact live-verified `sms/sms.send` normal-SMS request and response contract, including GSM7 flagging, UTF-16BE hexadecimal body encoding, timestamp format, trailing-comma recipient representation and SMS-specific success fields
- normalized the exact live-verified `sms/sms.delete` single-ID request and success response; deletion had been verified for Draft, Inbox and Outbox, with Inbox/Outbox read-back
- promoted the already verified Wi-Fi mode tokens `DUAL`, `DUAL GUEST`, `2.4G 5G` and `2.4G 5G GUEST` into the machine-readable `wireless/wifi_set_ap_config` contract
- documented Guest enable/disable as presence/absence of the `GUEST` token, with disruptive recovery/read-back and preservation of the current Guest block
- documented the live-verified DUAL ↔ split transition with Guest preservation and exact final restore
- documented Guest `maxassoc` range/evidence and the ACIY.3 Guest-isolation round-trip limitation
- expanded the SMS and Wi-Fi task recipes so SDK/client implementers can use these contracts without relying on the earlier private application

The published `v0.1.0` tag remains immutable. These additions exist on `main` for the next API release.

## 0.1.0 — 2026-08-26

First public stable release of the reverse-engineered NR2301 local API reference.

Publication cleanup and task-oriented documentation after the release-candidate review:

- replaced the remaining canonical-repository placeholder in `ATTRIBUTION.md` with `https://github.com/MarcLeinenDE/nr2301-api`
- added the canonical repository link to the recommended attribution text
- extended `tools/validate_public_repo.py` to reject common publication placeholders, require the canonical attribution URL, verify recipe coverage and enforce matching machine-readable release metadata
- added GitHub Actions validation on pushes and pull requests to `main`
- added `docs/recipes/` as a task-oriented "How do I …?" layer covering all 16 API namespaces
- added detailed workflows for authentication, diagnostics, mobile network, VPN, Wi-Fi/WPS, LAN/DHCP/DNS, firewall/NAT, client management, SMS, phonebook, SIM/PIN, traffic/package tracking, DDNS, OTA, TR-069 and system maintenance
- documented the live-verified manual-DNS workflow (`auto`/`manual`, upstream DNS-proxy behavior and read-back/recovery pattern)
- linked the recipe index prominently from the root README and API namespace index
- finalized both machine-readable specifications as release `0.1.0`
- no API method IDs were added or removed by the recipe layer

## 0.1-rc3 — 2026-08-26

Public-documentation readability and consistency pass.

- expanded the README coverage table so all 157 methods are accounted for
- clarified that inventory coverage does not imply a complete contract for every method
- added firmware/completeness guidance for client implementers
- added a reading guide for operation type, verification, authorization evidence and safety
- removed internal raw `observed_status` labels from generated human-readable method pages; they remain available in the machine-readable specification
- corrected the public safety classification of `cm/get_vpn_client_connect_status` from `WRITE_OR_SIDE_EFFECT` to `READ_OR_LOW_SIDE_EFFECT`; the source baseline inconsistency is recorded for later canonical consolidation
- no request/response or raw-value semantics changed

## 0.1-rc2 — 2026-08-26

Publication-policy update to the initial release candidate.

- selected CC BY-SA 4.0 for documentation and the machine-readable API specification
- selected GPL-3.0-or-later for repository software/tooling
- added explicit attribution to Marc Leinen
- added project-background and limited-maintainer-availability notes
- strengthened the AS IS / no-warranty and independent-project disclaimer
- clarified that copyleft applies to covered project material and does not automatically relicense independently written API clients

No API method semantics changed in this RC update.

## 0.1-rc1 — 2026-08-26

Initial public release candidate derived from the frozen NR2301 reverse-engineering baseline.

- 157 API methods across 16 namespaces
- normalized live/static evidence model
- administrator challenge-login flow
- single-call and multicall transport
- endpoint-scoped raw-value semantics
- safety classes and disruptive-write notes
- machine-readable method and semantics catalogs

No SDK or consumer application is included in this repository.
