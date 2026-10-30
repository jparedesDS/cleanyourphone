# Maintainer scripts

These scripts are for people adding or reviewing profiles. They are **not** used by the skill at
runtime and they are not imported by `tools/phone.py`. They may make network requests to read public
firmware metadata.

## `collect_device.ps1` (Windows, local PC)

Use this on the PC that is physically connected to the phone, not on a remote shell.

```powershell
powershell -ExecutionPolicy Bypass -File .\collect_device.ps1
```

It downloads Platform-Tools to `%TEMP%` if needed, reads the model/build/fingerprint, package lists,
roles, IME and user list, and writes a ZIP with no serial, IMEI or MAC. It never changes the phone.
Run it locally when the phone is connected by USB and USB debugging is authorized.

## `discover_projects.py`

Caches the Android-Dumps project list used by the batch builder:

```bash
python scripts/discover_projects.py
```

It writes `work/cache/discovery/<brand>.json` for Samsung, Xiaomi, Redmi, POCO and OnePlus. The
OnePlus list also includes `noescape-firmware-dumps/ONEPLUS`; generic `ossi` system images there are
skipped unless the build is device-specific. Set `GITLAB_TOKEN` to avoid the anonymous API rate
limit.

## `batch_profiles.py`

Builds documented profiles in bulk from the cached project lists:

```bash
python scripts/batch_profiles.py --min 14 --max 16 --dry-run
python scripts/batch_profiles.py --min 14 --max 16 --write
python scripts/batch_profiles.py --tablets --min 8 --max 16 --write
```

It clones the selected stock branches into `work/batch/dumps`, runs `dump_inventory.py` and writes
one profile per device to `profiles/`. Model names come from the public
[MobileModels](https://github.com/KHwang9883/MobileModels) tables, downloaded on demand into
`work/cache/models`. The curated `ask`/`never` catalog is `scripts/profile_catalog.json`.

The script skips custom ROMs, tablets unless `--tablets` is set, duplicate model numbers and
marketing names, and dumps whose package inventory does not match the catalog. A low-`ask` result is
a signal to curate the dump by hand, not to publish it.

## `update_profile_docs.py`

Rebuilds the profile tables in `README.md`, `README.es.md` and `profiles/README.md`, plus the file
tree in `profiles/README.md`:

```bash
python scripts/update_profile_docs.py
```

Existing rows keep their hand-written notes; new profiles are inserted in brand order.

## `report_profiles.py`

Reports coverage and curation flags: brand counts, thin `ask` lists, profiles without a marketing
name, `model: "*"` profiles and duplicate model/marketing groups.

```bash
python scripts/report_profiles.py
```

## `dump_inventory.py`

Builds a documented-profile draft from an Android Dumps repository.

```bash
python scripts/dump_inventory.py \
  --project Android-Dumps/samsung/pa3q \
  --marketing-name "Galaxy S25 Ultra" \
  --out work/pa3q
```

It writes:

- `work/pa3q/inventory.json`: dump metadata, build props, and package candidates with the evidence
  path for each one.
- `work/pa3q/draft-profile.json`: a draft with `verification: "documented"`, `auto_apply: false`,
  `tested: []`, `disable: []` and an empty `ask` list.

Downloads are cached under `work/cache`. If GitLab returns HTTP 429, wait a minute, set
`GITLAB_TOKEN` to a personal access token, or reuse the cache with `--cache-dir`.

To avoid the API entirely, use a sparse local clone:

```bash
git clone --depth 1 --filter=blob:none --sparse \
  https://gitlab.com/Android-Dumps/oneplus/OP5961L1.git work/dumps/op5961
cd work/dumps/op5961
git sparse-checkout set --no-cone README.md all_files.txt vendor/build.prop \
  system/system/build.prop product/etc/build.prop system_ext/etc/build.prop odm/etc/build.prop
```

Then run the inventory against the local directory:

```bash
python scripts/dump_inventory.py \
  --project Android-Dumps/oneplus/OP5961L1 \
  --local-dir work/dumps/op5961 \
  --model CPH2487 \
  --marketing-name "OnePlus 11R 5G" \
  --out work/op5961
```

`--model` is required when the dump's build.prop uses a generic product name (`ossi`, `qssi`) and
the real model only appears in the dump's README fingerprint.

The draft is intentionally incomplete. Curate `ask` by hand, copy the file to
`profiles/<brand>/<id>.json`, remove the `_draft` block, and run:

```bash
python tools/phone.py validate
```

Do not commit a documented profile until every `ask` entry has a real `why` and `breaks` text and
every package appears in the dump inventory. Documented profiles are never auto-applied.
