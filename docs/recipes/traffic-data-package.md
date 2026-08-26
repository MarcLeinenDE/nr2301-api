# Traffic counters and data-package recipes

Detailed references: [`statistics`](../../api/statistics.md) and [`package`](../../api/package.md).

The NR2301 has two related but separate concepts:

- raw/current/total traffic counters in `statistics`;
- a configurable data-package/allowance tracker in `package`.

Do not merge them into one data model.

## Read traffic counters

GET `statistics/stat_get_common_data`.

Returned fields include current and total RX/TX byte counters, combined counters, duration and error-byte counters.

Use `statistics/stat_get_traffic_transport_status` for the current RX/TX activity/status flags.

## Clear traffic/history counters

GET `statistics/stat_clear_common_data`.

> [!WARNING]
> This is an intentional destructive statistics action. It clears traffic/history counters.

If your application exposes this action, require an explicit user confirmation and refresh the counters afterward.

## Read data-package settings

GET `package/get_package_settings`.

The response can include package types for daily, monthly, three-month, half-year, one-year and unlimited-style tracking, together with threshold and usage fields.

## Read data-package status

GET `package/get_package_status`.

Known status values:

| Value | Meaning |
|---:|---|
| 0 | normal/no alert |
| 1 | warning threshold |
| 2 | limit exceeded |
| 3 | expired |

## Set current data-used value

POST `package/set_package_data_used` with:

```json
{
  "data_used": "NEW_OR_CURRENT_VALUE"
}
```

The same-state write is live verified. Read `get_package_settings` back afterward.

## Change package settings

Use `package/set_package_settings`, but apply a conservative read-copy-write pattern because the current public method page does not normalize a single complete request schema for every period type.

Recommended client behavior:

1. GET `get_package_settings`;
2. keep the current package type and all period-specific fields;
3. change only the intended package/threshold fields;
4. POST the frontend-shaped object;
5. GET settings and status again.

The `package_type=unlimited` frontend/runtime behavior still carries a numeric package-data value. Do not label it as proof of truly unlimited carrier data or assume enforcement behavior that was not tested.

## Client inventory vs traffic

Per-client inventory/allow-block state lives in `statistics/get_conn_clients_info` and related methods. The documented traffic counters here are global/router statistics, not a proven per-client byte-accounting API.