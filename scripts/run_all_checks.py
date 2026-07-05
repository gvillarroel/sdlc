#!/usr/bin/env python3
"""Run the full local quality and artifact regeneration workflow."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


COMMANDS = [
    [PYTHON, "-m", "unittest", "discover", "-s", "tests"],
    [PYTHON, "scripts/simulate_alternatives.py", "--trials", "5000", "--seed", "7331"],
    [PYTHON, "scripts/stress_test_simulation.py", "--trials", "1500", "--seed", "9011"],
    [PYTHON, "scripts/estimate_implementation_effort.py"],
    [PYTHON, "scripts/estimate_operational_costs.py"],
    [PYTHON, "scripts/estimate_pilot_sample_sizes.py"],
    [PYTHON, "scripts/analyze_score_drivers.py"],
    [PYTHON, "scripts/build_scenario_playbooks.py"],
    [PYTHON, "scripts/analyze_evidence_gaps.py"],
    [PYTHON, "scripts/rank_with_custom_weights.py"],
    [PYTHON, "scripts/license_audit.py"],
    [PYTHON, "scripts/generate_charts.py"],
    [PYTHON, "scripts/build_results_data_dictionary.py"],
    [PYTHON, "scripts/build_report_bundle.py"],
    [PYTHON, "scripts/check_local_artifact_references.py"],
    [PYTHON, "scripts/generate_artifact_manifest.py"],
    [
        PYTHON,
        "scripts/score_pilot_results.py",
        "--input",
        "examples/pilot_candidate_summary.example.csv",
        "--output",
        "results/pilot_decision_scores.example.csv",
    ],
    [PYTHON, "scripts/validate_csv_schemas.py"],
    [PYTHON, "scripts/generate_artifact_manifest.py"],
    [PYTHON, "scripts/validate_artifacts.py"],
]


def run_command(command: list[str]) -> None:
    print("+ " + " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    for command in COMMANDS:
        run_command(command)
    print("all checks OK")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.returncode)
