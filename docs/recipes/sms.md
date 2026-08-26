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

Use `sms/sms.save` with the frontend-shaped `sms` object. The method is live verified, but the complete public request object has not yet been normalized. Preserve the frontend/current object shape instead of inventing fields.

## Send an SMS

Use `sms/sms.send` with the frontend-shaped `sms` object.

End-to-end live verification observed semantic success, an Outbox record and physical receipt. A production client should still verify the returned SMS-specific success/failure fields rather than relying on HTTP 200.

## Delete messages

Use `sms/sms.delete` with the documented `sms` object/IDs. Single-message deletion was live verified for Draft, Inbox and Outbox and checked by read-back.

## Methods not implemented on the tested backend

- `sms/sms.get_config`
- `sms/sms.get_cds`

They are retained because the shipped frontend references them, but the tested runtime did not provide the expected working backend contract. Do not depend on them without firmware-specific re-verification.

## Recommended client behavior

For any SMS write:

1. capture the current relevant mailbox list/count;
2. perform the action;
3. inspect SMS-specific response values;
4. refresh the target mailbox and verify the resulting record/state;
5. never log message bodies or recipient/sender numbers by default.