#!/usr/bin/env python3
"""Generate a permissive-license audit for evaluated and excluded alternatives."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "alternatives.json"
DEFAULT_OUTPUT = ROOT / "results" / "license_audit.csv"
PERMISSIVE = {"MIT", "Apache-2.0"}


def license_audit_rows(data_path: Path = DEFAULT_DATA) -> list[dict[str, Any]]:
    raw = json.loads(data_path.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    for item in raw["alternatives"]:
        permissive = item["license"] in PERMISSIVE
        rows.append({
            "alternative": item["name"],
            "status": "included" if permissive else "excluded",
            "license": item["license"],
            "is_permissive": permissive,
            "repo": item["repo"],
            "url": item["url"],
            "reason": "Permissive OSS license accepted by this evaluation." if permissive else "License failed permissive OSS filter."
        })
    for item in raw["excluded"]:
        rows.append({
            "alternative": item["name"],
            "status": "excluded",
            "license": "not accepted for this evaluation",
            "is_permissive": False,
            "repo": "",
            "url": "",
            "reason": item["reason"]
        })
    rows.sort(key=lambda row: (row["status"], row["alternative"].lower()))
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "alternative",
                "status",
                "license",
                "is_permissive",
                "repo",
                "url",
                "reason"
            ],
            lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    rows = license_audit_rows(args.data)
    write_csv(args.output, rows)
    included = sum(1 for row in rows if row["status"] == "included")
    excluded = len(rows) - included
    print(f"included={included} excluded={excluded}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
