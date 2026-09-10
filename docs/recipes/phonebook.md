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

The response returns `contactcount` and `contactlist`. Preserve contact item fields raw because firmware representation can differ by field.

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

## Add a local contact

POST `phonebook/addnew_pb` with a nested object:

```json
{
  "addnew_pb": {
    "location": "0",
    "name": "Example",
    "mobile": "0123456789",
    "home": "",
    "office": "",
    "email": "example@example.invalid",
    "group": "0"
  }
}
```

On ACIY.3 this returned `result = 0` and produced a new local-contact index. Create-time read-back exactly preserved `mobile` and `group`; non-empty synthetic `home`/`office` inputs read back as `None`, while synthetic `name`/`email` returned non-empty strings that were not equality-identical to the plain inputs used by the profiler. Do not guess a normalization for those fields; preserve raw values.

## Update a local contact

POST `phonebook/update_pb` with the same nested contact fields plus `index`:

```json
{
  "update_pb": {
    "location": "0",
    "index": "14",
    "name": "Example",
    "mobile": "0123456789",
    "home": "",
    "office": "",
    "email": "example@example.invalid",
    "group": "0"
  }
}
```

The nested wrapper is required on tested firmware; the flat candidate returned `result = -5`.

ACIY.3 field-isolated read-back established that `mobile` and `group` are physically mutable. `name`, `home`, `office` and `email` remained at their actual create-time baselines even though the endpoint returned `result = 0`. Treat `result = 0` as endpoint acceptance, not proof that every supplied field changed.

## Delete one local contact

The currently physical-confirmed delete contract is one contact per request:

```json
{
  "delete_pb": {
    "location": "0",
    "count": "1",
    "indexarray": "14"
  }
}
```

POST to `phonebook/delete_pb`, then verify the index is absent. Multi-index serialization remains a separate evidence task.

## Move one contact to a group

The physically confirmed single-contact request is:

```json
{
  "newgroup": "4",
  "contacts": "14"
}
```

POST to `phonebook/move_contacts_to_group`. Both values are scalar strings. Verify with both the target-group view and the contact's local `group` field. Multi-contact representation remains to be established.

## Copy SIM contacts to local storage

GET `phonebook/copyallfromsimtolocal`.

The response can report `sim_count`, `count`, `duplicate`, `failed` and `invalid`. Treat duplicate/failed counts separately instead of using one generic success boolean.

## Test/restore discipline

For synthetic write testing, snapshot the initial local-contact index set. Treat every new index as test-owned and delete it during cleanup. A run is restored only when the final index set and cardinality exactly match the initial baseline; name-prefix matching alone is not sufficient because write behavior can alter contact text representation.

## Privacy

Names and phone numbers are personal data. Synthetic fixtures are preferred; sanitize real contact payloads before including them in logs, fixtures or bug reports.
