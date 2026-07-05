# Presentation Outline

Date: 2026-07-05

## Purpose

This outline turns the report into a short stakeholder presentation. It is not a slide deck; it is a source outline for preparing one.

## 1. Decision Context

- The source discussion listed AI coding-agent orchestrators, CLIs, SDKs, and control planes.
- The evaluation filters to permissive open-source candidates only: MIT and Apache-2.0.
- The output is a pilot shortlist, not a production adoption approval.

## 2. Main Recommendation

- There is no universal winner.
- Use scenario-specific pilot clusters.
- Start with OpenHands SDK and Deep Agents for custom Python orchestration.
- Use Flue for TypeScript-first product agents.
- Use Codex CLI for OpenAI-centered secure CLI/CI workflows.
- Use mini-SWE-agent and SWE-agent for research baselines.

## 3. Evidence Base

- 17 included permissive OSS alternatives.
- 2 excluded non-matching entries.
- Deterministic rankings and 5,000-trial Monte Carlo simulations.
- Sensitivity, stress, regret, Pareto, and rank-stability outputs.
- Evidence-gap, source URL, and GitHub metadata checks.
- Implementation effort model and security fixture catalog.

## 4. What Changes The Ranking

- Scenario weights.
- Security and sandbox assumptions.
- Provider neutrality requirements.
- Project maturity and source confidence.
- Model choice and task harness design.
- Repository representativeness.

## 5. Recommended Pilot

- Pick the target workflow first.
- Select 2-3 candidates from the matching scenario cluster.
- Run security fixtures before scaling to the full task suite.
- Capture task outcomes, cost, latency, human interventions, review acceptance, and artifacts.
- Score results with `scripts/score_pilot_results.py`.

## 6. No-Go Conditions

- Secret exposure.
- Workspace boundary failure.
- Prompt-injection compliance.
- Unapproved network access.
- Direct protected-branch push.
- Missing replayable logs or artifacts.
- Unreviewable diffs.

## 7. Ask From Stakeholders

- Confirm target scenario and hard gates.
- Confirm approved model providers.
- Select representative repository fixtures.
- Approve the pilot candidate set.
- Define cost, latency, and review-acceptance thresholds.
