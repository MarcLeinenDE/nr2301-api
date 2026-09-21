# `firewall` namespace

**26 methods** in the current public catalog.

Verification/auth/safety terminology: see [`../docs/method-status.md`](../docs/method-status.md).

| Method | Verification | Auth evidence | Safety |
|---|---|---|---|
| [`fw_edit_dmz_entry`](#fw-edit-dmz-entry) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
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
| [`ww_edit_ip_filter`](#ww-edit-ip-filter) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`ww_edit_port_filter`](#ww-edit-port-filter) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
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
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "dmz_dest_ip": "<non-empty IPv4 string>"
}
```

Basis: shipped NR2301 WebUI source plus physical write/read-back evidence.

### Response

No stable response schema is currently documented.

### Notes

- Non-empty destination writes are live verified.
- The stock NR2301 WebUI exposes no destination clear/delete operation; do not infer an empty-string clear contract.

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

```json
{
  "dmz_disable": "0"
}
```

`"0"` = enabled, `"1"` = disabled.

### Response

Known/observed response fields: `firewall`.

### Notes

- DMZ enable/disable was physically written, read back and restored.
- Changing the enable state does not clear the stored destination.

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

```json
{
  "pptp": 1,
  "l2tp": 1,
  "ipsec": 1
}
```

The stock page uses `toStringData:false`; all three flags are native JSON integers.

### Response

Known/observed response fields: `result`.

### Notes

- Native-integer same-state, mutation, read-back and restore were physically verified.

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

```json
{
  "admin_from_wan": {
    "admin_from_wan_enable": "1"
  }
}
```

Use string `"0"` or `"1"`.

### Response

Known/observed response fields: `firewall`.

### Notes

- The nested WebUI body was physically verified with same-state, mutation, read-back and restore.
- The stock WebUI separately schedules `router/restart_web_server` after a changed value; that disruptive follow-up is not part of this setter body.

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

```json
{
  "ping_from_wan": {
    "ping_from_wan_enable": "1"
  }
}
```

Use string `"0"` or `"1"`.

### Response

Known/observed response fields: `firewall`.

### Notes

- The nested WebUI body was physically verified with same-state, mutation, read-back and restore.

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

Disabled:

```json
{"enable":0}
```

Enabled uses exactly five indexed slots (0..4):

```json
{
  "enable": 1,
  "items": [
    {
      "index": 0,
      "name": "example",
      "mac": "02:00:00:00:00:01",
      "local_port": "65500",
      "wan_port": "65500"
    }
  ]
}
```

The stock page uses `toStringData:false`, so `enable` and `index` are native JSON integers.

### Response

Known/observed response fields: `resJson`.

### Notes

- The NR2301 WebUI exposes five Port Forward slots, not ten.
- A 2026-09-18 production-helper smoke physically reconfirmed create/read-back/list restore/disable restore with no synthetic residue.
- Observed `result=0` for the enabled write and `result=1` for the disabled restore; treat `result` as endpoint-state-dependent and verify with `get_port_forward`.
- 2026-09-21 physical SDK lifecycle: an uppercase synthetic MAC written through `set_port_forward` was returned by `get_port_forward` with lowercase hexadecimal letters. Compare MAC addresses semantically/case-insensitively for write verification; raw getter values remain raw.

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

Disabled:

```json
{"enable":0}
```

Enabled uses a complete ten-slot list:

```json
{
  "enable": 1,
  "items": [
    {
      "index": 0,
      "name": "example",
      "trigger_port": "65500",
      "start_port": "65501",
      "end_port": "65501"
    }
  ]
}
```

The stock page uses `toStringData:false`, so `enable` and `index` are native JSON integers.

### Response

Known/observed response fields: `result`.

### Notes

- `{"enable":0}` disables triggering but does not delete stored rules.
- Deletion was physically verified by sending `enable=1` with the complete ten-slot list and the target slot emptied, verifying removal, then restoring the original enable state.

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

Blacklist example:

```json
{
  "mode": "blacklist",
  "black_items": [
    {"value":"example.invalid","index":0}
  ]
}
```

Whitelist uses `white_items`; disabled mode is `{"mode":"disable"}`. The stock page uses `toStringData:false`, so item indices are native integers.

### Response

Known/observed response fields: `resJson`.

### Notes

- A synthetic blacklist lifecycle and semantic restore were physically verified.
- Disabling the filter does not by itself establish deletion of stored blacklist/whitelist entries.

<a id="ww-edit-ip-filter"></a>

## `ww_edit_ip_filter`

**Method ID:** `firewall/ww_edit_ip_filter`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "ww_ip_filter": {
    "list": [
      {"ip":"203.0.113.77","index":"0"},
      {"ip":"0","index":"1"}
    ]
  }
}
```

The complete request contains exactly ten entries. Indices are strings and empty slots use string `"0"`.

### Response

Known/observed response fields: `firewall`.

### Notes

- The exact ten-slot non-empty write/full-list read-back/list restore/switch restore lifecycle was physically verified.
- Full-list read uses `ww_read_ip_filter` with `{ww_ip_filter:{list:["all"]}}`.

<a id="ww-edit-port-filter"></a>

## `ww_edit_port_filter`

**Method ID:** `firewall/ww_edit_port_filter`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "ww_port_filter": {
    "list": [
      {"port":"65500:65500","index":"0"},
      {"port":"0","index":"1"}
    ]
  }
}
```

The complete request contains exactly ten entries. Indices are strings; populated entries use `"start:end"` and empty slots use string `"0"`.

### Response

Known/observed response fields: `firewall`.

### Notes

- The exact ten-slot non-empty write/full-list read-back/list restore/switch restore lifecycle was physically verified.
- Full-list read uses `ww_read_port_filter` with `{ww_port_filter:{list:["all"]}}`.

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

```json
{
  "ww_ip_filter": {
    "ip_filter_disable": "0"
  }
}
```

`"0"` = enabled, `"1"` = disabled.

### Response

Known/observed response fields: `firewall`.

### Notes

- Enable/disable plus restore was physically verified.

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

```json
{
  "ww_port_filter": {
    "port_filter_disable": "0"
  }
}
```

`"0"` = enabled, `"1"` = disabled. Although the page source uses numeric literals, the default WebUI serializer stringifies them on the wire.

### Response

Known/observed response fields: `firewall`.

### Notes

- Enable/disable plus restore was physically verified.

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

```json
{
  "ww_upnp": {
    "upnp_enable": "1"
  }
}
```

Use string `"0"` or `"1"`.

### Response

Known/observed response fields: `firewall`.

### Notes

- UPnP same-state/mutation/read-back/restore was physically verified.
- WPS and UPnP are independent controls on ACIY.3.

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

