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

## Public SDK confirmation

The public `nr2301-python` helper `client.phonebook.contacts_by_group()` was then exercised against the same ACIY.3 router through a targeted read-only integration test. The helper selected a real group index from `query_group`, sent the normalized nested request, and validated the response structure without printing group names or contact contents.

```text
tests/integration/test_readonly_router.py::test_phonebook_group_read PASSED
1 passed, 12 deselected in 0.46s
```

This confirms the normalized request not only through a raw direct-call probe but also through the public SDK serialization path.

## Evidence boundary

This establishes the nested request keys and string wire serialization on the tested NR2301 firmware. Because the selected group returned an empty list, this specific probe does not add new live evidence about non-empty contact item fields.

No phonebook state was changed.
