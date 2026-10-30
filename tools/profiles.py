"""Profile loading, matching, planning and validation for CleanYourPhone."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:  # imported as tools.profiles
    from . import adb, protected
except ImportError:  # run from tools/
    import adb  # type: ignore
    import protected  # type: ignore

ROOT = Path(__file__).resolve().parent.parent
PROFILES_DIR = ROOT / "profiles"

REQUIRED = [
    "id",
    "brand",
    "model",
    "android",
    "fingerprint_regex",
    "verification",
    "tested",
    "disable",
    "ask",
    "never",
    "notes",
]
ROLE_NAMES = ("DIALER", "SMS", "HOME", "EMERGENCY")
VERIFICATION_LEVELS = ("device", "documented", "reference")


def load_profiles(strict: bool = False) -> List[Dict[str, Any]]:
    """Load every profile JSON, skipping the schema.

    With strict=True (used by `phone.py validate`), a malformed file is an error instead of being
    silently ignored: a broken profile must not make the validation look clean.
    """
    if not PROFILES_DIR.exists():
        return []
    profiles: List[Dict[str, Any]] = []
    for path in sorted(PROFILES_DIR.glob("**/*.json")):
        if path.name == "schema.json":
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            if strict:
                raise ValueError(f"{path}: cannot read profile: {exc}") from exc
            continue
        if not isinstance(data, dict) or not data.get("id"):
            if strict:
                raise ValueError(f"{path}: profile must be a JSON object with an 'id'")
            continue
        data["_path"] = str(path)
        profiles.append(data)
    return profiles


def load_profile(ref: str) -> Dict[str, Any]:
    """Load a profile by id or by path."""
    path = Path(ref)
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise KeyError(f"cannot read profile {path}: {exc}") from exc
        if not isinstance(data, dict):
            raise KeyError(f"profile {path} must be a JSON object")
        data["_path"] = str(path)
        return data
    for profile in load_profiles():
        if profile.get("id") == ref:
            return profile
    available = ", ".join(sorted(p.get("id", "?") for p in load_profiles())) or "(none)"
    raise KeyError(f"profile not found: {ref}. Available: {available}")


def verification_level(profile: Dict[str, Any]) -> str:
    """Return the declared level, or the backward-compatible inferred level."""
    declared = str(profile.get("verification", "")).strip().lower()
    if declared in VERIFICATION_LEVELS:
        return declared
    if profile.get("generic") is True:
        return "reference"
    if profile.get("tested"):
        return "device"
    return "documented"


def profile_matches(profile: Dict[str, Any], probe: Dict[str, Any]) -> bool:
    """True when the profile's model/codename/fingerprint/Android version match the phone."""
    model = str(profile.get("model", "")).strip().lower()
    if model and model != "*":
        probe_model = str(probe.get("model", "")).strip().lower()
        if model != probe_model:
            return False
    codename = str(profile.get("codename", "")).strip().lower()
    if codename and codename != str(probe.get("device", "")).strip().lower():
        return False
    regex = str(profile.get("fingerprint_regex", "")).strip()
    if regex:
        fingerprint = str(probe.get("fingerprint", "")).strip()
        if not fingerprint:
            return False
        try:
            if not re.search(regex, fingerprint):
                return False
        except re.error:
            return False
    versions = profile.get("android")
    probe_android = str(probe.get("android", "")).strip()
    if isinstance(versions, list) and versions and probe_android:
        wanted = {str(item) for item in versions}
        major = probe_android.split(".")[0]
        if probe_android not in wanted and major not in wanted:
            return False
    return True


def never_packages(profile: Dict[str, Any]) -> set:
    """Packages the profile marks as never-touch, independent of the global protected list."""
    return {
        str(item.get("package", "")).strip()
        for item in profile.get("never", [])
        if isinstance(item, dict) and str(item.get("package", "")).strip()
    }


def never_for_phone(probe: Dict[str, Any]) -> set:
    """Union of `never` from every profile that matches this exact phone.

    Manual `disable` must respect these too: a package that is never-touch on the matching
    profile is never-touch even when the person types the command by hand.
    """
    packages: set = set()
    # Strict: a broken profile must stop a manual disable, not silently lose its never list.
    for profile in load_profiles(strict=True):
        if profile_matches(profile, probe):
            packages |= never_packages(profile)
    return packages


def build_matches(profile: Dict[str, Any], probe: Dict[str, Any]) -> bool:
    """True when the phone runs a build listed in `tested` (and auto-apply is allowed).

    A profile is versioned by firmware, not by marketing name. Auto-apply is refused on an OTA
    build even when the model and Android version still look right; the person can use `plan`
    and disable packages one at a time after reviewing the diff.
    """
    if verification_level(profile) != "device":
        return False
    if profile.get("auto_apply") is False:
        return False
    builds = {
        str(entry.get("build", "")).strip()
        for entry in profile.get("tested", [])
        if isinstance(entry, dict) and str(entry.get("build", "")).strip()
    }
    if not builds:
        return False
    fingerprint = str(probe.get("fingerprint", "")).strip()
    build_id = str(probe.get("build", "")).strip()
    if not fingerprint:
        return False
    return any(build in fingerprint or build == build_id for build in builds)


def classify(
    profile: Dict[str, Any],
    enabled: set,
    disabled: set,
    holders: Dict[str, List[str]],
    ime: str,
) -> List[Dict[str, str]]:
    """Build the plan rows: DISABLE, ASK, BLOCKED, SKIP, MISSING, KEEP."""
    rows: List[Dict[str, str]] = []
    seen = set()
    never = never_packages(profile)

    for section, wanted in (("disable", "DISABLE"), ("ask", "ASK")):
        for item in profile.get(section, []):
            package = item.get("package", "")
            if not package or package in seen:
                continue
            seen.add(package)
            row = {
                "action": wanted,
                "package": package,
                "why": item.get("why", ""),
                "breaks": item.get("breaks", ""),
                "section": section,
                "reason": "",
            }
            why_protected = protected.reason(package)
            if why_protected:
                row["action"] = "BLOCKED"
                row["reason"] = f"protected: {why_protected}"
            elif package in never:
                row["action"] = "BLOCKED"
                row["reason"] = "never-touch on this profile"
            elif package in disabled:
                row["action"] = "SKIP"
                row["reason"] = "already disabled"
            elif package not in enabled:
                row["action"] = "MISSING"
                row["reason"] = "not installed on this phone"
            else:
                role = role_conflict(package, holders, ime)
                if role:
                    row["action"] = "BLOCKED"
                    row["reason"] = role
            rows.append(row)

    for item in profile.get("never", []):
        package = item.get("package", "")
        if not package or package in seen:
            continue
        seen.add(package)
        rows.append(
            {
                "action": "KEEP",
                "package": package,
                "why": item.get("why", ""),
                "breaks": item.get("breaks", ""),
                "section": "never",
                "reason": "never on this profile",
            }
        )
    return rows


def role_conflict(package: str, holders: Dict[str, List[str]], ime: str) -> Optional[str]:
    """Return a reason if disabling `package` would remove a current role or keyboard."""
    for role in ROLE_NAMES:
        if package in holders.get(role, []):
            return f"it is the current {role} role holder"
    if ime and package == ime:
        return "it is the current keyboard (IME)"
    return None


def validate_profile(profile: Dict[str, Any], path: Optional[Path] = None) -> List[str]:
    """Validate one profile without external dependencies. Returns a list of errors."""
    errors: List[str] = []
    label = str(path or profile.get("_path") or profile.get("id") or "profile")

    for key in REQUIRED:
        if key not in profile:
            errors.append(f"{label}: missing required field '{key}'")

    profile_id = str(profile.get("id", ""))
    if profile_id and not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", profile_id):
        errors.append(f"{label}: id must be lowercase kebab-case, got '{profile_id}'")

    if not str(profile.get("model", "")).strip():
        errors.append(f"{label}: model is empty (use '*' only for a generic profile)")
    if (
        str(profile.get("model", "")).strip() == "*"
        and profile.get("generic") is not True
        and not str(profile.get("fingerprint_regex", "")).strip()
    ):
        errors.append(f"{label}: model '*' needs a fingerprint_regex unless the profile is generic")
    if profile.get("generic") is True and str(profile.get("model", "")).strip() != "*":
        errors.append(f"{label}: a generic profile must use model '*'")

    android = profile.get("android")
    if not isinstance(android, list) or not android or not all(isinstance(item, str) and item for item in android):
        errors.append(f"{label}: android must be a non-empty list of version strings")

    regex = str(profile.get("fingerprint_regex", ""))
    if regex:
        try:
            compiled = re.compile(regex)
        except re.error as exc:
            errors.append(f"{label}: fingerprint_regex does not compile: {exc}")
        else:
            if compiled.search("") is not None:
                errors.append(
                    f"{label}: fingerprint_regex matches an empty string; a failed probe would match every phone"
                )
    elif profile.get("generic") is not True:
        errors.append(f"{label}: fingerprint_regex is empty; pin the firmware family")

    declared_verification = str(profile.get("verification", "")).strip().lower()
    if declared_verification and declared_verification not in VERIFICATION_LEVELS:
        errors.append(
            f"{label}: verification must be one of {', '.join(VERIFICATION_LEVELS)}, got '{declared_verification}'"
        )
    verification = verification_level(profile)

    form_factor = str(profile.get("form_factor", "")).strip().lower()
    if form_factor and form_factor not in ("phone", "tablet"):
        errors.append(f"{label}: form_factor must be 'phone' or 'tablet', got '{form_factor}'")

    if "auto_apply" in profile and not isinstance(profile.get("auto_apply"), bool):
        errors.append(f"{label}: auto_apply must be true or false")
    if verification in ("documented", "reference") and profile.get("auto_apply") is not False:
        errors.append(f"{label}: {verification} profiles must set auto_apply: false")
    if verification == "reference" and profile.get("generic") is not True:
        errors.append(f"{label}: verification 'reference' requires generic: true")
    if verification == "documented" and profile.get("generic") is True:
        errors.append(f"{label}: a generic profile must use verification 'reference'")
    if verification == "device" and profile.get("generic") is True:
        errors.append(f"{label}: a generic profile cannot be verification 'device'")

    sources = profile.get("sources", [])
    if not isinstance(sources, list):
        errors.append(f"{label}: sources must be a list")
        sources = []
    for index, source in enumerate(sources):
        where = f"{label}: sources[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{where}: must be an object with title, url and retrieved")
            continue
        for key in ("title", "url", "retrieved"):
            if not str(source.get(key, "")).strip():
                errors.append(f"{where}: {key} is empty")
        url = str(source.get("url", "")).strip()
        if url and not re.match(r"^https?://", url):
            errors.append(f"{where}: url must start with http:// or https://")
        retrieved = str(source.get("retrieved", "")).strip()
        if retrieved and not re.match(r"^\d{4}-\d{2}-\d{2}$", retrieved):
            errors.append(f"{where}: retrieved must be YYYY-MM-DD")
    if verification == "documented" and not sources:
        errors.append(f"{label}: a documented profile needs at least one primary source")

    tested = profile.get("tested")
    if not isinstance(tested, list):
        errors.append(f"{label}: tested must be a list")
        tested = []
    if verification == "device":
        if not tested:
            errors.append(f"{label}: a device profile needs at least one real test")
        for index, entry in enumerate(tested):
            where = f"{label}: tested[{index}]"
            if not isinstance(entry, dict):
                errors.append(f"{where}: must be an object")
                continue
            for key in ("android", "build", "date", "by"):
                if not str(entry.get(key, "")).strip():
                    errors.append(f"{where}: {key} is empty")
    elif tested:
        errors.append(f"{label}: {verification} profiles must not claim tested entries")

    if not str(profile.get("notes", "")).strip():
        errors.append(f"{label}: notes is empty; say what is specific to this model")

    if verification in ("documented", "reference") and profile.get("disable"):
        errors.append(f"{label}: a generic/reference or documented profile must not have a 'disable' list")
    if verification == "documented" and not profile.get("ask"):
        errors.append(f"{label}: a documented profile needs a non-empty 'ask' list")

    seen = set()
    for section in ("disable", "ask", "never"):
        items = profile.get(section)
        if not isinstance(items, list):
            errors.append(f"{label}: {section} must be a list")
            continue
        for index, item in enumerate(items):
            where = f"{label}: {section}[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{where}: must be an object with a package")
                continue
            package = str(item.get("package", "")).strip()
            if not package:
                errors.append(f"{where}: package is empty")
                continue
            if not adb.valid_package(package):
                errors.append(f"{where}: invalid package name {package!r}")
            if package in seen:
                errors.append(f"{where}: duplicate package {package}")
            seen.add(package)
            if not str(item.get("why", "")).strip():
                errors.append(f"{where}: why is empty")
            if section in ("disable", "ask") and not str(item.get("breaks", "")).strip():
                errors.append(f"{where}: breaks is empty (say what the person loses)")
            if section in ("disable", "ask") and protected.is_protected(package):
                errors.append(f"{where}: {package} is protected; move it to never")
    return errors


def summary(profile: Dict[str, Any]) -> Dict[str, str]:
    return {
        "id": str(profile.get("id", "")),
        "brand": str(profile.get("brand", "")),
        "model": str(profile.get("model", "")),
        "marketing_name": str(profile.get("marketing_name", "")),
        "android": ", ".join(profile.get("android", [])),
        "verification": verification_level(profile),
        "sources": str(len(profile.get("sources", []))),
        "tested": str(len(profile.get("tested", []))),
        "disable": str(len(profile.get("disable", []))),
        "ask": str(len(profile.get("ask", []))),
    }
