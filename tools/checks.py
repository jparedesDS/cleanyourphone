"""Post-change health checks for CleanYourPhone."""

from __future__ import annotations

from typing import Any, Dict, List

try:  # imported as tools.checks
    from . import adb, protected, ui
except ImportError:  # run from tools/
    import adb  # type: ignore
    import protected  # type: ignore
    import ui  # type: ignore


def verify_checks(serial: str) -> List[Dict[str, str]]:
    checks: List[Dict[str, str]] = []

    def add(check: str, status: str, detail: str) -> None:
        checks.append({"check": check, "status": status, "detail": detail})

    probe = adb.probe_device(serial)
    add("Device", "PASS", f"{probe['brand']} {probe['model']} ({probe['device']}), Android {probe['android']}")
    add("Android", "PASS" if probe["sdk"] >= 26 else "WARN", f"SDK {probe['sdk']}")

    if probe["is_tv"]:
        add("Device type", "FAIL", "This is an Android TV/box; use cleanyour.tv, not this skill")
    else:
        add("Device type", "PASS", "Phone/tablet")

    if probe["managed"] is None:
        add("Managed device", "WARN", "Cannot read dumpsys device_policy; do not change packages")
    elif probe["managed"]:
        add("Managed device", "WARN", "Device owner or profile owner detected; do not change packages")
    else:
        add("Managed device", "PASS", "No device/profile owner")

    users = probe.get("users")
    if users is None:
        add("Android users", "WARN", "Cannot read pm list users")
    elif users > 1:
        add("Android users", "WARN", f"{users} users (work profile, guest or clone); do not change packages")
    else:
        add("Android users", "PASS", "1 user")

    enabled = adb.package_set(serial, "-e")
    try:
        holders, supported = adb.role_holders(serial)
    except adb.AdbError as exc:
        add("Role holders", "FAIL", f"cannot read: {exc}")
        holders, supported = {}, False
    telephony = probe["telephony"]
    if telephony:
        for role, label in (("DIALER", "Dialer"), ("SMS", "SMS")):
            values = holders.get(role, [])
            live = [package for package in values if package in enabled]
            add(label, "PASS" if live else "FAIL", ", ".join(live) or f"no enabled {label.lower()} app")
    else:
        add("Telephony", "WARN", "No telephony package (tablet or Wi-Fi-only device)")

    home_values = holders.get("HOME", [])
    home_live = [package for package in home_values if package in enabled]
    add("Home", "PASS" if home_live else "FAIL", ", ".join(home_live) or "no enabled Home app")
    try:
        ime = adb.read_default_ime(serial)
        ime_status = "PASS" if ime and ime in enabled else "FAIL"
        ime_detail = ime or "no default IME"
        if ime and ime not in enabled:
            ime_detail += " (disabled)"
        add("Keyboard", ime_status, ime_detail)
    except adb.AdbError as exc:
        add("Keyboard", "FAIL", f"cannot read default_input_method: {exc}")
    if supported and not holders.get("EMERGENCY"):
        add("Emergency role", "WARN", "No emergency role holder reported")
    for package, label in (
        ("com.google.android.gms", "Play Services"),
        ("com.android.vending", "Play Store"),
    ):
        if adb.package_installed(serial, package):
            add(label, "PASS" if package in enabled else "FAIL", package)
        else:
            add(label, "WARN", f"{package} not installed")

    disabled = adb.package_set(serial, "-d")
    applied = adb.load_applied(serial).get("packages", {})
    _, meta = adb.latest_backup(serial)
    meta_fingerprint = str(((meta or {}).get("probe") or {}).get("fingerprint", "")).strip()
    if meta and meta_fingerprint and meta_fingerprint == probe["fingerprint"]:
        before = set(meta.get("enabled", []))
        bad = sorted(package for package in disabled if package in before and protected.is_protected(package))
        if bad:
            add("Protected packages", "FAIL", "disabled: " + ", ".join(bad[:8]))
        else:
            add("Protected packages", "PASS", "none disabled")
    else:
        bad = sorted(package for package in disabled if package in applied and protected.is_protected(package))
        if bad:
            add("Protected packages", "FAIL", "disabled by this tool: " + ", ".join(bad[:8]))
        elif any(protected.is_protected(package) for package in disabled):
            add("Protected packages", "WARN", "protected packages were already disabled outside this tool")
        else:
            add("Protected packages", "PASS", "none disabled")

    reenabled = sorted(package for package in applied if package not in disabled)
    if reenabled:
        add("Recorded changes", "WARN", "re-enabled since the change (OTA?): " + ", ".join(reenabled[:8]))
    elif applied:
        add("Recorded changes", "PASS", f"{len(applied)} package(s) still disabled")
    else:
        add("Recorded changes", "PASS", "no packages disabled by this tool")

    level = probe["battery"].get("level")
    if level is not None:
        add("Battery", "WARN" if level < 15 else "PASS", f"{level}%")

    for label, command, bad_value in (
        ("Airplane mode", "settings get global airplane_mode_on", "1"),
        ("Wi-Fi", "settings get global wifi_on", "0"),
        ("Mobile data", "settings get global mobile_data", "0"),
    ):
        value = adb.shell(command, serial=serial).strip()
        if value == bad_value:
            add(label, "WARN", f"{value} (off)")
        else:
            add(label, "PASS", value or "unknown")

    boot = adb.getprop(serial, "sys.boot_completed")
    add("Boot completed", "PASS" if boot == "1" else "WARN", boot or "not reported")

    return checks


def print_checks(checks: List[Dict[str, str]]) -> None:
    ui.print_table(["CHECK", "STATUS", "DETAIL"], [[c["check"], c["status"], c["detail"]] for c in checks])


def has_failures(checks: List[Dict[str, str]]) -> bool:
    return any(check["status"] == "FAIL" for check in checks)
