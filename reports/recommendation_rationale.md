# Recommendation Rationale

Date: 2026-07-05

## Purpose

This appendix turns the generated screening outputs into a scenario-by-scenario decision rationale. It combines the deterministic shortlist, Monte Carlo stability, evidence-risk bands, implementation effort, and operation-adjusted ranks. It is still screening evidence: final selection requires the pilot protocol and security gates.

Generated output: `results/recommendation_rationale.csv`

Input outputs: `results/decision_shortlist.csv`, `results/evidence_gap_analysis.csv`, `results/implementation_effort_estimates.csv`, and `results/operational_fit_rankings.csv`.

Run:

```powershell
python scripts/build_recommendation_rationale.py
```

## Scenario Rationale

| Scenario | Rank | Candidate | Posture | Gap | Win | Top-3 | Evidence | Hardening | Operational ranks | Rationale |
|---|---:|---|---|---:|---:|---:|---|---|---|---|
| Custom orchestrator platform | 1 | Cline / Cline SDK | Head-to-head pilot | 0.000 | 31% | 83% | low | 2-4 weeks | 1 / 1 / 1 | scenario score leader; strong Monte Carlo shortlist stability (83% top-3 rate); leader is close enough that a head-to-head pilot is still required; low evidence-risk band; stays in the top three after operational-friction adjustment. |
| Custom orchestrator platform | 2 | OpenHands Software Agent SDK | Head-to-head pilot | 0.001 | 33% | 85% | low | 2-4 weeks | 2 / 2 / 2 | near-tie with the leader (0.001 score gap); strong Monte Carlo shortlist stability (85% top-3 rate); low evidence-risk band; stays in the top three after operational-friction adjustment. |
| Custom orchestrator platform | 3 | Deep Agents | Head-to-head pilot | 0.023 | 23% | 62% | low | 2-4 weeks | 3 / 3 / 3 | near-tie with the leader (0.023 score gap); moderate Monte Carlo shortlist stability (62% top-3 rate); low evidence-risk band; stays in the top three after operational-friction adjustment. |
| Custom orchestrator platform | 4 | Open SWE | Watchlist only | 0.147 | 4% | 22% | low | 6-12 weeks | 4 / 4 / 4 | 0.147 behind the scenario leader; fragile Monte Carlo shortlist position (22% top-3 rate); low evidence-risk band; 6-12 weeks hardening estimate; operational rank is broadly consistent with simulation rank. |
| Custom orchestrator platform | 5 | OpenHands Agent Canvas | Watchlist only | 0.179 | 4% | 18% | low | 3-6 weeks | 6 / 6 / 6 | 0.179 behind the scenario leader; fragile Monte Carlo shortlist position (18% top-3 rate); low evidence-risk band; 3-6 weeks hardening estimate; operational rank is broadly consistent with simulation rank. |
| Secure autonomous PRs | 1 | Codex CLI | Head-to-head pilot | 0.000 | 28% | 76% | low | 1-2 weeks | 1 / 1 / 1 | scenario score leader; strong Monte Carlo shortlist stability (76% top-3 rate); leader is close enough that a head-to-head pilot is still required; low evidence-risk band; stays in the top three after operational-friction adjustment. |
| Secure autonomous PRs | 2 | OpenHands Software Agent SDK | Head-to-head pilot | 0.022 | 21% | 69% | low | 2-4 weeks | 3 / 3 / 3 | near-tie with the leader (0.022 score gap); moderate Monte Carlo shortlist stability (69% top-3 rate); low evidence-risk band; stays in the top three after operational-friction adjustment. |
| Secure autonomous PRs | 3 | Cline / Cline SDK | Head-to-head pilot | 0.022 | 23% | 67% | low | 2-4 weeks | 2 / 2 / 2 | near-tie with the leader (0.022 score gap); moderate Monte Carlo shortlist stability (67% top-3 rate); low evidence-risk band; stays in the top three after operational-friction adjustment. |
| Secure autonomous PRs | 4 | Open SWE | Fallback or benchmark | 0.079 | 10% | 34% | low | 6-12 weeks | 4 / 4 / 4 | 0.079 behind the scenario leader; fragile Monte Carlo shortlist position (34% top-3 rate); low evidence-risk band; 6-12 weeks hardening estimate; operational rank is broadly consistent with simulation rank. |
| Secure autonomous PRs | 5 | Deep Agents | Fallback or benchmark | 0.110 | 9% | 28% | low | 2-4 weeks | 5 / 5 / 5 | 0.110 behind the scenario leader; fragile Monte Carlo shortlist position (28% top-3 rate); low evidence-risk band; operational rank is broadly consistent with simulation rank. |
| Quick local coding | 1 | Cline / Cline SDK | Primary pilot candidate | 0.000 | 82% | 99% | low | 2-4 weeks | 1 / 1 / 1 | scenario score leader; strong Monte Carlo shortlist stability (99% top-3 rate); credible win-rate signal (82%); low evidence-risk band; stays in the top three after operational-friction adjustment. |
| Quick local coding | 2 | OpenHands Software Agent SDK | Head-to-head pilot | 0.139 | 11% | 82% | low | 2-4 weeks | 2 / 2 / 2 | 0.139 behind the scenario leader; strong Monte Carlo shortlist stability (82% top-3 rate); low evidence-risk band; stays in the top three after operational-friction adjustment. |
| Quick local coding | 3 | OpenCode | Fallback or benchmark | 0.232 | 1% | 38% | low | 2-4 weeks | 4 / 5 / 5 | 0.232 behind the scenario leader; fragile Monte Carlo shortlist position (38% top-3 rate); low evidence-risk band; operational friction can push it down in rollout profiles. |
| Quick local coding | 4 | Deep Agents | Fallback or benchmark | 0.265 | 3% | 28% | low | 2-4 weeks | 5 / 4 / 4 | 0.265 behind the scenario leader; fragile Monte Carlo shortlist position (28% top-3 rate); low evidence-risk band; operational rank is broadly consistent with simulation rank. |
| Quick local coding | 5 | Codex CLI | Watchlist only | 0.272 | 1% | 24% | low | 1-2 weeks | 3 / 3 / 3 | 0.272 behind the scenario leader; fragile Monte Carlo shortlist position (24% top-3 rate); low evidence-risk band; stays in the top three after operational-friction adjustment. |
| Research benchmarking | 1 | mini-SWE-agent | Primary pilot candidate | 0.000 | 45% | 80% | low | 2-4 weeks | 1 / 1 / 1 | scenario score leader; strong Monte Carlo shortlist stability (80% top-3 rate); credible win-rate signal (45%); low evidence-risk band; stays in the top three after operational-friction adjustment. |
| Research benchmarking | 2 | SWE-agent | Head-to-head pilot | 0.112 | 23% | 76% | low | 1-2 weeks | 2 / 2 / 2 | 0.112 behind the scenario leader; strong Monte Carlo shortlist stability (76% top-3 rate); low evidence-risk band; stays in the top three after operational-friction adjustment. |
| Research benchmarking | 3 | OpenHands Software Agent SDK | Head-to-head pilot | 0.170 | 16% | 64% | low | 2-4 weeks | 3 / 3 / 3 | 0.170 behind the scenario leader; moderate Monte Carlo shortlist stability (64% top-3 rate); low evidence-risk band; stays in the top three after operational-friction adjustment. |
| Research benchmarking | 4 | Aider | Watchlist only | 0.310 | 3% | 24% | low | 2-4 weeks | 5 / 5 / 5 | 0.310 behind the scenario leader; fragile Monte Carlo shortlist position (24% top-3 rate); low evidence-risk band; operational rank is broadly consistent with simulation rank. |
| Research benchmarking | 5 | Deep Agents | Fallback or benchmark | 0.326 | 9% | 29% | low | 2-4 weeks | 4 / 4 / 4 | 0.326 behind the scenario leader; fragile Monte Carlo shortlist position (29% top-3 rate); low evidence-risk band; operational rank is broadly consistent with simulation rank. |
| Enterprise control plane | 1 | Cline / Cline SDK | Primary pilot candidate | 0.000 | 51% | 92% | low | 2-4 weeks | 1 / 1 / 1 | scenario score leader; strong Monte Carlo shortlist stability (92% top-3 rate); credible win-rate signal (51%); low evidence-risk band; stays in the top three after operational-friction adjustment. |
| Enterprise control plane | 2 | OpenHands Software Agent SDK | Head-to-head pilot | 0.064 | 20% | 78% | low | 2-4 weeks | 2 / 2 / 2 | 0.064 behind the scenario leader; strong Monte Carlo shortlist stability (78% top-3 rate); low evidence-risk band; stays in the top three after operational-friction adjustment. |
| Enterprise control plane | 3 | Deep Agents | Fallback or benchmark | 0.092 | 16% | 53% | low | 2-4 weeks | 3 / 3 / 3 | 0.092 behind the scenario leader; moderate Monte Carlo shortlist stability (53% top-3 rate); low evidence-risk band; stays in the top three after operational-friction adjustment. |
| Enterprise control plane | 4 | Codex CLI | Watchlist only | 0.187 | 2% | 22% | low | 1-2 weeks | 4 / 4 / 4 | 0.187 behind the scenario leader; fragile Monte Carlo shortlist position (22% top-3 rate); low evidence-risk band; operational rank is broadly consistent with simulation rank. |
| Enterprise control plane | 5 | Open SWE | Watchlist only | 0.210 | 3% | 17% | low | 6-12 weeks | 5 / 5 / 5 | 0.210 behind the scenario leader; fragile Monte Carlo shortlist position (17% top-3 rate); low evidence-risk band; 6-12 weeks hardening estimate; operational rank is broadly consistent with simulation rank. |

Operational ranks are shown as `pilot / team rollout / autonomous PR` ranks after applying the operating-cost model.

## Interpretation

- A `Primary pilot candidate` is strong enough to lead a pilot, but still needs the pilot protocol and security gates.
- A `Head-to-head pilot` is close enough to the leader that the report should not force a single winner without live task evidence.
- `Second-phase exploration` candidates can be useful design references, but their evidence or maturity profile should keep them out of the first production decision.
- `Fallback or benchmark` candidates are useful comparators for local productivity or research baselines.
