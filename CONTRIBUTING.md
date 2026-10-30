# Contributing

Thanks for helping. CleanYourPhone is a safety product first: a change that makes the skill longer
without making it safer or clearer is probably a bad change.

## Before you start

- Read [AGENTS.md](AGENTS.md) for the hard rules and the repo map.
- Read [docs/SAFETY.md](docs/SAFETY.md), [docs/FAQ.md](docs/FAQ.md) and
  [profiles/README.md](profiles/README.md).
- For a new model, open a **Profile request** issue with the primary source or the real-device test.
- For a change to the protected list, role checks or `SKILL.md` safety rules, open an issue first.

## What we accept

- New `documented` profiles built from a primary firmware dump, with every `ask` package verified.
- New `device` profiles only with a real test on an exact build and a completed checklist.
- CLI fixes that make the guardrails stronger or the output clearer.
- Documentation, translations and website fixes.

## What we do not accept

- Uninstall, root, custom ROM, bootloader unlock, Magisk or Shizuku as a requirement.
- A package from `tools/protected.py` in `disable` or `ask`.
- Copy-pasted package lists, forum lists without evidence, or profiles that claim a test that did
  not happen.
- Telemetry, analytics, third-party API calls or secrets/identifiers in the repo.

## Run the checks

```bash
python -m unittest discover -s tests -v
python tools/phone.py validate
python tools/phone.py profiles
python scripts/dump_inventory.py --help
```

No phone is needed for the test suite. Use [scripts/collect_device.ps1](scripts/collect_device.ps1)
if you have a real device and want to contribute an inventory.

## Commit and PR style

- Titles: `area: what changed`, for example `profiles: add Samsung SM-S918B`,
  `tools: refuse to disable a role holder`, `docs: explain the Private DNS undo`.
- The body says what changed, the model/Android build it was tested on, and the command used.
- One topic per PR. A profile and a tool fix for that same model may be one PR.
- Contributions are MIT.
