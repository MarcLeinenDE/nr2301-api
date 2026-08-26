# `package` namespace

**4 methods** in the current public catalog.

Verification/auth/safety terminology: see [`../docs/method-status.md`](../docs/method-status.md).

| Method | Verification | Auth evidence | Safety |
|---|---|---|---|
| [`get_package_settings`](#get-package-settings) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_package_status`](#get-package-status) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`set_package_data_used`](#set-package-data-used) | `LIVE_VERIFIED` | `UNTESTED` | `WRITE_OR_SIDE_EFFECT` |
| [`set_package_settings`](#set-package-settings) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |

<a id="get-package-settings"></a>

## `get_package_settings`

**Method ID:** `package/get_package_settings`  
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
  "alarm_threshold": "integer",
  "data_used": "integer",
  "package_data_daily": {
    "package_data": "integer"
  },
  "package_data_half_year": {
    "package_data": "integer",
    "start_date": "string"
  },
  "package_data_monthly": {
    "bill_day": "integer",
    "package_data": "integer"
  },
  "package_data_one_year": {
    "package_data": "integer",
    "start_date": "string"
  },
  "package_data_three_months": {
    "package_data": "integer",
    "start_date": "string"
  },
  "package_data_unlimited": {
    "package_data": "integer"
  },
  "package_type": "string"
}
```

<a id="get-package-status"></a>

## `get_package_status`

**Method ID:** `package/get_package_status`  
**Endpoint:** `/api.cgi`  
**Operation type:** `READ`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `GET`

No request body has been reconstructed as necessary for this method.

Observed frontend transport variants:

- `multicall_member` via `POST`; body present: `False`

### Response

```json
{
  "status": "integer"
}
```

### Semantics

- **`package.status.v1`**
  - `evidence`: STATIC_FRONTEND_VERIFIED
  - `field`: status
  - `values`: `{"0": "normal/no alert", "1": "warning threshold", "2": "limit exceeded", "3": "expired"}`

<a id="set-package-data-used"></a>

## `set_package_data_used`

**Method ID:** `package/set_package_data_used`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `data_used`.

### Response

Known/observed response fields: `result`.

### Notes

- Same-state data_used returned result=0.

<a id="set-package-settings"></a>

## `set_package_settings`

**Method ID:** `package/set_package_settings`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

No request body has been reconstructed as necessary for this method.

### Response

Known/observed response fields: `result`.

### Notes

- package_type=unlimited live round-trips a numeric package_data_unlimited value and exposes no period/reset field. Do not label this as unlimited data volume; enforcement at limit remains untested.

