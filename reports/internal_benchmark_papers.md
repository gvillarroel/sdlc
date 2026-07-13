# Research Papers for Internal Agent-Harness Benchmarks

Date: 2026-07-07

## Priority Reading

If the goal is to build internal organizational benchmarks for agent harnesses, these are the papers to read first:

| Priority | Paper | Why It Matters |
|---:|---|---|
| 1 | [SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://arxiv.org/abs/2310.06770) | Defines the issue-to-patch pattern with real repositories, tests, and patch-based evaluation. It is the natural starting point for internal software tasks. |
| 2 | [SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](https://arxiv.org/abs/2405.15793) | Shows that the harness and interface affect performance, not only the model. It is directly relevant to harness comparisons. |
| 3 | [OpenHands: An Open Platform for AI Software Developers as Generalist Agents](https://arxiv.org/abs/2407.16741) | Describes a platform with an integrated sandbox, tools, agents, and benchmarks. It is useful for designing harness architecture. |
| 4 | [Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces](https://arxiv.org/abs/2601.11868) | Provides a strong model for realistic terminal tasks with a unique environment, a human solution, and broad tests. |
| 5 | [TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks](https://arxiv.org/abs/2412.14161) | Closely resembles an organizational benchmark: it simulates a software company with internal sites, data, and workplace tasks. |
| 6 | [WorkArena: How Capable are Web Agents at Solving Common Knowledge Work Tasks?](https://arxiv.org/abs/2403.07718) | Helps frame internal tasks involving enterprise software, web workflows, and knowledge-work environments. |
| 7 | [WebArena: A Realistic Web Environment for Building Autonomous Agents](https://arxiv.org/abs/2307.13854) | Provides a strong example of a reproducible, self-hosted, realistic, and functional environment for web agents. |
| 8 | [AgentBench: Evaluating LLMs as Agents](https://arxiv.org/abs/2308.03688) | Provides a general framework for evaluating agents across several interactive environments; it is useful for taxonomy and comparability. |
| 9 | [Holistic Evaluation of Language Models](https://arxiv.org/abs/2211.09110) | Introduces a scenarios-plus-multiple-metrics approach instead of a single score. It is highly applicable to internal benchmarks. |
| 10 | [Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering](https://arxiv.org/abs/2604.01437) | Emphasizes Thought-Action-Result traces, interaction data, and reproducibility in agentic software-engineering evaluations. |
| 11 | [The SWE-Bench Illusion: When State-of-the-Art LLMs Remember](https://arxiv.org/abs/2506.12286) | Addresses leakage and contamination, reinforcing the need for private benchmarks and internal holdouts. |
| 12 | [Benchmark Data Contamination of Large Language Models: A Survey](https://arxiv.org/abs/2406.04244) | Surveys controls for contamination, leakage, and overfitting to public benchmarks. |

## Coding Agents and Software Engineering

| Paper | Year | Reusable Idea | Application to an Internal Benchmark |
|---|---:|---|---|
| [Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374) | 2021 | HumanEval popularized evaluation through functional tests and pass@k. | Use executable tests as a minimum, but do not stop at toy or single-file problems. |
| [RepoBench: Benchmarking Repository-Level Code Auto-Completion Systems](https://arxiv.org/abs/2306.03091) | 2023 | Evaluates repository-level retrieval, completion, and pipeline capabilities. | Include tasks that require navigating multiple files and internal conventions. |
| [SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://arxiv.org/abs/2310.06770) | 2023 | Builds tasks from real issues and pull requests, with test-based scoring. | Convert internal tickets and pull requests into reproducible cases with a starting commit, prompt, and grader. |
| [SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](https://arxiv.org/abs/2405.15793) | 2024 | Shows that the agent-computer interface affects navigation, editing, and test execution. | Evaluate the harness, model, and tools as a system, not only the model. |
| [OpenHands: An Open Platform for AI Software Developers as Generalist Agents](https://arxiv.org/abs/2407.16741) | 2024 | Presents an open platform with agents, a CLI, web interface, sandbox, and benchmarks. | Draw on its adapter lifecycle, sandboxing, logs, and multi-harness comparisons. |
| [The OpenHands Software Agent SDK: A Composable and ...](https://arxiv.org/html/2511.03690v1) | 2025 | Provides a software-agent SDK with flexibility, secure execution, and interfaces. | Use it as a reference for harness contracts and reusable components. |
| [Benchmarking AI Coding Agents on End-to-End Project Development](https://arxiv.org/html/2602.01655v1) | 2026 | Proposes end-to-end evaluation with diagnostic feedback and code review. | Add maintainability and pull-request quality review, not only tests. |
| [Code Review Agent Benchmark](https://arxiv.org/html/2603.23448v3) | 2026 | Evaluates commercial and open-source code-review agents. | Create a sub-suite for reviewing internal pull requests, detecting bugs, and measuring false positives. |
| [Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering](https://arxiv.org/abs/2604.01437) | 2026 | Recommends publishing or retaining Thought-Action-Result trajectories and LLM interactions. | Require traces, commands, tool calls, prompts, patches, and results as artifacts. |

## Agent Benchmarks in Realistic Environments

| Paper | Year | Reusable Idea | Application to an Internal Benchmark |
|---|---:|---|---|
| [WebArena: A Realistic Web Environment for Building Autonomous Agents](https://arxiv.org/abs/2307.13854) | 2023 | Provides a reproducible web environment with functional sites and realistic data. | Create self-hosted internal environments that emulate corporate tools. |
| [AgentBench: Evaluating LLMs as Agents](https://arxiv.org/abs/2308.03688) | 2023 | Provides eight interactive environments for evaluating reasoning and multi-turn decisions. | Classify internal benchmarks by environment: repository, CLI, web, API, ticketing, or CI. |
| [GAIA: a benchmark for General AI Assistants](https://arxiv.org/abs/2311.12983) | 2023 | Uses questions that are simple for humans but difficult for assistants with tools. | Design tasks that measure practical robustness instead of artificial difficulty. |
| [WorkArena: How Capable are Web Agents at Solving Common Knowledge Work Tasks?](https://arxiv.org/abs/2403.07718) | 2024 | Defines enterprise-software tasks using ServiceNow and BrowserGym. | Model real organizational workflows such as tickets, approvals, lists, and forms. |
| [OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments](https://arxiv.org/abs/2404.07972) | 2024 | Uses real desktop tasks with setup and evaluation scripts. | If the harness controls a GUI or desktop, use initialization and system-state verification. |
| [AndroidWorld: A Dynamic Benchmarking Environment for Autonomous Agents](https://arxiv.org/abs/2405.14573) | 2024 | Uses dynamic, parameterized tasks with initialization, success checks, and teardown. | Parameterize internal tasks to reduce memorization and measure robustness across variations. |
| [$\\tau$-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045) | 2024 | Simulates users, tools, and domain policies, and measures the final database state. | For user-facing agents, evaluate consistency, policy compliance, and database effects. |
| [TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks](https://arxiv.org/abs/2412.14161) | 2024 | Simulates a company with websites, code, programs, and communication among coworkers. | Use it as a conceptual template for a private organizational benchmark. |
| [Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces](https://arxiv.org/abs/2601.11868) | 2026 | Uses realistic CLI tasks with unique environments, human solutions, and broad tests. | Use it as a primary reference for harnesses that operate in shells, CI systems, and repositories. |

## Tool Use, Function Calling, and API Harnesses

| Paper or Resource | Year | Reusable Idea | Application to an Internal Benchmark |
|---|---:|---|---|
| [ToolBench](https://arxiv.org/abs/2305.16504) | 2023 | Evaluates tool and API use in real tasks. | Measure tool selection, correct arguments, and multi-tool composition. |
| [The Berkeley Function Calling Leaderboard: From Tool Use to Agentic Evaluation](https://openreview.net/forum?id=2GmDdhBdDk) | 2024 | Evaluates AST accuracy, executable accuracy, and function-call relevance. | Add separate metrics for schemas, selection, execution, and final answers. |
| [Benchmarking MCP Tool Invocation In Computer-Use Agents](https://arxiv.org/html/2510.24563v2) | 2025 | Evaluates MCP invocation and GUI use in computer-use scenarios. | If the organization uses MCP, create tasks with internal tools, distractors, and invocation logs. |
| [MCPWorld: A Unified Benchmarking Testbed for API, GUI ...](https://arxiv.org/html/2506.07672v1) | 2025 | Provides an MCP testbed for API, GUI, and hybrid interactions. | Use it for benchmarks that combine internal APIs and user interfaces. |
| [MCP-Atlas: A Large-Scale Benchmark for Tool-Use Competency](https://arxiv.org/html/2602.00933v1) | 2026 | Evaluates multi-tool coordination and grounding in tool output. | Score tool selection, parameterization, sequencing, and final answers separately. |

## Methodology, Contamination, and Validity

| Paper or Resource | Year | Reusable Idea | Application to an Internal Benchmark |
|---|---:|---|---|
| [Holistic Evaluation of Language Models](https://arxiv.org/abs/2211.09110) | 2022 | Combines scenarios, multiple metrics, and prompt-and-completion transparency. | Report by scenario, task family, cost, safety, robustness, and efficiency. |
| [Benchmark Data Contamination of Large Language Models: A Survey](https://arxiv.org/abs/2406.04244) | 2024 | Reviews benchmark contamination and mitigation techniques. | Maintain a private holdout, canaries, task rotation, and access controls. |
| [On Leakage of Code Generation Evaluation Datasets](https://arxiv.org/html/2407.07565v1) | 2024 | Examines leakage in code-generation datasets. | Do not expose solutions, hidden tests, or holdout prompts to external systems. |
| [Benchmarking Large Language Models Under Data Contamination](https://arxiv.org/html/2502.17521v2) | 2025 | Analyzes static and dynamic benchmarks under contamination. | Use parameterized variants and controlled generation of new tasks. |
| [The SWE-Bench Illusion: When State-of-the-Art LLMs Remember](https://arxiv.org/abs/2506.12286) | 2025 | Provides evidence of memorization and contamination in SWE-bench Verified. | Use private benchmarks instead of relying on public leaderboards for purchasing or adoption decisions. |
| [Towards More Standardized AI Evaluation: From Models to Agents](https://arxiv.org/html/2602.18029v1) | 2026 | Frames evaluations as a control function for agentic systems. | Turn benchmarks into continuous operational gates rather than one-time evaluations. |
| [LLM Benchmark Datasets Should Be Contamination-Resistant](https://arxiv.org/html/2605.19999v1) | 2026 | Argues for contamination-resistant benchmarks. | Design private data that is useful for inference but difficult to memorize. |

## Safety, Trust, and Human Review

| Paper or Resource | Year | Reusable Idea | Application to an Internal Benchmark |
|---|---:|---|---|
| [SecureAgentBench: Benchmarking Secure Code Generation ...](https://arxiv.org/html/2509.22097v1) | 2025 | Evaluates code that is both correct and secure, not merely functional. | Add fixtures in which safety and correctness are simultaneous requirements. |
| [Agentic AI Software Engineers: Programming with Trust](https://arxiv.org/abs/2502.13767) | 2025 | Emphasizes the shift from programming to establishing trust. | Measure reviewer comprehension, provenance, traces, and auditability. |
| [Trustworthy AI Software Engineers](https://arxiv.org/html/2602.06310v1) | 2026 | Presents a vision of what makes a software agent trustworthy. | Define trust gates before allowing autonomy in pull requests. |

## Applying the Research to the Main Report

Direct mapping to `reports/internal_benchmark_harnesses.md`:

| Report Section | Most Useful Papers |
|---|---|
| Task selection | SWE-bench, Terminal-Bench, TheAgentCompany, WorkArena |
| Harness adapter contract | SWE-agent, OpenHands, OpenHands SDK, Terminal-Bench |
| Environment and reproducibility | WebArena, OSWorld, AndroidWorld, Terminal-Bench |
| Scoring model | HELM, SWE-bench, tau-bench, BFCL |
| Human review rubric | End-to-end project development benchmark, Code Review Agent Benchmark, Agentic AI Software Engineers |
| Safety fixtures | SecureAgentBench, OpenHands, Terminal-Bench |
| Leakage and holdout governance | SWE-Bench Illusion, Benchmark Data Contamination survey, OpenAI SWE-bench Verified analysis |
| Enterprise workflow simulation | TheAgentCompany, WorkArena, tau-bench |

## Practical Recommendation

For an internal organizational benchmark, do not copy a single paper. Combine the strongest patterns:

1. **SWE-bench** for the issue-to-patch format.
2. **Terminal-Bench** for hermetic CLI environments and rigorous tests.
3. **TheAgentCompany/WorkArena** for simulating an organization, internal tools, and knowledge-work workflows.
4. **SWE-agent/OpenHands** for designing the harness and adapters.
5. **HELM** for reporting scenarios and multiple metrics.
6. **SWE-Bench Illusion + contamination surveys** for holdout governance, task rotation, and leakage controls.

The literature supports one consistent conclusion: a useful internal benchmark must evaluate the complete system, not only the model. The true object of evaluation is `model + harness + tools + sandbox + prompts + policy + environment + reviewer workflow`.
