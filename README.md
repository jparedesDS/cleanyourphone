# CleanYourPhone

**Your phone, minus the bloat.**

CleanYourPhone is a **skill for coding agents** (Claude Code, Codex, Cursor, Gemini CLI, OpenCode and
friends) that debloats an Android phone over ADB. No app to install, no root, no custom ROM, nothing
uninstalled. It disables preinstalled apps and services, optionally sets a Private DNS, verifies the
phone, and can undo every change with one command.

It is the phone version of [cleanyour.tv](https://cleanyour.tv), built the same way: one prompt, one
command, reversible, open source, and the person stays in control.

[Leer en español](README.es.md)

---

## Why a skill and not an app

An app that disables other apps needs root, Shizuku or device-owner privileges. That is a lot of
power and a lot of risk for something a shell command can do. A skill is just text: the person's
agent reads it, runs `adb`, shows a plan, and asks before touching anything. There is nothing to
install on the phone, nothing running in the background, and nothing that phones home.

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

### 3. Clone and check

```bash
git clone https://github.com/<your-user>/cleanyourphone
cd cleanyourphone
python tools/phone.py doctor
```

The CLI is optional. `SKILL.md` contains the raw `adb` commands too, so an agent can work without
Python. The CLI exists so the agent does not improvise the guardrails.

### 4. Give the skill to your agent

| Agent | Where to put it |
|---|---|
| **Claude Code** | `~/.claude/skills/clean-your-phone/SKILL.md` (personal) or `.claude/skills/clean-your-phone/SKILL.md` (project) |
| **OpenCode** | `~/.config/opencode/skills/clean-your-phone/SKILL.md` (global) or `.opencode/skills/clean-your-phone/SKILL.md` (project) |
| **Codex** | `AGENTS.md` in the project, or `~/.codex/AGENTS.md`; paste `PROMPT.md` if your build does not load skills |
| **Cursor** | `.cursor/rules/clean-your-phone.mdc` with the contents of `SKILL.md` |
| **Gemini CLI** | `GEMINI.md` in the project |
| **Any chat agent** | Paste `PROMPT.md`, then paste `SKILL.md` when it asks |

Spanish prompt: [PROMPT.es.md](PROMPT.es.md). The skill answers in the language the person writes in.

The simplest setup is to clone the repo and open your agent in that folder: `SKILL.md` is already at
the root, so `python tools/phone.py` works. If your agent loads skills from a global folder, copy
`SKILL.md` there and keep the repo cloned so the CLI is available:

```bash
mkdir -p ~/.claude/skills/clean-your-phone
cp SKILL.md ~/.claude/skills/clean-your-phone/SKILL.md
```

Without the repo, the skill still works: it includes the raw `adb` commands and tells the agent to
use them.

Then ask: **"Clean my phone"** or **"Use clean-your-phone on my Pixel"**.

## What it does

- Disables OEM telemetry, ad surfaces, recommendation rows, duplicate browsers/stores and unused
  preloads.
- Optionally sets Private DNS (`dns.adguard-dns.com`, NextDNS or your own resolver).
- Produces a report: what changed, why, what was kept, the backup path and the undo command.
- Measures a battery baseline before/after (`docs/BATTERY.md`), without promising miracles.

## What it does not do

- **No app.** Nothing is installed on the phone.
- **No root, no Magisk, no Shizuku requirement.**
- **No custom ROM, no bootloader unlock, no flashing.**
- **No uninstall.** `pm disable-user` is reversible; `pm uninstall` is not.
- **No work profile or MDM changes.** If the phone is managed, it stops.
- **No YouTube ad blocking.** Private DNS does not touch same-domain ads. `docs/FAQ.md` explains.
- **No "double battery" claims.** Realistic standby gain from debloat is 0–10%; the big wins are
  background restrictions, brightness/refresh rate and DNS.
- **No cloud requirement for the CLI.** It is local-only; a hosted agent still receives the session
  (model, package names, fingerprint), so use a local model if that matters.

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

| Profile | Model | Android | Verification |
|---|---|---|---|
| [`google-pixel-8`](profiles/google/pixel-8.json) | Pixel 8 (shiba) | 14–16 | device, tested Android 16 build |
| [`google-pixel-6`](profiles/google/pixel-6.json) | Pixel 6 (oriole) | 12 | documented, ask only |
| [`google-pixel-6-pro`](profiles/google/pixel-6-pro.json) | Pixel 6 Pro (raven) | 12 | documented, ask only |
| [`google-pixel-7`](profiles/google/pixel-7.json) | Pixel 7 (panther) | 13 | documented, ask only |
| [`google-pixel-7a`](profiles/google/pixel-7a.json) | Pixel 7a (lynx) | 13 | documented, ask only |
| [`samsung-sm-s918b`](profiles/samsung/sm-s918b.json) | Galaxy S23 Ultra (SM-S918B) | 13–16 | device, tested Android 14 build |
| [`samsung-sm-a022f`](profiles/samsung/sm-a022f.json) | Galaxy A02 (SM-A022F) | 11 | documented, ask only |
| [`samsung-sm-a042f`](profiles/samsung/sm-a042f.json) | Galaxy A04e (SM-A042F) | 14 | documented, ask only |
| [`samsung-sm-a065f`](profiles/samsung/sm-a065f.json) | Galaxy A06 (SM-A065F) | 16 | documented, ask only |
| [`samsung-sm-a145f`](profiles/samsung/sm-a145f.json) | Galaxy A14 (SM-A145F) | 13 | documented, ask only |
| [`samsung-sm-a146p`](profiles/samsung/sm-a146p.json) | Galaxy A14 5G (SM-A146P) | 14 | documented, ask only |
| [`samsung-sm-a226b`](profiles/samsung/sm-a226b.json) | Galaxy A22 5G (SM-A226B) | 13 | documented, ask only |
| [`samsung-sm-a245f`](profiles/samsung/sm-a245f.json) | Galaxy A24 (SM-A245F) | 13 | documented, ask only |
| [`samsung-sm-a305f`](profiles/samsung/sm-a305f.json) | Galaxy A30 (SM-A305F) | 11 | documented, ask only |
| [`samsung-sm-a325f`](profiles/samsung/sm-a325f.json) | Galaxy A32 (SM-A325F) | 13 | documented, ask only |
| [`samsung-sm-a326b`](profiles/samsung/sm-a326b.json) | Galaxy A32 5G (SM-A326B) | 13 | documented, ask only |
| [`samsung-sm-a505f`](profiles/samsung/sm-a505f.json) | Galaxy A50 (SM-A505F) | 11 | documented, ask only |
| [`samsung-sm-a546e`](profiles/samsung/sm-a546e.json) | Galaxy A54 5G (SM-A546E) | 13 | documented, ask only |
| [`samsung-sm-a576b`](profiles/samsung/sm-a576b.json) | Galaxy A57 5G (SM-A576B) | 16 | documented, ask only |
| [`samsung-sm-a600fn`](profiles/samsung/sm-a600fn.json) | Galaxy A6 (2018) (SM-A600FN) | 10 | documented, ask only |
| [`samsung-sm-a715f`](profiles/samsung/sm-a715f.json) | Galaxy A71 (SM-A715F) | 12 | documented, ask only |
| [`samsung-sm-a725f`](profiles/samsung/sm-a725f.json) | Galaxy A72 (SM-A725F) | 12 | documented, ask only |
| [`samsung-sm-e045f`](profiles/samsung/sm-e045f.json) | Galaxy F04 (SM-E045F) | 13 | documented, ask only |
| [`samsung-sm-e055f`](profiles/samsung/sm-e055f.json) | Galaxy F05 (SM-E055F) | 16 | documented, ask only |
| [`samsung-sm-e225f`](profiles/samsung/sm-e225f.json) | Galaxy F22 (SM-E225F) | 12 | documented, ask only |
| [`samsung-sm-e236b`](profiles/samsung/sm-e236b.json) | Galaxy F23 5G (SM-E236B) | 12 | documented, ask only |
| [`samsung-sm-e625f`](profiles/samsung/sm-e625f.json) | Galaxy F62 (SM-E625F) | 12 | documented, ask only |
| [`samsung-sm-j400f`](profiles/samsung/sm-j400f.json) | Galaxy J4 (SM-J400F) | 10 | documented, ask only |
| [`samsung-sm-j720f`](profiles/samsung/sm-j720f.json) | Galaxy J7 Duo (SM-J720F) | 10 | documented, ask only |
| [`samsung-on7xelte`](profiles/samsung/on7xelte.json) | Galaxy J7 Prime (`on7xelte`) | 8 | documented, ask only |
| [`samsung-sm-m015g`](profiles/samsung/sm-m015g.json) | Galaxy M01 (SM-M015G) | 11 | documented, ask only |
| [`samsung-sm-m105g`](profiles/samsung/sm-m105g.json) | Galaxy M10 (SM-M105G) | 10 | documented, ask only |
| [`samsung-sm-m115f`](profiles/samsung/sm-m115f.json) | Galaxy M11 (SM-M115F) | 11 | documented, ask only |
| [`samsung-sm-m136b`](profiles/samsung/sm-m136b.json) | Galaxy M13 5G (SM-M136B) | 14 | documented, ask only |
| [`samsung-sm-m146b`](profiles/samsung/sm-m146b.json) | Galaxy M14 5G (SM-M146B) | 13 | documented, ask only |
| [`samsung-sm-m325f`](profiles/samsung/sm-m325f.json) | Galaxy M32 (SM-M325F) | 11 | documented, ask only |
| [`samsung-sm-m526b`](profiles/samsung/sm-m526b.json) | Galaxy M52 5G (SM-M526B) | 12 | documented, ask only |
| [`samsung-sm-n970f`](profiles/samsung/sm-n970f.json) | Galaxy Note10 (SM-N970F) | 12 | documented, ask only |
| [`samsung-sm-n981b`](profiles/samsung/sm-n981b.json) | Galaxy Note20 (SM-N981B) | 12 | documented, ask only |
| [`samsung-sm-n986b`](profiles/samsung/sm-n986b.json) | Galaxy Note20 Ultra (SM-N986B) | 12 | documented, ask only |
| [`samsung-sm-g770f`](profiles/samsung/sm-g770f.json) | Galaxy S10 Lite (SM-G770F) | 13 | documented, ask only |
| [`samsung-sm-g980f`](profiles/samsung/sm-g980f.json) | Galaxy S20 (SM-G980F) | 12 | documented, ask only |
| [`samsung-sm-g981n`](profiles/samsung/sm-g981n.json) | Galaxy S20 (SM-G981N) | 12 | documented, ask only |
| [`samsung-sm-g780f`](profiles/samsung/sm-g780f.json) | Galaxy S20 FE (SM-G780F) | 13 | documented, ask only |
| [`samsung-sm-g988b`](profiles/samsung/sm-g988b.json) | Galaxy S20 Ultra (SM-G988B) | 12 | documented, ask only |
| [`samsung-sm-g986b`](profiles/samsung/sm-g986b.json) | Galaxy S20+ (SM-G986B) | 12 | documented, ask only |
| [`samsung-sm-g991b`](profiles/samsung/sm-g991b.json) | Galaxy S21 (SM-G991B) | 12 | documented, ask only |
| [`samsung-sm-g990b`](profiles/samsung/sm-g990b.json) | Galaxy S21 FE (SM-G990B) | 12 | documented, ask only |
| [`samsung-sm-g998b`](profiles/samsung/sm-g998b.json) | Galaxy S21 Ultra (SM-G998B) | 12 | documented, ask only |
| [`samsung-sm-g996b`](profiles/samsung/sm-g996b.json) | Galaxy S21+ (SM-G996B) | 12 | documented, ask only |
| [`samsung-sm-s938b`](profiles/samsung/sm-s938b.json) | Galaxy S25 Ultra (SM-S938B) | 16 | documented, ask only |
| [`samsung-sm-t500`](profiles/samsung/sm-t500.json) | Galaxy Tab A7 10.4 (SM-T500) | 11 | documented, ask only, tablet |
| [`samsung-sm-t505`](profiles/samsung/sm-t505.json) | Galaxy Tab A7 10.4 (SM-T505) | 12 | documented, ask only, tablet |
| [`samsung-sm-t227u`](profiles/samsung/sm-t227u.json) | Galaxy Tab A7 Lite (SM-T227U) | 11 | documented, ask only, tablet |
| [`samsung-sm-t577u`](profiles/samsung/sm-t577u.json) | Galaxy Tab Active3 (SM-T577U) | 13 | documented, ask only, tablet |
| [`samsung-sm-p615`](profiles/samsung/sm-p615.json) | Galaxy Tab S6 Lite (SM-P615) | 13 | documented, ask only, tablet |
| [`samsung-sm-t875`](profiles/samsung/sm-t875.json) | Galaxy Tab S7 (SM-T875) | 13 | documented, ask only, tablet |
| [`samsung-sm-t975`](profiles/samsung/sm-t975.json) | Galaxy Tab S7+ (SM-T975) | 13 | documented, ask only, tablet |
| [`samsung-sm-f707u1`](profiles/samsung/sm-f707u1.json) | Galaxy Z Flip 5G (SM-F707U1) | 13 | documented, ask only |
| [`samsung-sm-f916u`](profiles/samsung/sm-f916u.json) | Galaxy Z Fold2 (SM-F916U) | 13 | documented, ask only |
| [`oneplus-a6013`](profiles/oneplus/oneplus-a6013.json) | OnePlus 6T (ONEPLUS A6013) | 11 | device, tested OxygenOS 11.1.2.2 build |
| [`oneplus-cph2487`](profiles/oneplus/oneplus-cph2487.json) | OnePlus 11R 5G (CPH2487) | 16 | documented, ask only |
| [`oneplus-hd1925`](profiles/oneplus/oneplus-hd1925.json) | OnePlus 7T Pro 5G McLaren (HD1925) | 11 | documented, ask only |
| [`oneplus-in2013`](profiles/oneplus/oneplus-in2013.json) | OnePlus 8 (IN2013) | 11 | documented, ask only |
| [`oneplus-ac2003`](profiles/oneplus/oneplus-ac2003.json) | OnePlus Nord (AC2003) | 11 | documented, ask only |
| [`oneplus-nord-ce`](profiles/oneplus/oneplus-nord-ce.json) | OnePlus Nord CE 5G (`OnePlusNordCE`) | 11 | documented, ask only |
| [`oneplus-cph2719`](profiles/oneplus/oneplus-cph2719.json) | OnePlus Nord CE5 (CPH2719) | 16 | documented, ask only |
| [`xiaomi-hyperos`](profiles/xiaomi/hyperos.json) | Xiaomi/Redmi/POCO, HyperOS | 14–16 | device, family profile, no auto-apply |
| [`xiaomi-mi-10`](profiles/xiaomi/xiaomi-mi-10.json) | Mi 10 | 12 | documented, ask only |
| [`xiaomi-mi-11-ultra`](profiles/xiaomi/xiaomi-mi-11-ultra.json) | Mi 11 Ultra (`star`) | 12 | documented, ask only |
| [`xiaomi-mi-9-se`](profiles/xiaomi/xiaomi-mi-9-se.json) | Mi 9 SE (`grus`) | 10 | documented, ask only |
| [`xiaomi-mi-note-10`](profiles/xiaomi/xiaomi-mi-note-10.json) | tucana | 11 | documented, ask only |
| [`xiaomi-11t`](profiles/xiaomi/xiaomi-11t.json) | Xiaomi 11T (`agate`) | 14 | documented, ask only |
| [`xiaomi-11t-pro`](profiles/xiaomi/xiaomi-11t-pro.json) | Xiaomi 11T Pro (2107113SC) | 13 | documented, ask only |
| [`xiaomi-12-lite`](profiles/xiaomi/xiaomi-12-lite.json) | Xiaomi 12 Lite (2203129C) | 13 | documented, ask only |
| [`xiaomi-12x`](profiles/xiaomi/xiaomi-12x.json) | Xiaomi 12X (2112123AG) | 12 | documented, ask only |
| [`xiaomi-15-ultra`](profiles/xiaomi/xiaomi-15-ultra.json) | Xiaomi 15 Ultra (25010PN30G) | 16 | documented, ask only |
| [`xiaomi-15t`](profiles/xiaomi/xiaomi-15t.json) | Xiaomi 15T (25069PTEBG) | 16 | documented, ask only |
| [`xiaomi-17-ultra`](profiles/xiaomi/xiaomi-17-ultra.json) | Xiaomi 17 Ultra (2512BPNDAG) | 16 | documented, ask only |
| [`xiaomi-civi`](profiles/xiaomi/xiaomi-civi.json) | Xiaomi Civi (2109119BC) | 12 | documented, ask only |
| [`xiaomi-pad-6`](profiles/xiaomi/xiaomi-pad-6.json) | Xiaomi Pad 6 (23043RP34C) | 13 | documented, ask only, tablet |
| [`xiaomi-pad-6-pro`](profiles/xiaomi/xiaomi-pad-6-pro.json) | Xiaomi Pad 6 Pro (23046RP50C) | 13 | documented, ask only, tablet |
| [`redmi-note-9-pro-joyeuse`](profiles/redmi/redmi-note-9-pro-joyeuse.json) | joyeuse | 12 | documented, ask only |
| [`redmi-10`](profiles/redmi/redmi-10.json) | Redmi 10 (21061119AG) | 13 | documented, ask only |
| [`redmi-10-5g`](profiles/redmi/redmi-10-5g.json) | Redmi 10 5G / Redmi 11 Prime 5G (22041219G) | 14 | documented, ask only |
| [`redmi-10a`](profiles/redmi/redmi-10a.json) | Redmi 10A (220233L2G) | 11 | documented, ask only |
| [`redmi-10c`](profiles/redmi/redmi-10c.json) | Redmi 10C (`fog`) | 12 | documented, ask only |
| [`redmi-11-prime`](profiles/redmi/redmi-11-prime.json) | Redmi 11 Prime (22071219AI) | 14 | documented, ask only |
| [`redmi-12`](profiles/redmi/redmi-12.json) | Redmi 12 (`fire`) | 14 | documented, ask only |
| [`redmi-12-5g`](profiles/redmi/redmi-12-5g.json) | Redmi 12 5G (`sky`) | 15 | documented, ask only |
| [`redmi-12c`](profiles/redmi/redmi-12c.json) | Redmi 12C (22120RN86C) | 14 | documented, ask only |
| [`redmi-13c-5g`](profiles/redmi/redmi-13c-5g.json) | Redmi 13C 5G / Redmi 13R 5G (`air`) | 15 | documented, ask only |
| [`redmi-15c`](profiles/redmi/redmi-15c.json) | Redmi 15C (`dew`) | 16 | documented, ask only |
| [`redmi-9-cattail`](profiles/redmi/redmi-9-cattail.json) | Redmi 9 (M2006C3MII) | 11 | documented, ask only |
| [`redmi-9`](profiles/redmi/redmi-9.json) | Redmi 9 / Redmi 9 Prime (`lancelot`) | 12 | documented, ask only |
| [`redmi-9c-nfc`](profiles/redmi/redmi-9c-nfc.json) | Redmi 9C NFC (M2006C3MNG) | 11 | documented, ask only |
| [`redmi-9t`](profiles/redmi/redmi-9t.json) | Redmi 9T (M2010J19SL) | 12 | documented, ask only |
| [`redmi-9t-lime`](profiles/redmi/redmi-9t-lime.json) | Redmi 9T / Redmi 9 Power (`lime`) | 10 | documented, ask only |
| [`redmi-a1`](profiles/redmi/redmi-a1.json) | Redmi A1 (`ice`) | 12 | documented, ask only |
| [`redmi-a2`](profiles/redmi/redmi-a2.json) | Redmi A2+ (`water`) | 13 | documented, ask only |
| [`redmi-k20`](profiles/redmi/redmi-k20.json) | Redmi K20 (`davinciin`) | 11 | documented, ask only |
| [`redmi-k20-pro`](profiles/redmi/redmi-k20-pro.json) | Redmi K20 Pro (`raphaelin`) | 10 | documented, ask only |
| [`redmi-k20-pro-raphael`](profiles/redmi/redmi-k20-pro-raphael.json) | raphael | 11 | documented, ask only |
| [`redmi-k30-4g`](profiles/redmi/redmi-k30-4g.json) | Redmi K30 4G (`phoenix`) | 12 | documented, ask only |
| [`redmi-k40-gaming`](profiles/redmi/redmi-k40-gaming.json) | Redmi K40 Gaming (`ares`) | 12 | documented, ask only |
| [`redmi-k40-pro`](profiles/redmi/redmi-k40-pro.json) | Redmi K40 Pro (M2012K11C) | 12 | documented, ask only |
| [`redmi-k40s`](profiles/redmi/redmi-k40s.json) | Redmi K40S (22021211RC) | 13 | documented, ask only |
| [`redmi-note-10`](profiles/redmi/redmi-note-10.json) | Redmi Note 10 (M2103K19C) | 12 | documented, ask only |
| [`redmi-note-10-mojito`](profiles/redmi/redmi-note-10-mojito.json) | Redmi Note 10 (`mojito`) | 12 | documented, ask only |
| [`redmi-note-10-lite`](profiles/redmi/redmi-note-10-lite.json) | curtana | 11 | documented, ask only |
| [`redmi-note-10s`](profiles/redmi/redmi-note-10s.json) | Redmi Note 10S (`rosemary`) | 13 | documented, ask only |
| [`redmi-note-11-pro`](profiles/redmi/redmi-note-11-pro.json) | Redmi Note 11 Pro (`pissarro`) | 13 | documented, ask only |
| [`redmi-note-11-pro-5g`](profiles/redmi/redmi-note-11-pro-5g.json) | Redmi Note 11 Pro 5G (2201116SG) | 13 | documented, ask only |
| [`redmi-note-11s`](profiles/redmi/redmi-note-11s.json) | Redmi Note 11S (`fleur`) | 13 | documented, ask only |
| [`redmi-note-11t-5g`](profiles/redmi/redmi-note-11t-5g.json) | Redmi Note 11T 5G (`evergo`) | 13 | documented, ask only |
| [`redmi-note-12-pro-5g`](profiles/redmi/redmi-note-12-pro-5g.json) | Redmi Note 12 Pro 5G (`ruby`) | 14 | documented, ask only |
| [`redmi-note-12-pro-speed`](profiles/redmi/redmi-note-12-pro-speed.json) | Redmi Note 12 Pro Speed (22101320C) | 13 | documented, ask only |
| [`redmi-note-12s`](profiles/redmi/redmi-note-12s.json) | Redmi Note 12S (`sea`) | 15 | documented, ask only |
| [`redmi-note-13`](profiles/redmi/redmi-note-13.json) | Redmi Note 13 (`sapphire`) | 15 | documented, ask only |
| [`redmi-note-13-5g`](profiles/redmi/redmi-note-13-5g.json) | Redmi Note 13 5G (`gold`) | 15 | documented, ask only |
| [`redmi-note-13-pro`](profiles/redmi/redmi-note-13-pro.json) | Redmi Note 13 Pro (`emerald`) | 15 | documented, ask only |
| [`redmi-note-13r`](profiles/redmi/redmi-note-13r.json) | Redmi Note 13R (2406ERN9CC) | 16 | documented, ask only |
| [`redmi-note-14-4g`](profiles/redmi/redmi-note-14-4g.json) | Redmi Note 14 4G (`tanzanite`) | 16 | documented, ask only |
| [`redmi-note-15`](profiles/redmi/redmi-note-15.json) | Redmi Note 15 (`spinel`) | 16 | documented, ask only |
| [`redmi-note-15-5g`](profiles/redmi/redmi-note-15-5g.json) | Redmi Note 15 5G (`kunzite`) | 16 | documented, ask only |
| [`redmi-note-15-pro`](profiles/redmi/redmi-note-15-pro.json) | Redmi Note 15 Pro (`lapis`) | 16 | documented, ask only |
| [`redmi-note-17-pro-max-5g`](profiles/redmi/redmi-note-17-pro-max-5g.json) | Redmi Note 17 Pro Max 5G (`brussels`) | 16 | documented, ask only |
| [`redmi-note-7-pro`](profiles/redmi/redmi-note-7-pro.json) | Redmi Note 7 Pro (`violet`) | 10 | documented, ask only |
| [`redmi-note-8`](profiles/redmi/redmi-note-8.json) | Redmi Note 8 (`ginkgo`) | 11 | documented, ask only |
| [`redmi-note-8-2021`](profiles/redmi/redmi-note-8-2021.json) | Redmi Note 8 (2021) (`biloba`) | 11 | documented, ask only |
| [`redmi-note-8-pro`](profiles/redmi/redmi-note-8-pro.json) | Redmi Note 8 Pro (`begonia`) | 11 | documented, ask only |
| [`redmi-note-9`](profiles/redmi/redmi-note-9.json) | Redmi Note 9 (`merlin`) | 12 | documented, ask only |
| [`redmi-note-9-pro-gauguin`](profiles/redmi/redmi-note-9-pro-gauguin.json) | Redmi Note 9 Pro (`gauguin`) | 12 | documented, ask only |
| [`redmi-note-9-pro`](profiles/redmi/redmi-note-9-pro.json) | Redmi Note 9 Pro / Redmi Note 9S (`miatoll`) | 12 | documented, ask only |
| [`redmi-note-9-pro-max`](profiles/redmi/redmi-note-9-pro-max.json) | excalibur | 11 | documented, ask only |
| [`redmi-pad`](profiles/redmi/redmi-pad.json) | Redmi Pad (22081283G) | 12 | documented, ask only, tablet |
| [`redmi-pad-2`](profiles/redmi/redmi-pad-2.json) | Redmi Pad 2 (`taiko`) | 16 | documented, ask only, tablet |
| [`redmi-turbo-5-max`](profiles/redmi/redmi-turbo-5-max.json) | REDMI Turbo 5 Max (2602BRT18C) | 16 | documented, ask only |
| [`redmi-y3`](profiles/redmi/redmi-y3.json) | Redmi Y3 (`onc`) | 10 | documented, ask only |
| [`poco-c31`](profiles/poco/poco-c31.json) | POCO C31 (211033MI) | 11 | documented, ask only |
| [`poco-f3`](profiles/poco/poco-f3.json) | POCO F3 (M2012K11AG) | 12 | documented, ask only |
| [`poco-f5`](profiles/poco/poco-f5.json) | POCO F5 (`marble`) | 15 | documented, ask only |
| [`poco-f6`](profiles/poco/poco-f6.json) | POCO F6 (24069PC21G) | 16 | documented, ask only |
| [`poco-f9-ultra`](profiles/poco/poco-f9-ultra.json) | POCO F9 Ultra (26077PC53G) | 16 | documented, ask only |
| [`poco-m2`](profiles/poco/poco-m2.json) | POCO M2 (M2004J19PI) | 11 | documented, ask only |
| [`poco-m2-pro`](profiles/poco/poco-m2-pro.json) | gram | 11 | documented, ask only |
| [`poco-m3`](profiles/poco/poco-m3.json) | POCO M3 (M2010J19CG) | 12 | documented, ask only |
| [`poco-m4-pro-5g`](profiles/poco/poco-m4-pro-5g.json) | POCO M4 Pro 5G (`evergreen`) | 13 | documented, ask only |
| [`poco-x2`](profiles/poco/poco-x2.json) | POCO X2 (`phoenixin`) | 11 | documented, ask only |
| [`poco-x3-nfc`](profiles/poco/poco-x3-nfc.json) | POCO X3 NFC (M2007J20CG) | 12 | documented, ask only |
| [`poco-x3-pro`](profiles/poco/poco-x3-pro.json) | POCO X3 Pro (vayu_in) | 12 | documented, ask only |
| [`poco-x5-5g`](profiles/poco/poco-x5-5g.json) | POCO X5 5G (22111317PI) | 12 | documented, ask only |
| [`poco-x6-pro-5g`](profiles/poco/poco-x6-pro-5g.json) | POCO X6 Pro 5G (2311DRK48G) | 16 | documented, ask only |
| [`poco-x7-pro`](profiles/poco/poco-x7-pro.json) | POCO X7 Pro (2412DPC0AG) | 16 | documented, ask only |
| [`poco-x8-pro`](profiles/poco/poco-x8-pro.json) | POCO X8 Pro (2511FPC34G) | 16 | documented, ask only |
| [`generic-android`](profiles/generic/android.json) | Any Android 8+ | 8+ | reference, no auto-apply |

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
checks roles, backs up first and verifies in batches. The recovery path is in
[docs/RESTORE.md](docs/RESTORE.md).

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
stdlib-only and has no dependencies.

## Contributing

- A tested (`device`) profile for a new model: open a PR with `profiles/<brand>/<model>.json` and
  the test details.
- A `documented` profile: use `scripts/dump_inventory.py`, cite the primary dump in `sources`, and
  keep `disable` empty.
- A guard, parser or CLI fix: add a test in `tests/`.
- A safety rule change: open an issue first. Those rules are the product.
- Read [AGENTS.md](AGENTS.md) before changing the repo.

## License

MIT. See [LICENSE](LICENSE).
