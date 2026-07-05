#!/usr/bin/env python3
"""Analyze evidence gaps in the alternative dataset."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.simulate_alternatives import load_data, validate_data, write_csv  # noqa: E402


DEFAULT_RESULTS = ROOT / "results"
RETRIEVAL_DATE = date(2026, 7, 5)


def parse_date(value: str) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value)


def maturity_penalty(level: str) -> float:
    return {
        "production": 0.0,
        "beta": 1.0,
        "alpha": 2.0,
    }.get(level, 1.5)


def evidence_gaps(item: dict[str, Any]) -> list[str]:
    gaps = []
    if float(item["source_confidence"]) < 0.70:
        gaps.append("low_source_confidence")
    if item["maturity_level"] == "alpha":
        gaps.append("alpha_maturity")
    if not item["latest_release"]:
        gaps.append("missing_latest_release")
    if int(item["stars"]) < 100:
        gaps.append("low_repository_traction")
    if len(item["evidence_urls"]) < 2:
        gaps.append("single_evidence_url")

    pushed_at = parse_date(item["last_pushed_at"])
    if pushed_at is None:
        gaps.append("missing_last_push")
    elif (RETRIEVAL_DATE - pushed_at).days > 90:
        gaps.append("stale_last_push")

    created_at = parse_date(item["created_at"])
    if created_at is not None and (RETRIEVAL_DATE - created_at).days < 90:
        gaps.append("very_new_repository")

    return gaps


def risk_score(item: dict[str, Any], gaps: list[str]) -> float:
    confidence_penalty = (1.0 - float(item["source_confidence"])) * 4.0
    release_penalty = 0.5 if "missing_latest_release" in gaps else 0.0
    traction_penalty = 0.5 if "low_repository_traction" in gaps else 0.0
    evidence_penalty = 0.4 if "single_evidence_url" in gaps else 0.0
    freshness_penalty = 0.7 if "stale_last_push" in gaps else 0.0
    age_penalty = 0.4 if "very_new_repository" in gaps else 0.0
    return round(
        confidence_penalty
        + maturity_penalty(item["maturity_level"])
        + release_penalty
        + traction_penalty
        + evidence_penalty
        + freshness_penalty
        + age_penalty,
        3,
    )


def risk_band(score: float) -> str:
    if score >= 4.0:
        return "high"
    if score >= 2.5:
        return "medium"
    return "low"


def mitigation_for(gaps: list[str]) -> str:
    if "alpha_maturity" in gaps or "low_source_confidence" in gaps:
        return "Treat as reference-only or require a spike before inclusion in a serious pilot."
    if "missing_latest_release" in gaps or "single_evidence_url" in gaps:
        return "Verify docs, package/version story, and canonical repo before pilot setup."
    if "stale_last_push" in gaps:
        return "Check maintainership and issue activity before depending on it."
    return "Proceed with normal pilot evidence capture."


def adoption_implication(item: dict[str, Any], band: str) -> str:
    if band == "high":
        return "Do not choose as primary foundation without fresh evidence and a successful spike."
    if item["maturity_level"] == "alpha":
        return "Use as design reference or second-phase exploration."
    if band == "medium":
        return "Pilot only with explicit risk checks and version pinning."
    return "Evidence is sufficient for shortlist-level screening."


def evidence_gap_rows(raw_data: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for item in raw_data["alternatives"]:
        gaps = evidence_gaps(item)
        score = risk_score(item, gaps)
        band = risk_band(score)
        rows.append({
            "alternative_id": item["id"],
            "alternative": item["name"],
            "maturity_level": item["maturity_level"],
            "source_confidence": item["source_confidence"],
            "stars": item["stars"],
            "created_at": item["created_at"],
            "last_pushed_at": item["last_pushed_at"],
            "latest_release": item["latest_release"],
            "gap_count": len(gaps),
            "evidence_risk_score": score,
            "evidence_risk_band": band,
            "gaps": "; ".join(gaps),
            "mitigation": mitigation_for(gaps),
            "adoption_implication": adoption_implication(item, band),
        })
    rows.sort(
        key=lambda row: (
            -row["evidence_risk_score"],
            row["alternative"].lower(),
        )
    )
    return rows


def write_evidence_gap_outputs(rows: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        output_dir / "evidence_gap_analysis.csv",
        rows,
        [
            "alternative_id",
            "alternative",
            "maturity_level",
            "source_confidence",
            "stars",
            "created_at",
            "last_pushed_at",
            "latest_release",
            "gap_count",
            "evidence_risk_score",
            "evidence_risk_band",
            "gaps",
            "mitigation",
            "adoption_implication",
        ],
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=ROOT / "data" / "alternatives.json")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_RESULTS)
    args = parser.parse_args()

    raw_data, alternatives = load_data(args.data)
    validate_data(alternatives)
    rows = evidence_gap_rows(raw_data)
    write_evidence_gap_outputs(rows, args.output_dir)
    high_risk = sum(1 for row in rows if row["evidence_risk_band"] == "high")
    print(f"wrote {len(rows)} evidence gap rows; high-risk evidence gaps: {high_risk}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
