<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# AGENTS.md

Guidance for AI coding agents and automated contributors working in this repository.

This file applies to the entire repository. If a future subdirectory contains a more specific `AGENTS.md`, follow the nearest applicable file for work in that subtree.

## Project role

`nr2301-api` is the public protocol source of truth for the independently reverse-engineered local management API of the Zyxel NR2301.

Architecture:

```text
nr2301-api        protocol evidence and public contract
    ↓
nr2301-python     reusable Python SDK
    ↓
consumer apps / integrations / tools
```

Do not make the SDK or a consumer application the source of protocol truth.

## Core rule: evidence before convenience

Never invent protocol semantics because they look plausible or make an API nicer.

Before changing a request shape, response shape, enum, raw value, transport rule or safety classification, identify the evidence supporting it. Preserve uncertainty when evidence is incomplete.

Relevant evidence/status concepts include:

- `LIVE_VERIFIED`
- `LIVE_VERIFIED_LIMITED`
- `LIVE_DENIED`
- `LIVE_REJECTED`
- `LIVE_NOT_APPLICABLE`
- `STATIC_CONFIRMED`
- `NOT_IMPLEMENTED`

Do not silently promote static evidence to live verification.

## Canonical public files

Protocol changes normally need to stay synchronized across the relevant layers:

- `specification/methods.json`
- `specification/semantics.json`
- generated/human-readable namespace pages under `api/`
- task-oriented documentation under `docs/recipes/`
- `CHANGELOG.md`

A machine-readable contract and its human-readable documentation must not contradict each other.

## Release discipline

The published `v0.1.0` tag is immutable. Never move, rewrite or retarget an existing public release tag.

Development changes belong on `main` and must use the next development/release metadata. At the time this file was introduced, `main` uses `0.1.1.dev0` metadata.

Do not change a release identifier merely to satisfy a local edit unless the repository's release state actually changes.

## Validation

After modifying public API material, run:

```bash
python tools/validate_public_repo.py
```

The validator must pass before considering the change complete.

Do not weaken validation merely to make a failing change pass. Fix the underlying inconsistency unless the validator itself is demonstrably wrong.

## Request and response modeling

- HTTP 200 does not prove semantic API success.
- Do not globally stringify numeric values. The stock frontend often uses `toStringData=true`, but stringification is endpoint/field evidence, not a universal protocol rule.
- Preserve unknown response fields and unknown raw values.
- Do not create global enums from values that are only proven for one endpoint.
- Do not reuse integer meanings across unrelated methods just because the numbers match.
- If a complete write object is not reconstructed, document the limitation rather than filling gaps from guesses.

## Write safety

Use the documented safety classification when describing or testing a method:

- `READ_OR_LOW_SIDE_EFFECT`
- `WRITE_OR_SIDE_EFFECT`
- `DISRUPTIVE_RECOVERY_REQUIRED`
- `DO_NOT_TEST_FOR_COVERAGE`

Do not exercise dangerous operations merely to improve coverage.

Examples that require special caution or deliberate non-testing include factory reset, engineering/supervisor operations and SIM PIN/PUK mutation paths.

For disruptive writes, prefer evidence of the full lifecycle:

```text
read current state
→ preserve unrelated values
→ write
→ tolerate expected management interruption
→ recover/re-authenticate
→ read back
→ verify exact intended state
```

A lost HTTP response during a disruptive operation is inconclusive, not automatic failure or success.

## Known protocol pitfalls

### Wi-Fi

Verified mode tokens on the tested ACIY.3 firmware include:

- `DUAL`
- `DUAL GUEST`
- `2.4G 5G`
- `2.4G 5G GUEST`

`DUAL` means a combined/shared main SSID for 2.4 and 5 GHz in the verified frontend contract. Do **not** rename it to "Band Steering" unless steering behavior is separately proven.

Guest enable/disable is represented by the `GUEST` token in the top-level mode. There is no independently verified Guest-enable field.

Do not expose Guest `isolate` as independently round-trippable on ACIY.3: the getter does not return it as an independent Guest value.

### SMS

Normal SMS send and single-ID delete are live verified and normalized on `main`.

For normal SMS send, preserve the documented frontend contract including GSM7 detection, UTF-16BE uppercase hexadecimal body representation, trailing-comma address format, timestamp representation and endpoint-specific success fields.

Never include real SMS bodies or real phone numbers in public fixtures, logs or examples.

### SIM

Read-only status is documented. PIN/PUK mutation paths remain deliberately outside normal coverage unless new, explicit evidence and a safe test plan justify changing that status.

### Client/MAC filtering

Allow/block semantics depend on current filter mode. Do not model `set_allow` or `set_forbidden` as context-free CRUD without reading the documented mode semantics and recovery requirements.

## Historical implementation evidence

Earlier private applications and research captures may contain valid implementation evidence that was not fully normalized in an older public release.

When a newer SDK or consumer appears to have lost a previously working feature:

1. compare against the canonical reverse-engineering evidence and historical implementation;
2. decide whether the old behavior is sufficiently evidenced;
3. if yes, normalize the protocol fact here first;
4. only then update downstream SDKs/consumers.

Historical code is evidence, not automatically canonical truth. Never copy an old implementation into the public contract without re-checking what was actually proven.

## Privacy and publication hygiene

Never commit or publish real deployment secrets or private runtime identifiers, including:

- router/admin passwords or session cookies
- Wi-Fi keys
- VPN/DDNS credentials
- configuration backups containing secrets
- SMS contents or real phone numbers
- SIM/subscriber identifiers such as IMSI/ICCID
- IMEI/serial identifiers from a real private device
- live private MAC/IP identifiers from the maintainer's environment

Use synthetic values and documentation-reserved addresses where examples need concrete data.

## Attribution and licensing

Documentation and the machine-readable API specification are licensed under CC BY-SA 4.0 unless a file states otherwise. Repository tooling/software is GPL-3.0-or-later.

Preserve existing SPDX identifiers, attribution and copyright notices.

## Definition of done

A protocol change is not complete until:

1. the evidence level is explicit;
2. machine-readable and human-readable contracts agree;
3. safety implications are documented;
4. private data has been excluded;
5. `python tools/validate_public_repo.py` passes;
6. `CHANGELOG.md` is updated when the public development contract materially changes;
7. downstream SDK changes, if needed, are made only after this repository contains the corresponding protocol truth.
