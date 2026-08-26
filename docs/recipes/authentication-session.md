# Authentication and session recipe

Use this recipe for the normal administrator session used by the stock NR2301 web UI.

Detailed reference: [`account` namespace](../../api/account.md) and [Authentication](../authentication.md).

## Login flow

### 1. Check retry/lock state when useful

`account/get_retrytimes_and_time` is available before login and can be used to avoid blindly retrying a locked account.

### 2. Get a challenge

POST `account/get_rand`:

```json
{
  "type": "admin",
  "user_id": "RANDOM_CLIENT_VALUE"
}
```

Read `rand` from the response.

### 3. Build the password response

The stock frontend computes:

```text
MD5(rand + plaintext_password)
```

Use the hexadecimal MD5 digest as the `password` field. This is an application-level challenge mechanism; it does not turn plain HTTP into an encrypted transport.

### 4. Login

POST `account/login`:

```json
{
  "type": "admin",
  "username": "ADMIN_USERNAME",
  "password": "MD5_CHALLENGE_RESPONSE",
  "user_id": "RANDOM_CLIENT_VALUE"
}
```

A successful normal-admin login was observed with `result = 3`. Preserve the returned `CGISID` cookie.

## Authenticated calls

Send `CGISID` on subsequent API requests. Some account methods also use a JSON `session_id` field; follow the per-method contract instead of adding it globally.

## Session recovery

A robust client should:

1. detect an authentication/session error separately from an ordinary API error;
2. perform one fresh login;
3. retry the original operation once;
4. stop if that retry also fails.

Do not build an unbounded automatic login loop.

## Read/update account information

- `account/get_info` reads normal account/session information.
- `account/set_info` is live verified, but its full payload is not yet reconstructed in the public reference. Do not invent fields; preserve the exact frontend/current contract if you use it.

## Logout

Call `account/logout`, then discard the local `CGISID` cookie/session state.

## Related methods

This recipe covers all six `account` methods: `get_info`, `get_rand`, `get_retrytimes_and_time`, `login`, `logout`, and `set_info`.