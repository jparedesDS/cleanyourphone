# Battery

The honest version: debloating a modern Android phone usually saves **0–10% of standby drain**, and
sometimes nothing. The videos that promise "double battery" are either measuring a different thing,
or they disabled one app that was holding a wakelock. The big wins are elsewhere:

1. Restricting background activity for heavy apps (Instagram, TikTok, Facebook, AliExpress).
2. Lower brightness and refresh rate; turn off Always-On Display.
3. Turning off Wi-Fi/Bluetooth scanning and "Nearby devices" when you do not use them.
4. Private DNS: fewer ad requests, fewer network wakeups.
5. Removing OEM telemetry that wakes the phone at night.

Debloat helps most on Samsung/Xiaomi/Huawei phones with heavy preloads. On a Pixel it is often a
rounding error.

## Measure it, do not guess

Use the same phone, the same SIM, the same signal, the same brightness and the same apps. A test with
Wi-Fi on in one run and off in the other proves nothing.

### Protocol

1. Charge to 100% and unplug.
2. Turn off Always-On Display and set a fixed brightness (or adaptive with the same room light).
3. Do not use the phone for the test window.
4. Reset the stats:

```bash
python tools/phone.py battery reset
```

5. Leave it idle for 8 hours (overnight).
6. Snapshot:

```bash
python tools/phone.py battery snapshot
```

7. Do the debloat, reboot, charge to 100% again, and repeat steps 3–6.
8. Compare:

```bash
python tools/phone.py battery compare battery/<before> battery/<after>
```

The snapshot saves `batterystats.txt`, `battery.txt`, `deviceidle.txt`, `alarm.txt` and `power.txt`.

### What to read

In `batterystats.txt`:

- **Time on battery** and **Screen on**: the denominator. If screen-on time differs, the comparison
  is not valid.
- **Deep sleep**: higher is better.
- **Awake**: lower is better.
- **Estimated power use (mAh)**: the phone's own estimate; compare the same section, not the total.
- **Discharge**: the mAh used over the window.
- **Top apps** and **wakelocks**: the app that held the phone awake is the story. A debloat that
  removes a telemetry service shows up here.

In `deviceidle.txt`:

- `mState=IDLE` most of the night is good.
- `mLightState` and the whitelist show what is allowed to wake the phone.

In `alarm.txt`:

- Look for `*walarm*` and repeated wakes from one package. A preload that wakes every 15 minutes is
  a real battery cost.

In `power.txt`:

- `Wake Locks` and `mWakefulness` show what kept the CPU awake.

## Background restrictions (optional, ask first)

Android's App Standby and Doze already restrict background work. You can be more aggressive per app:

```bash
adb shell cmd appops set <package> RUN_IN_BACKGROUND ignore
adb shell cmd appops set <package> RUN_ANY_IN_BACKGROUND ignore
```

Undo:

```bash
adb shell cmd appops set <package> RUN_IN_BACKGROUND allow
adb shell cmd appops set <package> RUN_ANY_IN_BACKGROUND allow
```

This can break notifications, sync, alarms, messaging and banking push. Only do it for an app the
person explicitly says they do not need in the background, and test a notification afterwards. It is
not part of the default skill flow.

## Settings that matter more than debloat

- **Refresh rate**: 120 Hz costs more than 60 Hz. `settings put system peak_refresh_rate 60` and
  `min_refresh_rate 60` work on some phones, not all; the Settings UI is safer.
- **Brightness**: the single biggest variable. Do not compare a test at 30% with one at 80%.
- **Always-On Display**: off unless the person uses it.
- **Wi-Fi/Bluetooth scanning**: Settings → Location → Wi-Fi/Bluetooth scanning off; "Nearby devices"
  off if unused.
- **Hotspot, GPS, sync**: turn off when not needed; do not disable the services.
- **Battery saver apps**: do not install them. They add a background service and often make drain
  worse.

## DNS and ads

Private DNS reduces network requests from ad SDKs, which can reduce wakeups and data use. It does not
block YouTube ads (same domain as the video), and it is not a VPN. Measure it separately from the
debloat so you know which change did what.

## Custom ROMs

GrapheneOS and /e/OS can have better standby than a heavy OEM ROM, mostly because they remove the
OEM telemetry and preloads. They can also have worse standby if push notifications are proxied
differently. Do not promise a battery win from a ROM; measure it.

## Report template

```markdown
## Battery baseline

- Phone: <model>, Android <version>, build <build>
- Before: <date>, 8h idle, Wi-Fi on, mobile data on, brightness <x>%, AOD off
- After: <date>, same conditions
- Deep sleep: <before> → <after>
- Awake: <before> → <after>
- Discharge: <before> mAh → <after> mAh
- Top wakelock before: <package>
- Top wakelock after: <package>
- Verdict: <measured change>, <caveats>
```

If the numbers do not move, say so. A truthful "no measurable change" is better than a fake win.
