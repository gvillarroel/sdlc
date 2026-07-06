# Executive Brief: AI Coding-Agent Orchestrator Options

Date: 2026-07-05

## Decision

Do not pick a single universal winner. The best shortlist depends on the adoption scenario:

| Scenario | Primary shortlist | Decision bias |
|---|---|---|
| Custom orchestrator | OpenHands SDK, Deep Agents, Cline SDK | Favor OpenHands SDK or Deep Agents if building a Python platform; favor Cline if user workflow and approvals dominate. |
| Secure autonomous PRs | Codex CLI, OpenHands SDK, Cline SDK | Favor Codex CLI when OpenAI dependence is acceptable and sandboxing is central. |
| Quick local coding | Cline, OpenCode, Aider, Codex CLI | Favor Cline for broad workflow; favor OpenCode or Aider for lightweight local/provider-flexible use. |
| Research benchmarking | mini-SWE-agent, SWE-agent, OpenHands SDK | Favor mini-SWE-agent for ablations; favor SWE-agent for fuller issue-resolution research. |
| Enterprise control plane | Cline, OpenHands SDK, OpenHands Agent Canvas, Open SWE | Favor control-plane options only after proving multiple teams or async PR workflows need them. |

## Recommended Next Step

Run a two-week controlled pilot with:

1. OpenHands Software Agent SDK
2. Deep Agents
3. Flue or Codex CLI, depending on whether TypeScript framework fit or secure OpenAI-centered CLI/CI is more important
4. mini-SWE-agent as a minimal reproducibility baseline

Use `data/pilot_tasks.json` and the templates in `templates/` to capture metrics consistently.

## Main Finding

The evaluation is not a live benchmark of every candidate. It is a multi-criteria decision analysis backed by GitHub metadata, source links, license filtering, scoring criteria, Monte Carlo uncertainty, and sensitivity checks. It narrows the field and exposes tradeoffs; the pilot should decide final adoption.

## Market And Maintenance Addendum

AI-native creation lowers prototype cost, but it shifts the burden toward distribution, defensibility, trust, and maintenance. Read the four addenda before treating a fast-to-build framework as a product foundation:

| Question | Addendum |
|---|---|
| What is the combined go/no-go model? | `reports/market_maintenance_synthesis.md` |
| How have entry barriers moved? | `reports/market_entry_barriers_shift.md` |
| What happens when many generated tools fight for the same users? | `reports/market_fragmentation_user_share.md` |
| Can generated applications be supported over time? | `reports/long_term_ai_app_maintenance.md` |
| When should teams read AI-generated code versus trust verification gates? | `reports/ai_code_trust_matrix.md` |

## Highest Risks

| Risk | Why it matters | Required mitigation |
|---|---|---|
| Prompt injection | Coding agents ingest untrusted issue text, docs, web pages, and command output. | Include prompt-injection fixtures and verify policy hierarchy. |
| Secret exposure | Agents may read local files, logs, CI secrets, or package tokens. | Use secret traps, redaction, and runtime credential isolation. |
| Sandbox boundary failure | Autonomous commands can modify unintended files or systems. | Run workspace-boundary fixtures in disposable sandboxes. |
| Weak observability | Failed tasks become impossible to debug or audit. | Require full trajectories, prompts, diffs, commands, and test logs. |
| Benchmark mismatch | Public benchmark success may not transfer to private repos. | Use representative internal task fixtures and reviewer acceptance. |

## What To Avoid

- Do not adopt Alpha/low-evidence projects as the first production base. Track Omnigent as a meta-harness idea, but do not lead with it.
- Do not treat passing tests as sufficient. Reviewability, diff size, safety behavior, cost, and intervention count matter.
- Do not use broad network access or host filesystem access during autonomous runs unless a task explicitly requires it and the action is approved.
- Do not compare candidates on different tasks, prompts, or models and call the result a benchmark.

## Artifacts

- Full report: `reports/ai_orchestrator_frameworks_report.md`
- Dataset: `data/alternatives.json`
- Pilot tasks: `data/pilot_tasks.json`
- Risk register: `data/risk_register.json`
- License audit: `results/license_audit.csv`
- Evidence matrix: `results/evidence_matrix.csv`
- Source URL check: `results/source_check.csv`
