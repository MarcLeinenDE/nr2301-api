# `statistics` namespace

**11 methods** in the current public catalog.

Verification/auth/safety terminology: see [`../docs/method-status.md`](../docs/method-status.md).

| Method | Verification | Auth evidence | Safety |
|---|---|---|---|
| [`clear_offline_user`](#clear-offline-user) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`get_black_white_mode`](#get-black-white-mode) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_conn_clients_info`](#get-conn-clients-info) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_login_client_mac`](#get-login-client-mac) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`set_alias`](#set-alias) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`set_allow`](#set-allow) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`set_black_white_mode`](#set-black-white-mode) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`set_forbidden`](#set-forbidden) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`stat_clear_common_data`](#stat-clear-common-data) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`stat_get_common_data`](#stat-get-common-data) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`stat_get_traffic_transport_status`](#stat-get-traffic-transport-status) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |

<a id="clear-offline-user"></a>

## `clear_offline_user`

**Method ID:** `statistics/clear_offline_user`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `mac`.

### Response

Known/observed response fields: `clients_info`, `mode`.

### Notes

- Live verification used source-correct get_inactive_users. 3 inactive records before; clear_offline_user returned result=0; selected record disappeared and 2 remained.

<a id="get-black-white-mode"></a>

## `get_black_white_mode`

**Method ID:** `statistics/get_black_white_mode`  
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
  "mode": "string",
  "result": "integer"
}
```

### Notes

- Live client-list semantics depend on mode. Current test capture returned mode='black'. Read this before presenting allow/block controls.
- Real transition read-back verified: black -> white -> black, HTTP200/result0 writes and immediate mode read-back.
- 2026-08-31 sanitized read returned `mode='black'` with `result=1`; do not treat `result=0` as a universal success requirement for Statistics read endpoints.

<a id="get-conn-clients-info"></a>

## `get_conn_clients_info`

**Method ID:** `statistics/get_conn_clients_info`  
**Endpoint:** `/api.cgi`  
**Operation type:** `READ`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `GET`

Known top-level request keys from the shipped frontend: `request_type`.

Observed frontend transport variants:

- `direct_ajaxHandler` via `GET`; body present: `False`
- `direct_ajaxHandler` via `POST`; body present: `True`; keys: request_type

### Response

```json
{
  "clients_info": [
    {
      "alias": "string",
      "client_type": "integer",
      "cur_conn_time": "string",
      "forbidden": "integer",
      "ip": "string",
      "mac": "string",
      "name": "string",
      "type": "string"
    }
  ]
}
```

### Exact `request_type` tokens

The shipped frontend uses these four raw values when requesting explicit client views:

| Raw token | View |
|---|---|
| `get_active_users` | active clients |
| `get_inactive_users` | inactive/offline clients |
| `get_allow_users` | allow-list view |
| `get_forbidden_users` | forbidden/block-list view |

`get_inactive_users` is the exact source-backed token. Do **not** replace it with the previously guessed `get_offline_users`. Explicit views are sent as a top-level POST field, for example `{"request_type":"get_inactive_users"}`. The separately observed body-less GET variant remains valid and is not redefined here as one of these four explicit tokens.

Allow/forbidden semantics depend on the current Black/White MAC-filter mode; read `get_black_white_mode` before presenting them as policy state.

### Semantics

- **`clients.active`**
  - `evidence`: frontend exact + live client response schema
- **`clients.inactive`**
  - `evidence`: frontend exact + live read + clear_offline read-back
- **`clients.allow_list`**
  - `evidence`: frontend exact + live read
- **`clients.forbidden_list`**
  - `evidence`: frontend exact + live add/read/remove verification

### Notes

- get_allow_users/get_forbidden_users are mode-oriented views. In live black mode, an unknown MAC allowed via set_allow did not appear in get_allow_users; the same record was visible in inactive state.
- 2026-08-25 USB path test: with laptop Wi-Fi manually disabled, a fresh Admin session and normal reads remained available over USB; active inventory contained a USB client.
- During White, existing shared client rows switched from forbidden-field view to allow-field view with allow=0; get_allow_users remained empty.
- White-mode get_allow_users now live verified with a real Wi-Fi client: absent/allow=0 before set_allow, present/allow=1 after set_allow, active/allow=1 after actual WLAN reconnect, absent again after cleanup.
- 2026-08-31 sanitized SDK explicit-view sweep confirmed all four exact POST tokens in one Black-mode admin session: active=2, inactive=1, allow=0, forbidden=0. Active/inactive rows exposed `alias`, `client_type`, `cur_conn_time`, `forbidden`, `ip`, `mac`, `name`, `type`; only counts/schema keys were logged.

<a id="get-login-client-mac"></a>

## `get_login_client_mac`

**Method ID:** `statistics/get_login_client_mac`  
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
  "mac": "string",
  "result": "integer"
}
```

### Notes

- Do not require this method as the sole proof of USB management identity. One USB-only preflight returned no MAC, while a repeated run did return one. Treat it as optional diagnostic metadata.

<a id="set-alias"></a>

## `set_alias`

**Method ID:** `statistics/set_alias`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `mac`, `alias`.

### Response

Known/observed response fields: `clients_info`.

<a id="set-allow"></a>

## `set_allow`

**Method ID:** `statistics/set_allow`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `mac`, `alias`, `enable`.

Observed frontend transport variants:

- `direct_ajaxHandler` via `POST`; body present: `True`; keys: mac, alias, enable
- `direct_ajaxHandler` via `POST`; body present: `True`; keys: mac, enable

### Response

Known/observed response fields: `result`.

### Notes

- Distinct locally-administered fake MAC add returned result=0 and disable/remove call returned result=0.
- Do not model as independent Allow-list CRUD. Live black-mode test: enable=1 created an inactive client with forbidden=0 but did not appear in get_allow_users; enable=0 changed it to forbidden=1 and it appeared in get_forbidden_users.
- Original user.html invokes set_allow only when MAC filter mode is WHITE. White-mode live transition/read-back remains intentionally untested due management-lockout risk.
- 2026-08-25 White-mode real Wi-Fi test: set_allow(enable=1) returned result0, client appeared in get_allow_users with allow=1, and the same Wi-Fi client successfully reconnected and became active. enable=0 removed it from Allow and restored allow=0.
- During safe Black->White provisioning, success is not complete until intended MAC(s) are present in get_allow_users with allow=1. Failure triggers mandatory Black restore over verified recovery path.

<a id="set-black-white-mode"></a>

## `set_black_white_mode`

**Method ID:** `statistics/set_black_white_mode`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `mode`.

### Response

Known/observed response fields: `result`.

### Semantics

- **`clients.mac_filter_mode`**
  - `evidence`: frontend + live setter

### Notes

- 2026-08-25: live black->white->black transition succeeded over verified USB management path. White did not auto-populate get_allow_users; known USB/WIFI rows showed allow=0.
- Complete safe workflow now live verified: Black -> White over USB, explicit set_allow for real Wi-Fi MAC, actual WLAN reconnect, allow cleanup, restore Black.
- Safety: switching Black->White filtering can lock out Wi-Fi management. Use a separately verified recovery path before attempting this transition.
- After enabling White mode, explicitly allow the intended management client(s), verify allow=1 by read-back, and restore the previous mode if provisioning fails.

<a id="set-forbidden"></a>

## `set_forbidden`

**Method ID:** `statistics/set_forbidden`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `mac`, `alias`, `enable`.

Observed frontend transport variants:

- `direct_ajaxHandler` via `POST`; body present: `True`; keys: mac, alias, enable
- `direct_ajaxHandler` via `POST`; body present: `True`; keys: mac, enable

### Response

Known/observed response fields: `result`.

### Notes

- Live verification used a distinct locally-administered fake MAC. Add returned result=0, read-back in get_forbidden_users confirmed presence; remove returned result=0 and read-back confirmed absence.
- In black-list mode, an arbitrary previously unknown locally-administered unicast MAC can be added with enable=1, appears in get_forbidden_users with forbidden=1, and is removed from that list with enable=0.

<a id="stat-clear-common-data"></a>

## `stat_clear_common_data`

**Method ID:** `statistics/stat_clear_common_data`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `GET`

No request body has been reconstructed as necessary for this method.

### Response

Known/observed response fields: `statistics`.

### Notes

- GET returned statistics.setting_response='OK'. This intentionally clears traffic/history counters.

<a id="stat-get-common-data"></a>

## `stat_get_common_data`

**Method ID:** `statistics/stat_get_common_data`  
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
  "statistics": {
    "duration": "integer",
    "error_bytes": "integer",
    "rx_bytes": "integer",
    "rx_tx_bytes": "integer",
    "total_duration": "integer",
    "total_error_bytes": "integer",
    "total_rx_bytes": "integer",
    "total_rx_tx_bytes": "integer",
    "total_tx_bytes": "integer",
    "tx_bytes": "integer"
  }
}
```

<a id="stat-get-traffic-transport-status"></a>

## `stat_get_traffic_transport_status`

**Method ID:** `statistics/stat_get_traffic_transport_status`  
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
  "traffic_transport_status": {
    "rx_status": "integer",
    "tx_status": "integer"
  }
}
```

