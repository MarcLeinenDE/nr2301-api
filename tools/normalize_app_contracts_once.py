# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
import re
from pathlib import Path

METHODS = Path("specification/methods.json")
SEMANTICS = Path("specification/semantics.json")

methods_doc = json.loads(METHODS.read_text(encoding="utf-8"))
semantics_doc = json.loads(SEMANTICS.read_text(encoding="utf-8"))
methods_doc["release"] = "0.1.1.dev0"
semantics_doc["release"] = "0.1.1.dev0"
by_id = {m["method_id"]: m for m in methods_doc["methods"]}

# SMS delete: exact frontend + live delete/read-back contract.
delete = by_id["sms/sms.delete"]
delete["request"]["http_method"] = "POST"
delete["request"]["schema"] = {
    "sms": {"id": "message ID; numeric values are stringified on wire by the stock frontend"}
}
delete["request"]["basis"] = "exact shipped frontend request + live delete/read-back verification"
delete["response_schema"] = {
    "sms": {"resp": "integer", "smsDelSucc": "integer", "smsDelFail": "integer"}
}
delete["implementation_notes"] = [
    "The stock frontend request is {sms:{id:<message id>}} with default toStringData=true.",
    "Verified success is sms.resp=0, sms.smsDelSucc=1 and sms.smsDelFail=0; tested Inbox/Outbox IDs were absent on mailbox read-back.",
]

# SMS send: exact frontend + live end-to-end contract.
send = by_id["sms/sms.send"]
send["request"]["http_method"] = "POST"
send["request"]["schema"] = {
    "sms": {
        "id": "-1 for a new message; stock frontend stringifies it on wire",
        "gsm7": "1 when message uses GSM 03.38 basic/extension characters, otherwise 0",
        "address": "comma-separated recipient list with a trailing comma",
        "body": "frontend UniEncode: UTF-16BE code units as uppercase hexadecimal",
        "date": "YY,M,D,H,M,S,timezone; positive timezone sign is %2B",
        "protocol": "0 for the live-verified normal SMS flow",
    }
}
send["request"]["basis"] = "exact shipped frontend request + live end-to-end SMS verification"
send["response_schema"] = {
    "sms": {
        "resp": "integer",
        "smsSendSucc": "integer",
        "smsSendFail": "integer",
        "smsRef": "optional modem reference",
    }
}
send["implementation_notes"] = [
    "Default frontend serialization uses toStringData=true, so numeric request fields are stringified on wire.",
    "Live normal-SMS success returned sms.resp=0, smsSendSucc=1 and smsSendFail=0; a matching Outbox status=0 entry and physical receipt were confirmed.",
    "Recipient and message content were deliberately excluded from canonical/public evidence.",
]

# Wi-Fi: publish the already live-verified mode/Guest subcontracts.
wifi = by_id["wireless/wifi_set_ap_config"]
wifi["request"]["http_method"] = "POST"
wifi["request"]["schema"] = {
    "switch": "on|off (optional)",
    "maxassoc": "string (optional)",
    "mode": "DUAL|DUAL GUEST|2.4G 5G|2.4G 5G GUEST (optional; verified on tested firmware)",
    "wifi_if_24G": "object (optional; preserve current block when participating in a mode transition)",
    "wifi_if_5G": "object (optional; preserve current block when participating in a mode transition)",
    "wifi_if_DUAL": "object (optional; preserve current block when participating in a mode transition)",
    "wifi_if_GUEST": "object (optional; preserve current block; fields include band_mode, ssid, encryption, key, hidden, isolate, maxassoc)",
    "wifi_timed_off": "object (optional)",
}
wifi["request"]["basis"] = "exact shipped frontend contracts + live reset/recovery/read-back transitions"
existing = {c.get("id") for c in wifi.get("semantic_contracts", []) if isinstance(c, dict)}
if "wifi.mode_tokens.aci_y3.v1" not in existing:
    wifi.setdefault("semantic_contracts", []).append({
        "id": "wifi.mode_tokens.aci_y3.v1",
        "evidence": "LIVE_VERIFIED_WITH_RESET_READBACK_RESTORE",
        "field": "mode",
        "values": ["DUAL", "DUAL GUEST", "2.4G 5G", "2.4G 5G GUEST"],
    })
if "wifi.guest_token.v1" not in existing:
    wifi.setdefault("semantic_contracts", []).append({
        "id": "wifi.guest_token.v1",
        "evidence": "LIVE_VERIFIED_WITH_RESET_READBACK_RESTORE",
        "field": "mode",
        "rule": "Guest is enabled by presence of the GUEST token; preserve it across DUAL/split transitions.",
    })
notes = wifi.get("implementation_notes", []) + [
    "DUAL means a combined main SSID for 2.4/5 GHz in the tested frontend contract; do not label this Band Steering unless separately proven.",
    "DUAL GUEST <-> 2.4G 5G GUEST and final restore were live verified with Guest/Main configuration and secrets preserved.",
    "Guest enable/disable is controlled by the GUEST token in mode; there is no separate Guest-enable field.",
    "Guest maxassoc 10->9->10 was live read/write/read-back/restored; frontend range is 1..10.",
    "Do not expose Guest isolate independently on ACIY.3: the getter does not round-trip that field and the stock frontend sources it from main 5 GHz isolation.",
]
wifi["implementation_notes"] = list(dict.fromkeys(notes))

METHODS.write_text(json.dumps(methods_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
SEMANTICS.write_text(json.dumps(semantics_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

sms_path = Path("api/sms.md")
sms_text = sms_path.read_text(encoding="utf-8")
delete_block = '''<a id="smsdelete"></a>

## `sms.delete`

**Method ID:** `sms/sms.delete`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "sms": {
    "id": 123
  }
}
```

The stock frontend uses its default `toStringData=true`, so a numeric logical ID is serialized as a JSON string on the wire.

### Response

```json
{
  "sms": {
    "resp": 0,
    "smsDelSucc": 1,
    "smsDelFail": 0
  }
}
```

### Notes

- Exact frontend request: `{sms:{id:<message id>}}`.
- Single-ID delete was live verified for Draft, Inbox and Outbox.
- Verified success is `resp=0`, `smsDelSucc=1`, `smsDelFail=0`; Inbox/Outbox deletion was additionally confirmed by mailbox read-back with the ID absent.

'''
sms_text, n = re.subn(r'<a id="smsdelete"></a>.*?(?=<a id="smsget-brief-info"></a>)', delete_block, sms_text, flags=re.S)
assert n == 1, f"sms.delete replacements={n}"

send_block = '''<a id="smssend"></a>

## `sms.send`

**Method ID:** `sms/sms.send`  
**Endpoint:** `/api.cgi`  
**Operation type:** `WRITE_OR_ACTION`  
**Verification:** `LIVE_VERIFIED`  
**Auth evidence:** `ADMIN_OK`  
**Safety:** `WRITE_OR_SIDE_EFFECT`

### Request

HTTP method: `POST`

```json
{
  "sms": {
    "id": -1,
    "gsm7": 1,
    "address": "<recipient>,",
    "body": "<UTF-16BE uppercase hex>",
    "date": "26,8,25,6,23,57,%2B2",
    "protocol": "0"
  }
}
```

The stock frontend uses default `toStringData=true`; numeric request values such as `id` and `gsm7` are therefore stringified on the wire.

Field contract:

- `id`: `-1` for a new message.
- `gsm7`: `1` when all characters are in the GSM 03.38 basic/extension sets, otherwise `0`.
- `address`: comma-separated recipients with a trailing comma; a single recipient is therefore `<recipient>,`.
- `body`: frontend `UniEncode`, equivalent to UTF-16BE code units encoded as uppercase hexadecimal.
- `date`: local `YY,M,D,H,M,S,timezone`; the frontend encodes a positive timezone sign as `%2B`.
- `protocol`: normal SMS flow was live verified with `"0"`.

### Response

```json
{
  "sms": {
    "resp": 0,
    "smsSendSucc": 1,
    "smsSendFail": 0
  }
}
```

An optional modem `smsRef` may also be present.

### Notes

- Normal SMS was end-to-end live verified: `resp=0`, `smsSendSucc=1`, `smsSendFail=0`, matching Outbox entry `status=0`, and physical receipt confirmed.
- Recipient and message content were deliberately not retained in canonical/public evidence.
- Clients should inspect the SMS-specific success/failure fields; HTTP 200 alone is not sufficient.
'''
sms_text, n = re.subn(r'<a id="smssend"></a>.*\Z', send_block, sms_text, flags=re.S)
assert n == 1, f"sms.send replacements={n}"
sms_path.write_text(sms_text, encoding="utf-8")

wifi_path = Path("api/wireless.md")
wifi_text = wifi_path.read_text(encoding="utf-8")
pattern = r'(<a id="wifi-set-ap-config"></a>.*?### Request\n\nHTTP method: `POST`\n\n)(.*?)(\n### Response)'
request_text = '''Known optional top-level request fields/blocks from the shipped frontend and verified app contract:

- `switch`
- `maxassoc`
- `mode`
- `wifi_if_24G`
- `wifi_if_5G`
- `wifi_if_DUAL`
- `wifi_if_GUEST`
- `wifi_timed_off`

Verified mode tokens on firmware `V1.00(ACIY.3)C0`:

```text
DUAL             = combined main 2.4/5 GHz SSID, Guest off
DUAL GUEST       = combined main 2.4/5 GHz SSID, Guest on
2.4G 5G          = separate main 2.4 GHz and 5 GHz settings, Guest off
2.4G 5G GUEST    = separate main 2.4 GHz and 5 GHz settings, Guest on
```

There is no separate Guest-enable property: Guest is controlled by the presence of the `GUEST` token in `mode`.

For DUAL/split transitions, preserve current participating blocks instead of reconstructing them from defaults. The live-verified application flow copied `wifi_if_DUAL`, `wifi_if_24G`, `wifi_if_5G` and `wifi_if_GUEST`, changed only `mode`, then recovered and required exact mode read-back. This verified:

```text
DUAL
-> DUAL GUEST
-> 2.4G 5G GUEST
-> DUAL GUEST
-> DUAL
```

with Main/Guest configuration and secrets preserved and the original state restored.

Guest enable/disable can use `mode` plus the complete current `wifi_if_GUEST` block. Guest fields evidenced by the frontend are `band_mode`, `ssid`, `encryption`, `key`, `hidden`, `isolate`, `maxassoc`.

> [!CAUTION]
> On ACIY.3, do not expose `wifi_if_GUEST.isolate` as an independently round-trippable setting. The getter does not return it, while the stock frontend sources the written value from the main 5 GHz isolation control.

Guest `maxassoc` was live verified `10 -> 9 -> 10` with read-back/restore; frontend-supported normal range is `1..10`.
'''
wifi_text, n = re.subn(pattern, lambda m: m.group(1) + request_text + m.group(3), wifi_text, flags=re.S)
assert n == 1, f"wifi replacements={n}"
wifi_path.write_text(wifi_text, encoding="utf-8")

print("Normalized SMS send/delete and Wi-Fi mode/Guest contracts.")
