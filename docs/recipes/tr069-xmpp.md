# TR-069 and XMPP recipes

Detailed reference: [`tr069`](../../api/tr069.md).

TR-069 settings can expose ACS credentials and change remote-management behavior. Treat both reads and writes as sensitive administration operations.

## Read TR-069 configuration

GET `tr069/get_config`.

The response can include:

- ACS URL, username and password
- connection-request username/password/auth type
- periodic-inform enable/interval
- platform-specific notification fields

> [!WARNING]
> Redact ACS and request credentials from logs, bug reports and fixtures.

## Change TR-069 configuration

POST `tr069/set_config`.

A same-state write was live verified with the exact WW_OPERATOR_ZYXEL frontend payload. A previous request containing non-platform fields was rejected with `result=-1001`.

Recommended pattern:

1. GET `get_config`;
2. construct the write using only fields supported by the tested platform/frontend;
3. preserve secrets and untouched values exactly;
4. POST `set_config`;
5. GET the config again and verify non-secret and intended fields.

Do not assume every field returned by a getter is accepted by the platform's setter.

## Read XMPP configuration

GET `tr069/get_xmpp_config`.

It can expose username/password, domain/resource, server list, TLS/use settings, retry timers and allowed JID information. Treat these as sensitive.

## Set XMPP configuration — rejected on tested runtime

`tr069/set_xmpp_config` is referenced by the frontend and its request keys are reconstructed, but the tested full same-state request returned `result=-1001`.

Therefore this recipe does not present XMPP writing as a working supported operation. A client should keep it disabled/experimental until firmware-specific evidence shows a successful contract.