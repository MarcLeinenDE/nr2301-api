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

Physically confirmed nested local-contact shape; numeric values are strings on this write path. The shipped WebUI encodes `name` and `email` with `UniEncode()` before transport. `UniEncode()` writes each JavaScript UTF-16 code unit as four lowercase hexadecimal characters.

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

The example `name` decodes to `Example`; the example `email` decodes to `example@example.invalid`.

### Response

Observed `result = 0`; the new local contact index was visible through `getcontactbylocation`.

### Notes

- ACIY.3 physically round-tripped correctly `UniEncode()`-encoded `name`; decoding the raw read-back reproduced the original human-readable value exactly.
- `mobile` round-tripped exactly and `group` round-tripped as an integer.
- Correctly encoded synthetic `email` still read back as the literal string `"-"` on the observed local-contact read path.
- Non-empty `home` and `office` values read back as `None`.
- The earlier plaintext `name`/`email` probes are superseded: plaintext does not represent the shipped WebUI application-level contract for those fields.

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

Related backend source parses `indexarray` as a comma-separated string and parses `count` separately. This strongly supports the multi-contact shape but the NR2301 multi-index physical confirmation is tracked separately before a plural SDK helper is frozen.

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
- Synthetic local-contact runs confirmed item fields including `index`, `location`, `group`, `name`, `mobile`, `home`, `office` and `email` behavior.
- Raw local `name` is the WebUI `UniEncode()` representation and is decoded by the WebUI with `UniDecode()`.
- In the tested ACIY.3 state, local `email` read back as `"-"`, while `home` and `office` read back as `None` even when non-empty values were submitted.
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

Physically confirmed accepted nested shape. As with create, `name` and `email` must use the shipped WebUI `UniEncode()` representation:

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

The example `name` decodes to `ÄÖÜßé€2`. A flat object without the `update_pb` wrapper returned `result = -5` on ACIY.3.

### Response and firmware semantics

The corrected codec test returned `result = 0`, retained the same contact index, and created no copy row.

Physically confirmed on ACIY.3:

- `name`: **physically effective when `UniEncode()`-encoded**, including Unicode; raw read-back exactly matched `00c400d600dc00df00e920ac0032`, and `UniDecode()` reproduced `ÄÖÜßé€2`.
- `mobile`: **physically effective** as plain string.
- `group`: **physically effective** from the earlier isolated group-field test.
- `email`: correctly encoded input was accepted, but observed local read-back stayed `"-"`, unchanged from create baseline.
- `home`: non-empty input was accepted, but observed local read-back stayed `None`, unchanged from create baseline.
- `office`: non-empty input was accepted, but observed local read-back stayed `None`, unchanged from create baseline.

Therefore the earlier conclusion that `name` had no visible update effect is superseded; that result came from testing the field with the wrong plaintext wire representation. `result = 0` still must not be treated as proof of visible persistence for `email`, `home` or `office` on the tested firmware/read path.
