# `firewall` namespace

**26 methods** in the current public catalog.

Verification/auth/safety terminology: see [`../docs/method-status.md`](../docs/method-status.md).

| Method | Verification | Auth evidence | Safety |
|---|---|---|---|
| [`fw_edit_dmz_entry`](#fw-edit-dmz-entry) | `STATIC_CONFIRMED` | `UNTESTED` | `DO_NOT_TEST_FOR_COVERAGE` |
| [`fw_get_disable_info`](#fw-get-disable-info) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`fw_get_dmz_info`](#fw-get-dmz-info) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`fw_get_vpn_passthrough`](#fw-get-vpn-passthrough) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`fw_set_disable_info`](#fw-set-disable-info) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`fw_set_vpn_passthrough`](#fw-set-vpn-passthrough) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`get_admin_from_wan`](#get-admin-from-wan) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_ping_from_wan`](#get-ping-from-wan) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_port_forward`](#get-port-forward) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_port_trigger`](#get-port-trigger) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_url_filter`](#get-url-filter) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`set_admin_from_wan`](#set-admin-from-wan) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`set_ping_from_wan`](#set-ping-from-wan) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`set_port_forward`](#set-port-forward) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`set_port_trigger`](#set-port-trigger) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`set_url_filter`](#set-url-filter) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`ww_edit_ip_filter`](#ww-edit-ip-filter) | `LIVE_VERIFIED` | `UNTESTED` | `WRITE_OR_SIDE_EFFECT` |
| [`ww_edit_port_filter`](#ww-edit-port-filter) | `LIVE_VERIFIED` | `UNTESTED` | `WRITE_OR_SIDE_EFFECT` |
| [`ww_fw_set_disable_info`](#ww-fw-set-disable-info) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`ww_fw_set_port_disable_info`](#ww-fw-set-port-disable-info) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`ww_read_ip_filter`](#ww-read-ip-filter) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`ww_read_port_filter`](#ww-read-port-filter) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`ww_read_switch_mode_state`](#ww-read-switch-mode-state) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`ww_read_switch_port_mode_state`](#ww-read-switch-port-mode-state) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`ww_upnp_open_close`](#ww-upnp-open-close) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`ww_upnp_open_close_state`](#ww-upnp-open-close-state) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |

<a id="fw-edit-dmz-entry"></a>

## `fw_edit_dmz_entry`

**Method ID:** `firewall/fw_edit_dmz_entry`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `STATIC_CONFIRMED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `DO_NOT_TEST_FOR_COVERAGE`

> [!CAUTION]
> This method was deliberately not exercised merely to improve coverage because its potential impact outweighed the documentation value. Treat the contract as static evidence only.

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `dmz_dest_ip`.

### Response

No stable response schema is currently documented.

<a id="fw-get-disable-info"></a>

## `fw_get_disable_info`

**Method ID:** `firewall/fw_get_disable_info`  
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
  "firewall": {
    "dmz_disable": "string"
  }
}
```

<a id="fw-get-dmz-info"></a>

## `fw_get_dmz_info`

**Method ID:** `firewall/fw_get_dmz_info`  
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
  "firewall": {
    "dmz_dest_ip": "string"
  }
}
```

<a id="fw-get-vpn-passthrough"></a>

## `fw_get_vpn_passthrough`

**Method ID:** `firewall/fw_get_vpn_passthrough`  
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
  "ipsec": "integer",
  "l2tp": "integer",
  "pptp": "integer",
  "result": "integer"
}
```

<a id="fw-set-disable-info"></a>

## `fw_set_disable_info`

**Method ID:** `firewall/fw_set_disable_info`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `dmz_disable`.

### Response

Known/observed response fields: `firewall`.

<a id="fw-set-vpn-passthrough"></a>

## `fw_set_vpn_passthrough`

**Method ID:** `firewall/fw_set_vpn_passthrough`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `pptp`, `l2tp`, `ipsec`.

### Response

Known/observed response fields: `result`.

<a id="get-admin-from-wan"></a>

## `get_admin_from_wan`

**Method ID:** `firewall/get_admin_from_wan`  
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
  "firewall": {
    "admin_from_wan_enable": "string",
    "setting_response": "string"
  }
}
```

<a id="get-ping-from-wan"></a>

## `get_ping_from_wan`

**Method ID:** `firewall/get_ping_from_wan`  
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
  "firewall": {
    "ping_from_wan_enable": "string",
    "setting_response": "string"
  }
}
```

<a id="get-port-forward"></a>

## `get_port_forward`

**Method ID:** `firewall/get_port_forward`  
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
  "result": "integer",
  "settings": {
    "enable": "integer",
    "items": [
      "<empty>"
    ]
  }
}
```

<a id="get-port-trigger"></a>

## `get_port_trigger`

**Method ID:** `firewall/get_port_trigger`  
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
  "result": "integer",
  "settings": {
    "enable": "integer",
    "items": [
      "<empty>"
    ]
  }
}
```

<a id="get-url-filter"></a>

## `get_url_filter`

**Method ID:** `firewall/get_url_filter`  
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
  "result": "integer",
  "settings": {
    "black_items": [
      "<empty>"
    ],
    "mode": "string",
    "white_items": [
      "<empty>"
    ]
  }
}
```

<a id="set-admin-from-wan"></a>

## `set_admin_from_wan`

**Method ID:** `firewall/set_admin_from_wan`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `admin_from_wan`.

### Response

Known/observed response fields: `firewall`.

<a id="set-ping-from-wan"></a>

## `set_ping_from_wan`

**Method ID:** `firewall/set_ping_from_wan`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `ping_from_wan`.

### Response

Known/observed response fields: `firewall`.

<a id="set-port-forward"></a>

## `set_port_forward`

**Method ID:** `firewall/set_port_forward`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

No request body has been reconstructed as necessary for this method.

### Response

Known/observed response fields: `resJson`.

### Notes

- Transactional add/read-back/clear/disable succeeded. Empirical result=0 when enabled, result=1 when disabled; result is not a generic failure code.

<a id="set-port-trigger"></a>

## `set_port_trigger`

**Method ID:** `firewall/set_port_trigger`  
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

<a id="set-url-filter"></a>

## `set_url_filter`

**Method ID:** `firewall/set_url_filter`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

No request body has been reconstructed as necessary for this method.

### Response

Known/observed response fields: `resJson`.

<a id="ww-edit-ip-filter"></a>

## `ww_edit_ip_filter`

**Method ID:** `firewall/ww_edit_ip_filter`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `ww_ip_filter`.

### Response

Known/observed response fields: `firewall`.

### Notes

- Temporary documentation-IP rule added, read back, then list restored empty.

<a id="ww-edit-port-filter"></a>

## `ww_edit_port_filter`

**Method ID:** `firewall/ww_edit_port_filter`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `ww_port_filter`.

### Response

Known/observed response fields: `firewall`.

### Notes

- Temporary port rule added, read back, then list restored empty.

<a id="ww-fw-set-disable-info"></a>

## `ww_fw_set_disable_info`

**Method ID:** `firewall/ww_fw_set_disable_info`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `ww_ip_filter`.

### Response

Known/observed response fields: `firewall`.

<a id="ww-fw-set-port-disable-info"></a>

## `ww_fw_set_port_disable_info`

**Method ID:** `firewall/ww_fw_set_port_disable_info`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `ww_port_filter`.

### Response

Known/observed response fields: `firewall`.

<a id="ww-read-ip-filter"></a>

## `ww_read_ip_filter`

**Method ID:** `firewall/ww_read_ip_filter`  
**Endpoint:** `/api.cgi`  
**Operation type:** `READ`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "ww_ip_filter": {
    "list": [
      "string"
    ]
  }
}
```

Observed frontend transport variants:

- `multicall_member` via `POST`; body present: `True`; keys: ww_ip_filter

### Response

```json
{
  "firewall": {
    "list": [
      "<empty>"
    ],
    "setting_response": "string"
  }
}
```

<a id="ww-read-port-filter"></a>

## `ww_read_port_filter`

**Method ID:** `firewall/ww_read_port_filter`  
**Endpoint:** `/api.cgi`  
**Operation type:** `READ`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "ww_port_filter": {
    "list": [
      "string"
    ]
  }
}
```

Observed frontend transport variants:

- `multicall_member` via `POST`; body present: `True`; keys: ww_port_filter

### Response

```json
{
  "firewall": {
    "list": [
      "<empty>"
    ],
    "setting_response": "string"
  }
}
```

<a id="ww-read-switch-mode-state"></a>

## `ww_read_switch_mode_state`

**Method ID:** `firewall/ww_read_switch_mode_state`  
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
  "firewall": {
    "default_policy": "string",
    "ip_filter_disable": "string",
    "setting_response": "string"
  }
}
```

<a id="ww-read-switch-port-mode-state"></a>

## `ww_read_switch_port_mode_state`

**Method ID:** `firewall/ww_read_switch_port_mode_state`  
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
  "firewall": {
    "default_policy": "string",
    "port_filter_disable": "string",
    "setting_response": "string"
  }
}
```

<a id="ww-upnp-open-close"></a>

## `ww_upnp_open_close`

**Method ID:** `firewall/ww_upnp_open_close`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `ww_upnp`.

### Response

Known/observed response fields: `firewall`.

### Notes

- WPS and UPnP should be modeled as independent controls on ACIY.3; WPS enable left UPnP=0 in live test.

<a id="ww-upnp-open-close-state"></a>

## `ww_upnp_open_close_state`

**Method ID:** `firewall/ww_upnp_open_close_state`  
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
  "firewall": {
    "setting_response": "string",
    "upnp_enable": "string"
  }
}
```

