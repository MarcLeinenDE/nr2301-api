# `aoc` namespace

**3 methods** in the current public catalog.

Verification/auth/safety terminology: see [`../docs/method-status.md`](../docs/method-status.md).

| Method | Verification | Auth evidence | Safety |
|---|---|---|---|
| [`get_bat_info`](#get-bat-info) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`set_sleep_wait_time`](#set-sleep-wait-time) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`sleep_wait_time`](#sleep-wait-time) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |

<a id="get-bat-info"></a>

## `get_bat_info`

**Method ID:** `aoc/get_bat_info`  
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
  "capacity": "integer",
  "ind": "integer",
  "status": "integer",
  "temperature": "integer"
}
```

### Semantics

- **`battery.backend.v1`**
  - `evidence`: FIRMWARE_BACKEND_VERIFIED

### Notes

- The returned temperature field is interpreted by the stock frontend as battery temperature in °C.

<a id="set-sleep-wait-time"></a>

## `set_sleep_wait_time`

**Method ID:** `aoc/set_sleep_wait_time`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `time`.

### Response

Known/observed response fields: `result`.

<a id="sleep-wait-time"></a>

## `sleep_wait_time`

**Method ID:** `aoc/sleep_wait_time`  
**Endpoint:** `/api.cgi`  
**Operation type:** `READ`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `GET`

```json
{}
```

### Response

```json
{
  "result": "integer"
}
```

### Notes

- Live authenticated result=30. Frontend select values prove unit/enum: 0(off),10,20,30,40,60 minutes. Anonymous live response: HTTP 200 {'system_err':'session no exist'}.

