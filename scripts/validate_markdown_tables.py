#!/usr/bin/env python3
"""Validate Markdown table column consistency in README and reports."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.simulate_alternatives import write_csv  # noqa: E402


DEFAULT_RESULTS = ROOT / "results"
TABLE_SEPARATOR_RE = re.compile(r"^:?-{3,}:?$")


def markdown_sources() -> list[Path]:
    completed = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "-z",
            "*.md",
        ],
        check=True,
        capture_output=True,
    )
    relative_paths = [os.fsdecode(item) for item in completed.stdout.split(b"\0") if item]
    return sorted(
        (ROOT / relative for relative in relative_paths if (ROOT / relative).is_file()),
        key=lambda path: path.as_posix(),
    )


def table_cells(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def is_separator(line: str) -> bool:
    cells = table_cells(line)
    return bool(cells) and all(TABLE_SEPARATOR_RE.match(cell) for cell in cells)


def validate_file(path: Path) -> list[dict[str, Any]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    rows = []
    index = 0
    while index < len(lines) - 1:
        header = table_cells(lines[index])
        if not header or not is_separator(lines[index + 1]):
            index += 1
            continue

        expected = len(header)
        table_start = index + 1
        row_count = 1
        bad_rows = []
        index += 2
        while index < len(lines):
            cells = table_cells(lines[index])
            if not cells:
                break
            row_count += 1
            if len(cells) != expected:
                bad_rows.append(f"line {index + 1}: expected {expected}, found {len(cells)}")
            index += 1
        rows.append({
            "source_file": str(path.relative_to(ROOT)).replace("\\", "/"),
            "start_line": table_start,
            "rows_checked": row_count,
            "expected_columns": expected,
            "ok": not bad_rows,
            "message": "; ".join(bad_rows),
        })
    return rows


def validation_rows() -> list[dict[str, Any]]:
    rows = []
    for path in markdown_sources():
        rows.extend(validate_file(path))
    rows.sort(key=lambda row: (row["source_file"], int(row["start_line"])))
    return rows


def write_outputs(rows: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        output_dir / "markdown_table_check.csv",
        rows,
        [
            "source_file",
            "start_line",
            "rows_checked",
            "expected_columns",
            "ok",
            "message",
        ],
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_RESULTS)
    args = parser.parse_args()

    rows = validation_rows()
    write_outputs(rows, args.output_dir)
    failures = [row for row in rows if not row["ok"]]
    print(f"checked {len(rows)} markdown tables; failures={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
