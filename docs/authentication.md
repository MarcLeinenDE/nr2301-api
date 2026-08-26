# Authentication

## Normal administrator flow

The stock NR2301 web UI uses an application-level challenge flow for the normal administrator account.

### 1. Request a login random value

`account/get_rand` is available before an authenticated session exists.

```json
{
  "type": "admin",
  "user_id": "<random-client-value>"
}
```

Known response fields:

```json
{
  "rand": "<router-random-value>",
  "result": 0
}
```

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
  "user_id": "<same-random-client-value>"
}
```

A successful normal administrator login was observed with `result = 3` and establishes the `CGISID` session cookie.

### 4. Authenticated requests

Preserve and send the `CGISID` cookie. Some account requests also carry the session identifier in a JSON `session_id` field.

## Observed login result values

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
