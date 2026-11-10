"""Extra CleanYourPhone commands: battery, DNS, report, profiles, protected, validate."""

from __future__ import annotations

import argparse
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

try:  # imported as tools.extra
    from . import adb, bench, checks, profiles, protected, ui
except ImportError:  # run from tools/
    import adb  # type: ignore
    import bench  # type: ignore
    import checks  # type: ignore
    import profiles  # type: ignore
    import protected  # type: ignore
    import ui  # type: ignore

BATTERY_DIR = Path(os.environ.get("CLEANYOURPHONE_BATTERY", adb.ROOT / "battery"))

DNS_PROVIDERS = {
    "adguard": ("dns.adguard-dns.com", "AdGuard DNS: ads and trackers"),
    "adguard-family": ("family.adguard-dns.com", "AdGuard Family: ads, trackers and adult sites"),
    "controld": ("p2.freedns.controld.com", "Control D free: ads and trackers"),
    "mullvad": ("adblock.dns.mullvad.net", "Mullvad DNS: ads and trackers"),
}


def valid_hostname(hostname: str) -> bool:
    """A conservative hostname check for the Private DNS specifier."""
    hostname = hostname.strip()
    if not hostname or ".." in hostname or len(hostname) > 253:
        return False
    if any(not label or len(label) > 63 for label in hostname.split(".")):
        return False
    return bool(re.match(r"^[A-Za-z0-9]([A-Za-z0-9.-]*[A-Za-z0-9])?$", hostname))


def resolve_dns_provider(value: str) -> str | None:
    """Resolve a preset alias or a raw hostname to a valid DNS hostname."""
    value = (value or "").strip()
    preset = DNS_PROVIDERS.get(value.lower())
    if preset:
        return preset[0]
    return value if valid_hostname(value) else None


def _resolve(serial: str, host: str) -> str:
    """Return the IP a host resolves to on the phone, or an empty string."""
    try:
        out = adb.shell(f"ping -c 1 -W 3 {host}", serial=serial, timeout=20)
    except adb.AdbError:
        return ""
    match = re.search(r"PING \S+ \(([^)]+)\)", out)
    return match.group(1) if match else ""


def dns_check(serial: str) -> Dict[str, Any]:
    """Check an ad domain and a control domain from the phone."""
    ad_ip = _resolve(serial, "doubleclick.net")
    control_ip = _resolve(serial, "wikipedia.org")
    online = control_ip not in ("", "0.0.0.0", "::")
    blocked = None if not online else ad_ip in ("", "0.0.0.0", "::")
    return {
        "ad_domain": "doubleclick.net",
        "ad_ip": ad_ip,
        "ad_blocked": blocked,
        "control_domain": "wikipedia.org",
        "control_ip": control_ip,
        "online": online,
    }


def _record_dns_before(serial: str) -> Dict[str, Any]:
    """Record the original value and persist it *before* changing anything."""
    changes = adb.load_changes(serial)
    if "dns" not in changes:
        changes["dns"] = {"before": adb.dns_status(serial), "at": adb.now()}
        adb.save_changes(serial, changes)
    return changes


def apply_dns(serial: str, before: Any) -> tuple:
    """Apply a recorded Private DNS state and return (mode, specifier)."""
    if not isinstance(before, dict):
        raise ValueError("no Private DNS state to restore")
    mode = str(before.get("mode") or "opportunistic")
    specifier = str(before.get("specifier") or "")
    if mode not in ("off", "opportunistic", "hostname"):
        mode = "opportunistic"
    if mode == "hostname" and not specifier:
        mode = "opportunistic"
    if specifier:
        if not valid_hostname(specifier):
            ui.die("the recorded Private DNS specifier is invalid; restore it manually in Settings")
        adb.shell(f"settings put global private_dns_specifier {specifier}", serial=serial)
    adb.shell(f"settings put global private_dns_mode {mode}", serial=serial)
    return mode, specifier


def restore_dns(serial: str) -> None:
    changes = adb.load_changes(serial)
    before = changes.get("dns", {}).get("before")
    if not before:
        print("No DNS change recorded; leaving Private DNS alone.")
        return
    mode, specifier = apply_dns(serial, before)
    changes.pop("dns", None)
    adb.save_changes(serial, changes)
    print(f"DNS restored to mode={mode}" + (f" specifier={specifier}" if specifier else ""))


def cmd_dns(args: argparse.Namespace) -> int:
    if args.dns_command == "providers":
        data = {
            name: {"host": host, "description": description}
            for name, (host, description) in sorted(DNS_PROVIDERS.items())
        }
        if args.json:
            ui.print_json(data)
        else:
            ui.print_table(
                ["PRESET", "HOST", "WHAT IT BLOCKS"],
                [[name, item["host"], item["description"]] for name, item in data.items()],
            )
        return 0

    serial = adb.pick_serial(args.serial)
    if args.dns_command == "check":
        result = dns_check(serial)
        if args.json:
            ui.print_json(result)
        else:
            ui.print_table(
                ["CHECK", "VALUE"],
                [
                    ["Ad domain", result["ad_domain"]],
                    ["Ad resolves to", result["ad_ip"] or "(no answer)"],
                    ["Ad blocked", "yes" if result["ad_blocked"] else ("cannot test" if result["ad_blocked"] is None else "no")],
                    ["Control domain", result["control_domain"]],
                    ["Control resolves to", result["control_ip"] or "(no answer)"],
                    ["Online", "yes" if result["online"] else "no"],
                ],
            )
        if result["ad_blocked"] is True and result["online"]:
            return 0
        ui.warn("ads are not confirmed blocked; check Private DNS and the network")
        return 1

    if args.dns_command == "status":
        status = adb.dns_status(serial)
        if args.json:
            ui.print_json(status)
        else:
            print(f"Private DNS mode:      {status['mode']}")
            print(f"Private DNS specifier: {status['specifier'] or '(none)'}")
        return 0

    if args.dns_command == "set":
        hostname = resolve_dns_provider(args.hostname)
        if not hostname:
            ui.die(f"invalid DNS hostname or preset: {args.hostname!r}")
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
    if not loaded:
        print("ERROR: no profiles found. Check CLEANYOURPHONE_PROFILES or the installed package data.")
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


def cmd_bench(args: argparse.Namespace) -> int:
    if args.bench_command == "snapshot":
        serial = adb.pick_serial(args.serial)
        data = bench.measure(serial)
        path = bench.save(data, args.label)
        if args.json:
            ui.print_json({"path": str(path), "data": data})
        else:
            print(f"Bench snapshot written to {path}")
            print(
                f"RAM {data['ram_available_mb']} MB, {data['processes']} processes, "
                f"{data['packages_enabled']} enabled / {data['packages_disabled']} disabled packages"
            )
        return 0

    if args.bench_command == "compare":
        before = bench.load(Path(args.before))
        after = bench.load(Path(args.after))
        rows = bench.compare(before, after)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = bench.write_markdown(before, after, rows, bench.BENCH_DIR / f"compare-{stamp}.md")
        if args.json:
            ui.print_json({"path": str(path), "rows": rows})
        else:
            ui.print_table(
                ["METRIC", "BEFORE", "AFTER", "CHANGE"],
                [
                    [
                        row["label"],
                        row["before"],
                        row["after"],
                        f"{row['delta']:+g}" + (f" ({row['pct']:+.1f}%)" if row["pct"] is not None else ""),
                    ]
                    for row in rows
                ],
            )
            print(f"Comparison written to {path}")
            print("Approximate, measured on this phone; not causal.")
        return 0

    if args.bench_command == "list":
        paths = sorted(bench.BENCH_DIR.glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True)
        if args.json:
            ui.print_json([str(path) for path in paths])
        elif not paths:
            print("(none)")
        else:
            for path in paths:
                print(path)
        return 0

    ui.die("unknown bench command")
    return 2


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

    dns = sub.add_parser("dns", help="Private DNS: providers, status, set, check, off, restore")
    dns_sub = dns.add_subparsers(dest="dns_command", required=True)
    providers = dns_sub.add_parser("providers", help="list ad-blocking DNS presets")
    providers.set_defaults(func=cmd_dns)
    status = dns_sub.add_parser("status", help="show Private DNS mode and specifier")
    status.set_defaults(func=cmd_dns)
    set_cmd = dns_sub.add_parser("set", help="set a preset or an ad-blocking Private DNS hostname")
    set_cmd.add_argument("hostname")
    set_cmd.set_defaults(func=cmd_dns)
    check = dns_sub.add_parser("check", help="check whether ads are blocked and the phone is online")
    check.set_defaults(func=cmd_dns)
    off = dns_sub.add_parser("off", help="return Private DNS to opportunistic")
    off.set_defaults(func=cmd_dns)
    restore = dns_sub.add_parser("restore", help="restore the value recorded before the first change")
    restore.set_defaults(func=cmd_dns)

    bench_cmd = sub.add_parser("bench", help="measure RAM, packages and settings before/after")
    bench_sub = bench_cmd.add_subparsers(dest="bench_command", required=True)
    bench_snapshot = bench_sub.add_parser("snapshot", help="save a local benchmark snapshot")
    bench_snapshot.add_argument("--label", default="snapshot", help="label, e.g. before or after")
    bench_snapshot.set_defaults(func=cmd_bench)
    bench_compare = bench_sub.add_parser("compare", help="compare two saved snapshots")
    bench_compare.add_argument("before")
    bench_compare.add_argument("after")
    bench_compare.set_defaults(func=cmd_bench)
    bench_list = bench_sub.add_parser("list", help="list saved snapshots")
    bench_list.set_defaults(func=cmd_bench)

    report = sub.add_parser("report", help="write a Markdown report with changes and verification")
    report.set_defaults(func=cmd_report)

    profiles_cmd = sub.add_parser("profiles", help="list available profiles")
    profiles_cmd.set_defaults(func=cmd_profiles)

    protected_cmd = sub.add_parser("protected", help="list the packages that must never be disabled")
    protected_cmd.set_defaults(func=cmd_protected)

    validate = sub.add_parser("validate", help="validate every profile")
    validate.set_defaults(func=cmd_validate)
