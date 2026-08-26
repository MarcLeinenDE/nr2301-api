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

Known top-level request keys from the shipped frontend: `name`.

### Response

No stable response schema is currently documented.

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

Known top-level request keys from the shipped frontend: `addnew_pb`.

### Response

No stable response schema is currently documented.

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

Known top-level request keys from the shipped frontend: `index`.

### Response

Known/observed response fields: `result`.

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

Known top-level request keys from the shipped frontend: `delete_pb`.

### Response

Known/observed response fields: `result`.

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

Known top-level request keys from the shipped frontend: `getcontactbygroup`.

### Response

```json
{
  "contactcount": "integer",
  "contactlist": [
    "<empty>"
  ],
  "result": "integer"
}
```

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

```json
{
  "contactcount": "integer",
  "contactlist": [
    "<empty>"
  ],
  "result": "integer"
}
```

### Notes

- Live result=0, contactcount=0, contactlist empty. Static item fields: index, location, group, name, mobile. Anonymous live response: HTTP 200 {'system_err':'session no exist'}.

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

Known top-level request keys from the shipped frontend: `newgroup`, `contacts`.

### Response

Known/observed response fields: `result`.

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

Known top-level request keys from the shipped frontend: `name`, `index`.

### Response

No stable response schema is currently documented.

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

Known top-level request keys from the shipped frontend: `update_pb`.

### Response

No stable response schema is currently documented.

