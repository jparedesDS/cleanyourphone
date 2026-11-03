# Changelog

All notable changes to CleanYourPhone are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed

- Final logo system and palette: graphite `#121316` shared with CleanYourMail, purple `#A78BFA`,
  white `#F3F1EC` and a light purple `#C4B5FD` tint only for `ASK`. The sparkle is replaced by a
  contained return arrow, and the wordmark tints **Phone** in the logo purple. Primary, mark-only,
  monochrome, favicon and horizontal lockup assets are included. The brand rules are in
  `docs/BRAND.md`.

## [0.2.1] - 2026-11-02

### Added

- `restore --from-backup DIR`: if the undo journal is lost, compare the backup's pre-session
  disabled list with the phone, show the difference and require `--yes` before enabling anything.
  It refuses a backup from a different build or phone.
- Backups now record the Private DNS state, so a backup-based restore can put DNS back as well.

### Changed

- `SKILL.md` now has an explicit "If something breaks" section and distinguishes the backup
  baseline from the exact undo journal.
- `docs/RESTORE.md` and `docs/CLI.md` document the backup-based recovery path.
- `--version` now reports 0.2.1.

## [0.2.0] - 2026-11-02

### Added

- Installable CLI via `pyproject.toml`: `pipx install git+https://github.com/jparedesDS/cleanyourphone.git`
  adds the `cleanyourphone` command and the short alias `cyp`. `python -m cleanyourphone` works too.
- `wizard` command: detects the phone, chooses an exact profile, creates a backup, offers the tested
  `disable` list as one batch and asks for every user-facing package individually.
- `docs/CLI.md`: install, wizard, file locations, environment overrides and uninstall.
- CI job that builds and installs the wheel, then runs `cleanyourphone validate` from outside the repo.

### Changed

- `apply` and `wizard` share the same `apply_rows` batch, role-check, verification and rollback path.
- An installed CLI writes backups to `~/.cleanyourphone/backup` and battery reports to
  `~/.cleanyourphone/battery`; a source checkout keeps `backup/` and `battery/` at the repo root.
- Installed profiles are read from the package data in `share/cleanyourphone/profiles`; a source
  checkout keeps using `profiles/`.
- `--version` now reports 0.2.0.

## [0.1.1] - 2026-11-02

### Added

- Simulated-device test harness in `tests/test_simulation.py` and `docs/SIMULATION.md`: 8 scenarios
  plus a plan sweep over all 156 profiles. It checks plan/apply/verify/restore, the protected list,
  role holders, backup requirement, batch limits, managed phones and tablets without a real phone.
- The simulator records any unknown or dangerous ADB command (`pm uninstall`, `pm hide`, `pm clear`,
  `fastboot`, `reboot`) and fails the test if one appears.
- Catalog test in `tests/test_phone.py`: every profile codename must appear in its
  `fingerprint_regex` or a primary source, so a dead profile cannot pass CI again.
- GitHub Actions now runs the test suite on Python 3.14.

### Changed

- Stable, readable ids for the Redmi K20 Pro (global/India), Redmi Note 9 Pro (global/India) and
  Redmi 9T Android 10 variants.
- Added regional-model notes to Redmi 15C, Redmi Note 15 and Note 15 Pro.
- Corrected `redmi-9t-android-10` to the `lemon` codename (Redmi 9T NFC). The Android 12 profile
  `redmi-9t` remains `lime`.
- Corrected the `samsung-sm-m146b` source note from `essi` to `m14x`.
- Corrected stale catalog rows for `redmi-k20-pro` (`raphael`, not `raphaelin`) and
  `redmi-9t-android-10`.
- Localized READMEs now highlight their own language in the language selector.
- `--version` now reports 0.1.1.

### Removed

- `profiles/redmi/redmi-pad.json`: the profile claimed the `yunluo` codename but was built from the
  `mihal` firmware dump, so it could never match a real Redmi Pad. The catalog now has 156 profiles.

## [0.1.0] - 2026-10-30

The first public release.

### Added

- **The skill.** `SKILL.md`, `PROMPT.md` and `PROMPT.es.md` teach coding agents to identify an
  Android phone, back it up, review a package plan and disable preinstalled OEM packages over ADB.
- **The CLI.** `python tools/phone.py` with `doctor`, `probe`, `backup`, `list`, `roles`, `plan`,
  `apply`, `disable`, `enable`, `restore`, `verify`, `battery`, `dns`, `report`, `profiles`,
  `protected` and `validate`. Stdlib only.
- **Safety guardrails.** The protected list, role checks (dialer, SMS, Home, keyboard), backup
  requirement, five-package batches and the append-only undo journal.
- **157 profiles.** Google, Samsung, Xiaomi, Redmi, POCO and OnePlus, Android 8–16, including 11
  tablet profiles. Only four are `device`-tested; the rest are documented from primary firmware
  dumps and never auto-apply.
- **Bilingual website.** <https://jparedesds.github.io/cleanyourphone-web/> with a before/after demo,
  brand tabs, safety model, profile catalog and FAQ.
- **Documentation.** Safety, restore, battery, ROMs, FAQ, troubleshooting, profile rules, a
  model-by-model catalog in `docs/PROFILES.md` and localized README front pages in ten languages.
- **Repository automation.** Profile validation, a batch profile builder, catalog-consistency tests
  and GitHub Actions on Linux, macOS and Windows.

### Safety

- Disable, never uninstall. The only state change is `pm disable-user --user 0`; `pm enable` is the
  undo.
- No root, bootloader unlock, custom ROM, Magisk, Shizuku or flashing.
- No telemetry, account, analytics or third-party API.
- No package from the protected list in `disable` or `ask`; no dialer, SMS, Home or keyboard role
  holder is disabled.
- A documented profile never auto-applies, has no `disable` list and asks for every package.

[0.2.1]: https://github.com/jparedesDS/cleanyourphone/releases/tag/v0.2.1
[0.2.0]: https://github.com/jparedesDS/cleanyourphone/releases/tag/v0.2.0
[0.1.1]: https://github.com/jparedesDS/cleanyourphone/releases/tag/v0.1.1
[0.1.0]: https://github.com/jparedesDS/cleanyourphone/releases/tag/v0.1.0
