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

## Sensitivity Analysis

For each scenario and criterion, the script computes:

- ranking with the criterion weight halved
- ranking with the criterion weight doubled
- top-3 overlap against the base ranking

This identifies whether a scenario has a robust winner or a fragile top cluster.

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

## Confidence And Evidence

Source confidence is a manual value from 0 to 1. It reflects repository clarity, license clarity, docs, release posture, and whether the project appears canonical.

Evidence is exported to `results/evidence_matrix.csv`. Live URL status is exported to `results/source_check.csv`.

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
