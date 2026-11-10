#!/usr/bin/env python3
"""Send an opt-in checklist or feedback message to the CleanYourPhone Worker.

This is deliberately separate from ``tools/phone.py``: the CLI that touches
ADB stays local and network-free. This script only runs when a person asks for
it, shows exactly what will be sent, and requires ``--yes``.

Examples:
    python scripts/feedback.py --kind profile --checklist-file checklist.txt
    python scripts/feedback.py --yes --kind bug --message "Review screen ..."
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from typing import Any, Callable

DEFAULT_ENDPOINT = "https://cleanyourphone-feedback.subtitleme.workers.dev"
KINDS = ("feedback", "bug", "profile")
MAX_MESSAGE = 4000
MAX_CHECKLIST = 6000
MAX_CONTACT = 200

_IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_MAC_RE = re.compile(r"\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b")
_IMEI_RE = re.compile(r"\b\d{15}\b")
_SERIAL_RE = re.compile(r"(?im)^(\s*(?:serial|serialno|ro\.serialno)\s*[:=]\s*).+$")


def redact(text: str) -> str:
    """Remove the identifiers a feedback message must never contain."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    redacted = _IP_RE.sub("[redacted-ip]", text)
    redacted = _MAC_RE.sub("[redacted-mac]", redacted)
    redacted = _IMEI_RE.sub("[redacted-imei]", redacted)
    redacted = _SERIAL_RE.sub(r"\1[redacted-serial]", redacted)
    return redacted


def build_payload(
    *,
    kind: str,
    message: str,
    checklist: str,
    contact: str,
    app_version: str,
) -> dict[str, str]:
    if kind not in KINDS:
        raise ValueError(f"kind must be one of {', '.join(KINDS)}")
    message = redact(message).strip()
    checklist = redact(checklist).strip()
    contact = redact(contact).strip()
    if not message and not checklist:
        raise ValueError("a message or a checklist is required")
    if len(message) > MAX_MESSAGE:
        raise ValueError("message is too long")
    if len(checklist) > MAX_CHECKLIST:
        raise ValueError("checklist is too long")
    if len(contact) > MAX_CONTACT:
        raise ValueError("contact is too long")
    return {
        "kind": kind,
        "message": message,
        "checklist": checklist,
        "contact": contact,
        "app_version": app_version.strip(),
        "website": "",
    }


def send(
    payload: dict[str, Any],
    *,
    endpoint: str = DEFAULT_ENDPOINT,
    timeout: int = 20,
    opener: Callable[..., Any] | None = None,
) -> None:
    body = json.dumps(
        payload, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "CleanYourPhone-skill-feedback/1",
        },
    )
    open_request = opener or urllib.request.urlopen
    try:
        with open_request(request, timeout=timeout) as response:
            raw = response.read(4096)
    except urllib.error.HTTPError as error:
        if error.code == 429:
            raise RuntimeError(
                "rate limited; wait a few minutes and try again"
            ) from error
        if error.code == 503:
            raise RuntimeError("feedback is not configured") from error
        raise RuntimeError(f"feedback failed with HTTP {error.code}") from error
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        raise RuntimeError("could not reach the feedback service") from error

    try:
        parsed = json.loads(raw.decode("utf-8")) if raw else {}
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError("feedback service returned invalid JSON") from error
    if not isinstance(parsed, dict) or parsed.get("ok") is not True:
        raise RuntimeError("feedback service rejected the message")


def _read_checklist(path: str | None) -> str:
    if not path:
        return ""
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Send an opt-in CleanYourPhone checklist or feedback message."
    )
    parser.add_argument("--kind", choices=KINDS, default="feedback")
    parser.add_argument("--message", default="")
    parser.add_argument("--checklist", default="")
    parser.add_argument("--checklist-file")
    parser.add_argument("--contact", default="")
    parser.add_argument(
        "--app-version",
        default=os.environ.get("CLEANYOURPHONE_VERSION", "CleanYourPhone CLI"),
    )
    parser.add_argument(
        "--endpoint",
        default=os.environ.get(
            "CLEANYOURPHONE_FEEDBACK_URL", DEFAULT_ENDPOINT
        ),
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="actually send after showing the preview",
    )
    args = parser.parse_args(argv)

    checklist = args.checklist or _read_checklist(args.checklist_file)
    try:
        payload = build_payload(
            kind=args.kind,
            message=args.message,
            checklist=checklist,
            contact=args.contact,
            app_version=args.app_version,
        )
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    print("This is the exact message that will be sent:")
    print("")
    print(f"Kind: {payload['kind']}")
    print(f"Message: {payload['message'] or '(none)'}")
    print(f"Contact: {payload['contact'] or '(none)'}")
    print("Checklist:")
    print(payload["checklist"] or "(none)")
    print("")

    if not args.yes:
        print("Nothing sent. Re-run with --yes after the person approves.")
        return 2

    try:
        send(payload, endpoint=args.endpoint)
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print("Sent. Thank you.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
