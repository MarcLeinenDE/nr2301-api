# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path('specification/methods.json')
DOC = Path('api/sms.md')
CHANGELOG = Path('CHANGELOG.md')

root = json.loads(METHODS.read_text(encoding='utf-8'))
by_id = {m['method_id']: m for m in root['methods']}

get_by_id = by_id['sms/sms.get_by_id']
save = by_id['sms/sms.save']

get_by_id['request'] = {
    'http_method': 'POST',
    'schema': {'sms': {'id': 'message ID; stock frontend default serialization stringifies numeric values on wire'}},
    'basis': 'exact shipped frontend request + existing live response verification',
    'known_frontend_variants': get_by_id.get('request', {}).get('known_frontend_variants', []),
}
get_by_id['implementation_notes'] = list(dict.fromkeys(get_by_id.get('implementation_notes', []) + [
    'Exact shipped frontend request is {sms:{id:<message id>}}.',
    'Opening an unread inbound SMS may mark it read; use a known draft/outbox item for side-effect-free contract testing where possible.',
]))
get_by_id['semantic_contracts'] = [
    c for c in get_by_id.get('semantic_contracts', [])
    if not (isinstance(c, dict) and c.get('id') == 'sms.get_by_id.request.v1')
] + [{
    'id': 'sms.get_by_id.request.v1',
    'evidence': 'STATIC_FRONTEND_EXACT_PLUS_LIVE_RESPONSE',
    'request': {'sms': {'id': '<message id>'}},
    'side_effect_note': 'Reading an unread inbox item may alter read state.',
}]

save['request'] = {
    'http_method': 'POST',
    'schema': {
        'sms': {
            'id': '-1 for a new draft, existing draft ID for update; numeric value is stringified on stock wire',
            'gsm7': 'boolean: true when message is GSM 03.38 basic/extension encodable, else false',
            'address': 'comma-separated recipients with trailing comma',
            'body': 'frontend UniEncode: UTF-16BE code units as uppercase hexadecimal',
            'date': 'YY,M,D,H,M,S,timezone',
            'type': '2 for draft; stringified on stock wire',
            'protocol': 'protocol value; normal draft flow live-verified with 0 and stringified on stock wire',
        }
    },
    'basis': 'exact shipped frontend request + historical live write/response verification',
    'known_frontend_variants': save.get('request', {}).get('known_frontend_variants', []),
}
save['response_schema'] = {
    'sms': {
        'resp': 'integer',
        'smsSaveSucc': 'integer',
        'smsSaveFail': 'integer',
    }
}
save['response_fields'] = list(dict.fromkeys(save.get('response_fields', []) + ['sms']))
save['implementation_notes'] = list(dict.fromkeys(save.get('implementation_notes', []) + [
    'New-draft frontend request uses id=-1 and type=2; existing-draft update uses the current smsId and type=2.',
    'Historical live write returned sms.resp=0, smsSaveSucc=1, smsSaveFail=0.',
    'Historical stock-wire evidence stringified id/type/protocol while gsm7 remained a JSON boolean.',
    'Recipient and body are message content/private data and should not be logged by clients.',
]))
save['semantic_contracts'] = [
    c for c in save.get('semantic_contracts', [])
    if not (isinstance(c, dict) and c.get('id') == 'sms.save.draft.live.v1')
] + [{
    'id': 'sms.save.draft.live.v1',
    'evidence': 'STATIC_FRONTEND_EXACT_PLUS_HISTORICAL_LIVE_WRITE',
    'new_draft': {'id': -1, 'type': 2},
    'update_draft': {'id': '<existing smsId>', 'type': 2},
    'verified_protocol': 0,
    'verified_success': {'resp': 0, 'smsSaveSucc': 1, 'smsSaveFail': 0},
    'wire_note': 'id/type/protocol stringified; gsm7 retained boolean in captured stock-compatible write',
}]

METHODS.write_text(json.dumps(root, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

doc = DOC.read_text(encoding='utf-8')
old_get = '''### Request\n\nHTTP method: `POST`\n\nKnown top-level request keys from the shipped frontend: `sms`.\n'''
new_get = '''### Request\n\nHTTP method: `POST`\n\n```json\n{\n  "sms": {\n    "id": 123\n  }\n}\n```\n\nThe exact shipped-frontend request is `{sms:{id:<message id>}}`. With the stock frontend's default serialization, numeric IDs are stringified on the wire. Reading an unread inbound SMS may mark it read, so contract tests should prefer a known draft or otherwise disposable item.\n'''
get_anchor = '<a id="smsget-by-id"></a>'
next_anchor = '<a id="smsget-cds"></a>'
if get_anchor in doc and next_anchor in doc:
    before, rest = doc.split(get_anchor, 1)
    section, after = rest.split(next_anchor, 1)
    if old_get in section:
        section = section.replace(old_get, new_get, 1)
    doc = before + get_anchor + section + next_anchor + after

old_save = '''### Request\n\nHTTP method: `POST`\n\nKnown top-level request keys from the shipped frontend: `sms`.\n\n### Response\n\nNo stable response schema is currently documented.\n'''
new_save = '''### Request\n\nHTTP method: `POST`\n\nNew draft:\n\n```json\n{\n  "sms": {\n    "id": -1,\n    "gsm7": true,\n    "address": "<recipient>,",\n    "body": "<UTF-16BE uppercase hex>",\n    "date": "26,8,24,14,46,40,+2",\n    "type": 2,\n    "protocol": 0\n  }\n}\n```\n\nUpdating an existing draft uses the same object with `id=<existing smsId>`. `type=2` is the exact draft token. Historical live wire evidence using the stock frontend-compatible serializer showed `id`, `type` and `protocol` as JSON strings on the wire while `gsm7` remained a JSON boolean. `address` keeps the trailing comma and `body` uses the same frontend `UniEncode` representation as SMS send.\n\n### Response\n\n```json\n{\n  "sms": {\n    "resp": 0,\n    "smsSaveSucc": 1,\n    "smsSaveFail": 0\n  }\n}\n```\n\nThis success triple was live verified for a new draft. Recipient and message content are private data and should not be logged.\n'''
save_anchor = '<a id="smssave"></a>'
send_anchor = '<a id="smssend"></a>'
if save_anchor in doc and send_anchor in doc:
    before, rest = doc.split(save_anchor, 1)
    section, after = rest.split(send_anchor, 1)
    if old_save in section:
        section = section.replace(old_save, new_save, 1)
    doc = before + save_anchor + section + send_anchor + after
DOC.write_text(doc, encoding='utf-8')

changelog = CHANGELOG.read_text(encoding='utf-8')
entry = '- normalized the exact `sms/sms.save` new/update-draft request and live success triple, including draft `type=2`, GSM7 boolean wire behavior and stock stringification of id/type/protocol; normalized `sms/sms.get_by_id` as exact `{sms:{id}}` POST and retained its unread-read side-effect warning\n'
marker = 'Development metadata: `0.1.1.dev0`.\n\n'
if entry not in changelog and marker in changelog:
    changelog = changelog.replace(marker, marker + entry, 1)
CHANGELOG.write_text(changelog, encoding='utf-8')

print('Normalized SMS draft and get-by-id contracts.')
