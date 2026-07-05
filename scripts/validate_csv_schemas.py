#!/usr/bin/env python3
"""Validate generated CSV headers against expected schemas."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.simulate_alternatives import CRITERIA, DEFAULT_RESULTS, write_csv  # noqa: E402


SCHEMAS: dict[str, list[str]] = {
    "deterministic_rankings.csv": ["scenario", "rank", "alternative_id", "alternative", "score"],
    "monte_carlo_summary.csv": ["scenario", "alternative_id", "alternative", "mean_score", "p10_score", "p90_score", "mean_rank", "win_rate", "top3_rate", "trials"],
    "sensitivity_summary.csv": ["scenario", "criterion", "base_top", "half_weight_top", "double_weight_top", "half_weight_top3_overlap", "double_weight_top3_overlap"],
    "category_scores.csv": ["category", "rank", "alternative_id", "alternative", "score"],
    "decision_shortlist.csv": ["scenario", "deterministic_rank", "alternative_id", "alternative", "deterministic_score", "monte_carlo_mean_score", "monte_carlo_mean_rank", "win_rate", "top3_rate"],
    "scenario_weights.csv": ["scenario", "criterion", "raw_weight", "normalized_weight"],
    "criteria_definitions.csv": ["criterion", "definition"],
    "evidence_matrix.csv": ["alternative_id", "alternative", "repo", "url", "license", "primary_language", "maturity_level", "source_confidence", "stars", "created_at", "last_pushed_at", "latest_release", "summary", "implementation_notes", "risk_notes", "evidence_urls"],
    "alternative_scorecards.csv": ["alternative_id", "alternative", "license", "maturity_level", "source_confidence", *CRITERIA],
    "implementation_effort_estimates.csv": ["alternative_id", "alternative", "prototype_complexity_score", "prototype_effort", "hardening_complexity_score", "hardening_effort", "first_slice", "adoption_note"],
    "operational_cost_estimates.csv": ["operating_profile", "operating_profile_name", "alternative_id", "alternative", "monthly_task_volume", "review_hours", "admin_hours", "governance_hours", "failure_buffer_hours", "monthly_operational_hours", "hours_per_task", "relative_token_pressure", "latency_risk_score", "operational_friction_score", "cost_risk_band", "main_cost_driver"],
    "operational_fit_rankings.csv": ["scenario", "operating_profile", "rank", "alternative_id", "alternative", "simulation_rank", "simulation_score", "operational_friction_score", "monthly_operational_hours", "relative_token_pressure", "latency_risk_score", "adjusted_score", "rank_delta_vs_simulation"],
    "pilot_sample_size_estimates.csv": ["scenario", "top_candidate", "comparison_rank", "comparison_candidate", "score_gap", "estimated_top_success_rate", "estimated_comparison_success_rate", "tasks_per_candidate", "simulation_trials", "top_wins_probability", "tie_probability", "decision_confidence_target", "recommendation"],
    "evidence_gap_analysis.csv": ["alternative_id", "alternative", "evidence_risk_score", "evidence_risk_band", "gaps", "mitigation", "adoption_implication"],
    "custom_weights_example_rankings.csv": ["scenario", "rank", "alternative_id", "alternative", "score"],
    "regret_analysis.csv": ["scenario", "alternative_id", "alternative", "deterministic_rank", "deterministic_score", "regret_vs_best", "monte_carlo_mean_rank", "win_rate", "top3_rate"],
    "pareto_frontier.csv": ["alternative_id", "alternative", "is_pareto_frontier", "dominated_by_count", "dominated_by"],
    "rank_stability.csv": ["alternative_id", "alternative", "mean_deterministic_rank", "best_deterministic_rank", "worst_deterministic_rank", "top3_scenarios", "top3_scenario_rate", "mean_monte_carlo_rank", "mean_top3_rate"],
    "stress_test_summary.csv": ["stress_case", "scenario", "rank1", "rank2", "rank3", "baseline_rank1", "rank1_changed", "top3_overlap", "rank1_margin"],
    "stress_test_rankings.csv": ["stress_case", "scenario", "rank", "alternative_id", "alternative", "score"],
    "uncertainty_stress_summary.csv": ["uncertainty_case", "scenario", "weight_sigma", "score_sigma_multiplier", "rank1", "rank2", "baseline_rank1", "rank1_changed", "win_rate", "top3_rate", "win_rate_margin", "trials"],
    "uncertainty_stress_details.csv": ["uncertainty_case", "scenario", "alternative_id", "alternative", "mean_score", "mean_rank", "win_rate", "top3_rate", "trials"],
    "pilot_decision_scores.example.csv": ["rank", "candidate", "eligible", "final_score", "gate_failures", "task_success_rate", "review_acceptance_rate", "safety_score", "artifact_completeness", "cost_latency_score", "setup_maintenance_score", "notes"],
    "license_audit.csv": ["alternative", "status", "is_permissive", "license", "repo", "url", "reason"],
    "source_check.csv": ["url", "ok", "status", "elapsed_ms", "final_url", "error"],
    "local_artifact_reference_check.csv": ["source_file", "reference", "resolved_path", "exists"],
    "github_metadata_check.csv": ["alternative_id", "alternative", "repo", "ok", "dataset_license", "live_license", "license_matches", "archived"],
    "csv_schema_check.csv": ["filename", "ok", "missing_columns", "extra_columns", "actual_column_count", "required_column_count"],
    "artifact_manifest.csv": ["path", "size_bytes", "sha256"],
}


def csv_header(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        return next(reader)


def schema_rows(results_dir: Path = DEFAULT_RESULTS) -> list[dict[str, Any]]:
    rows = []
    for filename, required_columns in sorted(SCHEMAS.items()):
        path = results_dir / filename
        if not path.exists():
            rows.append({
                "filename": filename,
                "ok": False,
                "missing_columns": "; ".join(required_columns),
                "extra_columns": "",
                "actual_column_count": 0,
                "required_column_count": len(required_columns),
            })
            continue
        header = csv_header(path)
        missing = [column for column in required_columns if column not in header]
        extra = [column for column in header if column not in required_columns]
        rows.append({
            "filename": filename,
            "ok": not missing,
            "missing_columns": "; ".join(missing),
            "extra_columns": "; ".join(extra),
            "actual_column_count": len(header),
            "required_column_count": len(required_columns),
        })
    return rows


def write_schema_check(rows: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        output_dir / "csv_schema_check.csv",
        rows,
        [
            "filename",
            "ok",
            "missing_columns",
            "extra_columns",
            "actual_column_count",
            "required_column_count",
        ],
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    args = parser.parse_args()

    rows = schema_rows(args.results_dir)
    write_schema_check(rows, args.results_dir)
    failures = [row for row in rows if not row["ok"]]
    print(f"checked {len(rows)} CSV schemas; failures={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
