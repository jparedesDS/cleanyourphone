# FAQ

### What is CleanYourPhone?

A skill for coding agents that debloats an Android phone over ADB. The agent reads `SKILL.md`, backs
up the phone, shows a plan, disables preinstalled packages with `pm disable-user --user 0`, verifies
the phone and can undo everything.

### Is it an app?

No. Nothing is installed on the phone. The only things on the computer are the skill text and an
optional Python CLI that wraps `adb`.

### Why not an app?

An app that disables other apps needs root, Shizuku or device-owner privileges. That is a lot of
power for something a shell command can do. A skill is text: it is auditable, portable across
agents, and it cannot run in the background or phone home.

### Is it safe?

It is as safe as the rules in `SKILL.md`: disable never uninstall, back up first, never touch the
protected list, check roles, ask before user-facing apps, small batches, verify, reboot, verify
again. The CLI enforces the mechanical parts. The person still has to approve the plan.

### Can it brick my phone?

Disabling a core package can cause a boot loop. The protected list, the role checks and the backup
exist to prevent that. If it happens, `docs/RESTORE.md` has the recovery path. A factory reset is the
last resort, not the first.

### Does it void my warranty?

It is software configuration, not hardware modification, and it is reversible. In the EU a legal
guarantee is not automatically voided, but a repair centre may refuse modified software. The skill
does not unlock the bootloader or root the phone.

### Does it need root or Shizuku?

No. It uses ADB, which the person enables in Developer options. No root, no Magisk, no Shizuku.

### Does it remove YouTube ads?

No. An ad-blocking resolver over Private DNS blocks many in-app ads and trackers, but YouTube serves
ads from the same domain as the video. The skill does not install patched apps or ReVanced.

### Does it work on Samsung?

Yes, on the stock ROM. Use a profile for the exact model and build, or classify manually. The
`apply` command refuses a build that is not listed in the profile's `tested` block; after an OTA,
use `plan` and disable one package at a time. Do not unlock the bootloader: Knox is permanent.

### Does it work on Xiaomi/HyperOS?

Yes, but package names vary by region and HyperOS re-enables some packages after an OTA. Re-check
after updates. The `xiaomi-hyperos` profile is a family starting point with `auto_apply: false`; use
`plan` and disable one package at a time. It is not a guarantee.

### Does it work on Huawei/Honor?

The ADB method works, but many `com.google.*` packages do not exist and the OEM packages are
different. Do not apply a Samsung/Xiaomi list. Classify manually.

### Does it work on a work phone?

No. If `dumpsys device_policy` shows a device owner or profile owner, the skill stops. Changing
packages on a managed phone can break company policy and lock the person out of work apps. It also
stops when `pm list users` shows more than one user, because a work profile or guest is a separate
user.

### Does it work on a tablet?

Yes, if it runs Android 8+ and has ADB. Tablets may have no telephony, so the dialer/SMS checks are
warnings, not failures. The Home and keyboard checks still apply.

### Does it work over Wi-Fi?

Yes, with Android's Wireless debugging (Developer options → Wireless debugging → Pair device with
pairing code). USB is more reliable and is the recommended path. Turn Wireless debugging off when
done.

### What if I have more than one device connected?

Pass `--serial <serial>` to every command, or set `ANDROID_SERIAL`. `python tools/phone.py doctor`
lists the connected devices.

### Does it uninstall anything?

No. `pm disable-user` keeps the package installed and reversible. The skill never runs
`pm uninstall`, `pm hide`, `pm block` or `pm clear`.

### What happens after an OTA?

Some OEMs re-enable packages at boot or after a major update. Run
`python tools/phone.py list --state disabled` and compare with the backup. Re-apply only what the
person still wants, and note the packages that come back instead of fighting them.

### Will it improve battery life?

Maybe a little. Realistic standby gain from debloat is 0–10%, more on heavy OEM ROMs, often nothing
on a Pixel. The bigger wins are background restrictions, brightness/refresh rate and DNS. See
`docs/BATTERY.md`.

### Does it send my data anywhere?

The CLI does not: it runs `adb` locally, makes no network calls and keeps the backup on the computer
(git-ignored). Profiles must not contain identifiers. But the **agent** may be hosted: the phone
model, package names, fingerprint and your conversation can go to its provider. Use a local model or
redact those values if that matters.

### Can I use it on a client's phone?

The license is MIT, so you can. But you are responsible for the backup, the plan and the person's
consent. Do not run it on a phone you do not own without explicit permission, and do not run it on a
managed device.

### Can I contribute a profile?

Yes. Read `profiles/README.md`. A profile needs a real test, the build fingerprint, the packages you
disabled, and what broke. Run `python tools/phone.py validate` before opening a PR.

### Does it work on iPhone?

No. iOS does not expose an ADB-like interface.

### Does it work on Android TV?

No. Use [cleanyour.tv](https://cleanyour.tv), which is the same idea for TVs.

### Does it work on Fire OS?

Fire tablets are Android underneath and may expose ADB, but the package list and the roles are
different. It is not tested; treat it as a manual, careful session.

### What if `pm disable-user` is refused?

Some firmware refuses it with a `SecurityException`. Check `pm list packages -d` instead of trusting
the exit code. If it refuses every package, stop: there is nothing to debloat on that build. Fall
back to Private DNS and the phone's own privacy settings.

### What if I already have a Private DNS or a VPN?

Check first: `python tools/phone.py dns status`. If a VPN or a router-level blocker is already doing
the job, do not overwrite it. Private DNS bypasses the router's DNS, so a Pi-hole/AdGuard Home setup
stops applying to the phone.

### Why "CleanYourPhone" and not "CleanYourAndroid"?

It is a working name. The important part is the method, not the domain. Rename it if the name is
taken in your market.
