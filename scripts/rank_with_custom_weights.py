#!/usr/bin/env python3
"""Rank alternatives using user-provided scenario weights."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.simulate_alternatives import (  # noqa: E402
    CRITERIA,
    DEFAULT_DATA,
    DEFAULT_RESULTS,
    deterministic_rankings,
    load_data,
    validate_data,
    write_csv,
)


DEFAULT_WEIGHTS = ROOT / "examples" / "custom_weights.example.json"


def load_custom_scenarios(path: Path) -> dict[str, dict[str, float]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    scenarios = raw.get("scenarios")
    if not isinstance(scenarios, dict) or not scenarios:
        raise ValueError("weights file must contain a non-empty 'scenarios' object")

    parsed: dict[str, dict[str, float]] = {}
    for scenario, weights in scenarios.items():
        if not isinstance(weights, dict):
            raise ValueError(f"{scenario} weights must be an object")
        missing = set(CRITERIA) - set(weights)
        extra = set(weights) - set(CRITERIA)
        if missing:
            raise ValueError(f"{scenario} missing weights: {sorted(missing)}")
        if extra:
            raise ValueError(f"{scenario} has unknown weights: {sorted(extra)}")
        parsed_weights = {
            criterion: float(weights[criterion])
            for criterion in CRITERIA
        }
        if sum(parsed_weights.values()) <= 0:
            raise ValueError(f"{scenario} weights must sum to a positive value")
        if any(value < 0 for value in parsed_weights.values()):
            raise ValueError(f"{scenario} weights must be non-negative")
        parsed[scenario] = parsed_weights
    return parsed


def custom_ranking_rows(
    data_path: Path,
    weights_path: Path,
) -> list[dict[str, Any]]:
    _raw_data, alternatives = load_data(data_path)
    validate_data(alternatives)
    scenarios = load_custom_scenarios(weights_path)
    rankings = deterministic_rankings(alternatives, scenarios)
    return [
        row
        for rows in rankings.values()
        for row in rows
    ]


def write_custom_rankings(rows: list[dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_csv(
        output_path,
        rows,
        ["scenario", "rank", "alternative_id", "alternative", "score"],
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--weights", type=Path, default=DEFAULT_WEIGHTS)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_RESULTS / "custom_weights_example_rankings.csv",
    )
    args = parser.parse_args()

    rows = custom_ranking_rows(args.data, args.weights)
    write_custom_rankings(rows, args.output)
    scenarios = sorted({row["scenario"] for row in rows})
    print(f"wrote custom rankings for {len(scenarios)} scenarios")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
