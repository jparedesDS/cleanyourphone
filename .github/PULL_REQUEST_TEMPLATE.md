## What changed

<!-- One or two sentences. -->

## Why

<!-- The problem this solves. Link the issue if there is one. -->

## Safety impact

- [ ] No uninstall, `pm hide`, `pm clear` or `pm block`; the only state change is `pm disable-user`.
- [ ] No root, bootloader unlock, ROM, Magisk or Shizuku requirement.
- [ ] No package from `tools/protected.py` in `disable` or `ask`.
- [ ] No current dialer, SMS, Home or IME holder is disabled.
- [ ] No serial, IMEI, Android ID, MAC, account email, phone number or IP is committed.
- [ ] The change does not add telemetry or a third-party network call.
- [ ] `SKILL.md` safety rules were not weakened without an issue and maintainer review.

## How I tested

```text
python -m unittest discover -s tests -v
python tools/phone.py validate
python tools/phone.py profiles
```

<!-- Paste the relevant output. For a profile, include the model, Android build and the dump source. -->

## Profile checklist

<!-- Remove this section if the PR does not add or change a profile. -->

- [ ] `verification` is correct: `device` only with a real test, otherwise `documented` or `reference`.
- [ ] `documented` has `tested: []`, `disable: []`, `auto_apply: false`, sources and a non-empty `ask`.
- [ ] Every `ask` package appears in the firmware dump and has a real `why` and `breaks`.
- [ ] The fingerprint pins the firmware family and does not match an empty string.
- [ ] The profile is listed in `README.md`, `README.es.md` and `profiles/README.md`.
