from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DocsTest(unittest.TestCase):
    def test_public_install_uses_pypi(self):
        for name in ("README.md", "README.es.md", "docs/CLI.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(document=name):
                self.assertIn("pipx install cleanyourphone", text)
                self.assertNotIn(
                    "pipx install git+https://github.com/jparedesDS/cleanyourphone.git",
                    text,
                )
