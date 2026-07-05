# Permissive Open-Source AI Orchestrator Alternatives

Date: 2026-07-05

## Executive Summary

The shared ChatGPT conversation listed a broad set of AI coding-agent harnesses, CLIs, SDKs, and control planes. I filtered that set to permissive open-source projects only: MIT and Apache-2.0. Claude Agent SDK and Codex app were excluded because they do not satisfy that filter as framed in the source discussion.

This report should be read as a decision-support evaluation, not as a claim that one framework objectively beats all others. The Python simulations are multi-criteria Monte Carlo simulations over scored evidence, not live benchmark runs of every agent against the same repository. That distinction matters: the simulation is useful for narrowing the field and identifying sensitivity, while a final adoption decision still needs a real pilot on representative repositories.

There is no universal winner. The best choice depends on what is being built:

| Use case | Best candidates | Why |
|---|---|---|
| Custom programmable orchestrator | OpenHands Software Agent SDK, Deep Agents, Cline SDK, Flue | Strong SDK/framework surfaces, extensibility, state, tool control, and provider flexibility. |
| Secure autonomous PR workflow | Codex CLI, OpenHands SDK, Cline SDK, Open SWE | Strong CI/PR fit, sandbox or approval controls, mature coding-agent loops. |
| Quick local coding assistant | Cline, OpenCode, Aider, Codex CLI, goose | Lowest adoption friction and strong daily developer workflow. |
| Research and ablation studies | mini-SWE-agent, SWE-agent, OpenHands SDK | Reproducible scaffolds and strong benchmark orientation. |
| Enterprise/control-plane layer | Cline, OpenHands Agent Canvas, OpenHands SDK, Omnigent, Open SWE | Stronger orchestration/control surfaces, but Omnigent is still alpha. |

My practical recommendation is:

1. Use **OpenHands Software Agent SDK** or **Deep Agents** as the Python foundation for a custom orchestrator.
2. Use **Flue** if the implementation must be TypeScript-first and product-specific.
3. Use **Open SWE** if the target is an async internal coding-agent platform that opens PRs.
4. Use **Codex CLI** if OpenAI dependence is acceptable and sandboxed local/CI execution is more important than provider neutrality.
5. Use **mini-SWE-agent** or **SWE-agent** for research harnesses, benchmark experiments, and small ablation studies.

## How To Use This Report

Use this report in three passes:

1. Pick the target scenario: custom framework, secure PR automation, local coding, research benchmarking, or enterprise control plane.
2. Use the shortlist and category scorecards to choose 2-3 candidates, not one winner.
3. Run a pilot using the validation plan below before committing to a platform.

The most important negative result is that early or low-evidence projects can look attractive by feature checklist alone. The simulation intentionally gives them wider uncertainty and the narrative sections treat them as ideas to track unless their repo maturity and operational evidence justify more.

## Scope And License Filter

Included: Sandcastle, Flue, Anchor, Omnigent, OmniAgent, Omni Agent, Deep Agents, Codex CLI, OpenCode, Cline/Cline SDK, OpenHands Agent Canvas, OpenHands Software Agent SDK, Open SWE, Aider, goose, SWE-agent, and mini-SWE-agent.

Excluded:

| Excluded item | Reason |
|---|---|
| Claude Agent SDK | Not treated as permissive OSS in the shared table; official Anthropic/Claude-centric license and practical lock-in. |
| Codex app | Desktop app/commercial product, not the open-source CLI/framework. |

Notable verification corrections from the shared table:

| Item | Correction |
|---|---|
| Flue | Canonical repo verified as `withastro/flue`, Apache-2.0. |
| OpenCode | Current canonical repo appears as `anomalyco/opencode`; older `opencode-ai/opencode` is archived. |
| goose | Current canonical repo verified as `aaif-goose/goose`. |
| OpenHands | The SDK and Agent Canvas have separate MIT repos; the older/main monorepo can show mixed license metadata. |

## Implementation Complexity

| Alternative | License | Maturity used in model | Complexity | Best role | Main concern |
|---|---|---:|---|---|---|
| Aider | Apache-2.0 | Production | Low | Terminal pair-programming | Not a governance or multi-agent platform. |
| mini-SWE-agent | MIT | Beta | Low | Minimal research scaffold | Few platform features by design. |
| goose | Apache-2.0 | Production | Low-medium | Local general agent + MCP automation | Less coding-specific orchestration. |
| OpenCode | MIT | Production | Low-medium | Local coding agent with provider choice | Hard isolation is mostly external. |
| Codex CLI | Apache-2.0 | Production | Low-medium | Secure OpenAI-centered CLI/CI agent | Provider neutrality is limited. |
| Cline / Cline SDK | Apache-2.0 | Production | Medium | Product SDK, IDE, CLI, automation | Approval/checkpoint model is not the same as a hard sandbox. |
| OpenHands SDK | MIT | Production | Medium | Python software-agent foundation | Requires policy/tool/deployment design. |
| Deep Agents | MIT | Beta | Medium | Python custom orchestrator foundation | Not turnkey; you build the app layer. |
| Flue | Apache-2.0 | Beta | Medium | TypeScript agent harness | Beta API and Node/runtime choices matter. |
| Sandcastle | MIT | Beta | Medium-high | Sandbox runner around existing coding agents | Young project and provider examples lean Claude. |
| OpenHands Agent Canvas | MIT | Beta | Medium-high | Self-hosted control plane/UI | Backend selection defines the security boundary. |
| Open SWE | MIT | Beta | High | Async internal coding-agent platform | Needs sandbox providers and integration operations. |
| Omnigent | Apache-2.0 | Alpha | High | Multi-harness meta-control-plane | Promising but alpha and broad in scope. |
| Anchor | MIT | Alpha | Low | Narrow review workflow | Too narrow and low-evidence for platform use. |
| OmniAgent | MIT | Alpha | Medium | Experimental local CLI | Low evidence for sandboxing/governance. |
| Omni Agent | MIT | Alpha | Medium-high | Verification-native idea reference | Minimal traction and no release at retrieval time. |

## Implementation Effort Estimates

These estimates assume a small experienced engineering team, one representative repository, one primary model provider already approved, and a goal of producing a credible prototype rather than a hardened enterprise rollout.

| Alternative | Credible prototype | Production hardening | Hidden work |
|---|---:|---:|---|
| Aider | 0.5-1 day | 3-7 days | Repo conventions, model routing, test command integration, and human workflow. |
| mini-SWE-agent | 0.5-1 day | 1-2 weeks | Benchmark harness, sandbox wrapper, logs, and safety controls. |
| OpenCode | 1-2 days | 1-2 weeks | Provider setup, permissions, team conventions, and external sandboxing if needed. |
| goose | 1-2 days | 1-2 weeks | MCP extension governance, local permissions, and non-code workflow boundaries. |
| Codex CLI | 1-2 days | 1-3 weeks | Sandbox profile design, network allowlists, CI policy, and approval defaults. |
| Cline / Cline SDK | 2-4 days | 2-4 weeks | SDK integration, approval rules, automation config, and enterprise policy choices. |
| OpenHands SDK | 3-5 days | 3-6 weeks | Tool contracts, workspace lifecycle, sandbox strategy, telemetry, and PR gates. |
| Deep Agents | 3-7 days | 3-6 weeks | Custom tools, permissions, memory policy, sandbox backend, and eval harness. |
| Flue | 3-7 days | 3-6 weeks | Node/runtime baseline, durable state, deployment target, sandbox choice, and observability. |
| Sandcastle | 3-7 days | 2-5 weeks | Agent provider choice, Docker/Podman/Vercel setup, branch strategy, and mount safety. |
| OpenHands Agent Canvas | 5-10 days | 4-8 weeks | Backend topology, user auth, automations, remote execution, and operational ownership. |
| Open SWE | 1-2 weeks | 6-10 weeks | Cloud sandbox provider, queues, GitHub integration, PR automation, secrets, and tracing. |
| Omnigent | 1-2 weeks | 6-12 weeks | Backend adapters, policy model, collaboration workflow, and alpha-risk mitigation. |
| Anchor | 0.5-1 day | Not recommended | Narrow Claude-centered review flow; not a full orchestrator foundation. |
| OmniAgent | 1-3 days | Not recommended yet | Low evidence for security, CI, telemetry, and long-running maintenance. |
| Omni Agent | 2-5 days | Not recommended yet | Verification concept may be useful, but repo maturity is too low for platform adoption. |

The main implementation trap is confusing "installable" with "operationally usable." CLI tools can be installed in minutes, but an autonomous coding workflow is not credible until it has sandboxing, repeatable tests, review artifacts, failure handling, credential boundaries, and a rollback path.

## Evidence Confidence

| Confidence | Projects | Reason |
|---|---|---|
| High | Codex CLI, Cline, OpenCode, Aider, goose, SWE-agent, mini-SWE-agent, Deep Agents, OpenHands SDK | Clear repos, permissive licenses, active development, docs or releases, and enough ecosystem evidence to score with lower uncertainty. |
| Medium | Flue, Sandcastle, Open SWE, OpenHands Agent Canvas | Clear repos and strong concepts, but younger APIs, beta posture, or heavier dependence on deployment choices. |
| Low | Anchor, OmniAgent, Omni Agent | Very low traction or narrow scope; useful as design references, not primary adoption bets. |
| Medium-low | Omnigent | Strong meta-harness concept and visible traction, but alpha status and broad control-plane scope make implementation risk high. |

## Category Scorecards

These category scores are generated from `results/category_scores.csv`. They are separate from scenario rankings: they show where each candidate is intrinsically strong before scenario weights are applied.

| Category | Top candidates | Interpretation |
|---|---|---|
| Adoption readiness | Cline 4.40, Aider 4.33, OpenCode 4.30, goose 4.27, Codex CLI 4.23 | These are easiest to trial and have stronger practical maturity. |
| Agent architecture | Deep Agents 4.54, Cline 4.46, OpenHands SDK 4.44, Omnigent 4.40, Agent Canvas 4.36 | These have the richest architectural surfaces for tools, state, agents, and extension. |
| Execution safety | Codex CLI 4.60, Omnigent 4.47, OpenHands SDK 4.17, Open SWE 4.10, Deep Agents 4.07 | Codex CLI leads because sandboxing, approvals, and network controls are explicit and documented. |
| Operations | Open SWE 4.40, Cline 4.33, Flue 4.27, Agent Canvas 4.17, Codex CLI 4.13 | Open SWE scores well for async PR-oriented workflows and managed orchestration patterns. |
| Research fit | Deep Agents 4.23, OpenHands SDK 4.15, SWE-agent 4.15, mini-SWE-agent 4.10, Cline 4.08 | The research category is broad; the scenario-specific research ranking still favors mini-SWE-agent because simplicity was weighted more heavily. |

## Decision Shortlist

The table below combines deterministic score and Monte Carlo stability. High top-3 rate is more important than a tiny deterministic lead.

| Scenario | Practical shortlist | Decision note |
|---|---|---|
| Custom orchestrator | OpenHands SDK, Cline, Deep Agents | Treat these as a top cluster. Cline wins deterministic by a tiny margin; OpenHands SDK has slightly better Monte Carlo stability. |
| Secure autonomous PRs | Codex CLI, OpenHands SDK, Cline | Codex CLI is the default if OpenAI dependence is acceptable; OpenHands SDK is the better neutral SDK candidate. |
| Quick local coding | Cline, OpenHands SDK, OpenCode | Cline is the clearest winner; OpenCode is the most natural local/provider-neutral CLI alternative. |
| Research benchmarking | mini-SWE-agent, SWE-agent, OpenHands SDK | mini-SWE-agent is best for minimal ablations; SWE-agent is best for a fuller research harness. |
| Enterprise control plane | Cline, OpenHands SDK, Deep Agents, Agent Canvas | Cline is strongest under the chosen weights, but Agent Canvas becomes more relevant if the UI/control-plane layer is central. |

## Simulation Method

The Python simulation is in `scripts/simulate_alternatives.py`. It uses `data/alternatives.json` and produces:

- `results/deterministic_rankings.csv`
- `results/monte_carlo_summary.csv`
- `results/sensitivity_summary.csv`
- `results/all_results.json`

The score model uses 14 criteria on a 0-5 scale: implementation ease, maturity, provider portability, sandbox isolation, persistence/memory, multi-agent support, human control, CI/PR fit, observability, security/governance, extensibility, deployment flexibility, coding-task fit, and research reproducibility.

Five scenarios were simulated:

| Scenario | Intent |
|---|---|
| `custom_orchestrator_platform` | Build a product-specific orchestrator or framework. |
| `secure_autonomous_prs` | Safely run autonomous coding work and PR automation. |
| `quick_local_coding` | Adopt a practical local coding assistant quickly. |
| `research_benchmarking` | Run reproducible experiments and ablations. |
| `enterprise_control_plane` | Govern multiple agent workflows and backends. |

The Monte Carlo run used 5,000 trials with a fixed seed. Each trial perturbed scenario weights and per-alternative scores. Alpha and low-confidence projects received wider uncertainty.

Generated outputs:

| File | Purpose |
|---|---|
| `results/deterministic_rankings.csv` | Sorted weighted scores by scenario. |
| `results/monte_carlo_summary.csv` | Mean score, rank, win rate, and top-3 rate after uncertainty perturbation. |
| `results/sensitivity_summary.csv` | How rankings change when each criterion is halved or doubled. |
| `results/category_scores.csv` | Criteria grouped into adoption, architecture, safety, operations, and research categories. |
| `results/decision_shortlist.csv` | Scenario shortlist combining deterministic and Monte Carlo outputs. |
| `results/scenario_weights.csv` | Raw and normalized scenario weights for each criterion. |
| `results/criteria_definitions.csv` | Human-readable definitions for each scoring criterion. |
| `results/evidence_matrix.csv` | Per-alternative repository, license, confidence, summary, implementation note, risk note, and source URLs. |
| `results/alternative_scorecards.csv` | Wide table of all per-criterion scores by alternative. |
| `results/source_check.csv` | Live URL check of report and dataset sources. The latest run checked 41 URLs with 41 OK responses. |
| `results/all_results.json` | Complete machine-readable output. |

## Deterministic Results

| Scenario | Rank 1 | Rank 2 | Rank 3 | Rank 4 | Rank 5 |
|---|---|---|---|---|---|
| Custom orchestrator | Cline / Cline SDK | OpenHands SDK | Deep Agents | Open SWE | OpenHands Agent Canvas |
| Secure autonomous PRs | Codex CLI | OpenHands SDK | Cline / Cline SDK | Open SWE | Deep Agents |
| Quick local coding | Cline / Cline SDK | OpenHands SDK | OpenCode | Deep Agents | Codex CLI |
| Research benchmarking | mini-SWE-agent | SWE-agent | OpenHands SDK | Aider | Deep Agents |
| Enterprise control plane | Cline / Cline SDK | OpenHands SDK | Deep Agents | Codex CLI | Open SWE |

The custom-orchestrator deterministic winner is not stable: Cline and OpenHands SDK are separated by less than 0.001 points. In Monte Carlo, OpenHands SDK slightly outranks Cline by top-3 stability for that scenario.

## Monte Carlo Stability

| Scenario | Most stable candidate | Win rate | Top-3 rate | Readout |
|---|---:|---:|---:|---|
| Custom orchestrator | OpenHands SDK | 32.7% | 85.1% | OpenHands SDK, Cline, and Deep Agents form the top cluster. |
| Secure autonomous PRs | Codex CLI | 28.4% | 75.9% | Codex CLI wins, but OpenHands SDK and Cline are close. |
| Quick local coding | Cline | 81.9% | 98.9% | Cline is the clearest scenario winner. |
| Research benchmarking | mini-SWE-agent | 44.7% | 79.7% | SWE-agent is a close second; OpenHands SDK remains a strong broader SDK. |
| Enterprise control plane | Cline | 50.8% | 92.4% | Cline dominates under the chosen enterprise weights. |

## Sensitivity Findings

The model is most sensitive in the custom-orchestrator scenario. If sandboxing, provider portability, multi-agent behavior, observability, or persistence are doubled, the top choice often flips from Cline to OpenHands SDK or Deep Agents. That means Cline's lead is mostly a balanced-product lead, not a decisive framework-foundation lead.

The secure-autonomous-PR scenario is also sensitive. Codex CLI wins under the default weights, but OpenHands SDK can overtake it when provider portability, persistence, or security-governance weight is increased. Cline can overtake when human control, extensibility, or deployment flexibility is weighted more heavily.

The research scenario is stable around mini-SWE-agent and SWE-agent; halving implementation-ease weight moves SWE-agent into first place, which is expected because mini-SWE-agent's advantage is simplicity.

## Candidate Deep Dives

### OpenHands Software Agent SDK

Best role: Python foundation for a custom software-agent system.

Choose it when you need a coding-specific SDK, local or ephemeral workspaces, provider flexibility, and enough structure to build production workflows. Avoid it when the team wants a simple CLI tool with minimal integration work. Implementation difficulty is medium: the SDK gets you a solid agent substrate, but the team must still define tools, permissions, test gates, telemetry, and deployment boundaries.

Primary pilot task: implement an agent that clones a representative internal repo, runs the test suite, fixes one seeded bug, records artifacts, and opens a draft PR or patch.

### Deep Agents

Best role: general Python agent harness for custom orchestration.

Choose it when the main problem is architecture: tools, memory, subagents, context offloading, sandbox backends, and human-in-the-loop controls. Avoid it when the team expects a ready-made coding product. Implementation difficulty is medium: the primitives are strong, but production behavior depends heavily on custom tool and policy design.

Primary pilot task: build two agents with the same toolset, one single-agent and one subagent-enabled, then compare context growth, task completion, and trace quality.

### Flue

Best role: TypeScript-first programmable agent harness.

Choose it for product-specific TypeScript agents that need sessions, tools, skills, sandbox choices, deployment targets, and observability adapters. Avoid it if the organization cannot absorb beta API churn or Node.js version requirements. Implementation difficulty is medium: lower than building from raw model APIs, higher than adopting a CLI.

Primary pilot task: create a triage or bug-fix agent that uses a virtual sandbox first, then repeat with a container sandbox.

### Open SWE

Best role: async internal coding-agent platform that plans, codes, tests, and opens PRs.

Choose it when the target workflow resembles an internal engineering agent with cloud sandboxes and PR automation. Avoid it for simple pair-programming or a first-week prototype. Implementation difficulty is high because sandbox providers, GitHub/Slack/Linear integration, credentials, queues, and observability all matter.

Primary pilot task: run 10 issue-to-PR tasks in disposable sandboxes and measure queue latency, test reliability, PR quality, and human intervention rate.

### Codex CLI

Best role: secure OpenAI-centered coding CLI and CI runner.

Choose it when sandboxing, approvals, network controls, and GitHub Action integration are central. Avoid it if provider neutrality is a hard requirement. Implementation difficulty is low-medium: local usage is easy, but enterprise policy and CI configuration must be deliberate.

Primary pilot task: run the same repo task under read-only, workspace-write, and network-enabled policies to confirm the least-privilege profile needed.

### Cline / Cline SDK

Best role: broad developer workflow across IDE, CLI, SDK, automation, and human approval.

Choose it when the user experience and human control loop are as important as the orchestration API. Avoid it if the primary requirement is hard isolation from untrusted code execution. Implementation difficulty is medium: easy to trial, more work to govern at scale.

Primary pilot task: compare interactive IDE/CLI use against headless SDK execution for the same maintenance task, then measure review friction.

### OpenCode

Best role: local coding agent with strong provider portability and developer ergonomics.

Choose it when model choice, local workflow, terminal/desktop/IDE options, and fast adoption matter. Avoid it when the main question is sandbox-first autonomous execution. Implementation difficulty is low-medium.

Primary pilot task: run it on 5 common developer tasks: code explanation, small bug fix, refactor, test generation, and dependency update.

### SWE-agent And mini-SWE-agent

Best role: reproducible research and issue-resolution experiments.

Choose SWE-agent when you need a fuller harness and trajectory evidence. Choose mini-SWE-agent when you want a minimal, explainable scaffold for ablations. Avoid both as the first choice for an enterprise control plane. Implementation difficulty ranges from low for mini-SWE-agent to medium for SWE-agent.

Primary pilot task: run both on a small SWE-bench-style local task suite and compare pass rate, trajectory length, cost, and ease of modification.

### Omnigent

Best role: emerging meta-harness/control-plane idea.

Choose it for exploration if the long-term requirement is to orchestrate multiple different coding-agent backends under common policies and collaboration UI. Avoid it as the first production foundation until alpha risk is acceptable. Implementation difficulty is high.

Primary pilot task: connect two backends, run one identical task, and evaluate whether policy, session state, and artifact handling are actually backend-neutral.

## Recommended Pilot Plan

Run a two-week pilot before standardizing.

The concrete task suite is included in `data/pilot_tasks.json`. It contains 20 tasks: 8 bug fixes, 4 refactors, 4 test-generation tasks, 1 dependency update, 1 documentation/codebase explanation task, and 2 security fixtures. The point is not that these exact tasks are universal; it is that every candidate should face the same distribution of ordinary coding work, ambiguous engineering work, and safety pressure.

| Phase | Duration | Work | Exit criteria |
|---|---:|---|---|
| 1. Harness smoke test | 2 days | Install top 3 candidates for the target scenario, run one simple repo task, confirm model/provider setup and sandbox path. | Each candidate can read the repo, make a controlled edit, run tests, and leave inspectable logs. |
| 2. Representative task set | 5 days | Run 20 tasks: 8 bug fixes, 4 refactors, 4 test-generation tasks, 2 dependency updates, 2 documentation/codebase explanation tasks. | Track pass rate, intervention count, wall time, cost, unsafe action attempts, and review acceptance. |
| 3. Security and operations drill | 3 days | Run prompt-injection fixtures, secret-file traps, network-deny tests, flaky-test cases, and CI/PR workflow tests. | Candidate must enforce the required permission boundary and produce enough evidence for review. |
| 4. Decision review | 1-2 days | Compare results against the target scenario weights and operational requirements. | Pick one primary candidate and one fallback, or defer if no candidate meets security gates. |

Minimum task metrics:

| Metric | Why it matters |
|---|---|
| `pass@1` on repo tests | Basic correctness signal. |
| Human interventions per task | Measures autonomy without ignoring review cost. |
| Unsafe action attempts | Captures sandbox/policy pressure, not just successful work. |
| Tokens and API cost | Prevents choosing a system that only works under unrealistic spending. |
| Wall-clock latency | Separates fast local assistants from slow async platforms. |
| Diff size and review acceptance | Penalizes broad, hard-to-review changes. |
| Reproducibility across reruns | Catches brittle prompts and flaky harness behavior. |
| Artifact completeness | Determines whether failures can be debugged. |

## Security Checklist

Before running autonomous code-writing agents on real repositories:

| Check | Required evidence |
|---|---|
| Workspace boundary | A test proves the agent cannot write outside the intended workspace. |
| Secret handling | `.env`, credential stores, SSH keys, and package tokens are blocked or only available in setup phases. |
| Network policy | Network is off by default, or restricted to an explicit allowlist. |
| Dependency installation | Install scripts run in disposable environments or behind approval. |
| Git safety | Agents work on branches/worktrees and cannot push directly to protected branches. |
| PR gate | Tests, lint, and security checks run before a PR is considered complete. |
| Prompt-injection handling | Web pages, issue text, README content, and tool output are treated as untrusted input. |
| Audit trail | Every command, tool call, file edit, model response, and approval is reconstructable. |
| Human approval policy | Destructive actions, external writes, and credential access require approval. |
| Cleanup | Sandboxes, temporary files, credentials, and branches are removed or archived intentionally. |

## Adoption Risk Register

The full structured register is in `data/risk_register.json`. The highest-priority risks are:

| Risk | Category | Severity | Mitigation |
|---|---|---:|---|
| Prompt injection from issue text, web pages, docs, or tool output | Security | 9 | Treat external content as data and include injection fixtures in the pilot. |
| Sandbox escape or workspace boundary failure | Security | 6 | Run boundary tests and use disposable workspaces with denied external writes. |
| Secret exposure through setup, logs, or tool output | Security | 6 | Isolate setup credentials, deny secret paths, and use secret-trap fixtures. |
| Network policy too broad for autonomous execution | Security | 6 | Default network off and require explicit domain allowlists. |
| Observability is insufficient for production failures | Operational | 6 | Require full artifact capture and replayable failed-task traces. |
| Autonomous PRs create large or low-quality diffs | Quality | 6 | Score review acceptance, diff size, convention adherence, and minimality. |
| Benchmark success does not transfer to internal repositories | Evaluation | 6 | Use internal representative tasks and human review acceptance. |

## Simulation Risk Factors

These factors can materially change the ranking:

| Factor | Why it matters |
|---|---|
| Scenario weights | A platform team, research team, and solo developer do not value the same criteria. |
| Model choice | The same harness can perform very differently with GPT, Claude, Gemini, local models, or small open-weight models. |
| Tool design | Search, edit, shell, test, browser, memory, and PR tools often matter more than the framework label. |
| Sandbox provider | Docker, Podman, cloud microVMs, local shell, and no-sandbox modes have very different safety properties. |
| Network policy | Agent internet access affects capability, cost, reproducibility, and prompt-injection exposure. |
| Repository type | Monorepos, polyglot repos, flaky tests, large dependency graphs, and proprietary build systems change success rates. |
| Human-in-the-loop tolerance | Some teams want autonomous PRs; others require approval before every command. |
| Observability requirements | Production agents need traceability, replay, logs, artifacts, and failure analysis. |
| License clarity | Even permissive projects can have mixed monorepo licensing or generated assets that need separate review. |
| Project drift | Several candidates are young and changing quickly; releases after 2026-07-05 can change maturity and APIs. |
| API cost and rate limits | Long-running coding agents can spend heavily on tokens, tool calls, and sandbox minutes. |
| Benchmark mismatch | SWE-bench-style performance does not guarantee success on internal repos or interactive workflows. |
| Security threat model | Prompt injection, secret exfiltration, dependency install scripts, and malicious repos require explicit controls. |

## From This Simulation To A Real Evaluation

The current Python simulation is appropriate for screening alternatives. A real evaluation should add execution evidence:

| Upgrade | What to do | Why |
|---|---|---|
| Replace subjective scores with measured values | Measure setup time, pass rate, token cost, unsafe action attempts, and intervention count. | Reduces dependence on analyst judgment. |
| Use identical task fixtures | Run the same seeded bugs, refactors, and test-generation tasks across candidates. | Prevents comparing different workloads. |
| Pin models and prompts | Use the same model where possible, and record prompt/scaffold differences where not possible. | Separates model performance from harness quality. |
| Run repeated trials | Run each task at least 3 times per candidate. | Captures stochastic failures and ranking stability. |
| Capture full artifacts | Store prompts, trajectories, diffs, logs, command outputs, token usage, and final test results. | Makes failures debuggable and audit-ready. |
| Add adversarial fixtures | Include prompt-injection text, secret traps, malicious package scripts, and network-deny tests. | Tests safety, not just coding ability. |
| Score review quality | Have engineers rate diff size, maintainability, and merge readiness. | Passing tests alone can hide poor patches. |

If time is limited, the minimum real benchmark should compare OpenHands SDK, Deep Agents, Flue, Codex CLI, and mini-SWE-agent on 10 tasks. That set covers framework-building, TypeScript, secure CLI/CI, and research-minimal baselines.

## Final Recommendation

For a serious custom build, start with two tracks:

1. **Python track:** prototype with OpenHands Software Agent SDK and Deep Agents. Compare tool definitions, sandbox integration, memory, observability, and deployment ergonomics.
2. **TypeScript track:** prototype with Flue if the organization prefers TypeScript and wants an application framework rather than a CLI.

For autonomous engineering workflows that open PRs, evaluate Codex CLI and Open SWE next. Codex CLI is stronger when OpenAI lock-in is acceptable and sandboxed local/CI operation is a priority. Open SWE is better when the desired end state is an internal async coding-agent platform built on LangChain infrastructure.

Do not prioritize Anchor, OmniAgent, or Omni Agent except as reference material. Omnigent is worth tracking because the meta-harness idea fits multi-agent governance, but its alpha maturity makes it a second-phase candidate, not the first implementation foundation.

The strongest next action is not another desk review. It is a controlled pilot with OpenHands SDK, Deep Agents, and either Flue or Codex CLI depending on stack preference and provider constraints. The current simulation narrows the field; the pilot should decide.

## Sources

- Shared ChatGPT conversation: https://chatgpt.com/share/6a4aa2a4-c0b8-83ea-b971-d5d3089200c4
- Sandcastle: https://github.com/mattpocock/sandcastle
- Flue repo and docs: https://github.com/withastro/flue, https://flueframework.com/
- Omnigent: https://github.com/omnigent-ai/omnigent
- Deep Agents docs: https://docs.langchain.com/oss/python/deepagents/overview
- Codex CLI docs and security: https://developers.openai.com/codex/cli, https://developers.openai.com/codex/agent-approvals-security
- OpenCode docs: https://opencode.ai/docs/
- Cline docs: https://docs.cline.bot/cline-overview
- OpenHands SDK docs: https://docs.openhands.dev/sdk
- OpenHands Agent Canvas docs: https://docs.openhands.dev/openhands/usage/agent-canvas/overview
- Open SWE announcement: https://www.langchain.com/blog/open-swe-an-open-source-framework-for-internal-coding-agents
- Aider docs and repo map: https://aider.chat/docs/, https://aider.chat/docs/repomap.html
- goose docs: https://goose-docs.ai/
- SWE-agent docs: https://swe-agent.com/latest/
- mini-SWE-agent: https://github.com/SWE-agent/mini-swe-agent
- SWE-bench: https://www.swebench.com/
