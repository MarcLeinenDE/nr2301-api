# Configuration restore post-reboot API readiness — 2026-09-21

Physical device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

A production-SDK configuration backup/restore lifecycle used the stock
`/file.cgi` transport with an in-memory backup from the same router.

Observed:

```text
backup_size=15136
restore_uploaded_bytes=15136
restore_chunks=1
boot_before=236580
boot_after=56
outage_observed=True
final_upload_error=TransportError
```

These observations prove that the restore upload completed far enough to trigger
the expected full reboot and that management subsequently recovered.

Immediately after `router/get_runtime_info` was readable again, a later
configuration read `firewall/ww_upnp_open_close_state` returned HTTP 200 with
an empty/non-JSON body. Earlier configuration reads in the same post-reboot
snapshot had already succeeded.

Contract implication:

- device/runtime recovery does not guarantee every namespace/subsystem is
  immediately API-ready after a configuration restore reboot;
- clients that need to verify restored configuration should poll/retry the
  complete required state set until all relevant reads succeed in one stable
  pass;
- an isolated empty/non-JSON response during this settling window should not be
  interpreted as proof that the restore failed.

The test is being updated to wait for joint readiness of the stable
configuration reads before comparing pre/post restore state.
