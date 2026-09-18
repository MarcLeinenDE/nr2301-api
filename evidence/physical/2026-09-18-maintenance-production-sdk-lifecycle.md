# Maintenance production SDK lifecycle — 2026-09-18

Physical device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

A production-SDK maintenance lifecycle was exercised against the dedicated
non-production router.

## Legacy backup action

`router/router_backup_config` completed successfully through the body-less GET
transport and returned the documented success condition `rc=0`.

The legacy action itself does not represent the current stock-UI configuration
download path; the stock UI uses the separate `/file.cgi` family.

## Web-server restart

`router/restart_web_server` was invoked through the body-less GET transport.

Observed result:

```text
boot_before=13910
boot_after=13911
outage_observed=False
action_error=ProtocolError
```

The `ProtocolError` matches the already known ACIY.3 behavior where the action
returns HTTP 200 with an empty/non-JSON response body. Management remained
recoverable and router uptime continued monotonically, proving that this action
did **not** perform a full router reboot.

## Full router reboot

`router/router_call_reboot` was invoked through the body-less GET frontend
variant.

Observed result:

```text
boot_before=13911
boot_after=51
outage_observed=True
action_error=TransportError
```

The management outage plus the `boot_time` reset proves a real full-device
reboot. The router recovered and administrator access succeeded afterward.

This physically reconfirms the GET/no-body reboot transport on ACIY.3. The
alternate frontend POST variant remains historical/source evidence and was not
needed for the production SDK.

Final physical result: 3 tests passed.

No USB management-mode mutation was performed.
