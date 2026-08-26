# SIM and PIN recipes

Detailed reference: [`sim`](../../api/sim.md).

SIM PIN/PUK writes can consume limited retry counters or leave the SIM unusable until a correct PIN/PUK is entered. The write methods are therefore retained as **reference-only static contracts** in the current catalog rather than promoted to live-tested copy-paste operations.

## Read SIM/PIN status

GET `sim/get_sim_status`.

The response includes:

- `sim_status`
- `pin_status`
- `pin_enabled`
- `pin_attempts`
- `puk_attempts`

Use the endpoint-specific enum documented in the semantics reference.

`sim/get_lock_info` also exists, but the tested normal-admin runtime returned an empty HTTP 200 body. Treat it as limited evidence rather than a dependable status source.

## Provide PIN — reference only

`sim/provide_pin` is statically confirmed. The frontend uses a nested `pin_puk` object. It has not been deliberately live exercised in this research set.

## Enable/disable PIN — reference only

- `sim/enable_pin`
- `sim/disable_pin`

The frontend shape uses:

```json
{
  "pin_puk": {
    "pin": "PIN"
  }
}
```

These methods remain `DO_NOT_TEST_FOR_COVERAGE` in the public catalog.

## Change PIN — reference only

The static frontend contract for `sim/change_pin` uses:

```json
{
  "pin_puk": {
    "pin": "CURRENT_PIN",
    "new_pin": "NEW_PIN"
  }
}
```

Do not automate retries around this operation.

## Reset PIN using PUK — reference only

`sim/reset_pin_using_puk` is statically confirmed but intentionally not live exercised. A wrong PUK can permanently exhaust the SIM's recovery counter.

## Safe client design

A client that exposes SIM writes should:

1. read `get_sim_status` first;
2. display remaining retry counters prominently;
3. require explicit user action for every PIN/PUK submission;
4. never automatically retry a failed secret;
5. never log PINs or PUKs;
6. treat the current write contracts as firmware-sensitive until independently re-verified.