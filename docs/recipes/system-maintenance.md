# System maintenance recipes

Detailed references: [`router`](../../api/router.md), [`aoc`](../../api/aoc.md) and [`version`](../../api/version.md).

## Read firmware/runtime identity

Use `version/get_ww_version`, `router/get_device_info`, `router/get_runtime_info` and `router/get_feature_list` as appropriate. See [Device status and diagnostics](device-status-diagnostics.md) for monitoring-oriented reads.

## Reboot the router

`router/router_call_reboot` is live verified and classified `DISRUPTIVE_RECOVERY_REQUIRED`.

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

## Configuration backup

`router/router_backup_config` is a legacy action returning an internal backup path. The current stock UI downloads configuration through the separate `/file.cgi` family.

Configuration backups can contain secrets. Treat the returned binary/backup as sensitive, never commit it to this repository and never include it in diagnostics without explicit sanitization.

## Change UI language

Read `router/get_ui_language`, then POST `router/set_ui_language` with:

```json
{
  "language": "ROUTER_LANGUAGE_CODE"
}
```

Use lowercase router transport codes from the documented semantics. Uppercase abbreviations used for display are not necessarily API values.

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

`router/restart_web_server` is live verified but disruptive to management. Treat it with the same reconnect/re-login/read-back discipline used for other management-path disruptions.

## Engineering/debug operations — reference only

The router namespace also contains engineering USB/ADB methods. Normal-admin access is denied for some engineering reads and the write methods were deliberately not executed for coverage. They are not part of an ordinary maintenance workflow.