# Mobile network recipes

Detailed references: [`cm`](../../api/cm.md) and [`util_wan`](../../api/util_wan.md).

## Read current mobile settings

Call `cm/get_network_settings`. Important fields include:

- `network_settings.network_mode`
- `network_settings.data_roaming`
- `network_settings.connect_mode`
- `network_settings.profile_mode`
- `network_settings.profile.active_index`
- APN/profile fields under `network_settings.profile.data[]`

Call `cm/get_available_network_mode` before presenting selectable network modes. Do not hard-code a mode that the current firmware does not report as available.

## Change LTE/5G network mode

POST `cm/set_network_settings` with only the field being changed:

```json
{
  "network_mode": "MODE_RETURNED_BY_GET_AVAILABLE_NETWORK_MODE"
}
```

Then read `cm/get_network_settings` back and verify the resulting `network_mode`.

The setter is live verified. The public reference deliberately does not invent a universal list of mode strings; use the runtime's available-mode response and the documented semantics.

## Enable or disable data roaming

POST `cm/set_network_settings`:

```json
{
  "data_roaming": "1"
}
```

or:

```json
{
  "data_roaming": "0"
}
```

Read `cm/get_network_settings` back after the write.

## Reconnect mobile data

The observed sequence is:

1. call `cm/disconnect`;
2. wait briefly for the state change;
3. call `cm/connect`;
4. recover/re-authenticate if management connectivity is interrupted;
5. verify with `cm/get_current_wan_info` and/or `cm/get_cell_info`.

Both actions are classified `DISRUPTIVE_RECOVERY_REQUIRED`. A timeout or dropped management request is not by itself proof of failure.

## Read current WAN addressing

Use `cm/get_current_wan_info` for IPv4/IPv6 address, gateway and DNS values. Parse `connection_status` and `internet_status` numerically and keep them as separate concepts.

## APN/profile information

`cm/get_network_settings` exposes the active profile and profile list, including APN, authentication, IP type, username and password fields.

The current public contract does **not** document a fully reconstructed APN/profile write operation through `set_network_settings`. Do not infer one merely from the getter.

## Scan mobile operators

Call `util_wan/search_network`. Operator scans can take much longer than ordinary API reads, so clients should use a longer timeout.

## Read automatic/manual selection state

Call `util_wan/get_network_select_mode` and inspect `nw_sel_mode`.

## Select operator / return to automatic selection

POST `util_wan/select_network` with:

```json
{
  "network_param": "auto"
}
```

The same field carries the selected network parameter for manual selection as supplied by the scan/frontend contract. Do not construct a manual operator identifier from guesswork; use the scan result representation.

This operation can interrupt mobile and management connectivity. Reconnect and read the selection/WAN state back.

## Detailed radio metrics

`cm/query_eng_info` and `cm/get_ca_info` are useful for LTE/5G diagnostics, but normal-admin access on the tested firmware works through `/api.cgi?multicalls=1`, not direct path/method dispatch.

`cm/eng_get_bands`, `cm/eng_set_bands` and `cm/set_eng_mode` are engineering surfaces. The normal admin is denied for the engineering band read, and the write methods are intentionally not promoted to a practical recipe.