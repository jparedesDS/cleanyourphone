# Changelog

All notable changes to CleanYourPhone are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses
[Semantic Versioning](https://semver.org/).

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

[0.1.0]: https://github.com/jparedesDS/cleanyourphone/releases/tag/v0.1.0
