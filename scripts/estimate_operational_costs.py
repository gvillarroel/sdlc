#!/usr/bin/env python3
"""Estimate relative operating effort and operation-adjusted rankings."""

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
    SCENARIOS,
    Alternative,
    deterministic_rankings,
    load_data,
    validate_data,
    write_csv,
)


DEFAULT_MODEL = ROOT / "data" / "operational_cost_model.json"
DEFAULT_RESULTS = ROOT / "results"
DEFAULT_REPORT = ROOT / "reports" / "operational_cost_model.md"

RISK_BANDS = [
    (2.0, "Low"),
    (3.0, "Moderate"),
    (4.0, "High"),
    (5.0, "Very high"),
]


def load_model(path: Path = DEFAULT_MODEL) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def gap(scores: dict[str, float], criterion: str) -> float:
    return max(0.0, 5.0 - scores[criterion])


def clamp(value: float, lower: float = 1.0, upper: float = 5.0) -> float:
    return max(lower, min(upper, value))


def risk_band(score: float) -> str:
    for upper, label in RISK_BANDS:
        if score <= upper:
            return label
    raise ValueError(f"risk score outside expected range: {score}")


def token_pressure(alt: Alternative) -> float:
    scores = alt.scores
    pressure = (
        1.0
        + (scores["multi_agent"] - 2.5) * 0.07
        + (scores["persistence_memory"] - 2.5) * 0.05
        + gap(scores, "implementation_ease") * 0.04
        - (scores["provider_portability"] - 2.5) * 0.03
        - (scores["observability"] - 2.5) * 0.02
    )
    return max(0.65, min(1.80, pressure))


def latency_risk_score(alt: Alternative, pressure: float) -> float:
    scores = alt.scores
    return clamp(
        1.0
        + gap(scores, "implementation_ease") * 0.35
        + gap(scores, "deployment_flexibility") * 0.25
        + gap(scores, "provider_portability") * 0.15
        + max(0.0, pressure - 1.0) * 1.20
        - max(0.0, scores["observability"] - 3.0) * 0.12
    )


def main_cost_driver(alt: Alternative) -> str:
    scores = alt.scores
    driver_weights = {
        "review_load": gap(scores, "human_control") * 0.25 + gap(scores, "ci_pr") * 0.18,
        "administration": gap(scores, "deployment_flexibility") * 0.25 + gap(scores, "implementation_ease") * 0.20,
        "governance": gap(scores, "security_governance") * 0.25 + gap(scores, "sandbox_isolation") * 0.20,
        "failure_recovery": gap(scores, "maturity") * 0.24 + (1.0 - alt.source_confidence) * 0.60,
        "latency_tuning": token_pressure(alt) * 0.35 + gap(scores, "provider_portability") * 0.10,
    }
    return max(driver_weights.items(), key=lambda item: item[1])[0]


def estimate_profile_row(alt: Alternative, profile: dict[str, Any]) -> dict[str, Any]:
    scores = alt.scores
    tasks = int(profile["monthly_tasks"])
    pressure = token_pressure(alt)
    review_multiplier = (
        1.0
        + gap(scores, "human_control") * 0.08
        + gap(scores, "ci_pr") * 0.05
        + gap(scores, "coding_fit") * 0.04
        + (1.0 - alt.source_confidence) * 0.25
    )
    admin_multiplier = (
        1.0
        + gap(scores, "deployment_flexibility") * 0.10
        + gap(scores, "observability") * 0.08
        + gap(scores, "implementation_ease") * 0.07
        + gap(scores, "maturity") * 0.08
    )
    governance_multiplier = (
        1.0
        + gap(scores, "security_governance") * 0.12
        + gap(scores, "sandbox_isolation") * 0.10
        + gap(scores, "observability") * 0.05
    )
    failure_multiplier = (
        1.0
        + gap(scores, "maturity") * 0.12
        + gap(scores, "sandbox_isolation") * 0.08
        + gap(scores, "observability") * 0.08
        + (1.0 - alt.source_confidence) * 0.40
    )

    review_hours = tasks * float(profile["base_review_minutes_per_task"]) / 60.0 * review_multiplier
    admin_hours = float(profile["base_admin_hours"]) * admin_multiplier
    governance_hours = float(profile["base_governance_hours"]) * governance_multiplier
    failure_buffer_hours = (
        tasks
        * float(profile["incident_buffer_minutes_per_task"])
        / 60.0
        * failure_multiplier
    )
    monthly_hours = review_hours + admin_hours + governance_hours + failure_buffer_hours
    hours_per_task = monthly_hours / tasks
    friction_score = clamp(
        1.0
        + hours_per_task / 0.45
        + gap(scores, "observability") * 0.16
        + gap(scores, "security_governance") * 0.16
        + gap(scores, "maturity") * 0.12
    )
    latency_score = latency_risk_score(alt, pressure)
    return {
        "operating_profile": profile["id"],
        "operating_profile_name": profile["name"],
        "alternative_id": alt.id,
        "alternative": alt.name,
        "monthly_task_volume": tasks,
        "review_hours": round(review_hours, 2),
        "admin_hours": round(admin_hours, 2),
        "governance_hours": round(governance_hours, 2),
        "failure_buffer_hours": round(failure_buffer_hours, 2),
        "monthly_operational_hours": round(monthly_hours, 2),
        "hours_per_task": round(hours_per_task, 3),
        "relative_token_pressure": round(pressure, 3),
        "latency_risk_score": round(latency_score, 3),
        "operational_friction_score": round(friction_score, 3),
        "cost_risk_band": risk_band(friction_score),
        "main_cost_driver": main_cost_driver(alt),
    }


def estimate_rows(model: dict[str, Any], alternatives: list[Alternative]) -> list[dict[str, Any]]:
    profile_order = {
        profile["id"]: index
        for index, profile in enumerate(model["profiles"])
    }
    rows = [
        estimate_profile_row(alt, profile)
        for profile in model["profiles"]
        for alt in alternatives
    ]
    rows.sort(
        key=lambda row: (
            profile_order[row["operating_profile"]],
            row["operational_friction_score"],
            row["monthly_operational_hours"],
            row["alternative"].lower(),
        )
    )
    return rows


def operational_fit_rows(
    model: dict[str, Any],
    alternatives: list[Alternative],
    cost_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    cost_by_profile_and_alt = {
        (row["operating_profile"], row["alternative_id"]): row
        for row in cost_rows
    }
    base_rankings = deterministic_rankings(alternatives)
    rows = []
    for scenario, scenario_rows in base_rankings.items():
        simulation_rank_by_alt = {
            row["alternative_id"]: row["rank"]
            for row in scenario_rows
        }
        for profile in model["profiles"]:
            profile_id = profile["id"]
            penalty = float(profile["operational_penalty_weight"])
            adjusted_rows = []
            for row in scenario_rows:
                cost_row = cost_by_profile_and_alt[(profile_id, row["alternative_id"])]
                friction_penalty = (float(cost_row["operational_friction_score"]) - 1.0) * penalty
                adjusted_rows.append({
                    "scenario": scenario,
                    "operating_profile": profile_id,
                    "alternative_id": row["alternative_id"],
                    "alternative": row["alternative"],
                    "simulation_rank": row["rank"],
                    "simulation_score": row["score"],
                    "operational_friction_score": cost_row["operational_friction_score"],
                    "monthly_operational_hours": cost_row["monthly_operational_hours"],
                    "relative_token_pressure": cost_row["relative_token_pressure"],
                    "latency_risk_score": cost_row["latency_risk_score"],
                    "adjusted_score": row["score"] - friction_penalty,
                })
            adjusted_rows.sort(
                key=lambda item: (
                    -item["adjusted_score"],
                    item["operational_friction_score"],
                    item["alternative"].lower(),
                )
            )
            for index, row in enumerate(adjusted_rows, start=1):
                row["rank"] = index
                row["rank_delta_vs_simulation"] = simulation_rank_by_alt[row["alternative_id"]] - index
                rows.append(row)
    return rows


def top_rows(rows: list[dict[str, Any]], profile_id: str, count: int = 5) -> list[dict[str, Any]]:
    return [row for row in rows if row["operating_profile"] == profile_id][:count]


def largest_rank_shifts(rows: list[dict[str, Any]], count: int = 8) -> list[dict[str, Any]]:
    shifted = [
        row
        for row in rows
        if int(row["rank_delta_vs_simulation"]) != 0
    ]
    shifted.sort(
        key=lambda row: (
            -abs(int(row["rank_delta_vs_simulation"])),
            row["scenario"],
            row["operating_profile"],
            row["rank"],
            row["alternative"].lower(),
        )
    )
    return shifted[:count]


def build_report(
    model: dict[str, Any],
    cost_rows: list[dict[str, Any]],
    fit_rows: list[dict[str, Any]],
) -> str:
    lines = [
        "# Operational Cost Model",
        "",
        "Date: 2026-07-05",
        "",
        "This appendix estimates operational effort for the permissive open-source shortlist. It is not a vendor pricing model. Model and token prices change too frequently, so the output uses relative planning metrics: monthly operating hours, hours per task, token-pressure index, latency-risk score, and an operation-adjusted scenario ranking.",
        "",
        "Inputs: `data/operational_cost_model.json`, `data/alternatives.json`, and the existing 0-5 criteria scores. Generated outputs: `results/operational_cost_estimates.csv` and `results/operational_fit_rankings.csv`.",
        "",
        "## Operating Profiles",
        "",
        "| Profile | Monthly tasks | Review min/task | Admin hours | Governance hours | Incident min/task |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for profile in model["profiles"]:
        lines.append(
            "| {name} | {tasks} | {review} | {admin} | {governance} | {incident} |".format(
                name=profile["name"],
                tasks=profile["monthly_tasks"],
                review=profile["base_review_minutes_per_task"],
                admin=profile["base_admin_hours"],
                governance=profile["base_governance_hours"],
                incident=profile["incident_buffer_minutes_per_task"],
            )
        )

    lines.extend([
        "",
        "## Lowest-Friction Candidates",
        "",
    ])
    for profile in model["profiles"]:
        rows = top_rows(cost_rows, profile["id"])
        lines.extend([
            f"### {profile['name']}",
            "",
            "| Rank | Candidate | Monthly hours | Hours/task | Token pressure | Latency risk | Band | Main driver |",
            "|---:|---|---:|---:|---:|---:|---|---|",
        ])
        for index, row in enumerate(rows, start=1):
            lines.append(
                "| {rank} | {alternative} | {hours:.2f} | {hpt:.3f} | {token:.3f} | {latency:.3f} | {band} | {driver} |".format(
                    rank=index,
                    alternative=row["alternative"],
                    hours=float(row["monthly_operational_hours"]),
                    hpt=float(row["hours_per_task"]),
                    token=float(row["relative_token_pressure"]),
                    latency=float(row["latency_risk_score"]),
                    band=row["cost_risk_band"],
                    driver=row["main_cost_driver"],
                )
            )
        lines.append("")

    lines.extend([
        "## Operation-Adjusted Scenario Winners",
        "",
        "| Scenario | Profile | Rank 1 | Adjusted score | Simulation rank | Rank delta |",
        "|---|---|---|---:|---:|---:|",
    ])
    for scenario in SCENARIOS:
        for profile in model["profiles"]:
            winner = next(
                row
                for row in fit_rows
                if row["scenario"] == scenario
                and row["operating_profile"] == profile["id"]
                and row["rank"] == 1
            )
            lines.append(
                "| {scenario} | {profile} | {alternative} | {score:.3f} | {simulation_rank} | {delta} |".format(
                    scenario=scenario,
                    profile=profile["id"],
                    alternative=winner["alternative"],
                    score=float(winner["adjusted_score"]),
                    simulation_rank=winner["simulation_rank"],
                    delta=winner["rank_delta_vs_simulation"],
                )
            )

    shifts = largest_rank_shifts(fit_rows)
    lines.extend([
        "",
        "## Largest Operation-Adjusted Rank Shifts",
        "",
        "| Scenario | Profile | Candidate | Simulation rank | Adjusted rank | Delta | Adjusted score |",
        "|---|---|---|---:|---:|---:|---:|",
    ])
    for row in shifts:
        lines.append(
            "| {scenario} | {profile} | {alternative} | {simulation_rank} | {rank} | {delta} | {score:.3f} |".format(
                scenario=row["scenario"],
                profile=row["operating_profile"],
                alternative=row["alternative"],
                simulation_rank=row["simulation_rank"],
                rank=row["rank"],
                delta=row["rank_delta_vs_simulation"],
                score=float(row["adjusted_score"]),
            )
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "- Low-friction operating cost does not automatically mean best strategic fit. It identifies where review, administration, governance, and failure-recovery overhead are likely to be lower.",
        "- Multi-agent and durable-memory systems can carry more token and latency pressure even when they are architecturally attractive. The pilot should capture actual token usage, wall-clock latency, failed-run recovery time, and reviewer intervention count.",
        "- The operation-adjusted score is intentionally conservative: it starts from the same simulation score and subtracts a profile-specific penalty for operational friction. It should be used as a tie-breaker, not as a replacement for the main simulation.",
        "- The model excludes vendor price tables, hosted-seat costs, and internal labor rates. Add those after a pilot once the organization knows provider, model, and reviewer workflow choices.",
        "",
    ])
    return "\n".join(lines).rstrip() + "\n"


def write_outputs(
    cost_rows: list[dict[str, Any]],
    fit_rows: list[dict[str, Any]],
    output_dir: Path,
    report_output: Path,
    model: dict[str, Any],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    write_csv(
        output_dir / "operational_cost_estimates.csv",
        cost_rows,
        [
            "operating_profile",
            "operating_profile_name",
            "alternative_id",
            "alternative",
            "monthly_task_volume",
            "review_hours",
            "admin_hours",
            "governance_hours",
            "failure_buffer_hours",
            "monthly_operational_hours",
            "hours_per_task",
            "relative_token_pressure",
            "latency_risk_score",
            "operational_friction_score",
            "cost_risk_band",
            "main_cost_driver",
        ],
    )
    write_csv(
        output_dir / "operational_fit_rankings.csv",
        fit_rows,
        [
            "scenario",
            "operating_profile",
            "rank",
            "alternative_id",
            "alternative",
            "simulation_rank",
            "simulation_score",
            "operational_friction_score",
            "monthly_operational_hours",
            "relative_token_pressure",
            "latency_risk_score",
            "adjusted_score",
            "rank_delta_vs_simulation",
        ],
    )
    report_output.write_text(
        build_report(model, cost_rows, fit_rows),
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=ROOT / "data" / "alternatives.json")
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    model = load_model(args.model)
    _raw_data, alternatives = load_data(args.data)
    validate_data(alternatives)
    cost_rows = estimate_rows(model, alternatives)
    fit_rows = operational_fit_rows(model, alternatives, cost_rows)
    write_outputs(cost_rows, fit_rows, args.output_dir, args.report_output, model)
    print(f"wrote {len(cost_rows)} operational cost rows and {len(fit_rows)} fit rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
