# `ota` namespace

**7 methods** in the current public catalog.

Verification/auth/safety terminology: see [`../docs/method-status.md`](../docs/method-status.md).

| Method | Verification | Auth evidence | Safety |
|---|---|---|---|
| [`abandon_checked`](#abandon-checked) | `LIVE_NOT_APPLICABLE` | `UNTESTED` | `WRITE_OR_SIDE_EFFECT` |
| [`abandon_download_update`](#abandon-download-update) | `LIVE_NOT_APPLICABLE` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |
| [`clear_failed_state`](#clear-failed-state) | `LIVE_VERIFIED` | `UNTESTED` | `WRITE_OR_SIDE_EFFECT` |
| [`download_update`](#download-update) | `STATIC_CONFIRMED` | `UNTESTED` | `DO_NOT_TEST_FOR_COVERAGE` |
| [`get_updated_status`](#get-updated-status) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |
| [`manual_check_update`](#manual-check-update) | `LIVE_VERIFIED_LIMITED` | `UNTESTED` | `WRITE_OR_SIDE_EFFECT` |
| [`new_query`](#new-query) | `LIVE_VERIFIED` | `ADMIN_OK` | `READ_OR_LOW_SIDE_EFFECT` |

<a id="abandon-checked"></a>

## `abandon_checked`

**Method ID:** `ota/abandon_checked`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_NOT_APPLICABLE`  
**Auth evidence:** `UNTESTED`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `GET`

No request body has been reconstructed as necessary for this method.

### Response

No stable response schema is currently documented.

### Notes

- result='-1', response='not checked' because no checked OTA state was active.

<a id="abandon-download-update"></a>

## `abandon_download_update`

**Method ID:** `ota/abandon_download_update`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_NOT_APPLICABLE`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `GET`

No request body has been reconstructed as necessary for this method.

### Response

No stable response schema is currently documented.

### Notes

- HTTP 200 result='-1', response='not updating' because no OTA download/install session was active.

<a id="clear-failed-state"></a>

## `clear_failed_state`

**Method ID:** `ota/clear_failed_state`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `GET`

No request body has been reconstructed as necessary for this method.

### Response

No stable response schema is currently documented.

### Notes

- result='0'.

<a id="download-update"></a>

## `download_update`

**Method ID:** `ota/download_update`  
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

### Semantics

- **`ota.download_error.v1`**
  - `evidence`: FRONTEND_SOURCE_VERIFIED

<a id="get-updated-status"></a>

## `get_updated_status`

**Method ID:** `ota/get_updated_status`  
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
  "fota_auto_upgrade_status": "string",
  "result": "string"
}
```

### Semantics

- **`ota.auto_upgrade_notification.v1`**
  - `evidence`: STATIC_FRONTEND_VERIFIED
  - `field`: fota_auto_upgrade_status
  - `values`: `{"1": "show firmware-updated notification", "0": "no such notification"}`
  - `important`: Notification/status flag, not an Automatic Updates setting.

<a id="manual-check-update"></a>

## `manual_check_update`

**Method ID:** `ota/manual_check_update`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED_LIMITED`  
**Auth evidence:** `UNTESTED`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `GET`

No request body has been reconstructed as necessary for this method.

### Response

No stable response schema is currently documented.

### Notes

- ret='0'; subsequent new_query remained idle.
- manual_check_update HTTP200 ret=0 live verified; no download/install. new_query remained idle and get_updated_status remained result=-1 during poll window. Do not map idle alone to 'no update available'.

<a id="new-query"></a>

## `new_query`

**Method ID:** `ota/new_query`  
**Endpoint:** `/api.cgi`  
**Operation type:** `READ`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `READ_OR_LOW_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "type": 1
}
```

### Response

```json
{
  "response": "string"
}
```

### Semantics

- **`ota.state.v2`**
  - `evidence`: STATIC_FRONTEND_VERIFIED_PLUS_LIVE_IDLE
  - `field`: response
  - `values`: `{"idle": "neutral/ready; context-dependent no-update only after ~30 polls following manual request", "checking": "checking", "checked": "update available", "updating,manual_fota": "manual update in progress", "updating,local": "local update in progress", "updating,auto_fota": "automatic update in progress", "success": "success", "failed": "failed"}`
  - `important`: `["checked is source-verified update-available but has not been positively live-observed.", "idle alone remains neutral and must not be labeled firmware-current."]`

### Notes

- Live response='idle'. Frontend status enum includes idle, updating,local, success, failed. Anonymous live response: HTTP 200 {'system_err':'session no exist'}.
- Conflict resolution an earlier research run: set_update.html case checked is explicitly commented as update found and calls render_release_note(); canonical meaning is update available (STATIC_FRONTEND_VERIFIED_NOT_LIVE_OBSERVED).
- Idle remains context-sensitive: after manual_check_update the WebUI waits ~30 one-second polls before showing its no-update message. Immediate idle is not proof firmware is current.

