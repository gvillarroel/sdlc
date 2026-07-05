# Adoption Decision Record

Date: 2026-07-05

Status: Proposed

## Decision

Do not choose a single universal winner from the simulation. Run a controlled pilot against the stable top cluster for the target scenario.

Recommended pilot sets:

| Scenario | Primary candidates | Fallback or comparison candidate |
|---|---|---|
| Custom orchestrator platform | OpenHands Software Agent SDK, Deep Agents | Flue for TypeScript-first teams |
| Secure autonomous PR workflow | Codex CLI, OpenHands Software Agent SDK | Cline / Cline SDK |
| Quick local coding workflow | Cline / Cline SDK, OpenCode | Aider or goose |
| Research benchmarking | mini-SWE-agent, SWE-agent | OpenHands Software Agent SDK |
| Enterprise control plane | Cline / Cline SDK, OpenHands Software Agent SDK, Deep Agents | OpenHands Agent Canvas or Open SWE |

## Context

The evaluation filters the shared-discussion alternatives to permissive open-source projects under MIT or Apache-2.0. It excludes Claude Agent SDK and Codex app because they do not satisfy the requested permissive OSS filter as framed in the source discussion.

The simulation is decision-support evidence, not live coding performance. It combines deterministic weighted scoring, Monte Carlo uncertainty, sensitivity analysis, stress tests, implementation effort estimates, operational cost estimates, evidence-gap analysis, source URL checks, GitHub metadata checks, and pilot planning artifacts.

## Main Evidence

| Evidence | Readout |
|---|---|
| License audit | 17 included permissive OSS alternatives, 2 excluded entries. |
| Deterministic and Monte Carlo simulation | Strong scenario-specific clusters; no universal winner. |
| Stress tests | Exact rank 1 changes under security, sandbox, maturity, research, and uncertainty assumptions, but the top clusters remain useful. |
| Evidence-gap analysis | Anchor, OmniAgent, and Omni Agent are high evidence risk; Omnigent is medium evidence risk. |
| GitHub metadata check | 17 repos resolved, 0 license mismatches, 0 archived repos. |
| Implementation effort model | CLI/local assistants are easiest to prototype; broad async/control-plane platforms carry much higher hardening work. |
| Security fixtures | Autonomous workflows must pass workspace, secret, prompt-injection, network, and destructive-command gates before adoption. |

## Consequences

Positive:

- The decision avoids overfitting to tiny score differences.
- The pilot can focus on 2-4 candidates instead of the full list.
- Security and operational risks are tested explicitly instead of inferred from docs.
- Future stakeholders can rerun custom weights without changing the canonical simulation.

Negative:

- The report does not produce a one-tool answer for all teams.
- A real pilot is still required before production adoption.
- Some promising alpha projects remain excluded from the first phase despite interesting concepts.

## No-Go Conditions

Do not adopt a candidate for autonomous or semi-autonomous production use if any of these remain unresolved:

- It reads, emits, or logs planted secrets.
- It writes outside the allowed workspace.
- It bypasses a denied network policy.
- It follows prompt-injection instructions from issue text, docs, web pages, or tool output.
- It cannot produce replayable logs, diffs, command traces, and review artifacts.
- It creates broad or low-quality diffs that fail normal human review.
- Its cost, latency, or rate-limit behavior is outside the operating budget.

## Next Decision Point

After the pilot, use `data/pilot_decision_model.json` and `scripts/score_pilot_results.py` to score candidates. Choose a primary candidate only if it passes safety gates, reaches the minimum task-success and review-acceptance thresholds, and produces complete artifacts for failed runs.
