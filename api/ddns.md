# `ddns` namespace

**2 methods** in the current public catalog.

Verification/auth/safety terminology: see [`../docs/method-status.md`](../docs/method-status.md).

| Method | Verification | Auth evidence | Safety |
|---|---|---|---|
| [`get_ddns`](#get-ddns) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`set_ddns`](#set-ddns) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |

<a id="get-ddns"></a>

## `get_ddns`

**Method ID:** `ddns/get_ddns`  
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
  "ddns_ipaddr": "string",
  "ddns_state": "string",
  "domain": "string",
  "enabled": "string",
  "password": "string",
  "result": "integer",
  "service_name": "string",
  "username": "string"
}
```

### Semantics

- **`ddns.state.v1`**
  - `evidence`: STATIC_FRONTEND_VERIFIED
  - `field`: ddns_state
  - `values`: `{"0": "idle", "1": "updating", "2": "updating", "3": "OK", "4": "blocked"}`

### Notes

- Runtime getter does not return token. Custom-provider setter testing was skipped because exact credential restore cannot be guaranteed.

<a id="set-ddns"></a>

## `set_ddns`

**Method ID:** `ddns/set_ddns`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `enabled`, `service_name`, `domain`, `username`, `password`, `token`.

### Response

Known/observed response fields: `result`.

### Notes

- Safety: do not blindly rewrite an existing token-based profile because the token is not known to be round-trippable. Custom-provider writes remain unverified.

