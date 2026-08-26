# Client management recipes

Detailed reference: [`statistics`](../../api/statistics.md).

The client API mixes active/inactive inventory with MAC-filter views. Always read the current filter mode before deciding what an `allow` or `forbidden` action means.

## List connected/inactive/filter clients

Use `statistics/get_conn_clients_info`. The frontend can call it with different `request_type` views. Returned client objects can include:

- `mac`
- `ip`
- `name`
- `alias`
- `type` / `client_type`
- current connection time
- `forbidden` or mode-specific allow state

`statistics/get_login_client_mac` can provide the management client's MAC as optional diagnostic metadata, but it should not be the only identity mechanism for USB management.

## Rename a client

POST `statistics/set_alias`:

```json
{
  "mac": "CLIENT_MAC",
  "alias": "Friendly name"
}
```

Then refresh the relevant client view and verify the alias.

## Read MAC-filter mode

GET `statistics/get_black_white_mode`.

Known mode strings are:

- `black` — blacklist/block-list behavior
- `white` — allow-list behavior

## Block/unblock a client in black mode

POST `statistics/set_forbidden`:

```json
{
  "mac": "CLIENT_MAC",
  "alias": "Optional alias",
  "enable": 1
}
```

Use `enable: 0` to remove the forbidden state. Read the forbidden/client view back after the change.

## Allow/remove a client in white mode

POST `statistics/set_allow`:

```json
{
  "mac": "CLIENT_MAC",
  "alias": "Optional alias",
  "enable": 1
}
```

Use `enable: 0` to remove the allow entry.

Do not model `set_allow` as a context-free independent allow-list CRUD operation. Its visible meaning depends on the current MAC-filter mode.

## Switch black/white filter mode

POST `statistics/set_black_white_mode`:

```json
{
  "mode": "white"
}
```

or `black`.

> [!WARNING]
> Switching to white/allow-list mode can lock the management client out of Wi-Fi.

Safe workflow for `black -> white`:

1. establish a separately verified recovery path (for example USB management);
2. identify the Wi-Fi management client MAC;
3. switch to `white`;
4. explicitly `set_allow(enable=1)` for the intended client(s);
5. read the allow view back and require `allow=1`/presence;
6. test an actual Wi-Fi reconnect;
7. on failure, restore `black` over the recovery path.

This complete provisioning/reconnect/restore sequence was live verified.

## Remove an inactive history row

POST `statistics/clear_offline_user`:

```json
{
  "mac": "CLIENT_MAC"
}
```

Read the inactive view again and verify the row was removed.

## Traffic counters

Client inventory and global traffic statistics are separate. See [Traffic and data package](traffic-data-package.md) for `stat_get_common_data`, `stat_clear_common_data` and transport activity.