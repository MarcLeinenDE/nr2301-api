# Authentication

## Normal administrator flow

The stock NR2301 web UI uses an application-level challenge flow for the normal administrator account.

### 0. Check the administrator lockout state

Before requesting a challenge, a defensive client should POST `account/get_retrytimes_and_time`:

```json
{
  "type": "admin"
}
```

Known response fields include `remain_time`, `retry_times` and `result`.

The earlier live-working NR2301 application used this call as a lockout guard:

- if `remain_time > 0`, wait instead of attempting a login;
- if `retry_times <= 1`, abort rather than consume the final password attempt.

This guard does not authenticate the client and does not send the administrator password.

### 1. Request a login random value

`account/get_rand` is available before an authenticated session exists.

```json
{
  "type": "admin",
  "user_id": "a1b2c3d4"
}
```

The known live-working client format for `user_id` is **exactly eight lowercase alphanumeric characters** (`[a-z0-9]{8}`). The same value is reused in the subsequent `account/login` request.

During the first public-SDK physical USB smoke test on 2026-08-31, an SDK-generated 32-character hexadecimal `user_id` reproducibly received `result = 4` from `account/get_rand` before any password challenge was submitted. The historical live-working application used the eight-character format above. Until additional firmware evidence proves broader acceptance, clients should use the eight-character form for compatibility.

Known response fields:

```json
{
  "rand": "<router-random-value>",
  "result": 0
}
```

`result = 0` is the observed successful `get_rand` outcome. Do **not** automatically apply the `account/login` result-code table below to `account/get_rand`; those result semantics are endpoint-specific unless separately verified.

### 2. Build the challenge response

The observed frontend computes:

```text
MD5(rand + plaintext_password)
```

The hexadecimal MD5 result is sent in the `password` field. The plaintext password is not sent in this application-level request body.

### 3. Login

```json
{
  "type": "admin",
  "username": "<admin-username>",
  "password": "<md5-challenge-response>",
  "user_id": "<same-8-character-client-value>"
}
```

A successful normal administrator login was observed with `result = 3` and establishes the `CGISID` session cookie.

### 4. Authenticated requests

Preserve and send the `CGISID` cookie. Some account requests also carry the session identifier in a JSON `session_id` field.

## Observed `account/login` result values

The following table applies to the **`account/login` response**. Do not transfer these meanings to unrelated `result` fields without endpoint-specific evidence.

| Value | Meaning |
|---:|---|
| 0 | Username or password error |
| 1 | Password error |
| 2 | Username error |
| 3 | Success |
| 4 | Login timeout; retry |
| 5 | Hacking detected |
| 6 | Account locked |

Values 1, 2 and 3 were observed live during the research. The full mapping is derived from the shipped frontend logic.

## Session failure handling

A robust client should treat session/authentication failures separately from ordinary API errors, reacquire a session only once for a failed operation, and then retry that operation once. Avoid unbounded re-login loops.

## Other authentication surfaces

The tested runtime also exposes a Digest challenge at `/login.cgi`, but existence of that challenge is **not** evidence that it participates in the web UI's normal `CGISID` session flow. The documented client flow in this repository is the `/api.cgi` administrator flow above.

Engineering/supervisor credentials are intentionally not documented here. The API catalog may still contain engineering methods when their behavior or authorization boundary is relevant.
