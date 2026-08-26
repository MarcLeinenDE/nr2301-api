# Zyxel NR2301 local API — reverse-engineered reference

Unofficial documentation of the local management API used by the **Zyxel NR2301** web interface.

This repository is intended as a vendor-independent technical reference for people building their own clients, scripts, integrations or applications. It deliberately does **not** contain a specific control application or a private router configuration.

> **Tested baseline:** Zyxel NR2301, firmware `V1.00(ACIY.3)C0`, hardware runtime `MIFI.NR2301.H01`.
> Other firmware versions may differ.

## Current coverage

The current catalog contains **157 unique API methods across 16 namespaces**. Coverage is intentionally evidence-based rather than presented as complete manufacturer documentation.

| Verification state | Methods |
|---|---:|
| `LIVE_VERIFIED` | 133 |
| `LIVE_VERIFIED_LIMITED` | 4 |
| `LIVE_DENIED` | 3 |
| `LIVE_REJECTED` | 1 |
| `LIVE_NOT_APPLICABLE` | 2 |
| `STATIC_CONFIRMED` | 12 |
| `NOT_IMPLEMENTED` | 2 |
| **Total** | **157** |

In addition, the repository documents the administrator authentication/session flow, single-call and multicall transport, endpoint-scoped raw-value semantics, safety classifications and a machine-readable method catalog.

`157 methods` means 157 distinct methods have been normalized into the catalog. It does **not** mean that every request/response field, privilege boundary, side effect or firmware variant is fully understood. Each method therefore carries its own evidence state and notes.

## Start here

1. [Getting started](docs/getting-started.md)
2. [Authentication](docs/authentication.md)
3. [Transport](docs/transport.md)
4. [Multicall](docs/multicall.md)
5. [Method verification status](docs/method-status.md)
6. [Raw values and semantics](docs/raw-values.md)
7. [Security and safety](docs/security-safety.md)
8. [API namespace index](api/README.md)

## Core endpoint

A normal single API call uses:

```text
/api.cgi?path=<namespace>&method=<method>&timeout=<seconds>
```

Authenticated calls use the `CGISID` session cookie established by `account/login`.

The stock frontend's observed transport rule is:

- request body present → HTTP `POST` with JSON
- no request body → HTTP `GET`

This is an observed implementation rule, not a guarantee that every method accepts both forms.

## Evidence model

Every method carries a verification state. `LIVE_VERIFIED` means the method was successfully exercised on the tested physical router. `STATIC_CONFIRMED` means the method is referenced by the shipped frontend/firmware but was not deliberately live-executed. See [method-status.md](docs/method-status.md) before relying on a write/action method.

## Safety

Some API calls can disconnect Wi-Fi, alter LAN addressing, reboot or factory-reset the router, send SMS, change SIM PIN state, expose configuration data, or enable engineering/debug functions. The catalog therefore includes a `safety_class` and notes where live recovery/read-back was required.

Do not treat an HTTP `200` response as proof that a configuration change succeeded. For disruptive writes, reconnect and verify the resulting state.

## Machine-readable specification

- [`specification/methods.json`](specification/methods.json) — normalized method catalog
- [`specification/semantics.json`](specification/semantics.json) — endpoint-scoped raw-value mappings

These files are intended to be usable by SDKs and documentation tooling without making the SDK itself the source of truth.

## Compatibility and completeness

The reference is based on observations from a physical NR2301 running the tested firmware shown above, plus static analysis of the shipped web interface/runtime. Zyxel may change undocumented behavior between firmware releases.

When implementing a client:

- prefer fields and behaviors marked as live verified;
- preserve unknown values rather than inventing meanings;
- do not generalize endpoint-specific sentinel values to unrelated fields;
- treat write/action calls as firmware-sensitive until verified;
- report additional firmware evidence with exact version information when possible.

## Project scope

This repository documents the reverse-engineered API. Applications that consume the API (Android apps, desktop GUIs, Home Assistant integrations, etc.) should remain separate projects and use this repository as their reference.

## Project background and maintainer availability

This project started as a private spare-time reverse-engineering effort out of personal interest, primarily to understand the NR2301 well enough to build tools for my own use. I decided to publish the results so that other owners and developers can benefit from the research instead of having to repeat it from scratch.

Issues, corrections and pull requests are welcome. This is not a commercial project and there is no support or response-time commitment. I have a young child and limited spare time, so reviews and replies may sometimes take a while. Community contributions are nevertheless very welcome.

## Disclaimer and no warranty

This documentation is provided **AS IS**, without warranty of any kind. The API is undocumented by the manufacturer and was derived through independent reverse engineering and testing. Behaviour may differ between firmware versions and may change without notice.

Some API calls can modify configuration, interrupt connectivity, send messages, reboot the device, factory-reset it or expose sensitive configuration data. Use write/action methods at your own risk and verify the resulting state where practical.

This project is independent and is not affiliated with, endorsed by, or supported by Zyxel. Product and company names are trademarks of their respective owners. The licenses in this repository apply only to material that this project has the right to license; they do not grant rights to Zyxel firmware, trademarks or other third-party material.

## License

The repository intentionally uses copyleft licenses so that improvements to this project's published material can remain available to the community:

- **Documentation and machine-readable API specification:** [CC BY-SA 4.0](LICENSE.md)
- **Software/tooling in this repository:** [GPL-3.0-or-later](LICENSE.md)

Original work is attributed to **Marc Leinen**. See [`ATTRIBUTION.md`](ATTRIBUTION.md) and [`LICENSE.md`](LICENSE.md) for the exact scope and terms. Commercial use is permitted by these licenses; the ShareAlike/GPL obligations apply to covered adaptations and derivative works when they are shared or conveyed.
