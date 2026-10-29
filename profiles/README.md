# Profiles

A profile is a **tested package list for one model and firmware**. The skill uses it as a starting
point, not as permission to apply it silently. A profile that was not tested on a real phone is a
guess, and guesses are how phones lose their dialer.

## Files

```text
profiles/
├── schema.json
├── google/pixel-8.json
├── samsung/sm-s918b.json
├── xiaomi/hyperos.json
└── generic/android.json
```

The `id` is lowercase kebab-case and is what people pass to `phone.py plan --profile <id>`.

## Schema

```json
{
  "id": "samsung-sm-s918b",
  "brand": "Samsung",
  "model": "SM-S918B",
  "marketing_name": "Galaxy S23 Ultra",
  "codename": "dm3q",
  "android": ["13", "14", "15", "16"],
  "fingerprint_regex": "^samsung/dm3q",
  "auto_apply": true,
  "tested": [
    {"android": "14", "build": "UP1A.231005.007", "date": "2026-10-21", "by": "community"}
  ],
  "disable": [
    {"package": "com.samsung.android.app.spage", "why": "Samsung Free ads", "breaks": "Samsung Free"}
  ],
  "ask": [
    {"package": "com.samsung.android.bixby.agent", "why": "Bixby", "breaks": "Bixby voice"}
  ],
  "never": [
    {"package": "com.samsung.android.dialer", "why": "Dialer"}
  ],
  "notes": "One UI re-enables some packages after a major update."
}
```

| Field | Meaning |
|---|---|
| `id` | Unique, lowercase kebab-case. |
| `brand`, `model` | Match `ro.product.brand` / `ro.product.model`. Use `*` only for a generic profile or a family profile pinned by `fingerprint_regex` (for example Xiaomi/Redmi/POCO). |
| `marketing_name` | Human name, optional. |
| `codename` | Match `ro.product.device`, optional but recommended. |
| `android` | Android versions where this package list is expected to apply. It is a match filter, not a test claim. |
| `fingerprint_regex` | Match `ro.build.fingerprint`; pin the firmware family. It must not match an empty string. |
| `auto_apply` | `false` for a family/reference profile. Auto-apply also requires the phone to run a build listed in `tested`. |
| `generic` | `true` for a reference profile. A generic profile cannot have a `disable` list and cannot be auto-applied. |
| `tested` | At least one real test: the actual Android version, exact build, date, who. `build` must appear in the phone fingerprint for auto-apply. |
| `disable` | Packages tested on this model; low risk. Still shown to the person before applying. |
| `ask` | User-facing or dependency-heavy; ask per package. |
| `never` | Per-model additions to the global protected list. |
| `notes` | What is specific: region, carrier, OTA behaviour, known breakage. |

## Rules

1. **Test on the real phone.** A profile is not a list copied from a forum. Say which build, which
   region, and what you checked afterwards (call, SMS, camera, keyboard, Home, Play, notifications).
2. **No protected packages in `disable` or `ask`.** `tools/protected.py` is the source of truth. If
   you want to document one, put it in `never`.
3. **No current role holder in `disable`.** The CLI blocks it anyway, but a profile that depends on
   the block is a bad profile. A dialer, SMS app, Home app or keyboard can only be disabled after a
   replacement is set and confirmed.
4. **`disable` means "tested, low risk", not "I think it is fine".** If it is user-facing, put it in
   `ask`.
5. **Say what breaks.** "Nothing" is only acceptable for a pure telemetry/feedback package. If you
   do not know, put it in `ask` with "unknown; test it".
6. **Pin the firmware.** A major One UI/HyperOS/ColorOS update can rename or re-enable packages.
   Add a new `tested` entry instead of pretending the old test covers the new build. The CLI only
   auto-applies a profile when the phone build appears in `tested`; after an OTA it asks for
   `plan` plus one-by-one `disable` instead.
7. **No identifiers.** No serial, IMEI, Android ID, MAC, Wi-Fi name, phone number, email or IP.
8. **One model per file.** A family profile (Xiaomi/Redmi/POCO) is allowed only when
   `fingerprint_regex` pins the family and `notes` says which model, region and build were tested.
   Carrier variants with different package names get their own file.

## Test checklist

Before you add a package to `disable`, verify on the phone:

- [ ] `adb shell pm list packages <package>` shows it is installed.
- [ ] `dumpsys package <package>` shows what it is; the name is not enough.
- [ ] The phone still calls and receives calls.
- [ ] SMS sends and receives.
- [ ] Camera opens and saves a photo.
- [ ] The keyboard opens in a text field.
- [ ] Home and the app drawer open.
- [ ] Notifications arrive; an alarm rings.
- [ ] Wi-Fi, mobile data, Bluetooth and (if used) NFC still work.
- [ ] Play Services, Play Store, WhatsApp and the person's banking app still open.
- [ ] After a reboot, the package is still disabled (some OEMs re-enable it).

If any item fails, the package belongs in `ask` or `never`, not `disable`.

## Validate

```bash
python tools/phone.py validate
```

It checks the required fields, the id format, duplicate packages, protected packages in the wrong
section, and that a generic profile has no `disable` list. It does not replace a real test.

## Current profiles

| ID | Model | Android | Notes |
|---|---|---|---|
| `google-pixel-8` | Pixel 8 (shiba) | 14–16 | Tested on Android 16 (`BP2A.250705.008`); auto-apply only on that build. |
| `samsung-sm-s918b` | Galaxy S23 Ultra (SM-S918B) | 13–16 | Tested on Android 14 (`UP1A.231005.007`); Samsung Free is the main ad surface; Knox is permanent. |
| `xiaomi-hyperos` | Xiaomi/Redmi/POCO HyperOS | 14–16 | Family profile; `auto_apply: false`; MSA/GetApps; region-specific names; re-check after OTA. |
| `generic-android` | Any Android 8+ | 8–16 | Reference only; no auto-apply. |
