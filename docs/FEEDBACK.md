# Feedback and profile requests

CleanYourPhone has an optional feedback path for bugs, improvements and phone
profile requests. It is **not telemetry**. Nothing is sent at startup, during a
scan, during a backup, or while applying changes. A message leaves the computer
only when a person presses **Send** in the app or web form, or runs the separate
feedback script with `--yes`.

The skill and the CLI stay local. `tools/phone.py` never makes a network call.

## What is sent

```json
{
  "kind": "feedback",
  "message": "The review screen could explain ...",
  "checklist": "Phone: ...\nAndroid: ...\nBuild: ...",
  "contact": "optional Discord/GitHub/email",
  "app_version": "CleanYourPhone app 0.2.0",
  "website": ""
}
```

`kind` is `feedback`, `bug` or `profile`. The checklist should contain the model,
Android version, build, fingerprint and profile id. It must never contain a
serial number, IP address, IMEI, MAC address, account email or pairing code.

The Worker hashes the source IP with a secret salt to rate-limit abuse. It does
not store the IP, the message or the checklist.

## App and website

- In the app: **Feedback** in the header. The checklist is prefilled from the
  current session; every field is editable.
- On the website: the **Feedback** section. The form is sent only when the
  consent box is checked and **Send feedback** is pressed.
- The app and website post to the same Cloudflare Worker. You need the public
  Worker URL configured in the app and website; see
  `cleanyourphone-web/feedback-worker/README.md`.

## Skill

Show the checklist to the person and ask for explicit permission first. Then:

```bash
python scripts/feedback.py --kind profile --checklist-file checklist.txt
# Review the preview. If it is correct:
python scripts/feedback.py --yes --kind profile --checklist-file checklist.txt
```

Or send a short improvement message:

```bash
python scripts/feedback.py --yes --kind feedback --message "Please explain ..."
```

Useful options:

| Option | Meaning |
|---|---|
| `--kind feedback\|bug\|profile` | What kind of message this is |
| `--message TEXT` | Short message |
| `--checklist TEXT` | Inline checklist |
| `--checklist-file PATH` | Read the checklist from a file |
| `--contact TEXT` | Optional contact, visible to the maintainer |
| `--endpoint URL` | Override the Worker URL |
| `--yes` | Actually send; without it the script only prints the preview |

The script redacts IPv4 addresses, MAC addresses, 15-digit IMEI numbers and
`serial:`/`ro.serialno` values before previewing. Always read the preview: a
model name or a custom text field can still contain something private.

## Discord

The maintainer receives the message through a private Discord webhook stored as
a Worker secret. The webhook is never included in the app, the website or this
repository. To deploy or move the Worker, follow
`cleanyourphone-web/feedback-worker/README.md`.

## Limits

- The Worker accepts at most 16 KB per request.
- Messages are capped at 4,000 characters; checklists at 6,000.
- One request per hashed IP per five minutes.
- A honeypot field blocks simple bots.
- The Worker returns `503` when the Discord webhook is not configured.
