# Security

CleanYourPhone runs shell commands on a phone that belongs to someone else. Treat that as a security
boundary, not a convenience.

## Reporting a problem

Do **not** open a public issue for:

- A package that the protected list misses and that can brick a phone or remove telephony.
- A way to make the CLI disable a role holder or a protected package.
- A command injection, path traversal or unsafe `adb` invocation.
- A profile that exposes a person's serial, IMEI, Android ID, MAC, Wi-Fi name, phone number, email
  or IP address.

Report it privately to the maintainers (open a draft security advisory on GitHub, or use the
contact in the repository profile). Include the phone model, Android version, the exact command and
the output, with identifiers redacted.

## Scope

In scope: `tools/`, `SKILL.md`, `PROMPT.md`, `profiles/`, and the install instructions.

Out of scope: a phone that was already modified, a custom ROM, a rooted device, a work/MDM device, or
a person who ignored the "back up first" rule. Those are documented as stop conditions.

## What the project will not do

- Add an override for the protected list.
- Add `pm uninstall`, `pm hide`, `pm clear`, root, Shizuku, or a ROM flasher.
- Add telemetry, analytics or a network call to the CLI.
- Publish device identifiers in a profile, a test or a screenshot.
