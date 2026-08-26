# Changelog

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
