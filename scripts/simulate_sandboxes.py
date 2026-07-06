#!/usr/bin/env python3
"""Evaluate sandbox options for AI-agent code execution."""

from __future__ import annotations

import argparse
import csv
import json
import random
import statistics
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "sandbox_evaluation.json"
DEFAULT_RESULTS = ROOT / "results"
DEFAULT_REPORT = ROOT / "reports" / "sandbox_report.md"


def load_data(path: Path = DEFAULT_DATA) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def managed_dependency_risk(sandbox: dict[str, Any]) -> float:
    availability = sandbox["availability"]
    sandbox_type = sandbox["type"]
    if availability == "managed_cloud":
        return 1.0
    if availability == "managed_cloud_with_open_source_components":
        return 0.75
    if availability == "managed_cloud_with_open_source_platform":
        return 0.65
    if availability == "open_source_and_hosted_runtime_options":
        return 0.35
    if availability == "managed_microvm_sandbox":
        return 1.0
    if "managed" in sandbox_type or availability.startswith("managed"):
        return 0.8
    if "agent_framework" in sandbox_type:
        return 0.1
    if "agent_cli" in sandbox_type:
        return 0.45
    return 0.0


def weighted_score(
    scores: dict[str, float],
    weights: dict[str, float],
    managed_penalty: float = 0.0,
    dependency_risk: float = 0.0,
) -> float:
    total_weight = sum(weights.values())
    base_score = sum(scores[criterion] * weight for criterion, weight in weights.items()) / total_weight
    return max(0.0, base_score - managed_penalty * dependency_risk)


def deterministic_rankings(data: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    output: dict[str, list[dict[str, Any]]] = {}
    for scenario_id, scenario in data["scenarios"].items():
        rows = []
        for sandbox in data["sandboxes"]:
            rows.append({
                "scenario": scenario_id,
                "scenario_label": scenario["label"],
                "sandbox_id": sandbox["id"],
                "sandbox": sandbox["name"],
                "type": sandbox["type"],
                "score": round(
                    weighted_score(
                        sandbox["scores"],
                        scenario["weights"],
                        scenario.get("managed_dependency_penalty", 0.0),
                        managed_dependency_risk(sandbox),
                    ),
                    4,
                ),
            })
        rows.sort(key=lambda row: (-row["score"], row["sandbox"]))
        for index, row in enumerate(rows, start=1):
            row["rank"] = index
        output[scenario_id] = rows
    return output


def score_uncertainty(sandbox: dict[str, Any]) -> float:
    availability = sandbox["availability"]
    maturity = sandbox["scores"]["maturity"]
    if "managed_cloud" in availability:
        base = 0.22
    elif "agent" in sandbox["type"]:
        base = 0.24
    else:
        base = 0.18
    return base + max(0.0, 4.2 - maturity) * 0.07


def monte_carlo_rankings(
    data: dict[str, Any],
    trials: int,
    seed: int,
) -> dict[str, list[dict[str, Any]]]:
    rng = random.Random(seed)
    collected: dict[tuple[str, str], dict[str, list[float] | int | str]] = {}
    scenarios = data["scenarios"]
    sandboxes = data["sandboxes"]

    for scenario_id, scenario in scenarios.items():
        for sandbox in sandboxes:
            collected[(scenario_id, sandbox["id"])] = {
                "scenario": scenario_id,
                "sandbox_id": sandbox["id"],
                "sandbox": sandbox["name"],
                "scores": [],
                "ranks": [],
                "wins": 0,
                "top3": 0,
            }

    for _ in range(trials):
        for scenario_id, scenario in scenarios.items():
            weights = {
                criterion: max(0.05, rng.gauss(weight, 0.12 * weight))
                for criterion, weight in scenario["weights"].items()
            }
            trial_rows = []
            for sandbox in sandboxes:
                sigma = score_uncertainty(sandbox)
                sampled_scores = {
                    criterion: min(5.0, max(0.0, rng.gauss(score, sigma)))
                    for criterion, score in sandbox["scores"].items()
                }
                trial_rows.append((
                    sandbox["id"],
                    weighted_score(
                        sampled_scores,
                        weights,
                        scenario.get("managed_dependency_penalty", 0.0),
                        managed_dependency_risk(sandbox),
                    ),
                ))
            trial_rows.sort(key=lambda row: (-row[1], row[0]))
            for rank, (sandbox_id, score) in enumerate(trial_rows, start=1):
                bucket = collected[(scenario_id, sandbox_id)]
                bucket["scores"].append(score)  # type: ignore[union-attr]
                bucket["ranks"].append(rank)  # type: ignore[union-attr]
                if rank == 1:
                    bucket["wins"] = int(bucket["wins"]) + 1
                if rank <= 3:
                    bucket["top3"] = int(bucket["top3"]) + 1

    output: dict[str, list[dict[str, Any]]] = {}
    for scenario_id in scenarios:
        rows = []
        for sandbox in sandboxes:
            bucket = collected[(scenario_id, sandbox["id"])]
            scores = bucket["scores"]  # type: ignore[assignment]
            ranks = bucket["ranks"]  # type: ignore[assignment]
            rows.append({
                "scenario": scenario_id,
                "sandbox_id": sandbox["id"],
                "sandbox": sandbox["name"],
                "mean_score": round(statistics.fmean(scores), 4),
                "p10_score": round(quantile(scores, 0.10), 4),
                "p90_score": round(quantile(scores, 0.90), 4),
                "mean_rank": round(statistics.fmean(ranks), 4),
                "win_rate": round(int(bucket["wins"]) / trials, 4),
                "top3_rate": round(int(bucket["top3"]) / trials, 4),
                "trials": trials,
            })
        rows.sort(key=lambda row: (row["mean_rank"], -row["mean_score"], row["sandbox"]))
        output[scenario_id] = rows
    return output


def quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    index = int(round((len(ordered) - 1) * q))
    return ordered[index]


def threat_coverage_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for threat in data["threats"]:
        controls = threat["required_controls"]
        for sandbox in data["sandboxes"]:
            control_scores = [sandbox["scores"][control] for control in controls]
            coverage = statistics.fmean(control_scores)
            if coverage >= 4.2:
                band = "strong"
            elif coverage >= 3.4:
                band = "adequate"
            elif coverage >= 2.7:
                band = "partial"
            else:
                band = "weak"
            rows.append({
                "threat_id": threat["id"],
                "threat": threat["threat"],
                "sandbox_id": sandbox["id"],
                "sandbox": sandbox["name"],
                "required_controls": "; ".join(controls),
                "coverage_score": round(coverage, 3),
                "coverage_band": band,
            })
    rows.sort(key=lambda row: (row["threat_id"], -row["coverage_score"], row["sandbox"]))
    return rows


def decision_matrix_rows(
    deterministic: dict[str, list[dict[str, Any]]],
    monte_carlo: dict[str, list[dict[str, Any]]],
    data: dict[str, Any],
    top_n: int = 5,
) -> list[dict[str, Any]]:
    sandbox_by_id = {sandbox["id"]: sandbox for sandbox in data["sandboxes"]}
    rows = []
    for scenario_id, ranking in deterministic.items():
        mc_by_id = {row["sandbox_id"]: row for row in monte_carlo[scenario_id]}
        for row in ranking[:top_n]:
            sandbox = sandbox_by_id[row["sandbox_id"]]
            mc = mc_by_id[row["sandbox_id"]]
            posture = recommendation_posture(
                rank=int(row["rank"]),
                score=float(row["score"]),
                win_rate=float(mc["win_rate"]),
                top3_rate=float(mc["top3_rate"]),
                self_hosting=float(sandbox["scores"]["self_hosting_control"]),
                isolation=float(sandbox["scores"]["isolation_strength"]),
            )
            rows.append({
                "scenario": scenario_id,
                "scenario_label": row["scenario_label"],
                "rank": row["rank"],
                "sandbox_id": row["sandbox_id"],
                "sandbox": row["sandbox"],
                "type": row["type"],
                "deterministic_score": row["score"],
                "monte_carlo_mean_rank": mc["mean_rank"],
                "win_rate": mc["win_rate"],
                "top3_rate": mc["top3_rate"],
                "posture": posture,
                "best_for": sandbox["best_for"],
                "watch_for": sandbox["watch_for"],
            })
    return rows


def recommendation_posture(
    rank: int,
    score: float,
    win_rate: float,
    top3_rate: float,
    self_hosting: float,
    isolation: float,
) -> str:
    if rank == 1 and win_rate >= 0.35 and top3_rate >= 0.75:
        return "Primary candidate"
    if rank <= 3 and top3_rate >= 0.55:
        return "Pilot head-to-head"
    if isolation >= 4.4 and self_hosting >= 4.5:
        return "Security architecture option"
    if score >= 3.8 and top3_rate >= 0.25:
        return "Fallback or benchmark"
    return "Watchlist"


def source_rows(data: dict[str, Any]) -> list[dict[str, str]]:
    rows = []
    for sandbox in data["sandboxes"]:
        for url in sandbox["source_urls"]:
            rows.append({
                "sandbox_id": sandbox["id"],
                "sandbox": sandbox["name"],
                "url": url,
            })
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def flatten_rankings(rankings: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    return [row for rows in rankings.values() for row in rows]


def build_report(
    data: dict[str, Any],
    deterministic: dict[str, list[dict[str, Any]]],
    monte_carlo: dict[str, list[dict[str, Any]]],
    threat_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
) -> str:
    lines = [
        "# Sandbox Evaluation Report",
        "",
        "Date: 2026-07-05",
        "",
        "## Executive Summary",
        "",
        "Sandbox choice is not a single technology decision. For AI coding agents, the right boundary depends on whether the workload is local development, autonomous pull requests, arbitrary user code, high-scale evaluations, or enterprise self-hosted control.",
        "",
        "The simulation ranks sandbox options across five scenarios using 14 criteria: isolation strength, workspace reset, network control, secret boundary, filesystem mount control, dependency support, agent SDK fit, observability, startup speed, horizontal scale, self-hosting control, operational ease, cost predictability, and maturity. Local and self-hosted scenarios also apply an explicit managed-service dependency penalty.",
        "",
        "Generated outputs:",
        "",
        "| File | Purpose |",
        "|---|---|",
        "| `results/sandbox_deterministic_rankings.csv` | Weighted sandbox ranking by scenario. |",
        "| `results/sandbox_monte_carlo_summary.csv` | Ranking stability under score and weight uncertainty. |",
        "| `results/sandbox_threat_coverage.csv` | Threat-to-control coverage by sandbox option. |",
        "| `results/sandbox_decision_matrix.csv` | Scenario shortlist with recommendation posture and caveats. |",
        "| `results/sandbox_source_matrix.csv` | Official source URLs used by the sandbox dataset. |",
        "",
        "## Recommendations",
        "",
        "| Scenario | Recommendation | Why |",
        "|---|---|---|",
    ]
    for scenario_id in deterministic:
        scenario_rows = [row for row in decision_rows if row["scenario"] == scenario_id]
        primary = [row for row in scenario_rows if row["posture"] == "Primary candidate"]
        if primary:
            top = primary[0]
            recommendation = top["sandbox"]
            why = (
                f"Score {float(top['deterministic_score']):.3f}; "
                f"{float(top['top3_rate']):.0%} top-3 stability; {top['best_for']}"
            )
        else:
            shortlist = scenario_rows[:3]
            recommendation = " / ".join(row["sandbox"] for row in shortlist)
            why = "No decisive single winner; run a head-to-head pilot because the top cluster is close under uncertainty."
        lines.append(
            "| {scenario} | {recommendation} | {why} |".format(
                scenario=scenario_rows[0]["scenario_label"],
                recommendation=recommendation,
                why=why,
            )
        )

    lines.extend([
        "",
        "## Scenario Decision Matrix",
        "",
        "| Scenario | Rank | Sandbox | Type | Score | Mean rank | Win | Top-3 | Posture | Main caveat |",
        "|---|---:|---|---|---:|---:|---:|---:|---|---|",
    ])
    for row in decision_rows:
        lines.append(
            "| {scenario} | {rank} | {sandbox} | {type} | {score:.3f} | {mean_rank:.2f} | {win:.0%} | {top3:.0%} | {posture} | {watch_for} |".format(
                scenario=row["scenario_label"],
                rank=row["rank"],
                sandbox=row["sandbox"],
                type=row["type"],
                score=float(row["deterministic_score"]),
                mean_rank=float(row["monte_carlo_mean_rank"]),
                win=float(row["win_rate"]),
                top3=float(row["top3_rate"]),
                posture=row["posture"],
                watch_for=row["watch_for"],
            )
        )

    lines.extend([
        "",
        "## Sandbox Taxonomy",
        "",
        "| Type | What it means | Typical examples |",
        "|---|---|---|",
        "| Process sandbox | Constrains one command or process using namespaces, cgroups, seccomp, chroot, or similar controls. | nsjail, bubblewrap |",
        "| Container runtime | Provides disposable build/test environments with familiar images and tooling. | Docker rootless, Podman rootless |",
        "| Userspace kernel | Inserts an application kernel between the workload and host kernel. | gVisor runsc |",
        "| MicroVM or VM-backed containers | Uses hardware virtualization boundaries while preserving some container ergonomics. | Firecracker, Kata Containers, Vercel Sandbox |",
        "| Managed agent sandbox | Provides API-driven sandbox lifecycle for agents. | E2B, Daytona, Modal, OpenHands runtime API |",
        "| Agent control sandbox | Constrains an agent's tool calls through local workspace, network, and approval policy. | Codex sandbox, framework-level providers |",
        "",
        "## Threat Coverage Highlights",
        "",
        "| Threat | Strongest options | Weakest pattern to avoid |",
        "|---|---|---|",
    ])
    for threat in data["threats"]:
        rows = [row for row in threat_rows if row["threat_id"] == threat["id"]]
        strongest = "; ".join(row["sandbox"] for row in rows[:3])
        weak = rows[-1]["sandbox"]
        lines.append(f"| {threat['threat']} | {strongest} | {weak} |")

    lines.extend([
        "",
        "## Implementation Guidance",
        "",
        "1. Do not treat approval prompts as equivalent to hard isolation. Approval policy is useful, but it does not replace a host, kernel, filesystem, or network boundary.",
        "2. Default to disposable workspaces. Long-lived sandboxes should be explicit exceptions with retention, quota, and credential rules.",
        "3. Keep credentials outside the sandbox until a specific tool call needs them, and prefer short-lived scoped credentials.",
        "4. Disable network by default for autonomous code execution, then add domain allowlists for package registries, Git remotes, and required APIs.",
        "5. For arbitrary user code, prefer microVM, userspace-kernel, VM-backed container, or managed sandbox options over plain containers.",
        "6. For local developer agents, combine rootless containers or Codex-style workspace/network policies with explicit mount rules and review checkpoints.",
        "7. For self-hosted enterprise deployments, test Kubernetes hardened pods alone and with gVisor or Kata RuntimeClass before accepting container isolation as sufficient.",
        "",
        "## Source Notes",
        "",
        "The dataset uses official documentation and source repositories for Docker, Podman, gVisor, Firecracker, Kata Containers, nsjail, bubblewrap, E2B, Daytona, Modal, Vercel, OpenHands, Codex, Sandcastle, Flue, and Kubernetes. See `results/sandbox_source_matrix.csv` for the exact URLs.",
        "",
        "## Validation Boundary",
        "",
        "This report is a screening simulation. It does not prove that a particular hosted sandbox prevents escapes, protects secrets, or meets compliance needs. Before production use, run the security fixtures in `data/security_evaluation_fixtures.json`, add sandbox-specific escape and exfiltration tests, capture logs in `templates/pilot_run_log.csv`, and review the provider's legal and security documentation.",
        "",
    ])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--trials", type=int, default=4000)
    parser.add_argument("--seed", type=int, default=260705)
    args = parser.parse_args()

    data = load_data(args.data)
    deterministic = deterministic_rankings(data)
    monte_carlo = monte_carlo_rankings(data, args.trials, args.seed)
    threat_rows = threat_coverage_rows(data)
    decision_rows = decision_matrix_rows(deterministic, monte_carlo, data)
    sources = source_rows(data)

    write_csv(
        args.output_dir / "sandbox_deterministic_rankings.csv",
        flatten_rankings(deterministic),
        ["scenario", "scenario_label", "rank", "sandbox_id", "sandbox", "type", "score"],
    )
    write_csv(
        args.output_dir / "sandbox_monte_carlo_summary.csv",
        flatten_rankings(monte_carlo),
        [
            "scenario",
            "sandbox_id",
            "sandbox",
            "mean_score",
            "p10_score",
            "p90_score",
            "mean_rank",
            "win_rate",
            "top3_rate",
            "trials",
        ],
    )
    write_csv(
        args.output_dir / "sandbox_threat_coverage.csv",
        threat_rows,
        [
            "threat_id",
            "threat",
            "sandbox_id",
            "sandbox",
            "required_controls",
            "coverage_score",
            "coverage_band",
        ],
    )
    write_csv(
        args.output_dir / "sandbox_decision_matrix.csv",
        decision_rows,
        [
            "scenario",
            "scenario_label",
            "rank",
            "sandbox_id",
            "sandbox",
            "type",
            "deterministic_score",
            "monte_carlo_mean_rank",
            "win_rate",
            "top3_rate",
            "posture",
            "best_for",
            "watch_for",
        ],
    )
    write_csv(
        args.output_dir / "sandbox_source_matrix.csv",
        sources,
        ["sandbox_id", "sandbox", "url"],
    )
    args.report.write_text(
        build_report(data, deterministic, monte_carlo, threat_rows, decision_rows),
        encoding="utf-8",
        newline="\n",
    )
    print(
        "wrote sandbox evaluation: "
        f"{len(data['sandboxes'])} sandboxes, "
        f"{len(data['scenarios'])} scenarios, "
        f"{args.trials} trials"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
