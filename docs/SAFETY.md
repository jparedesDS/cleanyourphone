# Safety

Debloating a TV is low-stakes: if it breaks, the family watches on another screen. Debloating a phone
is not. The phone is the dialer, the SMS app, the alarm, the banking token, the camera and the work
profile. A wrong package can leave someone without calls, without a keyboard, or in a boot loop.

This document explains what the skill protects, why, and what to do when something goes wrong.

## The one rule

**Disable, never uninstall.** The only state change is:

```bash
adb shell pm disable-user --user 0 <package>
```

The undo is:

```bash
adb shell pm enable <package>
```

`pm uninstall --user 0` is not a real uninstall (it removes the package for user 0 and can be undone
with `cmd package install-existing`), but it can break OTA updates, factory reset behaviour and the
OEM's restore flow. `pm hide`, `pm block` and `pm clear` have their own side effects. None of them
are used here.

## The protected list

`tools/protected.py` is the hard denylist. The CLI refuses these packages before it runs anything.
The list is conservative on purpose: a package that is not on it can still be dangerous, which is why
the role checks, the backup and the "ask first" rule exist.

### Android framework and System UI

`android`, `com.android.systemui`, `com.android.settings`, `com.android.shell`. Without them the phone
does not boot, or boots without a status bar, notifications or a way to change settings.

### Telephony and emergency

`com.android.phone`, `com.android.server.telecom`, `com.android.incallui`, `com.android.mms.service`,
the telephony provider, `com.android.ims*`, `com.google.android.ims`, `com.android.carrierconfig`,
`com.android.cellbroadcast*`, `com.android.emergency`. Losing these means no calls, no SMS/MMS, no
VoLTE/Wi-Fi calling, no emergency alerts, or no mobile data.

### Permissions and package management

`com.android.permissioncontroller`, `com.google.android.permissioncontroller`,
`com.android.packageinstaller`, `com.google.android.packageinstaller`, `com.android.ext.services`,
`com.android.ext.shared`, the `com.google.android.overlay.modules*` family. Without the permission
controller, apps cannot ask for permissions; without the installer, nothing installs or updates.

### Google core

`com.google.android.gms*` (Play Services and every subpackage), `com.google.android.gsf*` (Services
Framework), `com.android.vending*` (Play Store), `com.google.android.webview*` / `com.android.webview*`. Disabling
GMS breaks push notifications, banking apps, WhatsApp backups, Find My Device, location and Play
Integrity. Disabling WebView breaks in-app browsers and many login screens.

### Hardware and identity

`com.android.se` (eSIM/NFC secure element), `com.android.nfc` (payments, transit, tags),
`com.android.bluetooth*` (earbuds, car, wearables), `com.android.networkstack*` and
`com.android.wifi*` (Wi-Fi, mobile data, captive portals), `com.android.keychain` and
`com.android.certinstaller` (certificates for banking, VPN and enterprise Wi-Fi),
`com.android.vpndialogs` (VPN consent), `com.android.documentsui` (the file picker other apps use).

### OEM security and telephony

Samsung: `com.samsung.android.incallui`, `com.samsung.android.app.telephonyui`,
`com.samsung.android.dialer`, `com.samsung.android.messaging`, `com.samsung.android.app.settings`,
`com.samsung.android.thermal`, `com.samsung.android.spay`, `com.samsung.android.samsungpass`,
`com.samsung.android.authfw`, `com.samsung.android.knox*`.

Xiaomi: `com.miui.securitycenter`, `com.miui.powerkeeper`, `com.miui.permcenter`, `com.miui.home`,
`com.miui.telephony`, `com.xiaomi.xmsf`, `com.xiaomi.push`.

Huawei: `com.huawei.systemmanager`, `com.huawei.phone`, `com.huawei.contacts`, `com.huawei.mms`,
`com.huawei.dialer`, `com.huawei.android.launcher`, `com.huawei.powergenie`.

Oppo/OnePlus/Realme: `com.coloros.securitypermission`, `com.oplus.battery`,
`com.coloros.phonemanager`, `com.coloros.telephony`, `com.oplus.telephony`.

These lists are not complete for every region or firmware. When a package is not on the list, read
`dumpsys package <package>` and ask before touching it.

## Role checks

Android has roles: default dialer, default SMS, default Home, default keyboard, emergency. The CLI
reads the current holders before every batch, refuses if a package is a holder, and also refuses if a
holder is currently disabled. If the roles or the keyboard cannot be read, it stops instead of
guessing. It re-reads them before each batch, because disabling one app can move a role to another.

If a critical role (dialer, SMS on a phone, or Home) has no holder, the phone is already broken: stop
and fix it before continuing. The emergency role is reported as a warning because some builds do not
assign it; do not disable the emergency packages regardless.

A stock launcher can be more than the HOME app: Pixel Launcher and Samsung One UI Home also provide
the Recents screen when a third-party launcher is set. The role check allows disabling a launcher
that is not the current HOME, but do not do it without warning the person that Recents may break.

## Backup

`python tools/phone.py backup` writes a timestamped folder under `backup/` with:

- `packages.txt`, `enabled.txt`, `disabled.txt`, `system.txt`, `user.txt`
- `getprop.txt`
- `settings-global.txt`, `settings-secure.txt`, `settings-system.txt`
- `role-*.txt`, `ime.txt`, `home.txt`
- `device-policy.txt`, `battery.txt`, `users.txt`
- `meta.json` with the parsed lists and the probe

The CLI refuses to disable anything without a backup for the same serial **and build fingerprint**.
It records every package it disables in `~/.cleanyourphone/applied.json`, per serial. `python
tools/phone.py restore` re-enables exactly those packages and restores the Private DNS value recorded
before the change.

`disabled.txt` in the backup is the phone's pre-session disabled list. It is **not** the change log:
the phone may have arrived with packages already disabled. If you use raw `adb` instead of the CLI,
keep your own session list; `restore` cannot see those changes.

## Managed devices

If `dumpsys device_policy` shows a **Device Owner** or **Profile Owner**, the phone is managed by an
employer, a school or an MDM. Changing packages can violate policy and lock the person out of work
apps. The skill stops. If the policy cannot be read, it stops too: an unknown state is not permission.
Do not try to remove the device owner; that is a different, destructive job.

## Work profiles

A work profile is a separate user. `pm disable-user --user 0` only touches the personal user, but a
package shared by both users can still affect the work side. The CLI blocks every change when
`pm list users` shows more than one user, or when the user list cannot be read. Do not bypass it.

## Boot loop

A boot loop after a debloat is usually one of three things: a launcher with no replacement, a
keyboard with no replacement, or a protected package that was disabled manually. The recovery path:

1. Do not factory reset yet.
2. Boot into safe mode (most phones: hold Volume Down while booting). Safe mode disables third-party
   apps but keeps the system packages; if the phone boots, you can re-enable the last batch.
3. Connect USB and run `adb devices`. If ADB works, `python tools/phone.py restore`.
4. If ADB does not work, use your session list of packages you disabled (the CLI keeps it in
   `~/.cleanyourphone/applied.json`) and `pm enable <package>` from a computer that can reach the
   phone in recovery/safe mode. `disabled.txt` is the pre-session baseline, not the change log.
5. If nothing works, a factory reset is the last resort. Warn the person about data loss first.

`docs/RESTORE.md` has the long version.

## Warranty and law

Debloating is software configuration, not hardware modification, and it is reversible. In the EU, a
legal guarantee is not automatically voided by software changes, but a repair centre may refuse to
work on modified software, and the OEM's own warranty terms may differ. The skill does not unlock the
bootloader, root the phone or flash a ROM, which are the changes that most clearly affect warranty
and Play Integrity.

Be honest with the person: "This is reversible and does not root your phone. Your manufacturer may
still see that packages were disabled if you send it for repair."

## ADB security

USB debugging is a powerful interface. While it is on:

- Anyone with physical access and the authorised key can run shell commands.
- Wireless debugging exposes a port on the local network; do not leave it on in a café, hotel or
  office.
- `adb shell` has more privileges than a normal app. Treat the cable and the computer as trusted.

When the job is done: turn off Wireless debugging, turn off USB debugging (unless the person asks to
keep it), revoke USB debugging authorisations, unplug, and confirm `adb devices` no longer lists the
phone.

## Privacy

The CLI is local-only: it runs `adb` and writes local files, with no telemetry or network calls. The
backup stays in the repo's `backup/` folder (git-ignored) or in `~/.cleanyourphone/`. The
`getprop.txt` backup redacts serial numbers, IMEIs and MAC addresses. Profiles must not contain
serials, IMEIs, Android IDs, MAC addresses, Wi-Fi names, phone numbers, emails or IPs.

This does not make the **agent** local. A hosted coding agent receives the conversation, including
the phone model, Android version, package names and fingerprint. If that matters to the person, use a
local model or redact those values before pasting the session into a hosted tool.

## What to tell the person before you start

- "I will disable preinstalled apps, not uninstall them."
- "I will back up the package list and settings first."
- "I will ask before anything you use: banking, WhatsApp, camera, alarm, VPN, smartwatch."
- "If something breaks, we re-enable the last batch; the undo is one command."
- "This does not root your phone or install a ROM."
- "The realistic battery gain is small; the big wins are DNS and background restrictions."
