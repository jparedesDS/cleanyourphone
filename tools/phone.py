#!/usr/bin/env python3
"""CleanYourPhone guardrail CLI.

A stdlib-only wrapper around adb. It never installs anything on the phone and never uninstalls a
package: the only state changes are `pm disable-user --user 0 <package>` and its undo,
`pm enable <package>`.

Run `python tools/phone.py --help` for the commands.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:  # imported as tools.phone
    from . import adb, checks, extra, profiles, protected, ui
except ImportError:  # run as tools/phone.py
    import adb  # type: ignore
    import checks  # type: ignore
    import extra  # type: ignore
    import profiles  # type: ignore
    import protected  # type: ignore
    import ui  # type: ignore


def load_applied(serial: str) -> Dict[str, Any]:
    return adb.load_applied(serial)


def save_applied(serial: str, data: Dict[str, Any]) -> None:
    adb.save_applied(serial, data)


def require_backup(serial: str, probe: Optional[Dict[str, Any]] = None):
    folder, meta = adb.latest_backup(serial)
    if not folder or not meta:
        ui.die("no backup for this phone. Run `python tools/phone.py backup` first.")
    if probe is not None:
        recorded = meta.get("probe") or {}
        recorded_fingerprint = str(recorded.get("fingerprint", "")).strip()
        current_fingerprint = str(probe.get("fingerprint", "")).strip()
        if not recorded_fingerprint:
            ui.die("the newest backup has no build fingerprint. Run `python tools/phone.py backup` again.")
        if recorded_fingerprint != current_fingerprint:
            ui.die(
                "the newest backup is from a different build. An OTA may have changed the package "
                "list; run `python tools/phone.py backup` again before changing anything."
            )
    return folder, meta


def guard_writable(serial: str) -> Dict[str, Any]:
    """Refuse to change packages on a TV, a managed phone, a multi-user phone or old Android."""
    probe = adb.probe_device(serial)
    if probe["is_tv"]:
        ui.die("this is an Android TV/box. Use https://cleanyour.tv instead.")
    if probe["managed"] is None:
        ui.die(
            "cannot read the device policy (dumpsys device_policy). Refusing to change packages on an "
            "unknown device state. Reconnect the USB cable and run `python tools/phone.py doctor`."
        )
    if probe["managed"]:
        ui.die("this phone has a device/profile owner (work or MDM). Changing packages can break policy.")
    if probe.get("users") is None:
        ui.die("cannot read `pm list users`. Refusing to change packages while the user list is unknown.")
    if probe["users"] > 1:
        ui.die(
            "this phone has more than one Android user (work profile, guest or clone). `pm disable-user "
            "--user 0` can still affect shared packages; remove the extra user or stop here."
        )
    if probe["sdk"] < 26:
        ui.die(f"Android {probe['android']} (SDK {probe['sdk']}) is older than Android 8. Use the backup and the safe list only.")
    return probe


def guard_roles(serial: str, probe: Dict[str, Any]) -> tuple:
    """Read and validate the critical role holders before any package change.

    Fails closed: if a role, the keyboard or the enabled state of a holder cannot be read, no
    package is disabled. An empty role is treated as an already-broken phone, not as permission.
    """
    try:
        holders, supported = adb.role_holders(serial)
    except adb.AdbError as exc:
        ui.die(f"cannot read the current role holders: {exc}. Refusing to change packages.")
    try:
        ime = adb.read_default_ime(serial)
    except adb.AdbError as exc:
        ui.die(f"cannot read the current keyboard: {exc}. Refusing to change packages.")
    if not ime:
        ui.die("cannot determine the current keyboard (default_input_method is empty). Set a keyboard, then retry.")

    enabled = adb.package_set(serial, "-e")
    missing = []
    if probe.get("telephony"):
        for role in ("DIALER", "SMS"):
            if not holders.get(role):
                missing.append(role)
    if not holders.get("HOME"):
        missing.append("HOME")
    if missing:
        ui.die(
            "cannot determine the current " + ", ".join(missing) + " app. The phone may already be "
            "broken; fix it before changing packages."
        )

    for role in ("DIALER", "SMS", "HOME"):
        for package in holders.get(role, []):
            if package not in enabled:
                ui.die(
                    f"the current {role} app {package} is disabled. Re-enable it before changing "
                    "packages; otherwise a batch could leave the phone without it."
                )
    if ime not in enabled:
        ui.die(f"the current keyboard {ime} is disabled. Re-enable it before changing packages.")
    if not supported:
        print("note: `cmd role` is unavailable on this Android version; roles were read from settings.")
    return holders, ime


def role_block_reason(
    serial: str,
    package: str,
    holders: Optional[Dict[str, List[str]]] = None,
    ime: Optional[str] = None,
) -> Optional[str]:
    if holders is None or ime is None:
        holders, ime = guard_roles(serial, adb.probe_device(serial))
    return profiles.role_conflict(package, holders, ime)


def disable_one(
    serial: str,
    package: str,
    meta: Dict[str, Any],
    applied: Dict[str, Any],
    why: str = "manual",
    profile: Optional[str] = None,
    holders: Optional[Dict[str, List[str]]] = None,
    ime: Optional[str] = None,
    never: Optional[set] = None,
    done: Optional[List[str]] = None,
) -> bool:
    if not adb.valid_package(package):
        ui.die(f"invalid package name: {package!r}")
    protected_reason = protected.reason(package)
    if protected_reason:
        ui.die(f"refusing {package}: protected ({protected_reason})")
    if never and package in never:
        ui.die(f"refusing {package}: the matching profile marks it as never-touch.")

    if package not in set(meta.get("enabled", [])):
        if package in set(meta.get("disabled", [])):
            print(f"SKIP {package}: already disabled at backup time")
            return False
        ui.die(f"refusing {package}: it was not installed and enabled in the backup. Run `phone.py backup` again.")

    if package in adb.package_set(serial, "-d"):
        print(f"SKIP {package}: already disabled")
        return False

    block = role_block_reason(serial, package, holders, ime)
    if block:
        ui.die(f"refusing {package}: {block}. Set a replacement first, then re-check the roles.")

    result = adb.adb_run(["shell", f"pm disable-user --user 0 {package}"], serial=serial)
    output = (result.stdout + "\n" + result.stderr).strip()
    if "SecurityException" in output or re.search(r"(?im)^\s*(error|exception)", output):
        ui.die(f"pm disable-user refused {package}: {output or 'no output'}")

    # Record before the post-check. If adb succeeds and the next query fails, restore must still
    # know that this package may have been disabled.
    applied.setdefault("packages", {})[package] = {
        "at": adb.now(),
        "why": why,
        "profile": profile or "",
        "backup": str(meta.get("timestamp", "")),
    }
    save_applied(serial, applied)
    if done is not None:
        done.append(package)
    print(f"DISABLED {package}")

    if package not in adb.package_set(serial, "-d"):
        ui.die(f"pm disable-user reported success but {package} is not disabled. It is recorded; run restore.")
    return True


def rollback_batch(serial: str, packages: List[str], applied: Dict[str, Any]) -> None:
    """Best-effort re-enable of the packages a failed batch disabled."""
    for package in packages:
        try:
            if package in adb.package_set(serial, "-d"):
                enable_one(serial, package, applied)
            else:
                applied.setdefault("packages", {}).pop(package, None)
                save_applied(serial, applied)
        except BaseException as exc:  # keep trying the rest, then report
            print(f"ROLLBACK FAILED {package}: {exc}", file=sys.stderr)


def enable_one(serial: str, package: str, applied: Dict[str, Any], record: bool = True) -> bool:
    if not adb.valid_package(package):
        ui.die(f"invalid package name: {package!r}")
    result = adb.adb_run(["shell", f"pm enable {package}"], serial=serial)
    output = (result.stdout + "\n" + result.stderr).strip()
    if "SecurityException" in output or re.search(r"(?im)^\s*(error|exception)", output):
        ui.die(f"pm enable refused {package}: {output or 'no output'}")
    if package not in adb.package_set(serial, "-e"):
        ui.die(f"pm enable did not enable {package}. Output: {output or 'no output'}")
    if record:
        applied.setdefault("packages", {}).pop(package, None)
        save_applied(serial, applied)
    print(f"ENABLED {package}")
    return True


def cmd_doctor(args: argparse.Namespace) -> int:
    if not adb.ADB:
        print("ADB ......... not found")
        print("")
        print("Install Android SDK Platform-Tools, add it to PATH, or set ADB to the full path")
        print("of the adb executable. Then run this command again.")
        return 2
    print(f"ADB ......... {adb.ADB}")
    try:
        version = adb.adb_run(["version"])
        first = (version.stdout or version.stderr).splitlines()
        print(f"ADB version . {first[0] if first else 'unknown'}")
        found = adb.devices()
    except adb.AdbError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"Devices ..... {adb.format_devices(found)}")
    if not found:
        print("")
        print("Connect the phone by USB, enable Developer options > USB debugging,")
        print("and accept the 'Allow USB debugging?' prompt.")
        return 2
    try:
        serial = adb.pick_serial(args.serial)
    except adb.AdbError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    probe = adb.probe_device(serial)
    print("")
    print(f"Device ...... {probe['brand']} {probe['model']} ({probe['device']})")
    print(f"Android ..... {probe['android']} (SDK {probe['sdk']})")
    print(f"Build ....... {probe['build']}")
    print(f"Fingerprint . {probe['fingerprint']}")
    print(f"Bootloader .. {probe['verified_boot'] or '?'} (locked={probe['flash_locked'] or '?'})")
    managed = probe["managed"]
    print(f"Managed ..... {'unknown (cannot read device policy)' if managed is None else ('yes' if managed else 'no')}")
    users = probe.get("users")
    print(f"Users ....... {users if users is not None else 'unknown (cannot read pm list users)'}")
    print(f"Telephony ... {'yes' if probe['telephony'] else 'no'}")
    battery = probe["battery"]
    print(f"Battery ..... {battery.get('level', '?')}%")

    folder, meta = adb.latest_backup(serial)
    print(f"Backup ...... {folder if folder else 'none (run: python tools/phone.py backup)'}")

    profile_error = ""
    try:
        loaded = profiles.load_profiles(strict=True)
    except ValueError as exc:
        profile_error = str(exc)
        loaded = profiles.load_profiles()
    exact = [p for p in loaded if not p.get("generic") and profiles.profile_matches(p, probe)]
    matches = [p["id"] for p in exact]
    auto = [p["id"] for p in exact if profiles.build_matches(p, probe)]
    references = [p["id"] for p in loaded if p.get("generic") and profiles.profile_matches(p, probe)]
    references += [p["id"] for p in exact if not profiles.build_matches(p, probe)]
    print(f"Profiles .... {', '.join(matches) if matches else 'none exact (classify manually)'}")
    print(f"Auto-apply .. {', '.join(auto) if auto else 'none (use plan + disable)'}")
    if references:
        print(f"Reference ... {', '.join(sorted(set(references)))} (not auto-applicable)")

    warnings = []
    if profile_error:
        warnings.append(f"Profile error: {profile_error}")
    if probe["is_tv"]:
        warnings.append("This is an Android TV/box. Use https://cleanyour.tv instead.")
    if managed is None:
        warnings.append("Cannot read the device policy. Do not change packages; reconnect and retry.")
    elif managed:
        warnings.append("Device/profile owner detected. Stop: this is a managed phone.")
    if users is None:
        warnings.append("Cannot read `pm list users`. Do not change packages while it is unknown.")
    elif users > 1:
        warnings.append("More than one Android user (work profile, guest or clone). Stop and ask.")
    if folder and meta:
        recorded_fingerprint = str((meta.get("probe") or {}).get("fingerprint", "")).strip()
        if not recorded_fingerprint:
            warnings.append("The newest backup has no build fingerprint. Run `backup` again before changing packages.")
        elif recorded_fingerprint != probe["fingerprint"]:
            warnings.append("The newest backup is from a different build. Run `backup` again before changing packages.")
    if probe["sdk"] < 26:
        warnings.append("Android is older than 8. Role commands may not exist; be extra careful.")
    if probe["flash_locked"] == "0" or probe["verified_boot"] not in ("green", ""):
        warnings.append("Bootloader unlocked or custom ROM. Debloating works, but banking/DRM may be affected.")
    level = battery.get("level")
    if isinstance(level, int) and level < 30:
        warnings.append("Battery below 30%. Charge before the reboot.")
    if not matches:
        warnings.append("No exact profile. Classify every package manually and ask before each one.")
    elif not auto:
        warnings.append("An exact profile exists but not for this build. Use `plan` and disable one by one.")
    if warnings:
        print("")
        for warning in warnings:
            print(f"WARNING: {warning}")
    return 0


def cmd_probe(args: argparse.Namespace) -> int:
    serial = adb.pick_serial(args.serial)
    probe = adb.probe_device(serial)
    profile_error = ""
    try:
        loaded = profiles.load_profiles(strict=True)
    except ValueError as exc:
        profile_error = str(exc)
        loaded = profiles.load_profiles()
    exact = [p for p in loaded if not p.get("generic") and profiles.profile_matches(p, probe)]
    probe["profile_error"] = profile_error
    probe["profiles"] = [p["id"] for p in exact]
    probe["auto_apply_profiles"] = [p["id"] for p in exact if profiles.build_matches(p, probe)]
    reference = [p["id"] for p in loaded if p.get("generic") and profiles.profile_matches(p, probe)]
    reference += [p["id"] for p in exact if not profiles.build_matches(p, probe)]
    probe["reference_profiles"] = sorted(set(reference))
    if args.json:
        ui.print_json(probe)
        return 0
    print(f"Device ...... {probe['brand']} {probe['model']} ({probe['device']})")
    print(f"Manufacturer  {probe['manufacturer']}")
    print(f"Android ..... {probe['android']} (SDK {probe['sdk']})")
    print(f"Build ....... {probe['build']}")
    print(f"Fingerprint . {probe['fingerprint']}")
    print(f"Security .... {probe['security_patch'] or '?'}")
    print(f"Bootloader .. {probe['verified_boot'] or '?'} (locked={probe['flash_locked'] or '?'})")
    managed = probe["managed"]
    print(f"Managed ..... {'unknown (cannot read device policy)' if managed is None else ('yes' if managed else 'no')}")
    users = probe.get("users")
    print(f"Users ....... {users if users is not None else 'unknown (cannot read pm list users)'}")
    print(f"Telephony ... {'yes' if probe['telephony'] else 'no'}")
    print(f"Battery ..... {probe['battery'].get('level', '?')}%")
    print(f"Profiles .... {', '.join(probe['profiles']) if probe['profiles'] else 'none exact'}")
    print(
        "Auto-apply .. "
        + (", ".join(probe["auto_apply_profiles"]) if probe["auto_apply_profiles"] else "none (use plan + disable)")
    )
    if probe["reference_profiles"]:
        print(f"Reference ... {', '.join(probe['reference_profiles'])} (not auto-applicable)")
    if probe["is_tv"]:
        print("WARNING: Android TV/box. Use https://cleanyour.tv instead.")
    if managed is None:
        print("WARNING: cannot read device policy. Do not change packages until it reads cleanly.")
    elif managed:
        print("WARNING: managed phone (device/profile owner). Stop.")
    if users is None:
        print("WARNING: cannot read `pm list users`. Do not change packages while it is unknown.")
    elif users > 1:
        print("WARNING: more than one Android user (work profile/guest). Stop and ask.")
    if profile_error:
        print(f"WARNING: profile error: {profile_error}")
    return 0


def cmd_backup(args: argparse.Namespace) -> int:
    serial = adb.pick_serial(args.serial)
    probe = adb.probe_device(serial)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = adb.BACKUP_DIR / f"{stamp}_{adb.slug(probe['brand'] + '-' + probe['model'])}"
    folder.mkdir(parents=True, exist_ok=True)

    commands = {
        "packages.txt": "pm list packages -f",
        "disabled.txt": "pm list packages -d",
        "enabled.txt": "pm list packages -e",
        "system.txt": "pm list packages -s",
        "user.txt": "pm list packages -3",
        "getprop.txt": "getprop",
        "settings-global.txt": "settings list global",
        "settings-secure.txt": "settings list secure",
        "settings-system.txt": "settings list system",
        "role-dialer.txt": "cmd role get-role-holders android.app.role.DIALER",
        "role-sms.txt": "cmd role get-role-holders android.app.role.SMS",
        "role-home.txt": "cmd role get-role-holders android.app.role.HOME",
        "role-emergency.txt": "cmd role get-role-holders android.app.role.EMERGENCY",
        "ime.txt": "ime list -s",
        "home.txt": "cmd package query-activities -a android.intent.action.MAIN -c android.intent.category.HOME",
        "device-policy.txt": "dumpsys device_policy",
        "battery.txt": "dumpsys battery",
        "users.txt": "pm list users",
    }
    for name, command in commands.items():
        try:
            result = adb.adb_run(["shell", command], serial=serial)
            text = result.stdout
            if result.stderr.strip():
                text += "\n# stderr:\n" + result.stderr
        except adb.AdbError as exc:
            text = f"# ERROR: {exc}\n"
        if name == "getprop.txt":
            text = adb.redact_getprop(text)
        (folder / name).write_text(text, encoding="utf-8", errors="replace")

    enabled = adb.package_set(serial, "-e")
    disabled = adb.package_set(serial, "-d")
    system = adb.package_set(serial, "-s")
    user = adb.package_set(serial, "-3")
    try:
        holders, roles_supported = adb.role_holders(serial)
    except adb.AdbError:
        holders, roles_supported = {}, False
    meta = {
        "timestamp": stamp,
        "serial": serial,
        "probe": probe,
        "enabled": sorted(enabled),
        "disabled": sorted(disabled),
        "system": sorted(system),
        "user": sorted(user),
        "roles": holders,
        "roles_supported": roles_supported,
        "ime": adb.default_ime(serial),
        "home": adb.home_activities(serial),
        "managed": probe["managed"],
    }
    adb.write_json(folder / "meta.json", meta)

    print(f"Backup written to {folder}")
    print(f"Packages: {len(enabled)} enabled, {len(disabled)} already disabled, {len(system)} system, {len(user)} user")
    if probe["managed"] is None:
        ui.warn("cannot read device policy: do not change packages until it reads cleanly")
    elif probe["managed"]:
        ui.warn("managed phone: do not change packages until the device/profile owner is removed")
    if probe.get("users") is None:
        ui.warn("cannot read `pm list users`: do not change packages while it is unknown")
    elif probe["users"] > 1:
        ui.warn("more than one Android user (work profile/guest): stop and ask before changing packages")
    if probe["is_tv"]:
        ui.warn("Android TV/box: use cleanyour.tv instead of this skill")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    serial = adb.pick_serial(args.serial)
    all_packages = adb.package_set(serial)
    enabled = adb.package_set(serial, "-e")
    disabled = adb.package_set(serial, "-d")
    system = adb.package_set(serial, "-s")
    user = adb.package_set(serial, "-3")
    if args.state == "enabled":
        selected = enabled
    elif args.state == "disabled":
        selected = disabled
    elif args.state == "system":
        selected = system
    elif args.state == "user":
        selected = user
    else:
        selected = all_packages

    rows = []
    for package in sorted(selected):
        flags = []
        if package in system:
            flags.append("system")
        if package in user:
            flags.append("user")
        if package in disabled:
            flags.append("disabled")
        rows.append({"package": package, "flags": flags, "protected": protected.is_protected(package)})

    if args.json:
        ui.print_json(rows)
        return 0
    for row in rows:
        flags = (" [" + ",".join(row["flags"]) + "]") if row["flags"] else ""
        mark = "!" if row["protected"] else " "
        print(f"{mark} {row['package']}{flags}")
    return 0


def cmd_roles(args: argparse.Namespace) -> int:
    serial = adb.pick_serial(args.serial)
    holders, supported = adb.role_holders(serial)
    ime = adb.default_ime(serial)
    home = adb.home_activities(serial)
    data = {
        "roles": holders,
        "roles_supported": supported,
        "ime": ime,
        "home_activities": home,
    }
    if args.json:
        ui.print_json(data)
        return 0
    print("Role holders" + ("" if supported else " (fallback; `cmd role` unavailable)"))
    for role in adb.ROLES:
        values = holders.get(role, [])
        print(f"  {role:<10} {', '.join(values) if values else '(none)'}")
    print(f"  {'KEYBOARD':<10} {ime or '(none)'}")
    print("HOME activities:")
    for component in home:
        print(f"  {component}")
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    try:
        profile = profiles.load_profile(args.profile)
    except KeyError as exc:
        ui.die(str(exc.args[0]) if exc.args else str(exc))
    errors = profiles.validate_profile(profile)
    if errors:
        ui.die("invalid profile:\n  " + "\n  ".join(errors))
    serial = adb.pick_serial(args.serial)
    probe = adb.probe_device(serial)
    matches = profiles.profile_matches(profile, probe)
    enabled = adb.package_set(serial, "-e")
    disabled = adb.package_set(serial, "-d")
    holders, ime = guard_roles(serial, probe)
    rows = profiles.classify(profile, enabled, disabled, holders, ime)
    auto = profiles.build_matches(profile, probe)

    if args.json:
        ui.print_json(
            {
                "profile": {k: v for k, v in profile.items() if k != "_path"},
                "match": matches,
                "auto_apply": auto,
                "rows": rows,
            }
        )
        return 0

    print(f"Profile: {profile.get('id')} ({profile.get('brand')} {profile.get('marketing_name') or profile.get('model')})")
    print(f"Phone:   {probe['brand']} {probe['model']} ({probe['device']}), Android {probe['android']}")
    if auto:
        auto_reason = "yes"
    elif profile.get("auto_apply") is False:
        auto_reason = "no - family/reference profile"
    else:
        auto_reason = "no - build not tested (use disable one by one after review)"
    print(f"Match:   {'yes' if matches else 'NO - this profile is for another model/firmware'}")
    print(f"Auto-apply: {auto_reason}")
    print("")
    for row in rows:
        print(f"{row['action']:<8} {row['package']}")
        if row.get("why"):
            print(f"         why: {row['why']}")
        if row.get("breaks"):
            print(f"         breaks: {row['breaks']}")
        if row.get("reason"):
            print(f"         note: {row['reason']}")
    if not matches:
        print("")
        print("WARNING: do not apply this profile to this phone. Use it only as a reference.")
    return 0


def cmd_apply(args: argparse.Namespace) -> int:
    try:
        profile = profiles.load_profile(args.profile)
    except KeyError as exc:
        ui.die(str(exc.args[0]) if exc.args else str(exc))
    errors = profiles.validate_profile(profile)
    if errors:
        ui.die("invalid profile:\n  " + "\n  ".join(errors))
    if profile.get("generic"):
        ui.die("a generic profile cannot be applied automatically. Use `plan` and `disable` after asking.")
    if profile.get("auto_apply") is False:
        ui.die(
            "this is a family/reference profile and is not auto-applicable. Run `plan`, review every "
            "row, then use `disable` one package at a time."
        )
    if args.batch_size < 1:
        ui.die("--batch-size must be at least 1")
    if args.batch_size > 5:
        ui.die("--batch-size cannot exceed 5: verify the phone between batches")

    serial = adb.pick_serial(args.serial)
    probe = guard_writable(serial)
    if not profiles.profile_matches(profile, probe):
        ui.die(f"profile {profile.get('id')} does not match this phone ({probe['brand']} {probe['model']})")
    if not profiles.build_matches(profile, probe):
        tested = ", ".join(
            sorted({str(entry.get("build", "")) for entry in profile.get("tested", []) if entry.get("build")})
        )
        ui.die(
            f"profile {profile.get('id')} was tested on build(s) {tested or '(none)'}; this phone is "
            f"{probe.get('build') or '(unknown)'} ({probe.get('fingerprint') or 'no fingerprint'}). "
            "Auto-apply is refused after an OTA. Run `plan`, review the diff, then use `disable` one at a time."
        )
    folder, meta = require_backup(serial, probe)
    enabled = adb.package_set(serial, "-e")
    disabled = adb.package_set(serial, "-d")
    holders, ime = guard_roles(serial, probe)
    rows = profiles.classify(profile, enabled, disabled, holders, ime)
    to_apply = [row for row in rows if row["action"] == "DISABLE"]
    never = profiles.never_packages(profile)

    if not to_apply:
        print("Nothing to disable: every 'disable' entry is blocked, missing or already disabled.")
        return 0

    print(f"Profile {profile.get('id')} on {probe['brand']} {probe['model']}; backup {folder}")
    for row in to_apply:
        print(f"  {'WOULD DISABLE' if not args.yes else 'DISABLE'} {row['package']}")
    if not args.yes:
        print("")
        print("Dry run. Re-run with --yes to apply, or use `disable <package>` one at a time.")
        return 0

    applied = load_applied(serial)
    batch_size = args.batch_size
    for start in range(0, len(to_apply), batch_size):
        batch = to_apply[start : start + batch_size]
        # Roles can move between batches; re-read them before every batch.
        holders, ime = guard_roles(serial, probe)
        done: List[str] = []
        failed = False
        try:
            for row in batch:
                disable_one(
                    serial,
                    row["package"],
                    meta,
                    applied,
                    why=row.get("why", ""),
                    profile=profile.get("id"),
                    holders=holders,
                    ime=ime,
                    never=never,
                    done=done,
                )
            result = checks.verify_checks(serial)
            checks.print_checks(result)
            if checks.has_failures(result):
                failed = True
        except BaseException:
            rollback_batch(serial, done, applied)
            raise
        if failed:
            rollback_batch(serial, done, applied)
            ui.die("verification failed after batch; the batch was re-enabled. Stop and investigate.")
    print("")
    print(f"Done. {len(to_apply)} packages disabled. Undo: python tools/phone.py restore")
    return 0


def cmd_disable(args: argparse.Namespace) -> int:
    if len(args.packages) > 5:
        ui.die("at most 5 packages per batch. Run `verify` between batches.")
    serial = adb.pick_serial(args.serial)
    probe = guard_writable(serial)
    holders, ime = guard_roles(serial, probe)
    _, meta = require_backup(serial, probe)
    never = profiles.never_for_phone(probe)
    applied = load_applied(serial)
    batch = list(dict.fromkeys(args.packages))
    done: List[str] = []
    failed = False
    try:
        for package in batch:
            disable_one(
                serial,
                package,
                meta,
                applied,
                holders=holders,
                ime=ime,
                never=never,
                done=done,
            )
        result = checks.verify_checks(serial)
        checks.print_checks(result)
        if checks.has_failures(result):
            failed = True
    except BaseException:
        rollback_batch(serial, done, applied)
        raise
    if failed:
        rollback_batch(serial, done, applied)
        ui.die("verification failed after the batch; the batch was re-enabled. Stop and investigate.")
    return 0


def cmd_enable(args: argparse.Namespace) -> int:
    serial = adb.pick_serial(args.serial)
    applied = load_applied(serial)
    for package in args.packages:
        enable_one(serial, package, applied)
    return 0


def cmd_restore(args: argparse.Namespace) -> int:
    serial = adb.pick_serial(args.serial)
    applied = load_applied(serial)
    packages = sorted(applied.get("packages", {}))
    if not packages:
        print("Nothing to restore: no package was disabled by this tool.")
        extra.restore_dns(serial)
        return 0
    disabled = adb.package_set(serial, "-d")
    for package in packages:
        if package not in disabled:
            print(f"SKIP {package}: not disabled")
            continue
        if args.dry_run:
            print(f"WOULD ENABLE {package}")
            continue
        enable_one(serial, package, applied, record=False)
    if args.dry_run:
        print("Dry run. Nothing changed.")
        return 0

    still_disabled = sorted(package for package in packages if package in adb.package_set(serial, "-d"))
    if still_disabled:
        ui.die(
            "restore is incomplete; still disabled: "
            + ", ".join(still_disabled)
            + ". The record was kept. Re-run restore or enable them manually, then verify."
        )
    extra.restore_dns(serial)
    applied["packages"] = {}
    applied["restored_at"] = adb.now()
    save_applied(serial, applied)
    print("Restore complete. Run `python tools/phone.py verify` and test calls, SMS, keyboard and Home.")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    serial = adb.pick_serial(args.serial)
    result = checks.verify_checks(serial)
    if args.json:
        ui.print_json(result)
    else:
        checks.print_checks(result)
    return 1 if checks.has_failures(result) else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="phone.py",
        description="CleanYourPhone: safe Android debloat over ADB. Disable, never uninstall.",
    )
    parser.add_argument("--serial", help="ADB serial to use when more than one device is connected")
    parser.add_argument("--json", action="store_true", help="machine-readable output where supported")
    parser.add_argument("--version", action="version", version="CleanYourPhone 0.1.0")

    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="check adb, device, backup and profile match")
    doctor.set_defaults(func=cmd_doctor)

    probe = sub.add_parser("probe", help="print model, Android version, fingerprint and state")
    probe.set_defaults(func=cmd_probe)

    backup = sub.add_parser("backup", help="save package lists, settings, roles and getprop")
    backup.set_defaults(func=cmd_backup)

    listing = sub.add_parser("list", help="list packages and their state")
    listing.add_argument("--state", choices=["all", "enabled", "disabled", "system", "user"], default="all")
    listing.set_defaults(func=cmd_list)

    roles = sub.add_parser("roles", help="show dialer/SMS/Home/IME role holders")
    roles.set_defaults(func=cmd_roles)

    plan = sub.add_parser("plan", help="show a profile's plan for this phone")
    plan.add_argument("--profile", required=True, help="profile id or path")
    plan.add_argument("--dry-run", action="store_true", help="accepted for symmetry; plan never changes anything")
    plan.set_defaults(func=cmd_plan)

    apply_cmd = sub.add_parser("apply", help="apply a matching profile's disable list")
    apply_cmd.add_argument("--profile", required=True, help="profile id or path")
    apply_cmd.add_argument("--yes", action="store_true", help="actually change the phone")
    apply_cmd.add_argument("--batch-size", type=int, default=5, help="packages per batch (default 5)")
    apply_cmd.set_defaults(func=cmd_apply)

    disable = sub.add_parser("disable", help="disable one or more packages (checks protected list and roles)")
    disable.add_argument("packages", nargs="+")
    disable.set_defaults(func=cmd_disable)

    enable = sub.add_parser("enable", help="re-enable one or more packages")
    enable.add_argument("packages", nargs="+")
    enable.set_defaults(func=cmd_enable)

    restore = sub.add_parser("restore", help="re-enable everything this tool disabled")
    restore.add_argument("--dry-run", action="store_true")
    restore.set_defaults(func=cmd_restore)

    verify = sub.add_parser("verify", help="check dialer, SMS, Home, keyboard, Play and protected packages")
    verify.set_defaults(func=cmd_verify)

    extra.add_subparsers(sub)
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args) or 0
    except adb.AdbError as exc:
        ui.die(str(exc))
    except adb.StateError as exc:
        ui.die(str(exc))
    except (KeyError, ValueError) as exc:
        ui.die(str(exc))
    except OSError as exc:
        ui.die(f"file error: {exc}")
    except KeyboardInterrupt:
        print("\ninterrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
