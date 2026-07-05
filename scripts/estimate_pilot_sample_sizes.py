#!/usr/bin/env python3
"""Estimate pilot task counts needed to separate close candidates."""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.simulate_alternatives import (  # noqa: E402
    SCENARIOS,
    deterministic_rankings,
    load_data,
    validate_data,
    write_csv,
)


DEFAULT_MODEL = ROOT / "data" / "pilot_sample_size_model.json"
DEFAULT_RESULTS = ROOT / "results"
DEFAULT_REPORT = ROOT / "reports" / "pilot_sample_size.md"


def load_model(path: Path = DEFAULT_MODEL) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def score_to_success_rate(score: float, model: dict[str, Any]) -> float:
    limits = model["score_to_success_rate"]
    floor = float(limits["floor"])
    ceiling = float(limits["ceiling"])
    return floor + (score / 5.0) * (ceiling - floor)


def simulate_pair(
    top_rate: float,
    comparison_rate: float,
    tasks_per_candidate: int,
    trials: int,
    rng: random.Random,
) -> tuple[float, float]:
    top_wins = 0
    ties = 0
    for _ in range(trials):
        top_successes = sum(
            1
            for _task in range(tasks_per_candidate)
            if rng.random() < top_rate
        )
        comparison_successes = sum(
            1
            for _task in range(tasks_per_candidate)
            if rng.random() < comparison_rate
        )
        if top_successes > comparison_successes:
            top_wins += 1
        elif top_successes == comparison_successes:
            ties += 1
    return top_wins / trials, ties / trials


def recommendation(win_probability: float, tie_probability: float, target: float) -> str:
    if win_probability >= target:
        return "Enough for directional separation"
    if win_probability + tie_probability >= target:
        return "Likely tie cluster; add qualitative review"
    return "Increase tasks or treat as unresolved"


def estimate_rows(model: dict[str, Any]) -> list[dict[str, Any]]:
    _raw, alternatives = load_data()
    validate_data(alternatives)
    rankings = deterministic_rankings(alternatives)
    rng = random.Random(int(model["seed"]))
    trials = int(model["simulation_trials"])
    target = float(model["decision_confidence_target"])
    rows = []
    for scenario in SCENARIOS:
        scenario_rows = rankings[scenario]
        top = scenario_rows[0]
        top_rate = score_to_success_rate(float(top["score"]), model)
        for comparison_rank in model["comparison_ranks"]:
            comparison = scenario_rows[int(comparison_rank) - 1]
            comparison_rate = score_to_success_rate(float(comparison["score"]), model)
            for task_count in model["task_counts_per_candidate"]:
                win_probability, tie_probability = simulate_pair(
                    top_rate,
                    comparison_rate,
                    int(task_count),
                    trials,
                    rng,
                )
                rows.append({
                    "scenario": scenario,
                    "top_candidate": top["alternative"],
                    "comparison_rank": comparison_rank,
                    "comparison_candidate": comparison["alternative"],
                    "score_gap": float(top["score"]) - float(comparison["score"]),
                    "estimated_top_success_rate": top_rate,
                    "estimated_comparison_success_rate": comparison_rate,
                    "tasks_per_candidate": task_count,
                    "simulation_trials": trials,
                    "top_wins_probability": win_probability,
                    "tie_probability": tie_probability,
                    "decision_confidence_target": target,
                    "recommendation": recommendation(win_probability, tie_probability, target),
                })
    return rows


def recommended_task_counts(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary_rows = []
    grouped: dict[tuple[str, int, str], list[dict[str, Any]]] = {}
    for row in rows:
        key = (
            row["scenario"],
            int(row["comparison_rank"]),
            row["comparison_candidate"],
        )
        grouped.setdefault(key, []).append(row)
    for (scenario, comparison_rank, comparison_candidate), group_rows in grouped.items():
        group_rows.sort(key=lambda row: int(row["tasks_per_candidate"]))
        enough = [
            row
            for row in group_rows
            if float(row["top_wins_probability"]) >= float(row["decision_confidence_target"])
        ]
        chosen = enough[0] if enough else group_rows[-1]
        summary_rows.append({
            "scenario": scenario,
            "comparison_rank": comparison_rank,
            "comparison_candidate": comparison_candidate,
            "recommended_tasks_per_candidate": chosen["tasks_per_candidate"] if enough else f">{chosen['tasks_per_candidate']}",
            "top_wins_probability": chosen["top_wins_probability"],
            "tie_probability": chosen["tie_probability"],
            "recommendation": chosen["recommendation"],
        })
    summary_rows.sort(key=lambda row: (row["scenario"], row["comparison_rank"]))
    return summary_rows


def build_report(model: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    summary_rows = recommended_task_counts(rows)
    lines = [
        "# Pilot Sample Size Estimate",
        "",
        "Date: 2026-07-05",
        "",
        "This appendix estimates how many pilot tasks per candidate are needed to distinguish close shortlist candidates. It is a planning simulation, not proof of live performance. The model maps the 0-5 scenario simulation score to an assumed task success rate, then simulates observed wins across repeated pilot task sets.",
        "",
        "Inputs: `data/pilot_sample_size_model.json` and `data/alternatives.json`. Generated output: `results/pilot_sample_size_estimates.csv`.",
        "",
        "## Assumptions",
        "",
        "| Assumption | Value |",
        "|---|---:|",
        f"| Success-rate floor | {model['score_to_success_rate']['floor']} |",
        f"| Success-rate ceiling | {model['score_to_success_rate']['ceiling']} |",
        f"| Simulation trials per comparison | {model['simulation_trials']} |",
        f"| Decision confidence target | {model['decision_confidence_target']} |",
        "",
        "## Recommended Task Counts",
        "",
        "| Scenario | Comparison | Recommended tasks/candidate | Top win probability | Tie probability | Recommendation |",
        "|---|---|---:|---:|---:|---|",
    ]
    for row in summary_rows:
        lines.append(
            "| {scenario} | Rank {rank}: {candidate} | {tasks} | {win:.3f} | {tie:.3f} | {recommendation} |".format(
                scenario=row["scenario"],
                rank=row["comparison_rank"],
                candidate=row["comparison_candidate"],
                tasks=row["recommended_tasks_per_candidate"],
                win=float(row["top_wins_probability"]),
                tie=float(row["tie_probability"]),
                recommendation=row["recommendation"],
            )
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "- Close deterministic scores usually require more tasks than a two-week pilot can comfortably run. If the model recommends more than 60 tasks per candidate, treat the candidates as a tie cluster and rely on qualitative review, safety gates, and operational fit.",
        "- Task-count estimates assume the task suite is balanced and comparable across candidates. Reusing the same task distribution from `data/pilot_tasks.json` matters more than increasing raw volume with unrepresentative tasks.",
        "- Replace the score-to-success mapping with measured pilot pass rates after the first pilot wave. At that point, this model becomes a recalibration tool rather than a desk-review estimate.",
        "",
    ])
    return "\n".join(lines).rstrip() + "\n"


def write_outputs(
    rows: list[dict[str, Any]],
    output_dir: Path,
    report_output: Path,
    model: dict[str, Any],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    write_csv(
        output_dir / "pilot_sample_size_estimates.csv",
        rows,
        [
            "scenario",
            "top_candidate",
            "comparison_rank",
            "comparison_candidate",
            "score_gap",
            "estimated_top_success_rate",
            "estimated_comparison_success_rate",
            "tasks_per_candidate",
            "simulation_trials",
            "top_wins_probability",
            "tie_probability",
            "decision_confidence_target",
            "recommendation",
        ],
    )
    report_output.write_text(
        build_report(model, rows),
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    model = load_model(args.model)
    rows = estimate_rows(model)
    write_outputs(rows, args.output_dir, args.report_output, model)
    print(f"wrote {len(rows)} pilot sample-size rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
