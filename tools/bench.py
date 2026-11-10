"""Local before/after measurements for CleanYourPhone."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

try:  # imported as tools.bench
    from . import adb
except ImportError:  # run from tools/
    import adb  # type: ignore

BENCH_DIR = Path(os.environ.get("CLEANYOURPHONE_BENCH", adb.STATE_DIR / "bench"))

METRICS = [
    ("ram_available_mb", "RAM available (MB)"),
    ("swap_used_mb", "Swap used (MB)"),
    ("processes", "Processes"),
    ("packages_installed", "Packages installed"),
    ("packages_enabled", "Packages enabled"),
    ("packages_disabled", "Packages disabled"),
    ("packages_system", "System packages"),
    ("packages_user", "User packages"),
    ("animation_window", "Window animation scale"),
    ("animation_transition", "Transition animation scale"),
    ("animation_duration", "Animator duration scale"),
    ("peak_refresh_rate", "Peak refresh rate (Hz)"),
]


def _number(text: str, default: float = 0.0) -> float:
    try:
        return float(text.strip())
    except (TypeError, ValueError):
        return default


def _setting(serial: str, namespace: str, key: str) -> str:
    try:
        return adb.shell(f"settings get {namespace} {key}", serial=serial).strip()
    except adb.AdbError:
        return ""


def _meminfo(serial: str) -> Dict[str, int]:
    try:
        text = adb.shell("cat /proc/meminfo", serial=serial)
    except adb.AdbError:
        return {}
    values: Dict[str, int] = {}
    for line in text.splitlines():
        match = re.match(r"([A-Za-z_]+):\s+(\d+)", line)
        if match:
            values[match.group(1)] = int(match.group(2))
    return values


def _process_count(serial: str) -> int | None:
    try:
        lines = adb.shell("ps -A -o NAME", serial=serial).splitlines()
    except adb.AdbError:
        return None
    return max(0, len([line for line in lines if line.strip()]) - 1)


def _package_count(serial: str, flag: str) -> int | None:
    try:
        return len(adb.package_set(serial, flag))
    except adb.AdbError:
        return None


def measure(serial: str) -> Dict[str, Any]:
    """Capture local, comparable metrics. Never stores a serial or fingerprint."""
    probe = adb.probe_device(serial)
    mem = _meminfo(serial)
    dns = adb.dns_status(serial)

    data: Dict[str, Any] = {
        "timestamp": adb.now(),
        "model": f"{probe.get('brand', '')} {probe.get('model', '')}".strip(),
        "android": probe.get("android", ""),
        "build": probe.get("build", ""),
        "ram_available_mb": (mem.get("MemAvailable", 0) // 1024) if "MemAvailable" in mem else None,
        "swap_used_mb": (
            max(0, mem.get("SwapTotal", 0) - mem.get("SwapFree", 0)) // 1024
            if "SwapTotal" in mem and "SwapFree" in mem
            else None
        ),
        "processes": _process_count(serial),
        "packages_installed": _package_count(serial, ""),
        "packages_enabled": _package_count(serial, "-e"),
        "packages_disabled": _package_count(serial, "-d"),
        "packages_system": _package_count(serial, "-s"),
        "packages_user": _package_count(serial, "-3"),
        "animation_window": _number(_setting(serial, "global", "window_animation_scale"), 1.0),
        "animation_transition": _number(_setting(serial, "global", "transition_animation_scale"), 1.0),
        "animation_duration": _number(_setting(serial, "global", "animator_duration_scale"), 1.0),
        "peak_refresh_rate": _number(_setting(serial, "system", "peak_refresh_rate"), 60.0),
        "private_dns_mode": dns.get("mode", ""),
        "private_dns_specifier": dns.get("specifier", ""),
        "battery_saver": _setting(serial, "global", "low_power") == "1",
    }
    return data


def save(data: Dict[str, Any], label: str) -> Path:
    """Write a snapshot under BENCH_DIR and return its path."""
    safe = re.sub(r"[^A-Za-z0-9_-]+", "-", (label or "snapshot").strip()).strip("-") or "snapshot"
    BENCH_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = BENCH_DIR / f"{stamp}_{safe}.json"
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


REQUIRED_KEYS = ("timestamp", "model", "android", "build", "ram_available_mb", "packages_enabled")


def load(path: Path) -> Dict[str, Any]:
    """Read a snapshot, rejecting malformed JSON or a non-snapshot object."""
    path = Path(path).expanduser()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read bench snapshot {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"bench snapshot {path} is not a JSON object")
    missing = [key for key in REQUIRED_KEYS if key not in data]
    if missing:
        raise ValueError(f"bench snapshot {path} is missing: {', '.join(missing)}")
    return data


def compare(before: Dict[str, Any], after: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return metric rows with absolute and percentage deltas."""
    rows: List[Dict[str, Any]] = []
    for key, label in METRICS:
        old = before.get(key)
        new = after.get(key)
        if not isinstance(old, (int, float)) or not isinstance(new, (int, float)):
            continue
        delta = new - old
        pct = round(delta * 100.0 / old, 1) if old else None
        rows.append(
            {
                "metric": key,
                "label": label,
                "before": old,
                "after": new,
                "delta": delta,
                "pct": pct,
            }
        )
    return rows


def write_markdown(
    before: Dict[str, Any],
    after: Dict[str, Any],
    rows: List[Dict[str, Any]],
    path: Path,
) -> Path:
    """Write a local comparison with an explicit no-causality caveat."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# CleanYourPhone before/after",
        "",
        f"- Before device: {before.get('model', '?')} / Android {before.get('android', '?')} / `{before.get('build', '?')}`",
        f"- After device: {after.get('model', '?')} / Android {after.get('android', '?')} / `{after.get('build', '?')}`",
        f"- Before: `{before.get('timestamp', '?')}`",
        f"- After: `{after.get('timestamp', '?')}`",
        f"- Battery Saver: {before.get('battery_saver', '?')} -> {after.get('battery_saver', '?')}",
        f"- Private DNS: {before.get('private_dns_mode', '?')} `{before.get('private_dns_specifier', '')}` -> {after.get('private_dns_mode', '?')} `{after.get('private_dns_specifier', '')}`",
        "",
    ]
    if (before.get("model"), before.get("android"), before.get("build")) != (
        after.get("model"),
        after.get("android"),
        after.get("build"),
    ):
        lines += [
            "> **Warning:** these snapshots are from different models, Android versions or builds.",
            "> Do not compare them as a before/after.",
            "",
        ]
    if before.get("battery_saver") != after.get("battery_saver"):
        lines += [
            "> **Warning:** Battery Saver changed between snapshots; compare again under the same conditions.",
            "",
        ]
    lines += [
        "| Metric | Before | After | Change |",
        "|---|---:|---:|---:|",
    ]
    for row in rows:
        pct = f"{row['pct']:+.1f}%" if row["pct"] is not None else "n/a"
        lines.append(f"| {row['label']} | {row['before']} | {row['after']} | {row['delta']:+g} ({pct}) |")
    lines += [
        "",
        "Measured on this phone with the same conditions as far as possible. Values are approximate",
        "and not causal: background apps, charging, battery saver, refresh settings and time since boot",
        "change the result.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
