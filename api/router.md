# `router` namespace

**27 methods** in the current public catalog.

Verification/auth/safety terminology: see [`../docs/method-status.md`](../docs/method-status.md).

| Method | Verification | Auth evidence | Safety |
|---|---|---|---|
| [`eng_check_adbd_status`](#eng-check-adbd-status) | `LIVE_DENIED` | `ADMIN_DENIED` | `READ_OR_LOW_SIDE_EFFECT` |
| [`eng_get_usb_mode`](#eng-get-usb-mode) | `LIVE_DENIED` | `ADMIN_DENIED` | `READ_OR_LOW_SIDE_EFFECT` |
| [`eng_set_usb_mode`](#eng-set-usb-mode) | `STATIC_CONFIRMED` | `UNTESTED` | `DO_NOT_TEST_FOR_COVERAGE` |
| [`get_device_info`](#get-device-info) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_diag_info`](#get-diag-info) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_diag_internet_info`](#get-diag-internet-info) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_feature_list`](#get-feature-list) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_mac_info`](#get-mac-info) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_runtime_info`](#get-runtime-info) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_ui_language`](#get-ui-language) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`restart_web_server`](#restart-web-server) | `LIVE_VERIFIED` | `UNTESTED` | `DISRUPTIVE_RECOVERY_REQUIRED` |
| [`router_backup_config`](#router-backup-config) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`router_call_reboot`](#router-call-reboot) | `LIVE_VERIFIED` | `ADMIN_OK` | `DISRUPTIVE_RECOVERY_REQUIRED` |
| [`router_call_rst_factory`](#router-call-rst-factory) | `STATIC_CONFIRMED` | `UNTESTED` | `DO_NOT_TEST_FOR_COVERAGE` |
| [`router_get_dhcp_settings`](#router-get-dhcp-settings) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`router_get_dhcp_settings_comb`](#router-get-dhcp-settings-comb) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`router_get_dhcp_static_ip`](#router-get-dhcp-static-ip) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`router_get_lan_ip`](#router-get-lan-ip) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`router_get_timed_reboot`](#router-get-timed-reboot) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`router_get_work_mode`](#router-get-work-mode) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`router_restart_adb`](#router-restart-adb) | `STATIC_CONFIRMED` | `UNTESTED` | `DO_NOT_TEST_FOR_COVERAGE` |
| [`router_set_dhcp_settings_comb`](#router-set-dhcp-settings-comb) | `LIVE_VERIFIED` | `ADMIN_OK` | `DISRUPTIVE_RECOVERY_REQUIRED` |
| [`router_set_dhcp_static_ip`](#router-set-dhcp-static-ip) | `LIVE_VERIFIED` | `UNKNOWN` | `DISRUPTIVE_RECOVERY_REQUIRED` |
| [`router_set_lan_ip`](#router-set-lan-ip) | `LIVE_VERIFIED` | `ADMIN_OK` | `DISRUPTIVE_RECOVERY_REQUIRED` |
| [`router_set_timed_reboot`](#router-set-timed-reboot) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`router_set_work_mode`](#router-set-work-mode) | `LIVE_VERIFIED` | `UNKNOWN` | `DISRUPTIVE_RECOVERY_REQUIRED` |
| [`set_ui_language`](#set-ui-language) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |

<a id="eng-check-adbd-status"></a>

## `eng_check_adbd_status`

**Method ID:** `router/eng_check_adbd_status`  
**Endpoint:** `/api.cgi`  
**Operation type:** `ENGINEERING_READ`  
**Verification:** `LIVE_DENIED`  
**Auth evidence:** `ADMIN_DENIED`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `GET`

No request body has been reconstructed as necessary for this method.

### Response

```json
{
  "system_err": "string"
}
```

### Notes

- Normal admin session: HTTP 200 JSON system_err='authorization is not ok'.

<a id="eng-get-usb-mode"></a>

## `eng_get_usb_mode`

**Method ID:** `router/eng_get_usb_mode`  
**Endpoint:** `/api.cgi`  
**Operation type:** `ENGINEERING_READ`  
**Verification:** `LIVE_DENIED`  
**Auth evidence:** `ADMIN_DENIED`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `GET`

No request body has been reconstructed as necessary for this method.

### Response

```json
{
  "system_err": "string"
}
```

### Notes

- Normal admin session: HTTP 200 JSON system_err='authorization is not ok'.

<a id="eng-set-usb-mode"></a>

## `eng_set_usb_mode`

**Method ID:** `router/eng_set_usb_mode`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `STATIC_CONFIRMED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `DO_NOT_TEST_FOR_COVERAGE`

> [!CAUTION]
> This method was deliberately not exercised merely to improve coverage because its potential impact outweighed the documentation value. Treat the contract as static evidence only.

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `usb_mode`.

### Response

No stable response schema is currently documented.

<a id="get-device-info"></a>

## `get_device_info`

**Method ID:** `router/get_device_info`  
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
  "ICCID": "string",
  "IMEI": "string",
  "IMSI": "string",
  "MDN": "string",
  "device_type": "string",
  "domain": "string",
  "lang_list": "string",
  "platform": "string",
  "result": "integer",
  "sn": "string"
}
```

<a id="get-diag-info"></a>

## `get_diag_info`

**Method ID:** `router/get_diag_info`  
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
  "cpu_temp_normal": "integer",
  "cpu_usage_lv": "integer",
  "login_pwd_lv": "integer",
  "mem_usage_lv": "integer",
  "wan_st": "integer"
}
```

### Semantics

- **`diag.router_levels.v1`**
  - `evidence`: STATIC_FRONTEND_VERIFIED
- **`diag.backend_thresholds.v2`**
  - `evidence`: FIRMWARE_BACKEND_VERIFIED

<a id="get-diag-internet-info"></a>

## `get_diag_internet_info`

**Method ID:** `router/get_diag_internet_info`  
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
  "access": "integer"
}
```

### Semantics

- **`diag.internet_access.v1`**
  - `evidence`: STATIC_FRONTEND_VERIFIED
  - `field`: access
  - `values`: `{"1": "available", "0": "unavailable"}`

<a id="get-feature-list"></a>

## `get_feature_list`

**Method ID:** `router/get_feature_list`  
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
  "features": {
    "device_type": "string",
    "local_update": "integer",
    "phonebook": "integer",
    "sdcard": "integer",
    "sms": "integer",
    "username": "integer",
    "ussd": "integer",
    "wds": "integer",
    "wifi_extender": "integer",
    "wizard": "integer"
  },
  "result": "integer"
}
```

<a id="get-mac-info"></a>

## `get_mac_info`

**Method ID:** `router/get_mac_info`  
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
  "5g_mac": "string",
  "eth_mac": "string",
  "extender_mac": "string",
  "guest_mac": "string",
  "result": "integer",
  "rndis_mac": "string",
  "wifi_mac": "string"
}
```

<a id="get-runtime-info"></a>

## `get_runtime_info`

**Method ID:** `router/get_runtime_info`  
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
  "boot_time": "integer",
  "cpu_temperature": "integer",
  "cpu_used_percentage": "integer",
  "memory_used_percentage": "integer",
  "result": "integer"
}
```

<a id="get-ui-language"></a>

## `get_ui_language`

**Method ID:** `router/get_ui_language`  
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
  "language": "string",
  "result": "integer"
}
```

### Semantics

- **`ui_language.transport_codes.v1`**
  - `evidence`: STATIC_FRONTEND_VERIFIED

<a id="restart-web-server"></a>

## `restart_web_server`

**Method ID:** `router/restart_web_server`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `DISRUPTIVE_RECOVERY_REQUIRED`

> [!WARNING]
> This method may interrupt management connectivity or require recovery/read-back. Treat a lost HTTP response as inconclusive until the resulting state has been verified.

### Request

HTTP method: `GET`

No request body has been reconstructed as necessary for this method.

### Response

No stable response schema is currently documented.

### Notes

- HTTP 200 empty response; web server recovered and admin re-login succeeded.

<a id="router-backup-config"></a>

## `router_backup_config`

**Method ID:** `router/router_backup_config`  
**Endpoint:** `/api.cgi`  
**Operation type:** `EXPORT_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `GET`

No request body has been reconstructed as necessary for this method.

### Response

Known/observed response fields: `rc`.

### Notes

- GET returned rc=0 and internal file path /var/volatile/config_bak/config_bak.bin. Current frontend backup UI bypasses this legacy action and downloads via /file.cgi.

<a id="router-call-reboot"></a>

## `router_call_reboot`

**Method ID:** `router/router_call_reboot`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `DISRUPTIVE_RECOVERY_REQUIRED`

> [!WARNING]
> This method may interrupt management connectivity or require recovery/read-back. Treat a lost HTTP response as inconclusive until the resulting state has been verified.

### Request

HTTP method: `not fully reconstructed`

No request body has been reconstructed as necessary for this method.

Observed frontend transport variants:

- `direct_ajaxHandler` via `GET`; body present: `False`
- `direct_ajaxHandler` via `POST`; body present: `True`

### Response

No stable response schema is currently documented.

### Notes

- Request timed out after 40 s because device rebooted during call. Router later recovered and normal admin re-login succeeded on recovery attempt 18.

<a id="router-call-rst-factory"></a>

## `router_call_rst_factory`

**Method ID:** `router/router_call_rst_factory`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `STATIC_CONFIRMED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `DO_NOT_TEST_FOR_COVERAGE`

> [!CAUTION]
> This method was deliberately not exercised merely to improve coverage because its potential impact outweighed the documentation value. Treat the contract as static evidence only.

### Request

HTTP method: `GET`

No request body has been reconstructed as necessary for this method.

### Response

No stable response schema is currently documented.

<a id="router-get-dhcp-settings"></a>

## `router_get_dhcp_settings`

**Method ID:** `router/router_get_dhcp_settings`  
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
  "dhcp": {
    "disabled": "string",
    "dns1": "string",
    "dns2": "string",
    "dnsmode": "string",
    "ipv6dns1": "string",
    "ipv6dns2": "string",
    "leasetime": "string",
    "limit": "string",
    "mtu": "string",
    "start": "string"
  }
}
```

<a id="router-get-dhcp-settings-comb"></a>

## `router_get_dhcp_settings_comb`

**Method ID:** `router/router_get_dhcp_settings_comb`  
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
  "dhcp": {
    "disabled": "string",
    "dns1": "string",
    "dns2": "string",
    "dnsmode": "string",
    "end": "string",
    "ipv6dns1": "string",
    "ipv6dns2": "string",
    "lan_ip": "string",
    "lan_netmask": "string",
    "leasetime": "string",
    "mtu": "string",
    "start": "string"
  }
}
```

### Notes

- Authenticated response observed; anonymous HTTP 200 body is {"system_err":"session no exist"}.

<a id="router-get-dhcp-static-ip"></a>

## `router_get_dhcp_static_ip`

**Method ID:** `router/router_get_dhcp_static_ip`  
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
  "dhcp": {
    "cnt": "integer",
    "data": [
      "<empty>"
    ]
  }
}
```

### Notes

- Authenticated response observed with cnt=0 and empty data[] on tested device; item fields index/mac/ip remain statically evidenced.

<a id="router-get-lan-ip"></a>

## `router_get_lan_ip`

**Method ID:** `router/router_get_lan_ip`  
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
  "router": {
    "lan_ip": "string",
    "lan_netmask": "string"
  }
}
```

<a id="router-get-timed-reboot"></a>

## `router_get_timed_reboot`

**Method ID:** `router/router_get_timed_reboot`  
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
  "repeat": "integer",
  "result": "integer",
  "time": "string"
}
```

### Semantics

- **`timed_reboot.repeat_bitmask.v1`**
  - `evidence`: STATIC_FRONTEND_EXECUTABLE_VERIFIED
  - `field`: repeat
  - `bits`: `{"0": "Sunday", "1": "Monday", "2": "Tuesday", "3": "Wednesday", "4": "Thursday", "5": "Friday", "6": "Saturday", "7": "No repeat"}`

<a id="router-get-work-mode"></a>

## `router_get_work_mode`

**Method ID:** `router/router_get_work_mode`  
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
  "work_mode": "string"
}
```

### Semantics

- **`work_mode.platform.v1`**
  - `evidence`: FRONTEND_SOURCE_VERIFIED
  - `values`: `["router", "bridge"]`

<a id="router-restart-adb"></a>

## `router_restart_adb`

**Method ID:** `router/router_restart_adb`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `STATIC_CONFIRMED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `DO_NOT_TEST_FOR_COVERAGE`

> [!CAUTION]
> This method was deliberately not exercised merely to improve coverage because its potential impact outweighed the documentation value. Treat the contract as static evidence only.

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `adbkey`.

### Response

Known/observed response fields: `result`.

<a id="router-set-dhcp-settings-comb"></a>

## `router_set_dhcp_settings_comb`

**Method ID:** `router/router_set_dhcp_settings_comb`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `DISRUPTIVE_RECOVERY_REQUIRED`

> [!WARNING]
> This method may interrupt management connectivity or require recovery/read-back. Treat a lost HTTP response as inconclusive until the resulting state has been verified.

### Request

HTTP method: `POST`

```json
{
  "disabled": "unknown/static",
  "lan_ip": "unknown/static",
  "lan_netmask": "unknown/static",
  "start": "unknown/static",
  "end": "unknown/static",
  "leasetime": "unknown/static",
  "mtu": "unknown/static",
  "dnsmode": "unknown/static",
  "dns1": "unknown/static",
  "dns2": "unknown/static",
  "ipv6dns1": "unknown/static",
  "ipv6dns2": "unknown/static"
}
```

### Response

Known/observed response fields: `router.setting_response`, `router.result`.

### Semantics

- **`dhcp.core`**
  - `evidence`: live same-state frontend-form multicall reset + recovery/read-back

### Notes

- 2026-08-31 public-SDK physical test through normal admin: DNS-only mutation preserved all seven non-DNS fields; the original complete 12-field DHCP/DNS object was restored and matched exactly on final read-back.
- Frontend-form multicall reset TCP connection; recovery succeeded and read-back unchanged.
- Original UI normally sends this as a multicall member with outer toStringData=false; LAN/DHCP changes can reset management TCP.
- Manual DNS is upstream DNS for the NR2301 DNS proxy, not direct DHCP option-6 distribution of the configured public resolvers.

<a id="router-set-dhcp-static-ip"></a>

## `router_set_dhcp_static_ip`

**Method ID:** `router/router_set_dhcp_static_ip`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `UNKNOWN`  
**Safety:** `DISRUPTIVE_RECOVERY_REQUIRED`

> [!WARNING]
> This method may interrupt management connectivity or require recovery/read-back. Treat a lost HTTP response as inconclusive until the resulting state has been verified.

### Request

HTTP method: `POST`

```json
{
  "data": "unknown/static"
}
```

### Response

Known/observed response fields: `dhcp.setting_response`.

### Semantics

- **`dhcp.static_reservations`**
  - `evidence`: 2026-08-25: empty table -> add index0 locally-administered MAC at 192.0.2.254 -> HTTP200 setting_response=OK -> read-back present -> exact empty-table restore -> read-back empty

### Notes

- Frontend-form multicall reset TCP connection; recovery succeeded and read-back unchanged.
- Original UI supports exactly 10 visible mapping slots (indices 0..9); setter is normally a multicall member with outer toStringData=false.
- State transition now live verified using a temporary free-slot reservation outside the dynamic DHCP pool.

<a id="router-set-lan-ip"></a>

## `router_set_lan_ip`

**Method ID:** `router/router_set_lan_ip`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `DISRUPTIVE_RECOVERY_REQUIRED`

> [!WARNING]
> This method may interrupt management connectivity or require recovery/read-back. Treat a lost HTTP response as inconclusive until the resulting state has been verified.

### Request

HTTP method: `POST`

```json
{
  "lan_ip": "unknown/static",
  "lan_netmask": "unknown/static"
}
```

### Response

No stable response schema is currently documented.

### Notes

- Deprecated same-state LAN setter returned router.setting_response='OK'; management recovery succeeded.

<a id="router-set-timed-reboot"></a>

## `router_set_timed_reboot`

**Method ID:** `router/router_set_timed_reboot`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `enable`, `time`, `repeat`.

### Response

Known/observed response fields: `router`.

<a id="router-set-work-mode"></a>

## `router_set_work_mode`

**Method ID:** `router/router_set_work_mode`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `UNKNOWN`  
**Safety:** `DISRUPTIVE_RECOVERY_REQUIRED`

> [!WARNING]
> This method may interrupt management connectivity or require recovery/read-back. Treat a lost HTTP response as inconclusive until the resulting state has been verified.

### Request

HTTP method: `POST`

```json
{
  "work_mode": "unknown/static"
}
```

### Response

No stable response schema is currently documented.

### Notes

- Frontend-form multicall reset TCP connection; recovery succeeded and work_mode remained router.

<a id="set-ui-language"></a>

## `set_ui_language`

**Method ID:** `router/set_ui_language`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `language`.

### Response

Known/observed response fields: `result`.

### Semantics

- **`ui_language.transport_codes.v1`**
  - `evidence`: STATIC_FRONTEND_VERIFIED
  - `important`: Use lowercase router API codes; uppercase strings are display abbreviations, not transport values.

