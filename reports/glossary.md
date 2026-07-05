# Glossary

Date: 2026-07-05

| Term | Meaning in this report |
|---|---|
| Agent harness | The runtime or framework that gives a model tools, memory, state, execution policy, and task loop behavior. |
| Agent orchestration | Coordinating tools, subagents, task state, approvals, workspaces, and outputs across a coding workflow. |
| Approval gate | A policy point where a human must approve a command, file edit, network call, or external write. |
| Artifact completeness | Whether a run preserves enough prompts, tool calls, logs, diffs, test results, cost, and review notes to debug failures. |
| Control plane | A layer for managing multiple agents, backends, users, workspaces, policies, queues, and review artifacts. |
| Deterministic ranking | The base weighted score before Monte Carlo uncertainty perturbation. |
| Evidence confidence | A manual confidence value reflecting source clarity, repo maturity, docs, releases, and canonical status. |
| Hard sandbox | An execution boundary enforced by the operating system, container, microVM, or equivalent isolation layer. |
| Human-in-the-loop | A workflow where people can review, approve, interrupt, redirect, or reject agent actions. |
| Monte Carlo stability | How often a candidate wins or remains top 3 when scores and weights are randomly perturbed. |
| Pareto frontier | Candidates that are not strictly dominated across all raw scoring criteria. |
| Permissive open source | Open-source licensing under MIT or Apache-2.0 for this report's filter. |
| Provider portability | How easily a harness can switch between model providers or use local/open-weight models. |
| Regret | The score gap between a candidate and the best candidate in the same scenario. |
| Scenario weights | The relative importance assigned to each criterion for a specific use case. |
| Scope adjustment | A manual effort-model adjustment for platform breadth that raw feature scores do not fully capture. |
| Soft control | Approval prompts, checkpoints, or policy conventions that reduce risk but are not equivalent to hard isolation. |
| Stress test | A deliberate change to assumptions, weights, maturity penalties, or uncertainty to see whether rankings are fragile. |
| Top-3 rate | The share of Monte Carlo trials where a candidate ranks in the top three. |
