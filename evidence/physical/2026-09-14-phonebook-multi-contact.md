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

No real names, phone numbers, e-mail addresses or SIM-contact contents were used or committed.
