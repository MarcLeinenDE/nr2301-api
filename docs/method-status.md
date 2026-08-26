# Method verification status

The public catalog separates **what was found** from **what was exercised on hardware**.

| Status | Meaning |
|---|---|
| `LIVE_VERIFIED` | Successfully exercised on the tested NR2301 runtime. Some actions have side effects; check the safety class and notes. |
| `LIVE_VERIFIED_LIMITED` | Live evidence exists, but only for a limited transport/context or with an incomplete behavioral result. |
| `LIVE_DENIED` | The method was reached live but normal administrator authorization was denied. |
| `LIVE_REJECTED` | The backend was reached live and rejected the tested request. |
| `LIVE_NOT_APPLICABLE` | The method exists but the tested runtime/state did not provide an applicable live case. |
| `STATIC_CONFIRMED` | Referenced by the shipped frontend/firmware, but not intentionally live-executed in this research set. |
| `NOT_IMPLEMENTED` | Referenced statically, but the tested backend returned method-not-found. |
| `UNTESTED` | No sufficient static or live evidence has been normalized yet. |

## Raw observed status

`specification/methods.json` also contains `observed_status`. This retains useful research distinctions such as a verified action that required recovery/read-back or a method that was only available through multicall. The generated human-readable namespace pages intentionally show the normalized `verification` state instead of exposing these internal research labels inline.

## Authorization evidence

The per-method `auth_evidence` field describes how well the **privilege boundary** was characterized; it is separate from the live-execution status. A method can therefore have successful live behavior while its privilege boundary remains `UNTESTED` or `UNKNOWN`.

| Value | Meaning |
|---|---|
| `ADMIN_OK` | Normal administrator access was explicitly confirmed. |
| `ADMIN_DENIED` | Normal administrator access reached the method but was denied. |
| `PREAUTH_ALLOWED` | Callable before an authenticated session. |
| `PREAUTH_AUTHENTICATOR` | Part of the login/authenticator flow. |
| `ADMIN_MULTICALL_ONLY` | Normal-admin evidence exists only through multicall in the current research. |
| `ADMIN_METHOD_NOT_FOUND` | Normal-admin live call reached a method-not-found result. |
| `ADMIN_OK_EMPTY_RESPONSE` | Normal-admin request was accepted but returned an empty response body. |
| `UNTESTED` / `UNKNOWN` | The privilege boundary was not independently characterized; do not interpret this as anonymous access. |

## Safety classes

| Safety class | Interpretation |
|---|---|
| `READ_OR_LOW_SIDE_EFFECT` | Read or low-impact helper. Still inspect individual notes. |
| `WRITE_OR_SIDE_EFFECT` | Changes state or performs an externally visible action. |
| `DISRUPTIVE_RECOVERY_REQUIRED` | May break the current management connection, reboot, change addressing or otherwise require recovery. |
| `DO_NOT_TEST_FOR_COVERAGE` | Deliberately not exercised merely to improve coverage because risk/impact outweighs documentation value. |

A verification state is **not** a safety rating. A live-verified factory reset remains destructive.
