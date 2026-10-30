#!/usr/bin/env python3
"""Maintainer helper: build documented profiles for every dump in an Android range.

It reads the cached Android-Dumps project lists, clones the selected stock branches with a
sparse checkout, runs scripts/dump_inventory.py, and writes one documented profile per device.
The ask/never catalog is in scripts/profile_catalog.json.

Usage:
    python scripts/batch_profiles.py --min 14 --max 16 --dry-run
    python scripts/batch_profiles.py --min 14 --max 16 --write
    python scripts/batch_profiles.py --tablets --min 8 --max 16 --write
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DISCOVERY = ROOT / "work" / "cache" / "discovery"
WORK = ROOT / "work" / "batch"
DUMPS = WORK / "dumps"
INV = WORK / "inv"
sys.path.insert(0, str(ROOT / "tools"))
import protected  # noqa: E402

BRANDS = ["samsung", "xiaomi", "redmi", "poco", "oneplus"]
BRAND_DIR = {"Samsung": "samsung", "Xiaomi": "xiaomi", "Redmi": "redmi",
             "POCO": "poco", "OnePlus": "oneplus"}
TABLETS = {
    "gta4l", "gta4lwifi", "gta4xl", "gta7lite", "gts7l", "gts7xl",
    "gtactive3", "pipa", "liuqin", "taiko", "mihal", "yunluo",
}
PLATFORM = {"mgvi_64_armv82", "duchamp_mgvi_64_armv82", "mivendor", "miproduct",
            "qssi_64", "missi"}
GENERIC_CODENAMES = {"ossi", "qssi", "mssi", "mivendor", "miproduct", "missi"}
CUSTOM = re.compile(r"lineage|aospa|evolution|arrow|crdroid|pixel|aosp|userdebug|test-keys", re.I)
GENERIC_MODEL = re.compile(
    r"^(unknown|generic|mainline|miproduct|missi|mivendor|qssi_64|SM\d{4}|"
    r".*for arm64.*|.*system image.*|.*qssi.*)$", re.I
)
CORE = {
    "android": "Android framework",
    "com.android.systemui": "Status bar, notifications, lock screen",
    "com.android.settings": "Android Settings",
    "com.android.shell": "ADB shell",
    "com.android.phone": "Telephony: calls, mobile data, SIM",
    "com.android.server.telecom": "Call routing",
    "com.android.incallui": "In-call UI",
    "com.android.mms.service": "MMS service",
    "com.android.providers.telephony": "SMS/APN provider",
    "com.android.providers.contacts": "Contacts provider",
    "com.android.permissioncontroller": "Permission controller",
    "com.google.android.permissioncontroller": "Permission controller",
    "com.android.packageinstaller": "Package installer",
    "com.google.android.packageinstaller": "Package installer",
    "com.google.android.gms": "Play Services: push, banking, backups",
    "com.google.android.gsf": "Google Services Framework",
    "com.android.vending": "Play Store",
    "com.google.android.webview": "WebView for in-app browsers",
    "com.android.nfc": "NFC payments and tags",
    "com.android.bluetooth": "Bluetooth: earbuds, car, wearables",
    "com.android.emergency": "Emergency information and dialer",
    "com.android.documentsui": "System file picker",
}
PATTERNS = """/README.md
/all_files.txt
/system/system/build.prop
/product/etc/build.prop
/system_ext/etc/build.prop
/vendor/build.prop
/odm/etc/build.prop
/vendor/odm/etc/build.prop
system/system/etc/permissions
product/etc/permissions
system_ext/etc/permissions
vendor/etc/permissions
vendor/odm/etc/permissions
odm/etc/permissions
"""


MODEL_URLS = {
    "xiaomi": "https://raw.githubusercontent.com/KHwang9883/MobileModels/master/brands/xiaomi_en.md",
    "samsung": "https://raw.githubusercontent.com/KHwang9883/MobileModels/master/brands/samsung_global_en.md",
    "oneplus": "https://raw.githubusercontent.com/KHwang9883/MobileModels/master/brands/oneplus_en.md",
}


def ensure_model_names():
    """Download the public model-name tables into the local cache when missing."""
    target = ROOT / "work" / "cache" / "models"
    target.mkdir(parents=True, exist_ok=True)
    for name, url in MODEL_URLS.items():
        path = target / f"{name}.md"
        if path.is_file():
            continue
        request = urllib.request.Request(url, headers={"User-Agent": "clean-your-phone-profile-inventory"})
        with urllib.request.urlopen(request, timeout=60) as response:
            path.write_bytes(response.read())


def load_model_maps():
    maps = {}
    for brand, filename in (("xiaomi", "xiaomi.md"), ("samsung", "samsung.md"),
                            ("oneplus", "oneplus.md")):
        path = ROOT / "work" / "cache" / "models" / filename
        by_model = {}
        by_codename = {}
        current = ""
        current_marketing = ""
        if not path.is_file():
            maps[brand] = {"by_model": by_model, "by_codename": by_codename}
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            header = re.match(r"^\*\*(.+?):\*\*$", stripped)
            if header:
                text = header.group(1)
                names = re.findall(r"`([^`]+)`", text)
                if names:
                    current = names[-1].lower()
                    current_marketing = re.sub(r"^\[`[^`]+`\]\s*", "", text)
                    current_marketing = re.sub(r"\s*\(`[^`]+`\).*$", "", current_marketing).strip()
                    current_marketing = re.sub(r"^REDMI\b", "Redmi", current_marketing)
                    names_for_code = by_codename.setdefault(current, [])
                    if current_marketing not in names_for_code:
                        names_for_code.append(current_marketing)
                continue
            model_line = re.match(r"^`([^`]+)`:\s*(.+)$", stripped)
            if model_line and current and current_marketing:
                model = model_line.group(1).strip().upper()
                if model not in by_model:
                    by_model[model] = current_marketing
        maps[brand] = {"by_model": by_model, "by_codename": by_codename}
    return maps


def lookup_marketing(maps, brand, model, codename, group):
    key = "xiaomi" if group in ("xiaomi", "redmi", "poco") else "samsung" if group == "samsung" else "oneplus"
    table = maps[key]
    if model:
        exact = table["by_model"].get(model.upper())
        if exact:
            return exact
        # Samsung region suffixes differ: SM-A146P vs SM-A146B.
        base = re.match(r"^(SM-[A-Z]\d{3})", model.upper())
        if base:
            for known_model, marketing in table["by_model"].items():
                if known_model.startswith(base.group(1)):
                    return marketing
    names = table["by_codename"].get(codename.lower(), [])
    if not names:
        return ""
    brand_token = brand.upper()
    if brand == "Xiaomi" and group in ("redmi", "poco"):
        brand_token = group.upper()
    matching = [name for name in names if name.upper().startswith(brand_token)]
    if len(matching) == 1:
        return matching[0]
    if matching:
        return matching[0]
    if len(names) == 1:
        return names[0]
    return ""


def load_catalogs():
    data = json.loads((ROOT / "scripts" / "profile_catalog.json").read_text(encoding="utf-8"))
    asks = {}
    nevers = {}
    for key in ("samsung", "xiaomi", "oneplus"):
        asks[key] = {package: tuple(values) for package, values in data[key]["ask"].items()}
        nevers[key] = dict(data[key]["never"])
        for package, why in CORE.items():
            nevers[key].setdefault(package, why)
    return asks, nevers


def android_of(branch: str):
    match = re.search(r"user-(\d{1,2})(?:\.\d+)*[-_]", branch or "")
    return int(match.group(1)) if match else None


def slug(text: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return value or "profile"


def prop(props, keys):
    for key in keys:
        value = str(props.get(key, "")).strip()
        if value:
            return value
    return ""


def pick_prop(props, keys, reject=()):
    """First non-empty, non-generic value; reject values equal to codename/project."""
    rejected = {str(item).strip().lower() for item in reject if item}
    for key in keys:
        value = str(props.get(key, "")).strip()
        if not value:
            continue
        if GENERIC_MODEL.match(value) or value.lower() in rejected:
            continue
        return value
    return ""


def normalize_brand(value: str) -> str:
    lowered = value.strip().lower()
    return {"samsung": "Samsung", "xiaomi": "Xiaomi", "redmi": "Redmi",
            "poco": "POCO", "oneplus": "OnePlus"}.get(lowered, value.strip())


def build_record(brand_group: str, name: str, project: str, branch: str, inventory: dict,
                 model_maps: dict):
    props = inventory.get("props", {})
    probe_brand = normalize_brand(prop(props, [
        "ro.product.vendor.brand", "ro.product.odm.brand", "ro.product.brand"]))
    brand = probe_brand if probe_brand in BRAND_DIR else normalize_brand(brand_group)
    codename = name if brand == "Samsung" else pick_prop(props, [
        "ro.product.odm.device", "ro.product.vendor.device", "ro.product.product.device",
        "ro.product.device"], reject=(name,)) or name
    model = pick_prop(props, [
        "ro.product.odm.model", "ro.product.vendor.model", "ro.product.product.model",
        "ro.product.model"], reject=(name, codename))
    marketing = pick_prop(props, [
        "ro.product.odm.marketname", "ro.product.vendor.marketname",
        "ro.product.product.marketname"], reject=(name, codename, model))
    if not marketing:
        marketing = lookup_marketing(model_maps, brand, model, codename, brand_group)
    if marketing:
        for candidate in ("Xiaomi", "Redmi", "POCO"):
            if marketing.upper().startswith(candidate.upper()):
                brand = candidate
                break
    elif brand == "Xiaomi" and brand_group in ("redmi", "poco"):
        brand = normalize_brand(brand_group)
    release = prop(props, ["ro.build.version.release"])
    match = re.match(r"(\d+)", release)
    android = match.group(1) if match else str(android_of(branch) or "")

    draft_path = INV / f"{brand_group}__{name}" / "draft-profile.json"
    fingerprint = ""
    if draft_path.is_file():
        draft = json.loads(draft_path.read_text(encoding="utf-8"))
        fingerprint = draft.get("_draft", {}).get("fingerprint", "")
    if not fingerprint:
        fingerprint = prop(props, ["ro.build.fingerprint", "ro.vendor.build.fingerprint"])
    prefix = fingerprint.split(":", 1)[0].strip()
    if "/" in prefix:
        regex = "^" + re.escape(prefix) + ":"
    else:
        regex = "^[^/]+/" + re.escape(codename)
    return {
        "brand_group": brand_group,
        "project": project,
        "branch": branch,
        "brand": brand,
        "codename": codename,
        "model": model,
        "marketing": marketing,
        "android": android,
        "fingerprint": fingerprint,
        "regex": regex,
        "candidates": inventory.get("candidates", {}),
    }


def make_profile(record: dict, asks: dict, nevers: dict, existing_ids: set):
    brand = record["brand"]
    key = "samsung" if brand == "Samsung" else "oneplus" if brand == "OnePlus" else "xiaomi"
    candidates = record["candidates"]
    never_packages = {package for package in nevers[key] if package in candidates or package in CORE}
    never = [{"package": package, "why": nevers[key][package]}
             for package in sorted(never_packages)]
    never_set = set(never_packages)
    ask = []
    for package in sorted(asks[key]):
        if package not in candidates or package in never_set:
            continue
        if protected.is_protected(package):
            continue
        why, breaks = asks[key][package]
        if not why or not breaks:
            continue
        ask.append({"package": package, "why": why, "breaks": breaks})
    if not ask:
        return None
    model_field = record["model"] or "*"
    if brand == "Samsung" and record["model"]:
        name_part = record["model"]
    else:
        name_part = record["marketing"] or record["model"] or record["codename"]
        prefix = brand + " "
        if name_part.lower().startswith(prefix.lower()):
            name_part = name_part[len(prefix):]
    name_part = name_part.split(" / ")[0].split(" + ")[0]
    profile_id = slug(f"{brand}-{name_part}")
    if profile_id in existing_ids:
        profile_id = slug(f"{brand}-{name_part}-{record['codename']}")
    suffix = 2
    base = profile_id
    while profile_id in existing_ids:
        profile_id = f"{base}-{suffix}"
        suffix += 1
    existing_ids.add(profile_id)

    source_base = f"https://gitlab.com/{record['project']}"
    raw_base = f"{source_base}/-/raw/{record['branch']}"
    notes = (
        f"Documented from the {record['codename']} firmware dump (Android {record['android'] or 'unknown'}), "
        f"not tested on a physical phone. {brand} package lists and preloads vary by region and carrier. "
    )
    if model_field == "*":
        notes += ("Regional model numbers vary; the profile is pinned by fingerprint and codename. ")
    if record.get("form_factor") == "tablet":
        notes += ("Tablet: dialer and SMS checks are warnings, not failures. ")
    notes += "No auto-apply; ask before every package."
    profile = {
        "id": profile_id,
        "brand": brand,
        "model": model_field,
        "marketing_name": record["marketing"],
        "codename": record["codename"],
        "android": [record["android"]] if record["android"] else [],
        "fingerprint_regex": record["regex"],
        "auto_apply": False,
        "verification": "documented",
        "sources": [
            {"title": f"Android Dumps: {record['project']}", "url": source_base,
             "retrieved": date.today().isoformat(),
             "note": f"Firmware dump for {record['marketing'] or record['model'] or record['codename']}"},
            {"title": "Dump README (build metadata)", "url": f"{raw_base}/README.md",
             "retrieved": date.today().isoformat(),
             "note": "Codename, build id and fingerprint"},
            {"title": "Dump all_files.txt (APK and permission inventory)",
             "url": f"{raw_base}/all_files.txt", "retrieved": date.today().isoformat(),
             "note": "Evidence that each package path exists in the firmware"},
        ],
        "tested": [],
        "disable": [],
        "ask": ask,
        "never": never,
        "notes": notes,
    }
    if record.get("form_factor") == "tablet":
        profile["form_factor"] = "tablet"
    return profile


def git(args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd, text=True, capture_output=True)


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)


def clone_dump(brand, name, project, branch):
    target = DUMPS / f"{brand}__{name}"
    if not (target / ".git").is_dir():
        target.parent.mkdir(parents=True, exist_ok=True)
        result = git(["clone", "--filter=blob:none", "--no-checkout", "--single-branch",
                      "--branch", branch, f"https://gitlab.com/{project}.git", str(target)])
        if result.returncode != 0:
            return False, result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "clone failed"
    git(["config", "core.protectNTFS", "false"], cwd=target)
    git(["config", "core.longpaths", "true"], cwd=target)
    git(["sparse-checkout", "init", "--no-cone"], cwd=target)
    (target / ".git" / "info" / "sparse-checkout").write_text(PATTERNS, encoding="ascii")
    result = git(["read-tree", "-mu", "HEAD"], cwd=target)
    if result.returncode != 0:
        return False, result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "checkout failed"
    return True, ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min", type=int, default=14)
    parser.add_argument("--max", type=int, default=16)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--names", default="")
    parser.add_argument("--include-unversioned", action="store_true")
    parser.add_argument("--tablets", action="store_true")
    args = parser.parse_args()

    asks, nevers = load_catalogs()
    try:
        ensure_model_names()
    except Exception as exc:  # network is optional; keep going with codenames.
        print(f"warning: cannot refresh model names: {exc}", file=sys.stderr)
    model_maps = load_model_maps()
    existing = set()
    existing_ids = set()
    existing_models = set()
    existing_marketing = set()
    for path in (ROOT / "profiles").glob("*/*.json"):
        profile = json.loads(path.read_text(encoding="utf-8"))
        if profile.get("codename"):
            existing.add(profile["codename"].lower())
        if profile.get("id"):
            existing_ids.add(profile["id"])
        if profile.get("model") and profile["model"] != "*":
            existing_models.add((profile.get("brand", "").lower(), profile["model"].lower()))
        elif profile.get("marketing_name"):
            existing_marketing.add(profile["marketing_name"].lower())

    wanted = {item.strip().lower() for item in args.names.split(",") if item.strip()}
    candidates = []
    for brand in BRANDS:
        for project in json.loads((DISCOVERY / f"{brand}.json").read_text(encoding="utf-8")):
            name = project["name"]
            is_tablet = name.lower() in TABLETS
            if is_tablet != args.tablets:
                continue
            if name.lower() in PLATFORM or name.lower() in existing:
                continue
            if wanted and name.lower() not in wanted:
                continue
            if CUSTOM.search(project["branch"] or ""):
                continue
            version = android_of(project["branch"])
            if version is None:
                if not args.include_unversioned:
                    continue
                version = 0
            elif not (args.min <= version <= args.max):
                continue
            candidates.append((brand, name, project["path"], project["branch"], version))
    candidates.sort(key=lambda item: (-item[4], item[0], item[1]))
    if args.limit:
        candidates = candidates[: args.limit]

    print(f"candidates: {len(candidates)}")
    records = []
    failures = []
    for index, (brand, name, project, branch, version) in enumerate(candidates, 1):
        print(f"[{index}/{len(candidates)}] {brand}/{name} ({version}) ... ", end="", flush=True)
        ok, error = clone_dump(brand, name, project, branch)
        if not ok:
            print("clone failed:", error)
            failures.append({"project": project, "error": error})
            continue
        inv_dir = INV / f"{brand}__{name}"
        result = run([sys.executable, str(ROOT / "scripts" / "dump_inventory.py"),
                      "--project", project, "--local-dir", str(DUMPS / f"{brand}__{name}"),
                      "--out", str(inv_dir)])
        if result.returncode != 0:
            print("inventory failed:", result.stderr.strip().splitlines()[-1])
            failures.append({"project": project, "error": result.stderr.strip()[-300:]})
            continue
        inventory = json.loads((inv_dir / "inventory.json").read_text(encoding="utf-8"))
        record = build_record(brand, name, project, branch, inventory, model_maps)
        record["form_factor"] = "tablet" if args.tablets else "phone"
        if record["codename"].lower() in GENERIC_CODENAMES:
            print(f"skip (generic build codename {record['codename']})")
            continue
        if not record["android"] or int(record["android"]) < args.min:
            print(f"skip (android {record['android']})")
            continue
        records.append(record)
        print(f"ok ({record['brand']} {record['model'] or record['codename']}, "
              f"android {record['android']}, {len(record['candidates'])} candidates)")

    # One profile per codename; prefer a record with a marketing name and a real model.
    best = {}
    for record in records:
        key = record["codename"].lower()
        score = (bool(record["marketing"]), bool(record["model"]),
                 1 if record["brand"] == normalize_brand(record["brand_group"]) else 0)
        if key not in best or score > best[key][0]:
            best[key] = (score, record)
    unique = [item[1] for item in best.values()]

    generated = []
    for record in unique:
        if record["model"] and (record["brand"].lower(), record["model"].lower()) in existing_models:
            print(f"skip {record['brand']} {record['model']}: model already has a profile")
            continue
        if not record["model"] and record["marketing"] and record["marketing"].lower() in existing_marketing:
            print(f"skip {record['brand']} {record['codename']}: marketing name already has a profile")
            continue
        profile = make_profile(record, asks, nevers, existing_ids)
        if not profile:
            print(f"skip {record['brand']} {record['codename']}: no catalog packages in dump")
            continue
        filename = profile["id"]
        if profile["brand"] == "Samsung" and filename.startswith("samsung-"):
            filename = filename[len("samsung-"):]
        path = ROOT / "profiles" / BRAND_DIR[profile["brand"]] / f"{filename}.json"
        generated.append((path, profile))
        if profile.get("model") and profile["model"] != "*":
            existing_models.add((profile["brand"].lower(), profile["model"].lower()))
        elif profile.get("marketing_name"):
            existing_marketing.add(profile["marketing_name"].lower())
        print(f"profile {profile['id']}: {profile['brand']} {profile['model']} "
              f"android {profile['android']} ask={len(profile['ask'])} never={len(profile['never'])}")

    print(f"records: {len(records)}; unique: {len(unique)}; profiles: {len(generated)}; failures: {len(failures)}")
    if args.write:
        for path, profile in generated:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(profile, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (WORK / "last-run.json").write_text(
            json.dumps({"at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "generated": [str(p) for p, _ in generated],
                        "failures": failures}, indent=2),
            encoding="utf-8")
        print("written")
    else:
        print("dry run: nothing written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
