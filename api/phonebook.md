# `phonebook` namespace

**11 methods** in the current public catalog.

Verification/auth/safety terminology: see [`../docs/method-status.md`](../docs/method-status.md).

| Method | Verification | Auth evidence | Safety |
|---|---|---|---|
| [`addnew_group`](#addnew-group) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`addnew_pb`](#addnew-pb) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`copyallfromsimtolocal`](#copyallfromsimtolocal) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`delete_group`](#delete-group) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`delete_pb`](#delete-pb) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`getcontactbygroup`](#getcontactbygroup) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`getcontactbylocation`](#getcontactbylocation) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`move_contacts_to_group`](#move-contacts-to-group) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`query_group`](#query-group) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`update_group`](#update-group) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`update_pb`](#update-pb) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |

<a id="addnew-group"></a>

## `addnew_group`

**Method ID:** `phonebook/addnew_group`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Physically confirmed ACIY.3 shape:

```json
{
  "name": "Example group"
}
```

### Response

Observed `result = 0`; read-back through `query_group` confirmed creation.

<a id="addnew-pb"></a>

## `addnew_pb`

**Method ID:** `phonebook/addnew_pb`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Physically confirmed nested local-contact shape; numeric values are strings on this write path:

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

### Response

Observed `result = 0`; the new local contact index was visible through `getcontactbylocation`.

### Notes

- ACIY.3 create-time read-back physically round-tripped `mobile` and `group` exactly.
- Non-empty `home` and `office` test values read back as `None`.
- Synthetic `name` and `email` read back as non-empty strings but not equality-identical to the plain synthetic inputs used by the profiler. Their exact transformation is not yet normalized; preserve raw read-back values.

<a id="copyallfromsimtolocal"></a>

## `copyallfromsimtolocal`

**Method ID:** `phonebook/copyallfromsimtolocal`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `GET`

No request body has been reconstructed as necessary for this method.

### Response

Known/observed response fields: `count`, `duplicate`, `failed`, `invalid`, `sim_count`.

### Notes

- Live result=0; sim_count=11, count=0, duplicate=11, failed=0, invalid=0. No local contacts were added in this runtime state.

<a id="delete-group"></a>

## `delete_group`

**Method ID:** `phonebook/delete_group`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Physically confirmed single-group shape:

```json
{
  "index": "3"
}
```

### Response

Known/observed response field: `result`. Synthetic groups returned `result = 0` and were absent on read-back.

<a id="delete-pb"></a>

## `delete_pb`

**Method ID:** `phonebook/delete_pb`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Physically confirmed single-local-contact shape:

```json
{
  "delete_pb": {
    "location": "0",
    "count": "1",
    "indexarray": "3"
  }
}
```

### Response

Known/observed response field: `result`. Multiple synthetic single-contact deletes returned `result = 0` and absence was verified after each call.

### Notes

The multi-index `indexarray` representation is not established by the current physical run; the exact evidence above is for one contact per request.

<a id="getcontactbygroup"></a>

## `getcontactbygroup`

**Method ID:** `phonebook/getcontactbygroup`  
**Endpoint:** `/api.cgi`  
**Operation type:** `READ`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `POST`

The 2026-09-08 ACIY.3 normal-admin probe confirmed:

```json
{
  "getcontactbygroup": {
    "group": "0",
    "pagecap": "1",
    "pageindex": "0"
  }
}
```

`group`, `pagecap` and `pageindex` are strings on the confirmed wire shape.

### Response

```json
{
  "contactcount": "integer",
  "contactlist": [],
  "result": "integer"
}
```

### Notes

The first group-read probe returned zero contacts; later synthetic write tests used this method successfully for group membership read-back without committing contact values.

<a id="getcontactbylocation"></a>

## `getcontactbylocation`

**Method ID:** `phonebook/getcontactbylocation`  
**Endpoint:** `/api.cgi`  
**Operation type:** `READ`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "getcontactbylocation": {
    "pagecap": 50,
    "pageindex": 0,
    "location": 0
  }
}
```

### Response

Known top-level fields: `contactcount`, `contactlist`, `result`.

### Notes

- Initial live result=0, contactcount=0, contactlist empty.
- Later synthetic local-contact runs confirmed item fields including `index`, `location`, `group`, `name`, `mobile`; `home`, `office` and `email` may also be present/represented by firmware and must be preserved raw.
- Anonymous live response: HTTP 200 `{'system_err':'session no exist'}`.

<a id="move-contacts-to-group"></a>

## `move_contacts_to_group`

**Method ID:** `phonebook/move_contacts_to_group`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Physically confirmed single-contact shape:

```json
{
  "newgroup": "4",
  "contacts": "7"
}
```

Both values are scalar strings in the confirmed ACIY.3 representation.

### Response

Observed `result = 0`.

### Notes

The move was confirmed both through `getcontactbygroup` and through the local contact's `group` field. Multi-contact representation remains to be established separately.

<a id="query-group"></a>

## `query_group`

**Method ID:** `phonebook/query_group`  
**Endpoint:** `/api.cgi`  
**Operation type:** `READ`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `GET`

No request body has been reconstructed as necessary for this method.

### Response

```json
{
  "grouplist": [
    {
      "contactcount": "integer",
      "desc": "string",
      "index": "integer",
      "name": "string",
      "valid": "integer"
    }
  ],
  "result": "integer"
}
```

<a id="update-group"></a>

## `update_group`

**Method ID:** `phonebook/update_group`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Physically confirmed shape:

```json
{
  "name": "Renamed group",
  "index": "3"
}
```

### Response

Observed `result = 0`; renamed synthetic group was confirmed through `query_group`.

<a id="update-pb"></a>

## `update_pb`

**Method ID:** `phonebook/update_pb`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Physically confirmed accepted nested shape:

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

A flat object without the `update_pb` wrapper returned `result = -5` on ACIY.3.

### Response and firmware semantics

Nested probes returned `result = 0`, retained the same contact index and created no copy row. Field-specific read-back relative to each contact's actual create-time baseline established:

- `mobile`: target applied — physically effective.
- `group`: target applied — physically effective.
- `name`: no visible change.
- `home`: no visible change; baseline/read-back was `None` in the tested create path.
- `office`: no visible change; baseline/read-back was `None` in the tested create path.
- `email`: no visible change.

Every non-target field remained stable in the isolated field probes. Therefore `result = 0` does not mean that every supplied field was applied. SDKs should preserve the complete evidenced wire object but document these tested-firmware semantics and use read-back when an exact mutation matters.
