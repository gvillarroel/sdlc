#!/usr/bin/env python3
"""Score post-pilot candidate summaries using the decision model."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = ROOT / "data" / "pilot_decision_model.json"
DEFAULT_INPUT = ROOT / "templates" / "pilot_candidate_summary.csv"
DEFAULT_OUTPUT = ROOT / "results" / "pilot_decision_scores.csv"


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def safe_rate(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return 0.0
    return numerator / denominator


def load_model(path: Path = DEFAULT_MODEL) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_input(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def score_row(row: dict[str, str], model: dict[str, Any]) -> dict[str, Any]:
    weights = model["weights"]
    gates = model["gates"]

    attempted = float(row["attempted_tasks"])
    successful = float(row["successful_tasks"])
    reviewed = float(row["reviewed_diffs"])
    accepted = float(row["accepted_diffs"])
    safety_failures = int(float(row["safety_failures"]))
    complete_artifacts = float(row["artifact_complete_runs"])

    task_success_rate = clamp(safe_rate(successful, attempted))
    review_acceptance_rate = clamp(safe_rate(accepted, reviewed))
    artifact_completeness = clamp(safe_rate(complete_artifacts, attempted))
    safety_score = 1.0 if safety_failures == 0 else 0.0
    cost_latency_score = clamp(float(row["cost_latency_score"]))
    setup_maintenance_score = clamp(float(row["setup_maintenance_score"]))

    final_score = 100.0 * (
        task_success_rate * weights["task_success"]
        + review_acceptance_rate * weights["review_acceptance"]
        + safety_score * weights["safety"]
        + artifact_completeness * weights["observability"]
        + cost_latency_score * weights["cost_latency"]
        + setup_maintenance_score * weights["setup_maintenance"]
    )

    gate_failures = []
    if safety_failures > gates["max_safety_failures"]:
        gate_failures.append("safety_failures")
    if task_success_rate < gates["minimum_task_success_rate"]:
        gate_failures.append("task_success_rate")
    if review_acceptance_rate < gates["minimum_review_acceptance_rate"]:
        gate_failures.append("review_acceptance_rate")
    if artifact_completeness < gates["minimum_artifact_completeness"]:
        gate_failures.append("artifact_completeness")

    return {
        "candidate": row["candidate"],
        "final_score": round(final_score, 2),
        "eligible": not gate_failures,
        "gate_failures": "; ".join(gate_failures),
        "task_success_rate": round(task_success_rate, 4),
        "review_acceptance_rate": round(review_acceptance_rate, 4),
        "safety_score": round(safety_score, 4),
        "artifact_completeness": round(artifact_completeness, 4),
        "cost_latency_score": round(cost_latency_score, 4),
        "setup_maintenance_score": round(setup_maintenance_score, 4),
        "notes": row.get("notes", "")
    }


def score_rows(rows: list[dict[str, str]], model: dict[str, Any]) -> list[dict[str, Any]]:
    scored = [score_row(row, model) for row in rows if row.get("candidate")]
    scored.sort(key=lambda row: (not row["eligible"], -row["final_score"], row["candidate"]))
    for rank, row in enumerate(scored, start=1):
        row["rank"] = rank
    return scored


def write_output(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "rank",
        "candidate",
        "final_score",
        "eligible",
        "gate_failures",
        "task_success_rate",
        "review_acceptance_rate",
        "safety_score",
        "artifact_completeness",
        "cost_latency_score",
        "setup_maintenance_score",
        "notes"
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    rows = score_rows(read_input(args.input), load_model(args.model))
    write_output(args.output, rows)
    print(f"scored={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
