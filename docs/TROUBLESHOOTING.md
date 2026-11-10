# Troubleshooting

## ADB

### `adb: command not found`

Install Android SDK Platform-Tools, unzip it, add the folder to `PATH`, or set `ADB` to the full path:

```bash
export ADB="$HOME/Android/Sdk/platform-tools/adb"
python tools/phone.py doctor
```

On Windows PowerShell:

```powershell
$env:ADB = "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe"
python tools\phone.py doctor
```

### `unauthorized`

The phone has not accepted the computer's key. Unlock the phone, unplug/replug the cable, and accept
**Allow USB debugging?**. If the prompt does not appear, revoke the USB debugging authorisations in
Developer options and replug.

### `offline`

Usually a cable, hub or driver problem. Try another cable, another USB port, and `adb kill-server`
then `adb start-server`. On Windows, install the OEM USB driver if the phone is not recognized.

### `more than one device`

```bash
python tools/phone.py doctor
python tools/phone.py --serial <serial> probe
```

Or set `ANDROID_SERIAL=<serial>`.

### The phone disconnects during the session

Some phones cut ADB when the screen locks or when the battery is low. Keep the screen awake, disable
USB debugging timeout if the OEM has one, and charge above 30%.

### “Wireless debugging” shows no pairing code

Android 11 and newer hide the pairing screen behind the row text. Turn Wireless debugging on, then
**tap the words “Wireless debugging”**, not only the switch. The detail screen has **Pair device with
pairing code**. If tapping does nothing, turn the switch off and on and try again. Android 10 and
older have no pairing-code flow; use USB.

### `protocol fault (couldn't read status message)` on `adb pair`

There are two ports, and this error usually means the wrong one was used:

- the **pairing port** is inside the **Pair device with pairing code** dialog;
- the **connection port** is on the main **Wireless debugging** screen.

Use the pairing port with `adb pair`, keep the dialog open, and use the current six-digit code. The
code expires and the port closes when the dialog closes. While the dialog is open, `adb mdns
services` lists `_adb-tls-pairing._tcp`; the main screen is `_adb-tls-connect._tcp`.

### `failed to connect` after a successful pair

Pairing and connection use different ports. Copy the IP:port from the main **Wireless debugging**
screen for `adb connect`. The port can change after the phone reconnects to Wi-Fi. Both devices must
be on the same network, VPNs should be off, and guest networks that isolate clients will not work.

### Windows does not see the phone at all

This is below ADB: the computer is not receiving USB data.

- Use a **data** cable, not a charge-only cable.
- Use a direct USB port, without a hub or adapter.
- Unlock the phone and choose **File transfer / MTP** in the USB notification.
- Check **Device Manager** for Android, ADB Interface, the phone brand, or an unknown device with a
  yellow warning sign.
- Install the official USB driver from the manufacturer. Do not install random “universal ADB”
  drivers.
- In Developer options, revoke the USB debugging authorisations, unplug, replug and accept the
  prompt again.
- `adb kill-server`, `adb start-server`, then `adb devices -l`.

## Packages

### `pm disable-user` refuses with `SecurityException`

Some firmware blocks it. Check the actual state:

```bash
adb shell pm list packages -d
```

If the package is not there, it was not disabled. Do not retry in a loop. If every package is
refused, stop: that build cannot be debloated this way. Use Private DNS and the phone's privacy
settings instead.

### `pm disable-user` says success but the package is still enabled

Check with `pm list packages -d`. Some OEMs print success and change nothing. If it is not disabled,
stop; do not try `pm hide` or `pm uninstall`.

### The package is not in the backup

The phone changed since the backup (an OTA, an app install, a factory reset, or a different user).
The CLI also refuses a backup whose build fingerprint does not match the current phone. Run
`python tools/phone.py backup` again, then re-plan. Do not disable a package that was not present when
the backup was taken.

### The package is already disabled

Skip it. It may have been disabled by the OEM or by a previous session. Do not enable it just to
disable it again.

### A package name is unfamiliar

```bash
adb shell dumpsys package <package> | grep -E "versionName|installerPackageName|firstInstallTime|enabled="
adb shell cmd package resolve-activity --brief <package>
```

Search the exact package name plus the model, or ask the person. Do not guess.

## Roles

### No dialer

```bash
adb shell cmd role get-role-holders android.app.role.DIALER
adb shell pm list packages | grep -i dialer
```

If the role is empty, set a dialer as default in Settings → Apps → Default apps → Phone. If the stock
dialer was disabled, re-enable it:

```bash
adb shell pm enable <dialer-package>
```

### No SMS

Same as the dialer, with `android.app.role.SMS` and Settings → Apps → Default apps → SMS.

### No Home

```bash
adb shell cmd role get-role-holders android.app.role.HOME
adb shell cmd package query-activities -a android.intent.action.MAIN -c android.intent.category.HOME
```

Set a launcher as Home in Settings → Apps → Default apps → Home. If the phone has no launcher, enable
the stock one from the backup.

### No keyboard

```bash
adb shell settings get secure default_input_method
adb shell ime list -s
```

Enable the stock keyboard and set it as default in Settings → System → Languages & input →
On-screen keyboard.

### `cmd role` is unknown

Android 9 and older do not have `cmd role`. The CLI falls back to the legacy settings
(`dialer_default_application`, `sms_default_application`) and the resolved HOME activity. The check is
less complete; be extra careful with dialer/SMS/Home packages.

## After a change

### Boot loop

See `docs/RESTORE.md`. Safe mode first, ADB restore second, factory reset last.

### Play Store or Play Services broken

You probably disabled `com.android.vending`, `com.google.android.gms` or `com.google.android.gsf`.
Re-enable them:

```bash
python tools/phone.py enable com.android.vending com.google.android.gms com.google.android.gsf
```

Then reboot. Do not disable them again.

### Notifications stopped

A disabled package may be the push provider (GMS, OEM push, the app itself). Re-enable the last
batch. Check `adb shell dumpsys notification` and the app's battery optimisation setting.

### Wi-Fi or mobile data stopped

Re-enable the last batch. Check that `com.android.phone`, the telephony provider, the IMS packages, the
carrier config, `com.android.networkstack` and `com.android.wifi` are enabled. If mobile data is off,
check `settings get global mobile_data` and the APN.

### Bluetooth stopped

Re-enable `com.android.bluetooth` and the OEM Bluetooth stack. Reboot.

### NFC or payments stopped

Re-enable `com.android.nfc` and `com.android.se`. Check that the wallet app is still installed and
that NFC is on.

### VoLTE or Wi-Fi calling stopped

Re-enable `com.android.ims`, `com.google.android.ims` and `com.android.carrierconfig`. Some carriers
need the OEM IMS app as well. Reboot and check Settings → Network → SIM → VoLTE.

### Camera or gallery broken

Re-enable the camera/gallery packages. If the camera app depends on an OEM framework package, the
backup list shows what was disabled.

### An app crashes or cannot log in

Re-enable the last batch, especially WebView, GMS, the permission controller and the certificate
store. If the app uses Play Integrity, a debloat is not the cause; a custom ROM or root would be.

### The package comes back after a reboot

Some OEM firmware re-enables packages at boot from its own list. Note it in the profile and stop
fighting it. Do not disable the updater or the OEM's package manager to win.

## Private DNS

### The network stops working after `dns set`

```bash
python tools/phone.py dns off
```

Some captive portals, corporate Wi-Fi networks and VPNs do not tolerate a strict resolver. Use
`opportunistic`, or set the DNS on the router instead.

### YouTube ads are still there

Expected. An ad-blocking resolver blocks domains, and YouTube serves ads from the same domain as the
video. The skill does not install patched apps.

### A banking app fails after DNS

Turn DNS off and test again. If it works, the resolver was blocking a domain the app needs; use a
different resolver or leave DNS off for that person.

## Browsers

### Websites show the desktop version

This is a browser setting, not a package change. Chrome and Brave remember **Desktop site** per tab
and per site.

- In Chrome or Brave: three dots → uncheck **Desktop site**.
- If it only happens on one site: tap the lock/icon next to the address → **Site settings** → turn off
  **Desktop site** for that site.
- If you changed a flag: open `chrome://flags`, search for “desktop”, and choose **Reset all**.

Do not re-enable packages or run `restore` for this. Only check `wm size` and `wm density` if the
whole Android interface looks oversized, not just one website.

## Windows

### Garbled characters in `dumpsys` output

The CLI writes UTF-8 with replacement characters. If your terminal is old, set the code page:

```powershell
chcp 65001
```

### `python` is not recognized

Install Python 3.9+ from python.org and tick "Add Python to PATH". The CLI uses only the standard
library; there is nothing to `pip install`.

### Long paths or permissions in `backup/`

Run the repo from a short path such as `C:\cleanyourphone`, or set
`CLEANYOURPHONE_BACKUP` to a writable folder.

## Xiaomi/HyperOS specifics

- HyperOS may re-enable MSA/GetApps after an OTA.
- `com.miui.securitycenter` is not optional: it carries permissions and privacy settings.
- Do not disable `com.miui.powerkeeper`; battery management and some background behaviour depend on it.
- Region affects package names. Verify each one.

## Samsung specifics

- `com.samsung.android.app.spage` (Samsung Free) is the main ad surface.
- Samsung Pass, Samsung Wallet/Pay and Knox are protected. Do not disable them at all.
- Do not unlock the bootloader: Knox is permanent.
- One UI can re-enable packages after a major update.
- Secure Folder and work profile packages are separate; do not touch them.

## Huawei/Honor specifics

- Many `com.google.*` packages do not exist.
- `com.huawei.systemmanager` carries permissions and battery; never disable it.
- The ROM scene is device-specific and often closed; do not promise a custom ROM.
