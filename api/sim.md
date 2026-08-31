# `sim` namespace

**7 methods** in the current public catalog.

Verification/auth/safety terminology: see [`../docs/method-status.md`](../docs/method-status.md).

| Method | Verification | Auth evidence | Safety |
|---|---|---|---|
| [`change_pin`](#change-pin) | `STATIC_CONFIRMED` | `UNTESTED` | `DO_NOT_TEST_FOR_COVERAGE` |
| [`disable_pin`](#disable-pin) | `STATIC_CONFIRMED` | `UNTESTED` | `DO_NOT_TEST_FOR_COVERAGE` |
| [`enable_pin`](#enable-pin) | `STATIC_CONFIRMED` | `UNTESTED` | `DO_NOT_TEST_FOR_COVERAGE` |
| [`get_lock_info`](#get-lock-info) | `LIVE_VERIFIED_LIMITED` | `ADMIN_OK_EMPTY_RESPONSE` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_sim_status`](#get-sim-status) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`provide_pin`](#provide-pin) | `STATIC_CONFIRMED` | `UNTESTED` | `DO_NOT_TEST_FOR_COVERAGE` |
| [`reset_pin_using_puk`](#reset-pin-using-puk) | `STATIC_CONFIRMED` | `UNTESTED` | `DO_NOT_TEST_FOR_COVERAGE` |

<a id="change-pin"></a>

## `change_pin`

**Method ID:** `sim/change_pin`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `STATIC_CONFIRMED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `DO_NOT_TEST_FOR_COVERAGE`

> [!CAUTION]
> This method was deliberately not exercised merely to improve coverage because its potential impact outweighed the documentation value. Treat the contract as static evidence only.

### Request

HTTP method: `POST`

Exact shipped-frontend payload:

```json
{
  "pin_puk": {
    "pin": "<secret>",
    "new_pin": "<secret>"
  }
}
```

Static source: `/html/set_pin.html line 281`; frontend expression `{pin_puk:{pin:pin,new_pin:new_pin}}`.

The PIN/PUK/new-PIN values are secrets and must be redacted. The corresponding WebUI password inputs are source-verified with `maxlength=8`; no stricter minimum length or character-set rule is asserted here.

### Response

Known/observed response fields: `pin_puk`, `response`.

<a id="disable-pin"></a>

## `disable_pin`

**Method ID:** `sim/disable_pin`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `STATIC_CONFIRMED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `DO_NOT_TEST_FOR_COVERAGE`

> [!CAUTION]
> This method was deliberately not exercised merely to improve coverage because its potential impact outweighed the documentation value. Treat the contract as static evidence only.

### Request

HTTP method: `POST`

Exact shipped-frontend payload:

```json
{
  "pin_puk": {
    "pin": "<secret>"
  }
}
```

Static source: `/html/set_pin.html line 277`; frontend expression `{pin_puk:{pin:pin}}`.

The PIN/PUK/new-PIN values are secrets and must be redacted. The corresponding WebUI password inputs are source-verified with `maxlength=8`; no stricter minimum length or character-set rule is asserted here.

### Response

Known/observed response fields: `pin_puk`, `response`.

<a id="enable-pin"></a>

## `enable_pin`

**Method ID:** `sim/enable_pin`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `STATIC_CONFIRMED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `DO_NOT_TEST_FOR_COVERAGE`

> [!CAUTION]
> This method was deliberately not exercised merely to improve coverage because its potential impact outweighed the documentation value. Treat the contract as static evidence only.

### Request

HTTP method: `POST`

Exact shipped-frontend payload:

```json
{
  "pin_puk": {
    "pin": "<secret>"
  }
}
```

Static source: `/html/set_pin.html line 273`; frontend expression `{pin_puk:{pin:pin}}`.

The PIN/PUK/new-PIN values are secrets and must be redacted. The corresponding WebUI password inputs are source-verified with `maxlength=8`; no stricter minimum length or character-set rule is asserted here.

### Response

Known/observed response fields: `pin_puk`, `response`.

<a id="get-lock-info"></a>

## `get_lock_info`

**Method ID:** `sim/get_lock_info`  
**Endpoint:** `/api.cgi`  
**Operation type:** `READ`  
**Verification:** `LIVE_VERIFIED_LIMITED`  
**Auth evidence:** `ADMIN_OK_EMPTY_RESPONSE`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `GET`

No request body has been reconstructed as necessary for this method.

### Response

Known/observed response fields: `cell_info`, `lock_status`, `result`, `sim_info`.

### Notes

- Normal admin session: HTTP 200, Content-Type application/json, zero-length body.

<a id="get-sim-status"></a>

## `get_sim_status`

**Method ID:** `sim/get_sim_status`  
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
  "pin_puk": {
    "pin_attempts": "integer",
    "pin_enabled": "integer",
    "pin_status": "integer",
    "puk_attempts": "integer",
    "sim_status": "integer"
  },
  "response": {
    "setting_response": "string"
  }
}
```

### Semantics

- **`sim.status_enum.v1`**
  - `evidence`: STATIC_FRONTEND_COMMENT_AND_BRANCH_VERIFIED

<a id="provide-pin"></a>

## `provide_pin`

**Method ID:** `sim/provide_pin`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `STATIC_CONFIRMED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `DO_NOT_TEST_FOR_COVERAGE`

> [!CAUTION]
> This method was deliberately not exercised merely to improve coverage because its potential impact outweighed the documentation value. Treat the contract as static evidence only.

### Request

HTTP method: `POST`

Exact shipped-frontend payload:

```json
{
  "pin_puk": {
    "pin": "<secret>"
  }
}
```

Static source: `/html/set_pin.html line 269`; frontend expression `{pin_puk:{pin:pin}}`.

The PIN/PUK/new-PIN values are secrets and must be redacted. The corresponding WebUI password inputs are source-verified with `maxlength=8`; no stricter minimum length or character-set rule is asserted here.

### Response

Known/observed response fields: `pin_puk`, `response`.

<a id="reset-pin-using-puk"></a>

## `reset_pin_using_puk`

**Method ID:** `sim/reset_pin_using_puk`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `STATIC_CONFIRMED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `DO_NOT_TEST_FOR_COVERAGE`

> [!CAUTION]
> This method was deliberately not exercised merely to improve coverage because its potential impact outweighed the documentation value. Treat the contract as static evidence only.

### Request

HTTP method: `POST`

Exact shipped-frontend payload:

```json
{
  "pin_puk": {
    "puk": "<secret>",
    "new_pin": "<secret>"
  }
}
```

Static source: `/html/set_pin.html line 328`; frontend expression `{pin_puk:{puk:puk,new_pin:pin}}`.

The PIN/PUK/new-PIN values are secrets and must be redacted. The corresponding WebUI password inputs are source-verified with `maxlength=8`; no stricter minimum length or character-set rule is asserted here.

### Response

Known/observed response fields: `pin_puk`, `response`.

## PIN/PUK physical-testing policy — 2026-08-31

The public contract now contains the exact shipped-frontend request shapes for all five PIN/PUK mutation methods. This does **not** promote their physical verification status. Physical testing must be deliberate rather than coverage-driven:

- obtain PIN/PUK only from local secret storage/environment; never publish them;
- read `get_sim_status` before every mutation and refuse exploratory writes when retry counts are low or unavailable;
- never send a deliberately incorrect PIN/PUK merely to discover error behavior;
- prefer reversible enable/disable/change-PIN sequences with read-back and restoration;
- `reset_pin_using_puk` remains a separate recovery-path capability and should not be exercised by intentionally exhausting PIN retries solely for coverage.
