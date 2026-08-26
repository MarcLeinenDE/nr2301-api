# `wireless` namespace

**14 methods** in the current public catalog.

Verification/auth/safety terminology: see [`../docs/method-status.md`](../docs/method-status.md).

| Method | Verification | Auth evidence | Safety |
|---|---|---|---|
| [`get_diag_wifi_info`](#get-diag-wifi-info) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_extender_config`](#get-extender-config) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_extender_status`](#get-extender-status) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`wifi_call_wps_cancel`](#wifi-call-wps-cancel) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`wifi_call_wps_pbc`](#wifi-call-wps-pbc) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`wifi_call_wps_pin`](#wifi-call-wps-pin) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`wifi_get_ap_config`](#wifi-get-ap-config) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`wifi_get_basic_info`](#wifi-get-basic-info) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`wifi_get_timed_off_status`](#wifi-get-timed-off-status) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`wifi_get_wps_disable`](#wifi-get-wps-disable) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`wifi_scan`](#wifi-scan) | `LIVE_VERIFIED` | `UNTESTED` | `READ_OR_LOW_SIDE_EFFECT` |
| [`wifi_set_ap_config`](#wifi-set-ap-config) | `LIVE_VERIFIED` | `ADMIN_OK` | `DISRUPTIVE_RECOVERY_REQUIRED` |
| [`wifi_set_wps_disable`](#wifi-set-wps-disable) | `LIVE_VERIFIED` | `ADMIN_OK` | `DISRUPTIVE_RECOVERY_REQUIRED` |
| [`wps_status`](#wps-status) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |

<a id="get-diag-wifi-info"></a>

## `get_diag_wifi_info`

**Method ID:** `wireless/get_diag_wifi_info`  
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
  "wifi_5g_pwd_lv": "integer",
  "wifi_dual_pwd_lv": "integer",
  "wifi_power": "integer",
  "wifi_pwd_lv": "integer",
  "wifi_st": "integer"
}
```

### Semantics

- **`diag.wifi.v1`**
  - `evidence`: STATIC_FRONTEND_VERIFIED

<a id="get-extender-config"></a>

## `get_extender_config`

**Method ID:** `wireless/get_extender_config`  
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
  "enable": "integer",
  "key": "string",
  "ssid": "string"
}
```

<a id="get-extender-status"></a>

## `get_extender_status`

**Method ID:** `wireless/get_extender_status`  
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
  "status": "integer"
}
```

### Semantics

- **`wifi_extender.status.v1`**
  - `evidence`: FRONTEND_SOURCE_VERIFIED
  - `field`: status
  - `values`: 0..5 exact frontend mapping

### Notes

- Authenticated response observed; anonymous HTTP 200 body is {"system_err":"session no exist"}.

<a id="wifi-call-wps-cancel"></a>

## `wifi_call_wps_cancel`

**Method ID:** `wireless/wifi_call_wps_cancel`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `GET`

No request body has been reconstructed as necessary for this method.

### Response

Known/observed response fields: `wireless`.

### Notes

- GET returned wps_call_cancel_result='OK' after both PBC and PIN tests.

<a id="wifi-call-wps-pbc"></a>

## `wifi_call_wps_pbc`

**Method ID:** `wireless/wifi_call_wps_pbc`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `GET`

No request body has been reconstructed as necessary for this method.

### Response

Known/observed response fields: `wireless`.

### Notes

- GET returned wireless.wps_call_pbc_result='OK'; immediately cancelled in test.

<a id="wifi-call-wps-pin"></a>

## `wifi_call_wps_pin`

**Method ID:** `wireless/wifi_call_wps_pin`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `wps_enable`, `wps_pin`.

### Response

Known/observed response fields: `wireless`.

### Notes

- POST wps_enable='1', wps_pin='12345670' returned wireless.wps_call_pin_result='OK'; immediately cancelled.

<a id="wifi-get-ap-config"></a>

## `wifi_get_ap_config`

**Method ID:** `wireless/wifi_get_ap_config`  
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
  "config": {
    "maxassoc": "string",
    "mode": "string",
    "password_modified": "integer",
    "power_level": "string",
    "switch": "string",
    "wifi_if_24G": {
      "bandwidth": "string",
      "channel": "string",
      "cur_channel": "string",
      "encryption": "string",
      "first_channel": "string",
      "hidden": "string",
      "isolate": "string",
      "key": "string",
      "last_channel": "string",
      "net_mode": "string",
      "ssid": "string"
    },
    "wifi_if_5G": {
      "bandwidth": "string",
      "channel": "string",
      "channel_list": {
        "dfs": "string",
        "indoor": "string",
        "indoor_or_dfs": "string"
      },
      "cur_channel": "string",
      "encryption": "string",
      "hidden": "string",
      "isolate": "string",
      "key": "string",
      "net_mode": "string",
      "ssid": "string"
    },
    "wifi_if_DUAL": {
      "encryption": "string",
      "hidden": "string",
      "key": "string",
      "ssid": "string"
    },
    "wifi_if_GUEST": {
      "band_mode": "string",
      "encryption": "string",
      "hidden": "string",
      "key": "string",
      "maxassoc": "string",
      "ssid": "string"
    },
    "wifi_timed_off": {
      "enable": "integer",
      "end_hour": "integer",
      "end_minute": "integer",
      "start_hour": "integer",
      "start_minute": "integer"
    }
  },
  "result": "integer"
}
```

### Semantics

- **`wifi.presentation_tokens.v1`**
  - `evidence`: STATIC_FRONTEND_VERIFIED

<a id="wifi-get-basic-info"></a>

## `wifi_get_basic_info`

**Method ID:** `wireless/wifi_get_basic_info`  
**Endpoint:** `/api.cgi`  
**Operation type:** `READ`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "sw_only": "1"
}
```

### Response

```json
{
  "switch": "string"
}
```

### Notes

- Authenticated response observed; anonymous HTTP 200 body is {"system_err":"session no exist"}.

<a id="wifi-get-timed-off-status"></a>

## `wifi_get_timed_off_status`

**Method ID:** `wireless/wifi_get_timed_off_status`  
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
  "status": "string"
}
```

<a id="wifi-get-wps-disable"></a>

## `wifi_get_wps_disable`

**Method ID:** `wireless/wifi_get_wps_disable`  
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
  "wireless": {
    "wps_enable": "string"
  }
}
```

<a id="wifi-scan"></a>

## `wifi_scan`

**Method ID:** `wireless/wifi_scan`  
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

- Returned live Wi-Fi scan_list; management session recovered immediately.

<a id="wifi-set-ap-config"></a>

## `wifi_set_ap_config`

**Method ID:** `wireless/wifi_set_ap_config`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `DISRUPTIVE_RECOVERY_REQUIRED`

> [!WARNING]
> This method may interrupt management connectivity or require recovery/read-back. Treat a lost HTTP response as inconclusive until the resulting state has been verified.

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `mode`, `wifi_if_GUEST`, `wifi_timed_off`, `wifi_if_5G`, `wifi_if_24G`, `wifi_if_DUAL`.

Observed frontend transport variants:

- `direct_ajaxHandler` via `POST`; body present: `True`
- `direct_ajaxHandler` via `POST`; body present: `True`; keys: mode, wifi_if_GUEST
- `direct_ajaxHandler` via `POST`; body present: `True`; keys: wifi_timed_off
- `direct_ajaxHandler` via `POST`; body present: `True`; keys: wifi_if_5G, wifi_if_24G, wifi_if_DUAL

### Response

No stable response schema is currently documented.

### Semantics

- **`wifi.master.dual`**
  - `evidence`: original live WebUI source + live same-state writes
- **`wifi.master.split`**
  - `evidence`: original live WebUI source
- **`wifi.guest`**
  - `evidence`: live DUAL -> DUAL GUEST -> DUAL with reset/read-back/exact restore

### Notes

- Timed-off same-state and main DUAL AP same-state both returned result=0. Calls took ~15.8 s / ~13.9 s and required recovery handling.
- Treat lost HTTP response as inconclusive until recovery/re-login/read-back; Guest toggle was verified this way.
- 2026-08-25: DUAL GUEST -> 2.4G 5G GUEST -> DUAL GUEST live verified over USB recovery. Guest config and Wi-Fi secrets preserved; final original DUAL/Guest-off state restored.
- Guest maxassoc 10->9->10 live read/write/restore verified. Frontend maximum 10.

<a id="wifi-set-wps-disable"></a>

## `wifi_set_wps_disable`

**Method ID:** `wireless/wifi_set_wps_disable`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `DISRUPTIVE_RECOVERY_REQUIRED`

> [!WARNING]
> This method may interrupt management connectivity or require recovery/read-back. Treat a lost HTTP response as inconclusive until the resulting state has been verified.

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `wps_enable`.

### Response

Known/observed response fields: `wireless`.

### Notes

- Same-state wps_enable=1 sent as string '1' returned wireless.setting_response='OK'; call took ~17.4 s and recovery succeeded.
- 2026-08-25 controlled test with UPnP=0: WPS 0->1 did NOT enable UPnP. Manual statement about automatic UPnP enable is not true on live ACIY.3 runtime.

<a id="wps-status"></a>

## `wps_status`

**Method ID:** `wireless/wps_status`  
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
  "pbc_status": "string"
}
```

### Semantics

- **`wps.pbc_status.v1`**
  - `evidence`: STATIC_FRONTEND_COMMENT_VERIFIED_ACTIVE_EXECUTABLE
  - `field`: pbc_status
  - `values`: `["Disabled", "Active", "Timed-out", "Overlap", "Unknown"]`

