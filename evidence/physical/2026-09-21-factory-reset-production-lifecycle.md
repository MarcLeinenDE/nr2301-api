# Factory reset + credential restore production lifecycle — 2026-09-21

Physical device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

The dedicated test router initially used its device-default administrator
password. A full production-SDK factory-reset lifecycle was exercised with a
temporary non-default administrator credential and two in-memory backups.

Observed sequence:

1. capture stable baseline configuration;
2. download baseline backup while the router still uses the default password;
3. change administrator password through source-verified `account/set_info`;
4. verify fresh login with the temporary password;
5. download a second backup containing the temporary password;
6. set a synthetic disabled timed-reboot marker;
7. call `router/router_call_rst_factory`;
8. recover using the device-default password;
9. verify the synthetic marker was cleared by factory reset;
10. restore the second backup and recover with the temporary password;
11. restore the baseline backup in the cleanup path and recover with the
    original/default password;
12. verify the original stable configuration state exactly.

Sanitized physical observations:

```text
baseline_backup_size=14440
test_backup_size=14448

factory_reset:
  boot_before=1864
  boot_after=50
  outage_observed=True
  action_error=TransportError
  default_credential_recovery=True

timed_reboot_marker:
  synthetic_before=(disabled, 23:57, repeat=85)
  after_factory_reset=(disabled, 00:00, repeat=0)

test_backup_restore:
  boot_before=51
  boot_after=58
  outage_observed=True
  action_error=TransportError
  uploaded_bytes=14448
  chunks=1
  temporary_credential_recovery=True

baseline_restore:
  boot_before=58
  boot_after=56
  outage_observed=True
  action_error=TransportError
  uploaded_bytes=14440
  chunks=1
  original/default_credential_recovery=True

post-cleanup:
  stable_configuration_equal=True
  UPnP API readiness required three transient retries and succeeded on attempt 4
```

The pytest harness reported a final FAILED status only because it asserted
`boot_time_after < boot_time_before` for the test-backup restore. That
assertion is invalid when a restore is issued shortly after a previous reboot:
pre-action uptime was only 51 seconds, while management recovery after the next
reboot completed at uptime 58 seconds.

The restore helper had already accepted this case using its second reboot proof:
observed management outage plus a fresh-uptime bound. The credential change back
to the temporary password and successful post-restore state reads independently
confirm that the backup was applied.

Contract implications:

- factory reset through body-less GET is physically verified;
- the device returns to the device-default administrator credential after reset;
- configuration restore can restore the administrator credential contained in
  the backup;
- for disruptive operations issued shortly after a previous reboot, direct
  `boot_time_after < boot_time_before` is not always a valid reboot test;
- clients should expose whether reboot verification came from a direct uptime
  reset or from outage + fresh-uptime evidence;
- final restore correctness must still be verified by recovered credentials and
  relevant configuration state.

No USB management-mode mutation was performed.
