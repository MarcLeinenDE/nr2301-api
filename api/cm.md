# `cm` namespace

**21 methods** in the current public catalog.

Verification/auth/safety terminology: see [`../docs/method-status.md`](../docs/method-status.md).

| Method | Verification | Auth evidence | Safety |
|---|---|---|---|
| [`active_vpn_client_item`](#active-vpn-client-item) | `LIVE_VERIFIED` | `UNTESTED` | `WRITE_OR_SIDE_EFFECT` |
| [`add_vpn_client_item`](#add-vpn-client-item) | `LIVE_VERIFIED` | `UNTESTED` | `WRITE_OR_SIDE_EFFECT` |
| [`connect`](#connect) | `LIVE_VERIFIED` | `UNTESTED` | `DISRUPTIVE_RECOVERY_REQUIRED` |
| [`del_vpn_client_item`](#del-vpn-client-item) | `LIVE_VERIFIED` | `UNTESTED` | `WRITE_OR_SIDE_EFFECT` |
| [`disconnect`](#disconnect) | `LIVE_VERIFIED` | `UNTESTED` | `DISRUPTIVE_RECOVERY_REQUIRED` |
| [`edit_vpn_client_item`](#edit-vpn-client-item) | `LIVE_VERIFIED` | `UNTESTED` | `WRITE_OR_SIDE_EFFECT` |
| [`eng_get_bands`](#eng-get-bands) | `LIVE_DENIED` | `ADMIN_DENIED` | `READ_OR_LOW_SIDE_EFFECT` |
| [`eng_set_bands`](#eng-set-bands) | `STATIC_CONFIRMED` | `UNTESTED` | `DO_NOT_TEST_FOR_COVERAGE` |
| [`get_available_network_mode`](#get-available-network-mode) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_ca_info`](#get-ca-info) | `LIVE_VERIFIED_LIMITED` | `ADMIN_MULTICALL_ONLY` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_cell_info`](#get-cell-info) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_current_wan_info`](#get-current-wan-info) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_network_settings`](#get-network-settings) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_vpn_client_connect_status`](#get-vpn-client-connect-status) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_vpn_clients`](#get-vpn-clients) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`get_wan_settings`](#get-wan-settings) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`open_close_vpn_clients`](#open-close-vpn-clients) | `LIVE_VERIFIED` | `UNTESTED` | `WRITE_OR_SIDE_EFFECT` |
| [`query_eng_info`](#query-eng-info) | `LIVE_VERIFIED_LIMITED` | `ADMIN_MULTICALL_ONLY` | `READ_OR_LOW_SIDE_EFFECT` |
| [`set_eng_mode`](#set-eng-mode) | `STATIC_CONFIRMED` | `UNTESTED` | `DO_NOT_TEST_FOR_COVERAGE` |
| [`set_network_settings`](#set-network-settings) | `LIVE_VERIFIED` | `UNTESTED` | `WRITE_OR_SIDE_EFFECT` |
| [`set_wan_settings`](#set-wan-settings) | `LIVE_VERIFIED` | `UNTESTED` | `WRITE_OR_SIDE_EFFECT` |

<a id="active-vpn-client-item"></a>

## `active_vpn_client_item`

**Method ID:** `cm/active_vpn_client_item`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "index": "string/index",
  "vpn_active": "active | inactive"
}
```

### Response

No stable response schema is currently documented.

### Semantics

- **`vpn.profile_active`**
  - `evidence`: frontend exact; inactive action live rc=0

### Notes

- Temporary VPN item set inactive; rc=0.

<a id="add-vpn-client-item"></a>

## `add_vpn_client_item`

**Method ID:** `cm/add_vpn_client_item`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "index": "-1",
  "vpn_name": "string",
  "protocol_type": "pptp | l2tp | l2tp/ipsec",
  "vpn_server": "string",
  "vpn_user_name": "string",
  "vpn_user_password": "string",
  "vpn_secure": "string/optional by protocol"
}
```

### Response

Known/observed response fields: `result`.

### Semantics

- **`vpn.profile_add`**
  - `evidence`: temporary PPTP profile live-added and read back

### Notes

- Temporary PPTP test item added; read-back present.
- Do not log vpn_user_password or L2TP/IPsec vpn_secure (PSK) in public/client diagnostics.
- 2026-08-25: temporary inactive L2TP and L2TP/IPsec profiles were added, read back and deleted with exact final profile-count restore. No VPN connection was attempted.

<a id="connect"></a>

## `connect`

**Method ID:** `cm/connect`  
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

- result=0; management recovery succeeded.

<a id="del-vpn-client-item"></a>

## `del_vpn_client_item`

**Method ID:** `cm/del_vpn_client_item`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "index": "existing index"
}
```

### Response

Known/observed response fields: `result`.

### Semantics

- **`vpn.profile_delete`**
  - `evidence`: temporary profile live-deleted result=0

### Notes

- Temporary VPN item deleted; result=0; final list empty.
- 2026-08-25: temporary inactive L2TP and L2TP/IPsec profiles were added, read back and deleted with exact final profile-count restore. No VPN connection was attempted.

<a id="disconnect"></a>

## `disconnect`

**Method ID:** `cm/disconnect`  
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

- result=0; followed by reconnect and recovery.

<a id="edit-vpn-client-item"></a>

## `edit_vpn_client_item`

**Method ID:** `cm/edit_vpn_client_item`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "index": "existing index",
  "vpn_name": "string",
  "protocol_type": "pptp | l2tp | l2tp/ipsec",
  "vpn_server": "string",
  "vpn_user_name": "string",
  "vpn_user_password": "string",
  "vpn_secure": "string/optional by protocol"
}
```

### Response

Known/observed response fields: `result`, `vpn_c`.

### Semantics

- **`vpn.profile_edit`**
  - `evidence`: temporary PPTP profile live-edited result=0

### Notes

- Temporary VPN item edited; result=0.
- Do not log vpn_user_password or L2TP/IPsec vpn_secure (PSK) in public/client diagnostics.

<a id="eng-get-bands"></a>

## `eng_get_bands`

**Method ID:** `cm/eng_get_bands`  
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

<a id="eng-set-bands"></a>

## `eng_set_bands`

**Method ID:** `cm/eng_set_bands`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `STATIC_CONFIRMED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `DO_NOT_TEST_FOR_COVERAGE`

> [!CAUTION]
> This method was deliberately not exercised merely to improve coverage because its potential impact outweighed the documentation value. Treat the contract as static evidence only.

### Request

HTTP method: `POST`

No request body has been reconstructed as necessary for this method.

### Response

Known/observed response fields: `cm`.

<a id="get-available-network-mode"></a>

## `get_available_network_mode`

**Method ID:** `cm/get_available_network_mode`  
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
  "network_modes": [
    "string"
  ],
  "result": "integer"
}
```

<a id="get-ca-info"></a>

## `get_ca_info`

**Method ID:** `cm/get_ca_info`  
**Endpoint:** `/api.cgi`  
**Operation type:** `ENGINEERING_READ`  
**Verification:** `LIVE_VERIFIED_LIMITED`  
**Auth evidence:** `ADMIN_MULTICALL_ONLY`  
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
- Normal admin MUST dispatch this read via /api.cgi?multicalls=1. A one-member multicall is sufficient; direct path/method dispatch is authorization-denied.
- During live NSA n28, nr_ca_info[] was empty despite query_eng_info exposing the active NR cell. Do not use nr_ca_info alone to determine NR attachment.
- Live 5G SA n28 also returned ca_info=[] and nr_ca_info=[]. Empty CA arrays do not imply absence of 5G.

<a id="get-cell-info"></a>

## `get_cell_info`

**Method ID:** `cm/get_cell_info`  
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
  "celluar_basic_info": {
    "data_mode": "integer",
    "network_name": "string",
    "roaming": "integer",
    "roaming_network_name": "string"
  },
  "signal_info": [
    {
      "level": "integer",
      "rat": "string"
    }
  ]
}
```

### Semantics

- **`cell.data_mode_full_enum.v1`**
  - `evidence`: STATIC_FRONTEND_VERIFIED_PLUS_LIVE_14_19_21_22
  - `field`: celluar_basic_info.data_mode
  - `range`: 1..22
- **`cell.signal_level_rendering.v2`**
  - `evidence`: STATIC_FRONTEND_RECONCILED
  - `field`: signal_info[].level
  - `raw_bar_range`: 0..5
  - `important`: Frontend render levels 6=no service and 7=no SIM/SIM error are synthesized from RAT/SIM state and are not promoted as raw API enum values.

### Notes

- Live WebUI correlation: signal_info[].level maps directly to the five-level signal UI (4 -> 4/5, 3 -> 3/5 in an NSA capture). Keep this separate from detailed dBm/dB metrics.
- Observed live transition: data_mode 19 (4G+/LTE-A) -> 22 (5G NSA), while WAN IPv4 remained unchanged.
- The stock frontend synthesizes render level 6 from rat=="no service" and level 7 from SIM status !=1. Do not document 6/7 as proven raw signal_info[].level values.

<a id="get-current-wan-info"></a>

## `get_current_wan_info`

**Method ID:** `cm/get_current_wan_info`  
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
  "contextlist": [
    {
      "connection_status": "integer",
      "internet_status": "integer",
      "ipv4_dns1": "string",
      "ipv4_dns2": "string",
      "ipv4_gateway": "string",
      "ipv4_ip": "string",
      "ipv4_submask": "string",
      "ipv6_dns1": "string",
      "ipv6_dns2": "string",
      "ipv6_gateway": "string",
      "ipv6_ip": "string"
    }
  ],
  "wan_name": "string",
  "wan_type": "string"
}
```

### Semantics

- **`wan.link_vs_internet.v1`**
  - `evidence`: FRONTEND_SOURCE_VERIFIED
  - `note`: Keep upstream/link connectivity separate from Internet availability.

### Notes

- Clients should parse connection_status/internet_status numerically; string '0' represents the false state and must not be treated as truthy-connected. Keep Internet availability separate from WAN-link state.

<a id="get-network-settings"></a>

## `get_network_settings`

**Method ID:** `cm/get_network_settings`  
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
  "network_settings": {
    "connect_mode": "string",
    "data_roaming": "string",
    "network_mode": "string",
    "profile": {
      "active_index": "integer",
      "data": [
        {
          "apn": "string",
          "auth_type": "string",
          "ip_type": "string",
          "name": "string",
          "password": "string",
          "username": "string"
        }
      ]
    },
    "profile_mode": "string"
  },
  "result": "integer"
}
```

<a id="get-vpn-client-connect-status"></a>

## `get_vpn_client_connect_status`

**Method ID:** `cm/get_vpn_client_connect_status`  
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
  "vpn_status": "string"
}
```

<a id="get-vpn-clients"></a>

## `get_vpn_clients`

**Method ID:** `cm/get_vpn_clients`  
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
  "vpn_client_active_index": "string",
  "vpn_client_enable": "string",
  "vpn_clients": [
    "<empty>"
  ]
}
```

### Notes

- Response may contain VPN profile passwords/PSKs; redact before logging.
- 2026-08-25: temporary inactive L2TP and L2TP/IPsec profiles were added, read back and deleted with exact final profile-count restore. No VPN connection was attempted.

<a id="get-wan-settings"></a>

## `get_wan_settings`

**Method ID:** `cm/get_wan_settings`  
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
  "mobile_ping_enable": "integer",
  "ping_address": "string",
  "static": {
    "ipv4_gw": "string",
    "ipv4_ip": "string",
    "ipv4_mask": "string"
  },
  "wan_type_primary": "string",
  "wifi_extender": {
    "password": "string",
    "ssid": "string"
  }
}
```

<a id="open-close-vpn-clients"></a>

## `open_close_vpn_clients`

**Method ID:** `cm/open_close_vpn_clients`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "vpn_client_enable": "enable | disable"
}
```

### Response

Known/observed response fields: `result`.

### Semantics

- **`vpn.global_enable`**
  - `evidence`: 2026-08-25: disable -> enable result=0/read-back enable -> disable result=0/read-back disable; exact initial state restored

### Notes

- Same-state global VPN enable returned result=0.
- Global VPN enable transition and exact restore are now live verified.

<a id="query-eng-info"></a>

## `query_eng_info`

**Method ID:** `cm/query_eng_info`  
**Endpoint:** `/api.cgi`  
**Operation type:** `ENGINEERING_READ`  
**Verification:** `LIVE_VERIFIED_LIMITED`  
**Auth evidence:** `ADMIN_MULTICALL_ONLY`  
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

### Semantics

- **`radio.invalid_int16_min.v1`**
  - `evidence`: LIVE_OBSERVED_NR2301_PLUS_QUALCOMM_QMI_CORROBORATED
  - `field`: sinr

### Notes

- Normal admin session: HTTP 200 JSON system_err='authorization is not ok'.
- Normal admin MUST dispatch this read via /api.cgi?multicalls=1. A one-member multicall is sufficient; direct path/method dispatch is authorization-denied.
- NSA live verified: eng_info.data contains both 'nr5g-nsa' and 'lte'. NR RSSI was absent; treat missing metrics as unavailable, never synthesize them.
- 5G SA live verified: eng_info.rat='nr5g-sa' and eng_info.data is a flat NR serving-cell object. RSSI and explicit frequency strings were absent in the capture.

<a id="set-eng-mode"></a>

## `set_eng_mode`

**Method ID:** `cm/set_eng_mode`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `STATIC_CONFIRMED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `DO_NOT_TEST_FOR_COVERAGE`

> [!CAUTION]
> This method was deliberately not exercised merely to improve coverage because its potential impact outweighed the documentation value. Treat the contract as static evidence only.

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `mode`.

### Response

No stable response schema is currently documented.

<a id="set-network-settings"></a>

## `set_network_settings`

**Method ID:** `cm/set_network_settings`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

Known top-level request keys from the shipped frontend: `data_roaming`, `network_mode`.

Observed frontend transport variants:

- `direct_ajaxHandler` via `POST`; body present: `True`
- `direct_ajaxHandler` via `POST`; body present: `True`; keys: data_roaming
- `direct_ajaxHandler` via `POST`; body present: `True`; keys: network_mode

### Response

Known/observed response fields: `result`.

### Semantics

- **`mobile.network_mode`**
  - `evidence`: available modes read live; same-state network settings live verified

### Notes

- Two same-state variants returned result=0; read-back unchanged.

<a id="set-wan-settings"></a>

## `set_wan_settings`

**Method ID:** `cm/set_wan_settings`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

No request body has been reconstructed as necessary for this method.

### Response

Known/observed response fields: `result`, `wan_type_primary`, `wifi_extender`.

### Notes

- Same-state WAN/extender write returned result=0; read-back unchanged.

