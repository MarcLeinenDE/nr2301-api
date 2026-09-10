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

`phonebook/delete_pb` successfully deleted a synthetic local contact in the first lifecycle run using:

```json
{
  "delete_pb": {
    "location": "0",
    "count": "1",
    "indexarray": "<index>"
  }
}
```

The first run verified absence after deletion.

## `update_pb` field-specific behavior

A second hardened run tested four candidate request shapes with isolated synthetic contacts.

### Nested full strings

- response: `result = 0`
- same contact index remained present
- target `name`: not observed
- target `mobile`: observed
- target `email`: not observed
- group matched, but group was intentionally unchanged in this probe
- no copy-on-update row observed

Classification: partial field update.

### Nested full with integer location/index/group

Same observed behavior as nested full strings: `result = 0`, target mobile observed, target name/email not observed, no copy row.

### Nested minimal strings

Same observed behavior: `result = 0`, target mobile observed, target name/email not observed, no copy row.

### Flat request fields

- response: `result = -5`
- target name/mobile/email not observed

The nested `update_pb` object is therefore required; a flat payload is rejected on the tested firmware.

Important: `result = 0` must not be treated as proof that all supplied `update_pb` fields were applied. Field-level read-back is required until the exact firmware behavior is resolved.

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

The second profiler run exposed a profiler defect: final local contact count was five while the initial count was zero, but the profiler still printed `PASS` because the old cleanup relied on synthetic name prefixes and only treated prefix presence as fatal. The five new indexes reported during the run were 3, 4, 5, 6 and 7.

This is test-harness evidence, not an API semantic conclusion. Follow-up tooling must track new indexes relative to the pre-run index set and must require final cardinality/index-set restoration before reporting PASS.
