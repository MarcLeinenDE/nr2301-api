# SMS recipes

Detailed reference: [`sms`](../../api/sms.md).

SMS content and phone numbers are personal data. Do not include real messages/numbers in public logs, tests or issue reports.

## Read mailbox summary

GET `sms/sms.get_brief_info` for unread/new counts, memory-full state and delivery/flash metadata.

## List messages by mailbox type

POST `sms/sms.list_by_type`:

```json
{
  "sms": {
    "page_index": 1,
    "list_type": 0
  }
}
```

`list_type` is interpreted using the endpoint's documented SMS list semantics (Inbox/Outbox/Draft). Do not reuse an enum from another SMS field merely because the integer values look similar.

The response contains paging information and message nodes.

## Query message IDs

POST `sms/sms.query`:

```json
{
  "sms": {
    "type": 4,
    "read": 2,
    "location": 0
  }
}
```

On semantic success the frontend treats `ids` as a comma-separated list. Follow the endpoint-specific result semantics.

## Read a message by ID

Use `sms/sms.get_by_id` with the `sms` request object documented on the method page.

This method is classified `READ_WITH_SIDE_EFFECT`: reading a message may affect its read/unread state. Do not assume all GET-like operations are side-effect free.

## Save a draft

Use `sms/sms.save` with the frontend-shaped `sms` object. The complete draft/edit request object is not yet normalized as a stable public contract. Preserve a separately verified frontend/current object shape instead of inventing fields.

## Send a normal SMS

POST `sms/sms.send` with the exact normal-SMS frontend shape:

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

Field rules:

- `id`: `-1` for a new message.
- `gsm7`: `1` if every character is in the GSM 03.38 basic/extension character sets, otherwise `0`.
- `address`: comma-separated recipient numbers with a trailing comma; one number is therefore `<recipient>,`.
- `body`: the frontend `UniEncode` representation, equivalent to UTF-16BE code units written as uppercase hexadecimal.
- `date`: local `YY,M,D,H,M,S,timezone`; a positive timezone sign is encoded as `%2B`.
- `protocol`: the end-to-end live-verified normal SMS flow uses `"0"`.

The stock frontend uses its default `toStringData=true`, so numeric fields such as `id` and `gsm7` are strings on the actual wire request.

Verified semantic success:

```json
{
  "sms": {
    "resp": 0,
    "smsSendSucc": 1,
    "smsSendFail": 0
  }
}
```

The live test also found a matching Outbox entry with `status=0`, and physical receipt was confirmed. Recipient and message content were deliberately excluded from canonical/public evidence.

A client must inspect the SMS-specific success/failure fields rather than relying on HTTP 200.

## Delete one message

POST `sms/sms.delete`:

```json
{
  "sms": {
    "id": 123
  }
}
```

The stock frontend again uses default `toStringData=true`, so a numeric logical ID is serialized as a string on the wire.

Verified success:

```json
{
  "sms": {
    "resp": 0,
    "smsDelSucc": 1,
    "smsDelFail": 0
  }
}
```

Single-ID deletion was live verified for Draft, Inbox and Outbox. Inbox/Outbox tests also confirmed by mailbox read-back that the deleted ID was absent.

## Methods not implemented on the tested backend

- `sms/sms.get_config`
- `sms/sms.get_cds`

They are retained because the shipped frontend references them, but the tested runtime did not provide the expected working backend contract. Do not depend on them without firmware-specific re-verification.

## Recommended client behavior

For any SMS write:

1. capture the current relevant mailbox list/count when useful for verification;
2. perform the action using the endpoint-specific request contract;
3. inspect the SMS-specific response values;
4. refresh the target mailbox when an exact post-action read-back is practical;
5. never log message bodies or recipient/sender numbers by default.
