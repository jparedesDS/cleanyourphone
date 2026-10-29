# OnePlus profiles

## CPH2487 — OnePlus 11R 5G

Documented from the Android Dumps project `oneplus/OP5961L1` (Android 16). No device test yet.

## CPH2719 — OnePlus Nord CE5

Documented from the Android Dumps project `oneplus/OP613BL1` (Android 16). No device test yet.

## A6013 — OnePlus 6T

The only Android Dumps project for this model (`oneplus/OnePlus6T`) is **LineageOS 19.1**, not stock
OxygenOS. Its `README.md` says `lineage_fajita-userdebug`, Android 12, build `SQ3A.220605.009.A1`,
while the fingerprint is a spoofed stock OnePlus 6T fingerprint. Do not turn that dump into a stock
OxygenOS profile.

To add a real OnePlus 6T profile, collect a package dump from the actual phone:

```bash
adb shell getprop ro.product.model
adb shell getprop ro.build.version.release
adb shell getprop ro.build.display.id
adb shell getprop ro.build.fingerprint
adb shell pm list packages -f
adb shell pm list packages -d
adb shell pm list packages -e
```

Or, from the repository:

```bash
python tools/phone.py probe
python tools/phone.py backup
```

Use the backup's `meta.json` as the inventory. Mark the profile `documented` until the package list
has been tested on the phone. If the phone runs LineageOS 19.1, say so explicitly: it needs its own
profile and a matching rule for `ro.build.display.id`, not the stock fingerprint.
