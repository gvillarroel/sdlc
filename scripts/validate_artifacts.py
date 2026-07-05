#!/usr/bin/env python3
"""Validate generated report artifacts without requiring network access."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
SCENARIO_COUNT = 5
DETERMINISTIC_STRESS_CASE_COUNT = 8
UNCERTAINTY_STRESS_CASE_COUNT = 5
CUSTOM_WEIGHT_SCENARIO_COUNT = 2

REQUIRED_RESULT_FILES = [
    "deterministic_rankings.csv",
    "monte_carlo_summary.csv",
    "sensitivity_summary.csv",
    "category_scores.csv",
    "decision_shortlist.csv",
    "scenario_weights.csv",
    "criteria_definitions.csv",
    "evidence_matrix.csv",
    "alternative_scorecards.csv",
    "implementation_effort_estimates.csv",
    "evidence_gap_analysis.csv",
    "custom_weights_example_rankings.csv",
    "regret_analysis.csv",
    "pareto_frontier.csv",
    "rank_stability.csv",
    "stress_test_summary.csv",
    "stress_test_rankings.csv",
    "uncertainty_stress_summary.csv",
    "uncertainty_stress_details.csv",
    "pilot_decision_scores.example.csv",
    "license_audit.csv",
    "source_check.csv",
    "local_artifact_reference_check.csv",
    "all_results.json"
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_required_files() -> None:
    for filename in REQUIRED_RESULT_FILES:
        path = RESULTS / filename
        assert_true(path.exists(), f"missing results file: {path}")
        assert_true(path.stat().st_size > 0, f"empty results file: {path}")


def validate_result_shapes() -> None:
    alternatives = json.loads((DATA / "alternatives.json").read_text(encoding="utf-8"))["alternatives"]
    alt_count = len(alternatives)

    assert_true(len(read_csv(RESULTS / "deterministic_rankings.csv")) == alt_count * SCENARIO_COUNT, "unexpected deterministic ranking row count")
    assert_true(len(read_csv(RESULTS / "monte_carlo_summary.csv")) == alt_count * SCENARIO_COUNT, "unexpected monte carlo row count")
    assert_true(len(read_csv(RESULTS / "regret_analysis.csv")) == alt_count * SCENARIO_COUNT, "unexpected regret row count")
    assert_true(len(read_csv(RESULTS / "rank_stability.csv")) == alt_count, "unexpected rank stability row count")
    assert_true(len(read_csv(RESULTS / "pareto_frontier.csv")) == alt_count, "unexpected pareto row count")
    assert_true(len(read_csv(RESULTS / "implementation_effort_estimates.csv")) == alt_count, "unexpected implementation effort row count")
    assert_true(len(read_csv(RESULTS / "evidence_gap_analysis.csv")) == alt_count, "unexpected evidence gap row count")
    assert_true(len(read_csv(RESULTS / "custom_weights_example_rankings.csv")) == CUSTOM_WEIGHT_SCENARIO_COUNT * alt_count, "unexpected custom weights row count")
    assert_true(len(read_csv(RESULTS / "stress_test_summary.csv")) == DETERMINISTIC_STRESS_CASE_COUNT * SCENARIO_COUNT, "unexpected stress test summary row count")
    assert_true(len(read_csv(RESULTS / "stress_test_rankings.csv")) == DETERMINISTIC_STRESS_CASE_COUNT * SCENARIO_COUNT * alt_count, "unexpected stress test rankings row count")
    assert_true(len(read_csv(RESULTS / "uncertainty_stress_summary.csv")) == UNCERTAINTY_STRESS_CASE_COUNT * SCENARIO_COUNT, "unexpected uncertainty stress summary row count")
    assert_true(len(read_csv(RESULTS / "uncertainty_stress_details.csv")) == UNCERTAINTY_STRESS_CASE_COUNT * SCENARIO_COUNT * alt_count, "unexpected uncertainty stress details row count")


def validate_license_and_sources() -> None:
    license_rows = read_csv(RESULTS / "license_audit.csv")
    included = [row for row in license_rows if row["status"] == "included"]
    excluded = [row for row in license_rows if row["status"] == "excluded"]
    assert_true(len(included) == 17, "expected 17 included permissive alternatives")
    assert_true(len(excluded) == 2, "expected 2 excluded alternatives")
    for row in included:
        assert_true(row["license"] in {"MIT", "Apache-2.0"}, f"non-permissive included row: {row}")

    source_rows = read_csv(RESULTS / "source_check.csv")
    assert_true(source_rows, "source check is empty")
    assert_true(all(row["ok"] == "True" for row in source_rows), "one or more source URLs failed latest check")

    reference_rows = read_csv(RESULTS / "local_artifact_reference_check.csv")
    assert_true(reference_rows, "local artifact reference check is empty")
    assert_true(all(row["exists"] == "True" for row in reference_rows), "one or more local artifact references are missing")


def validate_report_references() -> None:
    report = (REPORTS / "ai_orchestrator_frameworks_report.md").read_text(encoding="utf-8")
    for filename in REQUIRED_RESULT_FILES:
        assert_true(filename in report or filename in {"deterministic_rankings.csv", "monte_carlo_summary.csv", "sensitivity_summary.csv"}, f"report does not reference {filename}")
    for artifact in [
        "data/pilot_tasks.json",
        "data/risk_register.json",
        "data/security_evaluation_fixtures.json",
        "data/simulation_assumptions.json",
        "data/traceability_matrix.json",
        "reports/executive_brief.md",
        "reports/evidence_gap_analysis.md",
        "reports/methodology_appendix.md",
        "reports/requirements_traceability.md",
        "reports/security_evaluation_fixtures.md",
        "reports/simulation_assumptions.md"
    ]:
        assert_true(artifact in report, f"report does not reference {artifact}")


def validate_all() -> None:
    validate_required_files()
    validate_result_shapes()
    validate_license_and_sources()
    validate_report_references()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    validate_all()
    print("artifact validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
