# Wi-Fi, WPS and extender recipes

Detailed reference: [`wireless`](../../api/wireless.md). Some extender write state is also exposed through [`cm`](../../api/cm.md).

## Read the current Wi-Fi configuration

Use `wireless/wifi_get_ap_config`. It returns the current mode plus 2.4 GHz, 5 GHz, Dual and Guest configuration blocks, timed-off configuration and common settings.

Because Wi-Fi writes can disconnect the management client, always save the current object before changing it.

## Change SSID, password, channel or security

Use `wireless/wifi_set_ap_config`.

Recommended pattern:

1. GET `wifi_get_ap_config`;
2. copy the current relevant block;
3. change only the intended fields, for example `ssid`, `key`, `channel`, `hidden` or `encryption`;
4. POST the corresponding preserved block through `wifi_set_ap_config`;
5. expect the management connection to disappear temporarily;
6. reconnect/re-authenticate;
7. GET `wifi_get_ap_config` and verify the desired fields.

Do not rebuild an AP block from guessed defaults. Preserve fields returned by the router that you do not intend to change.

## Combined vs separate main SSIDs

The tested firmware uses these exact top-level `mode` tokens:

```text
DUAL             = combined main 2.4/5 GHz SSID, Guest off
DUAL GUEST       = combined main 2.4/5 GHz SSID, Guest on
2.4G 5G          = separate main 2.4 GHz and 5 GHz settings, Guest off
2.4G 5G GUEST    = separate main 2.4 GHz and 5 GHz settings, Guest on
```

Do not describe `DUAL` as Band Steering unless that behavior is separately proven. A safe user-facing description is **combined/shared SSID for 2.4 and 5 GHz** versus **separate 2.4 and 5 GHz settings**.

For a mode transition:

1. GET `wifi_get_ap_config`;
2. detect whether `GUEST` is currently present in `config.mode`;
3. choose `DUAL` or `2.4G 5G` and preserve the current Guest token;
4. copy the currently returned `wifi_if_DUAL`, `wifi_if_24G`, `wifi_if_5G` and `wifi_if_GUEST` blocks into the write payload when present;
5. change only `mode`;
6. POST `wifi_set_ap_config`;
7. recover/re-authenticate after the expected Wi-Fi reset;
8. require exact `config.mode` read-back.

The following full chain was live verified with recovery and final restore:

```text
DUAL
-> DUAL GUEST
-> 2.4G 5G GUEST
-> DUAL GUEST
-> DUAL
```

Main/Guest SSIDs and keys were preserved internally, the Guest configuration remained intact, and the original observable state was restored.

## Guest Wi-Fi on/off

There is **no dedicated Guest-enable field**. Guest is enabled by the `GUEST` token in top-level `config.mode`.

Examples:

```text
DUAL        -> Guest off
DUAL GUEST  -> Guest on

2.4G 5G        -> Guest off
2.4G 5G GUEST  -> Guest on
```

Safe enable/disable pattern:

1. read the current configuration;
2. preserve whether the main network is `DUAL` or `2.4G 5G`;
3. add or remove only the `GUEST` token;
4. send the resulting `mode` together with the complete current `wifi_if_GUEST` block;
5. recover/re-authenticate;
6. require exact mode read-back.

The Guest block is frontend-evidenced with:

- `band_mode`
- `ssid`
- `encryption`
- `key`
- `hidden`
- `isolate`
- `maxassoc`

Guest enable and disable were live verified with reset/read-back/exact restore.

### Guest maximum clients

`wifi_if_GUEST.maxassoc` was live changed `10 -> 9 -> 10`, read back after each write and restored. The frontend-supported normal range is `1..10`.

### Guest isolation caveat

On firmware `V1.00(ACIY.3)C0`, `wifi_get_ap_config` does not return an independent `wifi_if_GUEST.isolate` value. The stock frontend nevertheless sources the Guest write field from the main 5 GHz isolation control.

Therefore do **not** expose a separate Guest-isolation setting and do not infer its actual state from the main 5 GHz value. It is not safely round-trippable on this build.

## Timed Wi-Fi off

- read configured timer data from `wifi_get_ap_config`;
- read current timer status with `wifi_get_timed_off_status`;
- update the `wifi_timed_off` block through `wifi_set_ap_config`.

## Read/enable/disable WPS

Read `wireless/wifi_get_wps_disable`, then POST `wireless/wifi_set_wps_disable` with the `wps_enable` field.

The live runtime accepted the value as a string such as:

```json
{
  "wps_enable": "1"
}
```

This setter can take long enough to require reconnect/recovery handling.

## Start/cancel WPS PBC

- start: `wireless/wifi_call_wps_pbc` (GET)
- status: `wireless/wps_status`
- cancel: `wireless/wifi_call_wps_cancel` (GET)

The status enum includes `Disabled`, `Active`, `Timed-out`, `Overlap` and `Unknown`.

## WPS PIN

POST `wireless/wifi_call_wps_pin` with:

```json
{
  "wps_enable": "1",
  "wps_pin": "WPS_PIN"
}
```

Then monitor `wps_status` and cancel when appropriate.

## Scan nearby Wi-Fi networks

Call `wireless/wifi_scan`. The scan is live verified and returns the frontend scan list, but the response schema is not yet normalized as a stable public contract.

## Wi-Fi extender

- `wireless/get_extender_config` — current extender enable/SSID/key.
- `wireless/get_extender_status` — current extender status enum.
- `cm/get_wan_settings` also exposes extender credentials/state.

`cm/set_wan_settings` is live verified only as a same-state WAN/extender write and its full request body is not reconstructed in the public contract. Do not invent an extender write payload yet.
