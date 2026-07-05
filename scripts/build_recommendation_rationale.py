#!/usr/bin/env python3
"""Build scenario recommendation rationale from generated screening outputs."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS = ROOT / "results"
DEFAULT_REPORT = ROOT / "reports" / "recommendation_rationale.md"
DEFAULT_SCENARIOS = ROOT / "data" / "scenario_profiles.json"

PROFILE_COLUMNS = {
    "pilot_100_tasks": "pilot_operational_rank",
    "team_rollout_400_tasks": "team_rollout_operational_rank",
    "autonomous_pr_1000_tasks": "autonomous_pr_operational_rank",
}

FIELDNAMES = [
    "scenario",
    "rank",
    "alternative_id",
    "alternative",
    "posture",
    "score_gap_to_leader",
    "win_rate",
    "top3_rate",
    "evidence_risk_band",
    "prototype_effort",
    "hardening_effort",
    "pilot_operational_rank",
    "team_rollout_operational_rank",
    "autonomous_pr_operational_rank",
    "key_rationale",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_scenario_labels(path: Path = DEFAULT_SCENARIOS) -> dict[str, str]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {scenario["id"]: scenario["label"] for scenario in raw["scenarios"]}


def operational_rank_index(rows: list[dict[str, str]]) -> dict[tuple[str, str, str], str]:
    return {
        (row["scenario"], row["alternative_id"], row["operating_profile"]): row["rank"]
        for row in rows
    }


def decision_posture(rank: int, win_rate: float, top3_rate: float, evidence_band: str) -> str:
    if evidence_band == "high":
        return "Do not select as primary"
    if evidence_band == "medium":
        return "Second-phase exploration"
    if rank == 1 and win_rate >= 0.40 and top3_rate >= 0.75:
        return "Primary pilot candidate"
    if rank <= 3 and top3_rate >= 0.60:
        return "Head-to-head pilot"
    if top3_rate >= 0.25:
        return "Fallback or benchmark"
    return "Watchlist only"


def key_rationale(
    rank: int,
    score_gap: float,
    win_rate: float,
    top3_rate: float,
    evidence_band: str,
    hardening_effort: str,
    operational_ranks: list[int],
) -> str:
    parts = []
    if rank == 1:
        parts.append("scenario score leader")
    elif score_gap <= 0.05:
        parts.append(f"near-tie with the leader ({score_gap:.3f} score gap)")
    else:
        parts.append(f"{score_gap:.3f} behind the scenario leader")

    if top3_rate >= 0.75:
        parts.append(f"strong Monte Carlo shortlist stability ({top3_rate:.0%} top-3 rate)")
    elif top3_rate >= 0.40:
        parts.append(f"moderate Monte Carlo shortlist stability ({top3_rate:.0%} top-3 rate)")
    else:
        parts.append(f"fragile Monte Carlo shortlist position ({top3_rate:.0%} top-3 rate)")

    if win_rate >= 0.40:
        parts.append(f"credible win-rate signal ({win_rate:.0%})")
    elif rank == 1:
        parts.append("leader is close enough that a head-to-head pilot is still required")

    if evidence_band == "low":
        parts.append("low evidence-risk band")
    else:
        parts.append(f"{evidence_band} evidence-risk band")

    if hardening_effort in {"3-6 weeks", "6-12 weeks"}:
        parts.append(f"{hardening_effort} hardening estimate")

    if operational_ranks:
        best_rank = min(operational_ranks)
        worst_rank = max(operational_ranks)
        if worst_rank <= 3:
            parts.append("stays in the top three after operational-friction adjustment")
        elif worst_rank - rank >= 2:
            parts.append("operational friction can push it down in rollout profiles")
        else:
            parts.append("operational rank is broadly consistent with simulation rank")

    return "; ".join(parts) + "."


def rationale_rows(results_dir: Path = DEFAULT_RESULTS) -> list[dict[str, Any]]:
    shortlist_rows = read_csv(results_dir / "decision_shortlist.csv")
    evidence_by_id = {
        row["alternative_id"]: row
        for row in read_csv(results_dir / "evidence_gap_analysis.csv")
    }
    effort_by_id = {
        row["alternative_id"]: row
        for row in read_csv(results_dir / "implementation_effort_estimates.csv")
    }
    operational_ranks = operational_rank_index(
        read_csv(results_dir / "operational_fit_rankings.csv")
    )
    leader_score_by_scenario: dict[str, float] = {}
    for row in shortlist_rows:
        score = float(row["deterministic_score"])
        scenario = row["scenario"]
        leader_score_by_scenario[scenario] = max(
            leader_score_by_scenario.get(scenario, score),
            score,
        )

    rows = []
    for row in shortlist_rows:
        scenario = row["scenario"]
        alternative_id = row["alternative_id"]
        rank = int(row["deterministic_rank"])
        win_rate = float(row["win_rate"])
        top3_rate = float(row["top3_rate"])
        score_gap = leader_score_by_scenario[scenario] - float(row["deterministic_score"])
        evidence = evidence_by_id[alternative_id]
        effort = effort_by_id[alternative_id]
        profile_ranks = {
            column: operational_ranks[(scenario, alternative_id, profile)]
            for profile, column in PROFILE_COLUMNS.items()
        }
        numeric_profile_ranks = [int(rank_value) for rank_value in profile_ranks.values()]
        posture = decision_posture(
            rank,
            win_rate,
            top3_rate,
            evidence["evidence_risk_band"],
        )
        rows.append({
            "scenario": scenario,
            "rank": rank,
            "alternative_id": alternative_id,
            "alternative": row["alternative"],
            "posture": posture,
            "score_gap_to_leader": round(score_gap, 3),
            "win_rate": round(win_rate, 4),
            "top3_rate": round(top3_rate, 4),
            "evidence_risk_band": evidence["evidence_risk_band"],
            "prototype_effort": effort["prototype_effort"],
            "hardening_effort": effort["hardening_effort"],
            **profile_ranks,
            "key_rationale": key_rationale(
                rank,
                score_gap,
                win_rate,
                top3_rate,
                evidence["evidence_risk_band"],
                effort["hardening_effort"],
                numeric_profile_ranks,
            ),
        })
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_report(rows: list[dict[str, Any]], scenario_labels: dict[str, str]) -> str:
    lines = [
        "# Recommendation Rationale",
        "",
        "Date: 2026-07-05",
        "",
        "## Purpose",
        "",
        "This appendix turns the generated screening outputs into a scenario-by-scenario decision rationale. It combines the deterministic shortlist, Monte Carlo stability, evidence-risk bands, implementation effort, and operation-adjusted ranks. It is still screening evidence: final selection requires the pilot protocol and security gates.",
        "",
        "Generated output: `results/recommendation_rationale.csv`",
        "",
        "Input outputs: `results/decision_shortlist.csv`, `results/evidence_gap_analysis.csv`, `results/implementation_effort_estimates.csv`, and `results/operational_fit_rankings.csv`.",
        "",
        "Run:",
        "",
        "```powershell",
        "python scripts/build_recommendation_rationale.py",
        "```",
        "",
        "## Scenario Rationale",
        "",
        "| Scenario | Rank | Candidate | Posture | Gap | Win | Top-3 | Evidence | Hardening | Operational ranks | Rationale |",
        "|---|---:|---|---|---:|---:|---:|---|---|---|---|",
    ]
    for row in rows:
        operational = " / ".join([
            str(row["pilot_operational_rank"]),
            str(row["team_rollout_operational_rank"]),
            str(row["autonomous_pr_operational_rank"]),
        ])
        lines.append(
            "| {scenario} | {rank} | {alternative} | {posture} | {gap:.3f} | {win:.0%} | {top3:.0%} | {evidence} | {hardening} | {operational} | {rationale} |".format(
                scenario=scenario_labels.get(row["scenario"], row["scenario"]),
                rank=row["rank"],
                alternative=row["alternative"],
                posture=row["posture"],
                gap=float(row["score_gap_to_leader"]),
                win=float(row["win_rate"]),
                top3=float(row["top3_rate"]),
                evidence=row["evidence_risk_band"],
                hardening=row["hardening_effort"],
                operational=operational,
                rationale=row["key_rationale"],
            )
        )
    lines.extend([
        "",
        "Operational ranks are shown as `pilot / team rollout / autonomous PR` ranks after applying the operating-cost model.",
        "",
        "## Interpretation",
        "",
        "- A `Primary pilot candidate` is strong enough to lead a pilot, but still needs the pilot protocol and security gates.",
        "- A `Head-to-head pilot` is close enough to the leader that the report should not force a single winner without live task evidence.",
        "- `Second-phase exploration` candidates can be useful design references, but their evidence or maturity profile should keep them out of the first production decision.",
        "- `Fallback or benchmark` candidates are useful comparators for local productivity or research baselines.",
        "",
    ])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=DEFAULT_RESULTS / "recommendation_rationale.csv",
    )
    parser.add_argument("--output-report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    rows = rationale_rows(args.results_dir)
    write_csv(args.output_csv, rows)
    args.output_report.write_text(
        markdown_report(rows, read_scenario_labels()),
        encoding="utf-8",
        newline="\n",
    )
    print(f"wrote {len(rows)} recommendation rationale rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
