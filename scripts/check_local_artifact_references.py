#!/usr/bin/env python3
"""Check local artifact references in Markdown files."""

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
REFERENCE_RE = re.compile(
    r"(?:"
    r"\.github/[A-Za-z0-9_./:-]+\.[A-Za-z0-9_-]+"
    r"|\b(?:data|results|scripts|reports|templates|examples|tests|assets)/"
    r"[A-Za-z0-9_./:-]+\.[A-Za-z0-9_-]+"
    r"|docs/(?:assets|diagrams)/[A-Za-z0-9_./:-]+\.[A-Za-z0-9_-]+"
    r"|docs/(?:index\.html|\.nojekyll)"
    r")"
)


def markdown_sources(root: Path = ROOT) -> list[Path]:
    completed = subprocess.run(
        [
            "git",
            "-C",
            str(root),
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
        (root / relative for relative in relative_paths if (root / relative).is_file()),
        key=lambda path: path.as_posix(),
    )


MARKDOWN_SOURCES = markdown_sources()


def normalize_reference(reference: str) -> str:
    return reference.rstrip(".,:;)]}")


def resolve_reference(source: Path, reference: str) -> Path:
    if reference.startswith("assets/"):
        return source.parent / reference
    relative_candidate = source.parent / reference
    if source.parent != ROOT and relative_candidate.exists():
        return relative_candidate
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
