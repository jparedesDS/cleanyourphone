# AGENTS.md

Instructions for coding agents working **on this repository**. If you are here to clean a phone,
stop: read [SKILL.md](SKILL.md) or [PROMPT.md](PROMPT.md) and follow those instead. This file is for
changing the repo.

## What this project is

CleanYourPhone is a **skill**, not an app. People give `SKILL.md` to their coding agent; the agent
uses ADB to disable preinstalled Android packages with `pm disable-user --user 0`, optionally sets
Private DNS, verifies the phone, and can undo everything. There is no APK, no root, no uninstall,
no custom ROM, and no background service.

The product is the text in `SKILL.md` plus the guardrails in `tools/`. A change that makes the skill
longer without making it safer or clearer is probably a bad change.

## Repo map

| Path | What it is |
|---|---|
| `SKILL.md` | The skill. Agent-agnostic procedure and safety rules. |
| `PROMPT.md`, `PROMPT.es.md` | The short prompt people paste into an agent that does not support skills, in English and Spanish. |
| `README.md`, `README.es.md` | Front page and Spanish translation. |
| `tools/phone.py` | Cross-platform ADB CLI: `doctor`, `probe`, `backup`, `list`, `roles`, `plan`, `apply`, `disable`, `enable`, `restore`, `verify`, `battery`, `dns`, `report`, `profiles`, `protected`, `validate`. Stdlib only. |
| `tools/protected.py` | The packages that must never be disabled, with a reason for each. Imported by the CLI and the tests. |
| `profiles/` | One JSON file per tested model/firmware. `disable`, `ask`, `never`. |
| `docs/` | `SAFETY.md`, `RESTORE.md`, `BATTERY.md`, `ROMS.md`, `FAQ.md`, `TROUBLESHOOTING.md`. |
| `tests/` | Python `unittest` suite for the pure logic: protected list, role conflicts, profile matching, command building. |
| `backup/` | Created at runtime. Never commit it. It contains the person's package list and settings. |

## Hard rules

Never do these in a PR or in a profile:

- **No uninstall.** No `pm uninstall`, `pm uninstall --user 0`, `pm hide`, `pm block`, `pm clear`.
  The only state change is `pm disable-user --user 0` and its undo `pm enable`.
- **No root, no ROM, no bootloader unlock, no flashing, no Magisk, no Shizuku requirement.**
  `docs/ROMS.md` may explain the options; the skill must not execute them.
- **No package on the protected list.** `tools/protected.py` is the source of truth. Do not add an
  override flag, an `--i-know-what-i-am-doing`, or a "but this one is safe" exception.
- **No role-breaking change.** A profile may not disable the current dialer, SMS app, HOME app or
  IME. The CLI checks this; keep the check.
- **No secrets or identifiers** in profiles, docs, tests or screenshots: no serial numbers, IMEI,
  Android ID, MAC addresses, Wi-Fi names, account emails, phone numbers, IP addresses, ADB keys.
- **No prebuilt binaries or APKs** in the repo. Everything is source.
- **No telemetry, analytics or network calls** in `tools/phone.py`. It talks to `adb` and nothing
  else. Do not add a dependency that phones home.
- **No "double battery" claims.** `docs/BATTERY.md` sets the measurement method and the realistic
  range. A profile note may say "tested", not "miraculous".
- **No advice that bypasses Play Integrity, banking checks or app protection.** `docs/ROMS.md` can
  explain the trade-off; it must not provide a bypass recipe.
- **No changes to the safety rules in `SKILL.md`** without an issue and a maintainer review. Those
  rules are the product.

## Profiles

A profile is a claim that a package list was tested on a real model and firmware. Do not invent one.

Required fields: `id`, `brand`, `model`, `android`, `fingerprint_regex`, `tested`, `disable`, `ask`,
`never`, `notes`. See `profiles/README.md` and `profiles/schema.json`.

- `disable` entries must say **why** and **what breaks**.
- `ask` entries are the default for anything user-facing or dependency-heavy.
- `never` entries are per-model additions to the global protected list, not replacements.
- A profile that disables a role holder is invalid.
- If a package is region- or carrier-specific, say so in `notes`; do not put it in `disable`.
- A profile is versioned by fingerprint, not by marketing name. An OTA can change package names.
- Auto-apply requires the phone build to appear in `tested`. On any other build, use `plan` and
  `disable` one package at a time. `auto_apply: false` marks a family/reference profile.

## Tests

```bash
python -m unittest discover -s tests -v
```

The suite must pass on Windows, macOS and Linux. It must not need a phone or a real `adb`; use the
fixtures in `tests/`. Add a test for every new guard, parser or profile rule.

Also run, without a phone:

```bash
python tools/phone.py --help
python tools/phone.py protected
python tools/phone.py profiles
python tools/phone.py validate
```

`plan`, `doctor`, `probe` and everything that changes the phone need a connected device. They must
fail with a clear message and exit code 2 when there is none.

## Commit and PR style

- Titles: `area: what changed`, e.g. `profiles: add Samsung SM-S918B (One UI 7)`,
  `tools: refuse to disable a role holder`, `docs: explain the Private DNS undo`.
- The body says what changed, the model/Android version it was tested on, and the command used.
- One topic per PR. A profile and a tool fix for that same model can be one PR.
- Contributions are MIT.

## Where to ask

Open a GitHub Discussion for questions. Open an issue before changing `SKILL.md` safety rules, the
protected list, or the role checks. Security problems go privately, per `SECURITY.md`.
