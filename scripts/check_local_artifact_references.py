#!/usr/bin/env python3
"""Check local artifact references in Markdown files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.simulate_alternatives import write_csv  # noqa: E402

DEFAULT_RESULTS = ROOT / "results"
REFERENCE_RE = re.compile(
    r"\b(?:data|results|scripts|reports|templates|examples|ci|tests|assets)/[A-Za-z0-9_./:-]+"
)
MARKDOWN_SOURCES = [
    ROOT / "README.md",
    *sorted((ROOT / "reports").glob("*.md")),
]


def normalize_reference(reference: str) -> str:
    return reference.rstrip(".,:;)]}")


def resolve_reference(source: Path, reference: str) -> Path:
    if reference.startswith("assets/"):
        return source.parent / reference
    return ROOT / reference


def reference_rows(sources: list[Path] = MARKDOWN_SOURCES) -> list[dict[str, Any]]:
    rows = []
    seen: set[tuple[str, str]] = set()
    for source in sources:
        text = source.read_text(encoding="utf-8")
        for match in REFERENCE_RE.finditer(text):
            reference = normalize_reference(match.group(0))
            key = (str(source.relative_to(ROOT)), reference)
            if key in seen:
                continue
            seen.add(key)
            resolved = resolve_reference(source, reference)
            exists = resolved.exists()
            rows.append({
                "source_file": str(source.relative_to(ROOT)).replace("\\", "/"),
                "reference": reference,
                "resolved_path": str(resolved.relative_to(ROOT)).replace("\\", "/")
                if resolved.is_relative_to(ROOT)
                else str(resolved),
                "exists": exists,
            })
    rows.sort(key=lambda row: (row["source_file"], row["reference"]))
    return rows


def write_reference_check(rows: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        output_dir / "local_artifact_reference_check.csv",
        rows,
        ["source_file", "reference", "resolved_path", "exists"],
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_RESULTS)
    args = parser.parse_args()

    rows = reference_rows()
    write_reference_check(rows, args.output_dir)
    missing = [row for row in rows if not row["exists"]]
    print(f"checked {len(rows)} local artifact references; missing: {len(missing)}")
    if missing:
        for row in missing:
            print(f"missing {row['reference']} in {row['source_file']}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
