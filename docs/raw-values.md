# Raw values and semantics

The NR2301 API contains endpoint-specific integers and string tokens that are easy to misinterpret. This project therefore treats raw semantics as a separate part of the API contract.

Machine-readable mappings are in [`../specification/semantics.json`](../specification/semantics.json).

## Rules

- Preserve unknown raw values instead of inventing a label.
- Do not create a global error-code enum where the same integer has endpoint-specific meaning.
- Keep connection/link status separate from Internet reachability where the API exposes both.
- Preserve source-exact string tokens when capitalization is significant.
- Treat special invalid-measurement sentinels as field-scoped evidence, not universal magic values.

## SINR invalid sentinel

On the tested NR2301, `cm/query_eng_info` was observed returning SINR `-32768` when no usable measurement was available. This value is therefore normalized as **invalid/unavailable for that SINR field only**.

Do not automatically convert `-32768` in unrelated fields to unavailable unless separate evidence establishes the same contract.

## Selected examples

The semantic catalog includes, among others:

- cellular `data_mode` values;
- SIM/PIN state;
- battery state and battery indicator ranges;
- LTE/5G operator-scan access technology tokens;
- work-mode values;
- SMS endpoint-scoped status codes;
- endpoint-scoped error codes;
- WPS state tokens;
- scheduled reboot weekday bitmask.
