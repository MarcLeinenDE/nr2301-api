# Phonebook recipes

Detailed reference: [`phonebook`](../../api/phonebook.md).

The NR2301 phonebook API covers local contacts, SIM contacts and contact groups.

## List groups

GET `phonebook/query_group`.

The response includes group `index`, `name`, `desc`, `valid` and `contactcount` fields.

## Create, rename and delete a group

Create:

```json
{
  "name": "Example group"
}
```

with POST `phonebook/addnew_group`.

Rename/update:

```json
{
  "name": "Renamed group",
  "index": "3"
}
```

with POST `phonebook/update_group`.

Delete:

```json
{
  "index": "3"
}
```

with POST `phonebook/delete_group`.

All three shapes were physically confirmed on ACIY.3 with synthetic groups and read-back through `query_group`.

## List contacts by storage location

POST `phonebook/getcontactbylocation`:

```json
{
  "getcontactbylocation": {
    "pagecap": 50,
    "pageindex": 0,
    "location": 0
  }
}
```

The response returns `contactcount` and `contactlist`.

For local contacts, raw `name` is the WebUI `UniEncode()` representation. The shipped WebUI applies `UniDecode()` before display. On the tested ACIY.3 read path, `email` was observed as `"-"` and `home`/`office` as `None` even when values had been submitted.

## List contacts by group

POST `phonebook/getcontactbygroup`:

```json
{
  "getcontactbygroup": {
    "group": "0",
    "pagecap": "50",
    "pageindex": "0"
  }
}
```

`group`, `pagecap` and `pageindex` are strings on the physically confirmed wire shape.

## Contact text codec

Before add/update, the shipped WebUI runs `UniEncode()` on contact `name` and `email`. Each JavaScript UTF-16 code unit becomes four lowercase hexadecimal characters. `mobile`, `home` and `office` remain plain strings.

Examples:

```text
Example   -> 004500780061006d0070006c0065
ÄÖÜßé€2   -> 00c400d600dc00df00e920ac0032
```

On read, use the inverse four-hex-character `UniDecode()` operation for encoded contact names. Do not apply this codec to phone-number fields.

## Add a local contact

POST `phonebook/addnew_pb` with a nested object:

```json
{
  "addnew_pb": {
    "location": "0",
    "name": "004500780061006d0070006c0065",
    "mobile": "0123456789",
    "home": "",
    "office": "",
    "email": "006500780061006d0070006c00650040006500780061006d0070006c0065002e0069006e00760061006c00690064",
    "group": "0"
  }
}
```

On ACIY.3 this returned `result = 0` and produced a new local-contact index. A correctly encoded synthetic name round-tripped exactly and decoded to the submitted human-readable name. `mobile` also round-tripped exactly. Correctly encoded email still read back as `"-"`; non-empty `home`/`office` inputs read back as `None`.

## Update a local contact

POST `phonebook/update_pb` with the same nested contact fields plus `index`:

```json
{
  "update_pb": {
    "location": "0",
    "index": "41",
    "name": "00c400d600dc00df00e920ac0032",
    "mobile": "0123456789",
    "home": "",
    "office": "",
    "email": "006500780061006d0070006c00650040006500780061006d0070006c0065002e0069006e00760061006c00690064",
    "group": "0"
  }
}
```

The nested wrapper is required on tested firmware; the flat candidate returned `result = -5`.

Corrected physical testing established:

- `name` is physically mutable when `UniEncode()`-encoded, including Unicode;
- `mobile` is physically mutable;
- `group` is physically mutable;
- `email` remained `"-"` on the observed read path;
- `home` and `office` remained `None` on the observed read path.

The earlier plaintext-name update result is superseded because plaintext does not match the WebUI wire contract. Treat `result = 0` as endpoint acceptance, not proof that every supplied field became visible in read-back.

## Delete one local contact

The physically confirmed single-contact delete is:

```json
{
  "delete_pb": {
    "location": "0",
    "count": "1",
    "indexarray": "14"
  }
}
```

Related backend code parses `indexarray` by splitting on commas, so a comma-separated multi-index form is strongly supported statically. Physical NR2301 multi-delete confirmation remains a separate evidence step before a plural SDK helper is frozen.

## Move one contact to a group

The physically confirmed single-contact request is:

```json
{
  "newgroup": "4",
  "contacts": "14"
}
```

POST to `phonebook/move_contacts_to_group`. Both values are scalar strings. Verify with both the target-group view and the contact's local `group` field. Multi-contact representation remains to be established physically.

## Copy SIM contacts to local storage

GET `phonebook/copyallfromsimtolocal`.

The response can report `sim_count`, `count`, `duplicate`, `failed` and `invalid`. Treat duplicate/failed counts separately instead of using one generic success boolean.

## Test/restore discipline

For synthetic write testing, snapshot the initial local-contact index set. Treat every new index as test-owned and delete it during cleanup. A run is restored only when the final index set and cardinality exactly match the initial baseline.

## Privacy

Names and phone numbers are personal data. Synthetic fixtures are preferred; sanitize real contact payloads before including them in logs, fixtures or bug reports.
