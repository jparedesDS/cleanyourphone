# Restore

Every change the CLI makes is reversible. It records what it disabled (per phone serial) and
re-enables exactly that. It does not touch packages that were already disabled before the backup.
If you used raw `adb` instead of the CLI, read [Manual undo](#manual-undo) first: `restore` cannot see
those changes.

## The one command

```bash
python tools/phone.py restore
```

What it does:

1. Reads `~/.cleanyourphone/applied.json`.
2. For each package the tool disabled, checks `pm list packages -d`.
3. Runs `pm enable <package>` for the ones that are still disabled.
4. Re-reads `pm list packages -d`. If any recorded package is still disabled, it stops and keeps the
   record instead of claiming success.
5. Restores the Private DNS value recorded before the first change.
6. Clears the record and writes `restored_at` only after the final check passes.

Dry run first if you want to see the list:

```bash
python tools/phone.py restore --dry-run
```

## Manual undo

If the CLI is not available, use the list of packages you disabled in this session:

```bash
adb shell pm enable <package>
adb shell pm list packages -e <package>
```

Do **not** enable every package from `pm list packages -d`. That list includes packages the OEM
disabled before you started and packages a work profile needs left alone. `disabled.txt` in the backup
is the pre-session baseline, so it tells you what was already disabled, not what this session changed.

`pm enable` is the inverse of `pm disable-user --user 0`. It does not restore app data (data was
never touched), and it does not reinstall an app that was uninstalled (the skill never uninstalls).

If `pm enable` says the package is unknown, it may have been removed by an OTA or by the OEM. Check:

```bash
adb shell pm list packages <package>
adb shell cmd package install-existing <package>
```

The second command is for a package that was uninstalled for user 0, not for one that was disabled.
The skill does not use it; it is here only for a phone that someone else modified.

## Restore the DNS

```bash
python tools/phone.py dns restore
```

Or manually:

```bash
adb shell settings put global private_dns_mode opportunistic
```

The specifier can stay in settings; `opportunistic` is the Android default and ignores it.

## If the phone boot-loops

Do not factory reset as the first move.

### 1. Safe mode

Most phones boot into safe mode by holding **Volume Down** while the boot animation plays. In safe
mode, third-party apps are disabled but system packages stay as they are. If the phone boots:

```bash
adb devices
python tools/phone.py restore
```

Safe mode entry varies:

- **Pixel / stock Android:** hold Volume Down during boot, or press and hold Power → long-press
  "Power off" → "Reboot to safe mode".
- **Samsung:** hold Volume Down during boot; release at the Samsung logo.
- **Xiaomi/Redmi/POCO:** hold Volume Down during boot; release at the logo.
- **OnePlus/Oppo/Realme:** hold Volume Down during boot.
- **Motorola:** hold Volume Down during boot.

### 2. ADB in safe mode

If `adb devices` shows the phone as `device`, restore. If it shows `unauthorized`, unlock the phone
and accept the prompt. If it shows `offline`, replug the cable.

### 3. Recovery

If safe mode does not boot, the phone may need recovery. Stock recovery usually offers "Wipe cache
partition" (harmless) and "Factory reset" (destructive). ADB in stock recovery is often unavailable
or unauthorized. Do not wipe data until you have told the person what they will lose.

### 4. Factory reset

This is the last resort. It erases the phone. Before it:

- Confirm the person has a backup of photos, contacts and authenticator seeds.
- Remove the Google/Samsung/Xiaomi account if the phone has FRP (Factory Reset Protection), or the
  phone will ask for the previous account after the reset.
- Tell them the debloat is gone and they will have to set the phone up again.

## What restore does not do

- It does not re-enable a package that was disabled by the OEM before the backup.
- It does not restore settings you changed manually outside the tool.
- It does not undo a factory reset, a ROM flash or a root.
- It does not fix a phone that was already broken before the session.

## Verify after restore

```bash
python tools/phone.py verify
```

Then test on the phone: call, SMS, camera, keyboard, Home, notifications, alarm, Wi-Fi, mobile data,
Bluetooth, Play Store and the apps the person named. If something still fails, re-enable the last
batch manually and check `adb shell dumpsys package <package>`.

## Keep the backup

`backup/<timestamp>_<model>/` contains the package lists and settings from before the session. Keep
it until the person has used the phone normally for a few days. It is git-ignored; do not upload it.
