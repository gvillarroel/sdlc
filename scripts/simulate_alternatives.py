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

CATEGORY_GROUPS: dict[str, list[str]] = {
    "adoption_readiness": [
        "implementation_ease",
        "maturity",
        "deployment_flexibility"
    ],
    "agent_architecture": [
        "provider_portability",
        "persistence_memory",
        "multi_agent",
        "extensibility",
        "coding_fit"
    ],
    "execution_safety": [
        "sandbox_isolation",
        "human_control",
        "security_governance"
    ],
    "operations": [
        "ci_pr",
        "observability",
        "deployment_flexibility"
    ],
    "research_fit": [
        "research_reproducibility",
        "implementation_ease",
        "observability",
        "provider_portability"
    ]
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


def category_scores(alternatives: list[Alternative]) -> list[dict[str, Any]]:
    rows = []
    for alt in alternatives:
        for category, criteria in CATEGORY_GROUPS.items():
            score = statistics.fmean(alt.scores[criterion] for criterion in criteria)
            rows.append({
                "category": category,
                "alternative_id": alt.id,
                "alternative": alt.name,
                "score": score
            })
    rows.sort(key=lambda row: (row["category"], -row["score"], row["alternative"]))
    rank_by_category: dict[str, int] = {}
    for row in rows:
        category = row["category"]
        rank_by_category[category] = rank_by_category.get(category, 0) + 1
        row["rank"] = rank_by_category[category]
    return rows


def decision_shortlist(
    deterministic: dict[str, list[dict[str, Any]]],
    monte_carlo: dict[str, list[dict[str, Any]]],
    top_n: int = 5
) -> list[dict[str, Any]]:
    rows = []
    for scenario, deterministic_rows in deterministic.items():
        mc_by_id = {
            row["alternative_id"]: row
            for row in monte_carlo[scenario]
        }
        for row in deterministic_rows[:top_n]:
            mc_row = mc_by_id[row["alternative_id"]]
            rows.append({
                "scenario": scenario,
                "deterministic_rank": row["rank"],
                "alternative_id": row["alternative_id"],
                "alternative": row["alternative"],
                "deterministic_score": row["score"],
                "monte_carlo_mean_score": mc_row["mean_score"],
                "monte_carlo_mean_rank": mc_row["mean_rank"],
                "win_rate": mc_row["win_rate"],
                "top3_rate": mc_row["top3_rate"]
            })
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def scenario_weights_rows() -> list[dict[str, Any]]:
    rows = []
    for scenario, weights in SCENARIOS.items():
        total = sum(weights.values())
        for criterion, weight in weights.items():
            rows.append({
                "scenario": scenario,
                "criterion": criterion,
                "raw_weight": weight,
                "normalized_weight": weight / total
            })
    return rows


def criteria_definition_rows(raw_data: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "criterion": criterion,
            "definition": raw_data["criteria"][criterion]
        }
        for criterion in CRITERIA
    ]


def evidence_matrix_rows(raw_data: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for item in raw_data["alternatives"]:
        rows.append({
            "alternative_id": item["id"],
            "alternative": item["name"],
            "repo": item["repo"],
            "url": item["url"],
            "license": item["license"],
            "primary_language": item["primary_language"],
            "maturity_level": item["maturity_level"],
            "source_confidence": item["source_confidence"],
            "stars": item["stars"],
            "created_at": item["created_at"],
            "last_pushed_at": item["last_pushed_at"],
            "latest_release": item["latest_release"],
            "summary": item["summary"],
            "implementation_notes": item["implementation_notes"],
            "risk_notes": item["risk_notes"],
            "evidence_urls": "; ".join(item["evidence_urls"])
        })
    rows.sort(key=lambda row: row["alternative"].lower())
    return rows


def alternative_scorecard_rows(alternatives: list[Alternative]) -> list[dict[str, Any]]:
    rows = []
    for alt in alternatives:
        row: dict[str, Any] = {
            "alternative_id": alt.id,
            "alternative": alt.name,
            "license": alt.license,
            "maturity_level": alt.maturity_level,
            "source_confidence": alt.source_confidence
        }
        row.update({criterion: alt.scores[criterion] for criterion in CRITERIA})
        rows.append(row)
    rows.sort(key=lambda row: row["alternative"].lower())
    return rows


def regret_analysis_rows(
    deterministic: dict[str, list[dict[str, Any]]],
    monte_carlo: dict[str, list[dict[str, Any]]]
) -> list[dict[str, Any]]:
    rows = []
    for scenario, scenario_rows in deterministic.items():
        best_score = scenario_rows[0]["score"]
        mc_by_id = {
            row["alternative_id"]: row
            for row in monte_carlo[scenario]
        }
        for row in scenario_rows:
            mc_row = mc_by_id[row["alternative_id"]]
            rows.append({
                "scenario": scenario,
                "alternative_id": row["alternative_id"],
                "alternative": row["alternative"],
                "deterministic_rank": row["rank"],
                "deterministic_score": row["score"],
                "regret_vs_best": best_score - row["score"],
                "monte_carlo_mean_rank": mc_row["mean_rank"],
                "win_rate": mc_row["win_rate"],
                "top3_rate": mc_row["top3_rate"]
            })
    rows.sort(key=lambda row: (row["scenario"], row["regret_vs_best"], row["deterministic_rank"]))
    return rows


def dominates(candidate: Alternative, other: Alternative, criteria: list[str]) -> bool:
    at_least_as_good = all(candidate.scores[criterion] >= other.scores[criterion] for criterion in criteria)
    strictly_better = any(candidate.scores[criterion] > other.scores[criterion] for criterion in criteria)
    return at_least_as_good and strictly_better


def pareto_frontier_rows(alternatives: list[Alternative]) -> list[dict[str, Any]]:
    rows = []
    for alt in alternatives:
        dominated_by = [
            other.name
            for other in alternatives
            if other.id != alt.id and dominates(other, alt, CRITERIA)
        ]
        rows.append({
            "alternative_id": alt.id,
            "alternative": alt.name,
            "is_pareto_frontier": not dominated_by,
            "dominated_by_count": len(dominated_by),
            "dominated_by": "; ".join(dominated_by)
        })
    rows.sort(key=lambda row: (not row["is_pareto_frontier"], row["dominated_by_count"], row["alternative"]))
    return rows


def rank_stability_rows(
    deterministic: dict[str, list[dict[str, Any]]],
    monte_carlo: dict[str, list[dict[str, Any]]]
) -> list[dict[str, Any]]:
    scenario_count = len(deterministic)
    by_alt: dict[str, dict[str, Any]] = {}
    for scenario, rows in deterministic.items():
        mc_by_id = {
            row["alternative_id"]: row
            for row in monte_carlo[scenario]
        }
        for row in rows:
            entry = by_alt.setdefault(
                row["alternative_id"],
                {
                    "alternative_id": row["alternative_id"],
                    "alternative": row["alternative"],
                    "deterministic_ranks": [],
                    "top3_scenarios": 0,
                    "mean_rank_values": [],
                    "top3_rates": []
                }
            )
            entry["deterministic_ranks"].append(row["rank"])
            if row["rank"] <= 3:
                entry["top3_scenarios"] += 1
            entry["mean_rank_values"].append(mc_by_id[row["alternative_id"]]["mean_rank"])
            entry["top3_rates"].append(mc_by_id[row["alternative_id"]]["top3_rate"])
    rows = []
    for entry in by_alt.values():
        ranks = entry["deterministic_ranks"]
        rows.append({
            "alternative_id": entry["alternative_id"],
            "alternative": entry["alternative"],
            "mean_deterministic_rank": statistics.fmean(ranks),
            "best_deterministic_rank": min(ranks),
            "worst_deterministic_rank": max(ranks),
            "top3_scenarios": entry["top3_scenarios"],
            "top3_scenario_rate": entry["top3_scenarios"] / scenario_count,
            "mean_monte_carlo_rank": statistics.fmean(entry["mean_rank_values"]),
            "mean_top3_rate": statistics.fmean(entry["top3_rates"])
        })
    rows.sort(
        key=lambda row: (
            -row["top3_scenario_rate"],
            row["mean_deterministic_rank"],
            -row["mean_top3_rate"],
            row["alternative"]
        )
    )
    return rows


def write_outputs(
    raw_data: dict[str, Any],
    alternatives: list[Alternative],
    deterministic: dict[str, list[dict[str, Any]]],
    monte_carlo: dict[str, list[dict[str, Any]]],
    sensitivity: dict[str, list[dict[str, Any]]],
    categories: list[dict[str, Any]],
    shortlist: list[dict[str, Any]],
    regret: list[dict[str, Any]],
    pareto: list[dict[str, Any]],
    rank_stability: list[dict[str, Any]],
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
    write_csv(
        output_dir / "category_scores.csv",
        categories,
        ["category", "rank", "alternative_id", "alternative", "score"]
    )
    write_csv(
        output_dir / "decision_shortlist.csv",
        shortlist,
        [
            "scenario",
            "deterministic_rank",
            "alternative_id",
            "alternative",
            "deterministic_score",
            "monte_carlo_mean_score",
            "monte_carlo_mean_rank",
            "win_rate",
            "top3_rate"
        ]
    )
    write_csv(
        output_dir / "scenario_weights.csv",
        scenario_weights_rows(),
        ["scenario", "criterion", "raw_weight", "normalized_weight"]
    )
    write_csv(
        output_dir / "criteria_definitions.csv",
        criteria_definition_rows(raw_data),
        ["criterion", "definition"]
    )
    write_csv(
        output_dir / "evidence_matrix.csv",
        evidence_matrix_rows(raw_data),
        [
            "alternative_id",
            "alternative",
            "repo",
            "url",
            "license",
            "primary_language",
            "maturity_level",
            "source_confidence",
            "stars",
            "created_at",
            "last_pushed_at",
            "latest_release",
            "summary",
            "implementation_notes",
            "risk_notes",
            "evidence_urls"
        ]
    )
    write_csv(
        output_dir / "alternative_scorecards.csv",
        alternative_scorecard_rows(alternatives),
        [
            "alternative_id",
            "alternative",
            "license",
            "maturity_level",
            "source_confidence",
            *CRITERIA
        ]
    )
    write_csv(
        output_dir / "regret_analysis.csv",
        regret,
        [
            "scenario",
            "alternative_id",
            "alternative",
            "deterministic_rank",
            "deterministic_score",
            "regret_vs_best",
            "monte_carlo_mean_rank",
            "win_rate",
            "top3_rate"
        ]
    )
    write_csv(
        output_dir / "pareto_frontier.csv",
        pareto,
        [
            "alternative_id",
            "alternative",
            "is_pareto_frontier",
            "dominated_by_count",
            "dominated_by"
        ]
    )
    write_csv(
        output_dir / "rank_stability.csv",
        rank_stability,
        [
            "alternative_id",
            "alternative",
            "mean_deterministic_rank",
            "best_deterministic_rank",
            "worst_deterministic_rank",
            "top3_scenarios",
            "top3_scenario_rate",
            "mean_monte_carlo_rank",
            "mean_top3_rate"
        ]
    )
    with (output_dir / "all_results.json").open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(
            {
                "scenarios": SCENARIOS,
                "category_groups": CATEGORY_GROUPS,
                "deterministic_rankings": deterministic,
                "monte_carlo_summary": monte_carlo,
                "sensitivity_summary": sensitivity,
                "category_scores": categories,
                "decision_shortlist": shortlist,
                "scenario_weights": scenario_weights_rows(),
                "criteria_definitions": criteria_definition_rows(raw_data),
                "evidence_matrix": evidence_matrix_rows(raw_data),
                "alternative_scorecards": alternative_scorecard_rows(alternatives),
                "regret_analysis": regret,
                "pareto_frontier": pareto,
                "rank_stability": rank_stability
            },
            handle,
            indent=2
        )
        handle.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--trials", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=7331)
    args = parser.parse_args()

    raw_data, alternatives = load_data(args.data)
    validate_data(alternatives)
    deterministic = deterministic_rankings(alternatives)
    monte_carlo = run_monte_carlo(alternatives, trials=args.trials, seed=args.seed)
    sensitivity = sensitivity_summary(alternatives)
    categories = category_scores(alternatives)
    shortlist = decision_shortlist(deterministic, monte_carlo)
    regret = regret_analysis_rows(deterministic, monte_carlo)
    pareto = pareto_frontier_rows(alternatives)
    rank_stability = rank_stability_rows(deterministic, monte_carlo)
    write_outputs(
        raw_data,
        alternatives,
        deterministic,
        monte_carlo,
        sensitivity,
        categories,
        shortlist,
        regret,
        pareto,
        rank_stability,
        args.output_dir
    )

    for scenario, rows in deterministic.items():
        top = rows[0]
        print(f"{scenario}: {top['alternative']} ({top['score']:.3f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
