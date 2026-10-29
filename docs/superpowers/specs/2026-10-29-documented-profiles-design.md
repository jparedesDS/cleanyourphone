# Documented profiles: design

Date: 2026-10-29

## Goal

Add model profiles from primary firmware/documentation sources without pretending they were tested
on a physical phone. Documented profiles must be useful for planning and asking, but must never
auto-apply.

## Verification levels

Every profile declares `verification`:

- `device`: tested on a real phone. Only this level can set `auto_apply: true`, and `tested` must
  contain at least one real test.
- `documented`: built from a firmware dump or primary OEM documentation. `tested` is empty,
  `disable` is empty, `auto_apply` is false, and at least one `sources` entry is required.
- `reference`: the generic profile. `generic: true`, no `disable`, no `tested`, no auto-apply.

If `verification` is missing, infer `reference` for `generic: true`, otherwise `device` when `tested`
is non-empty, otherwise `documented`.

## Sources

```json
"sources": [
  {
    "title": "Android Dumps: samsung/pa3q",
    "url": "https://gitlab.com/Android-Dumps/samsung/pa3q",
    "retrieved": "2026-10-29",
    "note": "Firmware dump: README, build.prop, all_files.txt, permission XMLs"
  }
]
```

Sources must be `http(s)` URLs. No local paths, no identifiers.

## Documented profile rules

- `disable` must be empty.
- `ask` is the only package list that may contain candidates.
- Every listed package must appear in the firmware dump: `all_files.txt`, a permission XML, or an
  APK path.
- `never` is the global protected list plus model/brand core packages.
- `auto_apply` must be false.
- `tested` must be empty.
- `sources` must contain the dump and the specific evidence used.

## Data flow

1. Locate a dump in Android Dumps (GitLab).
2. Extract `README.md`, `build.prop`, `all_files.txt` and permission XMLs.
3. Extract model, codename, fingerprint, Android version, build.
4. Extract package IDs from permission XML filenames and contents.
5. Cross-check with `protected.py`.
6. Curate `ask` entries manually with `why` and `breaks`.
7. Validate with `phone.py validate`.
8. Review the diff and commit.

## Tooling

`scripts/dump_inventory.py` is a maintainer-only, stdlib-only helper. It fetches the dump metadata
and candidate package IDs, then writes an inventory report and a draft profile. It is not imported by
the runtime CLI and makes no network calls during `phone.py` execution.

## CLI behavior

- `profiles` shows the verification level.
- `plan` labels documented profiles as not auto-applicable.
- `apply` refuses documented/reference profiles with an explicit message.
- `doctor` and `probe` list documented profiles separately from auto-applicable device profiles.

## Testing

- Validation accepts a device profile with `tested`.
- Validation rejects documented profiles with `disable`, `tested`, `auto_apply: true`, or no sources.
- Validation accepts documented profiles with `ask`, `never`, sources and no `disable`.
- `build_matches` returns false for documented/reference.
- `apply` refuses documented profiles.
- Inventory parsing is unit-tested with fixtures; no network in tests.
