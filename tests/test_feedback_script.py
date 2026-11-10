"""The opt-in feedback helper: redaction, preview and explicit --yes."""

import contextlib
import io
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import feedback  # noqa: E402


class FeedbackScriptTests(unittest.TestCase):
    def test_redacts_common_identifiers(self):
        text = (
            "serial: ABC123\n"
            "ro.serialno=XYZ\n"
            "IP 192.168.1.10\n"
            "MAC aa:bb:cc:dd:ee:ff\n"
            "IMEI 123456789012345\n"
            "Build: ONEPLUS A6013_41_211125"
        )
        redacted = feedback.redact(text)
        self.assertNotIn("ABC123", redacted)
        self.assertNotIn("XYZ", redacted)
        self.assertNotIn("192.168.1.10", redacted)
        self.assertNotIn("aa:bb:cc:dd:ee:ff", redacted)
        self.assertNotIn("123456789012345", redacted)
        self.assertIn("ONEPLUS A6013_41_211125", redacted)

    def test_payload_requires_a_message_or_checklist(self):
        with self.assertRaises(ValueError):
            feedback.build_payload(
                kind="feedback",
                message="",
                checklist="",
                contact="",
                app_version="test",
            )

    def test_payload_rejects_an_unknown_kind(self):
        with self.assertRaises(ValueError):
            feedback.build_payload(
                kind="other",
                message="hello",
                checklist="",
                contact="",
                app_version="test",
            )

    def test_send_posts_json(self):
        response = mock.MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = b'{"ok":true}'
        opener = mock.Mock(return_value=response)
        feedback.send(
            {"kind": "feedback", "message": "hello", "website": ""},
            endpoint="https://feedback.test",
            opener=opener,
        )
        request = opener.call_args.args[0]
        self.assertEqual(request.full_url, "https://feedback.test")
        self.assertEqual(json.loads(request.data.decode("utf-8"))["message"], "hello")

    def test_without_yes_only_previews(self):
        out = io.StringIO()
        with mock.patch.object(feedback, "send") as send_mock, \
                contextlib.redirect_stdout(out):
            self.assertEqual(
                feedback.main(["--message", "hello", "--checklist", "Phone: X"]),
                2,
            )
        send_mock.assert_not_called()
        self.assertIn("Nothing sent", out.getvalue())
        self.assertIn("Phone: X", out.getvalue())

    def test_with_yes_sends_after_the_preview(self):
        out = io.StringIO()
        with mock.patch.object(feedback, "send") as send_mock, \
                contextlib.redirect_stdout(out):
            self.assertEqual(
                feedback.main(
                    [
                        "--yes",
                        "--kind",
                        "bug",
                        "--message",
                        "review copy",
                        "--checklist",
                        "Phone: X",
                    ]
                ),
                0,
            )
        send_mock.assert_called_once()
        payload = send_mock.call_args.args[0]
        self.assertEqual(payload["kind"], "bug")
        self.assertEqual(payload["message"], "review copy")
        self.assertIn("Sent", out.getvalue())


if __name__ == "__main__":
    unittest.main()
