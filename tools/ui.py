"""Small output helpers shared by the CleanYourPhone CLI."""

from __future__ import annotations

import json
import sys
from typing import Any, Iterable, List, Sequence


def die(message: str, code: int = 2) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(code)


def warn(message: str) -> None:
    print(f"warning: {message}", file=sys.stderr)


def print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def print_table(headers: Sequence[str], rows: Iterable[Sequence[Any]]) -> None:
    rows = [[str(cell) for cell in row] for row in rows]
    if not rows:
        print("(none)")
        return
    widths: List[int] = [len(header) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            if index < len(widths):
                widths[index] = max(widths[index], len(cell))
    print("  ".join(header.ljust(widths[index]) for index, header in enumerate(headers)))
    print("  ".join("-" * width for width in widths))
    for row in rows:
        print("  ".join(cell.ljust(widths[index]) for index, cell in enumerate(row)))
