# Profiles

A profile is either a **tested package list** for one model and firmware, or a **documented list**
built from a primary firmware dump. The skill uses it as a starting point, not as permission to
apply it silently.

A documented profile never auto-applies and never has a `disable` list. It exists to make the agent
ask the right questions with evidence, not to pretend the model was tested.

## Files

```text
profiles/
├── schema.json
├── google/pixel-6-pro.json
├── google/pixel-6.json
├── google/pixel-7.json
├── google/pixel-7a.json
├── google/pixel-8.json
├── samsung/on7xelte.json
├── samsung/sm-a022f.json
├── samsung/sm-a042f.json
├── samsung/sm-a065f.json
├── samsung/sm-a145f.json
├── samsung/sm-a146p.json
├── samsung/sm-a226b.json
├── samsung/sm-a245f.json
├── samsung/sm-a305f.json
├── samsung/sm-a325f.json
├── samsung/sm-a326b.json
├── samsung/sm-a505f.json
├── samsung/sm-a546e.json
├── samsung/sm-a576b.json
├── samsung/sm-a600fn.json
├── samsung/sm-a715f.json
├── samsung/sm-a725f.json
├── samsung/sm-e045f.json
├── samsung/sm-e055f.json
├── samsung/sm-e225f.json
├── samsung/sm-e236b.json
├── samsung/sm-e625f.json
├── samsung/sm-f707u1.json
├── samsung/sm-f916u.json
├── samsung/sm-g770f.json
├── samsung/sm-g780f.json
├── samsung/sm-g980f.json
├── samsung/sm-g981n.json
├── samsung/sm-g986b.json
├── samsung/sm-g988b.json
├── samsung/sm-g990b.json
├── samsung/sm-g991b.json
├── samsung/sm-g996b.json
├── samsung/sm-g998b.json
├── samsung/sm-j400f.json
├── samsung/sm-j720f.json
├── samsung/sm-m015g.json
├── samsung/sm-m105g.json
├── samsung/sm-m115f.json
├── samsung/sm-m136b.json
├── samsung/sm-m146b.json
├── samsung/sm-m325f.json
├── samsung/sm-m526b.json
├── samsung/sm-n970f.json
├── samsung/sm-n981b.json
├── samsung/sm-n986b.json
├── samsung/sm-p615.json
├── samsung/sm-s918b.json
├── samsung/sm-s938b.json
├── samsung/sm-t227u.json
├── samsung/sm-t500.json
├── samsung/sm-t505.json
├── samsung/sm-t577u.json
├── samsung/sm-t875.json
├── samsung/sm-t975.json
├── oneplus/README.md
├── oneplus/oneplus-5t.json
├── oneplus/oneplus-a6013.json
├── oneplus/oneplus-ac2003.json
├── oneplus/oneplus-cph2487.json
├── oneplus/oneplus-cph2719.json
├── oneplus/oneplus-hd1925.json
├── oneplus/oneplus-in2013.json
├── oneplus/oneplus-nord-ce.json
├── xiaomi/hyperos.json
├── xiaomi/xiaomi-11t-pro.json
├── xiaomi/xiaomi-11t.json
├── xiaomi/xiaomi-12-lite.json
├── xiaomi/xiaomi-12x.json
├── xiaomi/xiaomi-15-ultra.json
├── xiaomi/xiaomi-15t.json
├── xiaomi/xiaomi-17-ultra.json
├── xiaomi/xiaomi-civi.json
├── xiaomi/xiaomi-mi-10.json
├── xiaomi/xiaomi-mi-11-ultra.json
├── xiaomi/xiaomi-mi-9-se.json
├── xiaomi/xiaomi-mi-note-10.json
├── xiaomi/xiaomi-pad-6-pro.json
├── xiaomi/xiaomi-pad-6.json
├── redmi/redmi-10-5g.json
├── redmi/redmi-10.json
├── redmi/redmi-10a.json
├── redmi/redmi-10c.json
├── redmi/redmi-11-prime.json
├── redmi/redmi-12-5g.json
├── redmi/redmi-12.json
├── redmi/redmi-12c.json
├── redmi/redmi-13c-5g.json
├── redmi/redmi-15c.json
├── redmi/redmi-9-cattail.json
├── redmi/redmi-9.json
├── redmi/redmi-9c-nfc.json
├── redmi/redmi-9t-lime.json
├── redmi/redmi-9t.json
├── redmi/redmi-a1.json
├── redmi/redmi-a2.json
├── redmi/redmi-k20-pro-raphael.json
├── redmi/redmi-k20-pro.json
├── redmi/redmi-k20.json
├── redmi/redmi-k30-4g.json
├── redmi/redmi-k40-gaming.json
├── redmi/redmi-k40-pro.json
├── redmi/redmi-k40s.json
├── redmi/redmi-note-10-lite.json
├── redmi/redmi-note-10-mojito.json
├── redmi/redmi-note-10.json
├── redmi/redmi-note-10s.json
├── redmi/redmi-note-11-pro-5g.json
├── redmi/redmi-note-11-pro.json
├── redmi/redmi-note-11s.json
├── redmi/redmi-note-11t-5g.json
├── redmi/redmi-note-12-pro-5g.json
├── redmi/redmi-note-12-pro-speed.json
├── redmi/redmi-note-12s.json
├── redmi/redmi-note-13-5g.json
├── redmi/redmi-note-13-pro.json
├── redmi/redmi-note-13.json
├── redmi/redmi-note-13r.json
├── redmi/redmi-note-14-4g.json
├── redmi/redmi-note-15-5g.json
├── redmi/redmi-note-15-pro.json
├── redmi/redmi-note-15.json
├── redmi/redmi-note-17-pro-max-5g.json
├── redmi/redmi-note-7-pro.json
├── redmi/redmi-note-8-2021.json
├── redmi/redmi-note-8-pro.json
├── redmi/redmi-note-8.json
├── redmi/redmi-note-9-pro-gauguin.json
├── redmi/redmi-note-9-pro-joyeuse.json
├── redmi/redmi-note-9-pro-max.json
├── redmi/redmi-note-9-pro.json
├── redmi/redmi-note-9.json
├── redmi/redmi-pad-2.json
├── redmi/redmi-pad.json
├── redmi/redmi-turbo-5-max.json
├── redmi/redmi-y3.json
├── poco/poco-c31.json
├── poco/poco-f3.json
├── poco/poco-f5.json
├── poco/poco-f6.json
├── poco/poco-f9-ultra.json
├── poco/poco-m2-pro.json
├── poco/poco-m2.json
├── poco/poco-m3.json
├── poco/poco-m4-pro-5g.json
├── poco/poco-x2.json
├── poco/poco-x3-nfc.json
├── poco/poco-x3-pro.json
├── poco/poco-x5-5g.json
├── poco/poco-x6-pro-5g.json
├── poco/poco-x7-pro.json
├── poco/poco-x8-pro.json
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
  "verification": "device",
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

A documented profile looks like this:

```json
{
  "id": "samsung-sm-s938b",
  "brand": "Samsung",
  "model": "SM-S938B",
  "android": ["16"],
  "fingerprint_regex": "^samsung/pa3q",
  "auto_apply": false,
  "verification": "documented",
  "sources": [
    {
      "title": "Android Dumps: samsung/pa3q",
      "url": "https://gitlab.com/Android-Dumps/samsung/pa3q",
      "retrieved": "2026-10-29",
      "note": "Firmware dump"
    }
  ],
  "tested": [],
  "disable": [],
  "ask": [
    {"package": "com.samsung.android.app.spage", "why": "Samsung Free ads", "breaks": "Samsung Free"}
  ],
  "never": [
    {"package": "com.samsung.android.dialer", "why": "Dialer"}
  ],
  "notes": "Documented, not device-tested; no auto-apply."
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
| `verification` | `device` (real test), `documented` (primary firmware/documentation), or `reference` (generic). |
| `sources` | Required for `documented`: at least one `http(s)` URL with `title`, `url`, `retrieved` and optional `note`. |
| `auto_apply` | `false` for `documented` and `reference`. A `device` profile also needs the phone to run a build listed in `tested`. |
| `generic` | `true` for a reference profile. A generic profile cannot have a `disable` list and cannot be auto-applied. |
| `form_factor` | Optional: `phone` (default) or `tablet`. Tablet profiles keep the same rules; the CLI treats a missing dialer/SMS role as a warning. |
| `tested` | Required for `device`: the actual Android version, exact build, date, who. Empty for `documented` and `reference`. |
| `disable` | Packages tested on this model; low risk. Must be empty for `documented` and `reference`. |
| `ask` | User-facing or dependency-heavy; ask per package. A documented profile needs a non-empty `ask` list. |
| `never` | Per-model additions to the global protected list. |
| `notes` | What is specific: region, carrier, OTA behaviour, known breakage. |

## Rules

1. **A `device` profile needs a real test.** Say which build, which region, and what you checked
   afterwards (call, SMS, camera, keyboard, Home, Play, notifications). A profile is not a list
   copied from a forum. If you only have a firmware dump, use `documented` instead and do not claim
   a test.
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
9. **Documented means evidence, not a shopping list.** Every `ask` package must appear in the dump
   (`all_files.txt`, a permission XML, or an APK path). `disable` must be empty, `tested` must be
   empty, `auto_apply` must be false, and `sources` must include the dump.
10. **Generate, then curate.** `scripts/dump_inventory.py` produces a draft and a candidate list.
    A human must write every `why`/`breaks` and remove the `_draft` block before committing.

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
section, verification rules, source URLs, and that a documented/generic profile has no `disable`
list. It does not replace a real test.

## Current profiles

| ID | Model | Android | Verification | Notes |
|---|---|---|---|---|
| `google-pixel-8` | Pixel 8 (shiba) | 14–16 | device | Tested on Android 16 (`BP2A.250705.008`); auto-apply only on that build. |
| `google-pixel-6` | Pixel 6 (oriole) | 12 | documented | Android 12 dump; ask only, no auto-apply. |
| `google-pixel-6-pro` | Pixel 6 Pro (raven) | 12 | documented | Android 12 dump; ask only, no auto-apply. |
| `google-pixel-7` | Pixel 7 (panther) | 13 | documented | Android 13 dump; ask only, no auto-apply. |
| `google-pixel-7a` | Pixel 7a (lynx) | 13 | documented | Android 13 dump; ask only, no auto-apply. |
| `samsung-sm-s918b` | Galaxy S23 Ultra (SM-S918B) | 13–16 | device | Tested on Android 14 (`UP1A.231005.007`); Samsung Free is the main ad surface; Knox is permanent. |
| `samsung-sm-a022f` | Galaxy A02 (SM-A022F) | 11 | documented | From the `A02` firmware dump; ask only, no auto-apply. |
| `samsung-sm-a042f` | Galaxy A04e (SM-A042F) | 14 | documented | From the `a04e` firmware dump; ask only, no auto-apply. |
| `samsung-sm-a065f` | Galaxy A06 (SM-A065F) | 16 | documented | From the `a06` firmware dump; ask only, no auto-apply. |
| `samsung-sm-a145f` | Galaxy A14 (SM-A145F) | 13 | documented | From the `a14` firmware dump; ask only, no auto-apply. |
| `samsung-sm-a146p` | Galaxy A14 5G (SM-A146P) | 14 | documented | From the `a14xm` firmware dump; ask only, no auto-apply. |
| `samsung-sm-a226b` | Galaxy A22 5G (SM-A226B) | 13 | documented | From the `a22x` firmware dump; ask only, no auto-apply. |
| `samsung-sm-a245f` | Galaxy A24 (SM-A245F) | 13 | documented | From the `a24` firmware dump; ask only, no auto-apply. |
| `samsung-sm-a305f` | Galaxy A30 (SM-A305F) | 11 | documented | From the `a30` firmware dump; ask only, no auto-apply. |
| `samsung-sm-a325f` | Galaxy A32 (SM-A325F) | 13 | documented | From the `a32` firmware dump; ask only, no auto-apply. |
| `samsung-sm-a326b` | Galaxy A32 5G (SM-A326B) | 13 | documented | From the `a32x` firmware dump; ask only, no auto-apply. |
| `samsung-sm-a505f` | Galaxy A50 (SM-A505F) | 11 | documented | From the `a50` firmware dump; ask only, no auto-apply. |
| `samsung-sm-a546e` | Galaxy A54 5G (SM-A546E) | 13 | documented | From the `a54x` firmware dump; ask only, no auto-apply. |
| `samsung-sm-a576b` | Galaxy A57 5G (SM-A576B) | 16 | documented | From the `a57x` firmware dump; ask only, no auto-apply. |
| `samsung-sm-a600fn` | Galaxy A6 (2018) (SM-A600FN) | 10 | documented | From the `a6lte` firmware dump; ask only, no auto-apply. |
| `samsung-sm-a715f` | Galaxy A71 (SM-A715F) | 12 | documented | From the `a71` firmware dump; ask only, no auto-apply. |
| `samsung-sm-a725f` | Galaxy A72 (SM-A725F) | 12 | documented | From the `a72q` firmware dump; ask only, no auto-apply. |
| `samsung-sm-e045f` | Galaxy F04 (SM-E045F) | 13 | documented | From the `m04` firmware dump; ask only, no auto-apply. |
| `samsung-sm-e055f` | Galaxy F05 (SM-E055F) | 16 | documented | From the `a05m` firmware dump; ask only, no auto-apply. |
| `samsung-sm-e225f` | Galaxy F22 (SM-E225F) | 12 | documented | From the `f22` firmware dump; ask only, no auto-apply. |
| `samsung-sm-e236b` | Galaxy F23 5G (SM-E236B) | 12 | documented | From the `m23xq` firmware dump; ask only, no auto-apply. |
| `samsung-sm-e625f` | Galaxy F62 (SM-E625F) | 12 | documented | From the `f62` firmware dump; ask only, no auto-apply. |
| `samsung-sm-j400f` | Galaxy J4 (SM-J400F) | 10 | documented | From the `j4lte` firmware dump; ask only, no auto-apply. |
| `samsung-sm-j720f` | Galaxy J7 Duo (SM-J720F) | 10 | documented | From the `j7duolte` firmware dump; ask only, no auto-apply. |
| `samsung-on7xelte` | Galaxy J7 Prime (`on7xelte`) | 8 | documented | From the `on7xelte` firmware dump; ask only, no auto-apply. |
| `samsung-sm-m015g` | Galaxy M01 (SM-M015G) | 11 | documented | From the `m01q` firmware dump; ask only, no auto-apply. |
| `samsung-sm-m105g` | Galaxy M10 (SM-M105G) | 10 | documented | From the `m10lte` firmware dump; ask only, no auto-apply. |
| `samsung-sm-m115f` | Galaxy M11 (SM-M115F) | 11 | documented | From the `m11q` firmware dump; ask only, no auto-apply. |
| `samsung-sm-m136b` | Galaxy M13 5G (SM-M136B) | 14 | documented | From the `a13x` firmware dump; ask only, no auto-apply. |
| `samsung-sm-m146b` | Galaxy M14 5G (SM-M146B) | 13 | documented | From the `essi` firmware dump; ask only, no auto-apply. |
| `samsung-sm-m325f` | Galaxy M32 (SM-M325F) | 11 | documented | From the `m32` firmware dump; ask only, no auto-apply. |
| `samsung-sm-m526b` | Galaxy M52 5G (SM-M526B) | 12 | documented | From the `m52xq` firmware dump; ask only, no auto-apply. |
| `samsung-sm-n970f` | Galaxy Note10 (SM-N970F) | 12 | documented | From the `d1` firmware dump; ask only, no auto-apply. |
| `samsung-sm-n981b` | Galaxy Note20 (SM-N981B) | 12 | documented | From the `c1s` firmware dump; ask only, no auto-apply. |
| `samsung-sm-n986b` | Galaxy Note20 Ultra (SM-N986B) | 12 | documented | From the `c2s` firmware dump; ask only, no auto-apply. |
| `samsung-sm-g770f` | Galaxy S10 Lite (SM-G770F) | 13 | documented | From the `r5q` firmware dump; ask only, no auto-apply. |
| `samsung-sm-g980f` | Galaxy S20 (SM-G980F) | 12 | documented | From the `x1s` firmware dump; ask only, no auto-apply. |
| `samsung-sm-g981n` | Galaxy S20 (SM-G981N) | 12 | documented | From the `x1q` firmware dump; ask only, no auto-apply. |
| `samsung-sm-g780f` | Galaxy S20 FE (SM-G780F) | 13 | documented | From the `r8s` firmware dump; ask only, no auto-apply. |
| `samsung-sm-g988b` | Galaxy S20 Ultra (SM-G988B) | 12 | documented | From the `z3s` firmware dump; ask only, no auto-apply. |
| `samsung-sm-g986b` | Galaxy S20+ (SM-G986B) | 12 | documented | From the `y2s` firmware dump; ask only, no auto-apply. |
| `samsung-sm-g991b` | Galaxy S21 (SM-G991B) | 12 | documented | From the `o1s` firmware dump; ask only, no auto-apply. |
| `samsung-sm-g990b` | Galaxy S21 FE (SM-G990B) | 12 | documented | From the `r9q` firmware dump; ask only, no auto-apply. |
| `samsung-sm-g998b` | Galaxy S21 Ultra (SM-G998B) | 12 | documented | From the `p3s` firmware dump; ask only, no auto-apply. |
| `samsung-sm-g996b` | Galaxy S21+ (SM-G996B) | 12 | documented | From the `t2s` firmware dump; ask only, no auto-apply. |
| `samsung-sm-s938b` | Galaxy S25 Ultra (SM-S938B) | 16 | documented | From the `pa3q` firmware dump; ask only, no auto-apply. |
| `samsung-sm-t500` | Galaxy Tab A7 10.4 (SM-T500) | 11 | documented | Tablet; From the `gta4lwifi` firmware dump; ask only, no auto-apply. |
| `samsung-sm-t505` | Galaxy Tab A7 10.4 (SM-T505) | 12 | documented | Tablet; From the `gta4l` firmware dump; ask only, no auto-apply. |
| `samsung-sm-t227u` | Galaxy Tab A7 Lite (SM-T227U) | 11 | documented | Tablet; From the `gta7lite` firmware dump; ask only, no auto-apply. |
| `samsung-sm-t577u` | Galaxy Tab Active3 (SM-T577U) | 13 | documented | Tablet; From the `gtactive3` firmware dump; ask only, no auto-apply. |
| `samsung-sm-p615` | Galaxy Tab S6 Lite (SM-P615) | 13 | documented | Tablet; From the `gta4xl` firmware dump; ask only, no auto-apply. |
| `samsung-sm-t875` | Galaxy Tab S7 (SM-T875) | 13 | documented | Tablet; From the `gts7l` firmware dump; ask only, no auto-apply. |
| `samsung-sm-t975` | Galaxy Tab S7+ (SM-T975) | 13 | documented | Tablet; From the `gts7xl` firmware dump; ask only, no auto-apply. |
| `samsung-sm-f707u1` | Galaxy Z Flip 5G (SM-F707U1) | 13 | documented | From the `bloomxq` firmware dump; ask only, no auto-apply. |
| `samsung-sm-f916u` | Galaxy Z Fold2 (SM-F916U) | 13 | documented | From the `f2q` firmware dump; ask only, no auto-apply. |
| `oneplus-a6013` | OnePlus 6T (ONEPLUS A6013) | 11 | device | Tested on OxygenOS 11.1.2.2 build `ONEPLUS A6013_41_211125`; 8 low-risk telemetry packages in `disable`, user-facing apps in `ask`. |
| `oneplus-cph2487` | OnePlus 11R 5G (CPH2487) | 16 | documented | From the `OP5961L1` firmware dump; ask only, no auto-apply. |
| `oneplus-5t` | OnePlus 5T (`OnePlus5T`) | 10 | documented | From the `OnePlus5T` firmware dump; ask only, no auto-apply. |
| `oneplus-hd1925` | OnePlus 7T Pro 5G McLaren (HD1925) | 11 | documented | From the `OnePlus7TProNR` firmware dump; ask only, no auto-apply. |
| `oneplus-in2013` | OnePlus 8 (IN2013) | 11 | documented | From the `OnePlus8` firmware dump; ask only, no auto-apply. |
| `oneplus-ac2003` | OnePlus Nord (AC2003) | 11 | documented | From the `Nord` firmware dump; ask only, no auto-apply. |
| `oneplus-nord-ce` | OnePlus Nord CE 5G (`OnePlusNordCE`) | 11 | documented | Regional model numbers; fingerprint-pinned family profile; ask only. |
| `oneplus-cph2719` | OnePlus Nord CE5 (CPH2719) | 16 | documented | From the `OP613BL1` firmware dump; ask only, no auto-apply. |
| `xiaomi-hyperos` | Xiaomi/Redmi/POCO HyperOS | 14–16 | device | Family profile; `auto_apply: false`; MSA/GetApps; region-specific names; re-check after OTA. |
| `xiaomi-mi-10` | Mi 10 | 12 | documented | From the `umi` firmware dump; ask only, no auto-apply. |
| `xiaomi-mi-11-ultra` | Mi 11 Ultra (`star`) | 12 | documented | From the `star` firmware dump; ask only, no auto-apply. |
| `xiaomi-mi-9-se` | Mi 9 SE (`grus`) | 10 | documented | From the `grus` firmware dump; ask only, no auto-apply. |
| `xiaomi-mi-note-10` | tucana | 11 | documented | From the `tucana` firmware dump; ask only, no auto-apply. |
| `xiaomi-11t` | Xiaomi 11T (`agate`) | 14 | documented | From the `agate` firmware dump; ask only, no auto-apply. |
| `xiaomi-11t-pro` | Xiaomi 11T Pro (2107113SC) | 13 | documented | From the `vili` firmware dump; ask only, no auto-apply. |
| `xiaomi-12-lite` | Xiaomi 12 Lite (2203129C) | 13 | documented | From the `taoyao` firmware dump; ask only, no auto-apply. |
| `xiaomi-12x` | Xiaomi 12X (2112123AG) | 12 | documented | From the `psyche` firmware dump; ask only, no auto-apply. |
| `xiaomi-15-ultra` | Xiaomi 15 Ultra (25010PN30G) | 16 | documented | From the `xuanyuan` firmware dump; ask only, no auto-apply. |
| `xiaomi-15t` | Xiaomi 15T (25069PTEBG) | 16 | documented | From the `goya` firmware dump; ask only, no auto-apply. |
| `xiaomi-17-ultra` | Xiaomi 17 Ultra (2512BPNDAG) | 16 | documented | From the `nezha` firmware dump; ask only, no auto-apply. |
| `xiaomi-civi` | Xiaomi Civi (2109119BC) | 12 | documented | From the `mona` firmware dump; ask only, no auto-apply. |
| `xiaomi-pad-6` | Xiaomi Pad 6 (23043RP34C) | 13 | documented | Tablet; From the `pipa` firmware dump; ask only, no auto-apply. |
| `xiaomi-pad-6-pro` | Xiaomi Pad 6 Pro (23046RP50C) | 13 | documented | Tablet; From the `liuqin` firmware dump; ask only, no auto-apply. |
| `redmi-10` | Redmi 10 (21061119AG) | 13 | documented | From the `selene` firmware dump; ask only, no auto-apply. |
| `redmi-10-5g` | Redmi 10 5G / Redmi 11 Prime 5G (22041219G) | 14 | documented | From the `light` firmware dump; ask only, no auto-apply. |
| `redmi-10a` | Redmi 10A (220233L2G) | 11 | documented | From the `dandelion` firmware dump; ask only, no auto-apply. |
| `redmi-10c` | Redmi 10C (`fog`) | 12 | documented | From the `fog` firmware dump; ask only, no auto-apply. |
| `redmi-11-prime` | Redmi 11 Prime (22071219AI) | 14 | documented | From the `rock` firmware dump; ask only, no auto-apply. |
| `redmi-12` | Redmi 12 (`fire`) | 14 | documented | From the `fire` firmware dump; ask only, no auto-apply. |
| `redmi-12-5g` | Redmi 12 5G (`sky`) | 15 | documented | From the `sky` firmware dump; ask only, no auto-apply. |
| `redmi-12c` | Redmi 12C (22120RN86C) | 14 | documented | From the `earth` firmware dump; ask only, no auto-apply. |
| `redmi-13c-5g` | Redmi 13C 5G / Redmi 13R 5G (`air`) | 15 | documented | From the `air` firmware dump; ask only, no auto-apply. |
| `redmi-15c` | Redmi 15C (`dew`) | 16 | documented | Also sold as POCO C85 in some regions; fingerprint-pinned family profile; ask only. |
| `redmi-9-cattail` | Redmi 9 (M2006C3MII) | 11 | documented | From the `cattail` firmware dump; ask only, no auto-apply. |
| `redmi-9` | Redmi 9 / Redmi 9 Prime (`lancelot`) | 12 | documented | From the `lancelot` firmware dump; ask only, no auto-apply. |
| `redmi-9c-nfc` | Redmi 9C NFC (M2006C3MNG) | 11 | documented | From the `angelican` firmware dump; ask only, no auto-apply. |
| `redmi-9t` | Redmi 9T (M2010J19SL) | 12 | documented | From the `lime` firmware dump; ask only, no auto-apply. |
| `redmi-9t-lime` | Redmi 9T / Redmi 9 Power (`lime`) | 10 | documented | From the `lime` firmware dump; ask only, no auto-apply. |
| `redmi-a1` | Redmi A1 (`ice`) | 12 | documented | From the `ice` firmware dump; ask only, no auto-apply. |
| `redmi-a2` | Redmi A2+ (`water`) | 13 | documented | From the `water` firmware dump; ask only, no auto-apply. |
| `redmi-k20` | Redmi K20 (`davinciin`) | 11 | documented | From the `davinciin` firmware dump; ask only, no auto-apply. |
| `redmi-k20-pro-raphael` | raphael | 11 | documented | From the `raphael` firmware dump; ask only, no auto-apply. |
| `redmi-k20-pro` | Redmi K20 Pro (`raphaelin`) | 10 | documented | From the `raphaelin` firmware dump; ask only, no auto-apply. |
| `redmi-k30-4g` | Redmi K30 4G (`phoenix`) | 12 | documented | From the `phoenix` firmware dump; ask only, no auto-apply. |
| `redmi-k40-gaming` | Redmi K40 Gaming (`ares`) | 12 | documented | From the `ares` firmware dump; ask only, no auto-apply. |
| `redmi-k40-pro` | Redmi K40 Pro (M2012K11C) | 12 | documented | From the `haydn` firmware dump; ask only, no auto-apply. |
| `redmi-k40s` | Redmi K40S (22021211RC) | 13 | documented | From the `munch` firmware dump; ask only, no auto-apply. |
| `redmi-note-10` | Redmi Note 10 (M2103K19C) | 12 | documented | From the `camellia` firmware dump; ask only, no auto-apply. |
| `redmi-note-10-mojito` | Redmi Note 10 (`mojito`) | 12 | documented | From the `mojito` firmware dump; ask only, no auto-apply. |
| `redmi-note-10-lite` | curtana | 11 | documented | From the `curtana` firmware dump; ask only, no auto-apply. |
| `redmi-note-10s` | Redmi Note 10S (`rosemary`) | 13 | documented | From the `rosemary` firmware dump; ask only, no auto-apply. |
| `redmi-note-11-pro` | Redmi Note 11 Pro (`pissarro`) | 13 | documented | From the `pissarro` firmware dump; ask only, no auto-apply. |
| `redmi-note-11-pro-5g` | Redmi Note 11 Pro 5G (2201116SG) | 13 | documented | From the `veux` firmware dump; ask only, no auto-apply. |
| `redmi-note-11s` | Redmi Note 11S (`fleur`) | 13 | documented | From the `fleur` firmware dump; ask only, no auto-apply. |
| `redmi-note-11t-5g` | Redmi Note 11T 5G (`evergo`) | 13 | documented | From the `evergo` firmware dump; ask only, no auto-apply. |
| `redmi-note-12-pro-5g` | Redmi Note 12 Pro 5G (`ruby`) | 14 | documented | From the `ruby` firmware dump; ask only, no auto-apply. |
| `redmi-note-12-pro-speed` | Redmi Note 12 Pro Speed (22101320C) | 13 | documented | From the `redwood` firmware dump; ask only, no auto-apply. |
| `redmi-note-12s` | Redmi Note 12S (`sea`) | 15 | documented | From the `sea` firmware dump; ask only, no auto-apply. |
| `redmi-note-13` | Redmi Note 13 (`sapphire`) | 15 | documented | From the `sapphire` firmware dump; ask only, no auto-apply. |
| `redmi-note-13-5g` | Redmi Note 13 5G (`gold`) | 15 | documented | From the `gold` firmware dump; ask only, no auto-apply. |
| `redmi-note-13-pro` | Redmi Note 13 Pro (`emerald`) | 15 | documented | From the `emerald` firmware dump; ask only, no auto-apply. |
| `redmi-note-13r` | Redmi Note 13R (2406ERN9CC) | 16 | documented | From the `breeze` firmware dump; ask only, no auto-apply. |
| `redmi-note-14-4g` | Redmi Note 14 4G (`tanzanite`) | 16 | documented | Regional model numbers; fingerprint-pinned family profile; ask only. |
| `redmi-note-15` | Redmi Note 15 (`spinel`) | 16 | documented | Regional model numbers; fingerprint-pinned family profile; ask only. |
| `redmi-note-15-5g` | Redmi Note 15 5G (`kunzite`) | 16 | documented | From the `kunzite` firmware dump; ask only, no auto-apply. |
| `redmi-note-15-pro` | Redmi Note 15 Pro (`lapis`) | 16 | documented | Regional model numbers; fingerprint-pinned family profile; ask only. |
| `redmi-note-17-pro-max-5g` | Redmi Note 17 Pro Max 5G (`brussels`) | 16 | documented | From the `brussels` firmware dump; ask only, no auto-apply. |
| `redmi-note-7-pro` | Redmi Note 7 Pro (`violet`) | 10 | documented | From the `violet` firmware dump; ask only, no auto-apply. |
| `redmi-note-8` | Redmi Note 8 (`ginkgo`) | 11 | documented | From the `ginkgo` firmware dump; ask only, no auto-apply. |
| `redmi-note-8-2021` | Redmi Note 8 (2021) (`biloba`) | 11 | documented | From the `biloba` firmware dump; ask only, no auto-apply. |
| `redmi-note-8-pro` | Redmi Note 8 Pro (`begonia`) | 11 | documented | From the `begonia` firmware dump; ask only, no auto-apply. |
| `redmi-note-9` | Redmi Note 9 (`merlin`) | 12 | documented | From the `merlin` firmware dump; ask only, no auto-apply. |
| `redmi-note-9-pro-joyeuse` | joyeuse | 12 | documented | From the `joyeuse` firmware dump; ask only, no auto-apply. |
| `redmi-note-9-pro-gauguin` | Redmi Note 9 Pro (`gauguin`) | 12 | documented | From the `gauguin` firmware dump; ask only, no auto-apply. |
| `redmi-note-9-pro` | Redmi Note 9 Pro / Redmi Note 9S (`miatoll`) | 12 | documented | From the `miatoll` firmware dump; ask only, no auto-apply. |
| `redmi-note-9-pro-max` | excalibur | 11 | documented | From the `excalibur` firmware dump; ask only, no auto-apply. |
| `redmi-pad` | Redmi Pad (22081283G) | 12 | documented | Tablet; From the `yunluo` firmware dump; ask only, no auto-apply. |
| `redmi-pad-2` | Redmi Pad 2 (`taiko`) | 16 | documented | Tablet; From the `taiko` firmware dump; ask only, no auto-apply. |
| `redmi-turbo-5-max` | REDMI Turbo 5 Max (2602BRT18C) | 16 | documented | From the `dash` firmware dump; ask only, no auto-apply. |
| `redmi-y3` | Redmi Y3 (`onc`) | 10 | documented | From the `onc` firmware dump; ask only, no auto-apply. |
| `poco-c31` | POCO C31 (211033MI) | 11 | documented | From the `angelicain` firmware dump; ask only, no auto-apply. |
| `poco-f3` | POCO F3 (M2012K11AG) | 12 | documented | From the `alioth` firmware dump; ask only, no auto-apply. |
| `poco-f5` | POCO F5 (`marble`) | 15 | documented | From the `marble` firmware dump; ask only, no auto-apply. |
| `poco-f6` | POCO F6 (24069PC21G) | 16 | documented | From the `peridot` firmware dump; ask only, no auto-apply. |
| `poco-f9-ultra` | POCO F9 Ultra (26077PC53G) | 16 | documented | From the `songyuan` firmware dump; ask only, no auto-apply. |
| `poco-m2` | POCO M2 (M2004J19PI) | 11 | documented | From the `shiva` firmware dump; ask only, no auto-apply. |
| `poco-m2-pro` | gram | 11 | documented | From the `gram` firmware dump; ask only, no auto-apply. |
| `poco-m3` | POCO M3 (M2010J19CG) | 12 | documented | From the `citrus` firmware dump; ask only, no auto-apply. |
| `poco-m4-pro-5g` | POCO M4 Pro 5G (`evergreen`) | 13 | documented | From the `evergreen` firmware dump; ask only, no auto-apply. |
| `poco-x2` | POCO X2 (`phoenixin`) | 11 | documented | From the `phoenixin` firmware dump; ask only, no auto-apply. |
| `poco-x3-nfc` | POCO X3 NFC (M2007J20CG) | 12 | documented | From the `surya` firmware dump; ask only, no auto-apply. |
| `poco-x3-pro` | POCO X3 Pro (vayu_in) | 12 | documented | From the `vayu` firmware dump; ask only, no auto-apply. |
| `poco-x5-5g` | POCO X5 5G (22111317PI) | 12 | documented | From the `moonstone` firmware dump; ask only, no auto-apply. |
| `poco-x6-pro-5g` | POCO X6 Pro 5G (2311DRK48G) | 16 | documented | From the `duchamp` firmware dump; ask only, no auto-apply. |
| `poco-x7-pro` | POCO X7 Pro (2412DPC0AG) | 16 | documented | From the `rodin` firmware dump; ask only, no auto-apply. |
| `poco-x8-pro` | POCO X8 Pro (2511FPC34G) | 16 | documented | From the `klee` firmware dump; ask only, no auto-apply. |
| `generic-android` | Any Android 8+ | 8–16 | reference | Reference only; no auto-apply. |
