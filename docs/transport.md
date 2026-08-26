# Transport

## Single calls

Observed URL form:

```text
/api.cgi?path=<namespace>&method=<method>&timeout=<seconds>
```

The stock frontend helper behaves as follows:

- a truthy request body is JSON-serialized and sent with HTTP `POST`;
- an absent request body is sent with HTTP `GET`;
- authenticated browser requests rely on the `CGISID` cookie;
- the executable frontend helper defaults to approximately 10 seconds even though a nearby source comment claims 30 seconds.

## JSON numeric serialization

The stock frontend normally converts numeric JSON values to strings when its internal `toStringData` option is enabled (the default in the observed helper). Clients should therefore be tolerant where the backend accepts stringified numeric values.

Do **not** generalize this into an assumption that all number-like fields are interchangeable strings and integers. Follow the per-method evidence.

## Success and error handling

HTTP status alone is insufficient. Several API operations return HTTP 200 while reporting failure or authorization problems in the JSON body. Other disruptive actions may reset connectivity before a useful response arrives.

Recommended decision order:

1. evaluate HTTP/network outcome;
2. inspect method-specific response/error fields;
3. for actions that can disrupt management connectivity, reconnect;
4. re-authenticate if needed;
5. read the affected state back before declaring success.

## File endpoint

The stock web UI can download a configuration backup using `/file.cgi`. This is a separate CGI family from `/api.cgi` and may return opaque binary configuration data containing secrets. Do not log or publish such backups.
