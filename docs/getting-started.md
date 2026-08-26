# Getting started

## Base URL

The examples assume the router management interface is reachable at a base URL such as `http://192.168.1.1`. Use the address configured on your own device.

## Minimal flow

1. Create a random `user_id` value.
2. Call `account/get_rand` with `type=admin` and that `user_id`.
3. Calculate `MD5(rand + plaintext_password)` as the login challenge response.
4. Call `account/login` with `type=admin`, the administrator username, the MD5 challenge response and the same `user_id`.
5. Preserve the returned `CGISID` cookie for authenticated requests.
6. Call API methods through `/api.cgi`.
7. Log out with `account/logout` when appropriate.

See [Authentication](authentication.md) for the exact observed flow and caveats.

## Single-call example

```text
GET /api.cgi?path=cm&method=get_cell_info&timeout=10
Cookie: CGISID=<session>
```

A method requiring a JSON body is normally sent as a `POST`:

```text
POST /api.cgi?path=account&method=get_info&timeout=10
Content-Type: application/json
Cookie: CGISID=<session>

{"type":"admin","session_id":"<session>"}
```

Check the individual namespace page or `specification/methods.json` for each method's known request form.

## Compatibility rule

The documentation currently describes behavior observed on `V1.00(ACIY.3)C0`. Treat firmware compatibility as empirical until another version has been tested.
