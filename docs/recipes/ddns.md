# Dynamic DNS recipe

Detailed reference: [`ddns`](../../api/ddns.md).

## Read current DDNS state

GET `ddns/get_ddns`.

The response can contain:

- `enabled`
- `service_name`
- `domain`
- `username`
- `password`
- `ddns_ipaddr`
- `ddns_state`

Known `ddns_state` values include idle/updating/OK/blocked states as documented on the method page.

> [!WARNING]
> The getter can expose credentials. Redact them from logs and diagnostics.

## Configure DDNS

POST `ddns/set_ddns`. Known top-level fields are:

```text
enabled
service_name
domain
username
password
token
```

After writing, GET `get_ddns` again and verify the non-secret state/domain/provider fields plus `ddns_state` as appropriate.

## Token-based providers

The getter does not return a token even though the setter accepts one. That means an existing token-based profile cannot be assumed to be exactly round-trippable.

Safe rule:

- do not implement a generic "read profile, rewrite everything" operation for token-based DDNS;
- only send a token when the user explicitly supplies it;
- never replace an existing token-based configuration merely to perform a same-state test;
- never log password/token values.

Custom-provider writes therefore remain more constrained than the ordinary getter/setter existence might suggest.