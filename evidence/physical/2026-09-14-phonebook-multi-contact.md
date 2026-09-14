# Phonebook multi-contact physical evidence — 2026-09-14

Device/firmware: Zyxel NR2301, tested firmware V1.00(ACIY.3)C0.
Authentication: normal administrator session.
Scope: synthetic local-phonebook data and temporary groups only. No SIM mutation and no USB-management-mode mutation.

## Preconditions

- initial local contact count: `0`
- initial group count: `1`
- two temporary synthetic groups were created successfully

## Multi-contact move

Two synthetic local contacts were created in the first temporary group.

The first candidate used the comma-separated scalar-string representation:

```json
{
  "newgroup": "<target-group-index>",
  "contacts": "<contact-index-1>,<contact-index-2>"
}
```

Observed:

- `result = 0`
- both synthetic contacts read back in the target group
- target count = `2`
- no fallback candidate was required

Confirmed representation: `COMMA_STRING`.

## Multi-contact delete

Two fresh synthetic local contacts were created for the delete probe.

The first candidate used:

```json
{
  "delete_pb": {
    "location": "0",
    "count": "2",
    "indexarray": "<contact-index-1>,<contact-index-2>"
  }
}
```

Observed:

- `result = 0`
- remaining tested indexes = `0`
- both contacts were absent on read-back
- no fallback candidate was required

Confirmed representation: `COMMA_STRING`.

This matches the previously recorded related-backend static evidence that tokenizes `indexarray` on commas.

## Cleanup / restore

Both temporary groups were deleted with `result = 0`.

Final checks:

- final local contact count: `0`
- exact initial local index set restored: `True`
- exact initial group count restored: `True`
- profiler result: `PHONEBOOK_MULTI_CONTRACT_PROFILER = PASS`

## Public SDK high-level validation

After the raw contract was normalized, the permanent `nr2301-python` plural helpers were exercised through the public SDK surface on the same ACIY.3 device using Python 3.13.5.

`tests/integration/test_phonebook_multi_contact.py::test_phonebook_plural_helpers_move_delete_and_restore` passed **1/1 in 1.93 s**.

The high-level lifecycle:

- created two synthetic local contacts;
- called `client.phonebook.move_contacts_to_group([id1, id2], target_group)`;
- received `result = 0` and verified both contacts in the target group;
- called `client.phonebook.delete_contacts([id1, id2])`;
- received `result = 0` and verified both contacts absent;
- removed both temporary groups;
- finished with local contact count `0`;
- restored the exact initial local index set;
- restored the exact initial group count.

This confirms that the permanent plural SDK abstraction serializes the already-normalized comma-separated contracts correctly and preserves the required cleanup/recovery behavior.

No real names, phone numbers, e-mail addresses or SIM-contact contents were used or committed.
