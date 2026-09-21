# Configuration backup/restore production SDK lifecycle — 2026-09-21

Physical device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

The production SDK exercised the complete current stock-WebUI configuration
backup/restore path through `/file.cgi`.

Observed successful lifecycle:

```text
initial_backup_size=14424
initial_backup_sha256=ec87316928c9a3cb033ce2f2b3024bfdfd1c2c3efef43c94df8990549c1ea26e
uploaded_bytes=14424
chunk_count=1
boot_before=434
boot_after=55
outage_observed=True
final_upload_error=TransportError
```

After runtime recovery, the firewall/UPnP API was not immediately ready:

```text
attempt 1: upnp -> ProtocolError
attempt 2: upnp -> ProtocolError
attempt 3: upnp -> ProtocolError
attempt 4: upnp -> ProtocolError
attempt 5: joint configuration snapshot succeeded
```

The stable pre/post configuration snapshot matched exactly across:

- UI language
- work mode
- sleep-wait timer
- timed reboot settings
- LAN DNS settings
- UPnP state
- VPN passthrough state
- WAN ping state
- WAN admin-access state

A fresh backup after restore also succeeded:

```text
post_restore_backup_size=14432
post_restore_backup_sha256=bef1b50308da01d6b5f77d6b0d315b448ee26ef12d1d483e96c31111439c41ad
```

The changed size/hash despite an exactly matching stable configuration state
proves that backup byte identity is not a valid restore-equivalence check.
Restore verification should be based on relevant configuration state, not
backup-file hash equality.

No backup contents were logged or committed. No USB-mode mutation was
performed.

Final physical result: PASS.
