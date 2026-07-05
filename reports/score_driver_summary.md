# Score Driver Summary

Date: 2026-07-05

This appendix explains which scored criteria drive each candidate up or down in the simulation. It is generated from `data/alternatives.json` and the deterministic scenario rankings.

Generated outputs: `results/score_driver_summary.csv` and `results/criterion_spread_summary.csv`.

## Highest-Spread Criteria

| Criterion | Spread | Mean | Leaders | Laggards |
|---|---:|---:|---|---|
| multi_agent | 4.1 | 3.288 | Deep Agents; Open SWE | Anchor |
| maturity | 3.7 | 3.147 | Aider; Cline / Cline SDK; Codex CLI | OmniAgent |
| ci_pr | 3.6 | 3.618 | Open SWE | Anchor |
| observability | 3.6 | 3.247 | Deep Agents; Open SWE | Anchor |
| research_reproducibility | 3.6 | 3.318 | mini-SWE-agent | Anchor |
| persistence_memory | 3.4 | 3.312 | Deep Agents | Anchor |
| provider_portability | 3.3 | 4.141 | Omnigent; OpenCode; OpenHands Software Agent SDK; goose | Anchor |
| sandbox_isolation | 3.3 | 3.518 | Codex CLI; Open SWE | Anchor |

## Candidate Drivers

| Candidate | Strengths | Weaknesses | Best scenario | Worst scenario | Mean | Spread |
|---|---|---|---|---|---:|---:|
| Cline / Cline SDK | human_control=4.8; coding_fit=4.7; extensibility=4.7 | sandbox_isolation=2.8; research_reproducibility=3.4; observability=4.0 | custom_orchestrator_platform #1 | research_benchmarking #6 | 4.229 | 2.000 |
| Codex CLI | coding_fit=4.8; security_governance=4.8; sandbox_isolation=4.7 | provider_portability=2.0; persistence_memory=3.4; research_reproducibility=3.6 | secure_autonomous_prs #1 | research_benchmarking #7 | 4.064 | 2.800 |
| mini-SWE-agent | research_reproducibility=4.9; provider_portability=4.7; implementation_ease=4.6 | multi_agent=1.0; persistence_memory=1.8; observability=2.2 | research_benchmarking #1 | custom_orchestrator_platform #14 | 3.386 | 3.900 |
| OpenHands Software Agent SDK | provider_portability=4.8; coding_fit=4.6; extensibility=4.5 | implementation_ease=3.8; observability=3.8; ci_pr=4.0 | custom_orchestrator_platform #2 | research_benchmarking #3 | 4.207 | 1.000 |
| SWE-agent | research_reproducibility=4.8; provider_portability=4.6; coding_fit=4.5 | multi_agent=2.0; persistence_memory=2.5; human_control=3.1 | research_benchmarking #2 | quick_local_coding #12 | 3.721 | 2.800 |
| Deep Agents | extensibility=4.7; provider_portability=4.7; multi_agent=4.6 | ci_pr=3.4; maturity=3.5; implementation_ease=3.6 | custom_orchestrator_platform #3 | secure_autonomous_prs #5 | 4.157 | 1.300 |
| OpenCode | provider_portability=4.8; coding_fit=4.7; extensibility=4.5 | sandbox_isolation=2.6; observability=2.8; security_governance=3.3 | quick_local_coding #3 | custom_orchestrator_platform #9 | 3.921 | 2.200 |
| Open SWE | ci_pr=4.8; sandbox_isolation=4.7; coding_fit=4.6 | implementation_ease=2.7; maturity=3.0; human_control=3.2 | custom_orchestrator_platform #4 | quick_local_coding #10 | 4.036 | 2.100 |
| Aider | coding_fit=4.8; implementation_ease=4.7; provider_portability=4.7 | multi_agent=1.8; observability=2.4; sandbox_isolation=2.4 | research_benchmarking #4 | custom_orchestrator_platform #13 | 3.607 | 3.000 |
| OpenHands Agent Canvas | provider_portability=4.7; deployment_flexibility=4.6; multi_agent=4.5 | maturity=3.0; research_reproducibility=3.0; implementation_ease=3.6 | custom_orchestrator_platform #5 | research_benchmarking #12 | 4.007 | 1.700 |
| goose | extensibility=4.8; provider_portability=4.8; deployment_flexibility=4.3 | multi_agent=2.6; observability=2.8; research_reproducibility=3.2 | quick_local_coding #6 | custom_orchestrator_platform #10 | 3.821 | 2.200 |
| Omnigent | provider_portability=4.8; human_control=4.7; extensibility=4.6 | maturity=2.0; implementation_ease=2.8; research_reproducibility=3.0 | custom_orchestrator_platform #7 | research_benchmarking #13 | 3.950 | 2.800 |
| Flue | extensibility=4.6; provider_portability=4.6; deployment_flexibility=4.5 | maturity=3.0; human_control=3.2; research_reproducibility=3.2 | custom_orchestrator_platform #8 | quick_local_coding #11 | 3.914 | 1.600 |
| Sandcastle | sandbox_isolation=4.6; coding_fit=4.2; ci_pr=4.1 | observability=2.7; maturity=2.8; persistence_memory=2.8 | custom_orchestrator_platform #12 | quick_local_coding #14 | 3.557 | 1.900 |
| Omni Agent | security_governance=4.0; human_control=3.5; multi_agent=3.5 | maturity=1.0; research_reproducibility=1.8; implementation_ease=2.4 | custom_orchestrator_platform #15 | custom_orchestrator_platform #15 | 2.964 | 3.000 |
| OmniAgent | provider_portability=4.0; human_control=3.7; extensibility=3.2 | maturity=0.8; ci_pr=1.5; observability=1.5 | custom_orchestrator_platform #16 | custom_orchestrator_platform #16 | 2.429 | 3.200 |
| Anchor | human_control=4.0; implementation_ease=4.0; coding_fit=2.8 | multi_agent=0.5; maturity=1.0; observability=1.0 | custom_orchestrator_platform #17 | custom_orchestrator_platform #17 | 1.850 | 3.500 |

## Interpretation

- Criteria with high spread drive more ranking separation. Low-spread criteria should be treated as weaker differentiators unless a stakeholder explicitly weights them heavily.
- Candidate strengths and weaknesses are scorecard diagnostics, not standalone recommendations. Always read them with evidence confidence, operational cost, security gates, and pilot results.
- A candidate with a strong best scenario and a poor worst scenario is specialized; avoid generalizing it across workflows without changing scenario weights and rerunning the simulation.
