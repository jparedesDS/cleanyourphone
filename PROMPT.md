# The prompt

Paste this into Claude Code, Codex, Cursor, Gemini CLI, OpenCode or any coding agent with shell
access, on a computer connected to the phone by USB. It works on Android phones and tablets
(Android 8 and newer). It does **not** work on iPhones, Android TV boxes, or a managed/work phone.

Before you start, on the phone: Settings → About phone → tap **Build number** 7 times → back →
**Developer options** → turn on **USB debugging**. Connect the phone by USB and accept the
**Allow USB debugging?** prompt. Keep the phone unlocked and charged above 30%.

If you cloned this repo, mention it: the agent can use `tools/phone.py`, `profiles/` and
`docs/` instead of writing its own commands.

---

I want to clean my Android phone: disable preinstalled apps, ads and telemetry, and improve battery
life, without root and without uninstalling anything. My phone is: **<MODEL HERE>**.

Read `SKILL.md` from this repo and follow it exactly. If you cannot read it, stop and ask me to paste
it; do not improvise. Work on the real phone, step by step, and show me the plan before changing
anything.

The non-negotiables:

- **Disable, never uninstall.** Only `pm disable-user --user 0`, one package per shell call. No
  `pm uninstall`, no `pm hide`, no `pm clear`, no root, no ROM, no factory reset.
- **Back up first.** Run `python tools/phone.py backup` before the first change. Tell me where it is.
- **Never disable a protected package.** The list is in `tools/protected.py` and `docs/SAFETY.md`.
  If a package is on it, refuse. No override.
- **Never leave me without a dialer, SMS app, Home app or keyboard.** Check the role holders before
  disabling any of them, and check again after every batch.
- **Ask me before anything I use**: banking, payments, WhatsApp, camera, gallery, alarm, VPN,
  password manager, authenticator, smartwatch, eSIM, VoLTE/Wi-Fi calling, hotspot, accessibility,
  work apps. Give me one checklist and disable only what I do not tick.
- **Small batches, verify between.** At most 5 packages per batch, then `python tools/phone.py
  verify`. If anything fails, re-enable the batch and stop.
- **Reboot once at the end, wait, and verify again.** Some phones re-enable packages at boot; note
  those instead of fighting them.
- **Close ADB when done.** Turn off Wireless debugging and USB debugging, revoke authorisations, and
  confirm `adb devices` no longer lists my phone.
- **Speak to me in my language.** If I write in Spanish, answer in Spanish.

Start by asking me the questions in the "First response" section of `SKILL.md`, then connect with
`adb devices -l` and run `python tools/phone.py doctor` and `python tools/phone.py probe`.

When you finish, give me: the backup path, the list of packages you disabled and why, what you kept
and why, the DNS state, the battery baseline if we measured one, and the exact undo command
(`python tools/phone.py restore`).
