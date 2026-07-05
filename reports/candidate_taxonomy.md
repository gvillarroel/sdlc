# Candidate Taxonomy

Date: 2026-07-05

## Purpose

The report compares tools that are not identical product categories. This taxonomy explains the adoption shape of each group so the rankings are read within the right context.

The machine-readable taxonomy is `data/candidate_taxonomy.json`.

## Groups

| Group | Candidates | Use when | Watch for |
|---|---|---|---|
| Programmable SDK or framework | OpenHands SDK, Deep Agents, Flue, Sandcastle | Building a product-specific orchestrator or agent workflow. | The team must still design policy, tools, telemetry, deployment, and failure handling. |
| Local developer CLI or assistant | Cline, OpenCode, Aider, goose, Codex CLI | Fast developer productivity, local workflow, or lightweight automation. | Local convenience does not automatically provide autonomous-execution safety. |
| Secure PR automation | Codex CLI, Open SWE, OpenHands SDK, Cline | Controlled autonomous or semi-autonomous issue-to-PR work. | Sandboxing, network policy, credentials, branch protection, and review artifacts are mandatory. |
| Research harness | mini-SWE-agent, SWE-agent, OpenHands SDK | Reproducible experiments, ablations, or SWE-bench-style evaluations. | Benchmark fit is not the same as enterprise workflow fit. |
| Control plane or multi-backend layer | OpenHands Agent Canvas, Open SWE, Omnigent | Coordinating multiple backends, users, queues, policies, and artifacts. | Operational ownership and integration scope can dominate framework selection. |
| Experimental reference | Anchor, OmniAgent, Omni Agent, Omnigent | Tracking design ideas or running exploratory spikes. | High evidence risk or alpha maturity prevents first-phase production adoption. |

## How To Use This Taxonomy

Use the taxonomy before reading the ranking tables:

1. Pick the group that matches the target workflow.
2. Compare candidates inside that group first.
3. Use cross-group comparison only when the adoption path is genuinely open.
4. Treat candidates in the experimental-reference group as second-phase unless fresh evidence changes their risk profile.

This prevents a common mistake: choosing a polished local assistant when the actual need is a governed platform, or choosing a platform starter when the actual need is a quick local coding tool.
