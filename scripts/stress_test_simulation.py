#!/usr/bin/env python3
"""Stress-test the ranking model against plausible assumption shifts."""

from __future__ import annotations

import argparse
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.simulate_alternatives import (  # noqa: E402
    Alternative,
    SCENARIOS,
    clamp,
    deterministic_rankings,
    load_data,
    run_monte_carlo,
    validate_data,
    write_csv,
)


DEFAULT_RESULTS = ROOT / "results"


DETERMINISTIC_STRESS_CASES: list[dict[str, Any]] = [
    {
        "id": "baseline",
        "description": "Base analyst scores and scenario weights.",
        "weight_multipliers": {},
        "score_adjustment": None,
    },
    {
        "id": "security_strict",
        "description": "Security, sandboxing, approvals, and PR gates matter more.",
        "weight_multipliers": {
            "sandbox_isolation": 2.0,
            "security_governance": 1.8,
            "human_control": 1.4,
            "ci_pr": 1.2,
        },
        "score_adjustment": None,
    },
    {
        "id": "provider_neutral",
        "description": "Provider portability and deployment flexibility dominate.",
        "weight_multipliers": {
            "provider_portability": 2.0,
            "deployment_flexibility": 1.4,
            "extensibility": 1.2,
        },
        "score_adjustment": None,
    },
    {
        "id": "fast_adoption",
        "description": "Short prototype timeline and daily developer ergonomics dominate.",
        "weight_multipliers": {
            "implementation_ease": 2.0,
            "maturity": 1.6,
            "human_control": 1.2,
            "coding_fit": 1.3,
            "persistence_memory": 0.7,
            "multi_agent": 0.7,
        },
        "score_adjustment": None,
    },
    {
        "id": "research_heavy",
        "description": "Reproducibility, observability, and explainability dominate.",
        "weight_multipliers": {
            "research_reproducibility": 2.5,
            "observability": 1.4,
            "implementation_ease": 1.3,
        },
        "score_adjustment": None,
    },
    {
        "id": "maturity_discount",
        "description": "Alpha and beta projects receive an explicit production-readiness discount.",
        "weight_multipliers": {},
        "score_adjustment": "maturity_discount",
    },
    {
        "id": "evidence_discount",
        "description": "Low-confidence source evidence receives an explicit score discount.",
        "weight_multipliers": {},
        "score_adjustment": "evidence_discount",
    },
    {
        "id": "sandbox_gate",
        "description": "Weak sandboxing also drags down governance, CI, deployment, and coding fit.",
        "weight_multipliers": {
            "sandbox_isolation": 1.7,
            "security_governance": 1.5,
        },
        "score_adjustment": "sandbox_gate",
    },
]


UNCERTAINTY_STRESS_CASES: list[dict[str, Any]] = [
    {
        "id": "baseline_uncertainty",
        "description": "Base Monte Carlo uncertainty.",
        "weight_sigma": 0.22,
        "score_sigma_multiplier": 1.0,
    },
    {
        "id": "low_uncertainty",
        "description": "Scores and weights are assumed more certain than the base model.",
        "weight_sigma": 0.12,
        "score_sigma_multiplier": 0.6,
    },
    {
        "id": "high_score_uncertainty",
        "description": "Analyst scores are much noisier, but scenario weights stay normal.",
        "weight_sigma": 0.22,
        "score_sigma_multiplier": 1.6,
    },
    {
        "id": "volatile_weights",
        "description": "Stakeholders disagree more strongly about scenario weights.",
        "weight_sigma": 0.40,
        "score_sigma_multiplier": 1.0,
    },
    {
        "id": "high_all_uncertainty",
        "description": "Both analyst scores and scenario weights are much noisier.",
        "weight_sigma": 0.40,
        "score_sigma_multiplier": 1.6,
    },
]


def stressed_scenarios(weight_multipliers: dict[str, float]) -> dict[str, dict[str, float]]:
    return {
        scenario: {
            criterion: weight * weight_multipliers.get(criterion, 1.0)
            for criterion, weight in weights.items()
        }
        for scenario, weights in SCENARIOS.items()
    }


def adjust_alternative_scores(alt: Alternative, adjustment: str | None) -> Alternative:
    if adjustment is None:
        return alt

    scores = dict(alt.scores)
    if adjustment == "maturity_discount":
        discount = {
            "production": 0.0,
            "beta": 0.25,
            "alpha": 0.60,
        }.get(alt.maturity_level, 0.35)
        scores = {criterion: clamp(score - discount) for criterion, score in scores.items()}
    elif adjustment == "evidence_discount":
        penalty = (1.0 - alt.source_confidence) * 1.2
        scores = {criterion: clamp(score - penalty) for criterion, score in scores.items()}
    elif adjustment == "sandbox_gate":
        sandbox_shortfall = max(0.0, 3.5 - scores["sandbox_isolation"])
        penalty = sandbox_shortfall * 0.6
        for criterion in [
            "security_governance",
            "ci_pr",
            "deployment_flexibility",
            "coding_fit",
        ]:
            scores[criterion] = clamp(scores[criterion] - penalty)
    else:
        raise ValueError(f"unknown score adjustment: {adjustment}")

    return replace(alt, scores=scores)


def adjusted_alternatives(
    alternatives: list[Alternative],
    adjustment: str | None,
) -> list[Alternative]:
    return [
        adjust_alternative_scores(alt, adjustment)
        for alt in alternatives
    ]


def top3_ids(rows: list[dict[str, Any]]) -> set[str]:
    return {row["alternative_id"] for row in rows[:3]}


def deterministic_stress_results(
    alternatives: list[Alternative],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    baseline = deterministic_rankings(alternatives)
    baseline_top = {
        scenario: rows[0]["alternative"]
        for scenario, rows in baseline.items()
    }
    baseline_top3 = {
        scenario: top3_ids(rows)
        for scenario, rows in baseline.items()
    }

    summary_rows: list[dict[str, Any]] = []
    ranking_rows: list[dict[str, Any]] = []

    for case in DETERMINISTIC_STRESS_CASES:
        case_alternatives = adjusted_alternatives(alternatives, case["score_adjustment"])
        case_scenarios = stressed_scenarios(case["weight_multipliers"])
        rankings = deterministic_rankings(case_alternatives, case_scenarios)

        for scenario, rows in rankings.items():
            top = rows[0]
            second = rows[1]
            third = rows[2]
            summary_rows.append({
                "stress_case": case["id"],
                "scenario": scenario,
                "description": case["description"],
                "rank1": top["alternative"],
                "rank2": second["alternative"],
                "rank3": third["alternative"],
                "baseline_rank1": baseline_top[scenario],
                "rank1_changed": top["alternative"] != baseline_top[scenario],
                "top3_overlap": len(top3_ids(rows) & baseline_top3[scenario]),
                "rank1_margin": top["score"] - second["score"],
            })
            for row in rows:
                ranking_rows.append({
                    "stress_case": case["id"],
                    "scenario": scenario,
                    "rank": row["rank"],
                    "alternative_id": row["alternative_id"],
                    "alternative": row["alternative"],
                    "score": row["score"],
                })

    return summary_rows, ranking_rows


def uncertainty_stress_results(
    alternatives: list[Alternative],
    trials: int,
    seed: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    baseline_rows = run_monte_carlo(
        alternatives,
        trials=trials,
        seed=seed,
        weight_sigma=UNCERTAINTY_STRESS_CASES[0]["weight_sigma"],
        score_sigma_multiplier=UNCERTAINTY_STRESS_CASES[0]["score_sigma_multiplier"],
    )
    baseline_top = {
        scenario: rows[0]["alternative"]
        for scenario, rows in baseline_rows.items()
    }

    summary_rows: list[dict[str, Any]] = []
    detail_rows: list[dict[str, Any]] = []

    for case in UNCERTAINTY_STRESS_CASES:
        rows_by_scenario = run_monte_carlo(
            alternatives,
            trials=trials,
            seed=seed,
            weight_sigma=case["weight_sigma"],
            score_sigma_multiplier=case["score_sigma_multiplier"],
        )
        for scenario, rows in rows_by_scenario.items():
            top = rows[0]
            second = rows[1]
            summary_rows.append({
                "uncertainty_case": case["id"],
                "scenario": scenario,
                "description": case["description"],
                "weight_sigma": case["weight_sigma"],
                "score_sigma_multiplier": case["score_sigma_multiplier"],
                "rank1": top["alternative"],
                "rank2": second["alternative"],
                "baseline_rank1": baseline_top[scenario],
                "rank1_changed": top["alternative"] != baseline_top[scenario],
                "win_rate": top["win_rate"],
                "top3_rate": top["top3_rate"],
                "win_rate_margin": top["win_rate"] - second["win_rate"],
                "trials": trials,
            })
            for row in rows:
                detail_rows.append({
                    "uncertainty_case": case["id"],
                    "scenario": scenario,
                    "alternative_id": row["alternative_id"],
                    "alternative": row["alternative"],
                    "mean_score": row["mean_score"],
                    "mean_rank": row["mean_rank"],
                    "win_rate": row["win_rate"],
                    "top3_rate": row["top3_rate"],
                    "trials": row["trials"],
                })

    return summary_rows, detail_rows


def write_stress_outputs(
    deterministic_summary: list[dict[str, Any]],
    deterministic_rankings_rows: list[dict[str, Any]],
    uncertainty_summary: list[dict[str, Any]],
    uncertainty_details: list[dict[str, Any]],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        output_dir / "stress_test_summary.csv",
        deterministic_summary,
        [
            "stress_case",
            "scenario",
            "description",
            "rank1",
            "rank2",
            "rank3",
            "baseline_rank1",
            "rank1_changed",
            "top3_overlap",
            "rank1_margin",
        ],
    )
    write_csv(
        output_dir / "stress_test_rankings.csv",
        deterministic_rankings_rows,
        [
            "stress_case",
            "scenario",
            "rank",
            "alternative_id",
            "alternative",
            "score",
        ],
    )
    write_csv(
        output_dir / "uncertainty_stress_summary.csv",
        uncertainty_summary,
        [
            "uncertainty_case",
            "scenario",
            "description",
            "weight_sigma",
            "score_sigma_multiplier",
            "rank1",
            "rank2",
            "baseline_rank1",
            "rank1_changed",
            "win_rate",
            "top3_rate",
            "win_rate_margin",
            "trials",
        ],
    )
    write_csv(
        output_dir / "uncertainty_stress_details.csv",
        uncertainty_details,
        [
            "uncertainty_case",
            "scenario",
            "alternative_id",
            "alternative",
            "mean_score",
            "mean_rank",
            "win_rate",
            "top3_rate",
            "trials",
        ],
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=ROOT / "data" / "alternatives.json")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--trials", type=int, default=1500)
    parser.add_argument("--seed", type=int, default=9011)
    args = parser.parse_args()

    _raw_data, alternatives = load_data(args.data)
    validate_data(alternatives)

    deterministic_summary, deterministic_rows = deterministic_stress_results(alternatives)
    uncertainty_summary, uncertainty_rows = uncertainty_stress_results(
        alternatives,
        trials=args.trials,
        seed=args.seed,
    )
    write_stress_outputs(
        deterministic_summary,
        deterministic_rows,
        uncertainty_summary,
        uncertainty_rows,
        args.output_dir,
    )

    changed = sum(1 for row in deterministic_summary if row["rank1_changed"])
    uncertain_changed = sum(1 for row in uncertainty_summary if row["rank1_changed"])
    print(f"deterministic stress rank-1 changes: {changed}")
    print(f"uncertainty stress rank-1 changes: {uncertain_changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
