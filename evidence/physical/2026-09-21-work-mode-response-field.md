# Work-mode response field — physical read — 2026-09-21

Device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

A read-only production-SDK probe called `router/router_get_work_mode` under a
normal administrator session. No configuration write was performed.

Observed complete response:

```json
{"work_mode":"router"}
```

This corrects an earlier source-derived assumption that the response field was
named `mode`. On the tested ACIY.3 runtime the canonical field name is
`work_mode`.

Known values remain `router` and `bridge`.

No USB-management-mode mutation or other configuration mutation occurred.
