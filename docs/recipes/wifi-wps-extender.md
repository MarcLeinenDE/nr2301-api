# Wi-Fi, WPS and extender recipes

Detailed reference: [`wireless`](../../api/wireless.md). Some extender write state is also exposed through [`cm`](../../api/cm.md).

## Read the current Wi-Fi configuration

Use `wireless/wifi_get_ap_config`. It returns the current mode plus 2.4 GHz, 5 GHz, Dual and Guest configuration blocks, timed-off configuration and common settings.

Because Wi-Fi writes can disconnect the management client, always save the current object before changing it.

## Change SSID, password, channel, security or Guest Wi-Fi

Use `wireless/wifi_set_ap_config`.

The setter accepts different top-level blocks depending on the part being changed:

- `mode`
- `wifi_if_24G`
- `wifi_if_5G`
- `wifi_if_DUAL`
- `wifi_if_GUEST`
- `wifi_timed_off`

Recommended pattern:

1. GET `wifi_get_ap_config`;
2. copy the current relevant block;
3. change only the intended fields (for example `ssid`, `key`, `channel`, `hidden`, `encryption` or Guest `maxassoc`);
4. POST the corresponding block(s) through `wifi_set_ap_config`;
5. expect the management connection to disappear temporarily;
6. reconnect/re-authenticate;
7. GET `wifi_get_ap_config` and verify the desired fields.

Do not rebuild an entire AP block from guessed defaults. Preserve fields returned by the router that you do not intend to change.

## Wi-Fi mode / split vs Dual

The same `wifi_set_ap_config` method controls the frontend's Wi-Fi mode. Live tests verified transitions between Dual and separate 2.4/5 GHz configurations with recovery/read-back and exact restoration.

Treat mode changes as disruptive even if the HTTP request itself appears successful.

## Guest Wi-Fi

Read Guest fields under `wifi_if_GUEST`, then write the Guest block through `wifi_set_ap_config`. Live verification covered Guest on/off and `maxassoc` changes.

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