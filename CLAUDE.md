# CLAUDE.md

Fast entry point for Claude Code. `AGENTS.md` is the canonical maintainer handbook; if this file and
`AGENTS.md` disagree, `AGENTS.md` wins.

## What this project is

CleanYourPhone is a **skill**, not an app. A person gives `SKILL.md` to a coding agent; the agent uses
ADB to disable preinstalled Android packages with `pm disable-user --user 0`, optionally sets Private
DNS, verifies the phone, and can undo everything. There is no APK, root, uninstall, custom ROM or
background service.

The product is the text in `SKILL.md` plus the guardrails in `tools/`. A change that makes the skill
longer without making it safer or clearer is probably the wrong change.

## If you are here to clean a phone

Stop. Read `SKILL.md` or `PROMPT.md` and follow those instructions. This file is for changing the
repository.

## Non-negotiables

- Never uninstall: no `pm uninstall`, `pm hide`, `pm block`, `pm clear`.
- No root, ROM, bootloader unlock, flashing, Magisk or Shizuku.
- Never disable a package in `tools/protected.py`, or the current dialer, SMS, Home or keyboard.
- Back up before the first change.
- At most five packages per batch, then verify.
- No secrets or personal identifiers in profiles, docs, tests or screenshots.
- No telemetry, analytics, network calls or third-party runtime dependencies in `tools/`.
- Do not weaken the safety rules in `SKILL.md` without an issue and maintainer review.

## Repo map

| Path | What it is |
|---|---|
| `SKILL.md` | The product: agent-agnostic procedure and safety rules. |
| `PROMPT.md`, `PROMPT.es.md` | Short prompts for agents that do not load skills. |
| `README.md`, `README.es.md` | Front page and Spanish translation. |
| `tools/phone.py` | The CLI: `doctor`, `probe`, `backup`, `list`, `roles`, `plan`, `apply`, `wizard`, `disable`, `enable`, `restore`, `verify`, `battery`, `dns`, `report`, `profiles`, `protected`, `validate`. |
| `tools/protected.py` | Packages that must never be disabled. Source of truth. |
| `profiles/` | One JSON file per model/firmware. |
| `tests/` | Stdlib `unittest` suite. No phone or real `adb` needed. |
| `docs/` | Safety, restore, battery, ROMs, FAQ, troubleshooting, CLI and simulation notes. |
| `scripts/` | Maintainer helpers only; not used at runtime. |
| `pyproject.toml` | Installs the CLI as `cleanyourphone` and `cyp`. Source stays in `tools/`. |

## Commands

```bash
python -m unittest discover -s tests -v
python tools/phone.py validate
python tools/phone.py --help
python tools/phone.py protected
python tools/phone.py profiles
python tools/phone.py wizard --help
```

Packaging check:

```bash
python -m pip install -e .
cleanyourphone --version
```

`plan`, `doctor`, `probe` and every command that changes the phone need a connected device. Without
one they must fail with a clear message and exit code 2.

## Profiles

- `verification: device` means tested on a real model and firmware. Only `device` profiles may have a
  `disable` list and auto-apply.
- `verification: documented` comes from a primary firmware dump. It must have `tested: []`,
  `disable: []`, `auto_apply: false`, a non-empty `ask` list and at least one primary source. Every
  `ask` package must exist in the dump.
- `verification: reference` is reserved for the generic profile: `generic: true`, no `disable`, no
  `tested`.
- Required fields: `id`, `brand`, `model`, `android`, `fingerprint_regex`, `tested`, `disable`, `ask`,
  `never`, `notes`, plus `verification`.
- A profile is versioned by fingerprint, not by marketing name. An OTA can change package names.
- Every `codename` must appear in `fingerprint_regex` or in a primary source; the catalog test
  enforces this.
- Use `scripts/dump_inventory.py` to draft a profile, then curate every `why` and `breaks` by hand.
- Never invent a `device` profile or promote a simulated profile to `device`.

## Code and tests

- `tools/` is stdlib only. Do not add a runtime dependency.
- The suite must pass on Windows, macOS and Linux.
- Add a test for every new guard, parser or profile rule.
- `tests/test_simulation.py` uses a fake ADB transport. It proves behaviour, not a real phone.
- After changing profiles, keep `profiles/README.md` and `docs/PROFILES.md` in sync with
  `python scripts/update_profile_docs.py`.
- `apply` and `wizard` share `apply_rows`; keep the batch, role-check, verification and rollback path
  in one place.

## CLI packaging

- The import package is `cleanyourphone`, mapped to the `tools/` directory by `pyproject.toml`.
  Do not duplicate the modules or move them without updating the package mapping, tests and docs.
- A source checkout reads `profiles/`, writes `backup/` and `battery/` at the repo root.
- An installed CLI reads package data from `share/cleanyourphone/profiles` and writes backups to
  `~/.cleanyourphone/backup`.
- Keep `python tools/phone.py` working; it is the documented repo-local form.
- `wizard` is interactive and must never auto-apply a documented profile or an untested build.

## Style

- Commit titles: `area: what changed`, for example `profiles: add Samsung SM-S918B` or
  `tools: refuse to disable a role holder`.
- One topic per PR. Say what changed, the model/Android version tested, and the command used.
- English is the default for code and docs. `README.es.md` and `PROMPT.es.md` are the Spanish entry
  points.
- Contributions are MIT.

## Read next

- `AGENTS.md` — full maintainer rules, hard rules and PR style.
- `SKILL.md` — the product and the safety procedure.
- `profiles/README.md` — profile policy and the device-test checklist.
- `docs/CLI.md` — install, wizard, file locations and uninstall.
- `docs/SAFETY.md` — the safety model in detail.
