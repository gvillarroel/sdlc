# AI Code Reading And Trust Matrix

Date: 2026-07-06

## Question

How are mental frameworks evolving along two dimensions: whether developers read generated code, and how much they trust AI output?

## Research Method

This matrix synthesizes human-AI interaction research, trust studies for code generation, code-review papers, LLM-enabled compiler research, and local sandbox requirements. The goal is not to decide whether AI is "good" or "bad" at coding. The goal is to calibrate when unread generated code is acceptable, when human comprehension is mandatory, and when verification gates can substitute for manual reading.

## Dimensions

| Dimension | Low end | High end |
|---|---|---|
| Code reading | The developer treats generated code as an opaque artifact and relies on tests, demos, or tool reputation. | The developer reads code line by line, understands intent, and reviews architecture, security, and behavior. |
| Trust in AI output | The developer assumes output is provisional and potentially wrong. | The developer assumes output is usually correct enough to merge with limited intervention. |

## Matrix

|  | Low trust in AI output | High trust in AI output |
|---|---|---|
| Low code reading | **Generator skeptic**. Uses AI for throwaway prototypes but avoids relying on generated code in production. Risk: loses productivity gains because trust never becomes operationalized. | **Compiler-abstraction optimist**. Treats LLM output like a higher-level compilation target. Risk: category error when no formal semantics or deterministic correctness guarantee exists. |
| High code reading | **Engineering auditor**. Uses AI aggressively but requires human comprehension, tests, and review before merge. Risk: review becomes the bottleneck if generated diffs are too large. | **Guardrailed autonomist**. Trusts AI when bounded by evals, typed interfaces, tests, sandboxes, policy gates, and rollback. Risk: misplaced confidence if gates measure the wrong behavior. |

## Quadrant Operating Model

| Quadrant | Merge policy | Good use | Bad use |
|---|---|---|---|
| Generator skeptic | Do not merge AI code unless rewritten or fully reviewed. | Learning, throwaway prototypes, comparison prompts. | Production features where speed matters. |
| Compiler-abstraction optimist | Merge only if independent verification is stronger than human reading would be. | Generated artifacts with formal specs, generated clients, schemas, or codegen-like outputs. | Business logic, security, data migrations, or architecture changes without review. |
| Engineering auditor | Human author remains accountable for understanding. | Most current production AI-assisted development. | Huge opaque diffs that reviewers cannot realistically inspect. |
| Guardrailed autonomist | Merge through policy gates, traceability, CI, evals, sandboxing, and owner approval. | Autonomous PR workflows in bounded repos. | Open-ended agents with broad tools and weak observability. |

## How Frameworks Are Evolving

| Mental framework | Direction of evolution | Practical reading |
|---|---|---|
| AI as autocomplete | From local suggestions to multi-file changes. | Reading remains mandatory because the user is still the author of record. |
| AI as junior developer | From task delegation to supervised PR production. | Review focuses on intent, design fit, and hidden edge cases. |
| AI as compiler | From metaphor to hybrid toolchains with validators. | The analogy works only when outputs are checked by formal, test, type, or differential-verification layers. |
| AI as autonomous agent | From one-shot generation to tool-using workflows. | Trust shifts from the model alone to the whole system: prompts, tools, sandbox, evals, logs, and approval policy. |
| AI as maintained collaborator | From code generation to lifecycle ownership. | The system must preserve rationale, provenance, and regression evidence across future changes. |

## Trust Maturity Ladder

| Level | Description | Typical evidence |
|---|---|---|
| 0. Untrusted text | Output is treated as a suggestion. | Manual inspection only. |
| 1. Runnable artifact | Output executes in a local or sandboxed environment. | Passing smoke tests and command logs. |
| 2. Reviewed change | A human understands and accepts the change. | Code review notes and reviewer ownership. |
| 3. Tested behavior | Behavior is checked against representative tests. | Unit, integration, regression, mutation, or security checks. |
| 4. Governed workflow | AI actions are constrained and traceable. | Tool permissions, sandbox, provenance, policy approvals, and rollback. |
| 5. Verified generation class | The generated artifact belongs to a class with strong external validation. | Formal specs, type contracts, generated clients, differential tests, or certified build pipeline. |

## Compiler Analogy Assessment

The compiler analogy is useful only in a narrow sense: both transform higher-level intent into lower-level executable artifacts. It breaks down on the properties that make compilers trustworthy.

| Property | Traditional compiler | LLM code generator |
|---|---|---|
| Input language | Formal grammar and semantics. | Natural language, partial code, examples, repository context, and implicit intent. |
| Output guarantee | Designed to preserve semantics within known constraints. | Produces plausible code without inherent semantic guarantee. |
| Failure mode | Syntax/type errors, compiler bugs, undefined behavior, or optimization bugs. | Hallucinated APIs, incomplete requirements, insecure code, inconsistent architecture, brittle tests. |
| Validation | Compiler tests, formal methods, differential testing, reproducible builds. | Human review, unit/integration tests, static analysis, sandboxing, evals, and runtime monitoring. |
| User obligation | Rarely read generated machine code. | Read generated source unless external verification is strong enough for the risk class. |

## When Not Reading Code Is Defensible

Not reading generated code is defensible only when the artifact class is constrained enough that other checks dominate human inspection.

| Artifact class | Can skip line-by-line reading? | Required condition |
|---|---|---|
| Generated API client from stable schema | Often | Schema, generator, and compatibility tests are trusted. |
| Migration touching production data | Rarely | Requires dry run, rollback, data invariants, and human review. |
| UI copy or layout prototype | Sometimes | Low risk and easily reversible. |
| Security-sensitive code | No | Requires human and automated security review. |
| Refactor of core business logic | No | Requires behavioral equivalence evidence and review. |
| Agent-authored PR in bounded repo | Sometimes | Requires sandboxed execution, full trace, CI, diff limits, and accountable reviewer. |

## Trust Calibration Rules

| Situation | Recommended trust level | Required verification |
|---|---|---|
| Prototype, throwaway internal utility | Medium | Run locally, inspect sensitive operations, keep scope narrow. |
| Production feature in familiar codebase | Medium-low | Human review, tests, static analysis, dependency review, rollback path. |
| Security-sensitive code | Low | Security review, threat modeling, SAST/DAST, adversarial tests, least privilege. |
| Large generated refactor | Low | Smaller diffs, behavior-preserving tests, architecture review, staged rollout. |
| Generated code behind strong formal/spec gates | Medium-high | Preserve the gates and audit their coverage. |
| Autonomous PR workflow | Conditional | Sandbox, trace logs, policy approvals, CI, reviewer ownership, and post-merge monitoring. |

## Evidence Base

The curated source matrix for this addendum is `data/sources/market_maintenance_source_matrix.csv`; filter `relevant_reports` by `ai_code_trust_matrix.md`.

- A 2023/2024 study on trust in AI-powered code generation found developer trust to be situational and rooted in perceived ability, integrity, and benevolence, while current tools lack enough affordances for efficient trust evaluation: https://arxiv.org/abs/2305.11248
- A 2025 trust-terrain review analyzes 88 papers and expert feedback to clarify trust-related concepts for LLMs in software engineering: https://arxiv.org/abs/2503.13793
- A 2025 taxonomy of human-AI collaboration in software engineering identifies interaction types and research needs around control, trust, and usability: https://arxiv.org/abs/2501.08774
- A 2025 empirical study on LLM-assisted code review examines how developers perceive and interact with LLM support during review tasks: https://arxiv.org/abs/2505.16339
- A 2026 survey on LLM-enabled compilation identifies correctness and scalability as major challenges and hybrid systems as the promising path: https://arxiv.org/abs/2601.02045
- Agentic AI Software Engineers argues that future workflows should shift from programming at scale to programming with trust: https://arxiv.org/abs/2502.13767
- Reproducible, explainable evaluations of agentic AI for software engineering recommend exposing Thought-Action-Result trajectories and LLM interaction data for systematic comparison: https://arxiv.org/abs/2604.01437
- Sonar's 2026 developer survey reports a verification gap: most developers do not fully trust AI-generated code, but far fewer always verify it before committing: https://www.sonarsource.com/company/press-releases/sonar-data-reveals-critical-verification-gap-in-ai-coding/
- The local sandbox evaluation in `reports/sandbox_report.md` and `data/sandbox_evaluation.json` supports the same trust model: agent output should be bounded by execution controls, not trusted as text alone.

## Bottom Line

The durable position is not blind trust or blanket rejection. The strongest framework is conditional trust: read code when consequences are material, reduce generated diff size so reading is feasible, and raise trust only when independent verification gates are strong enough for the risk class.
