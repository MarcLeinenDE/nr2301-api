# API ↔ SDK full-coverage audit — 2026-09-21

## Scope and pinned baselines

This audit compares:

- canonical API: `nr2301-api` commit `14c1cdf96609a558570f09ec7aaf7ceba8452cf6`;
- SDK: `nr2301-python` commit `a6f937c32377d6cf6dcfad358141761e230e9532`.

Campaign target: every documented NR2301 API capability should be represented and deliberately tested through the public SDK where the firmware exposes a usable contract.

### Hard exclusion

The only hard mutation exclusion is:

- `router/eng_set_usb_mode`

USB management is the active control/recovery anchor and must not be changed during this campaign. Read-only USB/engineering inspection remains eligible. The physical reset button is the final recovery path.

Credential changes, administrator-password recovery, VPN/DDNS/TR-069 credentials, SIM PIN/PUK, factory reset, WAN interruption, ADB/engineering research, radio changes, and other disruptive/recovery operations are campaign-eligible when the request contract and recovery scenario are explicit.

Safety classes such as `DO_NOT_TEST_FOR_COVERAGE` remain useful risk metadata. Except for USB-mode mutation, they are not permanent campaign bans.

## Audit dimensions

A method is not considered complete merely because it exists somewhere.

1. **API contract** — method exists in the canonical 157-method catalog with current evidence/status.
2. **SDK surface** — a concrete namespace/client implementation references the API method.
3. **Offline coverage** — normal tests contain endpoint/helper contract coverage. The count below uses literal method-reference coverage as a conservative static proxy.
4. **Physical SDK harness** — a persisted physical integration test reaches the method through the public SDK (or an explicit raw call inside the physical test).

Physical-harness reachability is a static audit of the committed test suite; it is not, by itself, a claim that every reachable test has been run successfully in the current router state.

## Headline numbers

- API catalog: **157 / 157**
- API verification distribution:
  - `LIVE_VERIFIED`: **134**
  - `LIVE_VERIFIED_LIMITED`: **4**
  - `LIVE_DENIED`: **3**
  - `LIVE_NOT_APPLICABLE`: **2**
  - `LIVE_REJECTED`: **1**
  - `NOT_IMPLEMENTED`: **2**
  - `STATIC_CONFIRMED`: **11**
- SDK surface: **136 / 157**
- conservative offline literal-method coverage: **135 / 157**
- persisted physical SDK harness reachability: **113 / 157**
- physical-harness gaps: **44**
  - existing SDK surface but no persisted physical reach: **23**
  - no SDK surface: **21**
  - of those 21, exactly **1** is the deliberate USB-mode mutation exclusion
  - therefore **43 non-excluded methods** still need either physical SDK coverage, upstream contract completion, a credential/state campaign, or an explicit negative/not-implemented disposition.

Both repositories are CI-green at the pinned baselines:
- SDK push workflow #389: SUCCESS
- API validator push workflow #197: SUCCESS

Green CI therefore confirms consistency of the current implementation, not completion of the full-coverage campaign.

## Namespace matrix

| Namespace | API | SDK surface | Offline proxy | Physical SDK harness |
|---|---:|---:|---:|---:|
| account | 6 | 6 | 6 | 6 |
| aoc | 3 | 3 | 3 | 3 |
| cm | 21 | 17 | 17 | 17 |
| ddns | 2 | 1 | 1 | 1 |
| firewall | 26 | 26 | 26 | 13 |
| ota | 7 | 2 | 2 | 2 |
| package | 4 | 2 | 2 | 2 |
| phonebook | 11 | 11 | 11 | 11 |
| router | 27 | 23 | 23 | 22 |
| sim | 7 | 6 | 6 | 5 |
| sms | 9 | 7 | 7 | 6 |
| statistics | 11 | 11 | 11 | 8 |
| tr069 | 4 | 2 | 2 | 2 |
| util_wan | 3 | 3 | 3 | 3 |
| version | 2 | 2 | 2 | 1 |
| wireless | 14 | 14 | 13 | 11 |
| **Total** | **157** | **136** | **135** | **113** |

## Existing SDK helpers that still lack persisted physical SDK reach

These are the fastest coverage wins because an SDK implementation already exists.

### Firewall/NAT — 13 write methods

- `firewall/fw_edit_dmz_entry`
- `firewall/fw_set_disable_info`
- `firewall/fw_set_vpn_passthrough`
- `firewall/set_admin_from_wan`
- `firewall/set_ping_from_wan`
- `firewall/set_port_forward`
- `firewall/set_port_trigger`
- `firewall/set_url_filter`
- `firewall/ww_edit_ip_filter`
- `firewall/ww_edit_port_filter`
- `firewall/ww_fw_set_disable_info`
- `firewall/ww_fw_set_port_disable_info`
- `firewall/ww_upnp_open_close`

The API contracts are already live-verified and the SDK has helpers/unit coverage. What is missing is a committed physical SDK lifecycle suite with mutation/read-back/restore evidence.

### Other existing helpers — 10 methods

- `router/get_mac_info` — sanitize values; assert only shape/types.
- `sim/reset_pin_using_puk` — deliberate PIN-block/PUK recovery campaign required; never guess PUK.
- `sms/sms.query`
- `statistics/get_login_client_mac`
- `statistics/set_black_white_mode`
- `statistics/stat_clear_common_data`
- `version/get_magicnumber`
- `wireless/get_diag_wifi_info`
- `wireless/get_extender_config`
- `wireless/wifi_get_timed_off_status`

## API methods with no SDK surface — 21

### Deliberate hard exclusion

- `router/eng_set_usb_mode` — do not execute or expose a routine physical setter while USB is the recovery anchor.

### Non-excluded surface gaps — 20

#### CM / engineering / WAN
- `cm/eng_get_bands` — normal admin denied; engineering-authorization research required.
- `cm/eng_set_bands` — static contract only; engineering credential + request-contract research required.
- `cm/set_eng_mode` — static contract only; engineering credential + lifecycle research required.
- `cm/set_wan_settings` — live same-state evidence exists, but the complete request object is not normalized enough for a stable high-level helper.

#### DDNS
- `ddns/set_ddns` — frontend keys and live evidence exist, but token/custom-provider round-trip semantics remain incomplete; normalize API first.

#### OTA
- `ota/abandon_checked`
- `ota/abandon_download_update`
- `ota/clear_failed_state`
- `ota/download_update`
- `ota/manual_check_update`

These need a state-machine campaign. `download_update` is intentionally last-phase because a firmware install can change the tested firmware baseline and a factory reset does not downgrade firmware.

#### Package
- `package/set_package_data_used`
- `package/set_package_settings`

Both have live evidence but incomplete normalized request schemas. Complete the API contracts first, then add SDK setters and physical restore tests.

#### Router engineering / ADB
- `router/eng_check_adbd_status` — normal admin denied; authorized engineering path required.
- `router/eng_get_usb_mode` — read-only and eligible, but normal admin denied.
- `router/router_restart_adb` — source-confirmed `adbkey` request; credential/key semantics and recovery behavior require API research first.

#### SIM
- `sim/get_lock_info` — authenticated request returns HTTP 200 with an empty body on ACIY.3. The API must define the stable SDK behavior for this non-JSON response before a high-level helper is added.

#### SMS
- `sms/sms.get_cds` — current firmware returned a non-JSON response and remains `NOT_IMPLEMENTED`; deliberately recheck/sanitize the technical response.
- `sms/sms.get_config` — current firmware returned `Method not found`; a negative physical SDK disposition is appropriate unless firmware changes.

#### TR-069
- `tr069/set_config` — exact platform-compatible same-state request has live evidence, but a stable SDK setter is still missing.
- `tr069/set_xmpp_config` — frontend-typed same-state object returned `result=-1001`; resolve rejection semantics before helper promotion.

## API metadata drift found by the audit

### Administrator direct-IP login is not universally broken

The older 2026-08-31 A/B observation showed `192.168.1.1` returning `result=4` for administrator pre-auth while `zyxel.home` succeeded.

On 2026-09-21, however, `zyxel.home` did not resolve on the test PC. The campaign explicitly set:

`NR2301_URL=http://192.168.1.1`

The guarded static-DHCP cleanup and the complete destructive LAN/router lifecycle then both passed. Both scripts call `client.login()` before authenticated operations, so the successful run establishes that direct-IP administrator challenge/login can succeed on the same ACIY.3 device in a later runtime state.

Therefore the old observation is valid historical evidence but must not be documented as a permanent firmware rule or as proof that `zyxel.home` is the only usable administrator authority.

### Stale auth-evidence metadata

Several methods are marked `auth_evidence=UNTESTED` even though committed public-SDK physical tests use an authenticated normal-admin session and reach them. At minimum this applies to the VPN profile/control lifecycle and WAN operator scan. These metadata rows should be normalized upstream.

## Campaign order from this audit

1. **API metadata corrections** — direct-IP authentication scope + stale auth evidence.
2. **Safe read-only SDK omissions** — add sanitized physical tests for existing read helpers and negative endpoints.
3. **Firewall/NAT physical SDK lifecycle** — 13 existing write helpers, exact restore.
4. **Statistics write closure** — black/white mode and traffic-clear lifecycle.
5. **SIM PUK recovery** — only with known correct PUK and explicit retry-budget guards.
6. **API-first missing setters** — WAN settings, DDNS, Package, TR-069.
7. **Engineering/credential block** — engineering bands/mode, ADB status/restart, USB-mode read; no credential brute force and no USB-mode mutation.
8. **OTA state-machine block** — manual check/cancel/failure-state actions.
9. **OTA download/install last** — only after all ACIY.3-dependent work is captured, because firmware replacement may be irreversible by factory reset.

## Definition of full campaign completion

The campaign is complete when every method has one explicit disposition:

- physical SDK read/write/recovery test passed; or
- physically confirmed denied/rejected/not-applicable/not-implemented with the current authorized context; or
- the single hard exclusion `router/eng_set_usb_mode`.

For state-changing methods, a pass requires the strongest practical form of:

`snapshot → mutate/action → recover/re-authenticate → read-back → restore → verify restore`.

New protocol findings always update `nr2301-api` first; only then may the SDK implementation/test be considered final.
