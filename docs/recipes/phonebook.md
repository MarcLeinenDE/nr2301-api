# Phonebook recipes

Detailed reference: [`phonebook`](../../api/phonebook.md).

The NR2301 phonebook API covers local contacts, SIM contacts and contact groups.

## List groups

GET `phonebook/query_group`.

The response includes group `index`, `name`, `desc`, `valid` and `contactcount` fields.

## Create a group

POST `phonebook/addnew_group` with:

```json
{
  "name": "Example group"
}
```

Refresh `query_group` and locate the new group.

## Rename/update a group

POST `phonebook/update_group` with `name` and the existing group `index`, then refresh the group list.

## Delete a group

POST `phonebook/delete_group` with the target `index`, then verify it is absent from `query_group`.

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

The response returns `contactcount` and `contactlist`. Known item fields include `index`, `location`, `group`, `name` and `mobile`.

## List contacts by group

Use `phonebook/getcontactbygroup` with the frontend-shaped `getcontactbygroup` request object.

## Add/update/delete a contact

- add: `phonebook/addnew_pb` with an `addnew_pb` object
- update: `phonebook/update_pb` with an `update_pb` object
- delete: `phonebook/delete_pb` with a `delete_pb` object

These methods are live verified, but the nested contact request structures are not yet fully normalized in the public method pages. Preserve the actual frontend/current object shape rather than inventing field names.

After every change, query the relevant storage/group view and verify the record.

## Move contacts to a group

Use `phonebook/move_contacts_to_group` with:

- `newgroup`
- `contacts`

Refresh both the source/target views after the operation.

## Copy SIM contacts to local storage

GET `phonebook/copyallfromsimtolocal`.

The response can report `sim_count`, `count`, `duplicate`, `failed` and `invalid`. Treat duplicate/failed counts separately instead of using one generic success boolean.

## Privacy

Names and phone numbers are personal data. Sanitize contact payloads before using them as fixtures or including them in bug reports.