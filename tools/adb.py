"""ADB wrapper and parsers for CleanYourPhone. Stdlib only, no phone-side install."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
BACKUP_DIR = Path(os.environ.get("CLEANYOURPHONE_BACKUP", ROOT / "backup"))
STATE_DIR = Path(os.environ.get("CLEANYOURPHONE_STATE", Path.home() / ".cleanyourphone"))

ROLES = {
    "DIALER": "android.app.role.DIALER",
    "SMS": "android.app.role.SMS",
    "HOME": "android.app.role.HOME",
    "ASSISTANT": "android.app.role.ASSISTANT",
    "EMERGENCY": "android.app.role.EMERGENCY",
}

PROPS = [
    "ro.product.brand",
    "ro.product.manufacturer",
    "ro.product.model",
    "ro.product.device",
    "ro.product.name",
    "ro.build.version.release",
    "ro.build.version.sdk",
    "ro.build.version.security_patch",
    "ro.build.fingerprint",
    "ro.build.display.id",
    "ro.build.characteristics",
    "ro.boot.verifiedbootstate",
    "ro.boot.flash.locked",
    "ro.debuggable",
]


class AdbError(RuntimeError):
    """A problem before or while talking to the phone."""


class StateError(RuntimeError):
    """A local state file is corrupt or unreadable. Never guess: stop and keep the evidence."""


PACKAGE_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*(\.[A-Za-z][A-Za-z0-9_]*)*$")
SENSITIVE_PROP_KEYS = ("serialno", "imei", "meid", "macaddr", "android_id")


def valid_package(package: str) -> bool:
    """True for a plausible Android package name.

    Package names are interpolated into `adb shell` commands, so this is a small security
    boundary as well as a typo check. It refuses spaces, semicolons, slashes and shell syntax.
    """
    return bool(PACKAGE_RE.match(package))


def redact_getprop(text: str) -> str:
    """Remove serial numbers, IMEIs and MAC addresses from a getprop dump.

    The backup is local and git-ignored, but it does not need these values to undo a debloat.
    """
    lines: List[str] = []
    for line in text.splitlines():
        match = re.match(r"^(\[[^\]]+\]):\s*\[.*\]\s*$", line)
        if match and any(key in match.group(1).lower() for key in SENSITIVE_PROP_KEYS):
            lines.append(f"{match.group(1)}: [redacted]")
        else:
            lines.append(line)
    return "\n".join(lines)


def find_adb() -> Optional[str]:
    """Find adb on PATH, in the usual SDK locations, or via the ADB environment variable."""
    env = os.environ.get("ADB")
    if env and Path(env).is_file():
        return env
    found = shutil.which("adb")
    if found:
        return found
    home = Path.home()
    candidates = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Android/Sdk/platform-tools/adb.exe",
        home / "AppData/Local/Android/Sdk/platform-tools/adb.exe",
        home / "Library/Android/sdk/platform-tools/adb",
        home / "Android/Sdk/platform-tools/adb",
        Path("/usr/bin/adb"),
        Path("/usr/local/bin/adb"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    return None


ADB = find_adb()


def adb_run(args: List[str], serial: Optional[str] = None, timeout: int = 120) -> subprocess.CompletedProcess:
    """Run one adb command and return the completed process."""
    if not ADB:
        raise AdbError(
            "adb not found. Install Android SDK Platform-Tools and add it to PATH, or set ADB to the "
            "full path of the adb executable."
        )
    command = [ADB]
    if serial:
        command += ["-s", serial]
    command += list(args)
    try:
        return subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except FileNotFoundError as exc:
        raise AdbError(f"adb not found at {ADB}: {exc}") from exc
    except subprocess.TimeoutExpired as exc:
        raise AdbError(f"adb timed out after {timeout}s: {' '.join(command)}") from exc


def shell(command: str, serial: Optional[str] = None, timeout: int = 120) -> str:
    """Run one shell command on the phone and return stdout, stripped."""
    result = adb_run(["shell", command], serial=serial, timeout=timeout)
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "").strip()
        raise AdbError(f"adb shell failed ({result.returncode}): {message or command}")
    return result.stdout.strip()


def devices() -> List[Dict[str, str]]:
    """Parse `adb devices -l`."""
    result = adb_run(["devices", "-l"])
    if result.returncode != 0:
        raise AdbError((result.stderr or result.stdout or "adb devices failed").strip())
    found: List[Dict[str, str]] = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("List of devices") or line.startswith("*"):
            continue
        parts = line.split()
        if len(parts) >= 2:
            found.append({"serial": parts[0], "state": parts[1], "details": " ".join(parts[2:])})
    return found


def pick_serial(explicit: Optional[str] = None) -> str:
    """Pick the one connected phone, or fail with instructions."""
    serial = explicit or os.environ.get("ANDROID_SERIAL")
    found = devices()
    if serial:
        match = next((item for item in found if item["serial"] == serial), None)
        if not match:
            raise AdbError(f"device {serial} is not connected. Connected: {format_devices(found)}")
        if match["state"] != "device":
            raise AdbError(f"device {serial} is {match['state']}. Unlock the phone and accept the USB debugging prompt.")
        return serial
    if not found:
        raise AdbError(
            "no Android device found. Connect the phone by USB, enable Developer options > USB debugging, "
            "and accept the 'Allow USB debugging?' prompt."
        )
    if len(found) > 1:
        raise AdbError(f"more than one device. Pass --serial <serial>. Connected: {format_devices(found)}")
    only = found[0]
    if only["state"] != "device":
        raise AdbError(f"device {only['serial']} is {only['state']}. Unlock the phone and accept the USB debugging prompt.")
    return only["serial"]


def format_devices(found: List[Dict[str, str]]) -> str:
    if not found:
        return "(none)"
    return ", ".join(f"{item['serial']} ({item['state']})" for item in found)


def getprop(serial: str, key: str) -> str:
    return shell(f"getprop {key}", serial=serial).strip()


def parse_battery(text: str) -> Dict[str, Any]:
    def number(key: str) -> Optional[int]:
        match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*(-?\d+)", text)
        return int(match.group(1)) if match else None

    return {
        "level": number("level"),
        "status": number("status"),
        "health": number("health"),
        "temperature": number("temperature"),
        "voltage": number("voltage"),
    }


def _owner_lines(text: str) -> List[str]:
    """Collect lines inside `Device Owner(s):` / `Profile Owner(s):` dumpsys sections."""
    lines = text.splitlines()
    selected: List[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        low = stripped.lower()
        heading = (
            low.startswith("device owner:")
            or low.startswith("profile owner:")
            or low.startswith("device owners:")
            or low.startswith("profile owners:")
            or low.startswith("mdeviceowner=")
            or low.startswith("deviceowner=")
            or low.startswith("mprofileowner=")
            or low.startswith("profileowner=")
        )
        if not heading:
            index += 1
            continue

        selected.append(line)
        inline = "admin=" in low or "component=" in low or "componentinfo{" in low
        base = len(line) - len(line.lstrip())
        index += 1
        if inline:
            continue
        while index < len(lines):
            child = lines[index]
            child_stripped = child.strip()
            if not child_stripped:
                index += 1
                continue
            indent = len(child) - len(child.lstrip())
            if indent <= base and child_stripped.endswith(":"):
                break
            selected.append(child)
            index += 1
    return selected


def is_managed(serial: str) -> Optional[bool]:
    """True/False when device policy can be read; None when it cannot be determined.

    Fail closed: the caller must stop on None. A heading such as "Device Owner Type: -1" is not
    an owner; only a real ComponentInfo/admin line inside an owner section counts.
    """
    try:
        text = shell("dumpsys device_policy", serial=serial)
    except AdbError:
        return None
    if not text.strip():
        return None
    low_text = text.lower()
    if any(
        marker in low_text
        for marker in ("permission denial", "can't find service", "service not found", "unknown command", "error:")
    ):
        return None
    for line in _owner_lines(text):
        low = line.lower()
        if "null" in low or "none" in low:
            continue
        match = re.search(r"ComponentInfo\{([A-Za-z][A-Za-z0-9_.]+)/", line, re.I)
        if not match:
            match = re.search(r"(?:admin|component)\s*=\s*([A-Za-z][A-Za-z0-9_.]+)/", line, re.I)
        if match and match.group(1).lower() not in ("null", "none"):
            return True
    return False


def user_count(serial: str) -> Optional[int]:
    """Number of Android users, including work profiles and guests; None if unreadable."""
    out = _shell_or_empty("pm list users", serial)
    if not out.strip() or _pm_error(out):
        return None
    count = len(re.findall(r"UserInfo\{", out))
    return count if count >= 1 else None


def probe_device(serial: str) -> Dict[str, Any]:
    props = {key: getprop(serial, key) for key in PROPS}
    battery = parse_battery(shell("dumpsys battery", serial=serial))
    characteristics = props.get("ro.build.characteristics", "") or ""
    sdk = 0
    try:
        sdk = int(props.get("ro.build.version.sdk") or 0)
    except ValueError:
        sdk = 0
    return {
        "serial": serial,
        "brand": props.get("ro.product.brand", ""),
        "manufacturer": props.get("ro.product.manufacturer", ""),
        "model": props.get("ro.product.model", ""),
        "device": props.get("ro.product.device", ""),
        "product": props.get("ro.product.name", ""),
        "android": props.get("ro.build.version.release", ""),
        "sdk": sdk,
        "security_patch": props.get("ro.build.version.security_patch", ""),
        "fingerprint": props.get("ro.build.fingerprint", ""),
        "build": props.get("ro.build.display.id", ""),
        "characteristics": characteristics,
        "is_tv": "tv" in characteristics.lower() or "box" in characteristics.lower(),
        "managed": is_managed(serial),
        "users": user_count(serial),
        "telephony": package_installed(serial, "com.android.phone"),
        "battery": battery,
        "flash_locked": props.get("ro.boot.flash.locked", ""),
        "verified_boot": props.get("ro.boot.verifiedbootstate", ""),
        "debuggable": props.get("ro.debuggable", ""),
    }


def _shell_or_empty(command: str, serial: str) -> str:
    """Run a read-only shell command, returning '' instead of aborting a backup or probe."""
    try:
        return shell(command, serial=serial)
    except AdbError:
        return ""


def _cmd_role_missing(text: str) -> bool:
    """True when the output says the `cmd role` interface does not exist on this build."""
    low = text.lower()
    return any(
        marker in low
        for marker in ("unknown command", "unknown role", "cmd: not found", "cmd not found", "does not exist")
    )


def resolve_activity_package(
    serial: str,
    action: str,
    category: str = "android.intent.category.DEFAULT",
    data: str = "",
) -> Optional[str]:
    """Resolve the default package for an intent, using `cmd package resolve-activity`."""
    command = f"cmd package resolve-activity --brief -a {action} -c {category}"
    if data:
        command += f" -d {data}"
    out = _shell_or_empty(command, serial)
    for line in reversed(out.splitlines()):
        line = line.strip()
        if "/" not in line or line.startswith("priority="):
            continue
        package = line.split("/")[0].strip()
        if valid_package(package):
            return package
    return None


def role_holders(serial: str) -> Tuple[Dict[str, List[str]], bool]:
    """Return role -> package list and whether `cmd role` worked (Android 10+).

    A read failure raises AdbError. Only a genuinely missing `cmd role` interface (older Android)
    falls back to the legacy settings, and the caller must still verify that every critical role
    was found and is enabled before changing a package.
    """
    holders: Dict[str, List[str]] = {}
    supported = True
    for name, role in ROLES.items():
        result = adb_run(["shell", f"cmd role get-role-holders {role}"], serial=serial)
        out = (result.stdout or "").strip()
        err = (result.stderr or "").strip()
        combined = f"{out}\n{err}".strip()
        low = combined.lower()
        if _cmd_role_missing(combined):
            supported = False
            break
        if result.returncode != 0:
            raise AdbError(f"cannot read role {name}: {combined or 'no output'}")
        if any(
            marker in low
            for marker in ("error:", "exception", "permission denial", "not allowed", "can't find service", "service not found")
        ):
            raise AdbError(f"cannot read role {name}: {combined}")
        packages: List[str] = []
        for line in out.splitlines():
            line = line.strip()
            if not line or line.lower().startswith("error"):
                continue
            package = line.split("/")[0].strip()
            if package and not package.startswith("priority=") and valid_package(package):
                packages.append(package)
        holders[name] = sorted(set(packages))

    if not supported:
        holders = {}
        dialer = _shell_or_empty("settings get secure dialer_default_application", serial).strip()
        if not dialer or dialer == "null":
            dialer = resolve_activity_package(serial, "android.intent.action.DIAL") or ""
        if dialer and dialer != "null":
            holders["DIALER"] = [dialer]
        sms = _shell_or_empty("settings get secure sms_default_application", serial).strip()
        if not sms or sms == "null":
            sms = resolve_activity_package(serial, "android.intent.action.SENDTO", data="sms:") or ""
        if sms and sms != "null":
            holders["SMS"] = [sms]
        home = default_home_package(serial)
        if home:
            holders["HOME"] = [home]
    return holders, supported


def default_home_package(serial: str) -> Optional[str]:
    out = _shell_or_empty(
        "cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.HOME",
        serial,
    )
    for line in reversed(out.splitlines()):
        line = line.strip()
        if "/" in line and not line.startswith("priority="):
            return line.split("/")[0].strip()
    focused = _shell_or_empty("dumpsys activity activities", serial)
    match = re.search(r"mFocusedApp=.*?\s([A-Za-z0-9_.]+)/[A-Za-z0-9_.$]+", focused)
    return match.group(1) if match else None


def home_activities(serial: str) -> List[str]:
    out = _shell_or_empty(
        "cmd package query-activities -a android.intent.action.MAIN -c android.intent.category.HOME",
        serial,
    )
    components = set()
    for line in out.splitlines():
        match = re.search(r"([A-Za-z0-9_.]+)/([A-Za-z0-9_.$]+)", line)
        if match:
            components.add(f"{match.group(1)}/{match.group(2)}")
    return sorted(components)


def read_default_ime(serial: str) -> str:
    """Read the current keyboard, raising AdbError if the setting cannot be read."""
    out = shell("settings get secure default_input_method", serial=serial).strip()
    if not out or out == "null":
        return ""
    return out.split("/")[0].strip()


def default_ime(serial: str) -> str:
    """Best-effort keyboard read for backups; security-sensitive callers use read_default_ime."""
    try:
        return read_default_ime(serial)
    except AdbError:
        return ""


def parse_packages(text: str) -> List[str]:
    packages: List[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("package:"):
            continue
        rest = line[len("package:") :]
        if "=" in rest:
            rest = rest.rsplit("=", 1)[1]
        package = rest.strip()
        if package:
            packages.append(package)
    return packages


def _pm_error(text: str) -> str:
    """Return an error line from `pm` output, or ''. Prevents an empty/error list being read as 'none'."""
    for line in text.splitlines():
        stripped = line.strip()
        low = stripped.lower()
        if (
            low.startswith("error")
            or "permission denial" in low
            or "can't find service" in low
            or "service not found" in low
        ):
            return stripped
    return ""


def package_set(serial: str, flag: str = "") -> set:
    command = "pm list packages" + (f" {flag}" if flag else "")
    text = shell(command, serial=serial)
    error = _pm_error(text)
    if error:
        raise AdbError(f"cannot list packages ({command}): {error}")
    return set(parse_packages(text))


def package_installed(serial: str, package: str) -> bool:
    out = shell(f"pm list packages {package}", serial=serial)
    error = _pm_error(out)
    if error:
        raise AdbError(f"cannot query package {package}: {error}")
    return f"package:{package}" in {line.strip() for line in out.splitlines()}


def package_disabled(serial: str, package: str) -> bool:
    return package in package_set(serial, "-d")


def package_enabled(serial: str, package: str) -> bool:
    return package in package_set(serial, "-e")


def dns_status(serial: str) -> Dict[str, str]:
    mode = shell("settings get global private_dns_mode", serial=serial).strip()
    specifier = shell("settings get global private_dns_specifier", serial=serial).strip()
    for value in (mode, specifier):
        low = value.lower()
        if low.startswith("error") or "permission denial" in low or "can't find service" in low:
            raise AdbError(f"cannot read Private DNS state: {value}")
    if not mode or mode == "null":
        mode = "opportunistic"
    if mode not in ("off", "opportunistic", "hostname"):
        raise AdbError(f"unexpected Private DNS mode: {mode!r}")
    if specifier == "null":
        specifier = ""
    return {"mode": mode, "specifier": specifier}


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def read_json(path: Path, default: Any, strict: bool = False) -> Any:
    """Read JSON. With strict=True, a corrupt or unreadable existing file raises StateError.

    State files must never be silently treated as empty: that would make `restore` forget what the
    tool disabled and leave the phone in a half-cleaned state.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return default
    except OSError as exc:
        if strict:
            raise StateError(f"cannot read state file {path}: {exc}") from exc
        return default
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        if strict:
            raise StateError(
                f"state file {path} is corrupt: {exc}. Move it aside before continuing; do not delete it."
            ) from exc
        return default


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


APPLIED_PATH = STATE_DIR / "applied.json"
CHANGES_PATH = STATE_DIR / "changes.json"


def _load_devices(path: Path) -> Dict[str, Any]:
    data = read_json(path, {}, strict=True)
    if not isinstance(data, dict):
        raise StateError(f"state file {path} is corrupt: expected a JSON object")
    if not data:
        return {}
    if "devices" not in data:
        raise StateError(f"state file {path} uses an unsupported format; move it aside, do not delete it")
    devices = data.get("devices")
    if not isinstance(devices, dict):
        raise StateError(f"state file {path} is corrupt: 'devices' must be an object")
    return devices


def load_applied(serial: str) -> Dict[str, Any]:
    """Changes this tool made on one phone. State is keyed by serial, never shared."""
    device = _load_devices(APPLIED_PATH).get(serial)
    if not isinstance(device, dict):
        return {"packages": {}}
    packages = device.get("packages", {})
    if not isinstance(packages, dict):
        raise StateError(f"state file {APPLIED_PATH} is corrupt: packages for {serial} must be an object")
    device["packages"] = packages
    return device


def save_applied(serial: str, data: Dict[str, Any]) -> None:
    devices = _load_devices(APPLIED_PATH)
    devices[serial] = data
    write_json(APPLIED_PATH, {"devices": devices})


def load_changes(serial: str) -> Dict[str, Any]:
    """Settings (currently Private DNS) this tool changed on one phone."""
    device = _load_devices(CHANGES_PATH).get(serial)
    if device is None:
        return {}
    if not isinstance(device, dict):
        raise StateError(f"state file {CHANGES_PATH} is corrupt: changes for {serial} must be an object")
    return device


def save_changes(serial: str, data: Dict[str, Any]) -> None:
    devices = _load_devices(CHANGES_PATH)
    devices[serial] = data
    write_json(CHANGES_PATH, {"devices": devices})


def latest_backup(serial: Optional[str] = None) -> Tuple[Optional[Path], Optional[Dict[str, Any]]]:
    """Return (folder, meta) for the newest backup, optionally for one serial."""
    if not BACKUP_DIR.exists():
        return None, None
    candidates: List[Tuple[str, Path, Dict[str, Any]]] = []
    for meta_path in BACKUP_DIR.glob("*/meta.json"):
        meta = read_json(meta_path, None)
        if not isinstance(meta, dict):
            continue
        if serial and meta.get("serial") != serial:
            continue
        candidates.append((str(meta.get("timestamp", "")), meta_path.parent, meta))
    if not candidates:
        return None, None
    candidates.sort(key=lambda item: item[0])
    _, folder, meta = candidates[-1]
    return folder, meta


def slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-").lower()
    return cleaned or "phone"
