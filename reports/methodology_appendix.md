# Methodology Appendix

Date: 2026-07-05

## Objective

The evaluation answers one screening question: among the alternatives from the shared discussion, which permissive open-source options are worth piloting for AI coding-agent orchestration?

It does not claim to measure actual coding performance. It ranks candidates by decision criteria, evidence confidence, and uncertainty so the pilot can focus on the most plausible options.

## License Filter

Included licenses:

- MIT
- Apache-2.0

Excluded entries:

- Claude Agent SDK
- Codex app

The generated audit is `results/license_audit.csv`.

## Criteria

Each alternative receives a score from 0 to 5 on 14 criteria:

- `implementation_ease`
- `maturity`
- `provider_portability`
- `sandbox_isolation`
- `persistence_memory`
- `multi_agent`
- `human_control`
- `ci_pr`
- `observability`
- `security_governance`
- `extensibility`
- `deployment_flexibility`
- `coding_fit`
- `research_reproducibility`

Definitions are exported to `results/criteria_definitions.csv`.

The scoring anchors are documented in `data/scoring_rubric.json`. Each criterion has low, mid, and high anchors for the 0-5 scale so future reviewers can adjust scores consistently.

## Weighted Scenario Score

For an alternative `a` and scenario `s`, the deterministic score is:

```text
score(a, s) = sum(score(a, c) * weight(s, c) for c in criteria) / sum(weight(s, c) for c in criteria)
```

Scenario weights are exported to `results/scenario_weights.csv` with both raw and normalized values.

## Monte Carlo Model

The Monte Carlo simulation runs 5,000 trials by default.

For each trial:

1. Scenario weights are perturbed with a log-normal multiplier.
2. Each criterion score is perturbed with a normal distribution.
3. Perturbed scores are clamped to the 0-5 range.
4. Alternatives are ranked for the scenario.
5. Win rate, top-3 rate, mean score, score bands, and mean rank are accumulated.

The weight perturbation is:

```text
perturbed_weight(c) = base_weight(c) * exp(N(0, weight_sigma))
```

The score perturbation standard deviation depends on maturity and source confidence:

```text
sigma(a) = min(1.15, maturity_sigma(a) + (1 - source_confidence(a)) * 0.8)
```

Maturity sigma:

| Maturity | Sigma |
|---|---:|
| Production | 0.25 |
| Beta | 0.45 |
| Alpha | 0.75 |

This means alpha or weakly verified projects can still rank well if their feature scores are strong, but the model treats their outcomes as less certain.

The stress-test runner reuses the same Monte Carlo implementation with alternate `weight_sigma` values and a `score_sigma_multiplier` parameter. The base report keeps the default score uncertainty multiplier at `1.0`; stress cases raise or lower it to test how fragile the ranking is when analyst score uncertainty changes.

## Sensitivity Analysis

For each scenario and criterion, the script computes:

- ranking with the criterion weight halved
- ranking with the criterion weight doubled
- top-3 overlap against the base ranking

This identifies whether a scenario has a robust winner or a fragile top cluster.

## Robustness Outputs

The simulator also emits three robustness views:

| Output | Meaning |
|---|---|
| `results/regret_analysis.csv` | For each scenario, the deterministic score gap between every candidate and the scenario winner. A tiny regret means the practical difference is negligible. |
| `results/pareto_frontier.csv` | Whether a candidate is strictly dominated across all criteria. A dominated candidate is no better on any criterion and worse on at least one criterion versus another candidate. |
| `results/rank_stability.csv` | Average deterministic rank, best/worst rank, number of top-3 scenarios, mean Monte Carlo rank, and mean top-3 rate. |

The Pareto frontier is computed over the raw criteria, not scenario-weighted scores. This intentionally answers a different question: whether a candidate has any criterion-level advantage before use-case weighting.

## Assumption Stress Tests

The assumption and stress-test appendix is `reports/simulation_assumptions.md`. The machine-readable assumption register is `data/simulation_assumptions.json`.

Run:

```powershell
python scripts/stress_test_simulation.py --trials 1500 --seed 9011
```

This produces:

- `results/stress_test_summary.csv`
- `results/stress_test_rankings.csv`
- `results/uncertainty_stress_summary.csv`
- `results/uncertainty_stress_details.csv`

These outputs intentionally test model fragility, not live coding performance. They answer whether the shortlist changes when security, provider neutrality, adoption speed, research reproducibility, maturity, evidence confidence, sandbox assumptions, or uncertainty levels are stressed.

## Custom Scenario Weights

Custom deterministic rankings can be generated without editing the base simulation script:

```powershell
python scripts/rank_with_custom_weights.py --weights examples/custom_weights.example.json --output results/custom_weights_example_rankings.csv
```

The weights file must contain one or more named scenarios, each with every criterion from the scoring model. This is the fastest way to test stakeholder-specific priorities before changing the canonical scenario set.

## Category Scorecards

Category scorecards group criteria before scenario weights are applied:

| Category | Criteria |
|---|---|
| Adoption readiness | implementation ease, maturity, deployment flexibility |
| Agent architecture | provider portability, persistence/memory, multi-agent, extensibility, coding fit |
| Execution safety | sandbox isolation, human control, security governance |
| Operations | CI/PR, observability, deployment flexibility |
| Research fit | research reproducibility, implementation ease, observability, provider portability |

The generated output is `results/category_scores.csv`.

## Implementation Effort Model

The generated effort estimate is `results/implementation_effort_estimates.csv`, produced by:

```powershell
python scripts/estimate_implementation_effort.py
```

It computes two separate 1-5 complexity scores:

- Prototype complexity: driven by implementation ease, extensibility, coding fit, provider portability, deployment flexibility, and a scope adjustment for platform breadth.
- Hardening complexity: driven by maturity, sandboxing, security/governance, observability, CI/PR fit, deployment flexibility, and a scope adjustment for operational breadth.

The scope adjustment is explicit in the script because a broad async PR platform can score well technically while still requiring more integration work than a local CLI.

## Operational Cost Model

The generated operating-cost estimates are `results/operational_cost_estimates.csv` and `results/operational_fit_rankings.csv`, produced by:

```powershell
python scripts/estimate_operational_costs.py
```

The model uses `data/operational_cost_model.json` to define three operating profiles: a controlled pilot, a team rollout, and an autonomous PR lane. It estimates review hours, administration hours, governance hours, failure-recovery buffer, relative token pressure, latency risk, and an operation-adjusted ranking.

The operation-adjusted ranking starts from the same scenario simulation score, then subtracts a profile-specific penalty for operating friction. It is a tie-breaker for adoption planning, not a replacement for live pilot evidence or provider-specific cost data.

## Pilot Sample-Size Model

The generated task-count estimate is `results/pilot_sample_size_estimates.csv`, produced by:

```powershell
python scripts/estimate_pilot_sample_sizes.py
```

The model uses `data/pilot_sample_size_model.json` to map the 0-5 scenario simulation score into an assumed task success rate, then repeatedly simulates observed pass-rate comparisons between the scenario winner and the rank 2 and rank 3 candidates. It estimates whether the top candidate would beat a close comparison candidate at the configured confidence target for 10, 20, 30, 40, and 60 tasks per candidate.

This is intentionally conservative. If the model says the candidates remain unresolved, the pilot should treat them as a tie cluster and decide with safety gates, reviewer judgment, operational fit, and measured cost/latency.

## Confidence And Evidence

Source confidence is a manual value from 0 to 1. It reflects repository clarity, license clarity, docs, release posture, and whether the project appears canonical.

Evidence is exported to `results/evidence_matrix.csv`. Live URL status is exported to `results/source_check.csv`.

Evidence gaps are exported to `results/evidence_gap_analysis.csv` by:

```powershell
python scripts/analyze_evidence_gaps.py
```

The evidence-gap score combines source confidence, maturity, release availability, repository traction, evidence URL count, freshness, and repository age. It is a review-priority signal, not a direct product-quality score.

Live GitHub metadata is exported to `results/github_metadata_check.csv` by:

```powershell
python scripts/refresh_github_metadata.py --timeout 20
```

This live check is intentionally optional because it depends on the GitHub API. The committed CSV records the latest successful check and the offline validation verifies that all checked repositories resolved, licenses matched, and none were archived.

## Known Limitations

- Scores are analyst judgments, not measured execution results.
- GitHub stars are weak signals and should not be read as quality scores.
- The model does not normalize for project age beyond the maturity/confidence values.
- The same framework can perform differently under different models, prompts, tools, and sandbox providers.
- Some candidates are products or CLIs more than libraries; the model intentionally compares them because the adoption decision often mixes those categories.
- The model does not replace a real pilot on representative repositories.

## How To Customize

To adapt this evaluation:

1. Edit `data/alternatives.json` scores or evidence.
2. Edit scenario weights in `scripts/simulate_alternatives.py`.
3. Run `python scripts/simulate_alternatives.py --trials 5000 --seed 7331`.
4. Review `results/decision_shortlist.csv`, `results/sensitivity_summary.csv`, and `results/category_scores.csv`.
5. Run the pilot tasks in `data/pilot_tasks.json` against the new shortlist.
