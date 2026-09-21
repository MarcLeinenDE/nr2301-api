# `account` namespace

**6 methods** in the current public catalog.

Verification/auth/safety terminology: see [`../docs/method-status.md`](../docs/method-status.md).

> [!IMPORTANT]
> Administrator pre-auth showed authority-dependent behavior in one 2026-08-31 A/B test, but a 2026-09-21 recheck successfully completed the full SDK challenge/login flow through `http://192.168.1.1` after `zyxel.home` failed to resolve locally. Treat authority behavior as runtime/environment/state dependent; do not reject direct-IP login pre-emptively. See [`../docs/authentication.md`](../docs/authentication.md).

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
  - `evidence`: LIVE_STATE_DEPENDENT_2026_08_31_AND_2026_09_21
  - tested firmware: `V1.00(ACIY.3)C0`
  - 2026-08-31: direct IP returned `result=4`; `zyxel.home` returned `result=0`
  - 2026-09-21: direct IP successfully completed the same SDK pre-auth/login flow
  - conclusion: do not encode either authority as universally required

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
- `http://zyxel.home` remains the SDK default, but direct-IP login is also physically proven to work in a later ACIY.3 runtime state. If one authority fails pre-auth, the alternative known authority is a recovery option.

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

The stock frontend uses the same setter for two admin-setting variants.

Password change:

```json
{
  "type": "admin",
  "session_id": "<current CGISID>",
  "password": "<new password>"
}
```

Session timeout change:

```json
{
  "type": "admin",
  "session_id": "<current CGISID>",
  "total_time": "<seconds as string>"
}
```

The password form's `password_confirm` field is frontend-only validation and is
not transmitted. The old password is also not sent in the setter body.

### Response

```json
{
  "result": "integer"
}
```

### Notes

- Platform WW_OPERATOR_ZYXEL. Same-state `total_time=900` with current `session_id` returned `result=0`; numeric `total_time` was stringified on wire.
- Read-only source capture on 2026-09-21 reconstructed the password setter exactly as `type=admin`, current `CGISID`, and the new `password`.
- General frontend password validation on this build requires length 5..32, characters accepted by `checkLoginPassword()`, and rejects an all-space value. Operator-specific variants can impose stronger rules.
- The frontend maps `result=-1001` to the message that the new password cannot be the same as the default password.
