# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path("specification/methods.json")
DOC = Path("api/sms.md")
CHANGELOG = Path("CHANGELOG.md")

root = json.loads(METHODS.read_text(encoding="utf-8"))
by_id = {m["method_id"]: m for m in root["methods"]}


def replace_contract(method: dict, contract: dict) -> None:
    cid = contract["id"]
    method["semantic_contracts"] = [
        c for c in method.get("semantic_contracts", [])
        if not (isinstance(c, dict) and c.get("id") == cid)
    ] + [contract]


send = by_id["sms/sms.send"]
replace_contract(send, {
    "id": "sms.send.sdk_external_e2e.live_2026_08_31.v1",
    "evidence": "LIVE_VERIFIED_SDK_PLUS_PHYSICAL_RECEIPT",
    "verified_success": {"resp": 0, "smsSendSucc": 1, "smsSendFail": 0},
    "external_path": "SDK send -> mobile network -> physical handset receipt confirmed by operator",
    "privacy": "recipient and body deliberately omitted from canonical evidence",
})
send["live_note"] = (
    "Normal SMS was end-to-end live verified through the public SDK: "
    "sms.resp=0, smsSendSucc=1, smsSendFail=0 and physical handset receipt were confirmed. "
    "Recipient/body were not retained."
)
send["implementation_notes"] = list(dict.fromkeys(send.get("implementation_notes", []) + [
    "2026-08-31 public-SDK E2E: a real handset received the synthetic test SMS after the verified send success triple.",
]))

listing = by_id["sms/sms.list_by_type"]
replace_contract(listing, {
    "id": "sms.list.body_representation.live_2026_08_31.v1",
    "evidence": "LIVE_VERIFIED_REAL_SEND_REPLY_EXCHANGE",
    "observed": {
        "outbox.body": "UTF-16BE hexadecimal string",
        "inbox.body": "UTF-16BE hexadecimal string",
    },
    "correlation_note": (
        "A real SDK send was delivered successfully but an initial byte-exact full-body Outbox "
        "correlation was too strict. A recovery read decoded the expected synthetic prefix. "
        "Prefer new message ID + normalized address for correlation; treat body representation as raw data."
    ),
    "privacy": "body/address values deliberately not retained",
})
listing["implementation_notes"] = list(dict.fromkeys(listing.get("implementation_notes", []) + [
    "2026-08-31 real send/reply exchange: both Outbox and Inbox list body values were decodable as UTF-16BE hexadecimal; message values were not retained.",
    "Do not require byte-exact full-body equality as the sole Outbox correlation key; use message ID/address and content only as secondary evidence.",
]))

get_by_id = by_id["sms/sms.get_by_id"]
replace_contract(get_by_id, {
    "id": "sms.get_by_id.inbound_reply.live_2026_08_31.v1",
    "evidence": "LIVE_VERIFIED_SDK_REAL_INBOUND_REPLY",
    "precondition": "new inbound reply was present in Inbox with read=0 before get_by_id",
    "response_fields": [
        "address", "body", "contact_id", "date", "id", "location",
        "protocol", "read", "resp", "status", "type",
    ],
    "body_representation": "UTF-16BE hexadecimal string",
    "read_side_effect": "not re-read after get_by_id in this campaign; do not claim a read-state transition from this evidence alone",
    "privacy": "sender/body values deliberately not retained",
})
get_by_id["live_note"] = (
    "Live verified through the public SDK on a newly arrived real inbound reply. "
    "The prior Inbox row had read=0; get_by_id returned the complete documented field set and a UTF-16BE-hex body. "
    "No post-read state check was performed, so this run does not prove whether read state changed."
)
get_by_id["implementation_notes"] = list(dict.fromkeys(get_by_id.get("implementation_notes", []) + [
    "2026-08-31 public-SDK E2E: get_by_id succeeded on a newly arrived real inbound reply; response fields matched the documented schema and body decoded from UTF-16BE hex.",
    "The reply was observed with read=0 before get_by_id, but no post-read Inbox state was captured; preserve the side-effect warning without asserting a transition occurred.",
]))

METHODS.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

doc = DOC.read_text(encoding="utf-8")

doc = doc.replace(
    '    "body": "string",\n    "contact_id": "integer",\n    "date": "string",\n    "id": "integer",\n    "location": "integer",\n    "protocol": "integer",',
    '    "body": "string (UTF-16BE hexadecimal observed live)",\n    "contact_id": "integer",\n    "date": "string",\n    "id": "integer",\n    "location": "integer",\n    "protocol": "integer",',
    1,
)
get_anchor = '<a id="smsget-cds"></a>'
get_note = '''\n### 2026-08-31 SDK inbound-reply evidence\n\nA real reply to an SDK-originated SMS was detected as a new Inbox item and then read with `sms.get_by_id`. Before the call, the Inbox row reported `read=0`. The returned `sms` object contained exactly these observed fields: `address`, `body`, `contact_id`, `date`, `id`, `location`, `protocol`, `read`, `resp`, `status`, `type`. The body was decodable as UTF-16BE hexadecimal. Sender and body values were deliberately not retained. No post-read Inbox check was performed, so this run does **not** prove that `get_by_id` changed the read flag.\n\n'''
if "### 2026-08-31 SDK inbound-reply evidence" not in doc and get_anchor in doc:
    doc = doc.replace(get_anchor, get_note + get_anchor, 1)

list_anchor = '<a id="smsquery"></a>'
list_note = '''\n### 2026-08-31 SDK list representation evidence\n\nDuring a real SDK-send / handset-reply exchange, both the matching Outbox body and the new Inbox body were observed as UTF-16BE hexadecimal strings. The values themselves were not retained. An initial E2E test that required byte-for-byte equality against the entire sent body was unnecessarily brittle even though delivery succeeded; correlation should primarily use a newly appearing message ID plus normalized address, with body content as secondary evidence.\n\n'''
if "### 2026-08-31 SDK list representation evidence" not in doc and list_anchor in doc:
    doc = doc.replace(list_anchor, list_note + list_anchor, 1)

send_note = '- 2026-08-31 public-SDK E2E: the verified success triple was followed by physical handset receipt; the handset reply was subsequently observed in the router Inbox.\n'
needle = '- Normal SMS was end-to-end live verified: `resp=0`, `smsSendSucc=1`, `smsSendFail=0`, matching Outbox entry `status=0`, and physical receipt confirmed.\n'
if send_note not in doc and needle in doc:
    doc = doc.replace(needle, needle + send_note, 1)

DOC.write_text(doc, encoding="utf-8")

changelog = CHANGELOG.read_text(encoding="utf-8")
entry = (
    "- completed a public-SDK real SMS exchange: send returned `resp=0/smsSendSucc=1/smsSendFail=0` and was physically received; the handset reply appeared as a new Inbox item and `sms.get_by_id` returned the complete documented field set; Inbox/Outbox bodies were observed as UTF-16BE hex, with all phone numbers and message contents excluded from repository evidence\n"
)
marker = 'Development metadata: `0.1.1.dev0`.\n\n'
if entry not in changelog and marker in changelog:
    changelog = changelog.replace(marker, marker + entry, 1)
CHANGELOG.write_text(changelog, encoding="utf-8")

print("Recorded sanitized SMS SDK E2E evidence.")
