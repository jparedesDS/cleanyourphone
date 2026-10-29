import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import adb  # noqa: E402
import extra  # noqa: E402
import phone  # noqa: E402
import profiles  # noqa: E402
import protected  # noqa: E402


class ProtectedTests(unittest.TestCase):
    def test_core_packages_are_protected(self):
        for package in (
            "android",
            "com.android.systemui",
            "com.android.settings",
            "com.android.phone",
            "com.android.providers.telephony",
            "com.android.permissioncontroller",
            "com.android.packageinstaller",
            "com.google.android.gms",
            "com.android.vending",
            "com.google.android.webview",
            "com.android.cellbroadcastreceiver",
            "com.android.ims",
            "com.android.se",
            "com.android.nfc",
            "com.android.bluetooth",
            "com.android.networkstack",
            "com.android.wifi",
        ):
            with self.subTest(package=package):
                self.assertTrue(protected.is_protected(package))

    def test_prefixes_are_protected(self):
        for package in (
            "com.google.android.gms.location.history",
            "com.google.android.overlay.modules.foo",
            "com.android.providers.contacts",
            "com.samsung.android.knox.attestation",
        ):
            with self.subTest(package=package):
                self.assertTrue(protected.is_protected(package))

    def test_bloat_is_not_protected(self):
        for package in (
            "com.samsung.android.app.spage",
            "com.miui.msa.global",
            "com.xiaomi.mipicks",
            "com.google.android.apps.wellbeing",
            "com.google.android.feedback",
        ):
            with self.subTest(package=package):
                self.assertFalse(protected.is_protected(package))

    def test_reason_is_human_readable(self):
        self.assertIn("framework", protected.reason("android").lower())
        self.assertIn("Play Services", protected.reason("com.google.android.gms"))


class ParserTests(unittest.TestCase):
    def test_parse_packages_with_paths(self):
        text = (
            "package:/data/app/~~abc==/com.foo/base.apk=com.foo\n"
            "package:com.bar\n"
            "\n"
            "not a package line\n"
        )
        self.assertEqual(adb.parse_packages(text), ["com.foo", "com.bar"])

    def test_parse_packages_empty(self):
        self.assertEqual(adb.parse_packages(""), [])

    def test_parse_battery(self):
        battery = adb.parse_battery("level: 80\nstatus: 2\nhealth: 2\ntemperature: 310\n")
        self.assertEqual(battery["level"], 80)
        self.assertEqual(battery["status"], 2)
        self.assertEqual(battery["health"], 2)
        self.assertEqual(battery["temperature"], 310)

    def test_slug(self):
        self.assertEqual(adb.slug("Google Pixel 8"), "google-pixel-8")
        self.assertEqual(adb.slug("  "), "phone")

    def test_valid_hostname(self):
        self.assertTrue(extra.valid_hostname("dns.adguard-dns.com"))
        self.assertTrue(extra.valid_hostname("abc123"))
        self.assertFalse(extra.valid_hostname(""))
        self.assertFalse(extra.valid_hostname("dns..example.com"))
        self.assertFalse(extra.valid_hostname("http://example.com"))
        self.assertFalse(extra.valid_hostname("-bad.example.com"))

    def test_dns_status_parses_and_rejects_errors(self):
        with mock.patch.object(adb, "shell", side_effect=["hostname", "dns.example.com"]):
            self.assertEqual(
                adb.dns_status("SERIAL"), {"mode": "hostname", "specifier": "dns.example.com"}
            )
        with mock.patch.object(adb, "shell", side_effect=["Error: no settings service", ""]):
            with self.assertRaises(adb.AdbError):
                adb.dns_status("SERIAL")

    def test_package_set_error_raises(self):
        with mock.patch.object(adb, "shell", return_value="Error: no package service"):
            with self.assertRaises(adb.AdbError):
                adb.package_set("SERIAL", "-d")

    def test_redact_getprop(self):
        text = (
            "[ro.product.model]: [Pixel 8]\n"
            "[ro.serialno]: [ABC123]\n"
            "[ro.boot.imei]: [123456789012345]\n"
            "[ro.boot.wifimacaddr]: [aa:bb:cc:dd:ee:ff]\n"
            "[ro.build.version.release]: [16]\n"
        )
        redacted = adb.redact_getprop(text)
        self.assertIn("[ro.product.model]: [Pixel 8]", redacted)
        self.assertIn("[ro.build.version.release]: [16]", redacted)
        self.assertNotIn("ABC123", redacted)
        self.assertNotIn("123456789012345", redacted)
        self.assertNotIn("aa:bb:cc:dd:ee:ff", redacted)

    def test_valid_package(self):
        self.assertTrue(adb.valid_package("com.google.android.gms"))
        self.assertTrue(adb.valid_package("com.example.app_2"))
        self.assertTrue(adb.valid_package("android"))
        self.assertFalse(adb.valid_package("com.example..app"))
        self.assertFalse(adb.valid_package("com.example.app;reboot"))
        self.assertFalse(adb.valid_package("com.example.app --user all"))
        self.assertFalse(adb.valid_package("com.example/app"))
        self.assertFalse(adb.valid_package(""))


class ProfileTests(unittest.TestCase):
    def test_pixel_matches(self):
        profile = {
            "model": "Pixel 8",
            "codename": "shiba",
            "fingerprint_regex": "^google/shiba/",
        }
        probe = {
            "model": "Pixel 8",
            "device": "shiba",
            "fingerprint": "google/shiba/shiba:16/BP2A.250705.008/123:user/release-keys",
        }
        self.assertTrue(profiles.profile_matches(profile, probe))

    def test_pixel_does_not_match_pro(self):
        profile = {
            "model": "Pixel 8",
            "codename": "shiba",
            "fingerprint_regex": "^google/shiba/",
        }
        probe = {
            "model": "Pixel 8 Pro",
            "device": "husky",
            "fingerprint": "google/husky/husky:16/BP2A.250705.008/123:user/release-keys",
        }
        self.assertFalse(profiles.profile_matches(profile, probe))

    def test_samsung_matches(self):
        profile = {
            "model": "SM-S918B",
            "codename": "dm3q",
            "fingerprint_regex": "^samsung/dm3q",
        }
        probe = {
            "model": "SM-S918B",
            "device": "dm3q",
            "fingerprint": "samsung/dm3q/dm3q:15/UP1A.231005.007/123:user/release-keys",
        }
        self.assertTrue(profiles.profile_matches(profile, probe))

    def test_generic_matches_anything(self):
        profile = {"model": "*", "fingerprint_regex": ""}
        probe = {"model": "Whatever", "device": "whatever", "fingerprint": "brand/whatever"}
        self.assertTrue(profiles.profile_matches(profile, probe))

    def test_model_is_exact_not_a_prefix(self):
        profile = {"model": "Pixel 8", "fingerprint_regex": ""}
        probe = {"model": "Pixel 8 Pro", "device": "", "fingerprint": ""}
        self.assertFalse(profiles.profile_matches(profile, probe))

    def test_android_version_must_be_listed(self):
        profile = {"model": "Pixel 8", "android": ["14", "15"], "fingerprint_regex": ""}
        probe = {"model": "Pixel 8", "android": "16", "device": "", "fingerprint": ""}
        self.assertFalse(profiles.profile_matches(profile, probe))

    def test_android_minor_version_matches_major(self):
        profile = {"model": "*", "android": ["8"], "fingerprint_regex": ""}
        probe = {"model": "Whatever", "android": "8.1.0", "device": "", "fingerprint": ""}
        self.assertTrue(profiles.profile_matches(profile, probe))

    def test_empty_fingerprint_does_not_match(self):
        profile = {"model": "Pixel 8", "android": ["16"], "fingerprint_regex": "^google/shiba/"}
        probe = {"model": "Pixel 8", "device": "shiba", "android": "16", "fingerprint": ""}
        self.assertFalse(profiles.profile_matches(profile, probe))

    def test_build_matches_only_a_tested_build(self):
        profile = {
            "tested": [{"android": "16", "build": "BP2A.250705.008", "date": "x", "by": "x"}],
        }
        self.assertTrue(
            profiles.build_matches(
                profile,
                {
                    "build": "BP2A.250705.008",
                    "fingerprint": "google/shiba/shiba:16/BP2A.250705.008/123:user/release-keys",
                },
            )
        )
        self.assertFalse(
            profiles.build_matches(
                profile,
                {
                    "build": "BP2A.250805.009",
                    "fingerprint": "google/shiba/shiba:16/BP2A.250805.009/123:user/release-keys",
                },
            )
        )

    def test_build_matches_rejects_documented(self):
        profile = {
            "verification": "documented",
            "auto_apply": False,
            "tested": [{"android": "16", "build": "BP2A.250705.008", "date": "x", "by": "x"}],
        }
        self.assertFalse(
            profiles.build_matches(
                profile,
                {"build": "BP2A.250705.008", "fingerprint": "google/shiba:16/BP2A.250705.008/x"},
            )
        )

    def test_verification_inference(self):
        self.assertEqual(profiles.verification_level({"generic": True}), "reference")
        self.assertEqual(profiles.verification_level({"tested": [{"build": "x"}]}), "device")
        self.assertEqual(profiles.verification_level({}), "documented")

    def test_build_matches_needs_fingerprint(self):
        profile = {"tested": [{"android": "16", "build": "BP2A.250705.008", "date": "x", "by": "x"}]}
        self.assertFalse(profiles.build_matches(profile, {"build": "BP2A.250705.008", "fingerprint": ""}))

    def test_build_matches_respects_auto_apply_false(self):
        profile = {
            "auto_apply": False,
            "tested": [{"android": "15", "build": "OS2.0.1.0", "date": "x", "by": "x"}],
        }
        self.assertFalse(
            profiles.build_matches(profile, {"build": "OS2.0.1.0", "fingerprint": "xiaomi/foo:15/OS2.0.1.0/x"})
        )

    def test_never_for_phone_uses_matching_profile(self):
        profile = {
            "model": "*",
            "fingerprint_regex": "^(xiaomi|redmi|poco)/",
            "never": [{"package": "com.miui.securitycenter", "why": "permissions"}],
        }
        probe = {
            "model": "Whatever",
            "device": "whatever",
            "android": "15",
            "fingerprint": "xiaomi/whatever:15/OS2/x",
        }
        with mock.patch.object(profiles, "load_profiles", return_value=[profile]):
            self.assertIn("com.miui.securitycenter", profiles.never_for_phone(probe))

    def test_classify_never_overrides_disable(self):
        profile = {
            "disable": [{"package": "com.example.keep", "why": "test", "breaks": "nothing"}],
            "ask": [],
            "never": [{"package": "com.example.keep", "why": "never"}],
        }
        rows = profiles.classify(
            profile,
            enabled={"com.example.keep"},
            disabled=set(),
            holders={},
            ime="com.example.ime",
        )
        self.assertEqual(rows[0]["action"], "BLOCKED")
        self.assertIn("never", rows[0]["reason"])

    def test_classify_actions(self):
        profile = {
            "disable": [{"package": "com.example.safe", "why": "test", "breaks": "nothing"}],
            "ask": [{"package": "com.example.ask", "why": "test", "breaks": "something"}],
            "never": [{"package": "com.android.systemui", "why": "core"}],
        }
        rows = profiles.classify(
            profile,
            enabled={"com.example.safe", "com.example.ask"},
            disabled=set(),
            holders={"DIALER": ["com.example.dialer"]},
            ime="com.example.ime",
        )
        by_package = {row["package"]: row for row in rows}
        self.assertEqual(by_package["com.example.safe"]["action"], "DISABLE")
        self.assertEqual(by_package["com.example.ask"]["action"], "ASK")
        self.assertEqual(by_package["com.android.systemui"]["action"], "KEEP")

    def test_classify_blocks_protected_role_and_ime(self):
        profile = {
            "disable": [
                {"package": "com.android.systemui", "why": "test", "breaks": "boot"},
                {"package": "com.example.dialer", "why": "test", "breaks": "calls"},
                {"package": "com.example.ime", "why": "test", "breaks": "keyboard"},
            ],
            "ask": [],
            "never": [],
        }
        rows = profiles.classify(
            profile,
            enabled={"com.android.systemui", "com.example.dialer", "com.example.ime"},
            disabled=set(),
            holders={"DIALER": ["com.example.dialer"]},
            ime="com.example.ime",
        )
        actions = {row["package"]: row["action"] for row in rows}
        self.assertEqual(actions["com.android.systemui"], "BLOCKED")
        self.assertEqual(actions["com.example.dialer"], "BLOCKED")
        self.assertEqual(actions["com.example.ime"], "BLOCKED")

    def test_classify_skips_disabled_and_missing(self):
        profile = {
            "disable": [
                {"package": "com.example.disabled", "why": "test", "breaks": "nothing"},
                {"package": "com.example.missing", "why": "test", "breaks": "nothing"},
            ],
            "ask": [],
            "never": [],
        }
        rows = profiles.classify(
            profile,
            enabled={"com.example.disabled"},
            disabled={"com.example.disabled"},
            holders={},
            ime="",
        )
        actions = {row["package"]: row["action"] for row in rows}
        self.assertEqual(actions["com.example.disabled"], "SKIP")
        self.assertEqual(actions["com.example.missing"], "MISSING")


class ValidationTests(unittest.TestCase):
    def base_profile(self):
        return {
            "id": "test-device",
            "brand": "Test",
            "model": "TEST-1",
            "android": ["15"],
            "fingerprint_regex": "^test/test/",
            "verification": "device",
            "tested": [{"android": "15", "build": "BUILD", "date": "2026-10-29", "by": "test"}],
            "disable": [{"package": "com.example.bloat", "why": "test", "breaks": "nothing"}],
            "ask": [{"package": "com.example.ask", "why": "test", "breaks": "something"}],
            "never": [{"package": "com.android.systemui", "why": "core"}],
            "notes": "test profile",
        }

    def documented_profile(self):
        profile = self.base_profile()
        profile["verification"] = "documented"
        profile["auto_apply"] = False
        profile["tested"] = []
        profile["disable"] = []
        profile["sources"] = [
            {
                "title": "Firmware dump",
                "url": "https://gitlab.com/Android-Dumps/samsung/pa3q",
                "retrieved": "2026-10-29",
                "note": "test",
            }
        ]
        return profile

    def test_valid_profile(self):
        self.assertEqual(profiles.validate_profile(self.base_profile()), [])

    def test_documented_profile_is_valid(self):
        self.assertEqual(profiles.validate_profile(self.documented_profile()), [])

    def test_documented_requires_sources(self):
        profile = self.documented_profile()
        profile["sources"] = []
        errors = profiles.validate_profile(profile)
        self.assertTrue(any("primary source" in error for error in errors))

    def test_documented_forbids_disable(self):
        profile = self.documented_profile()
        profile["disable"] = [{"package": "com.example.bloat", "why": "test", "breaks": "nothing"}]
        errors = profiles.validate_profile(profile)
        self.assertTrue(any("must not have a 'disable' list" in error for error in errors))

    def test_documented_forbids_tested(self):
        profile = self.documented_profile()
        profile["tested"] = [{"android": "16", "build": "B", "date": "2026-10-29", "by": "x"}]
        errors = profiles.validate_profile(profile)
        self.assertTrue(any("must not claim tested entries" in error for error in errors))

    def test_documented_forbids_auto_apply(self):
        profile = self.documented_profile()
        profile["auto_apply"] = True
        errors = profiles.validate_profile(profile)
        self.assertTrue(any("must set auto_apply: false" in error for error in errors))

    def test_documented_forbids_generic(self):
        profile = self.documented_profile()
        profile["generic"] = True
        errors = profiles.validate_profile(profile)
        self.assertTrue(any("generic profile must use verification 'reference'" in error for error in errors))

    def test_reference_requires_generic(self):
        profile = self.base_profile()
        profile["verification"] = "reference"
        errors = profiles.validate_profile(profile)
        self.assertTrue(any("requires generic: true" in error for error in errors))

    def test_device_requires_tested(self):
        profile = self.base_profile()
        profile["verification"] = "device"
        profile["tested"] = []
        errors = profiles.validate_profile(profile)
        self.assertTrue(any("needs at least one real test" in error for error in errors))

    def test_source_url_must_be_http(self):
        profile = self.documented_profile()
        profile["sources"][0]["url"] = "file:///tmp/dump"
        errors = profiles.validate_profile(profile)
        self.assertTrue(any("url must start with http" in error for error in errors))

    def test_bad_verification_value(self):
        profile = self.base_profile()
        profile["verification"] = "maybe"
        errors = profiles.validate_profile(profile)
        self.assertTrue(any("verification must be one of" in error for error in errors))

    def test_missing_field(self):
        profile = self.base_profile()
        del profile["notes"]
        errors = profiles.validate_profile(profile)
        self.assertTrue(any("notes" in error for error in errors))

    def test_protected_package_in_disable(self):
        profile = self.base_profile()
        profile["disable"] = [{"package": "com.android.systemui", "why": "test", "breaks": "boot"}]
        errors = profiles.validate_profile(profile)
        self.assertTrue(any("protected" in error for error in errors))

    def test_duplicate_package(self):
        profile = self.base_profile()
        profile["ask"] = [{"package": "com.example.bloat", "why": "test", "breaks": "nothing"}]
        errors = profiles.validate_profile(profile)
        self.assertTrue(any("duplicate" in error for error in errors))

    def test_generic_cannot_disable(self):
        profile = self.base_profile()
        profile["generic"] = True
        profile["verification"] = "reference"
        profile["tested"] = []
        profile["auto_apply"] = False
        errors = profiles.validate_profile(profile)
        self.assertTrue(any("generic profile" in error for error in errors))

    def test_generic_needs_star_model(self):
        profile = self.base_profile()
        profile["generic"] = True
        profile["verification"] = "reference"
        profile["tested"] = []
        profile["auto_apply"] = False
        profile["disable"] = []
        errors = profiles.validate_profile(profile)
        self.assertTrue(any("model '*'" in error for error in errors))

    def test_non_generic_needs_fingerprint(self):
        profile = self.base_profile()
        profile["fingerprint_regex"] = ""
        errors = profiles.validate_profile(profile)
        self.assertTrue(any("fingerprint_regex" in error for error in errors))

    def test_family_profile_can_use_star_with_fingerprint(self):
        profile = self.base_profile()
        profile["model"] = "*"
        profile["fingerprint_regex"] = "^xiaomi/"
        errors = profiles.validate_profile(profile)
        self.assertFalse(any("model '*'" in error for error in errors))

    def test_bad_id(self):
        profile = self.base_profile()
        profile["id"] = "Test Device"
        errors = profiles.validate_profile(profile)
        self.assertTrue(any("kebab-case" in error for error in errors))

    def test_bad_regex(self):
        profile = self.base_profile()
        profile["fingerprint_regex"] = "("
        errors = profiles.validate_profile(profile)
        self.assertTrue(any("fingerprint_regex" in error for error in errors))

    def test_regex_that_matches_empty_is_rejected(self):
        profile = self.base_profile()
        profile["fingerprint_regex"] = ".*"
        errors = profiles.validate_profile(profile)
        self.assertTrue(any("empty string" in error for error in errors))

    def test_invalid_package_is_rejected(self):
        profile = self.base_profile()
        profile["disable"] = [
            {"package": "com.example.bloat;reboot", "why": "test", "breaks": "nothing"}
        ]
        errors = profiles.validate_profile(profile)
        self.assertTrue(any("invalid package" in error for error in errors))

    def test_auto_apply_must_be_boolean(self):
        profile = self.base_profile()
        profile["auto_apply"] = "yes"
        errors = profiles.validate_profile(profile)
        self.assertTrue(any("auto_apply" in error for error in errors))

    def test_strict_loading_reports_bad_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "broken.json").write_text("{not json", encoding="utf-8")
            with mock.patch.object(profiles, "PROFILES_DIR", Path(tmp)):
                with self.assertRaises(ValueError):
                    profiles.load_profiles(strict=True)


class StateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old_applied = adb.APPLIED_PATH
        self.old_changes = adb.CHANGES_PATH
        adb.APPLIED_PATH = Path(self.tmp.name) / "applied.json"
        adb.CHANGES_PATH = Path(self.tmp.name) / "changes.json"

    def tearDown(self):
        adb.APPLIED_PATH = self.old_applied
        adb.CHANGES_PATH = self.old_changes
        self.tmp.cleanup()

    def test_applied_is_per_serial(self):
        first = adb.load_applied("SERIAL-A")
        first["packages"]["com.example.bloat"] = {"why": "test"}
        adb.save_applied("SERIAL-A", first)

        self.assertEqual(adb.load_applied("SERIAL-B")["packages"], {})
        self.assertIn("com.example.bloat", adb.load_applied("SERIAL-A")["packages"])

    def test_changes_are_per_serial(self):
        adb.save_changes("SERIAL-A", {"dns": {"before": {"mode": "off", "specifier": ""}}})
        self.assertEqual(adb.load_changes("SERIAL-B"), {})
        self.assertEqual(adb.load_changes("SERIAL-A")["dns"]["before"]["mode"], "off")

    def test_corrupt_applied_is_fatal(self):
        adb.APPLIED_PATH.write_text("{not json", encoding="utf-8")
        with self.assertRaises(adb.StateError):
            adb.load_applied("SERIAL-A")
        with self.assertRaises(adb.StateError):
            adb.save_applied("SERIAL-A", {"packages": {}})

    def test_corrupt_changes_is_fatal(self):
        adb.CHANGES_PATH.write_text("[1, 2]", encoding="utf-8")
        with self.assertRaises(adb.StateError):
            adb.load_changes("SERIAL-A")

    def test_old_state_format_is_fatal(self):
        adb.APPLIED_PATH.write_text('{"packages": {}}', encoding="utf-8")
        with self.assertRaises(adb.StateError):
            adb.load_applied("SERIAL-A")


class DeviceTests(unittest.TestCase):
    def test_managed_component_is_detected(self):
        text = (
            "Device Owner Type: -1\n"
            "Device Owner: admin=ComponentInfo{com.example.mdm/com.example.mdm.Admin}\n"
        )
        with mock.patch.object(adb, "shell", return_value=text):
            self.assertTrue(adb.is_managed("SERIAL"))

    def test_managed_heading_is_not_an_owner(self):
        text = "Device Owner Type: -1\nProfile Owner Type: -1\n"
        with mock.patch.object(adb, "shell", return_value=text):
            self.assertFalse(adb.is_managed("SERIAL"))

    def test_managed_section_detects_owner_on_next_line(self):
        text = (
            "  Device Owners:\n"
            "    admin=ComponentInfo{com.example.mdm/com.example.mdm.Admin}\n"
            "  Profile Owners:\n"
            "    admin=null\n"
        )
        with mock.patch.object(adb, "shell", return_value=text):
            self.assertTrue(adb.is_managed("SERIAL"))

    def test_managed_singular_heading_detects_next_line(self):
        text = (
            "  Device Owner:\n"
            "    admin=ComponentInfo{com.example.mdm/com.example.mdm.Admin}\n"
            "  Device Admins (User 0, provisioningState: 0):\n"
            "    admin=ComponentInfo{com.google.android.gms/.FindMyDeviceAdmin}\n"
        )
        with mock.patch.object(adb, "shell", return_value=text):
            self.assertTrue(adb.is_managed("SERIAL"))

    def test_managed_internal_field_is_detected(self):
        text = "mDeviceOwner=ComponentInfo{com.example.mdm/com.example.mdm.Admin}\n"
        with mock.patch.object(adb, "shell", return_value=text):
            self.assertTrue(adb.is_managed("SERIAL"))

    def test_plain_device_admin_is_not_an_owner(self):
        text = (
            "  Device Admins (User 0, provisioningState: 0):\n"
            "    admin=ComponentInfo{com.google.android.gms/com.google.android.gms.mdm.FindMyDeviceAdmin}\n"
        )
        with mock.patch.object(adb, "shell", return_value=text):
            self.assertFalse(adb.is_managed("SERIAL"))

    def test_managed_read_failure_is_none(self):
        with mock.patch.object(adb, "shell", side_effect=adb.AdbError("boom")):
            self.assertIsNone(adb.is_managed("SERIAL"))

    def test_managed_empty_output_is_none(self):
        with mock.patch.object(adb, "shell", return_value=""):
            self.assertIsNone(adb.is_managed("SERIAL"))

    def test_managed_error_output_is_none(self):
        with mock.patch.object(adb, "shell", return_value="Permission Denial: cannot dump device_policy"):
            self.assertIsNone(adb.is_managed("SERIAL"))

    def test_user_count(self):
        text = "Users:\n\tUserInfo{0:Owner:13} running\n\tUserInfo{10:Work profile:30} running\n"
        with mock.patch.object(adb, "_shell_or_empty", return_value=text):
            self.assertEqual(adb.user_count("SERIAL"), 2)
        with mock.patch.object(adb, "_shell_or_empty", return_value=""):
            self.assertIsNone(adb.user_count("SERIAL"))
        with mock.patch.object(adb, "_shell_or_empty", return_value="Error: no users"):
            self.assertIsNone(adb.user_count("SERIAL"))
        with mock.patch.object(adb, "_shell_or_empty", return_value="Users:\n"):
            self.assertIsNone(adb.user_count("SERIAL"))

    def test_role_read_error_raises(self):
        result = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="Error: boom")
        with mock.patch.object(adb, "adb_run", return_value=result):
            with self.assertRaises(adb.AdbError):
                adb.role_holders("SERIAL")

    def test_role_permission_denial_raises(self):
        result = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="Permission Denial: cannot read role holders", stderr=""
        )
        with mock.patch.object(adb, "adb_run", return_value=result):
            with self.assertRaises(adb.AdbError):
                adb.role_holders("SERIAL")

    def test_no_role_holder_message_is_not_a_package(self):
        result = subprocess.CompletedProcess(args=[], returncode=0, stdout="No role holders", stderr="")
        with mock.patch.object(adb, "adb_run", return_value=result):
            holders, supported = adb.role_holders("SERIAL")
        self.assertTrue(supported)
        self.assertEqual(holders["DIALER"], [])

    def test_resolve_activity_package(self):
        out = (
            "priority=0 preferredOrder=0 match=0x108000 specificIndex=-1 isDefault=true\n"
            "com.oneplus.dialer/com.android.dialer.oneplus.activity.OPDialtactsActivity\n"
        )
        with mock.patch.object(adb, "_shell_or_empty", return_value=out):
            self.assertEqual(adb.resolve_activity_package("SERIAL", "android.intent.action.DIAL"), "com.oneplus.dialer")

    def test_role_fallback_uses_resolve_activity(self):
        unknown = subprocess.CompletedProcess(args=[], returncode=0, stdout="Unknown command: get-role-holders", stderr="")
        with mock.patch.object(adb, "adb_run", return_value=unknown):
            with mock.patch.object(adb, "_shell_or_empty", return_value="null"):
                with mock.patch.object(
                    adb,
                    "resolve_activity_package",
                    side_effect=["com.oneplus.dialer", "com.oneplus.mms"],
                ):
                    with mock.patch.object(adb, "default_home_package", return_value="net.oneplus.launcher"):
                        holders, supported = adb.role_holders("SERIAL")
        self.assertFalse(supported)
        self.assertEqual(holders["DIALER"], ["com.oneplus.dialer"])
        self.assertEqual(holders["SMS"], ["com.oneplus.mms"])
        self.assertEqual(holders["HOME"], ["net.oneplus.launcher"])

    def test_missing_cmd_role_falls_back(self):
        result = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="/system/bin/sh: cmd: not found", stderr=""
        )
        with mock.patch.object(adb, "adb_run", return_value=result):
            with mock.patch.object(adb, "_shell_or_empty", return_value=""):
                holders, supported = adb.role_holders("SERIAL")
        self.assertFalse(supported)
        self.assertEqual(holders, {})


class ChangeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old_applied = adb.APPLIED_PATH
        adb.APPLIED_PATH = Path(self.tmp.name) / "applied.json"

    def tearDown(self):
        adb.APPLIED_PATH = self.old_applied
        self.tmp.cleanup()

    def test_disable_is_recorded_before_post_check(self):
        meta = {"enabled": ["com.example.bloat"], "disabled": [], "timestamp": "t"}
        applied = {"packages": {}}
        result = subprocess.CompletedProcess(args=[], returncode=0, stdout="new state: disabled-user", stderr="")
        with mock.patch.object(phone.adb, "package_set", side_effect=[set(), set()]):
            with mock.patch.object(phone.adb, "adb_run", return_value=result):
                with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        phone.disable_one(
                            "SERIAL",
                            "com.example.bloat",
                            meta,
                            applied,
                            holders={},
                            ime="com.example.ime",
                        )
        self.assertIn("com.example.bloat", adb.load_applied("SERIAL")["packages"])

    def test_rollback_enables_a_disabled_package(self):
        applied = {"packages": {"com.example.bloat": {"why": "test"}}}
        with mock.patch.object(phone.adb, "package_set", return_value={"com.example.bloat"}):
            with mock.patch.object(phone, "enable_one") as enable:
                phone.rollback_batch("SERIAL", ["com.example.bloat"], applied)
        enable.assert_called_once_with("SERIAL", "com.example.bloat", applied)

    def test_guard_writable_unknown_managed_dies(self):
        probe = {
            "is_tv": False,
            "managed": None,
            "users": 1,
            "sdk": 33,
            "android": "13",
        }
        with mock.patch.object(phone.adb, "probe_device", return_value=probe):
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    phone.guard_writable("SERIAL")

    def test_plan_marks_documented_rows_as_ask(self):
        profile = {
            "id": "test-documented",
            "brand": "Test",
            "model": "TEST-1",
            "android": ["16"],
            "fingerprint_regex": "^test/",
            "auto_apply": False,
            "verification": "documented",
            "sources": [
                {"title": "dump", "url": "https://example.com/dump", "retrieved": "2026-10-29"}
            ],
            "tested": [],
            "disable": [],
            "ask": [{"package": "com.example.ask", "why": "test", "breaks": "something"}],
            "never": [],
            "notes": "test",
        }
        probe = {
            "brand": "Test",
            "model": "TEST-1",
            "device": "test",
            "android": "16",
            "fingerprint": "test/test/test:16/BUILD/x",
        }
        args = SimpleNamespace(profile="test-documented", json=True, dry_run=False, serial=None)
        output = io.StringIO()
        with mock.patch.object(phone.profiles, "load_profile", return_value=profile):
            with mock.patch.object(phone.adb, "pick_serial", return_value="SERIAL"):
                with mock.patch.object(phone.adb, "probe_device", return_value=probe):
                    with mock.patch.object(
                        phone.adb, "package_set", side_effect=[{"com.example.ask"}, set()]
                    ):
                        with mock.patch.object(
                            phone, "guard_roles", return_value=({"HOME": ["com.example.home"]}, "com.example.ime")
                        ):
                            with contextlib.redirect_stdout(output):
                                code = phone.cmd_plan(args)
        data = json.loads(output.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(data["verification"], "documented")
        self.assertFalse(data["auto_apply"])
        self.assertEqual(data["rows"][0]["action"], "ASK")

    def test_apply_refuses_documented_profile(self):
        profile = {
            "id": "test-documented",
            "brand": "Test",
            "model": "TEST-1",
            "android": ["16"],
            "fingerprint_regex": "^test/",
            "auto_apply": False,
            "verification": "documented",
            "sources": [
                {"title": "dump", "url": "https://example.com/dump", "retrieved": "2026-10-29"}
            ],
            "tested": [],
            "disable": [],
            "ask": [{"package": "com.example.ask", "why": "test", "breaks": "something"}],
            "never": [],
            "notes": "test",
        }
        args = SimpleNamespace(profile="test-documented", batch_size=5, yes=False, serial=None)
        with mock.patch.object(phone.profiles, "load_profile", return_value=profile):
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    phone.cmd_apply(args)

    def test_restore_keeps_record_when_final_check_fails(self):
        adb.save_applied("SERIAL", {"packages": {"com.example.bloat": {"why": "test"}}})
        args = SimpleNamespace(serial=None, dry_run=False)
        result = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        with mock.patch.object(phone.adb, "pick_serial", return_value="SERIAL"):
            with mock.patch.object(phone.adb, "adb_run", return_value=result):
                with mock.patch.object(
                    phone.adb,
                    "package_set",
                    side_effect=[{"com.example.bloat"}, {"com.example.bloat"}, {"com.example.bloat"}],
                ):
                    with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
                        with self.assertRaises(SystemExit):
                            phone.cmd_restore(args)
        self.assertIn("com.example.bloat", adb.load_applied("SERIAL")["packages"])

    def test_guard_writable_second_user_dies(self):
        probe = {
            "is_tv": False,
            "managed": False,
            "users": 2,
            "sdk": 33,
            "android": "13",
        }
        with mock.patch.object(phone.adb, "probe_device", return_value=probe):
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    phone.guard_writable("SERIAL")


if __name__ == "__main__":
    unittest.main()
