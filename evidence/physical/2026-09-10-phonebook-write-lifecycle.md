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

## `addnew_pb` create-time read-back behavior

The final field-specific profiler started from zero local contacts and created one isolated synthetic contact per field probe. All requested values were synthetic.

On ACIY.3, the immediate local-contact read-back behaved as follows:

- `mobile`: exact requested string round-tripped.
- `group`: exact requested group round-tripped as an integer.
- `home`: requested non-empty value did not round-trip; read-back was `None`.
- `office`: requested non-empty value did not round-trip; read-back was `None`.
- `name`: returned a non-empty string, but it was not byte-for-byte/equality-identical to the plain synthetic input used by the profiler.
- `email`: returned a non-empty string, but it was not byte-for-byte/equality-identical to the plain synthetic input used by the profiler.

The exact create-time transformation/representation of `name` and `email` is not established by this run and must not be guessed. The result is sufficient to distinguish create/read representation effects from later `update_pb` effects.

## `update_pb` request shape and field-specific behavior

A hardened lifecycle run first tested several candidate request shapes. The nested `update_pb` object was accepted; a flat payload returned `result = -5`.

Confirmed nested shape:

```json
{
  "update_pb": {
    "location": "0",
    "index": "<contact-index>",
    "name": "<name>",
    "mobile": "<mobile>",
    "home": "<home>",
    "office": "<office>",
    "email": "<email>",
    "group": "<group-index>"
  }
}
```

The final observed-baseline profiler changed one field at a time. Every probe returned `result = 0`, retained the same contact index, created no copy row, and kept every non-target field stable relative to the actual create-time read-back.

Final per-field result on ACIY.3:

- `name`: target not reached; observed value stayed equal to its create-time baseline. **No visible update effect.**
- `mobile`: target reached and differed from baseline. **Update physically effective.**
- `home`: target not reached; observed value stayed at its create-time `None` baseline. **No visible update effect.**
- `office`: target not reached; observed value stayed at its create-time `None` baseline. **No visible update effect.**
- `email`: target not reached; observed value stayed equal to its create-time baseline. **No visible update effect.**
- `group`: target reached and differed from baseline. **Update physically effective.**

Therefore `result = 0` must not be treated as proof that all supplied contact fields were applied. On tested firmware, only `mobile` and `group` are physically confirmed mutable through this endpoint. The other accepted fields remain part of the wire contract but have no visible update effect in this firmware state.

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

## Profiler cleanup finding and recovery

An intermediate lifecycle profiler exposed a harness defect: final local contact count was five while the initial count was zero, but the old profiler still printed `PASS` because cleanup relied on synthetic name prefixes. The five new indexes were `3,4,5,6,7`.

A dedicated cleanup verified that the complete local index set was exactly those five indexes, deleted every index individually with `result = 0`, verified each absent, and restored the known baseline of zero local contacts.

The final field-specific profiler then created indexes `14` through `19` one at a time, deleted each after its probe, ended with an index set exactly equal to the initial empty set, and removed both synthetic groups. Final output included `FINAL_INDEX_SET_MATCH = True` and `FINAL_SYNTHETIC_GROUP_PRESENT = False`.

The corrected research rule is therefore: track synthetic contacts by index delta from the pre-run set and require exact final index-set/cardinality restoration before reporting PASS.
