#!/usr/bin/env python3
"""Maintainer helper: rebuild the profile catalog and documentation tables."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROFILES = ROOT / "profiles"
ORDER = {"google": 0, "samsung": 1, "oneplus": 2, "xiaomi": 3, "redmi": 4, "poco": 5, "generic": 6}
VERIFY_RANK = {"device": 0, "documented": 1, "reference": 2}
BRANDS = ["Google", "Samsung", "Xiaomi", "Redmi", "POCO", "OnePlus"]


def load():
    rows = []
    for path in PROFILES.glob("*/*.json"):
        profile = json.loads(path.read_text(encoding="utf-8"))
        rel = path.relative_to(PROFILES).as_posix()
        rows.append((path.parent.name, rel, profile))
    rows.sort(key=lambda item: (ORDER.get(item[0], 9),
                                VERIFY_RANK.get(item[2].get("verification", ""), 9),
                                (item[2].get("marketing_name") or item[2].get("model") or item[0]).lower(),
                                item[2]["id"]))
    return rows


def display(profile):
    marketing = str(profile.get("marketing_name", "")).strip()
    model = str(profile.get("model", "")).strip()
    codename = str(profile.get("codename", "")).strip()
    if profile.get("generic"):
        return "Any Android 8+"
    if marketing and model and model != "*" and model.lower() not in marketing.lower():
        return f"{marketing} ({model})"
    if marketing and model == "*" and codename:
        return f"{marketing} (`{codename}`)"
    if marketing:
        return marketing
    if model and model != "*":
        return model
    return codename or profile["id"]


def android_text(profile):
    versions = [str(item) for item in profile.get("android", [])]
    if not versions:
        return ""
    if all(item.isdigit() for item in versions):
        numbers = sorted(int(item) for item in versions)
        if numbers == list(range(numbers[0], numbers[-1] + 1)):
            return f"{numbers[0]}\u2013{numbers[-1]}" if len(numbers) > 1 else str(numbers[0])
        return ", ".join(str(item) for item in numbers)
    return ", ".join(versions)


def verification(profile, spanish=False):
    level = str(profile.get("verification", "")).strip()
    tablet = profile.get("form_factor") == "tablet"
    if level == "device":
        tested = profile.get("tested") or []
        if tested:
            version = tested[0].get("android", "")
            text = (f"device, build Android {version} probado" if spanish
                    else f"device, tested Android {version} build")
        else:
            text = "device"
    elif level == "reference":
        text = "reference, sin auto-apply" if spanish else "reference, no auto-apply"
    else:
        text = "documented, solo preguntar" if spanish else "documented, ask only"
    return f"{text}, tablet" if tablet else text


def row_catalog(rel, profile):
    level = str(profile.get("verification", "")).strip()
    if level == "device":
        tested = profile.get("tested") or []
        if tested:
            notes = (f"Tested on Android {tested[0].get('android','')} "
                     f"(`{tested[0].get('build','')}`); auto-apply only on that build.")
        else:
            notes = "Tested on a physical phone."
    elif level == "reference":
        notes = "Reference only; no auto-apply."
    else:
        notes = (f"From the `{profile.get('codename','')}` firmware dump; "
                 "ask only, no auto-apply.")
    if profile.get("form_factor") == "tablet":
        notes = "Tablet; " + notes
    return (f"| `{profile['id']}` | {display(profile)} | {android_text(profile)} | "
            f"{level} | {notes} |")


def summary_rows(rows, spanish=False):
    lines = []
    for brand in BRANDS:
        values = [profile for _, _, profile in rows if profile.get("brand") == brand]
        if not values:
            continue
        device = sum(1 for profile in values if profile.get("verification") == "device")
        tablets = sum(1 for profile in values if profile.get("form_factor") == "tablet")
        lines.append(f"| **{brand}** | {len(values)} | {device} | {tablets} |")
    generic = sum(1 for _, _, profile in rows if profile.get("generic") is True)
    if generic:
        lines.append(f"| **{'Generic' if not spanish else 'Genérico'}** | {generic} | 0 | 0 |")
    return lines


def full_table(rows):
    return [row_catalog(rel, profile) for _, rel, profile in rows]


def replace_full_table(text, marker, header, rows):
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(marker):
            end = index + 2
            while end < len(lines) and lines[end].startswith("|"):
                end += 1
            return "\n".join(lines[:index + 2] + rows + lines[end:]) + ("\n" if text.endswith("\n") else "")
    return text


def replace_summary_table(text, marker, header, rows):
    pattern = re.compile(
        re.escape(marker) + r"\n\|(?:---\|)+\n(?:\|.*\n)+"
    )
    block = marker + "\n" + header + "\n" + "\n".join(rows) + "\n"
    return pattern.sub(block, text, count=1)


def replace_tree(text, entries):
    block = "```text\nprofiles/\n" + "\n".join(entries) + "\n```"
    return re.sub(r"```text\nprofiles/\n.*?\n```", block, text, count=1, flags=re.S)


def main():
    argparse.ArgumentParser(
        description="Rebuild the profile catalog and documentation tables."
    ).parse_args()
    rows = load()
    catalog_key = re.compile(r"^\| `([^`]+)`")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme = replace_summary_table(
        readme,
        "| Brand | Profiles | Device-tested | Tablets |",
        "|---|---|---|---|",
        summary_rows(rows),
    )
    (ROOT / "README.md").write_text(readme, encoding="utf-8")

    readme_es = (ROOT / "README.es.md").read_text(encoding="utf-8")
    readme_es = replace_summary_table(
        readme_es,
        "| Marca | Perfiles | Probados en móvil | Tablets |",
        "|---|---|---|---|",
        summary_rows(rows, spanish=True),
    )
    (ROOT / "README.es.md").write_text(readme_es, encoding="utf-8")

    catalog = (PROFILES / "README.md").read_text(encoding="utf-8")
    old_cat = {}
    lines = catalog.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("| ID | Model | Android | Verification | Notes |"):
            for row in lines[index + 2:]:
                if not row.startswith("|"):
                    break
                match = catalog_key.search(row)
                if match:
                    old_cat[match.group(1)] = row
            break
    new_cat = [old_cat.get(profile["id"]) or row_catalog(rel, profile) for _, rel, profile in rows]
    catalog = replace_full_table(catalog, "| ID | Model | Android | Verification | Notes |",
                                 "|---|---|---|---|---|", new_cat)

    entries = ["\u251c\u2500\u2500 schema.json"]
    for group in sorted({rel.split("/")[0] for _, rel, _ in rows}, key=lambda item: ORDER.get(item, 9)):
        group_rows = sorted([rel for _, rel, _ in rows if rel.startswith(group + "/")])
        if group == "oneplus":
            group_rows = ["oneplus/README.md"] + group_rows
        entries.extend("\u251c\u2500\u2500 " + rel for rel in group_rows)
    entries[-1] = "\u2514\u2500\u2500 " + entries[-1][4:]
    catalog = replace_tree(catalog, entries)
    (PROFILES / "README.md").write_text(catalog, encoding="utf-8")

    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    doc = ["# Profile catalog", "",
           f"CleanYourPhone ships **{len(rows)} profiles** across six brands. A `device` profile was",
           "tested on a real phone and can auto-apply only on the build listed in `tested`. A",
           "`documented` profile comes from a primary firmware dump, never auto-applies and only asks.",
           "", "| Brand | Profiles | Device-tested | Tablets |", "|---|---|---|---|"]
    doc += summary_rows(rows)
    doc += ["", "## Full catalog", "",
            "| ID | Model | Android | Verification | Notes |", "|---|---|---|---|---|"]
    doc += full_table(rows)
    (docs / "PROFILES.md").write_text("\n".join(doc) + "\n", encoding="utf-8")
    print(f"updated docs for {len(rows)} profiles")


if __name__ == "__main__":
    main()
