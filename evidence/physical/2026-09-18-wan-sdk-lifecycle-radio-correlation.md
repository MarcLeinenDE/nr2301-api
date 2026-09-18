# Mobile WAN production SDK lifecycle and radio correlation — 2026-09-18

Physical device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

A disruptive production-SDK WAN-control lifecycle was re-run after teaching the
SDK that `connection_status=2` is a valid non-final transition state.

Observed sanitized trace:

```text
initial           connection_status=1 internet_status=1 data_mode=22 RATs=4g,nr
after-disconnect  connection_status=1 internet_status=1 data_mode=22 RATs=4g,nr
after-disconnect  connection_status=0 internet_status=0 data_mode=22 RATs=4g,nr
after-connect     connection_status=0 internet_status=0 data_mode=22 RATs=4g,nr
after-connect     connection_status=0 internet_status=0 data_mode=22 RATs=4g,nr
after-connect     connection_status=1 internet_status=1 data_mode=22 RATs=4g,nr
production-final  connection_status=1 internet_status=1 data_mode=22 RATs=4g,nr
restored          connection_status=1 internet_status=1 data_mode=22 RATs=4g,nr
```

The same run also physically passed `util_wan/select_network` with
`network_param="auto"` and exact automatic-mode read-back/restore.

Key interpretation:

- simultaneous `4g` + `nr` radio presence is observable while
  `connection_status=1` and Internet connectivity is fully restored;
- the radio combination therefore does **not** explain the previously observed
  WAN `connection_status=2`;
- `connection_status` remains a WAN/link-state concept and must be kept
  separate from radio-access technology / NSA coexistence;
- the earlier value `2` remains a rare physically observed non-final WAN
  transition whose exact frontend label is still unresolved.

No USB management-mode mutation was performed.

Final physical result: 2 tests passed.
