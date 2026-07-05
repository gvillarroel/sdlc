# Scenario Playbooks

Date: 2026-07-05

This appendix turns each simulated scenario into a short execution playbook. Use it after choosing the scenario and before starting the pilot.

Generated output: `results/scenario_playbook_summary.csv`.

## Custom orchestrator platform

Question: What should we build on if we need our own agent orchestration layer?

| Field | Recommendation |
|---|---|
| Primary candidate | Cline / Cline SDK (4.237) |
| Fallback candidates | OpenHands Software Agent SDK; Deep Agents |
| Priority summary | Extensibility; Multi-agent orchestration; Provider portability; Sandbox isolation |
| Pilot focus | Build one minimal orchestrator slice with tools, sandbox policy, trace capture, and a rollback path. |
| No-go condition | No inspectable tool boundary, traces, or extension path for product-specific policy. |
| Related artifacts | reports/pilot_protocol.md; reports/pilot_sample_size.md; reports/operational_cost_model.md |

## Secure autonomous PRs

Question: What should run autonomous coding work safely and open PRs?

| Field | Recommendation |
|---|---|
| Primary candidate | Codex CLI (4.221) |
| Fallback candidates | OpenHands Software Agent SDK; Cline / Cline SDK |
| Priority summary | Sandbox isolation; Security governance; CI/PR workflow; Observability |
| Pilot focus | Run autonomous issue-to-PR tasks under the strictest sandbox, network, secret, branch, and approval gates. |
| No-go condition | Any unresolved safety gate failure, secret exposure, protected-branch write, or missing audit log. |
| Related artifacts | reports/pilot_protocol.md; reports/pilot_sample_size.md; reports/operational_cost_model.md |

## Quick local coding

Question: What should a developer try first for local coding productivity?

| Field | Recommendation |
|---|---|
| Primary candidate | Cline / Cline SDK (4.363) |
| Fallback candidates | OpenHands Software Agent SDK; OpenCode |
| Priority summary | Implementation ease; Maturity; Human control; Coding fit |
| Pilot focus | Measure developer setup time, review friction, accepted diffs, and daily workflow ergonomics. |
| No-go condition | Setup or review friction is higher than current developer workflow for routine tasks. |
| Related artifacts | reports/pilot_protocol.md; reports/pilot_sample_size.md; reports/operational_cost_model.md |

## Research benchmarking

Question: What should we use for reproducible experiments and ablations?

| Field | Recommendation |
|---|---|
| Primary candidate | mini-SWE-agent (4.356) |
| Fallback candidates | SWE-agent; OpenHands Software Agent SDK |
| Priority summary | Research reproducibility; Implementation ease; Coding fit; Observability |
| Pilot focus | Run fixed-seed benchmark tasks with complete trajectories, patches, costs, and ablation notes. |
| No-go condition | Runs cannot be reproduced with fixed seeds, task definitions, logs, and patch artifacts. |
| Related artifacts | reports/pilot_protocol.md; reports/pilot_sample_size.md; reports/operational_cost_model.md |

## Enterprise control plane

Question: What should govern multiple teams, agents, backends, and workflows?

| Field | Recommendation |
|---|---|
| Primary candidate | Cline / Cline SDK (4.277) |
| Fallback candidates | OpenHands Software Agent SDK; Deep Agents |
| Priority summary | Security governance; Observability; Deployment flexibility; Human control |
| Pilot focus | Evaluate admin controls, auditability, multi-team workflow ownership, and backend portability. |
| No-go condition | No credible ownership model for users, permissions, audit logs, incidents, and upgrades. |
| Related artifacts | reports/pilot_protocol.md; reports/pilot_sample_size.md; reports/operational_cost_model.md |

## Use Notes

- Treat the primary candidate as a starting hypothesis, not a final selection.
- If the pilot sample-size appendix says the top cluster is unresolved, keep both primary and fallback candidates in the same pilot wave.
- If the operational-cost appendix contradicts the scenario winner, decide whether strategic fit or operating friction matters more for the current adoption phase.
