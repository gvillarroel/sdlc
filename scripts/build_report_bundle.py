#!/usr/bin/env python3
"""Build a single Markdown bundle from the report artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
DEFAULT_OUTPUT = REPORTS / "final_report_bundle.md"

SOURCE_REPORTS = [
    "executive_brief.md",
    "release_notes.md",
    "ai_orchestrator_frameworks_report.md",
    "sandbox_report.md",
    "market_maintenance_synthesis.md",
    "market_entry_barriers_shift.md",
    "market_fragmentation_user_share.md",
    "long_term_ai_app_maintenance.md",
    "ai_code_trust_matrix.md",
    "candidate_taxonomy.md",
    "exclusions.md",
    "adoption_decision_record.md",
    "methodology_appendix.md",
    "simulation_assumptions.md",
    "score_driver_summary.md",
    "operational_cost_model.md",
    "evidence_gap_analysis.md",
    "recommendation_rationale.md",
    "github_metadata_check.md",
    "security_evaluation_fixtures.md",
    "residual_risks.md",
    "risk_validation_matrix.md",
    "presentation_outline.md",
    "scenario_playbooks.md",
    "pilot_protocol.md",
    "pilot_sample_size.md",
    "validation_summary.md",
    "environment_prerequisites.md",
    "results_data_dictionary.md",
    "maintenance_guide.md",
    "requirements_traceability.md",
    "artifact_index.md",
]


def bundle_markdown(source_reports: list[str] = SOURCE_REPORTS) -> str:
    lines = [
        "# Final Report Bundle",
        "",
        "Date: 2026-07-05",
        "",
        "This generated bundle concatenates the main report and key appendices for one-file review. Source files remain authoritative for editing.",
        "",
        "## Included Files",
        "",
    ]
    for filename in source_reports:
        lines.append(f"- `reports/{filename}`")
    lines.append("")

    for filename in source_reports:
        path = REPORTS / filename
        content = path.read_text(encoding="utf-8").strip()
        lines.extend([
            "---",
            "",
            f"<!-- Source: reports/{filename} -->",
            "",
            content,
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    args.output.write_text(bundle_markdown(), encoding="utf-8", newline="\n")
    print(f"wrote {args.output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
