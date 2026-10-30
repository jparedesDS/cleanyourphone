# Simulated devices

The simulator is a **test harness**, not a device farm. It runs the real `phone.py` code against a
fake ADB transport and representative package sets, without a phone and without changing anything.

## What it proves

- Every one of the 157 profiles can produce a plan without crashing or malformed rows.
- `apply` refuses documented/family profiles and never runs without a backup.
- The protected list and current role holders cannot be disabled.
- A missing package is refused instead of guessed.
- `disable` and `apply` never exceed five packages per batch.
- A managed phone is refused.
- `restore` re-enables exactly the packages recorded by `apply`.
- A tablet with no telephony gets warnings, not failures.
- The fake transport records any unknown or dangerous command (`pm uninstall`, `pm hide`,
  `pm clear`, `fastboot`, `reboot`) and the tests fail if one appears.

## What it does not prove

It cannot prove that a package is safe on a real Samsung, Xiaomi, OnePlus or tablet firmware. It
does not see real OEM dependencies, re-enable behaviour after an OTA, boot loops, camera/banking/
notification regressions or battery changes. **A simulated profile is never promoted to `device`.**

## Run it

```bash
python -m unittest tests.test_simulation -v
```

The suite uses `tests/test_simulation.py`:

- Google Pixel 8, Samsung S23 Ultra and OnePlus 6T `device` scenarios.
- A documented Samsung tablet with no telephony.
- A family HyperOS profile that must refuse `apply`.
- Guardrail cases: protected package, role holder, missing package, six-package batch, managed
  phone, no backup.
- A sweep that runs `plan --json` for every profile in `profiles/`.

## Adding a scenario

Build a `FakeDevice` with the props, package set, roles, IME and settings of the model. Add a
`test_*` method using `with simulated(device):`. Do not mark the profile as `device` just because
the scenario passes; real-device testing is a separate checklist in `profiles/README.md`.
