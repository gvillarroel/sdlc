#!/usr/bin/env python3
"""Generate implementation effort estimates from the scoring dataset."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.simulate_alternatives import Alternative, load_data, validate_data, write_csv  # noqa: E402


DEFAULT_RESULTS = ROOT / "results"


PROTOTYPE_WEIGHTS = {
    "implementation_ease": 0.40,
    "extensibility": 0.20,
    "coding_fit": 0.20,
    "provider_portability": 0.10,
    "deployment_flexibility": 0.10,
}

HARDENING_WEIGHTS = {
    "maturity": 0.20,
    "sandbox_isolation": 0.20,
    "security_governance": 0.20,
    "observability": 0.15,
    "ci_pr": 0.15,
    "deployment_flexibility": 0.10,
}

PROTOTYPE_BANDS = [
    (1.8, "0.5-1 day"),
    (2.4, "1-2 days"),
    (3.1, "2-5 days"),
    (3.8, "3-7 days"),
    (5.0, "1-2 weeks"),
]

HARDENING_BANDS = [
    (1.8, "3-7 days"),
    (2.4, "1-2 weeks"),
    (3.1, "2-4 weeks"),
    (3.8, "3-6 weeks"),
    (5.0, "6-12 weeks"),
]

PROTOTYPE_SCOPE_ADJUSTMENT = {
    "aider": -0.1,
    "mini_swe_agent": 0.0,
    "goose": 0.2,
    "opencode": 0.2,
    "codex_cli": 0.5,
    "swe_agent": 0.4,
    "cline": 1.0,
    "openhands_sdk": 1.3,
    "deep_agents": 1.1,
    "flue": 1.0,
    "sandcastle": 1.0,
    "openhands_agent_canvas": 1.5,
    "open_swe": 1.9,
    "omnigent": 2.0,
    "anchor": 0.0,
    "omniagent": 0.5,
    "omni_agent": 0.8,
}

HARDENING_SCOPE_ADJUSTMENT = {
    "aider": 0.2,
    "mini_swe_agent": 0.2,
    "goose": 0.4,
    "opencode": 0.5,
    "codex_cli": 0.7,
    "swe_agent": 0.5,
    "cline": 1.2,
    "openhands_sdk": 1.3,
    "deep_agents": 1.2,
    "flue": 1.2,
    "sandcastle": 1.3,
    "openhands_agent_canvas": 1.8,
    "open_swe": 2.5,
    "omnigent": 2.5,
    "anchor": 1.3,
    "omniagent": 1.2,
    "omni_agent": 1.3,
}


FIRST_SLICE_BY_ID = {
    "openhands_sdk": "Disposable workspace plus read/edit/shell/test tools and artifact capture.",
    "deep_agents": "Single-agent graph and subagent graph with the same tool boundary.",
    "flue": "Minimal TypeScript agent server with one coding workflow and virtual sandbox.",
    "codex_cli": "One task under read-only, workspace-write, and restricted-network profiles.",
    "cline": "One interactive task and one headless SDK task with approval metrics.",
    "mini_swe_agent": "Fixed-seed task run with complete trajectory and patch capture.",
    "swe_agent": "Small SWE-style task suite with trajectory, patch, and cost capture.",
    "open_swe": "One sandbox provider and five issue-to-PR tasks.",
}


def weighted_difficulty(scores: dict[str, float], weights: dict[str, float]) -> float:
    total_weight = sum(weights.values())
    return sum((5.0 - scores[criterion]) * weight for criterion, weight in weights.items()) / total_weight


def complexity_score(scores: dict[str, float], weights: dict[str, float]) -> float:
    return 1.0 + (weighted_difficulty(scores, weights) / 5.0) * 4.0


def adjusted_complexity(score: float, adjustment: float) -> float:
    return min(5.0, max(1.0, score + adjustment))


def effort_band(score: float, bands: list[tuple[float, str]]) -> str:
    for upper, label in bands:
        if score <= upper:
            return label
    raise ValueError(f"complexity score outside expected range: {score}")


def top_driver(scores: dict[str, float], weights: dict[str, float]) -> str:
    drivers = sorted(
        (
            ((5.0 - scores[criterion]) * weight, criterion)
            for criterion, weight in weights.items()
        ),
        reverse=True,
    )
    return drivers[0][1]


def adoption_note(alt: Alternative) -> str:
    if alt.maturity_level == "alpha" and alt.source_confidence < 0.70:
        return "Reference-only until maturity and source evidence improve."
    if alt.scores["sandbox_isolation"] < 3.0:
        return "Use for human-in-the-loop workflows unless an external sandbox is added."
    if alt.scores["provider_portability"] < 3.0:
        return "Proceed only if provider dependence is acceptable."
    if alt.scores["implementation_ease"] >= 4.0:
        return "Good low-friction smoke-test candidate."
    return "Pilot with explicit policy, telemetry, and rollback criteria."


def estimate_rows(
    raw_data: dict[str, Any],
    alternatives: list[Alternative],
) -> list[dict[str, Any]]:
    raw_by_id = {
        item["id"]: item
        for item in raw_data["alternatives"]
    }
    rows = []
    for alt in alternatives:
        prototype_scope_adjustment = PROTOTYPE_SCOPE_ADJUSTMENT.get(alt.id, 0.5)
        hardening_scope_adjustment = HARDENING_SCOPE_ADJUSTMENT.get(alt.id, 0.8)
        prototype_score = adjusted_complexity(
            complexity_score(alt.scores, PROTOTYPE_WEIGHTS),
            prototype_scope_adjustment,
        )
        hardening_score = adjusted_complexity(
            complexity_score(alt.scores, HARDENING_WEIGHTS),
            hardening_scope_adjustment,
        )
        raw = raw_by_id[alt.id]
        rows.append({
            "alternative_id": alt.id,
            "alternative": alt.name,
            "license": alt.license,
            "maturity_level": alt.maturity_level,
            "source_confidence": alt.source_confidence,
            "prototype_complexity_score": round(prototype_score, 3),
            "prototype_scope_adjustment": prototype_scope_adjustment,
            "prototype_effort": effort_band(prototype_score, PROTOTYPE_BANDS),
            "prototype_driver": top_driver(alt.scores, PROTOTYPE_WEIGHTS),
            "hardening_complexity_score": round(hardening_score, 3),
            "hardening_scope_adjustment": hardening_scope_adjustment,
            "hardening_effort": effort_band(hardening_score, HARDENING_BANDS),
            "hardening_driver": top_driver(alt.scores, HARDENING_WEIGHTS),
            "first_slice": FIRST_SLICE_BY_ID.get(
                alt.id,
                "Install, run one controlled task, capture logs, tests, diff, and review outcome.",
            ),
            "adoption_note": adoption_note(alt),
            "risk_notes": raw["risk_notes"],
        })
    rows.sort(
        key=lambda row: (
            row["hardening_complexity_score"],
            row["prototype_complexity_score"],
            row["alternative"].lower(),
        )
    )
    return rows


def write_effort_outputs(rows: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        output_dir / "implementation_effort_estimates.csv",
        rows,
        [
            "alternative_id",
            "alternative",
            "license",
            "maturity_level",
            "source_confidence",
            "prototype_complexity_score",
            "prototype_scope_adjustment",
            "prototype_effort",
            "prototype_driver",
            "hardening_complexity_score",
            "hardening_scope_adjustment",
            "hardening_effort",
            "hardening_driver",
            "first_slice",
            "adoption_note",
            "risk_notes",
        ],
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=ROOT / "data" / "alternatives.json")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_RESULTS)
    args = parser.parse_args()

    raw_data, alternatives = load_data(args.data)
    validate_data(alternatives)
    rows = estimate_rows(raw_data, alternatives)
    write_effort_outputs(rows, args.output_dir)
    print(f"wrote {len(rows)} implementation effort estimates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
