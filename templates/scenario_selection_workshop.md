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

## 3. Weighting Priorities

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

## 4. Candidate Selection

| Scenario | Candidate 1 | Candidate 2 | Candidate 3 | Reason |
|---|---|---|---|---|
| Primary scenario | | | | |
| Fallback scenario | | | | |

## 5. Pilot Exit Decision

| Decision question | Answer |
|---|---|
| What pass rate is acceptable? | |
| What review acceptance rate is acceptable? | |
| What safety failures are tolerated? | None by default |
| What cost and latency budget is acceptable? | |
| What artifact completeness threshold is required? | |
| Who can approve adoption? | |
