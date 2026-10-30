#!/usr/bin/env python3
"""Maintainer helper: cache the Android-Dumps project lists used by batch_profiles.py.

This reads public GitLab metadata only. It writes one JSON file per brand under
work/cache/discovery/. Set GITLAB_TOKEN to avoid the anonymous rate limit.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "work" / "cache" / "discovery"
API = "https://gitlab.com/api/v4"
SOURCES = {
    "samsung": ["Android-Dumps/samsung"],
    "xiaomi": ["Android-Dumps/xiaomi"],
    "redmi": ["Android-Dumps/redmi"],
    "poco": ["Android-Dumps/poco"],
    "oneplus": ["Android-Dumps/oneplus", "noescape-firmware-dumps/ONEPLUS"],
}


def request(path: str) -> list:
    headers = {"User-Agent": "cleanyourphone-profile-inventory"}
    token = os.environ.get("GITLAB_TOKEN", "").strip()
    if token:
        headers["PRIVATE-TOKEN"] = token
    url = API + path
    for attempt in range(3):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                return json.loads(response.read().decode("utf-8-sig"))
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < 2:
                wait = 30 * (attempt + 1)
                print(f"rate limited; waiting {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            raise
    return []


def main() -> int:
    argparse.ArgumentParser(
        description="Cache the Android-Dumps project lists under work/cache/discovery."
    ).parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for brand, sources in SOURCES.items():
        projects = {}
        for source in sources:
            group = urllib.parse.quote(source, safe="")
            page = 1
            while True:
                batch = request(f"/groups/{group}/projects?per_page=100&page={page}"
                                "&order_by=last_activity_at&sort=desc")
                for project in batch:
                    projects[project["path_with_namespace"]] = project
                if len(batch) < 100:
                    break
                page += 1
        slim = [
            {
                "path": project["path_with_namespace"],
                "name": project["name"],
                "branch": project.get("default_branch"),
                "activity": project.get("last_activity_at"),
            }
            for project in projects.values()
        ]
        slim.sort(key=lambda item: item["activity"] or "", reverse=True)
        (OUT / f"{brand}.json").write_text(
            json.dumps(slim, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{brand}: {len(slim)} projects")
    return 0


if __name__ == "__main__":
    sys.exit(main())
