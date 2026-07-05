#!/usr/bin/env python3
"""Build scenario-specific decision playbooks from rankings and profiles."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.simulate_alternatives import (  # noqa: E402
    deterministic_rankings,
    load_data,
    validate_data,
    write_csv,
)


DEFAULT_PROFILES = ROOT / "data" / "scenario_profiles.json"
DEFAULT_RESULTS = ROOT / "results"
DEFAULT_REPORT = ROOT / "reports" / "scenario_playbooks.md"

PILOT_FOCUS_BY_SCENARIO = {
    "custom_orchestrator_platform": "Build one minimal orchestrator slice with tools, sandbox policy, trace capture, and a rollback path.",
    "secure_autonomous_prs": "Run autonomous issue-to-PR tasks under the strictest sandbox, network, secret, branch, and approval gates.",
    "quick_local_coding": "Measure developer setup time, review friction, accepted diffs, and daily workflow ergonomics.",
    "research_benchmarking": "Run fixed-seed benchmark tasks with complete trajectories, patches, costs, and ablation notes.",
    "enterprise_control_plane": "Evaluate admin controls, auditability, multi-team workflow ownership, and backend portability.",
}

NO_GO_BY_SCENARIO = {
    "custom_orchestrator_platform": "No inspectable tool boundary, traces, or extension path for product-specific policy.",
    "secure_autonomous_prs": "Any unresolved safety gate failure, secret exposure, protected-branch write, or missing audit log.",
    "quick_local_coding": "Setup or review friction is higher than current developer workflow for routine tasks.",
    "research_benchmarking": "Runs cannot be reproduced with fixed seeds, task definitions, logs, and patch artifacts.",
    "enterprise_control_plane": "No credible ownership model for users, permissions, audit logs, incidents, and upgrades.",
}


def load_profiles(path: Path = DEFAULT_PROFILES) -> dict[str, dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {
        item["id"]: item
        for item in raw["scenarios"]
    }


def playbook_rows(profiles: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    _raw, alternatives = load_data()
    validate_data(alternatives)
    rankings = deterministic_rankings(alternatives)
    rows = []
    for scenario, scenario_rows in rankings.items():
        profile = profiles[scenario]
        top3 = scenario_rows[:3]
        rows.append({
            "scenario": scenario,
            "label": profile["label"],
            "question": profile["question"],
            "primary_candidate": top3[0]["alternative"],
            "primary_score": round(float(top3[0]["score"]), 3),
            "fallback_candidates": "; ".join(row["alternative"] for row in top3[1:]),
            "priority_summary": "; ".join(profile["priorities"][:4]),
            "pilot_focus": PILOT_FOCUS_BY_SCENARIO[scenario],
            "no_go_condition": NO_GO_BY_SCENARIO[scenario],
            "related_artifacts": "reports/pilot_protocol.md; reports/pilot_sample_size.md; reports/operational_cost_model.md",
        })
    return rows


def build_report(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Scenario Playbooks",
        "",
        "Date: 2026-07-05",
        "",
        "This appendix turns each simulated scenario into a short execution playbook. Use it after choosing the scenario and before starting the pilot.",
        "",
        "Generated output: `results/scenario_playbook_summary.csv`.",
        "",
    ]
    for row in rows:
        lines.extend([
            f"## {row['label']}",
            "",
            f"Question: {row['question']}",
            "",
            "| Field | Recommendation |",
            "|---|---|",
            f"| Primary candidate | {row['primary_candidate']} ({row['primary_score']}) |",
            f"| Fallback candidates | {row['fallback_candidates']} |",
            f"| Priority summary | {row['priority_summary']} |",
            f"| Pilot focus | {row['pilot_focus']} |",
            f"| No-go condition | {row['no_go_condition']} |",
            f"| Related artifacts | {row['related_artifacts']} |",
            "",
        ])
    lines.extend([
        "## Use Notes",
        "",
        "- Treat the primary candidate as a starting hypothesis, not a final selection.",
        "- If the pilot sample-size appendix says the top cluster is unresolved, keep both primary and fallback candidates in the same pilot wave.",
        "- If the operational-cost appendix contradicts the scenario winner, decide whether strategic fit or operating friction matters more for the current adoption phase.",
        "",
    ])
    return "\n".join(lines).rstrip() + "\n"


def write_outputs(rows: list[dict[str, Any]], output_dir: Path, report_output: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    write_csv(
        output_dir / "scenario_playbook_summary.csv",
        rows,
        [
            "scenario",
            "label",
            "question",
            "primary_candidate",
            "primary_score",
            "fallback_candidates",
            "priority_summary",
            "pilot_focus",
            "no_go_condition",
            "related_artifacts",
        ],
    )
    report_output.write_text(build_report(rows), encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profiles", type=Path, default=DEFAULT_PROFILES)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    rows = playbook_rows(load_profiles(args.profiles))
    write_outputs(rows, args.output_dir, args.report_output)
    print(f"wrote {len(rows)} scenario playbooks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
