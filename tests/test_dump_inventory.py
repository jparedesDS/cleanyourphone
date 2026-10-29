import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import dump_inventory as di  # noqa: E402


class InventoryTests(unittest.TestCase):
    def test_parse_readme(self):
        text = (
            "## pa3qxxx-user 16 BP2A\n"
            "- Manufacturer: samsung\n"
            "- Codename: pa3q\n"
            "- Release Version: 16\n"
            "- Fingerprint: samsung/pa3qxxx/pa3q:15/AP3A/x:user/release-keys\n"
        )
        meta = di.parse_readme(text)
        self.assertEqual(meta["manufacturer"], "samsung")
        self.assertEqual(meta["codename"], "pa3q")
        self.assertEqual(meta["release"], "16")

    def test_parse_props(self):
        props = di.parse_props("ro.product.vendor.model=SM-S938B\n# comment\nro.build.version.release=16\n")
        self.assertEqual(props["ro.product.vendor.model"], "SM-S938B")
        self.assertEqual(props["ro.build.version.release"], "16")

    def test_package_candidates(self):
        text = (
            "system/system/etc/permissions/privapp-permissions-com.example.priv.xml\n"
            "system/system/etc/permissions/signature-permissions-com.samsung.android.app.spage.xml\n"
            "system/system/etc/permissions/privapp-permissions-aer.xml\n"
            "system/system/priv-app/AREmoji/AREmoji.apk\n"
            "product/app/com.google.android.modulemetadata/com.google.android.modulemetadata.apk\n"
        )
        found = di.package_candidates(text)
        self.assertIn("com.example.priv", found)
        self.assertIn("com.samsung.android.app.spage", found)
        self.assertIn("com.google.android.modulemetadata", found)
        self.assertNotIn("aer", found)

    def test_cache_name(self):
        self.assertEqual(di.cache_name("README.md"), "readme-md.txt")
        self.assertEqual(di.cache_name("vendor/build.prop"), "vendor-build-prop.txt")

    def test_fingerprint_regex(self):
        regex = di.build_fingerprint_regex(
            "samsung/pa3qxxx/pa3q:15/AP3A.240905.015.A2/S938BXXS8BZC1:user/release-keys",
            "pa3q",
        )
        self.assertEqual(regex, "^samsung/pa3qxxx/pa3q")
        self.assertEqual(di.build_fingerprint_regex("", "a54x"), "^[^/]+/a54x")


if __name__ == "__main__":
    unittest.main()
