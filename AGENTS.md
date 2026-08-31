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

## Project target: complete evidenced coverage

The long-term target is to reconstruct and document the complete locally reachable NR2301 management API and to make every sufficiently reconstructed method usable from `nr2301-python`.

This is not permission to invent missing request fields or semantics. Instead, incomplete methods are research work items: use static/frontend evidence, historical captures and the dedicated physical test router to complete their contracts where feasible.

When a downstream SDK test produces new protocol evidence, this repository must be updated as part of the same work stream. In particular:

- a successfully exercised method previously marked `STATIC_CONFIRMED` or otherwise not live verified must be promoted to the appropriate live verification status;
- newly observed request fields, response fields, raw values, result semantics, transport behavior and recovery behavior must be normalized here;
- rejected, denied, not-applicable or not-implemented outcomes must also be recorded rather than hidden by the SDK;
- only after the protocol truth is represented here should downstream helpers be considered complete.

The API and SDK are therefore developed iteratively, but protocol findings always flow back into `nr2301-api`.

## Dedicated physical test router authority

The maintainer has explicitly designated the current NR2301 as a **non-production test device**. It is connected to the test PC through USB and may be used for deliberate read, write, disruptive and recovery testing.

Recovery assumptions for this device:

- configuration loss is acceptable during planned testing;
- a physical factory-reset button is available as the final recovery path;
- tests should still capture/read current state and restore it when practical, because successful restore behavior is valuable protocol evidence.

### Current hard exclusion: USB management mode

Do **not** change the router's USB/management mode (including engineering USB-mode setters) during routine API/SDK coverage work. Losing the USB management path could remove the very recovery/control channel used for the test campaign.

Reading USB-mode state is acceptable when already authorized and non-disruptive. A future explicit test plan may change this exclusion, but the general permission to test the dedicated router does not implicitly authorize USB-mode mutation.

### Test levels

Use explicit levels rather than treating every write equally:

1. **read-only** — no configuration mutation;
2. **reversible write** — state is read first and restored/verified afterwards;
3. **disruptive/recovery** — connectivity or service interruption is expected and a recovery path is prepared;
4. **destructive/reset** — configuration loss or factory reset can occur and is deliberately accepted.

Safety classifications remain important documentation and planning metadata. They are not permanent bans on testing this dedicated device. Methods marked `DO_NOT_TEST_FOR_COVERAGE` require a specific scenario and recovery rationale rather than broad automated probing.

Authorization boundaries still matter: do not brute-force or repeatedly guess supervisor/engineering credentials merely because the device can be reset.

## Jurisdiction-neutral capability documentation

The API contract is global and must not hard-code Germany-, EU-, FCC-, or other jurisdiction-specific Wi-Fi channel, band or transmit-power policy merely because the maintainer or physical test router is located in one jurisdiction.

Document the raw capabilities, option tokens, firmware regulatory-domain behavior and acceptance/rejection results that are actually evidenced. A documented capability is **not** a claim that using it is lawful in every country or deployment.

Do not invent unsupported radio values and do not bypass firmware/hardware enforcement. If firmware rejects or masks a value, record that behavior. Deployment-specific legal/regulatory policy belongs to the consumer/integrator/operator and/or the router firmware's regulatory domain, not to the protocol abstraction itself.

Physical lab testing on the dedicated non-production router may exercise evidenced or deliberately exploratory router-accepted radio settings to establish the technical contract. Clearly distinguish WebUI-proven enums, live-accepted values and unresolved exploratory values.

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

Do not silently promote static evidence to live verification. Conversely, when a physical SDK/API test genuinely establishes live behavior, do not leave the public status stale.

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
- If a complete write object is not reconstructed, document the limitation and use the dedicated test router to close the gap where a deliberate test is possible rather than filling it from guesses.

## Write and recovery discipline

For reversible/disruptive writes, prefer evidence of the full lifecycle:

```text
read current state
→ preserve unrelated values
→ write the smallest evidenced change
→ tolerate expected management interruption
→ recover/re-authenticate
→ read back
→ verify exact intended state
→ restore original state when practical
→ verify the restore
```

A lost HTTP response during a disruptive operation is inconclusive, not automatic failure or success.

Factory reset is available as a final recovery mechanism on the dedicated test router, but it should not replace ordinary read-back/restore evidence where a reversible test is possible.

## Known protocol pitfalls

### Authentication

The administrator challenge flow has historical live-working evidence, but physical SDK retests can reveal environment/state-dependent behavior. Treat `result` meanings as endpoint-specific. In particular, do not transfer the `account/login` result table to `account/get_rand` without separate evidence.

### Wi-Fi

Verified mode tokens on the tested ACIY.3 firmware include:

- `DUAL`
- `DUAL GUEST`
- `2.4G 5G`
- `2.4G 5G GUEST`

`DUAL` means a combined/shared main SSID for 2.4 and 5 GHz in the verified frontend contract. Do **not** rename it to "Band Steering" unless steering behavior is separately proven.

Guest enable/disable is represented by the `GUEST` token in the top-level mode. There is no independently verified Guest-enable field.

Do not expose Guest `isolate` as independently round-trippable on ACIY.3 until new physical evidence closes the getter/setter asymmetry.

### SMS

Normal SMS send and single-ID delete are live verified and normalized on `main`.

For normal SMS send, preserve the documented frontend contract including GSM7 detection, UTF-16BE uppercase hexadecimal body representation, trailing-comma address format, timestamp representation and endpoint-specific success fields.

Never include real SMS bodies or real phone numbers in public fixtures, logs or examples. Physical SMS testing may use controlled real values locally, but sanitize the published evidence.

### SIM

Read-only status is documented. PIN/PUK paths are eligible for deliberate testing on the dedicated non-production router when a specific safe scenario exists, but they must not be broad/probabilistic coverage tests that risk exhausting retries without a recovery plan.

### Client/MAC filtering

Allow/block semantics depend on current filter mode. Do not model `set_allow` or `set_forbidden` as context-free CRUD. Physical verification must preserve a management/recovery path and should test restore behavior.

## Historical implementation evidence

Earlier private applications and research captures may contain valid implementation evidence that was not fully normalized in an older public release.

When a newer SDK or consumer appears to have lost a previously working feature:

1. compare against the canonical reverse-engineering evidence and historical implementation;
2. decide whether the old behavior is sufficiently evidenced;
3. if yes, normalize the protocol fact here;
4. implement/test it downstream;
5. feed any new physical result back here, including changed verification status or corrected semantics.

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

The dedicated physical router may expose these values locally during testing. Redact/sanitize them before committing evidence, logs, fixtures or documentation. Use synthetic values and documentation-reserved addresses where examples need concrete data.

## Attribution and licensing

Documentation and the machine-readable API specification are licensed under CC BY-SA 4.0 unless a file states otherwise. Repository tooling/software is GPL-3.0-or-later.

Preserve existing SPDX identifiers, attribution and copyright notices.

## Definition of done

A protocol change or physical verification step is not complete until:

1. the evidence level is explicit and reflects the newest physical result;
2. machine-readable and human-readable contracts agree;
3. safety/recovery implications are documented;
4. private data has been excluded from public artifacts;
5. `python tools/validate_public_repo.py` passes;
6. `CHANGELOG.md` is updated when the public development contract materially changes;
7. downstream SDK changes, if needed, are aligned with this repository;
8. any new SDK-derived protocol evidence has been fed back into this repository rather than remaining SDK-only.
