# Phonebook write lifecycle physical evidence — 2026-09-10

Device/firmware: Zyxel NR2301, tested firmware V1.00(ACIY.3)C0.
Authentication: normal administrator session.
Scope: synthetic local-phonebook data only. No SIM contacts and no USB-management-mode changes.

## Confirmed group lifecycle

Physical profiler runs confirmed all of the following with `result = 0` and read-back verification:

- `phonebook/addnew_group`
- `phonebook/update_group`
- `phonebook/delete_group`

Two synthetic groups were created, one was renamed, and both were later deleted. Final group count returned to the initial count.

## Confirmed local contact creation/deletion

`phonebook/addnew_pb` with the nested `addnew_pb` object successfully created synthetic local contacts and returned `result = 0`.

`phonebook/delete_pb` successfully deleted synthetic local contacts using:

```json
{
  "delete_pb": {
    "location": "0",
    "count": "1",
    "indexarray": "<index>"
  }
}
```

A dedicated cleanup run subsequently started from exactly five local contacts with indexes `3,4,5,6,7`, deleted each index individually with `result = 0`, verified each index absent after deletion, and ended with zero local contacts. This restored the known pre-profiler baseline exactly.

## Contact text codec correction

The shipped WebUI establishes that local-contact `name` and `email` are not sent as plain text. Before `addnew_pb` / `update_pb`, the WebUI calls `UniEncode()` for those two fields. `UniEncode()` serializes each JavaScript UTF-16 code unit as four lowercase hexadecimal characters. On read, the WebUI calls `UniDecode()` and reconstructs text from four-hex-character code units.

Equivalent examples:

- `CodecA1` -> `0043006f00640065006300410031`
- a non-BMP character would be represented by its UTF-16 surrogate-pair code units, preserving WebUI behavior.

`mobile`, `home`, `office`, `location`, `index` and `group` are not passed through this text codec by the WebUI.

Earlier physical probes that sent plain text in `name`/`email` therefore did **not** represent the correct application-level write contract. Their apparent `name`/`email` update failures are superseded by the corrected codec test below.

## Corrected `addnew_pb` create behavior

A hard-gated physical test using the corrected SDK codec started from zero local contacts and created one synthetic contact.

Observed on ACIY.3:

- `result = 0`;
- exactly one new local index appeared;
- raw `name` read-back exactly matched the WebUI `UniEncode()` representation;
- decoding the raw `name` produced exactly the submitted human-readable name;
- `mobile` round-tripped exactly;
- correctly `UniEncode()`-encoded `email` still read back as the literal string `"-"`;
- non-empty `home` read back as `None`;
- non-empty `office` read back as `None`.

Therefore the correct wire codec for `name` is physically verified. The correct WebUI codec is also used for `email`, but tested firmware does not expose the submitted email value through the observed local-contact read path.

## Corrected `update_pb` behavior

The accepted nested shape remains:

```json
{
  "update_pb": {
    "location": "0",
    "index": "<contact-index>",
    "name": "<UniEncode(name)>",
    "mobile": "<mobile>",
    "home": "<home>",
    "office": "<office>",
    "email": "<UniEncode(email)>",
    "group": "<group-index>"
  }
}
```

A flat object without the `update_pb` wrapper previously returned `result = -5` and remains rejected evidence.

The corrected physical test updated the same synthetic contact with:

- Unicode name `ÄÖÜßé€2`;
- a new mobile value;
- new non-empty home/office values;
- a new encoded email value.

Observed:

- `result = 0`;
- same contact index retained;
- raw `name` became `00c400d600dc00df00e920ac0032`, exactly matching `UniEncode("ÄÖÜßé€2")`;
- decoding that raw value returned exactly `ÄÖÜßé€2`;
- `mobile` changed to the requested target;
- `email` remained `"-"`, unchanged from its create-time read-back;
- `home` remained `None`, unchanged from its create-time read-back;
- `office` remained `None`, unchanged from its create-time read-back.

Together with the prior isolated group-field test, the physically demonstrated mutable/read-back-visible fields on ACIY.3 are now:

- `name` — effective when sent in the WebUI `UniEncode()` format, including Unicode;
- `mobile` — effective as plain string;
- `group` — effective as the confirmed numeric-string write field.

For the observed read path, `email`, `home` and `office` do not expose the submitted values on this firmware even when using the WebUI-compatible request representation. `result = 0` must therefore not be interpreted as proof of visible persistence for those fields.

No copy-on-update behavior was observed; the contact retained the same index.

## Confirmed `move_contacts_to_group`

The following representation was physically confirmed with both group-specific read-back and the local contact `group` field:

```json
{
  "newgroup": "<group-index>",
  "contacts": "<single-contact-index>"
}
```

Observed response: `result = 0`.

This confirms, for a single local contact on ACIY.3, that both `newgroup` and `contacts` may be scalar strings. The multi-contact representation remains to be physically established.

## Multi-delete static evidence

Related backend source shows `delete_pb.indexarray` is parsed as a comma-separated string using tokenization on `,`, while `count` is parsed separately as a string integer. This strongly supports comma-separated multi-index serialization, but NR2301 physical multi-delete evidence is still tracked separately before a plural SDK helper is frozen.

## Profiler cleanup finding and recovery

An intermediate lifecycle profiler exposed a harness defect: final local contact count was five while the initial count was zero, but the old profiler still printed `PASS` because cleanup relied on synthetic name prefixes. The five new indexes were `3,4,5,6,7`.

A dedicated cleanup verified that the complete local index set was exactly those five indexes, deleted every index individually with `result = 0`, verified each absent, and restored the known baseline of zero local contacts.

Subsequent field and codec tests use index-delta ownership and require the exact initial index set at the end. The corrected codec test created index `41`, deleted it with `result = 0`, and ended with `FINAL_LOCAL_CONTACT_COUNT = 0` and `FINAL_INDEX_SET_MATCH = True`.

## Public SDK lifecycle validation

The normalized single-contact/group contracts were exercised through the public `nr2301-python` high-level Phonebook helpers on 2026-09-10 using Python 3.13.5.

The hard-gated integration suite `tests/integration/test_phonebook_writes.py` passed **2/2 tests in 4.32 s**:

- the high-level group/contact lifecycle created and renamed synthetic groups, created one synthetic local contact, exercised update and move paths, deleted all test-owned rows/groups, and restored the exact initial local-contact index set;
- the SIM-to-local action exercised `copy_all_from_sim_to_local()`, modified no SIM storage, treated only newly created local indexes as test-owned, removed those local rows and restored the exact initial local-contact index set.

The later codec-correction integration test passed **1/1 in 1.02 s**, physically proving WebUI-compatible `name` create/update behavior including Unicode and characterizing the remaining fields as described above.

No real contact names, phone numbers or SIM-contact contents were printed or committed.
