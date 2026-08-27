# Contributing

Contributions are welcome when they improve reproducibility or firmware coverage.

For API claims, please state:

- NR2301 firmware version;
- whether the evidence is live, static frontend/firmware analysis, or inferred;
- exact namespace/method;
- request shape with all secrets and personal/device identifiers redacted;
- response schema or behavior;
- whether the operation has side effects;
- read-back/recovery result for disruptive writes.

Do not submit real credentials, session cookies, IMSI/ICCID/IMEI values, phone numbers, SMS content, private SSIDs, VPN secrets, full configuration backups, or unredacted captures.

## AI coding agents

AI coding agents and automated contributors should read [`AGENTS.md`](AGENTS.md) before changing protocol contracts. It documents the repository's evidence hierarchy, source-of-truth rules, safety boundaries, known protocol pitfalls, privacy requirements and definition of done.

The central rule is that protocol semantics must be supported by evidence and normalized in this repository before downstream SDKs or applications treat them as protocol truth.

## Maintainer availability

This is a personal spare-time project. The maintainer has a young child and limited free time, so there is no guaranteed response or review time for issues and pull requests. Please do not interpret a delayed response as rejection. Well-documented contributions that are easy to reproduce and review are especially helpful.

## Licensing of contributions

By submitting a contribution, you agree that your contribution may be distributed under the license that applies to the part of the repository you modify:

- documentation and API specification: **CC BY-SA 4.0**;
- software/tooling: **GPL-3.0-or-later**.

Please do not submit material that you do not have the right to contribute under those terms.
