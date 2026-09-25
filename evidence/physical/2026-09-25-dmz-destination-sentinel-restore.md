# DMZ destination sentinel / restore semantics — 2026-09-25

Device: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

## Historical context

A prior physical read on 2026-08-25 already observed the DMZ getter returning the
incomplete string:

```text
192.168.
```

That value was one reason DMZ-destination writes were deliberately deferred at
the time: the original state could not be proven restorable through the verified
setter.

The 2026-09-14 Firewall/NAT campaign later confirmed that a valid synthetic DMZ
destination can be written and read back, but no verified NR2301 clear/delete
operation exists for returning to a no-real-destination state.

## 2026-09-25 public-SDK test

The dedicated public-SDK DMZ-destination test started from:

- DMZ disabled;
- getter value `dmz_dest_ip = "192.168."`.

The harness incorrectly classified every non-empty getter string as
setter-restorable.

It then:

1. captured an in-memory configuration backup;
2. enabled DMZ temporarily as needed;
3. wrote a valid synthetic in-LAN IPv4 destination;
4. verified that destination by read-back;
5. attempted to restore the original getter text `"192.168."` through
   `fw_edit_dmz_entry`;
6. restored DMZ enable state.

The restore setter call did not raise an SDK transport/protocol exception, but
the final getter still returned the synthetic valid IPv4 destination.

All other sampled Firewall state matched the original snapshot.

## Physical result

The important state transition was:

```text
original getter: incomplete/non-IPv4 sentinel
valid synthetic write: persisted and read back
attempted sentinel write-back: did not restore getter state
final getter: synthetic valid IPv4 remained
```

Therefore a non-empty getter string is **not sufficient** evidence that the value
is safely restorable through `fw_edit_dmz_entry`.

## Canonical contract consequences

### Getter

`firewall/fw_get_dmz_info.dmz_dest_ip` is a raw firmware string and may contain
an incomplete/non-IPv4 sentinel-like value such as the physically observed
`"192.168."` when no normal restorable destination is configured.

Clients must preserve the raw value. They must not assume that every non-empty
getter string is a valid IPv4 address or a setter-round-trippable value.

### Setter

`firewall/fw_edit_dmz_entry` remains verified only for syntactically valid,
non-empty IPv4 destination strings.

A successful HTTP/API call alone does not prove that an invalid/incomplete value
was persisted. Setter success must be decided from semantic getter read-back.

### Restore planning

Before mutating the DMZ destination:

- parse the original getter value as IPv4;
- if it is a valid IPv4 address, it may be restored through the same verified
  setter and must still be read back;
- if it is empty or not a valid IPv4 address, treat it as **not setter-restorable**
  and use a full configuration-backup restore path after the test.

The dedicated physical test must therefore choose its recovery mode from
`valid IPv4 vs. not valid IPv4`, not from `empty vs. non-empty`.

## Current lab-router residue

Because the 2026-09-25 test selected the wrong restore path, the synthetic valid
DMZ destination remained stored after the process exited, although DMZ itself
was disabled.

The in-memory pre-test backup disappeared with the test process and cannot be
used retrospectively. Do not perform additional DMZ-destination mutations until
this known residue has been explicitly handled.

No credentials, session identifiers, real client identifiers or unrelated
configuration values are included here.
