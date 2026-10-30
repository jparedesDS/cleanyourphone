#!/usr/bin/env python3
"""Maintainer helper: report profile coverage and data-quality issues."""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROFILES = ROOT / "profiles"


def main() -> int:
    argparse.ArgumentParser(description="Report profile coverage and curation issues.").parse_args()
    rows = [json.loads(path.read_text(encoding="utf-8")) for path in PROFILES.glob("*/*.json")]
    brands = collections.Counter(row["brand"] for row in rows)
    verification = collections.Counter(row["verification"] for row in rows)
    print(f"total: {len(rows)}")
    print("brands:", dict(sorted(brands.items())))
    print("verification:", dict(sorted(verification.items())))
    for brand in sorted(brands):
        values = [row for row in rows if row["brand"] == brand]
        versions = sorted({item for row in values for item in row.get("android", [])},
                          key=lambda item: int(item) if item.isdigit() else 99)
        print(f"  {brand}: {len(values)} profiles, Android {', '.join(versions)}")

    thin = sorted((len(row["ask"]), row["id"]) for row in rows
                  if row["verification"] == "documented" and len(row["ask"]) < 20)
    print(f"\ndocumented profiles with fewer than 20 ask entries: {len(thin)}")
    for count, profile_id in thin:
        print(f"  {count:>2}  {profile_id}")

    no_name = sorted(row["id"] for row in rows
                     if not row.get("marketing_name") and not row.get("generic"))
    print(f"\nprofiles without marketing_name: {len(no_name)}")
    for profile_id in no_name:
        print(f"  {profile_id}")

    star = sum(1 for row in rows if row.get("model") == "*")
    print(f"\nprofiles with model '*': {star}")

    by_model = collections.defaultdict(list)
    by_marketing = collections.defaultdict(list)
    for row in rows:
        if row.get("model") and row["model"] != "*":
            by_model[(row["brand"].lower(), row["model"].lower())].append(row["id"])
        elif row.get("marketing_name"):
            by_marketing[row["marketing_name"].lower()].append(row["id"])
    duplicates = [values for values in by_model.values() if len(values) > 1]
    duplicates += [values for values in by_marketing.values() if len(values) > 1]
    print(f"duplicate model/marketing groups: {len(duplicates)}")
    for values in duplicates:
        print("  ", ", ".join(values))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
