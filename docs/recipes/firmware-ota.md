# Firmware / OTA recipes

Detailed reference: [`ota`](../../api/ota.md).

Firmware update APIs can download/install new firmware and potentially reboot or leave the device temporarily unreachable. The current research intentionally distinguishes **checking/status** from **actually installing**.

## Read current OTA state

POST `ota/new_query`:

```json
{
  "type": 1
}
```

Known state strings include:

- `idle`
- `checking`
- `checked` — source-verified meaning: update available
- `updating,manual_fota`
- `updating,local`
- `updating,auto_fota`
- `success`
- `failed`

Important: an immediate `idle` response is neutral. It is not by itself proof that the firmware is current.

## Manually check for an update

Call `ota/manual_check_update`, then poll `ota/new_query` rather than treating the immediate return as the final update result.

The stock frontend waits through repeated polling before presenting its no-update result. A client should therefore model checking as a state machine, not a single synchronous request.

## Firmware-updated notification flag

GET `ota/get_updated_status`.

`fota_auto_upgrade_status` is documented as a notification/status flag. Do **not** label it as an "automatic updates enabled" setting.

## Clear a failed state

`ota/clear_failed_state` is live verified and returned `result='0'` in testing. Use it only when there is an applicable failed OTA state, then query the OTA state again.

## Abandon/cancel states

- `ota/abandon_checked`
- `ota/abandon_download_update`

Both endpoints exist, but the live tests occurred while there was no corresponding active checked/download state and therefore returned not-applicable responses. Treat them as state-dependent operations.

## Download/install update — reference only

`ota/download_update` is statically confirmed but deliberately classified `DO_NOT_TEST_FOR_COVERAGE`.

This repository does not provide a "run this command to install firmware" recipe because that path was not deliberately live exercised merely to improve API coverage. Applications should not promote it to a one-click operation without firmware-specific validation, power/recovery planning and explicit user confirmation.