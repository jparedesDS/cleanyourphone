"""Extra CleanYourPhone commands: battery, DNS, report, profiles, protected, validate."""

from __future__ import annotations

import argparse
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

try:  # imported as tools.extra
    from . import adb, checks, profiles, protected, ui
except ImportError:  # run from tools/
    import adb  # type: ignore
    import checks  # type: ignore
    import profiles  # type: ignore
    import protected  # type: ignore
    import ui  # type: ignore

BATTERY_DIR = Path(os.environ.get("CLEANYOURPHONE_BATTERY", adb.ROOT / "battery"))


def valid_hostname(hostname: str) -> bool:
    """A conservative hostname check for the Private DNS specifier."""
    hostname = hostname.strip()
    if not hostname or ".." in hostname or len(hostname) > 253:
        return False
    if any(not label or len(label) > 63 for label in hostname.split(".")):
        return False
    return bool(re.match(r"^[A-Za-z0-9]([A-Za-z0-9.-]*[A-Za-z0-9])?$", hostname))


def _record_dns_before(serial: str) -> Dict[str, Any]:
    """Record the original value and persist it *before* changing anything."""
    changes = adb.load_changes(serial)
    if "dns" not in changes:
        changes["dns"] = {"before": adb.dns_status(serial), "at": adb.now()}
        adb.save_changes(serial, changes)
    return changes


def restore_dns(serial: str) -> None:
    changes = adb.load_changes(serial)
    before = changes.get("dns", {}).get("before")
    if not before:
        print("No DNS change recorded; leaving Private DNS alone.")
        return
    mode = before.get("mode") or "opportunistic"
    specifier = before.get("specifier") or ""
    if mode not in ("off", "opportunistic", "hostname"):
        mode = "opportunistic"
    if mode == "hostname" and not specifier:
        mode = "opportunistic"
    if specifier:
        if not valid_hostname(specifier):
            ui.die("the recorded Private DNS specifier is invalid; restore it manually in Settings")
        adb.shell(f"settings put global private_dns_specifier {specifier}", serial=serial)
    adb.shell(f"settings put global private_dns_mode {mode}", serial=serial)
    changes.pop("dns", None)
    adb.save_changes(serial, changes)
    print(f"DNS restored to mode={mode}" + (f" specifier={specifier}" if specifier else ""))


def cmd_dns(args: argparse.Namespace) -> int:
    serial = adb.pick_serial(args.serial)
    if args.dns_command == "status":
        status = adb.dns_status(serial)
        if args.json:
            ui.print_json(status)
        else:
            print(f"Private DNS mode:      {status['mode']}")
            print(f"Private DNS specifier: {status['specifier'] or '(none)'}")
        return 0

    if args.dns_command == "set":
        hostname = (args.hostname or "").strip()
        if not valid_hostname(hostname):
            ui.die(f"invalid DNS hostname: {hostname!r}")
        changes = _record_dns_before(serial)
        adb.shell(f"settings put global private_dns_specifier {hostname}", serial=serial)
        adb.shell("settings put global private_dns_mode hostname", serial=serial)
        after = adb.dns_status(serial)
        if after["mode"] != "hostname" or after["specifier"] != hostname:
            ui.die(f"Private DNS did not stick: {after}")
        changes["dns"]["after"] = after
        changes["dns"]["at"] = adb.now()
        adb.save_changes(serial, changes)
        print(f"Private DNS set to {hostname}. Undo: python tools/phone.py dns off")
        print("An ad-blocking resolver over Private DNS blocks many in-app ads/trackers, not YouTube ads.")
        return 0

    if args.dns_command == "off":
        changes = _record_dns_before(serial)
        adb.shell("settings put global private_dns_mode opportunistic", serial=serial)
        after = adb.dns_status(serial)
        if after["mode"] != "opportunistic":
            ui.die(f"Private DNS did not return to opportunistic: {after}")
        changes["dns"]["after"] = after
        changes["dns"]["at"] = adb.now()
        adb.save_changes(serial, changes)
        print("Private DNS set to opportunistic (the Android default).")
        return 0

    if args.dns_command == "restore":
        restore_dns(serial)
        return 0

    ui.die("unknown dns command")
    return 2


def cmd_battery(args: argparse.Namespace) -> int:
    serial = adb.pick_serial(args.serial)
    if args.battery_command == "reset":
        adb.shell("dumpsys batterystats --reset", serial=serial)
        print("Battery stats reset. Leave the phone idle for 8 hours, then run:")
        print("  python tools/phone.py battery snapshot")
        return 0

    if args.battery_command == "snapshot":
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder = BATTERY_DIR / stamp
        folder.mkdir(parents=True, exist_ok=True)
        commands = {
            "batterystats.txt": "dumpsys batterystats --charged",
            "battery.txt": "dumpsys battery",
            "deviceidle.txt": "dumpsys deviceidle",
            "alarm.txt": "dumpsys alarm",
            "power.txt": "dumpsys power",
        }
        for name, command in commands.items():
            result = adb.adb_run(["shell", command], serial=serial)
            text = result.stdout
            if result.stderr.strip():
                text += "\n# stderr:\n" + result.stderr
            (folder / name).write_text(text, encoding="utf-8", errors="replace")
        print(f"Battery snapshot written to {folder}")
        return 0

    if args.battery_command == "compare":
        first = Path(args.first)
        second = Path(args.second)
        keys = [
            "Time on battery:",
            "Screen on:",
            "Deep sleep:",
            "Awake:",
            "Estimated power use (mAh):",
            "Capacity:",
            "Discharge:",
        ]
        rows = []
        values = {}
        for label, folder in (("A", first), ("B", second)):
            path = folder / "batterystats.txt"
            if not path.is_file():
                ui.die(f"missing {path}. Run `python tools/phone.py battery snapshot` first.")
            text = path.read_text(encoding="utf-8", errors="replace")
            values[label] = {}
            for key in keys:
                match = re.search(rf"(?m)^\s*{re.escape(key)}\s*(.*)$", text)
                values[label][key] = match.group(1).strip() if match else "?"
        for key in keys:
            rows.append([key, values["A"][key], values["B"][key]])
        ui.print_table(["METRIC", "A", "B"], rows)
        return 0

    ui.die("unknown battery command")
    return 2


def cmd_report(args: argparse.Namespace) -> int:
    serial = adb.pick_serial(args.serial)
    probe = adb.probe_device(serial)
    folder, meta = adb.latest_backup(serial)
    applied = adb.load_applied(serial)
    result = checks.verify_checks(serial)
    dns = adb.dns_status(serial)

    lines: List[str] = [
        "# CleanYourPhone report",
        "",
        f"- Date: {adb.now()}",
        f"- Device: {probe['brand']} {probe['model']} ({probe['device']})",
        f"- Android: {probe['android']} (SDK {probe['sdk']})",
        f"- Build: {probe['build']}",
        f"- Fingerprint: `{probe['fingerprint']}`",
        f"- Backup: `{folder}`" if folder else "- Backup: none",
        f"- Managed: {'unknown' if probe['managed'] is None else ('yes' if probe['managed'] else 'no')}",
        f"- Private DNS: `{dns['mode']}`" + (f" `{dns['specifier']}`" if dns["specifier"] else ""),
        "",
        "## Disabled by this tool",
        "",
    ]
    packages = applied.get("packages", {})
    if packages:
        lines += ["| Package | Why | When | Profile |", "|---|---|---|---|"]
        for package, record in sorted(packages.items()):
            lines.append(
                f"| `{package}` | {record.get('why', '')} | {record.get('at', '')} | {record.get('profile', '')} |"
            )
    else:
        lines.append("(none)")

    lines += ["", "## Verification", "", "| Check | Status | Detail |", "|---|---|---|"]
    for check in result:
        lines.append(f"| {check['check']} | {check['status']} | {check['detail']} |")

    lines += [
        "",
        "## Undo",
        "",
        "```bash",
        "python tools/phone.py restore",
        "```",
        "",
        "If the phone does not boot, see `docs/RESTORE.md`.",
        "",
    ]

    path = (folder / "report.md") if folder else (adb.STATE_DIR / "report.md")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written to {path}")
    if args.json:
        ui.print_json({"path": str(path), "packages": packages, "checks": result, "dns": dns})
    return 1 if checks.has_failures(result) else 0


def cmd_profiles(args: argparse.Namespace) -> int:
    loaded = profiles.load_profiles()
    if args.json:
        ui.print_json([profiles.summary(profile) for profile in loaded])
        return 0
    rows = [
        [
            profile.get("id", ""),
            profile.get("brand", ""),
            profile.get("marketing_name") or profile.get("model", ""),
            ", ".join(profile.get("android", [])),
            profiles.verification_level(profile),
            len(profile.get("tested", [])),
            len(profile.get("sources", [])),
        ]
        for profile in loaded
    ]
    ui.print_table(["ID", "BRAND", "MODEL", "ANDROID", "VERIFIED", "TESTS", "SOURCES"], rows)
    return 0


def cmd_protected(args: argparse.Namespace) -> int:
    patterns = protected.patterns()
    if args.json:
        ui.print_json([{"pattern": pattern, "reason": reason} for pattern, reason in patterns])
        return 0
    ui.print_table(["PATTERN", "REASON"], patterns)
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    try:
        loaded = profiles.load_profiles(strict=True)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    errors: List[str] = []
    for profile in loaded:
        errors += profiles.validate_profile(profile, Path(profile.get("_path", "")))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"{len(errors)} error(s) in {len(loaded)} profile(s).")
        return 1
    print(f"OK: {len(loaded)} profile(s) valid.")
    return 0


def add_subparsers(sub: argparse._SubParsersAction) -> None:
    battery = sub.add_parser("battery", help="battery baseline: reset, snapshot, compare")
    battery_sub = battery.add_subparsers(dest="battery_command", required=True)
    reset = battery_sub.add_parser("reset", help="reset batterystats before an idle test")
    reset.set_defaults(func=cmd_battery)
    snapshot = battery_sub.add_parser("snapshot", help="save batterystats, battery, deviceidle, alarm and power")
    snapshot.set_defaults(func=cmd_battery)
    compare = battery_sub.add_parser("compare", help="compare two snapshot folders")
    compare.add_argument("first")
    compare.add_argument("second")
    compare.set_defaults(func=cmd_battery)

    dns = sub.add_parser("dns", help="Private DNS: status, set, off, restore")
    dns_sub = dns.add_subparsers(dest="dns_command", required=True)
    status = dns_sub.add_parser("status", help="show Private DNS mode and specifier")
    status.set_defaults(func=cmd_dns)
    set_cmd = dns_sub.add_parser("set", help="set an ad-blocking Private DNS hostname")
    set_cmd.add_argument("hostname")
    set_cmd.set_defaults(func=cmd_dns)
    off = dns_sub.add_parser("off", help="return Private DNS to opportunistic")
    off.set_defaults(func=cmd_dns)
    restore = dns_sub.add_parser("restore", help="restore the value recorded before the first change")
    restore.set_defaults(func=cmd_dns)

    report = sub.add_parser("report", help="write a Markdown report with changes and verification")
    report.set_defaults(func=cmd_report)

    profiles_cmd = sub.add_parser("profiles", help="list available profiles")
    profiles_cmd.set_defaults(func=cmd_profiles)

    protected_cmd = sub.add_parser("protected", help="list the packages that must never be disabled")
    protected_cmd.set_defaults(func=cmd_protected)

    validate = sub.add_parser("validate", help="validate every profile")
    validate.set_defaults(func=cmd_validate)
