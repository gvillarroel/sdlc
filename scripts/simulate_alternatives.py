#!/usr/bin/env python3
"""Run deterministic and Monte Carlo scoring for OSS coding-agent alternatives."""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "alternatives.json"
DEFAULT_RESULTS = ROOT / "results"

CRITERIA = [
    "implementation_ease",
    "maturity",
    "provider_portability",
    "sandbox_isolation",
    "persistence_memory",
    "multi_agent",
    "human_control",
    "ci_pr",
    "observability",
    "security_governance",
    "extensibility",
    "deployment_flexibility",
    "coding_fit",
    "research_reproducibility"
]

PERMISSIVE_LICENSES = {"MIT", "Apache-2.0"}

SCENARIOS: dict[str, dict[str, float]] = {
    "custom_orchestrator_platform": {
        "implementation_ease": 0.9,
        "maturity": 0.8,
        "provider_portability": 1.1,
        "sandbox_isolation": 1.1,
        "persistence_memory": 1.0,
        "multi_agent": 1.2,
        "human_control": 0.6,
        "ci_pr": 0.8,
        "observability": 1.0,
        "security_governance": 1.0,
        "extensibility": 1.4,
        "deployment_flexibility": 1.1,
        "coding_fit": 1.0,
        "research_reproducibility": 0.6
    },
    "secure_autonomous_prs": {
        "implementation_ease": 0.6,
        "maturity": 1.0,
        "provider_portability": 0.6,
        "sandbox_isolation": 1.5,
        "persistence_memory": 0.7,
        "multi_agent": 0.8,
        "human_control": 1.0,
        "ci_pr": 1.4,
        "observability": 1.1,
        "security_governance": 1.5,
        "extensibility": 0.8,
        "deployment_flexibility": 1.0,
        "coding_fit": 1.2,
        "research_reproducibility": 0.6
    },
    "quick_local_coding": {
        "implementation_ease": 1.5,
        "maturity": 1.2,
        "provider_portability": 1.1,
        "sandbox_isolation": 0.5,
        "persistence_memory": 0.6,
        "multi_agent": 0.4,
        "human_control": 1.2,
        "ci_pr": 0.7,
        "observability": 0.5,
        "security_governance": 0.7,
        "extensibility": 0.9,
        "deployment_flexibility": 0.9,
        "coding_fit": 1.5,
        "research_reproducibility": 0.5
    },
    "research_benchmarking": {
        "implementation_ease": 2.0,
        "maturity": 0.5,
        "provider_portability": 0.6,
        "sandbox_isolation": 0.4,
        "persistence_memory": 0.1,
        "multi_agent": 0.1,
        "human_control": 0.1,
        "ci_pr": 0.1,
        "observability": 0.6,
        "security_governance": 0.2,
        "extensibility": 0.5,
        "deployment_flexibility": 0.4,
        "coding_fit": 1.0,
        "research_reproducibility": 5.0
    },
    "enterprise_control_plane": {
        "implementation_ease": 0.7,
        "maturity": 1.2,
        "provider_portability": 1.1,
        "sandbox_isolation": 1.0,
        "persistence_memory": 1.0,
        "multi_agent": 1.2,
        "human_control": 1.1,
        "ci_pr": 1.0,
        "observability": 1.2,
        "security_governance": 1.4,
        "extensibility": 1.1,
        "deployment_flexibility": 1.2,
        "coding_fit": 1.0,
        "research_reproducibility": 0.4
    }
}

MATURITY_SIGMA = {
    "production": 0.25,
    "beta": 0.45,
    "alpha": 0.75
}


@dataclass(frozen=True)
class Alternative:
    id: str
    name: str
    license: str
    maturity_level: str
    source_confidence: float
    scores: dict[str, float]


def load_data(path: Path = DEFAULT_DATA) -> tuple[dict[str, Any], list[Alternative]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    alternatives = [
        Alternative(
            id=item["id"],
            name=item["name"],
            license=item["license"],
            maturity_level=item["maturity_level"],
            source_confidence=float(item["source_confidence"]),
            scores={criterion: float(item["scores"][criterion]) for criterion in CRITERIA}
        )
        for item in raw["alternatives"]
    ]
    return raw, alternatives


def validate_data(alternatives: Iterable[Alternative]) -> None:
    seen = set()
    for alt in alternatives:
        if alt.id in seen:
            raise ValueError(f"duplicate alternative id: {alt.id}")
        seen.add(alt.id)
        if alt.license not in PERMISSIVE_LICENSES:
            raise ValueError(f"{alt.name} is not permissive OSS: {alt.license}")
        if not 0 <= alt.source_confidence <= 1:
            raise ValueError(f"{alt.name} has invalid source_confidence")
        for criterion in CRITERIA:
            score = alt.scores.get(criterion)
            if score is None:
                raise ValueError(f"{alt.name} missing score for {criterion}")
            if not 0 <= score <= 5:
                raise ValueError(f"{alt.name}.{criterion}={score} outside 0..5")


def weighted_score(scores: dict[str, float], weights: dict[str, float]) -> float:
    total_weight = sum(weights.values())
    if total_weight <= 0:
        raise ValueError("scenario weights must sum to a positive value")
    return sum(scores[criterion] * weights[criterion] for criterion in CRITERIA) / total_weight


def deterministic_rankings(
    alternatives: list[Alternative],
    scenarios: dict[str, dict[str, float]] = SCENARIOS
) -> dict[str, list[dict[str, Any]]]:
    rankings: dict[str, list[dict[str, Any]]] = {}
    for scenario, weights in scenarios.items():
        rows = [
            {
                "scenario": scenario,
                "alternative_id": alt.id,
                "alternative": alt.name,
                "score": weighted_score(alt.scores, weights)
            }
            for alt in alternatives
        ]
        rows.sort(key=lambda row: row["score"], reverse=True)
        for index, row in enumerate(rows, start=1):
            row["rank"] = index
        rankings[scenario] = rows
    return rankings


def alt_sigma(alt: Alternative) -> float:
    maturity_sigma = MATURITY_SIGMA.get(alt.maturity_level, 0.6)
    confidence_penalty = (1.0 - alt.source_confidence) * 0.8
    return min(1.15, maturity_sigma + confidence_penalty)


def clamp(value: float, lower: float = 0.0, upper: float = 5.0) -> float:
    return max(lower, min(upper, value))


def perturb_weights(
    weights: dict[str, float],
    rng: random.Random,
    sigma: float
) -> dict[str, float]:
    perturbed = {
        criterion: weight * math.exp(rng.gauss(0.0, sigma))
        for criterion, weight in weights.items()
    }
    total = sum(perturbed.values())
    return {criterion: value / total for criterion, value in perturbed.items()}


def sample_scores(alt: Alternative, rng: random.Random) -> dict[str, float]:
    sigma = alt_sigma(alt)
    return {
        criterion: clamp(rng.gauss(score, sigma))
        for criterion, score in alt.scores.items()
    }


def percentile(values: list[float], pct: float) -> float:
    if not values:
        raise ValueError("percentile requires values")
    ordered = sorted(values)
    pos = (len(ordered) - 1) * pct
    lower = math.floor(pos)
    upper = math.ceil(pos)
    if lower == upper:
        return ordered[int(pos)]
    fraction = pos - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def run_monte_carlo(
    alternatives: list[Alternative],
    trials: int = 5000,
    seed: int = 7331,
    weight_sigma: float = 0.22,
    scenarios: dict[str, dict[str, float]] = SCENARIOS
) -> dict[str, list[dict[str, Any]]]:
    rng = random.Random(seed)
    summaries: dict[str, list[dict[str, Any]]] = {}
    for scenario, base_weights in scenarios.items():
        per_alt: dict[str, dict[str, Any]] = {
            alt.id: {
                "alternative": alt.name,
                "scores": [],
                "ranks": [],
                "wins": 0,
                "top3": 0
            }
            for alt in alternatives
        }

        for _ in range(trials):
            weights = perturb_weights(base_weights, rng, weight_sigma)
            rows = []
            for alt in alternatives:
                score = weighted_score(sample_scores(alt, rng), weights)
                rows.append((alt.id, score))
                per_alt[alt.id]["scores"].append(score)
            rows.sort(key=lambda item: item[1], reverse=True)
            for rank, (alt_id, _score) in enumerate(rows, start=1):
                per_alt[alt_id]["ranks"].append(rank)
                if rank == 1:
                    per_alt[alt_id]["wins"] += 1
                if rank <= 3:
                    per_alt[alt_id]["top3"] += 1

        summary_rows = []
        for alt in alternatives:
            values = per_alt[alt.id]
            score_values = values["scores"]
            rank_values = values["ranks"]
            summary_rows.append({
                "scenario": scenario,
                "alternative_id": alt.id,
                "alternative": alt.name,
                "mean_score": statistics.fmean(score_values),
                "p10_score": percentile(score_values, 0.10),
                "p90_score": percentile(score_values, 0.90),
                "mean_rank": statistics.fmean(rank_values),
                "win_rate": values["wins"] / trials,
                "top3_rate": values["top3"] / trials,
                "trials": trials
            })
        summary_rows.sort(key=lambda row: (row["win_rate"], row["top3_rate"], row["mean_score"]), reverse=True)
        summaries[scenario] = summary_rows
    return summaries


def sensitivity_summary(
    alternatives: list[Alternative],
    scenarios: dict[str, dict[str, float]] = SCENARIOS
) -> dict[str, list[dict[str, Any]]]:
    base = deterministic_rankings(alternatives, scenarios)
    output: dict[str, list[dict[str, Any]]] = {}
    for scenario, weights in scenarios.items():
        base_top3 = {row["alternative_id"] for row in base[scenario][:3]}
        rows = []
        for criterion in CRITERIA:
            half_weights = dict(weights)
            half_weights[criterion] *= 0.5
            double_weights = dict(weights)
            double_weights[criterion] *= 2.0
            half_ranking = deterministic_rankings(alternatives, {scenario: half_weights})[scenario]
            double_ranking = deterministic_rankings(alternatives, {scenario: double_weights})[scenario]
            rows.append({
                "scenario": scenario,
                "criterion": criterion,
                "base_top": base[scenario][0]["alternative"],
                "half_weight_top": half_ranking[0]["alternative"],
                "double_weight_top": double_ranking[0]["alternative"],
                "half_weight_top3_overlap": len(base_top3 & {row["alternative_id"] for row in half_ranking[:3]}),
                "double_weight_top3_overlap": len(base_top3 & {row["alternative_id"] for row in double_ranking[:3]})
            })
        output[scenario] = rows
    return output


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_outputs(
    deterministic: dict[str, list[dict[str, Any]]],
    monte_carlo: dict[str, list[dict[str, Any]]],
    sensitivity: dict[str, list[dict[str, Any]]],
    output_dir: Path = DEFAULT_RESULTS
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    deterministic_rows = [
        row
        for rows in deterministic.values()
        for row in rows
    ]
    monte_carlo_rows = [
        row
        for rows in monte_carlo.values()
        for row in rows
    ]
    sensitivity_rows = [
        row
        for rows in sensitivity.values()
        for row in rows
    ]

    write_csv(
        output_dir / "deterministic_rankings.csv",
        deterministic_rows,
        ["scenario", "rank", "alternative_id", "alternative", "score"]
    )
    write_csv(
        output_dir / "monte_carlo_summary.csv",
        monte_carlo_rows,
        [
            "scenario",
            "alternative_id",
            "alternative",
            "mean_score",
            "p10_score",
            "p90_score",
            "mean_rank",
            "win_rate",
            "top3_rate",
            "trials"
        ]
    )
    write_csv(
        output_dir / "sensitivity_summary.csv",
        sensitivity_rows,
        [
            "scenario",
            "criterion",
            "base_top",
            "half_weight_top",
            "double_weight_top",
            "half_weight_top3_overlap",
            "double_weight_top3_overlap"
        ]
    )
    (output_dir / "all_results.json").write_text(
        json.dumps(
            {
                "scenarios": SCENARIOS,
                "deterministic_rankings": deterministic,
                "monte_carlo_summary": monte_carlo,
                "sensitivity_summary": sensitivity
            },
            indent=2
        ),
        encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--trials", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=7331)
    args = parser.parse_args()

    _raw, alternatives = load_data(args.data)
    validate_data(alternatives)
    deterministic = deterministic_rankings(alternatives)
    monte_carlo = run_monte_carlo(alternatives, trials=args.trials, seed=args.seed)
    sensitivity = sensitivity_summary(alternatives)
    write_outputs(deterministic, monte_carlo, sensitivity, args.output_dir)

    for scenario, rows in deterministic.items():
        top = rows[0]
        print(f"{scenario}: {top['alternative']} ({top['score']:.3f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
