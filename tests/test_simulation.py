"""Simulated-device tests: run the real CLI against a fake ADB transport.

These are not device tests and never promote a profile to `device`. They exercise the plan,
apply, verify and restore paths, the protected list, role checks, backup requirement and batch
limits against representative OEM package sets.
"""

from __future__ import annotations

import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import adb  # noqa: E402
import phone  # noqa: E402
import profiles  # noqa: E402

ROLES = {
    "DIALER": "com.google.android.dialer",
    "SMS": "com.google.android.apps.messaging",
    "HOME": "com.google.android.apps.nexuslauncher",
    "ASSISTANT": "",
    "EMERGENCY": "com.android.emergency",
}
CORE = {
    "com.google.android.gms",
    "com.android.vending",
    "com.google.android.webview",
    "com.android.systemui",
    "com.android.settings",
    "com.android.permissioncontroller",
    "com.android.packageinstaller",
}


class FakeDevice:
    def __init__(self, serial, props, packages, roles=None, telephony=True,
                 managed=False, settings=None, ime="com.google.android.inputmethod.latin"):
        self.serial = serial
        self.props = dict(props)
        self.enabled = set(packages)
        self.disabled = set()
        self.roles = dict(roles or {name: [pkg] if pkg else [] for name, pkg in ROLES.items()})
        self.telephony = telephony
        self.managed = managed
        self.settings = dict(settings or {
            "private_dns_mode": "off",
            "private_dns_specifier": "",
            "airplane_mode_on": "0",
            "wifi_on": "1",
            "mobile_data": "1",
        })
        self.ime = ime
        self.unknown = []
        self.dangerous = []

    @property
    def installed(self):
        return self.enabled | self.disabled

    def probe(self):
        return {
            "serial": self.serial,
            "brand": self.props.get("ro.product.brand", ""),
            "model": self.props.get("ro.product.model", ""),
            "device": self.props.get("ro.product.device", ""),
            "fingerprint": self.props.get("ro.build.fingerprint", ""),
            "build": self.props.get("ro.build.display.id", ""),
        }

    def result(self, code=0, out="", err=""):
        return subprocess.CompletedProcess(["adb"], code, out, err)

    def run(self, args, serial=None, timeout=120):
        if args == ["version"]:
            return self.result(out="Android Debug Bridge version 1.0.41")
        if args and args[0] == "devices":
            return self.result(out=f"List of devices attached\n{self.serial}\tdevice product:test model:Test\n")
        if not args or args[0] != "shell":
            self.unknown.append(" ".join(args))
            return self.result(out="")
        command = args[1] if len(args) > 1 else ""
        return self.shell(command)

    def shell(self, command):
        parts = command.split()
        if not parts:
            return self.result(out="")
        if any(token in command for token in (
            "pm uninstall", "pm hide", "pm clear", "pm block", "fastboot", "reboot"
        )):
            self.dangerous.append(command)
        if parts[0] == "getprop":
            key = parts[1] if len(parts) > 1 else ""
            if key == "sys.boot_completed":
                return self.result(out="1\n")
            return self.result(out=str(self.props.get(key, "")) + "\n")
        if command == "dumpsys battery":
            return self.result(out="Current Battery Service state:\n  level: 82\n  status: 2\n  health: 2\n")
        if command == "dumpsys device_policy":
            if self.managed:
                out = "Device Owner: ComponentInfo{com.example.mdm/.Admin}\n"
            else:
                out = "Device Owner: none\nProfile Owner: none\n"
            return self.result(out=out)
        if command == "pm list users":
            return self.result(out="Users:\n\tUserInfo{0:Owner:c13} running\n")
        if command == "dumpsys activity activities":
            return self.result(out="mFocusedApp=ActivityRecord{1 com.google.android.apps.nexuslauncher/.NexusLauncherActivity}\n")
        if command.startswith("pm list packages"):
            return self.packages(parts[3:])
        if command.startswith("pm disable-user --user 0 "):
            package = parts[-1]
            if package not in self.installed:
                return self.result(1, out="Error: package not found\n")
            self.enabled.discard(package)
            self.disabled.add(package)
            return self.result(out=f"Package {package} new state: disabled-user\n")
        if command.startswith("pm enable "):
            package = parts[-1]
            if package not in self.installed:
                return self.result(1, out="Error: package not found\n")
            self.disabled.discard(package)
            self.enabled.add(package)
            return self.result(out=f"Package {package} new state: enabled\n")
        if command.startswith("cmd role get-role-holders "):
            role = parts[-1].rsplit(".", 1)[-1]
            values = self.roles.get(role, [])
            return self.result(out="\n".join(values) + ("\n" if values else ""))
        if command == "settings get secure default_input_method":
            return self.result(out=(self.ime + "/.Gboard\n") if self.ime else "null\n")
        if command == "settings get secure dialer_default_application":
            return self.result(out="com.google.android.dialer\n")
        if command.startswith("settings get global "):
            key = parts[-1]
            return self.result(out=self.settings.get(key, "") + "\n")
        if command.startswith("settings put global "):
            key = parts[-2]
            value = " ".join(parts[-1:])
            self.settings[key] = value
            return self.result(out="")
        if command.startswith("cmd package resolve-activity"):
            package = self.roles.get("HOME", ["com.google.android.apps.nexuslauncher"])[0]
            return self.result(out=f"priority=0\n{package}/.Main\n")
        if command.startswith("cmd package query-activities"):
            values = self.roles.get("HOME", [])
            return self.result(out="\n".join(f"  {value}/.Main" for value in values))
        self.unknown.append(command)
        return self.result(out="")

    def packages(self, args):
        selected = self.enabled
        package_filter = ""
        for arg in args:
            if arg == "-d":
                selected = self.disabled
            elif arg == "-e":
                selected = self.enabled
            elif arg in ("-s", "-3"):
                selected = self.installed
            elif not arg.startswith("-"):
                package_filter = arg
        values = sorted(selected)
        if package_filter:
            values = [value for value in values if value == package_filter]
        return self.result(out="".join(f"package:{value}\n" for value in values))


def profile_packages(profile):
    packages = set(CORE)
    packages.update(value for value in ROLES.values() if value)
    for section in ("disable", "ask", "never"):
        packages.update(item["package"] for item in profile.get(section, []))
    if profile.get("form_factor") != "tablet":
        packages.add("com.android.phone")
    return packages


def device_for(profile, *, serial="SIM-SERIAL", build=None, fingerprint=None,
               managed=False, tablet=None):
    android = str(profile.get("android", ["16"])[0])
    sdk = int(android) + 20 if android.isdigit() else 36
    codename = profile.get("codename") or "synthetic"
    model = profile.get("model") if profile.get("model") != "*" else "Synthetic"
    is_tablet = profile.get("form_factor") == "tablet" if tablet is None else tablet
    props = {
        "ro.product.brand": profile.get("brand", "Test"),
        "ro.product.manufacturer": profile.get("brand", "Test"),
        "ro.product.model": model,
        "ro.product.device": codename,
        "ro.product.name": codename,
        "ro.build.version.release": android,
        "ro.build.version.sdk": str(sdk),
        "ro.build.version.security_patch": "2026-10-01",
        "ro.build.fingerprint": fingerprint or f"test/{codename}/{codename}:{android}/BUILD/1:user/release-keys",
        "ro.build.display.id": build or "BUILD",
        "ro.build.characteristics": "tablet" if is_tablet else "phone",
        "ro.boot.verifiedbootstate": "green",
        "ro.boot.flash.locked": "1",
        "ro.debuggable": "0",
    }
    roles = {name: [value] if value else [] for name, value in ROLES.items()}
    if is_tablet:
        roles["DIALER"] = []
        roles["SMS"] = []
    packages = profile_packages(profile)
    packages.add("com.google.android.inputmethod.latin")
    if is_tablet:
        packages.discard("com.android.phone")
    return FakeDevice(
        serial,
        props,
        packages,
        roles=roles,
        telephony=not is_tablet,
        managed=managed,
    )


@contextlib.contextmanager
def simulated(device, backup=True):
    temp = tempfile.TemporaryDirectory()
    old_backup = adb.BACKUP_DIR
    old_applied = adb.APPLIED_PATH
    old_changes = adb.CHANGES_PATH
    old_adb = adb.ADB
    try:
        adb.BACKUP_DIR = Path(temp.name) / "backup"
        adb.APPLIED_PATH = Path(temp.name) / "state" / "applied.json"
        adb.CHANGES_PATH = Path(temp.name) / "state" / "changes.json"
        adb.ADB = "fake-adb"
        if backup:
            folder = adb.BACKUP_DIR / "2026-10-30T00-00-00"
            folder.mkdir(parents=True)
            meta = {
                "serial": device.serial,
                "timestamp": "2026-10-30T00:00:00+00:00",
                "probe": device.probe(),
                "enabled": sorted(device.enabled),
                "disabled": sorted(device.disabled),
            }
            (folder / "meta.json").write_text(json.dumps(meta), encoding="utf-8")
        with mock.patch.object(adb, "adb_run", side_effect=device.run):
            yield device
        if device.unknown:
            raise AssertionError("simulated ADB received unknown command(s): " + "; ".join(device.unknown))
        if device.dangerous:
            raise AssertionError("simulated ADB received dangerous command(s): " + "; ".join(device.dangerous))
    finally:
        adb.BACKUP_DIR = old_backup
        adb.APPLIED_PATH = old_applied
        adb.CHANGES_PATH = old_changes
        adb.ADB = old_adb
        temp.cleanup()


def run_cli(device, *args):
    stdout, stderr = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        try:
            code = phone.main(["--serial", device.serial, *args])
        except SystemExit as exc:
            code = exc.code
    return code, stdout.getvalue(), stderr.getvalue()


class SimulationTests(unittest.TestCase):
    def test_pixel_plan_apply_restore(self):
        profile = profiles.load_profile("google-pixel-8")
        device = device_for(
            profile,
            build="BP2A.250705.008",
            fingerprint="google/shiba/shiba:16/BP2A.250705.008/1234567:user/release-keys",
        )
        with simulated(device):
            code, out, err = run_cli(device, "plan", "--profile", "google-pixel-8")
            self.assertEqual(code, 0, out)
            self.assertIn("DISABLE", out)
            code, out, err = run_cli(device, "apply", "--profile", "google-pixel-8", "--yes")
            self.assertEqual(code, 0, out)
            self.assertEqual(device.disabled, {"com.google.android.apps.wellbeing", "com.google.android.feedback"})
            self.assertIn("Done.", out)
            code, out, err = run_cli(device, "restore")
            self.assertEqual(code, 0, out)
            self.assertEqual(device.disabled, set())
            self.assertEqual(device.unknown, [])

    def test_oneplus_applies_in_two_batches(self):
        profile = profiles.load_profile("oneplus-a6013")
        device = device_for(
            profile,
            build="ONEPLUS A6013_41_211125",
            fingerprint="OnePlus/OnePlus6T/OnePlus6T:11/RKQ1.201217.002/2111252327:user/release-keys",
        )
        with simulated(device):
            code, out, err = run_cli(device, "apply", "--profile", "oneplus-a6013", "--yes", "--batch-size", "5")
            self.assertEqual(code, 0, out)
            self.assertEqual(len(device.disabled), 8)
            code, out, err = run_cli(device, "restore")
            self.assertEqual(code, 0, out)
            self.assertEqual(device.disabled, set())
            self.assertEqual(device.unknown, [])

    def test_documented_profile_never_autoapplies(self):
        profile = profiles.load_profile("samsung-sm-t505")
        device = device_for(profile, tablet=True)
        with simulated(device):
            code, out, err = run_cli(device, "apply", "--profile", "samsung-sm-t505", "--yes")
            self.assertEqual(code, 2)
            self.assertIn("documented", err)
            self.assertEqual(device.disabled, set())

    def test_apply_requires_backup(self):
        profile = profiles.load_profile("google-pixel-8")
        device = device_for(profile, build="BP2A.250705.008",
                            fingerprint="google/shiba/shiba:16/BP2A.250705.008/1:user/release-keys")
        with simulated(device, backup=False):
            code, out, err = run_cli(device, "apply", "--profile", "google-pixel-8", "--yes")
            self.assertEqual(code, 2)
            self.assertIn("no backup", err)
            self.assertEqual(device.disabled, set())

    def test_guardrails_block_protected_role_missing_and_large_batches(self):
        profile = profiles.load_profile("google-pixel-8")
        device = device_for(profile, build="BP2A.250705.008",
                            fingerprint="google/shiba/shiba:16/BP2A.250705.008/1:user/release-keys")
        device.roles["DIALER"] = ["com.example.dialer"]
        device.enabled.add("com.example.dialer")
        with simulated(device):
            code, out, err = run_cli(device, "disable", "com.android.systemui")
            self.assertEqual(code, 2)
            self.assertIn("protected", err)
            code, out, err = run_cli(device, "disable", "com.example.dialer")
            self.assertEqual(code, 2)
            self.assertIn("current DIALER", err)
            code, out, err = run_cli(device, "disable", "com.example.absent")
            self.assertEqual(code, 2)
            self.assertIn("not installed", err)
            code, out, err = run_cli(
                device, "disable", "com.google.android.apps.wellbeing",
                "com.google.android.feedback", "com.android.traceur",
                "com.android.bips", "com.android.musicfx", "com.android.printspooler",
            )
            self.assertEqual(code, 2)
            self.assertIn("at most 5", err)
            self.assertEqual(device.disabled, set())

    def test_managed_phone_is_refused(self):
        profile = profiles.load_profile("google-pixel-8")
        device = device_for(profile, build="BP2A.250705.008",
                            fingerprint="google/shiba/shiba:16/BP2A.250705.008/1:user/release-keys",
                            managed=True)
        with simulated(device):
            code, out, err = run_cli(device, "disable", "com.google.android.apps.wellbeing")
            self.assertEqual(code, 2)
            self.assertIn("device/profile owner", err)

    def test_tablet_has_no_telephony_failure(self):
        profile = profiles.load_profile("samsung-sm-t505")
        device = device_for(profile, tablet=True)
        with simulated(device):
            code, out, err = run_cli(device, "plan", "--profile", "samsung-sm-t505")
            self.assertEqual(code, 0, out)
            code, out, err = run_cli(device, "verify")
            self.assertEqual(code, 0, out)
            self.assertIn("Telephony", out)
            self.assertNotIn("FAIL", out)
            self.assertEqual(device.unknown, [])

    def test_every_profile_plan_runs(self):
        for path in sorted((ROOT / "profiles").glob("*/*.json")):
            profile = json.loads(path.read_text(encoding="utf-8"))
            with self.subTest(profile=profile["id"]):
                device = device_for(profile)
                with simulated(device, backup=False):
                    code, out, err = run_cli(device, "--json", "plan", "--profile", profile["id"])
                    self.assertEqual(code, 0, f"{out}\n{err}")
                    payload = json.loads(out)
                    self.assertEqual(payload["profile"]["id"], profile["id"])
                    self.assertEqual(device.unknown, [])


if __name__ == "__main__":
    unittest.main()
