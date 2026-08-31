# Authentication

## Normal administrator flow

The stock NR2301 web UI uses an application-level challenge flow for the normal administrator account.

## Canonical management host on tested firmware

Administrator pre-auth is **host/authority sensitive** on tested firmware `V1.00(ACIY.3)C0`.

During a controlled physical USB A/B test on 2026-08-31, `zyxel.home` resolved to the same management address as `192.168.1.1`, but the pre-auth account methods behaved differently:

```text
http://192.168.1.1
  account/get_retrytimes_and_time -> result=4
  account/get_rand                -> result=4

http://zyxel.home
  account/get_retrytimes_and_time -> result=0, retry_times=5, remain_time=0
  account/get_rand                -> result=0, rand=<8-byte challenge>
```

The same result was reproduced with normal `requests` JSON POSTs, compact historical request bodies/headers and `urllib`. Loading the WebUI first did not create a prerequisite cookie, and explicit WebUI logout did not change the direct-IP failure. This establishes that anonymous/status reads succeeding on `192.168.1.1` do **not** prove that the direct IP is suitable for administrator login.

For this firmware, use the canonical management URL:

```text
http://zyxel.home
```

The current evidence establishes host/authority-dependent behavior. It does not justify assigning a universal semantic meaning to `result=4` on these pre-auth endpoints.

### 0. Check the administrator lockout state

Before requesting a challenge, a defensive client should POST `account/get_retrytimes_and_time`:

```json
{
  "type": "admin"
}
```

Known successful response fields include `remain_time`, `retry_times` and `result`.

The earlier live-working NR2301 application used this call as a lockout guard:

- if `remain_time > 0`, wait instead of attempting a login;
- if `retry_times <= 1`, abort rather than consume the final password attempt.

This guard does not authenticate the client and does not send the administrator password.

### 1. Request a login random value

`account/get_rand` is part of the live-verified normal administrator login flow.

```json
{
  "type": "admin",
  "user_id": "a1b2c3d4"
}
```

Historical live-working clients generated `user_id` as **exactly eight lowercase alphanumeric characters** (`[a-z0-9]{8}`) and reused the same value in the subsequent `account/login` request.

The initial public SDK temporarily used a 32-character hexadecimal `user_id`, but a controlled retest showed that user-id length was not the cause of the observed `result=4`: both that format and the corrected historical `[a-z0-9]{8}` format failed through the direct IP, while the historical eight-character format succeeded immediately through `zyxel.home`.

Known successful response fields:

```json
{
  "rand": "<router-random-value>",
  "result": 0
}
```

On the direct-IP path, `account/get_rand` reproducibly returned `result=4` before password submission. Do **not** apply the `account/login` result-code table below to that value; result semantics are endpoint-specific unless separately verified.

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

Values 1, 2 and 3 were observed live during the original research. The full mapping is derived from the shipped frontend logic.

## Session failure handling

A robust client should treat session/authentication failures separately from ordinary API errors, reacquire a session only once for a failed operation, and then retry that operation once. Avoid unbounded re-login loops.

## Other authentication surfaces

The tested runtime also exposes a Digest challenge at `/login.cgi`. Earlier live work also showed host canonicalization toward `zyxel.home` on that surface, which is consistent with the later `/api.cgi` administrator pre-auth A/B result. Existence of the Digest challenge is still **not** evidence that it participates in the normal web UI `CGISID` session flow.

Engineering/supervisor credentials are intentionally not documented here. The API catalog may still contain engineering methods when their behavior or authorization boundary is relevant.
