# Multicall

The web UI uses a batch endpoint:

```text
POST /api.cgi?multicalls=1
Content-Type: application/json
Cookie: CGISID=<session>
```

Observed outer body shape:

```json
{
  "requests": [
    {
      "path": "cm",
      "method": "get_cell_info",
      "data": {},
      "timeout": 2
    }
  ]
}
```

`data` and the per-item `timeout` are optional depending on the member call.

Some methods were only successfully exercised by the normal administrator through multicall. The method catalog marks those as `LIVE_VERIFIED_LIMITED` and preserves the observed raw status `VERIFIED_ADMIN_MULTICALL_ONLY`.

## Error handling

Do not infer success from the outer HTTP 200 alone. Inspect each member result individually. A batch may contain a mixture of successful and failed method results.
