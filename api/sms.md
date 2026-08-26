# `sms` namespace

**9 methods** in the current public catalog.

Verification/auth/safety terminology: see [`../docs/method-status.md`](../docs/method-status.md).

| Method | Verification | Auth evidence | Safety |
|---|---|---|---|
| [`sms.delete`](#smsdelete) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`sms.get_brief_info`](#smsget-brief-info) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`sms.get_by_id`](#smsget-by-id) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`sms.get_cds`](#smsget-cds) | `NOT_IMPLEMENTED` | `ADMIN_METHOD_NOT_FOUND` | `READ_OR_LOW_SIDE_EFFECT` |
| [`sms.get_config`](#smsget-config) | `NOT_IMPLEMENTED` | `ADMIN_METHOD_NOT_FOUND` | `READ_OR_LOW_SIDE_EFFECT` |
| [`sms.list_by_type`](#smslist-by-type) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`sms.query`](#smsquery) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`sms.save`](#smssave) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`sms.send`](#smssend) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |

<a id="smsdelete"></a>

## `sms.delete`

**Method ID:** `sms/sms.delete`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "sms": {
    "id": 123
  }
}
```

The stock frontend uses its default `toStringData=true`, so a numeric logical ID is serialized as a JSON string on the wire.

### Response

```json
{
  "sms": {
    "resp": 0,
    "smsDelSucc": 1,
    "smsDelFail": 0
  }
}
```

### Notes

- Exact frontend request: `{sms:{id:<message id>}}`.
- Single-ID delete was live verified for Draft, Inbox and Outbox.
- Verified success is `resp=0`, `smsDelSucc=1`, `smsDelFail=0`; Inbox/Outbox deletion was additionally confirmed by mailbox read-back with the ID absent.

<a id="smsget-brief-info"></a>

## `sms.get_brief_info`

**Method ID:** `sms/sms.get_brief_info`  
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
  "delivery_list": [
    "<empty>"
  ],
  "flash_msg_ids": [
    "<empty>"
  ],
  "memory_full": "integer",
  "new_num": "integer",
  "unread_num": "integer"
}
```

<a id="smsget-by-id"></a>

## `sms.get_by_id`

**Method ID:** `sms/sms.get_by_id`  
**Endpoint:** `/api.cgi`  
**Operation type:** `READ_WITH_SIDE_EFFECT`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `sms`.

### Response

```json
{
  "sms": {
    "address": "string",
    "body": "string",
    "contact_id": "integer",
    "date": "string",
    "id": "integer",
    "location": "integer",
    "protocol": "integer",
    "read": "integer",
    "resp": "integer",
    "status": "integer",
    "type": "integer"
  }
}
```

<a id="smsget-cds"></a>

## `sms.get_cds`

**Method ID:** `sms/sms.get_cds`  
**Endpoint:** `/api.cgi`  
**Operation type:** `READ`  
**Verification:** `NOT_IMPLEMENTED`  
**Auth evidence:** `ADMIN_METHOD_NOT_FOUND`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `GET`

```json
{}
```

### Response

Known/observed response fields: `cds_list`, `result`.

### Semantics

- **`sms.cds_status.v1`**
  - `evidence`: FRONTEND_SOURCE_VERIFIED
  - `field`: status
  - `note`: 0/1/2 all success-group; other failure-group. Do not reuse outbox.status enum.

### Notes

- Authenticated HTTP 200 returned non-JSON body of exactly 16 characters. Frontend expects JSON {result, cds_list[]}. Raw text was intentionally not retained; exact technical response remains to be rechecked. Anonymous live response: HTTP 200 {'system_err':'session no exist'}.

<a id="smsget-config"></a>

## `sms.get_config`

**Method ID:** `sms/sms.get_config`  
**Endpoint:** `/api.cgi`  
**Operation type:** `READ`  
**Verification:** `NOT_IMPLEMENTED`  
**Auth evidence:** `ADMIN_METHOD_NOT_FOUND`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `GET`

No request body has been reconstructed as necessary for this method.

### Response

Known/observed response fields: `sms`.

### Notes

- Normal admin session: HTTP 200 text/plain-like body 'Method not found'.

<a id="smslist-by-type"></a>

## `sms.list_by_type`

**Method ID:** `sms/sms.list_by_type`  
**Endpoint:** `/api.cgi`  
**Operation type:** `READ`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "sms": {
    "page_index": 1,
    "list_type": 0
  }
}
```

### Response

```json
{
  "sms": {
    "count": "integer",
    "node_list": {
      "s1": {
        "address": "string",
        "body": "string",
        "contact_id": "integer",
        "date": "string",
        "id": "integer",
        "location": "integer",
        "read": "integer",
        "status": "integer",
        "type": "integer"
      }
    },
    "page_count": "integer",
    "resp": "integer",
    "total": "integer"
  }
}
```

### Semantics

- **`sms.list.inbox`**
- **`sms.list.outbox`**
- **`sms.list.draft`**

### Notes

- Live resp=0,count=1,total=1,page_count=1. Raw SMS values were not stored. Anonymous live response: HTTP 200 {'system_err':'session no exist'}.

<a id="smsquery"></a>

## `sms.query`

**Method ID:** `sms/sms.query`  
**Endpoint:** `/api.cgi`  
**Operation type:** `READ`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "sms": {
    "type": 4,
    "read": 2,
    "location": 0
  }
}
```

### Response

```json
{
  "sms": {
    "ids": "string",
    "resp": "integer"
  }
}
```

### Semantics

- **`sms.query`**

### Notes

- Live contract/schema confirmed; tested query returned resp=-2. Frontend treats resp=0 as semantic success and ids as comma-separated IDs. Anonymous live response: HTTP 200 {'system_err':'session no exist'}.

<a id="smssave"></a>

## `sms.save`

**Method ID:** `sms/sms.save`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `sms`.

### Response

No stable response schema is currently documented.

<a id="smssend"></a>

## `sms.send`

**Method ID:** `sms/sms.send`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "sms": {
    "id": -1,
    "gsm7": 1,
    "address": "<recipient>,",
    "body": "<UTF-16BE uppercase hex>",
    "date": "26,8,25,6,23,57,%2B2",
    "protocol": "0"
  }
}
```

The stock frontend uses default `toStringData=true`; numeric request values such as `id` and `gsm7` are therefore stringified on the wire.

Field contract:

- `id`: `-1` for a new message.
- `gsm7`: `1` when all characters are in the GSM 03.38 basic/extension sets, otherwise `0`.
- `address`: comma-separated recipients with a trailing comma; a single recipient is therefore `<recipient>,`.
- `body`: frontend `UniEncode`, equivalent to UTF-16BE code units encoded as uppercase hexadecimal.
- `date`: local `YY,M,D,H,M,S,timezone`; the frontend encodes a positive timezone sign as `%2B`.
- `protocol`: normal SMS flow was live verified with `"0"`.

### Response

```json
{
  "sms": {
    "resp": 0,
    "smsSendSucc": 1,
    "smsSendFail": 0
  }
}
```

An optional modem `smsRef` may also be present.

### Notes

- Normal SMS was end-to-end live verified: `resp=0`, `smsSendSucc=1`, `smsSendFail=0`, matching Outbox entry `status=0`, and physical receipt confirmed.
- Recipient and message content were deliberately not retained in canonical/public evidence.
- Clients should inspect the SMS-specific success/failure fields; HTTP 200 alone is not sufficient.
