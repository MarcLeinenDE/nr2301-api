# `account` namespace

**6 methods** in the current public catalog.

Verification/auth/safety terminology: see [`../docs/method-status.md`](../docs/method-status.md).

> [!IMPORTANT]
> On tested firmware `V1.00(ACIY.3)C0`, administrator pre-auth is host/authority sensitive. `zyxel.home` and `192.168.1.1` resolve to the same router address, but the direct-IP path returned `result=4` for both pre-auth methods while `http://zyxel.home` returned normal `result=0` responses. Use `http://zyxel.home` for the administrator challenge/login flow on this firmware. See [`../docs/authentication.md`](../docs/authentication.md).

| Method | Verification | Auth evidence | Safety |
|---|---|---|---|
| [`get_info`](#get-info) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_rand`](#get-rand) | `LIVE_VERIFIED` | `PREAUTH_ALLOWED` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_retrytimes_and_time`](#get-retrytimes-and-time) | `LIVE_VERIFIED` | `PREAUTH_ALLOWED` | `READ_OR_LOW_SIDE_EFFECT` |
| [`login`](#login) | `LIVE_VERIFIED` | `PREAUTH_AUTHENTICATOR` | `READ_OR_LOW_SIDE_EFFECT` |
| [`logout`](#logout) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`set_info`](#set-info) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |

<a id="get-info"></a>

## `get_info`

**Method ID:** `account/get_info`  
**Endpoint:** `/api.cgi`  
**Operation type:** `READ`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "type": "string",
  "session_id": "string"
}
```

### Response

```json
{
  "modified": "integer",
  "password": "string",
  "remaining_time": "string",
  "result": "integer",
  "status": "string",
  "total_time": "integer",
  "username": "string"
}
```

<a id="get-rand"></a>

## `get_rand`

**Method ID:** `account/get_rand`  
**Endpoint:** `/api.cgi`  
**Operation type:** `READ`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `PREAUTH_ALLOWED`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "type": "admin",
  "user_id": "<random>"
}
```

### Response

```json
{
  "rand": "string",
  "result": "integer"
}
```

### Semantics

- **`account.preauth_host_authority.v1`**
  - `evidence`: LIVE_AB_VERIFIED_2026_08_31
  - tested firmware: `V1.00(ACIY.3)C0`
  - canonical management URL: `http://zyxel.home`
  - direct-IP observation: `http://192.168.1.1` → `result=4`
  - canonical-host observation: `http://zyxel.home` → `result=0`
  - scope: host/authority-dependent behavior; this does **not** define `4` as a universal `get_rand` error enum

### Notes

- Live pre-auth helper used successfully by normal admin login.
- Historical live-working clients used an eight-character lowercase-alphanumeric `user_id` and reused it for `account/login`.
- During the physical USB A/B test, user-id length, requests-vs-urllib transport, compact JSON/header reproduction, WebUI bootstrap and prior explicit WebUI logout did not explain the direct-IP failure; switching only to the canonical host made pre-auth succeed.

<a id="get-retrytimes-and-time"></a>

## `get_retrytimes_and_time`

**Method ID:** `account/get_retrytimes_and_time`  
**Endpoint:** `/api.cgi`  
**Operation type:** `READ`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `PREAUTH_ALLOWED`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "type": "admin"
}
```

### Response

```json
{
  "remain_time": "integer",
  "result": "integer",
  "retry_times": "integer"
}
```

### Semantics

- **`account.preauth_host_authority.v1`**
  - `evidence`: LIVE_AB_VERIFIED_2026_08_31
  - tested firmware: `V1.00(ACIY.3)C0`
  - canonical management URL: `http://zyxel.home`
  - direct-IP observation: `http://192.168.1.1` → `result=4`
  - canonical-host observation: `http://zyxel.home` → `result=0`, `retry_times=5`, `remain_time=0`

### Notes

- Live pre-auth helper; normal admin `retry_times` remained 5 before/after login in earlier research.
- Use this method as a lockout guard before requesting the challenge.

<a id="login"></a>

## `login`

**Method ID:** `account/login`  
**Endpoint:** `/api.cgi`  
**Operation type:** `AUTH_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `PREAUTH_AUTHENTICATOR`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "type": "admin",
  "username": "<admin>",
  "password": "<md5 challenge response>",
  "user_id": "<random>"
}
```

### Response

```json
{
  "result": "integer"
}
```

### Semantics

- **`account.login_result.v1`**
  - `evidence`: FRONTEND_SOURCE_VERIFIED_WITH_LIVE_SUBSET
  - `field`: result
  - `values`: 0..6; live subset 1/2/3

### Notes

- Normal admin login returned result=3 and established CGISID.
- On tested firmware, perform the challenge/login flow through `http://zyxel.home`; direct-IP pre-auth can fail before the password is submitted.

<a id="logout"></a>

## `logout`

**Method ID:** `account/logout`  
**Endpoint:** `/api.cgi`  
**Operation type:** `AUTH_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `GET`

No request body has been reconstructed as necessary for this method.

### Response

Known/observed response fields: `result`.

<a id="set-info"></a>

## `set_info`

**Method ID:** `account/set_info`  
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

- Platform WW_OPERATOR_ZYXEL. Same-state total_time=900 with current session_id returned result=0; numeric total_time was stringified on wire.
