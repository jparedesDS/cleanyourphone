import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import adb  # noqa: E402
import bench  # noqa: E402


def fake_shell(command, serial=None, timeout=120):
    if command == "cat /proc/meminfo":
        return "MemTotal: 4000000 kB\nMemAvailable: 2097152 kB\nSwapTotal: 1000000 kB\nSwapFree: 800000 kB\n"
    if command == "ps -A -o NAME":
        return "NAME\ninit\nsystem_server\ncom.foo\n"
    values = {
        "settings get global window_animation_scale": "0.5",
        "settings get global transition_animation_scale": "0.5",
        "settings get global animator_duration_scale": "1.0",
        "settings get system peak_refresh_rate": "120",
        "settings get global low_power": "0",
    }
    return values.get(command, "")


class BenchTests(unittest.TestCase):
    def setUp(self):
        self.probe = {
            "brand": "Google",
            "model": "Pixel 8",
            "android": "16",
            "build": "AP1A.240905.004",
        }
        self.mocks = [
            mock.patch.object(adb, "probe_device", return_value=self.probe),
            mock.patch.object(adb, "shell", side_effect=fake_shell),
            mock.patch.object(
                adb,
                "package_set",
                side_effect=lambda serial, flag="": {
                    "": {"a", "b", "c"},
                    "-e": {"a", "b"},
                    "-d": {"c"},
                    "-s": {"a"},
                    "-3": {"b"},
                }[flag],
            ),
            mock.patch.object(
                adb,
                "dns_status",
                return_value={"mode": "hostname", "specifier": "dns.adguard-dns.com"},
            ),
        ]
        for patcher in self.mocks:
            patcher.start()
        self.addCleanup(lambda: [patcher.stop() for patcher in self.mocks])

    def test_measure_parses_metrics_and_omits_identity(self):
        data = bench.measure("SERIAL")
        self.assertEqual(data["ram_available_mb"], 2048)
        self.assertEqual(data["swap_used_mb"], 195)
        self.assertEqual(data["processes"], 3)
        self.assertEqual(data["packages_installed"], 3)
        self.assertEqual(data["packages_enabled"], 2)
        self.assertEqual(data["packages_disabled"], 1)
        self.assertEqual(data["animation_window"], 0.5)
        self.assertEqual(data["peak_refresh_rate"], 120.0)
        self.assertEqual(data["private_dns_mode"], "hostname")
        self.assertNotIn("serial", data)
        self.assertNotIn("fingerprint", data)
        self.assertNotIn("SERIAL", json.dumps(data))

    def test_compare_reports_deltas(self):
        rows = bench.compare(
            {"ram_available_mb": 1000, "packages_enabled": 200},
            {"ram_available_mb": 1200, "packages_enabled": 180},
        )
        by_metric = {row["metric"]: row for row in rows}
        self.assertEqual(by_metric["ram_available_mb"]["delta"], 200)
        self.assertEqual(by_metric["ram_available_mb"]["pct"], 20.0)
        self.assertEqual(by_metric["packages_enabled"]["delta"], -20)

    def test_save_and_load_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(bench, "BENCH_DIR", Path(tmp)):
                data = bench.measure("SERIAL")
                path = bench.save(data, "before")
                self.assertTrue(path.is_file())
                self.assertEqual(bench.load(path)["ram_available_mb"], 2048)
                self.assertIn("before", path.name)
                self.assertNotIn("SERIAL", path.name)

    def test_markdown_has_no_causal_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            before = {"model": "Pixel 8", "android": "16", "build": "A", "ram_available_mb": 1000}
            after = {"model": "Pixel 8", "android": "16", "build": "A", "ram_available_mb": 1200}
            path = bench.write_markdown(before, after, bench.compare(before, after), Path(tmp) / "report.md")
            text = path.read_text(encoding="utf-8")
            self.assertIn("approximate", text.lower())
            self.assertIn("not causal", text.lower())
            self.assertIn("RAM available", text)

    def test_markdown_warns_on_different_devices_and_battery_saver(self):
        with tempfile.TemporaryDirectory() as tmp:
            before = {"model": "Pixel 8", "android": "16", "build": "A", "battery_saver": False, "ram_available_mb": 1000}
            after = {"model": "Galaxy S23", "android": "16", "build": "B", "battery_saver": True, "ram_available_mb": 1200}
            path = bench.write_markdown(before, after, bench.compare(before, after), Path(tmp) / "report.md")
            text = path.read_text(encoding="utf-8")
            self.assertIn("different models", text)
            self.assertIn("Battery Saver changed", text)

    def test_load_rejects_empty_and_partial_snapshots(self):
        with tempfile.TemporaryDirectory() as tmp:
            empty = Path(tmp) / "empty.json"
            empty.write_text("{}", encoding="utf-8")
            with self.assertRaises(ValueError):
                bench.load(empty)
            wrong = Path(tmp) / "wrong.json"
            wrong.write_text("[]", encoding="utf-8")
            with self.assertRaises(ValueError):
                bench.load(wrong)


if __name__ == "__main__":
    unittest.main()
