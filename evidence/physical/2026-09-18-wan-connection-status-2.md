# WAN reconnect transition state — 2026-09-18

Physical device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

During a disruptive production-SDK WAN-control test, the following sequence was
confirmed:

1. `cm/disconnect`
2. `cm/get_current_wan_info` reached `connection_status=0`
3. `cm/connect`
4. a subsequent `cm/get_current_wan_info` returned:

```json
{
  "wan_type": "mobile",
  "contextlist": [
    {
      "connection_status": 2,
      "internet_status": 0
    }
  ]
}
```

The public semantic table previously documented only 0=disconnected and
1=connected. The value 2 must therefore be accepted as a non-final transition
during reconnect. The exact frontend label for value 2 is not yet reconstructed
and is deliberately not guessed.

The original test treated value 2 as invalid, causing its cleanup path to stop
early. A following network-selection read then timed out while the device was
still recovering. No USB-mode mutation was involved.
