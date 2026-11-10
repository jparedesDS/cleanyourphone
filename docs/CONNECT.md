# Connect your phone

This guide is for a first-time ADB user. You do not need to understand ADB to follow it.
CleanYourPhone only reads or changes the phone after `adb devices -l` shows `device`.

If you are using the Windows app, the same steps apply; the app can find the Wi-Fi endpoint for you.

## Before you start

- Unlock the phone and keep it unlocked while you connect.
- Charge it above 30%.
- Use a phone you own. Do not use a work phone managed by an employer, MDM or a work profile.
- For Wi-Fi: the phone and the computer must be on the same Wi-Fi network.
- For USB: use a cable that carries data, not a charge-only cable.

## Enable Developer options

The menu names vary a little by brand. The usual path is:

1. **Settings → About phone**.
2. Find **Build number**. On Samsung it is under **Software information**. On Xiaomi/Redmi/POCO
   tap the **OS version** or **HyperOS version** instead. On OnePlus it is under **About device →
   Version**.
3. Tap it **seven times**.
4. Enter the phone PIN or pattern if asked. A message says developer mode is enabled.
5. Go back to **Settings → System → Developer options**. On Samsung it may be under **Settings →
   Developer options** directly.

Do not change anything else in Developer options. You only need the debugging switches.

## Option A: Wi-Fi (Android 11 or newer)

Wi-Fi is usually easier because you do not need a cable. The part that confuses most people is that
Android shows **two different ports**. Read the next steps carefully.

1. Open **Settings → System → Developer options → Wireless debugging**.
2. Turn **Wireless debugging** on. Keep Wi-Fi on.
3. **Tap the words “Wireless debugging”**, not only the switch. This opens the detail screen.
4. On that screen, tap **Pair device with pairing code**.
5. A dialog opens with:
   - a **six-digit code**;
   - an **IP address and port** *inside this dialog*.
6. Leave the dialog open. The code expires after a short time, and the pairing port closes when the
   dialog closes.
7. In the app, open **Connect → Wi-Fi**, tap **Find automatically**, and enter the six-digit code.
   If the app does not fill the address, type the **IP:port from the pairing dialog**. Then tap
   **Connect**.
8. If the phone asks **Allow debugging?**, accept it.

With the command line, the sequence is:

```bash
adb mdns services
adb pair <ip>:<pairing-port> <six-digit-code>
adb connect <ip>:<connect-port>
```

`adb mdns services` shows two services when the pairing dialog is open:

- `_adb-tls-pairing._tcp` is the **pairing** port. Use this one with `adb pair`.
- `_adb-tls-connect._tcp` is the **connection** port. Use this one with `adb connect`.

The port on the main **Wireless debugging** screen is the connection port. It is **not** the pairing
port. Using it with `adb pair` produces `protocol fault (couldn't read status message)`.

### If Wi-Fi pairing fails

- **`protocol fault`**: you used the connection port, or the pairing dialog closed and the code
  expired. Open **Pair device with pairing code** again and copy the address from that dialog.
- **`failed to connect`**: the connection port changed, or Wireless debugging is off. Open the main
  **Wireless debugging** screen and copy the current IP:port.
- **`Connection refused`**: turn Wireless debugging off and on again, then reopen the pairing dialog.
- **No device found**: make sure both devices are on the same Wi-Fi, turn off any VPN, and avoid guest
  networks that isolate clients. Windows Firewall can also block mDNS; type the address manually.
- **The phone IP changed**: reconnect to Wi-Fi and copy the new address. Do not reuse the old one.
- **Android 10 or older**: there is no pairing-code dialog. Use USB instead.

## Option B: USB

1. Open **Settings → System → Developer options**.
2. Turn on **USB debugging**.
3. Connect the phone to the computer with a data cable.
4. Unlock the phone. In the USB notification, choose **File transfer / MTP** or **PTP**. Do not leave
   it on “charging only”.
5. When **Allow USB debugging?** appears, tick **Always allow from this computer** and tap **Allow**.
6. Run:

   ```bash
   adb devices -l
   ```

   The phone must say `device`. `unauthorized` means you have not accepted the prompt. `offline` means
   the cable, hub or driver is failing.

### If Windows does not see the phone at all

- Try another **data** cable. Charge-only cables are the most common cause.
- Try another USB port directly on the computer, without a hub or adapter.
- Unlock the phone and check the USB notification again.
- Open **Device Manager**. Look for **Android**, **ADB Interface**, **OnePlus**, or an unknown device
  with a yellow warning sign.
- Install the official USB driver from the phone manufacturer. Do not install random “universal ADB”
  drivers.
- In Developer options, tap **Revoke USB debugging authorisations**, unplug, replug and accept the
  prompt again.
- Restart the ADB server:

  ```bash
  adb kill-server
  adb start-server
  adb devices -l
  ```

## Check the connection

```bash
adb devices -l
```

A good result looks like this (the serial and model will be different):

```text
<serial>    device product:<product> model:<model> device:<device> transport_id:1
```

Then run:

```bash
cleanyourphone doctor
cleanyourphone probe
```

If you are using the repository instead of the installed CLI:

```bash
python tools/phone.py doctor
python tools/phone.py probe
```

`doctor` shows which ADB and which device the CLI will use. `probe` shows the model, Android version
and build. If more than one device appears, pass `--serial <serial>` to every command or set
`ANDROID_SERIAL=<serial>`.

It is normal for the same phone to appear twice during Wi-Fi debugging: once as an IP address and
once as an mDNS name. Pick one and use it for the whole session. Do not switch transports in the
middle.

## Quick fixes

| What you see | What to do |
|---|---|
| `no devices` | Check the cable, choose File transfer, accept the prompt, or reopen Wireless debugging. |
| `unauthorized` | Unlock the phone and accept **Allow USB debugging?**. If it never appears, revoke authorisations and replug. |
| `offline` | Try another cable/port, then `adb kill-server` and `adb start-server`. |
| `more than one device` | Pass `--serial <serial>` or set `ANDROID_SERIAL`. |
| `protocol fault` on `adb pair` | You used the connection port. Use the port inside the pairing dialog, and keep the dialog open. |
| `failed to connect` after pairing | Copy the current connection port from the main Wireless debugging screen. |
| mDNS finds nothing | Same Wi-Fi, VPN off, guest network off, or type the IP:port manually. |
| Windows sees nothing | Data cable, direct port, File transfer mode, OEM driver. |

## Security

ADB can install apps, read logs and change settings. Treat it like a root password.

- Use your own computer and your own Wi-Fi.
- Turn **Wireless debugging** off when you finish.
- On a shared computer, revoke the phone's USB debugging authorisations.
- Never share your serial number, IMEI, IP address or pairing code in a public issue.

## Still stuck?

Open an issue at <https://github.com/jparedesDS/cleanyourphone/issues> with:

- the computer operating system;
- the phone model and Android version;
- the exact command you ran;
- the exact error message.

Remove serial numbers, IP addresses, pairing codes and account names before posting.
