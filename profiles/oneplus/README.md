# OnePlus profiles

## CPH2487 — OnePlus 11R 5G

Documented from the Android Dumps project `oneplus/OP5961L1` (Android 16). No device test yet.

## CPH2719 — OnePlus Nord CE5

Documented from the Android Dumps project `oneplus/OP613BL1` (Android 16). No device test yet.

## A6013 — OnePlus 6T

The Android Dumps project `oneplus/OnePlus6T` is **LineageOS 19.1**, not stock OxygenOS. Its
`README.md` says `lineage_fajita-userdebug`, Android 12, build `SQ3A.220605.009.A1`, while the
fingerprint is a spoofed stock OnePlus 6T fingerprint. It was **not** used for the stock profile.

`oneplus-a6013.json` is documented from a read-only package inventory collected from the owner's
actual OnePlus 6T:

- Model: `ONEPLUS A6013`
- OxygenOS 11.1.2.2, Android 11
- Build: `ONEPLUS A6013_41_211125`
- Fingerprint: `OnePlus/OnePlus6T/OnePlus6T:11/RKQ1.201217.002/2111252327:user/release-keys`

It has no `disable` list and no auto-apply. Only system packages are listed; the owner's user apps
are excluded. Promote it to `device` only after testing a batch and running the checklist.

If a phone runs LineageOS 19.1, it needs its own profile and a matching rule for
`ro.build.display.id`, not the stock fingerprint.
