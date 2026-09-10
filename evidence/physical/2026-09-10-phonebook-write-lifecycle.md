# Phonebook write lifecycle physical evidence — 2026-09-10

Device/firmware: Zyxel NR2301, tested firmware V1.00(ACIY.3)C0.
Authentication: normal administrator session.
Scope: synthetic local-phonebook data only. No SIM contacts and no USB-management-mode changes.

## Confirmed group lifecycle

Physical profiler runs confirmed all of the following with `result = 0` and read-back verification:

- `phonebook/addnew_group`
- `phonebook/update_group`
- `phonebook/delete_group`

Two synthetic groups were created, one was renamed, and both were later deleted. Final group count returned to the initial count.

## Confirmed local contact creation/deletion

`phonebook/addnew_pb` with the nested `addnew_pb` object successfully created synthetic local contacts and returned `result = 0`.

`phonebook/delete_pb` successfully deleted synthetic local contacts using:

```json
{
  "delete_pb": {
    "location": "0",
    "count": "1",
    "indexarray": "<index>"
  }
}
```

A dedicated cleanup run subsequently started from exactly five local contacts with indexes `3,4,5,6,7`, deleted each index individually with `result = 0`, verified each index absent after deletion, and ended with zero local contacts. This restored the known pre-profiler baseline exactly.

## `update_pb` field-specific behavior

A hardened lifecycle run tested four candidate request shapes with isolated synthetic contacts.

### Nested full strings

- response: `result = 0`
- same contact index remained present
- target `name`: not observed
- target `mobile`: observed
- target `email`: not observed
- group matched, but group was intentionally unchanged in this probe
- no copy-on-update row observed

### Nested full with integer location/index/group

Same observed behavior as nested full strings: `result = 0`, target mobile observed, target name/email not observed, no copy row.

### Nested minimal strings

Same observed behavior: `result = 0`, target mobile observed, target name/email not observed, no copy row.

### Flat request fields

- response: `result = -5`
- target name/mobile/email not observed

The nested `update_pb` object is therefore required; a flat payload is rejected on the tested firmware.

Important: `result = 0` must not be treated as proof that all supplied `update_pb` fields were applied. Field-level read-back is required.

## Dedicated field-specific `update_pb` run

A later field-specific profiler started from zero local contacts and created one isolated synthetic contact per field probe. Each probe used a nested `update_pb` object and cleaned its newly-created index afterwards. The final local index set matched the initial empty baseline, and both synthetic groups were removed.

Observed per-field results:

- `name`: `result = 0`, same index remained, requested target name was not observed.
- `mobile`: `result = 0`, same index remained, requested target mobile was observed.
- `home`: `result = 0`, same index remained, requested target home was not observed; observed home was empty after the update.
- `office`: `result = 0`, same index remained, requested target office was not observed; observed office was empty after the update.
- `email`: `result = 0`, same index remained, requested target email was not observed.
- `group`: `result = 0`, same index remained, requested target group was observed.

The first version of this field profiler reported `BASELINE_EXACT = False` for every probe. That means at least one field already differed from the requested create payload before each update. Therefore the first field-specific run is sufficient to confirm that target `mobile` and target `group` were reached, and that target name/home/office/email were not reached, but it is not sufficient to prove whether the latter fields were unchanged, cleared, or normalized relative to their actual create-time values.

A follow-up profiler revision now records per-field create-baseline match/empty/type flags and evaluates each update relative to the observed create baseline rather than the requested create payload.

## Confirmed `move_contacts_to_group`

The following representation was physically confirmed with both group-specific read-back and the local contact `group` field:

```json
{
  "newgroup": "<group-index>",
  "contacts": "<single-contact-index>"
}
```

Observed response: `result = 0`.

This confirms, for a single local contact on ACIY.3, that both `newgroup` and `contacts` may be scalar strings. The multi-contact representation is not yet established by this run.

## Profiler cleanup finding

The second lifecycle profiler run exposed a profiler defect: final local contact count was five while the initial count was zero, but the profiler still printed `PASS` because the old cleanup relied on synthetic name prefixes and only treated prefix presence as fatal. The five new indexes reported during the run were `3,4,5,6,7`.

A dedicated cleanup immediately afterwards verified that the complete current local index set was exactly those five indexes, then deleted them one-by-one with read-back. Final local contact count was zero and the final index set was empty.

This is test-harness evidence, not an API semantic conclusion. Follow-up tooling must track new indexes relative to the pre-run index set and must require final cardinality/index-set restoration before reporting PASS.
