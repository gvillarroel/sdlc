#!/usr/bin/env python3
"""Build a Markdown data dictionary for generated CSV outputs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_csv_schemas import SCHEMAS  # noqa: E402


DEFAULT_OUTPUT = ROOT / "reports" / "results_data_dictionary.md"

FILE_DESCRIPTIONS = {
    "deterministic_rankings.csv": "Base weighted rankings by scenario.",
    "monte_carlo_summary.csv": "Monte Carlo score and rank stability by scenario.",
    "sensitivity_summary.csv": "Criterion weight sensitivity results.",
    "category_scores.csv": "Criterion-group scorecards independent of scenario weights.",
    "decision_shortlist.csv": "Scenario shortlist combining deterministic and Monte Carlo evidence.",
    "scenario_weights.csv": "Raw and normalized weights by scenario and criterion.",
    "criteria_definitions.csv": "Human-readable scoring criterion definitions.",
    "evidence_matrix.csv": "Source, metadata, notes, and evidence URLs by alternative.",
    "alternative_scorecards.csv": "Wide scorecard of all 0-5 criterion scores.",
    "implementation_effort_estimates.csv": "Prototype and hardening effort estimates.",
    "operational_cost_estimates.csv": "Relative monthly operating effort, token pressure, latency risk, and cost-risk bands.",
    "operational_fit_rankings.csv": "Scenario rankings adjusted by operating-profile friction.",
    "pilot_sample_size_estimates.csv": "Pilot task-count simulation for separating close shortlist candidates.",
    "evidence_gap_analysis.csv": "Evidence risk signals and mitigation notes.",
    "custom_weights_example_rankings.csv": "Example deterministic rankings from custom weights.",
    "regret_analysis.csv": "Score gaps versus scenario winners.",
    "pareto_frontier.csv": "Raw-criteria Pareto dominance analysis.",
    "rank_stability.csv": "Cross-scenario deterministic and Monte Carlo rank stability.",
    "stress_test_summary.csv": "Deterministic stress-test summary.",
    "stress_test_rankings.csv": "Full deterministic rankings under stress cases.",
    "uncertainty_stress_summary.csv": "Monte Carlo summary under alternate uncertainty cases.",
    "uncertainty_stress_details.csv": "Full Monte Carlo rows under alternate uncertainty cases.",
    "pilot_decision_scores.example.csv": "Example post-pilot decision score output.",
    "license_audit.csv": "Permissive-license audit.",
    "source_check.csv": "Live external source URL check.",
    "local_artifact_reference_check.csv": "Local Markdown artifact reference check.",
    "github_metadata_check.csv": "Live GitHub repository metadata check.",
    "csv_schema_check.csv": "Generated CSV schema validation output.",
}


def build_dictionary() -> str:
    lines = [
        "# Results Data Dictionary",
        "",
        "Date: 2026-07-05",
        "",
        "This generated dictionary summarizes the CSV outputs in `results/`. Expected columns come from `scripts/validate_csv_schemas.py`.",
        "",
    ]
    for filename in sorted(SCHEMAS):
        lines.extend([
            f"## `{filename}`",
            "",
            FILE_DESCRIPTIONS.get(filename, "Generated CSV artifact."),
            "",
            "| Column |",
            "|---|",
        ])
        for column in SCHEMAS[filename]:
            lines.append(f"| `{column}` |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    args.output.write_text(build_dictionary(), encoding="utf-8", newline="\n")
    print(f"wrote {args.output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
