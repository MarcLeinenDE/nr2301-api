# System maintenance recipes

Detailed references: [`router`](../../api/router.md), [`aoc`](../../api/aoc.md) and [`version`](../../api/version.md).

## Read firmware/runtime identity

Use `version/get_ww_version`, `router/get_device_info`, `router/get_runtime_info` and `router/get_feature_list` as appropriate. See [Device status and diagnostics](device-status-diagnostics.md) for monitoring-oriented reads.

## Reboot the router

`router/router_call_reboot` is live verified and classified `DISRUPTIVE_RECOVERY_REQUIRED`. A 2026-09-18 production-SDK lifecycle physically reconfirmed the body-less GET frontend variant: management dropped, the device later recovered, and `boot_time` reset from 13911 to 51.

The stock frontend has both GET/POST observations for this action. The live request timed out because the router rebooted, then the device recovered and normal admin login succeeded later.

Safe client behavior:

1. present an explicit confirmation;
2. send the reboot action;
3. treat connection loss/timeout as expected but not definitive success;
4. stop ordinary API traffic while the device is rebooting;
5. poll the management address conservatively;
6. perform a fresh login and normal read to confirm recovery.

## Factory reset — reference only

`router/router_call_rst_factory` is statically confirmed and intentionally `DO_NOT_TEST_FOR_COVERAGE`.

Do not expose it as a casual recipe/action merely because the method name is known. A factory reset destroys configuration and can change management credentials/addressing.

## Schedule automatic reboot

Read `router/router_get_timed_reboot`.

Write `router/router_set_timed_reboot` with:

```json
{
  "enable": 1,
  "time": "03:30",
  "repeat": 62
}
```

`repeat` is a bitmask:

- bit 0 Sunday
- bit 1 Monday
- bit 2 Tuesday
- bit 3 Wednesday
- bit 4 Thursday
- bit 5 Friday
- bit 6 Saturday
- bit 7 no-repeat

The numeric example above is illustrative; compute the bitmask for the intended schedule and read the setting back after writing.

> [!NOTE]
> A targeted public-SDK lifecycle on tested firmware `V1.00(ACIY.3)C0` on 2026-09-08 first observed the raw getter value `time="0:0"`, proving that `router_get_timed_reboot.time` is not guaranteed to be zero-padded `HH:MM`. After the client was corrected to compare parsed hour/minute semantics, a disabled probe schedule (`enable=0`) was written, read back successfully, and the original `enable`/`time`/`repeat` state was restored and verified. The SDK used canonical zero-padded times for setter writes. Clients should preserve the raw getter value but compare parsed hour/minute semantics when deciding whether a schedule matches or has been restored.

## Configuration backup and restore

`router/router_backup_config` is a legacy action returning an internal backup path. A 2026-09-18 production-SDK run reconfirmed the body-less GET action with `rc=0`. The current stock UI bypasses that action for the actual backup download.

Current source-verified backup download:

```text
GET /file.cgi?Action=Download&file=backup_config&dl=1
```

Current source-verified restore transport:

```text
POST /file.cgi?Action=Upload&file=restore_config
Content-Type: application/octet-stream
<body: raw configuration bytes>
```

The frontend uploads sequential 1 MiB chunks, without multipart/form-data, filename form fields or `Content-Range`. Its selected-file limit is 200 MiB. A response containing `other error` is failure. The final successful chunk has no separate API apply call; the frontend expects the device to reboot after a successful restore.

A safe restore client should snapshot externally observable state, upload only a trusted backup, tolerate management loss on the last chunk, wait for device recovery, log in again and verify both a fresh boot and restored state.

Physical restore testing on 2026-09-21 showed that `router/get_runtime_info` can become readable before every subsystem is fully API-ready: a later firewall/UPnP read briefly returned HTTP 200 with an empty body. Verification clients should therefore retry the **entire required configuration snapshot** until all relevant reads succeed in one pass before comparing restored state.

Configuration backups can contain secrets. Treat backup bytes as sensitive, never commit them to this repository and never include them in diagnostics without explicit sanitization.

## Change UI language

Read `router/get_ui_language`, then POST `router/set_ui_language` with:

```json
{
  "language": "ROUTER_LANGUAGE_CODE"
}
```

Use lowercase router transport codes from the documented semantics. Uppercase abbreviations used for display are not necessarily API values.

On tested firmware `V1.00(ACIY.3)C0` on 2026-09-08, `router/get_device_info.lang_list` advertised the runtime list `en,dk,fr,fi,pt,it,se,de` while the current language was `en`. A targeted public-SDK reversible test changed `en → de`, required exact `router/get_ui_language` read-back, then restored `de → en` in `finally` and passed `1/1` in 1.33 s.

Clients should treat `lang_list` as the target router's runtime capability list rather than assuming the observed ACIY.3 list is universal. Validate a requested lowercase transport code against the current `lang_list`, avoid same-state writes, and verify the getter after changing it.

## Auto-sleep / power timeout

- read: `aoc/sleep_wait_time`
- write: `aoc/set_sleep_wait_time` with `time`

Verified frontend values are `0` (off), `10`, `20`, `30`, `40` and `60` minutes.

Example:

```json
{
  "time": 30
}
```

Read the value back afterward.

## Restart web server

`router/restart_web_server` is live verified but disruptive to management. Treat it with the same reconnect/re-login/read-back discipline used for other management-path disruptions. In the 2026-09-18 production-SDK lifecycle it returned an empty/non-JSON body (`ProtocolError` at the strict JSON layer), but management remained available/recovered and `boot_time` advanced from 13910 to 13911, proving no full-device reboot occurred.

## Engineering/debug operations — reference only

The router namespace also contains engineering USB/ADB methods. Normal-admin access is denied for some engineering reads and the write methods were deliberately not executed for coverage. They are not part of an ordinary maintenance workflow.
