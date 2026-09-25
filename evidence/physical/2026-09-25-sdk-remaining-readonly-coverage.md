# Public-SDK remaining read-only coverage — 2026-09-25

Device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

## Scope

This run closed seven previously missing public-SDK physical read-only coverage
paths identified by the canonical API↔SDK audit.

The test used:

`tests/integration/test_remaining_readonly_coverage.py`

with a normal authenticated administrator session.

## Physical result

```text
READONLY_ROUTER_MAC_INFO fields_present=6 sensitive_values_logged=False
READONLY_LOGIN_CLIENT_MAC mac_present=True sensitive_value_logged=False
READONLY_MAGIC_NUMBER magic_present=True raw_value_logged=False
READONLY_WIFI_DIAGNOSTICS mode_present=True sensitive_values_logged=False
READONLY_WIFI_EXTENDER_CONFIG enable_present=True ssid_present=True key_present=True credential_values_logged=False
READONLY_WIFI_TIMED_OFF_STATUS status_present=True semantic_value_logged=False
READONLY_SMS_QUERY semantic_success=False resp=-2 ids_logged=False
```

Pytest result:

```text
7 passed in 0.86s
```

## Closed physical SDK gaps

- `router/get_mac_info`
- `statistics/get_login_client_mac`
- `version/get_magicnumber`
- `wireless/get_diag_wifi_info`
- `wireless/get_extender_config`
- `wireless/wifi_get_timed_off_status`
- `sms/sms.query`

## Privacy handling

The physical test deliberately did not print:

- concrete MAC addresses;
- SSIDs;
- extender keys;
- version magic values;
- SMS IDs.

Only type/presence metadata and the SMS endpoint's non-sensitive semantic
`resp` code were logged.

## SMS query semantics

The existing SDK helper treats only `sms.query resp=0` as semantic success.
The physical run returned `resp=-2`, matching prior API evidence. The test
therefore passed by confirming that the SDK raises its endpoint-specific
`APIError` for this non-success response while preserving the documented raw
method semantics.

This does not change the API contract.

No private device identifiers, credentials, message contents, phone numbers,
Wi-Fi credentials or session tokens are published here.
