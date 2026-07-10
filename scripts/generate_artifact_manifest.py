#!/usr/bin/env python3
"""Generate a SHA-256 manifest for repository artifacts."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.simulate_alternatives import DEFAULT_RESULTS, write_csv  # noqa: E402


INCLUDED_DIRS = [".github", "ci", "data", "docs", "examples", "reports", "results", "scripts", "templates", "tests"]
EXCLUDED_SUFFIXES = {".pyc"}
EXCLUDED_PATHS = {"results/artifact_manifest.csv"}
EXCLUDED_DIR_NAMES = {"__pycache__", "coverage", "dist", "node_modules"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_paths() -> list[Path]:
    paths: list[Path] = [ROOT / "README.md"]
    for dirname in INCLUDED_DIRS:
        directory = ROOT / dirname
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            relative_path = path.relative_to(ROOT)
            relative = str(relative_path).replace("\\", "/")
            if (
                path.is_file()
                and not EXCLUDED_DIR_NAMES.intersection(relative_path.parts)
                and path.suffix not in EXCLUDED_SUFFIXES
                and relative not in EXCLUDED_PATHS
            ):
                paths.append(path)
    return sorted(set(paths), key=lambda path: str(path.relative_to(ROOT)).replace("\\", "/"))


def manifest_rows() -> list[dict[str, Any]]:
    rows = []
    for path in artifact_paths():
        relative = str(path.relative_to(ROOT)).replace("\\", "/")
        rows.append({
            "path": relative,
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        })
    return rows


def write_manifest(rows: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        output_dir / "artifact_manifest.csv",
        rows,
        ["path", "size_bytes", "sha256"],
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_RESULTS)
    args = parser.parse_args()

    rows = manifest_rows()
    write_manifest(rows, args.output_dir)
    print(f"wrote {len(rows)} artifact manifest rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
