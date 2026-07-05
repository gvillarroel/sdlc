# Operational Cost Model

Date: 2026-07-05

This appendix estimates operational effort for the permissive open-source shortlist. It is not a vendor pricing model. Model and token prices change too frequently, so the output uses relative planning metrics: monthly operating hours, hours per task, token-pressure index, latency-risk score, and an operation-adjusted scenario ranking.

Inputs: `data/operational_cost_model.json`, `data/alternatives.json`, and the existing 0-5 criteria scores. Generated outputs: `results/operational_cost_estimates.csv` and `results/operational_fit_rankings.csv`.

## Operating Profiles

| Profile | Monthly tasks | Review min/task | Admin hours | Governance hours | Incident min/task |
|---|---:|---:|---:|---:|---:|
| Controlled pilot, 100 tasks/month | 100 | 18 | 6 | 4 | 4 |
| Team rollout, 400 tasks/month | 400 | 12 | 14 | 8 | 3 |
| Autonomous PR lane, 1000 tasks/month | 1000 | 10 | 24 | 14 | 5 |

## Lowest-Friction Candidates

### Controlled pilot, 100 tasks/month

| Rank | Candidate | Monthly hours | Hours/task | Token pressure | Latency risk | Band | Main driver |
|---:|---|---:|---:|---:|---:|---|---|
| 1 | Codex CLI | 52.80 | 0.528 | 1.171 | 2.089 | Moderate | latency_tuning |
| 2 | Cline / Cline SDK | 53.59 | 0.536 | 1.130 | 1.486 | Moderate | governance |
| 3 | Deep Agents | 57.65 | 0.577 | 1.200 | 1.783 | Moderate | review_load |
| 4 | OpenHands Software Agent SDK | 56.09 | 0.561 | 1.150 | 1.684 | Moderate | review_load |
| 5 | Open SWE | 57.88 | 0.579 | 1.238 | 2.379 | Moderate | administration |

### Team rollout, 400 tasks/month

| Rank | Candidate | Monthly hours | Hours/task | Token pressure | Latency risk | Band | Main driver |
|---:|---|---:|---:|---:|---:|---|---|
| 1 | Codex CLI | 137.88 | 0.345 | 1.171 | 2.089 | Moderate | latency_tuning |
| 2 | Cline / Cline SDK | 139.77 | 0.349 | 1.130 | 1.486 | Moderate | governance |
| 3 | Deep Agents | 150.72 | 0.377 | 1.200 | 1.783 | Moderate | review_load |
| 4 | Open SWE | 151.36 | 0.378 | 1.238 | 2.379 | Moderate | administration |
| 5 | OpenHands Software Agent SDK | 146.53 | 0.366 | 1.150 | 1.684 | Moderate | review_load |

### Autonomous PR lane, 1000 tasks/month

| Rank | Candidate | Monthly hours | Hours/task | Token pressure | Latency risk | Band | Main driver |
|---:|---|---:|---:|---:|---:|---|---|
| 1 | Codex CLI | 327.10 | 0.327 | 1.171 | 2.089 | Moderate | latency_tuning |
| 2 | Cline / Cline SDK | 336.71 | 0.337 | 1.130 | 1.486 | Moderate | governance |
| 3 | Deep Agents | 358.53 | 0.359 | 1.200 | 1.783 | Moderate | review_load |
| 4 | Open SWE | 360.06 | 0.360 | 1.238 | 2.379 | Moderate | administration |
| 5 | OpenHands Software Agent SDK | 348.84 | 0.349 | 1.150 | 1.684 | Moderate | review_load |

## Operation-Adjusted Scenario Winners

| Scenario | Profile | Rank 1 | Adjusted score | Simulation rank | Rank delta |
|---|---|---|---:|---:|---:|
| custom_orchestrator_platform | pilot_100_tasks | Cline / Cline SDK | 4.114 | 1 | 0 |
| custom_orchestrator_platform | team_rollout_400_tasks | Cline / Cline SDK | 4.102 | 1 | 0 |
| custom_orchestrator_platform | autonomous_pr_1000_tasks | Cline / Cline SDK | 4.039 | 1 | 0 |
| secure_autonomous_prs | pilot_100_tasks | Codex CLI | 4.104 | 1 | 0 |
| secure_autonomous_prs | team_rollout_400_tasks | Codex CLI | 4.095 | 1 | 0 |
| secure_autonomous_prs | autonomous_pr_1000_tasks | Codex CLI | 4.039 | 1 | 0 |
| quick_local_coding | pilot_100_tasks | Cline / Cline SDK | 4.240 | 1 | 0 |
| quick_local_coding | team_rollout_400_tasks | Cline / Cline SDK | 4.228 | 1 | 0 |
| quick_local_coding | autonomous_pr_1000_tasks | Cline / Cline SDK | 4.166 | 1 | 0 |
| research_benchmarking | pilot_100_tasks | mini-SWE-agent | 4.163 | 1 | 0 |
| research_benchmarking | team_rollout_400_tasks | mini-SWE-agent | 4.127 | 1 | 0 |
| research_benchmarking | autonomous_pr_1000_tasks | mini-SWE-agent | 4.020 | 1 | 0 |
| enterprise_control_plane | pilot_100_tasks | Cline / Cline SDK | 4.154 | 1 | 0 |
| enterprise_control_plane | team_rollout_400_tasks | Cline / Cline SDK | 4.142 | 1 | 0 |
| enterprise_control_plane | autonomous_pr_1000_tasks | Cline / Cline SDK | 4.079 | 1 | 0 |

## Largest Operation-Adjusted Rank Shifts

| Scenario | Profile | Candidate | Simulation rank | Adjusted rank | Delta | Adjusted score |
|---|---|---|---:|---:|---:|---:|
| quick_local_coding | autonomous_pr_1000_tasks | Codex CLI | 5 | 3 | 2 | 3.909 |
| quick_local_coding | autonomous_pr_1000_tasks | OpenCode | 3 | 5 | -2 | 3.859 |
| quick_local_coding | autonomous_pr_1000_tasks | Omnigent | 9 | 11 | -2 | 3.610 |
| quick_local_coding | pilot_100_tasks | Codex CLI | 5 | 3 | 2 | 3.974 |
| quick_local_coding | team_rollout_400_tasks | Codex CLI | 5 | 3 | 2 | 3.965 |
| quick_local_coding | team_rollout_400_tasks | OpenCode | 3 | 5 | -2 | 3.946 |
| custom_orchestrator_platform | autonomous_pr_1000_tasks | Codex CLI | 6 | 5 | 1 | 3.866 |
| custom_orchestrator_platform | autonomous_pr_1000_tasks | OpenHands Agent Canvas | 5 | 6 | -1 | 3.801 |

## Interpretation

- Low-friction operating cost does not automatically mean best strategic fit. It identifies where review, administration, governance, and failure-recovery overhead are likely to be lower.
- Multi-agent and durable-memory systems can carry more token and latency pressure even when they are architecturally attractive. The pilot should capture actual token usage, wall-clock latency, failed-run recovery time, and reviewer intervention count.
- The operation-adjusted score is intentionally conservative: it starts from the same simulation score and subtracts a profile-specific penalty for operational friction. It should be used as a tie-breaker, not as a replacement for the main simulation.
- The model excludes vendor price tables, hosted-seat costs, and internal labor rates. Add those after a pilot once the organization knows provider, model, and reviewer workflow choices.
