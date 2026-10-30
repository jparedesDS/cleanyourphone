# OnePlus profiles

## IN2013 – OnePlus 8

Documented from the Android Dumps project `oneplus/OnePlus8` (Android 11). No device test yet.

## OnePlusNordCE – OnePlus Nord CE 5G

Documented from the Android Dumps project `oneplus/OnePlusNordCE` (Android 11). Regional model
numbers EB2101/EB2103; the dump is the global build. No device test yet.

## CPH2487 – OnePlus 11R 5G

Documented from the Android Dumps project `oneplus/OP5961L1` (Android 16). No device test yet.

## CPH2719 — OnePlus Nord CE5

Documented from the Android Dumps project `oneplus/OP613BL1` (Android 16). No device test yet.

## A6013 — OnePlus 6T

The Android Dumps project `oneplus/OnePlus6T` is **LineageOS 19.1**, not stock OxygenOS. Its
`README.md` says `lineage_fajita-userdebug`, Android 12, build `SQ3A.220605.009.A1`, while the
fingerprint is a spoofed stock OnePlus 6T fingerprint. It was **not** used for the stock profile.

`oneplus-a6013.json` is tested on the owner's actual OnePlus 6T:

- Model: `ONEPLUS A6013`
- OxygenOS 11.1.2.2, Android 11
- Build: `ONEPLUS A6013_41_211125`
- Fingerprint: `OnePlus/OnePlus6T/OnePlus6T:11/RKQ1.201217.002/2111252327:user/release-keys`
- Verification: `device`
- Auto-apply: only on that exact build

The owner disabled 23 packages in five batches, rebooted, and passed all dialer/SMS/Home/keyboard/
Play checks. The public profile promotes only the 8 low-risk telemetry/logging packages to `disable`.
The user-facing apps (Google Photos, YouTube Music, Meet, Game Space, Zen Mode, AOD, screen recorder,
OnePlus Photos, OnePlus Backup, etc.) remain in `ask` so another owner can decide.

If a phone runs LineageOS 19.1, it needs its own profile and a matching rule for
`ro.build.display.id`, not the stock fingerprint.
