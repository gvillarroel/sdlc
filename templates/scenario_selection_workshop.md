# Scenario Selection Workshop

Date: 2026-07-05

Use this worksheet before changing weights or choosing pilot candidates.

## 1. Target Workflow

| Question | Answer |
|---|---|
| Is the target interactive local coding, autonomous PRs, custom orchestrator, research benchmarking, or enterprise control plane? | |
| Who approves commands, file edits, dependency installs, network access, and external writes? | |
| What repository type must the candidate handle first? | |
| What model providers are approved? | |
| What environments are allowed: local shell, container, CI, cloud sandbox, remote workspace? | |

## 2. Hard Gates

| Gate | Required? | Notes |
|---|---:|---|
| MIT or Apache-2.0 license | Yes | |
| No unresolved security fixture failures | Yes | |
| Provider neutrality | | |
| Hard sandboxing | | |
| Self-hosting | | |
| CI/PR automation | | |
| Human approval before shell commands | | |
| Complete logs and replayable traces | | |
| Market defense gate | | |
| User-share realism gate | | |
| Maintenance capacity gate | | |
| Trust posture gate | | |

## 3. Market, Maintenance, And Trust Gate

Use `reports/market_maintenance_synthesis.md` before selecting pilot candidates.

| Gate | Required evidence before pilot | Owner |
|---|---|---|
| Market defense | Workflow depth, proprietary data/evaluation traces, distribution, switching cost, or regulated trust. | |
| User-share realism | Narrow target segment, usage frequency, substitute map, and budget or retention signal. | |
| Maintenance capacity | Named maintainers, test strategy, observability plan, support budget, and ownership model. | |
| Trust posture | Policy for when generated code must be read and which verification gates can substitute for reading. | |

## 4. Weighting Priorities

Score each priority from 0 to 5 before looking at candidate rankings.

| Priority | Weight |
|---|---:|
| Fast setup and low implementation burden | |
| Mature project and release posture | |
| Provider portability | |
| Strong sandbox isolation | |
| Durable state or memory | |
| Multi-agent orchestration | |
| Human approval and steering | |
| CI/PR automation fit | |
| Observability and replay | |
| Security and governance policy | |
| Extensibility and custom tools | |
| Deployment flexibility | |
| Coding-task specialization | |
| Research reproducibility | |
| Market defensibility evidence | |
| Retention or workflow integration evidence | |
| Long-term maintenance capacity | |
| Trust-gate strength | |

## 5. Candidate Selection

| Scenario | Candidate 1 | Candidate 2 | Candidate 3 | Reason |
|---|---|---|---|---|
| Primary scenario | | | | |
| Fallback scenario | | | | |

## 6. Pilot Exit Decision

| Decision question | Answer |
|---|---|
| What pass rate is acceptable? | |
| What review acceptance rate is acceptable? | |
| What minimum product-readiness rubric score is required? | |
| What safety failures are tolerated? | None by default |
| What cost and latency budget is acceptable? | |
| What artifact completeness threshold is required? | |
| What trust gate is required for production-impacting changes? | |
| Who can approve adoption? | |
