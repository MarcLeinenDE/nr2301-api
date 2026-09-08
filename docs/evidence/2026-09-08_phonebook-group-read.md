# Phonebook group-read evidence — 2026-09-08

Target: Zyxel NR2301, tested firmware family `V1.00(ACIY.3)C0`, normal administrator session.

A sanitized read-only probe tested the previously incomplete nested request contract for `phonebook/getcontactbygroup`.

## Confirmed request

```json
{
  "getcontactbygroup": {
    "group": "<group index>",
    "pagecap": "1",
    "pageindex": "0"
  }
}
```

All three inner values were sent as strings.

## Observed response structure

The physical probe confirmed:

- top-level response is a JSON object
- `result` is an integer
- `contactcount` is an integer
- `contactlist` is a JSON list
- selected test group returned zero contact items

The probe intentionally did not print group names, contact names, phone numbers or contact-list contents.

## Evidence boundary

This establishes the nested request keys and string wire serialization on the tested NR2301 firmware. Because the selected group returned an empty list, this specific probe does not add new live evidence about non-empty contact item fields.

No phonebook state was changed.
