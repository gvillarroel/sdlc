#!/usr/bin/env python3
"""Summarize candidate score strengths, weaknesses, and criterion spread."""

from __future__ import annotations

import argparse
import statistics
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.simulate_alternatives import (  # noqa: E402
    CRITERIA,
    Alternative,
    deterministic_rankings,
    load_data,
    validate_data,
    write_csv,
)


DEFAULT_RESULTS = ROOT / "results"
DEFAULT_REPORT = ROOT / "reports" / "score_driver_summary.md"


def format_drivers(items: list[tuple[str, float]]) -> str:
    return "; ".join(f"{criterion}={score:.1f}" for criterion, score in items)


def candidate_driver_rows(alternatives: list[Alternative]) -> list[dict[str, Any]]:
    rankings = deterministic_rankings(alternatives)
    ranks_by_alt: dict[str, list[tuple[str, int]]] = {}
    for scenario, rows in rankings.items():
        for row in rows:
            ranks_by_alt.setdefault(row["alternative_id"], []).append((scenario, int(row["rank"])))

    rows = []
    for alt in alternatives:
        sorted_scores = sorted(
            alt.scores.items(),
            key=lambda item: (-item[1], item[0]),
        )
        weak_scores = sorted(
            alt.scores.items(),
            key=lambda item: (item[1], item[0]),
        )
        ranks = ranks_by_alt[alt.id]
        best_scenario, best_rank = min(ranks, key=lambda item: item[1])
        worst_scenario, worst_rank = max(ranks, key=lambda item: item[1])
        values = list(alt.scores.values())
        rows.append({
            "alternative_id": alt.id,
            "alternative": alt.name,
            "maturity_level": alt.maturity_level,
            "source_confidence": alt.source_confidence,
            "top_strengths": format_drivers(sorted_scores[:3]),
            "top_weaknesses": format_drivers(weak_scores[:3]),
            "best_scenario": best_scenario,
            "best_rank": best_rank,
            "worst_scenario": worst_scenario,
            "worst_rank": worst_rank,
            "mean_score": round(statistics.fmean(values), 3),
            "score_spread": round(max(values) - min(values), 3),
        })
    rows.sort(key=lambda row: (row["best_rank"], row["worst_rank"], row["alternative"].lower()))
    return rows


def criterion_spread_rows(alternatives: list[Alternative]) -> list[dict[str, Any]]:
    rows = []
    for criterion in CRITERIA:
        values = [
            (alt.name, alt.scores[criterion])
            for alt in alternatives
        ]
        scores = [score for _name, score in values]
        max_score = max(scores)
        min_score = min(scores)
        leaders = [
            name
            for name, score in values
            if score == max_score
        ]
        laggards = [
            name
            for name, score in values
            if score == min_score
        ]
        rows.append({
            "criterion": criterion,
            "mean_score": round(statistics.fmean(scores), 3),
            "min_score": min_score,
            "max_score": max_score,
            "score_spread": round(max_score - min_score, 3),
            "leaders": "; ".join(sorted(leaders)),
            "laggards": "; ".join(sorted(laggards)),
        })
    rows.sort(key=lambda row: (-row["score_spread"], row["criterion"]))
    return rows


def build_report(
    candidate_rows: list[dict[str, Any]],
    criterion_rows: list[dict[str, Any]],
) -> str:
    lines = [
        "# Score Driver Summary",
        "",
        "Date: 2026-07-05",
        "",
        "This appendix explains which scored criteria drive each candidate up or down in the simulation. It is generated from `data/alternatives.json` and the deterministic scenario rankings.",
        "",
        "Generated outputs: `results/score_driver_summary.csv` and `results/criterion_spread_summary.csv`.",
        "",
        "## Highest-Spread Criteria",
        "",
        "| Criterion | Spread | Mean | Leaders | Laggards |",
        "|---|---:|---:|---|---|",
    ]
    for row in criterion_rows[:8]:
        lines.append(
            "| {criterion} | {spread:.1f} | {mean:.3f} | {leaders} | {laggards} |".format(
                criterion=row["criterion"],
                spread=float(row["score_spread"]),
                mean=float(row["mean_score"]),
                leaders=row["leaders"],
                laggards=row["laggards"],
            )
        )
    lines.extend([
        "",
        "## Candidate Drivers",
        "",
        "| Candidate | Strengths | Weaknesses | Best scenario | Worst scenario | Mean | Spread |",
        "|---|---|---|---|---|---:|---:|",
    ])
    for row in candidate_rows:
        lines.append(
            "| {alternative} | {strengths} | {weaknesses} | {best} #{best_rank} | {worst} #{worst_rank} | {mean:.3f} | {spread:.3f} |".format(
                alternative=row["alternative"],
                strengths=row["top_strengths"],
                weaknesses=row["top_weaknesses"],
                best=row["best_scenario"],
                best_rank=row["best_rank"],
                worst=row["worst_scenario"],
                worst_rank=row["worst_rank"],
                mean=float(row["mean_score"]),
                spread=float(row["score_spread"]),
            )
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "- Criteria with high spread drive more ranking separation. Low-spread criteria should be treated as weaker differentiators unless a stakeholder explicitly weights them heavily.",
        "- Candidate strengths and weaknesses are scorecard diagnostics, not standalone recommendations. Always read them with evidence confidence, operational cost, security gates, and pilot results.",
        "- A candidate with a strong best scenario and a poor worst scenario is specialized; avoid generalizing it across workflows without changing scenario weights and rerunning the simulation.",
        "",
    ])
    return "\n".join(lines).rstrip() + "\n"


def write_outputs(
    candidate_rows: list[dict[str, Any]],
    criterion_rows: list[dict[str, Any]],
    output_dir: Path,
    report_output: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    write_csv(
        output_dir / "score_driver_summary.csv",
        candidate_rows,
        [
            "alternative_id",
            "alternative",
            "maturity_level",
            "source_confidence",
            "top_strengths",
            "top_weaknesses",
            "best_scenario",
            "best_rank",
            "worst_scenario",
            "worst_rank",
            "mean_score",
            "score_spread",
        ],
    )
    write_csv(
        output_dir / "criterion_spread_summary.csv",
        criterion_rows,
        [
            "criterion",
            "mean_score",
            "min_score",
            "max_score",
            "score_spread",
            "leaders",
            "laggards",
        ],
    )
    report_output.write_text(
        build_report(candidate_rows, criterion_rows),
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    _raw, alternatives = load_data()
    validate_data(alternatives)
    candidate_rows = candidate_driver_rows(alternatives)
    criterion_rows = criterion_spread_rows(alternatives)
    write_outputs(candidate_rows, criterion_rows, args.output_dir, args.report_output)
    print(f"wrote {len(candidate_rows)} candidate score drivers and {len(criterion_rows)} criterion spread rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
