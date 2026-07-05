# Permissive Open-Source AI Orchestrator Alternatives

Date: 2026-07-05

## Executive Summary

The shared ChatGPT conversation listed a broad set of AI coding-agent harnesses, CLIs, SDKs, and control planes. I filtered that set to permissive open-source projects only: MIT and Apache-2.0. Claude Agent SDK and Codex app were excluded because they do not satisfy that filter as framed in the source discussion.

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

## Final Recommendation

For a serious custom build, start with two tracks:

1. **Python track:** prototype with OpenHands Software Agent SDK and Deep Agents. Compare tool definitions, sandbox integration, memory, observability, and deployment ergonomics.
2. **TypeScript track:** prototype with Flue if the organization prefers TypeScript and wants an application framework rather than a CLI.

For autonomous engineering workflows that open PRs, evaluate Codex CLI and Open SWE next. Codex CLI is stronger when OpenAI lock-in is acceptable and sandboxed local/CI operation is a priority. Open SWE is better when the desired end state is an internal async coding-agent platform built on LangChain infrastructure.

Do not prioritize Anchor, OmniAgent, or Omni Agent except as reference material. Omnigent is worth tracking because the meta-harness idea fits multi-agent governance, but its alpha maturity makes it a second-phase candidate, not the first implementation foundation.

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
