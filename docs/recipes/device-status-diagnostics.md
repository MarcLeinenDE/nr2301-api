# Device status and diagnostics

This recipe collects the low-impact reads commonly needed for dashboards, monitoring and troubleshooting.

## Device identity and firmware

- `router/get_device_info` — device/platform identifiers and cellular subscriber identifiers.
- `version/get_ww_version` — firmware/software version information.
- `version/get_magicnumber` — platform/version helper value.
- `router/get_feature_list` — capabilities exposed by the runtime.

> [!WARNING]
> `get_device_info` can return IMEI, IMSI, ICCID, MDN and serial-number data. Treat these as sensitive and redact them from logs, bug reports and fixtures.

## Runtime health

- `router/get_runtime_info` — boot time, CPU temperature, CPU use and memory use.
- `router/get_diag_info` — diagnostic health levels.
- `router/get_diag_internet_info` — Internet-availability diagnostic.
- `aoc/get_bat_info` — battery capacity/status and battery temperature.
- `wireless/get_diag_wifi_info` — high-level Wi-Fi diagnostic state.

Do not merge different health concepts into one boolean. For example, WAN link state and Internet availability are separate signals.

## Mobile/WAN status

- `cm/get_cell_info` — network name, roaming, data mode and high-level signal bars.
- `cm/get_current_wan_info` — WAN address, gateway, DNS and separate link/Internet status.
- `cm/get_ca_info` — carrier-aggregation detail; normal admin requires multicall dispatch.
- `cm/query_eng_info` — detailed radio metrics; normal admin requires multicall dispatch.

For `query_eng_info`, preserve missing metrics as unavailable. The known `sinr = -32768` sentinel is endpoint/field-specific and must not be generalized to unrelated integers.

For `get_ca_info`, empty CA arrays do **not** prove that 5G is absent. NSA and SA captures were observed with empty CA arrays.

## Wi-Fi and clients

- `wireless/wifi_get_basic_info` — high-level Wi-Fi switch state.
- `wireless/wifi_get_ap_config` — full AP configuration/status view.
- `wireless/get_extender_status` and `get_extender_config` — extender state.
- `statistics/get_conn_clients_info` — active/inactive/filter-oriented client views.

## Traffic

- `statistics/stat_get_common_data` — current and total byte/duration counters.
- `statistics/stat_get_traffic_transport_status` — RX/TX transport activity.
- `package/get_package_status` — data-package alert/status state.

## Multicall dashboard pattern

For a dashboard, group compatible read methods into `/api.cgi?multicalls=1` rather than issuing many sequential requests. Inspect every member response independently; an outer HTTP 200 does not mean every member succeeded.

Engineering reads `cm/get_ca_info` and `cm/query_eng_info` are especially important: direct normal-admin dispatch is authorization-denied, while a one-member multicall is sufficient on the tested firmware.

## Methods intentionally not treated as diagnostics

Engineering/debug write methods such as band setters, ADB/USB-mode setters or engineering-mode setters are not required to obtain ordinary status data and remain reference-only where the catalog marks them `DO_NOT_TEST_FOR_COVERAGE`.