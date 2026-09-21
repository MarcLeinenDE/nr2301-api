# Administrator password setter source contract — 2026-09-21

Target: Zyxel NR2301 WebUI, tested firmware family `V1.00(ACIY.3)C0`.

A read-only capture of `html/set_admin.html` reconstructed the administrator
settings form and `account/set_info` payload.

The password-change path builds:

```javascript
var postData = {
  type: 'admin',
  session_id: GetCookie("CGISID")
}
postData.password = password
ajaxHandler('account', 'set_info', postData)
```

Canonical password-change body:

```json
{
  "type": "admin",
  "session_id": "<current CGISID>",
  "password": "<new password>"
}
```

Important details:

- transport is the already documented POST `direct_ajaxHandler` variant;
- the current session cookie value is copied into the JSON `session_id` field;
- no old-password field is sent;
- `password_confirm` is only compared in the browser and is never transmitted;
- the same setter uses `total_time` instead of `password` for login-timeout changes;
- frontend success condition is `result === 0`;
- frontend maps `result === -1001` to the default-password-equality warning;
- general-build validation requires at least 5 characters, a maximum input length
  of 32, supported ASCII characters, and rejects all-space passwords.

No password change was performed while collecting this source evidence. No real
password value is included in this public evidence.
