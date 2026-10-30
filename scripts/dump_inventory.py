#!/usr/bin/env python3
"""Maintainer helper: build a documented-profile draft from an Android Dumps repository.

This script is NOT used by the runtime skill. It only reads public firmware metadata and writes
local inventory files. It never touches a phone.

Example:
    python scripts/dump_inventory.py \
        --project Android-Dumps/samsung/pa3q \
        --marketing-name "Galaxy S25 Ultra" \
        --out work/pa3q
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import adb  # noqa: E402

API = "https://gitlab.com/api/v4"
USER_AGENT = "cleanyourphone-profile-inventory"
README_KEYS = {
    "Manufacturer": "manufacturer",
    "Platform": "platform",
    "Codename": "codename",
    "Brand": "brand",
    "Flavor": "flavor",
    "Release Version": "release",
    "Kernel Version": "kernel",
    "Id": "build_id",
    "Incremental": "incremental",
    "Tags": "tags",
    "Fingerprint": "readme_fingerprint",
    "Branch": "branch",
    "Repo": "repo",
}

PERMISSION_RE = re.compile(r"(?:privapp|signature|default)-permissions-([A-Za-z0-9_.]+)\.xml$")
PREFERRED_RE = re.compile(r"preferred-apps/([A-Za-z0-9_.]+)\.xml$")
SYSCONFIG_RE = re.compile(r"sysconfig/([A-Za-z0-9_.]+)\.xml$")
APK_RE = re.compile(r"^(.*?)/(?:[^/]+)\.apk$")
BRAND_NAMES = {
    "samsung": "Samsung",
    "google": "Google",
    "xiaomi": "Xiaomi",
    "redmi": "Redmi",
    "poco": "POCO",
    "oneplus": "OnePlus",
    "oppo": "OPPO",
    "realme": "realme",
    "huawei": "Huawei",
    "honor": "Honor",
}


def _headers() -> Dict[str, str]:
    headers = {"User-Agent": USER_AGENT}
    token = os.environ.get("GITLAB_TOKEN", "").strip()
    if token:
        headers["PRIVATE-TOKEN"] = token
    return headers


def request(url: str, cache_path: Optional[Path] = None, timeout: int = 60) -> bytes:
    if cache_path and cache_path.is_file():
        return cache_path.read_bytes()
    req = urllib.request.Request(url, headers=_headers())
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read()
    except urllib.error.HTTPError as exc:
        if exc.code == 429:
            raise RuntimeError(
                "GitLab rate limit (HTTP 429). Wait a minute, set GITLAB_TOKEN, or reuse the cache."
            ) from exc
        raise
    if cache_path:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_bytes(data)
    return data


def api_json(path: str, cache_path: Optional[Path] = None) -> Any:
    return json.loads(request(f"{API}{path}", cache_path=cache_path).decode("utf-8-sig"))


def cache_name(path: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", path).strip("-").lower() + ".txt"


def project_info(full_path: str, cache_dir: Path) -> Dict[str, Any]:
    encoded = urllib.parse.quote(full_path, safe="")
    cache = cache_dir / "project.json"
    return api_json(f"/projects/{encoded}", cache_path=cache)


def fetch_file(project_id: int, path: str, ref: str, cache_dir: Path) -> str:
    encoded_path = urllib.parse.quote(path, safe="")
    encoded_ref = urllib.parse.quote(ref, safe="")
    url = f"{API}/projects/{project_id}/repository/files/{encoded_path}/raw?ref={encoded_ref}"
    cache = cache_dir / cache_name(path)
    return request(url, cache_path=cache).decode("utf-8-sig", errors="replace")


def parse_readme(text: str) -> Dict[str, str]:
    metadata: Dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"^-\s*([^:]+):\s*(.*)$", line.strip())
        if not match:
            continue
        key = README_KEYS.get(match.group(1).strip())
        if key:
            metadata[key] = match.group(2).strip()
    return metadata


def parse_props(text: str) -> Dict[str, str]:
    props: Dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        props[key.strip()] = value.strip()
    return props


def first_prop(props: Dict[str, str], keys: List[str]) -> str:
    for key in keys:
        value = props.get(key, "").strip()
        if value:
            return value
    return ""


def package_candidates(all_files: str) -> Dict[str, str]:
    """Return package -> first evidence path, from permission XMLs and APK paths."""
    found: Dict[str, str] = {}
    for line in all_files.splitlines():
        path = line.strip()
        if not path:
            continue
        for regex in (PERMISSION_RE, PREFERRED_RE, SYSCONFIG_RE):
            match = regex.search(path)
            if match:
                package = match.group(1)
                if "." in package and adb.valid_package(package):
                    found.setdefault(package, path)
        match = APK_RE.match(path)
        if match:
            folder = match.group(1).rsplit("/", 1)[-1]
            if "." in folder and adb.valid_package(folder):
                found.setdefault(folder, path)
    return dict(sorted(found.items()))


XML_PACKAGE_RE = re.compile(r'\bpackage\s*=\s*"([A-Za-z][A-Za-z0-9_.]*)"')
PERMISSION_PATH_RE = re.compile(r"(?:^|/)(?:etc/)?(?:permissions|default-permissions)/[^/]+\.xml$")


def scan_xml_candidates(local_dir: Path, all_files: str) -> Dict[str, str]:
    """Read permission XML contents from a local dump and return package -> evidence path."""
    found: Dict[str, str] = {}
    for line in all_files.splitlines():
        path = line.strip()
        if not path or not PERMISSION_PATH_RE.search(path):
            continue
        xml_file = local_dir / path
        if not xml_file.is_file():
            continue
        try:
            text = xml_file.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        for package in XML_PACKAGE_RE.findall(text):
            if "." in package and adb.valid_package(package):
                found.setdefault(package, path)
    return dict(sorted(found.items()))


def build_fingerprint_regex(fingerprint: str, codename: str) -> str:
    if fingerprint:
        prefix = fingerprint.split(":", 1)[0]
        if prefix:
            return "^" + re.escape(prefix)
    if codename:
        return "^[^/]+/" + re.escape(codename)
    return ""


def build_draft(
    project: Dict[str, Any],
    ref: str,
    metadata: Dict[str, str],
    props: Dict[str, str],
    candidates: Dict[str, str],
    marketing_name: str,
    source_urls: List[Dict[str, str]],
    model_override: str = "",
) -> Dict[str, Any]:
    model = model_override.strip() or first_prop(
        props, ["ro.product.vendor.model", "ro.product.model", "ro.product.system.model"]
    )
    codename = metadata.get("codename", "") or first_prop(
        props, ["ro.product.vendor.device", "ro.product.device", "ro.product.system.device"]
    )
    brand = metadata.get("brand", "") or first_prop(
        props, ["ro.product.vendor.brand", "ro.product.brand", "ro.product.system.brand"]
    )
    release = first_prop(props, ["ro.build.version.release"]) or metadata.get("release", "")
    build = first_prop(props, ["ro.build.display.id"]) or metadata.get("build_id", "")
    fingerprint = first_prop(
        props,
        ["ro.build.fingerprint", "ro.vendor.build.fingerprint", "ro.system.build.fingerprint"],
    )
    readme_fingerprint = metadata.get("readme_fingerprint", "")
    if readme_fingerprint and codename and codename.lower() in readme_fingerprint.lower():
        fingerprint = readme_fingerprint
    if not fingerprint:
        fingerprint = readme_fingerprint
    if not model:
        model = metadata.get("model", "")
    brand = BRAND_NAMES.get(brand.lower(), brand)

    profile_id = adb.slug(f"{brand or project['name']}-{model or codename or project['path']}")
    draft = {
        "id": profile_id,
        "brand": brand,
        "model": model or codename,
        "marketing_name": marketing_name,
        "codename": codename,
        "android": [release] if release else [],
        "fingerprint_regex": build_fingerprint_regex(fingerprint, codename),
        "auto_apply": False,
        "verification": "documented",
        "sources": source_urls,
        "tested": [],
        "disable": [],
        "ask": [],
        "never": [],
        "notes": (
            "DOCUMENTED DRAFT. Built from a firmware dump, not tested on a physical phone. "
            "Curate 'ask' with real why/breaks text before validating and committing."
        ),
        "_draft": {
            "project": project["path_with_namespace"],
            "ref": ref,
            "build_id": build,
            "fingerprint": fingerprint,
            "candidate_count": len(candidates),
            "candidates": candidates,
        },
    }
    return draft


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="GitLab project path, e.g. Android-Dumps/samsung/pa3q")
    parser.add_argument("--local-dir", help="read a sparse/local clone instead of the GitLab API")
    parser.add_argument("--ref", help="branch/tag/commit; default: the project default branch")
    parser.add_argument("--model", default="", help="exact model number, e.g. SM-S938B or CPH2487")
    parser.add_argument("--marketing-name", default="", help="human model name, e.g. Galaxy S25 Ultra")
    parser.add_argument("--out", required=True, help="output directory")
    parser.add_argument("--cache-dir", default="work/cache", help="download cache (default: work/cache)")
    args = parser.parse_args(argv)

    local = Path(args.local_dir) if args.local_dir else None
    if local:
        if not local.is_dir():
            print(f"error: local dump directory not found: {local}", file=sys.stderr)
            return 2
        ref = args.ref or "local"
        project = {
            "id": 0,
            "path_with_namespace": args.project,
            "name": args.project.rsplit("/", 1)[-1],
            "path": args.project.rsplit("/", 1)[-1],
            "default_branch": ref,
        }
        try:
            readme = (local / "README.md").read_text(encoding="utf-8-sig")
            all_files = (local / "all_files.txt").read_text(encoding="utf-8-sig")
        except OSError as exc:
            print(f"error: cannot read the local dump: {exc}", file=sys.stderr)
            return 2
        metadata = parse_readme(readme)
        if not args.ref and metadata.get("branch"):
            ref = metadata["branch"]
        props: Dict[str, str] = {}
        for prop_path in (
            "vendor/build.prop",
            "system/system/build.prop",
            "product/etc/build.prop",
            "system_ext/etc/build.prop",
            "odm/etc/build.prop",
        ):
            prop_file = local / prop_path
            if prop_file.is_file():
                props.update(parse_props(prop_file.read_text(encoding="utf-8-sig")))
    else:
        project_cache = Path(args.cache_dir) / adb.slug(args.project)
        try:
            project = project_info(args.project, project_cache)
        except Exception as exc:
            print(f"error: cannot read {args.project}: {exc}", file=sys.stderr)
            return 2
        ref = args.ref or project.get("default_branch")
        if not ref:
            print("error: project has no default branch", file=sys.stderr)
            return 2
        file_cache = project_cache / adb.slug(ref)
        try:
            readme = fetch_file(project["id"], "README.md", ref, file_cache)
            all_files = fetch_file(project["id"], "all_files.txt", ref, file_cache)
        except Exception as exc:
            print(f"error: cannot download the dump files: {exc}", file=sys.stderr)
            return 2
        metadata = parse_readme(readme)
        props = {}
        for prop_path in (
            "vendor/build.prop",
            "system/system/build.prop",
            "product/etc/build.prop",
            "system_ext/etc/build.prop",
            "odm/etc/build.prop",
        ):
            try:
                props.update(parse_props(fetch_file(project["id"], prop_path, ref, file_cache)))
            except Exception:
                continue

    output = Path(args.out)
    output.mkdir(parents=True, exist_ok=True)

    candidates = package_candidates(all_files)
    if local:
        candidates.update(scan_xml_candidates(local, all_files))
        candidates = dict(sorted(candidates.items()))
    base_url = f"https://gitlab.com/{project['path_with_namespace']}"
    raw_url = f"{base_url}/-/raw/{urllib.parse.quote(ref, safe='')}"
    source_urls = [
        {
            "title": f"Android Dumps: {project['path_with_namespace']}",
            "url": base_url,
            "retrieved": date.today().isoformat(),
            "note": "Firmware dump: README, build.prop, all_files.txt",
        },
        {
            "title": "README.md",
            "url": f"{raw_url}/README.md",
            "retrieved": date.today().isoformat(),
            "note": "Dump metadata and fingerprint",
        },
        {
            "title": "all_files.txt",
            "url": f"{raw_url}/all_files.txt",
            "retrieved": date.today().isoformat(),
            "note": "APK and permission XML inventory",
        },
    ]

    draft = build_draft(
        project,
        ref,
        metadata,
        props,
        candidates,
        args.marketing_name,
        source_urls,
        model_override=args.model,
    )
    (output / "inventory.json").write_text(
        json.dumps(
            {
                "project": project["path_with_namespace"],
                "ref": ref,
                "metadata": metadata,
                "props": props,
                "candidates": candidates,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (output / "draft-profile.json").write_text(
        json.dumps(draft, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Project: {project['path_with_namespace']} ({ref})")
    print(f"Candidates: {len(candidates)}")
    print(f"Wrote: {output / 'inventory.json'}")
    print(f"Wrote: {output / 'draft-profile.json'}")
    print("Next: curate 'ask' and 'never', remove '_draft', then run phone.py validate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
