# Configuration backup/restore file-CGI contract — 2026-09-21

Physical/source target: Zyxel NR2301, firmware `V1.00(ACIY.3)C0`.

The stock WebUI page `html/set_config.html` and shared
`js/base/ajax_calls.js` were captured read-only from the authenticated router
session and inspected without performing a restore.

## Backup download

The current frontend backup button directly assigns:

```text
/file.cgi?Action=Download&file=backup_config&dl=1
```

to a hidden iframe. The older `router/router_backup_config` call is present
only as commented-out frontend code on this page.

Canonical transport:

- HTTP: `GET`
- endpoint: `/file.cgi`
- query: `Action=Download&file=backup_config&dl=1`
- body: none
- response: opaque binary configuration backup

## Configuration restore

The page reads the selected configuration file in sequential 1 MiB slices and
passes each slice to the shared `configFileUpload` function.

The shared function sends each chunk as:

```text
POST /file.cgi?Action=Upload&file=restore_config
Content-Type: application/octet-stream
<body: raw binary chunk>
```

Observed frontend behavior:

- no multipart/form-data wrapper;
- no filename form field;
- no `Content-Range` header for configuration restore;
- no first-chunk total-size content-type extension (unlike the firmware-upload
  helper nearby in the same source);
- chunks are posted sequentially to the same URL;
- frontend chunk size is 1 MiB;
- frontend file-size limit is 200 MiB;
- a response body containing `other error` is treated as failure;
- after the final successful chunk, the frontend calls only the local
  `config_effective()` UI function;
- there is no separate API apply/commit call in the captured restore flow;
- the UI explicitly warns that a successful restore causes the device to reboot.

## Security

Configuration backup bytes can contain credentials and other secrets. Do not
publish, log or commit real backup data. Public evidence should contain only
transport metadata, sizes/hashes where appropriate, and sanitized state
verification.

No restore was performed while collecting this source evidence.
