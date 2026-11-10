<p align="center">
  <a href="https://jparedesds.github.io/cleanyourphone-web/">
    <img src="assets/banner.png" alt="CleanYourPhone — your phone, minus the bloat" width="100%">
  </a>
</p>

<p align="center">
  <b>English</b> ·
  <a href="README.es.md">Español</a> ·
  <a href="README.pt-BR.md">Português (BR)</a> ·
  <a href="README.fr.md">Français</a> ·
  <a href="README.de.md">Deutsch</a> ·
  <a href="README.it.md">Italiano</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <a href="https://github.com/jparedesDS/cleanyourphone/actions/workflows/ci.yml"><img src="https://github.com/jparedesDS/cleanyourphone/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/license-MIT-a78bfa?labelColor=121316" alt="MIT">
  <img src="https://img.shields.io/badge/python-3.10%2B-a78bfa?labelColor=121316" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/telemetry-none-a78bfa?labelColor=121316" alt="No telemetry">
  <img src="https://img.shields.io/badge/profiles-156-a78bfa?labelColor=121316" alt="156 profiles">
  <a href="https://github.com/jparedesDS/cleanyourphone/releases"><img src="https://img.shields.io/github/v/release/jparedesDS/cleanyourphone?color=a78bfa&labelColor=121316" alt="release"></a>
  <a href="https://github.com/jparedesDS/cleanyourphone-app/releases"><img src="https://img.shields.io/github/v/release/jparedesDS/cleanyourphone-app?color=a78bfa&label=app&labelColor=121316" alt="app release"></a>
</p>

# CleanYourPhone

**Your phone, minus the bloat.** An open-source, reversible debloat skill for Android, built for
coding agents. It disables preinstalled apps and services over ADB: no root, no custom ROM, nothing
uninstalled, and one command to restore the changes the CLI recorded.

Read the story and the safety model at
**[jparedesds.github.io/cleanyourphone-web](https://jparedesds.github.io/cleanyourphone-web/)**.

There is also an optional **Windows app** for people who prefer buttons over prompts:
**[Download the Early MVP](https://github.com/jparedesDS/cleanyourphone-app/releases/latest)**. It is a
GUI over the same CLI. The skill remains the main product and the path for phones without a profile.

It is the phone version of [cleanyour.tv](https://cleanyour.tv), built the same way: one prompt, one
command, reversible, open source, and the person stays in control.

[SKILL.md](SKILL.md) · [PROMPT.md](PROMPT.md) · [App](https://github.com/jparedesDS/cleanyourphone-app) · [Safety](docs/SAFETY.md) · [156 profiles](docs/PROFILES.md) · [Feedback](docs/FEEDBACK.md) · [Changelog](CHANGELOG.md)

## Start here

| You have | Start with |
|---|---|
| A phone and a coding agent | The quick start below. |
| Prefer buttons over prompts | [Download the Windows app](https://github.com/jparedesDS/cleanyourphone-app/releases/latest) (Early MVP). |
| Want to see it first | [The website](https://jparedesds.github.io/cleanyourphone-web/). |
| Need the safety rules | [docs/SAFETY.md](docs/SAFETY.md). |
| Need a model profile | [Browse the 156 profiles](profiles/README.md). |
| Your phone is not listed | Use the skill manually, or send a [profile request](docs/FEEDBACK.md). |
| Prefer a terminal | [Install the CLI](docs/CLI.md). |

| Part | Status |
|---|---|
| **Skill** | Main product, in this repository. |
| **CLI** | `0.3.2`, published on PyPI as `cleanyourphone` / `cyp`. |
| **Windows app** | `0.2.0` Early MVP, optional, unsigned. |
| **Website** | 10 languages at [jparedesds.github.io/cleanyourphone-web](https://jparedesds.github.io/cleanyourphone-web/). |
| **Feedback** | Optional web/app/skill form to Discord; no automatic telemetry. |

---

## Why the skill comes first

An app that disables other apps needs root, Shizuku or device-owner privileges. That is a lot of
power and a lot of risk for something a shell command can do. A skill is just text: the person's
agent reads it, runs `adb`, shows a plan, and asks before touching anything. There is nothing to
install on the phone, nothing running in the background, and nothing that phones home.

There is now an optional Windows app, but it does not replace the skill. It is a GUI over the same
CLI, and it only continues when it can match an exact `device` profile with a tested build, or a
`documented` profile after an explicit acknowledgement and one package per batch. If it cannot match
the phone, it stops and sends the person here. The skill can still inspect the package list, ask
about each app and continue manually.

The phone is a daily driver, so the skill is deliberately conservative:

- **Disable, never uninstall.** `pm disable-user --user 0` only. `pm enable` is the undo.
- **Back up first.** Package lists, settings, roles, IMEs and `getprop` before the first change.
- **Protected list.** Core Android, telephony, Play Services, WebView, permission controller,
  emergency alerts, IME/telecom, NFC/SE and OEM security packages are refused by the CLI.
- **Role checks.** It will not leave you without a dialer, SMS app, Home app or keyboard.
- **Small batches.** Five packages at a time, verify, then continue.
- **Ask first.** Banking, payments, WhatsApp, camera, alarm, VPN, authenticator, smartwatch, eSIM,
  VoLTE/Wi-Fi calling and work apps are a checklist, not a default.

## How it works

1. **On the phone:** enable Developer options and USB debugging. Connect it by USB.
2. **On the computer:** give your agent `SKILL.md` (or paste `PROMPT.md`).
3. **Follow along:** the agent identifies the phone, backs up, shows a table of packages, asks what
   you use, disables in batches, reboots and verifies. `python tools/phone.py restore` undoes it.

```text
$ python tools/phone.py doctor
ADB ......... C:\platform-tools\adb.exe
ADB version . Android Debug Bridge version 1.0.41
Devices ..... <serial> (device)

Device ...... Google Pixel 8 (shiba)
Android ..... 16 (SDK 36)
Managed ..... no
Users ....... 1
Battery ..... 82%
Backup ...... none (run: python tools/phone.py backup)
Profiles .... google-pixel-8
Auto-apply .. google-pixel-8

$ python tools/phone.py plan --profile google-pixel-8
Profile: google-pixel-8 (Google Pixel 8)
Phone:   Google Pixel 8 (shiba), Android 16
Match:   yes
Auto-apply: yes

DISABLE  com.google.android.apps.wellbeing
         why: Digital Wellbeing: screen-time tracking and telemetry
         breaks: Screen-time dashboard and app timers
ASK      com.google.android.apps.turbo
         why: Adaptive Battery and Device Health
         breaks: Adaptive Battery, battery diagnostics
```

## The optional Windows app

For people who prefer buttons, the app wraps the same CLI in a guided Windows flow: connect, check,
backup, review, apply, verify and undo.

<p align="center">
  <a href="https://github.com/jparedesDS/cleanyourphone-app/releases/latest">
    <img src="assets/app-review.png" alt="CleanYourPhone app review screen with a documented profile warning and one selected app" width="760">
  </a>
</p>

- **Connect by Wi-Fi or USB.** The app finds the phone, checks the build and shows the exact profile.
- **Exact `device` profiles** follow the tested path. **`documented` profiles** are manual: visible
  warning, explicit acknowledgement and one app per batch. No profile means stop and use the skill.
- **Backup is mandatory.** Review every package, apply in batches, verify and undo the whole journal.
- **Optional extras:** Private DNS ad blocking (not YouTube) and a local before/after benchmark.
- **Optional feedback:** an editable checklist can be sent to the maintainer after consent. No
  automatic telemetry.
- **No root, no uninstall, no app installed on the phone.** The installer is unsigned; verify the
  SHA-256 before running it.

[Download `v0.2.0`](https://github.com/jparedesDS/cleanyourphone-app/releases/latest) ·
[Source](https://github.com/jparedesDS/cleanyourphone-app) ·
[Connection guide](docs/CONNECT.md).

## Quick start

### 1. Install ADB

Download [Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools)
for Windows, macOS or Linux, unzip it, and add it to `PATH`. Check with:

```bash
adb version
```

### 2. Prepare the phone

Settings → About phone → tap **Build number** 7 times → back → **Developer options** → turn on
**USB debugging**. Connect the phone by USB and accept the **Allow USB debugging?** prompt. Keep the
phone unlocked and above 30% battery.

Android 11 and newer can use **Wireless debugging** instead: turn it on, tap the words (not only the
switch), choose **Pair device with pairing code**, and keep that dialog open. The pairing dialog has
its own port; it is not the connection port on the main screen. See
[docs/CONNECT.md](docs/CONNECT.md) for the first-time walkthrough and the common fixes.

### 3. Clone and check

```bash
git clone https://github.com/jparedesDS/cleanyourphone
cd cleanyourphone
python tools/phone.py doctor
```

The CLI is optional. `SKILL.md` contains the raw `adb` commands too, so an agent can work without
Python. The CLI exists so the agent does not improvise the guardrails.

Prefer a terminal? Install the command with [pipx](https://pipx.pypa.io/):

```bash
pipx install cleanyourphone
cleanyourphone doctor
```

This adds `cleanyourphone` and the short alias `cyp`. [docs/CLI.md](docs/CLI.md) covers the wizard,
the installed file locations and the safety rules. `python tools/phone.py` keeps working.

### 4. Give the skill to your agent

| Agent | Where to put it |
|---|---|
| **Claude Code** | `~/.claude/skills/cleanyourphone/SKILL.md` (personal) or `.claude/skills/cleanyourphone/SKILL.md` (project) |
| **OpenCode** | `~/.config/opencode/skills/cleanyourphone/SKILL.md` (global) or `.opencode/skills/cleanyourphone/SKILL.md` (project) |
| **Codex** | `AGENTS.md` in the project, or `~/.codex/AGENTS.md`; paste `PROMPT.md` if your build does not load skills |
| **Cursor** | `.cursor/rules/cleanyourphone.mdc` with the contents of `SKILL.md` |
| **Gemini CLI** | `GEMINI.md` in the project |
| **Any chat agent** | Paste `PROMPT.md`, then paste `SKILL.md` when it asks |

Spanish prompt: [PROMPT.es.md](PROMPT.es.md). The skill answers in the language the person writes in.

The simplest setup is to clone the repo and open your agent in that folder: `SKILL.md` is already at
the root, so `python tools/phone.py` works. If your agent loads skills from a global folder, copy
`SKILL.md` there; install the CLI with pipx (above) and you do not need to keep the repo cloned:

```bash
mkdir -p ~/.claude/skills/cleanyourphone
cp SKILL.md ~/.claude/skills/cleanyourphone/SKILL.md
```

Without the repo, the skill still works: it includes the raw `adb` commands and tells the agent to
use them.

Then ask: **"Clean my phone"** or **"Use cleanyourphone on my Pixel"**.

## What it does

- Disables OEM telemetry, ad surfaces, recommendation rows, duplicate browsers/stores and unused
  preloads.
- Optionally sets Private DNS with presets (`adguard`, `adguard-family`, `controld`, `mullvad`) or
  your own resolver, and checks whether ads are actually blocked. Not a YouTube ad blocker; see
  [docs/ADS.md](docs/ADS.md).
- Produces a report: what changed, why, what was kept, the backup path and the undo command.
- Treats `documented` profiles as manual evidence: no `disable` list, no auto-apply, one package at
  a time after review.
- Offers an optional Windows GUI for the same flow (`device` profiles automatic, `documented`
  manual, everything else stops and links here).
- Measures free RAM, processes and package counts before/after with `bench snapshot` and
  `bench compare`; approximate, local and not causal. See [docs/BENCH.md](docs/BENCH.md).
- Measures a battery baseline before/after (`docs/BATTERY.md`), without promising miracles.

## Feedback and profile requests

If a phone is not covered, the person can ask for a profile or report a bug without sharing a serial
number, IP address, IMEI or MAC address:

- **Web:** [cleanyourphone feedback form](https://jparedesds.github.io/cleanyourphone-web/#feedback).
- **App:** **Feedback** in the header; the checklist is prefilled and editable.
- **Skill:** `python scripts/feedback.py --kind profile --checklist-file feedback.txt` previews the
  payload; add `--yes` only after the person approves.

The message goes to a Cloudflare Worker and then to the maintainer's Discord. Nothing is sent at
startup or during a scan. The app/website use the same Worker; `tools/phone.py` stays network-free.
See [docs/FEEDBACK.md](docs/FEEDBACK.md) for the payload, redaction and rate limit.

## Block ads (optional)

Private DNS can block many in-app ad and tracker domains. It is not a YouTube blocker, not a VPN, and
it can break captive portals. The presets are:

```bash
python tools/phone.py dns providers
python tools/phone.py dns set adguard
python tools/phone.py dns check
python tools/phone.py dns restore
```

`dns check` distinguishes “blocked” from “cannot test” when the control domain does not resolve. See
[docs/ADS.md](docs/ADS.md) for the OEM ad-switch checklist and caveats.

## Measure the result

Record a local before/after snapshot; no serial or fingerprint is stored:

```bash
python tools/phone.py bench snapshot --label before
# apply, reboot and verify
python tools/phone.py bench snapshot --label after
python tools/phone.py bench compare <before.json> <after.json>
```

The comparison is approximate and not causal. See [docs/BENCH.md](docs/BENCH.md).

## What it does not do

- **No app installed on the phone.** The optional Windows app runs on the computer; the phone only
  receives `pm disable-user` / `pm enable`.
- **No root, no Magisk, no Shizuku requirement.**
- **No custom ROM, no bootloader unlock, no flashing.**
- **No uninstall.** `pm disable-user` is reversible; `pm uninstall` is not.
- **No work profile or MDM changes.** If the phone is managed, it stops.
- **No YouTube ad blocking.** Private DNS does not touch same-domain ads. `docs/FAQ.md` explains.
- **No automatic telemetry.** The CLI is local; the optional feedback form sends only when a person
  presses Send. A hosted agent still receives the session (model, package names, fingerprint), so
  use a local model if that matters.
- **No "double battery" claims.** Realistic standby gain from debloat is 0–10%; the big wins are
  background restrictions, brightness/refresh rate and DNS.

## Safety

Read [docs/SAFETY.md](docs/SAFETY.md) before your first run. The short version:

- The CLI refuses packages on the protected list, packages that hold a role, and any change without
  a backup.
- Every disable is recorded. `python tools/phone.py restore` re-enables exactly what the tool
  disabled, and leaves alone anything you had already disabled.
- If the phone boot-loops, [docs/RESTORE.md](docs/RESTORE.md) has the recovery path. Do not factory
  reset as a first move.
- Debloating is reversible, but your OEM may see it differently. It does not void a legal warranty
  by itself in the EU, but a repair centre can refuse to work on modified software. Be honest with
  the person.

## Profiles

A profile is either a package list tested on a real phone (`device`) or a list built from a primary
firmware dump (`documented`). Documented profiles never auto-apply and have no `disable` list; use
them to ask per package. `apply` only runs for a `device` profile on a build listed in `tested`.
Tablet profiles set `form_factor: tablet`; a missing dialer/SMS role is a warning, not a failure.

The Windows app follows the same rule: `device` profiles can use the tested flow, `documented`
profiles require a warning and an explicit acknowledgement and run one package per batch. If no
profile matches, the app stops and links to this skill instead of guessing.

The full, model-by-model catalog is in [docs/PROFILES.md](docs/PROFILES.md).

| Brand | Profiles | Device-tested | Tablets |
|---|---|---|---|
| **Google** | 5 | 1 | 0 |
| **Samsung** | 55 | 1 | 7 |
| **Xiaomi** | 15 | 1 | 2 |
| **Redmi** | 56 | 0 | 1 |
| **POCO** | 16 | 0 | 0 |
| **OnePlus** | 8 | 1 | 0 |
| **Generic** | 1 | 0 | 0 |

Want to add yours? Read [profiles/README.md](profiles/README.md). A `device` profile needs a real
test; a `documented` profile needs a primary firmware dump or an owner-collected device inventory,
plus at least one source URL.

## The open-source OS question

Yes, it exists. No, it is not the first thing to do. [docs/ROMS.md](docs/ROMS.md) explains the real
trade-offs:

- **GrapheneOS** is excellent, but only on Pixel 6–10 (October 2026). Best security and privacy;
  sandboxed Play Services; locked bootloader.
- **/e/OS** has the widest easy-install list, with microG instead of Google.
- **LineageOS** is broad but higher-maintenance; official builds vary by device.
- **CalyxOS** covers Pixel, Fairphone and some Motorola models.

The costs are real: bootloader unlock wipes the phone, Play Integrity can break banking/Wallet and
drop Netflix to SD, some carriers lose VoLTE/Wi-Fi calling, and you become the maintainer of the
security patches. On Samsung, unlocking trips Knox permanently. That is why the skill stays on the
stock ROM: it removes the ad and telemetry surface most people notice, without those costs. It is not
a hardened OS and it is not a substitute for GrapheneOS on a Pixel.

## FAQ

**Does it void my warranty?**
Debloating is software configuration, not hardware modification, and it is reversible. In the EU a
legal guarantee is not automatically voided, but a repair centre may refuse modified software. The
skill does not unlock the bootloader.

**Can I brick my phone?**
Disabling the wrong core package can cause a boot loop. That is why the CLI refuses a protected list,
checks roles, backs up first and verifies in batches. `restore` undoes exactly what the tool disabled;
if its journal is lost, `restore --from-backup` reconstructs the change from the backup. The full
recovery path, including safe mode, is in [docs/RESTORE.md](docs/RESTORE.md).

**Does it remove ads from YouTube?**
No. An ad-blocking resolver over Private DNS blocks many in-app ads and trackers, but YouTube serves
ads from the same domain as the video. The skill does not install patched apps.

**Does it work on a work phone?**
No. If `dumpsys device_policy` shows a device or profile owner, or `pm list users` shows more than one
user, the skill stops.

**Does it work on Samsung/Xiaomi/Huawei?**
The method works on any Android 8+ phone. The package names and the safe list differ. Use a profile
for your exact model, or let the agent classify manually and ask before each package. On Huawei/Honor
without Google services, many `com.google.*` packages do not exist.

**Do I need Python?**
No. The skill includes the raw `adb` commands. The CLI is a guardrail and a convenience; it is
stdlib-only and has no dependencies. The Windows app bundles the CLI and does not require Python.

**Is there a GUI?**
Yes, an optional Windows app in [cleanyourphone-app](https://github.com/jparedesDS/cleanyourphone-app).
It is an Early MVP, not code-signed, and only continues on a known profile. The skill remains the
path for every other phone.

**How do I report a phone or send feedback?**
Use the [web form](https://jparedesds.github.io/cleanyourphone-web/#feedback), **Feedback** in the
app, or `scripts/feedback.py` from the skill. It is opt-in, previews the payload and excludes serial,
IP, IMEI and MAC addresses. See [docs/FEEDBACK.md](docs/FEEDBACK.md).

## Contributing

- A tested (`device`) profile for a new model: open a PR with `profiles/<brand>/<model>.json` and
  the test details.
- A `documented` profile: use `scripts/dump_inventory.py`, cite the primary dump in `sources`, and
  keep `disable` empty.
- A guard, parser or CLI fix: add a test in `tests/`.
- A safety rule change: open an issue first. Those rules are the product.
- A phone you cannot test yourself: send a [profile request](https://jparedesds.github.io/cleanyourphone-web/#feedback)
  with model, Android, build and fingerprint. No serial or IP.
- Brand or logo changes: read [docs/BRAND.md](docs/BRAND.md) before changing assets.
- Read [AGENTS.md](AGENTS.md) before changing the repo.

## License

MIT. See [LICENSE](LICENSE).
