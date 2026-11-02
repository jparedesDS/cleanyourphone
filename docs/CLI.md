# CleanYourPhone CLI

`tools/phone.py` is the guardrail CLI. It talks to `adb`, never uninstalls a package, and can undo
every change. It has no third-party dependencies: Python 3.10+ and Android Platform-Tools are enough.

There are three ways to run it:

```bash
# Inside a clone (always works)
python tools/phone.py doctor

# Installed as a command
cleanyourphone doctor
cyp doctor

# Installed as a module
python -m cleanyourphone doctor
```

## Install the command

With [pipx](https://pipx.pypa.io/), from a clone or directly from GitHub:

```bash
pipx install git+https://github.com/jparedesDS/cleanyourphone.git
cleanyourphone --version
```

Each GitHub release also attaches a wheel and an sdist. Install a pinned wheel with:

```bash
pipx install ./cleanyourphone-X.Y.Z-py3-none-any.whl
```

For development, install the checkout in editable mode:

```bash
python -m venv .venv
. .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -e .
cleanyourphone --version
```

The package installs two identical entry points: `cleanyourphone` and the short alias `cyp`.

## Where files live

| What | Source checkout | Installed command |
|---|---|---|
| Profiles | `profiles/` | `share/cleanyourphone/profiles/` inside the environment |
| Backups | `backup/` at the repo root | `~/.cleanyourphone/backup/` |
| Undo journal | `~/.cleanyourphone/` | `~/.cleanyourphone/` |
| Battery reports | `battery/` at the repo root | `~/.cleanyourphone/battery/` |

Override them with environment variables:

- `CLEANYOURPHONE_PROFILES`: profile directory.
- `CLEANYOURPHONE_BACKUP`: backup directory.
- `CLEANYOURPHONE_STATE`: undo-journal directory.
- `CLEANYOURPHONE_BATTERY`: battery-report directory.

## Commands

| Command | What it does |
|---|---|
| `doctor` | Checks ADB, the phone, the backup and exact profile matches. |
| `probe` | Prints model, Android, fingerprint, roles and profile matches. |
| `backup` | Saves package lists, roles, settings, IME, device policy and a redacted `getprop`. |
| `plan --profile ID` | Shows `DISABLE`, `ASK`, `BLOCKED`, `SKIP` and `MISSING` rows without changing anything. |
| `apply --profile ID --yes` | Applies a tested device profile's `disable` list in batches of five. |
| `wizard` | Guided flow: detect, choose profile, back up, review every package, then apply. |
| `disable PKG...` | Disables up to five reviewed packages. |
| `enable PKG...` | Re-enables packages. |
| `restore` | Re-enables everything this tool disabled and restores Private DNS. |
| `verify` | Checks dialer, SMS, Home, keyboard, Play and protected packages. |
| `battery`, `dns`, `report` | Measurement and reporting helpers. |
| `profiles`, `protected`, `validate` | Catalog, protected list and profile validation. |

Run `cleanyourphone --help` or `cleanyourphone <command> --help` for the full list.

## The wizard

```bash
cleanyourphone wizard
```

The wizard:

1. Refuses TVs, managed phones, multi-user phones and Android older than 8.
2. Finds exact profile matches and lets you choose when there is more than one.
3. Creates a backup before it shows any package.
4. Offers the tested `disable` list as one low-risk batch only when the build is in `tested`.
5. Asks for every user-facing package one by one, with `why` and `breaks`.
6. Re-checks role holders before every batch, verifies after each batch and rolls the batch back if
   verification fails.
7. Never uninstalls, never uses root and never touches the protected list.

On a documented profile, or on a device build that is not in `tested`, the wizard asks for every
package individually. It never turns an untested build into an automatic apply.

## Safety

The CLI keeps the rules in [SKILL.md](../SKILL.md):

- The only state change is `pm disable-user --user 0`; the undo is `pm enable`.
- No uninstall, root, ROM, bootloader unlock, Magisk or Shizuku.
- Back up before the first change.
- Refuse protected packages and current dialer, SMS, Home or keyboard holders.
- Five packages per batch, then verify.
- `apply` only runs for a `device` profile whose build is listed in `tested`.

`wizard` uses the same `apply_rows` function as `apply`, so both paths share the batch, verification
and rollback rules.

## Remove the command

```bash
pipx uninstall cleanyourphone
```

Uninstalling the CLI does not re-enable anything on the phone. Run `cleanyourphone restore` first if
you want to undo the last session.
