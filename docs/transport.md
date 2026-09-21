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

The stock web UI uses `/file.cgi` as a separate binary-transfer CGI family from `/api.cgi`.

### Configuration backup download

Source-verified on tested ACIY.3:

```text
GET /file.cgi?Action=Download&file=backup_config&dl=1
```

The response is opaque configuration-backup bytes and can contain credentials and other secrets.

### Configuration restore upload

Source-verified on tested ACIY.3:

```text
POST /file.cgi?Action=Upload&file=restore_config
Content-Type: application/octet-stream

<raw configuration bytes>
```

The stock frontend reads the file in sequential 1 MiB slices and POSTs each slice to the same URL. It does **not** use multipart/form-data and does not send a filename field or `Content-Range` header for configuration restore. A response containing `other error` is treated as failure. After the last successful chunk there is no separate apply API call; the frontend only updates its UI and expects the device to reboot.

The frontend limits selected restore files to 200 MiB.

Treat configuration backup/restore bytes as secret-bearing data. Never log, publish or commit real backup contents.
