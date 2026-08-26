# VPN client recipes

The NR2301 exposes a built-in VPN-client profile API in the `cm` namespace.

Detailed reference: [`cm`](../../api/cm.md).

## Read VPN state

- `cm/get_vpn_clients` — global enable state, active profile index and configured profiles.
- `cm/get_vpn_client_connect_status` — current VPN connection status.

> [!WARNING]
> `get_vpn_clients` may return profile passwords and L2TP/IPsec PSKs. Redact them from logs, traces and issue reports.

## Enable or disable the VPN client subsystem

POST `cm/open_close_vpn_clients`:

```json
{
  "vpn_client_enable": "enable"
}
```

or:

```json
{
  "vpn_client_enable": "disable"
}
```

Read `get_vpn_clients` back and verify `vpn_client_enable`.

## Add a profile

POST `cm/add_vpn_client_item`:

```json
{
  "index": "-1",
  "vpn_name": "Example profile",
  "protocol_type": "l2tp/ipsec",
  "vpn_server": "vpn.example.invalid",
  "vpn_user_name": "USERNAME",
  "vpn_user_password": "PASSWORD",
  "vpn_secure": "PSK"
}
```

Supported protocol strings reconstructed from the frontend are:

- `pptp`
- `l2tp`
- `l2tp/ipsec`

`vpn_secure` is protocol-dependent. Never log secret fields.

After adding, call `get_vpn_clients` and locate the new profile/index.

## Edit a profile

POST `cm/edit_vpn_client_item` with the existing `index` and the full profile fields:

```json
{
  "index": "EXISTING_INDEX",
  "vpn_name": "Example profile",
  "protocol_type": "l2tp",
  "vpn_server": "vpn.example.invalid",
  "vpn_user_name": "USERNAME",
  "vpn_user_password": "PASSWORD",
  "vpn_secure": ""
}
```

Read the profile list back after editing.

## Mark a profile active/inactive

POST `cm/active_vpn_client_item`:

```json
{
  "index": "EXISTING_INDEX",
  "vpn_active": "active"
}
```

or use `inactive`.

## Delete a profile

POST `cm/del_vpn_client_item`:

```json
{
  "index": "EXISTING_INDEX"
}
```

Read `get_vpn_clients` back and verify that the profile is gone.

## Connection behavior

The profile CRUD/global-enable paths were live verified with temporary profiles and exact cleanup. Those tests intentionally did **not** establish a real external VPN tunnel. Treat actual tunnel connectivity as dependent on the configured protocol/server and verify it using `get_vpn_client_connect_status` plus an external connectivity test.

Do not confuse `cm/connect` / `cm/disconnect` with the VPN profile API; those methods belong to mobile WAN connection control.