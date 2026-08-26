# `util_wan` namespace

**3 methods** in the current public catalog.

Verification/auth/safety terminology: see [`../docs/method-status.md`](../docs/method-status.md).

| Method | Verification | Auth evidence | Safety |
|---|---|---|---|
| [`get_network_select_mode`](#get-network-select-mode) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`search_network`](#search-network) | `LIVE_VERIFIED` | `UNTESTED` | `READ_OR_LOW_SIDE_EFFECT` |
| [`select_network`](#select-network) | `LIVE_VERIFIED` | `ADMIN_OK` | `DISRUPTIVE_RECOVERY_REQUIRED` |

<a id="get-network-select-mode"></a>

## `get_network_select_mode`

**Method ID:** `util_wan/get_network_select_mode`  
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
  "nw_sel_mode": "string",
  "result": "integer"
}
```

<a id="search-network"></a>

## `search_network`

**Method ID:** `util_wan/search_network`  
**Endpoint:** `/api.cgi`  
**Operation type:** `SCAN_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `GET`

No request body has been reconstructed as necessary for this method.

### Response

No stable response schema is currently documented.

### Notes

- Operator scan returned live network_list.

<a id="select-network"></a>

## `select_network`

**Method ID:** `util_wan/select_network`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `DISRUPTIVE_RECOVERY_REQUIRED`

> [!WARNING]
> This method may interrupt management connectivity or require recovery/read-back. Treat a lost HTTP response as inconclusive until the resulting state has been verified.

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `network_param`.

### Response

Known/observed response fields: `response`.

### Notes

- Current selection mode was auto; POST network_param='auto' returned response.setting_response='OK' and management recovery succeeded on first attempt.

