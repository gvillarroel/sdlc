# Pilot Sample Size Estimate

Date: 2026-07-05

This appendix estimates how many pilot tasks per candidate are needed to distinguish close shortlist candidates. It is a planning simulation, not proof of live performance. The model maps the 0-5 scenario simulation score to an assumed task success rate, then simulates observed wins across repeated pilot task sets.

Inputs: `data/pilot_sample_size_model.json` and `data/alternatives.json`. Generated output: `results/pilot_sample_size_estimates.csv`.

## Assumptions

| Assumption | Value |
|---|---:|
| Success-rate floor | 0.45 |
| Success-rate ceiling | 0.88 |
| Simulation trials per comparison | 5000 |
| Decision confidence target | 0.8 |

## Recommended Task Counts

| Scenario | Comparison | Recommended tasks/candidate | Top win probability | Tie probability | Recommendation |
|---|---|---:|---:|---:|---|
| custom_orchestrator_platform | Rank 2: OpenHands Software Agent SDK | >60 | 0.456 | 0.094 | Increase tasks or treat as unresolved |
| custom_orchestrator_platform | Rank 3: Deep Agents | >60 | 0.469 | 0.093 | Increase tasks or treat as unresolved |
| enterprise_control_plane | Rank 2: OpenHands Software Agent SDK | >60 | 0.492 | 0.093 | Increase tasks or treat as unresolved |
| enterprise_control_plane | Rank 3: Deep Agents | >60 | 0.497 | 0.090 | Increase tasks or treat as unresolved |
| quick_local_coding | Rank 2: OpenHands Software Agent SDK | >60 | 0.520 | 0.084 | Increase tasks or treat as unresolved |
| quick_local_coding | Rank 3: OpenCode | >60 | 0.568 | 0.086 | Increase tasks or treat as unresolved |
| research_benchmarking | Rank 2: SWE-agent | >60 | 0.518 | 0.095 | Increase tasks or treat as unresolved |
| research_benchmarking | Rank 3: OpenHands Software Agent SDK | >60 | 0.529 | 0.098 | Increase tasks or treat as unresolved |
| secure_autonomous_prs | Rank 2: OpenHands Software Agent SDK | >60 | 0.468 | 0.097 | Increase tasks or treat as unresolved |
| secure_autonomous_prs | Rank 3: Cline / Cline SDK | >60 | 0.468 | 0.098 | Increase tasks or treat as unresolved |

## Interpretation

- Close deterministic scores usually require more tasks than a two-week pilot can comfortably run. If the model recommends more than 60 tasks per candidate, treat the candidates as a tie cluster and rely on qualitative review, safety gates, and operational fit.
- Task-count estimates assume the task suite is balanced and comparable across candidates. Reusing the same task distribution from `data/pilot_tasks.json` matters more than increasing raw volume with unrepresentative tasks.
- Replace the score-to-success mapping with measured pilot pass rates after the first pilot wave. At that point, this model becomes a recalibration tool rather than a desk-review estimate.
