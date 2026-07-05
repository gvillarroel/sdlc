# Residual Risks

Date: 2026-07-05

## Purpose

This report records what remains uncertain after the license filter, simulations, stress tests, source checks, GitHub metadata checks, and offline validation.

## Residual Risk Register

| Risk | Why it remains | Next evidence needed |
|---|---|---|
| Simulated rankings may not predict live task success. | The current model uses scored evidence, not direct candidate execution on the same repositories. | Run the pilot task suite in `data/pilot_tasks.json`. |
| Model choice can dominate framework choice. | A stronger model in a weaker harness can outperform a stronger harness with a weaker model. | Pin or record model/provider for every pilot run. |
| Sandbox claims can differ from actual isolation. | Docs and feature lists do not prove workspace, network, secret, or destructive-command boundaries. | Run `data/security_evaluation_fixtures.json`. |
| Internal repositories may behave differently from public benchmarks. | Monorepos, proprietary build systems, flaky tests, and legacy code can change outcomes. | Include at least one representative internal repository in the pilot. |
| Cost and latency are not measured yet. | Simulations do not execute real model calls or sandbox workloads. | Capture tokens, cost, retries, queue time, and wall-clock latency in `templates/pilot_run_log.csv`. |
| Review quality is not measured yet. | Passing tests does not guarantee maintainable, minimal, or mergeable diffs. | Use `templates/reviewer_scorecard.md` for every accepted or partial result. |
| Legal review is not final. | Project-level MIT or Apache-2.0 screening does not replace dependency, asset, or generated-code legal review. | Run organization-standard legal/dependency scans before adoption. |
| Project metadata can drift. | Fast-moving repos can change license, release posture, APIs, or maintainership after 2026-07-05. | Rerun live source and GitHub metadata checks before a final decision. |

## Decision Impact

These residual risks do not invalidate the screening result. They define the boundary of the result: the report is strong enough to choose pilot candidates, not strong enough to approve production adoption without execution evidence.

The most important residual risk is security boundary evidence. Any candidate intended for autonomous or semi-autonomous repository work should fail closed until the security fixtures pass.
