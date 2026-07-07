# Internal Organizational Benchmarks For Agent Harnesses

Date: 2026-07-07

## Executive Position

An internal benchmark for agent harnesses should measure whether a harness can complete the organization's real work under the organization's constraints. Public benchmarks such as SWE-bench are useful calibration references, but they are not enough for adoption decisions because they do not cover private build systems, internal code conventions, repository scale, approval rules, data boundaries, deployment policies, or reviewer trust.

The right benchmark is a controlled production simulator:

1. Representative tasks copied or synthesized from real internal work.
2. Hermetic repositories or worktrees with seeded bugs, tests, fixtures, policies, and expected artifacts.
3. A common adapter contract so every harness is run through the same lifecycle.
4. Automatic checks for correctness, tests, safety, cost, latency, observability, and reproducibility.
5. Human review scoring for diff quality, maintainability, minimality, and whether a normal reviewer would accept the change.
6. A private holdout set and governance process that prevents benchmark overfitting and leakage.

The existing repository already contains most of the decision scaffolding needed to start: `data/pilot_tasks.json`, `data/pilot_decision_model.json`, `data/security_evaluation_fixtures.json`, `templates/pilot_run_log.csv`, `templates/reviewer_scorecard.md`, `templates/security_gate_checklist.md`, and `examples/pilot_adapter_contract.py`. The missing layer is a real internal benchmark pack: repository fixtures, task manifests, harness runners, automatic graders, and a governance process around task selection and refresh.

## What The Benchmark Should Decide

The benchmark should answer four separate questions. Keeping them separate prevents a high pass rate from hiding unsafe or unmaintainable behavior.

| Decision Question | Primary Evidence | Do Not Substitute With |
|---|---|---|
| Can the harness solve our tasks? | Task success, test pass, acceptance criteria pass | Public benchmark leaderboard |
| Can humans safely review the output? | Reviewer acceptance, diff minimality, explanation quality | Agent transcript fluency |
| Can the harness operate inside policy? | Sandbox, network, secret, approval, and provenance gates | Vendor promises or default settings |
| Can the team run it repeatedly? | Setup time, flake rate, cost, latency, artifact completeness | One successful demo |

The benchmark should not try to produce one universal score for all organizational uses. It should produce profiles, such as controlled developer assistant, CI repair bot, autonomous PR lane, documentation maintenance, dependency update lane, security-remediation lane, and research harness.

## Lessons From External Benchmarks And Eval Frameworks

Public and research benchmarks provide useful design patterns, but each pattern must be adapted for internal use.

| Source Pattern | What To Reuse | Internal Adaptation |
|---|---|---|
| SWE-bench issue-to-patch tasks | Use real repository tasks, tests, and patch-based scoring | Build tasks from internal issue history and private repositories |
| SWE-bench Verified-style curation | Human validation improves task quality | Require task author plus independent reviewer before adding tasks |
| OpenAI Evals-style datasets and graders | Separate samples, model outputs, and graders | Store task manifests, run traces, and graders as versioned artifacts |
| Inspect AI-style solver/scorer/sandbox separation | Keep agent logic, task environment, and scoring separate | Define one runner lifecycle for every harness and a sandbox profile per task |
| HELM-style scenarios and metrics | Evaluate by scenario, not just aggregate average | Publish scenario scorecards for each internal workflow |
| METR-style task families and time horizons | Measure task duration and autonomy boundaries | Add intervention budgets and maximum autonomous action limits |
| WorkArena/WebArena-style environment tasks | Test tool use in realistic UI/API environments | Add browser, CLI, ticketing, repository, and CI tasks only when they match real workflows |
| NIST AI RMF measurement mindset | Tie measurement to risk management | Convert benchmark failures into adoption gates and mitigations |

The most important lesson is methodological: the harness should be evaluated as a system. Model quality, tool design, sandboxing, prompt policy, repository fixture quality, reviewer workflow, and CI gates all affect the result. A benchmark that only records "task passed" will mis-rank systems that are risky, expensive, brittle, or impossible to audit.

## Benchmark Object Model

Use a small, explicit object model rather than an ad hoc folder of prompts.

| Object | Purpose | Required Fields |
|---|---|---|
| Benchmark suite | Versioned collection of task packs | Suite id, owner, version, scenario weights, changelog |
| Task pack | Group of related tasks for one workflow | Category, difficulty mix, target repositories, required tools |
| Task case | One runnable benchmark item | Task id, prompt, repo fixture, start commit, allowed files, acceptance criteria |
| Environment spec | Reproducible runtime | Image, language/runtime versions, dependency cache, network policy, secrets policy |
| Grader | Automatic scoring logic | Test commands, static checks, artifact checks, policy checks, scoring function |
| Harness adapter | Candidate integration wrapper | Setup, run, stop, collect artifacts, reset, cost accounting |
| Run record | Immutable execution result | Candidate, model, task, seed, timestamps, status, costs, logs, patches, scores |
| Review record | Human review result | Reviewer id or role, acceptance, review friction, maintainability notes |
| Decision report | Stakeholder-facing result | Scenario rankings, gates, failure taxonomy, recommendation, residual risks |

This object model lets the organization add more harnesses without rewriting the benchmark and add more tasks without rewriting each harness integration.

## Proposed Repository Layout

Use a dedicated benchmark root so task fixtures do not get mixed into the main evaluation report.

```text
benchmarks/
  README.md
  suites/
    coding-agent-v1/
      suite.yaml
      task_manifest.yaml
      scoring.yaml
      scenarios.yaml
      tasks/
        BUG-001/
          task.yaml
          prompt.md
          acceptance.md
          seed.patch
          expected_signals.yaml
          graders/
            grade.py
        SEC-001/
          task.yaml
          prompt.md
          malicious_issue_body.md
          secret_trap.txt
          graders/
            grade.py
      fixtures/
        service-api/
          repo.bundle
          start_commit.txt
          environment.yaml
      holdout/
        encrypted_or_access_controlled_tasks/
  harnesses/
    adapters/
      codex_cli.py
      openhands.py
      mini_swe_agent.py
    runner.py
    artifact_schema.json
  results/
    raw/
    normalized/
    reports/
```

The exact names can change, but the separation should remain: suites define what to run, harnesses define how candidates run, results preserve what happened.

## Task Selection Strategy

Start with the task suite already defined in `data/pilot_tasks.json`, then replace abstract task descriptions with runnable internal fixtures. The first internal benchmark should contain 30 to 60 tasks, not hundreds. Quality and representativeness matter more than volume.

Recommended first-suite mix:

| Task Family | Share | Examples | Why It Matters |
|---|---:|---|---|
| Bug fixes | 30% | Pagination, timezone, cache invalidation, async race | Measures diagnosis and minimal patching |
| Test generation | 15% | Missing unit, integration, property-style tests | Measures ability to improve safety nets |
| Refactors | 15% | Reduce complexity, parser-backed rewrite, module split | Measures maintainability and local conventions |
| Dependency updates | 10% | Minor API change, lockfile update, migration notes | Measures tool use, package management, and CI discipline |
| Documentation/code navigation | 10% | Update architecture notes from current code | Measures repository understanding |
| CI/build repair | 10% | Failing job, flaky test, platform-specific failure | Measures operational debugging |
| Security/policy fixtures | 10% | Prompt injection, secret trap, network deny | Measures safety under adversarial conditions |

Task inclusion criteria:

1. The task maps to a real internal workflow.
2. A competent engineer can solve it in a bounded time.
3. The expected outcome can be validated by tests, static checks, artifact checks, or reviewer rubric.
4. The starting repository state is reproducible.
5. The task has at least one clear failure mode.
6. The task does not expose production secrets, customer data, or export-controlled code.

Task exclusion criteria:

1. The task is mainly product judgment with no verifiable outcome.
2. It requires undocumented tribal knowledge unless that is the explicit behavior being tested.
3. It depends on live production services.
4. It has no stable oracle and cannot be reviewed consistently.
5. It is so large that failure cannot be classified cleanly.

## Turning Internal Work Into Benchmark Tasks

Use a three-stage conversion process.

### Stage 1: Mine Candidate Work

Sources:

- Closed internal tickets and PRs.
- Flaky CI incidents.
- Security remediation tickets.
- Dependency upgrade PRs.
- Documentation drift fixes.
- Repeated reviewer complaints about agent-generated code.
- Postmortems where code navigation or tests were difficult.

For each candidate task, capture:

- Original problem statement.
- Repository and commit range.
- Human patch summary.
- Tests that failed before and passed after.
- Review comments.
- Runtime assumptions.
- Sensitive data concerns.

Do not add raw internal tickets directly to the benchmark. Normalize them into task cases.

### Stage 2: Sanitize And Reconstruct

For each task:

1. Remove customer data, tokens, internal hostnames, and unnecessary business identifiers.
2. Keep the technical shape of the task intact.
3. Create a fixture repository or branch at the pre-fix state.
4. Add failing tests only if they existed or if they represent the real acceptance criteria.
5. Preserve the original human solution only in a restricted reference area, not in the prompt.
6. Add canary strings to detect leakage of hidden solution material.

Synthetic tasks are acceptable when they are calibrated against real internal failure modes. A synthetic task should have a provenance note explaining which real workflow it represents.

### Stage 3: Validate The Task

Before a task enters the benchmark:

1. A task author confirms the task is realistic.
2. A second engineer solves or reviews the task without seeing the hidden solution.
3. The grader fails on the starting state.
4. The grader passes on the reference solution.
5. The task runs twice in a clean environment with identical results.
6. The task owner records expected difficulty, time budget, and likely failure modes.

Tasks that cannot pass this validation become training or exploratory tasks, not benchmark tasks.

## Harness Adapter Contract

The benchmark should not call each candidate with custom logic. It should call a common adapter inspired by `examples/pilot_adapter_contract.py`.

Required adapter lifecycle:

1. `prepare(task, environment)` installs or verifies candidate dependencies.
2. `reset(task)` restores the fixture to the exact starting state.
3. `run(task, budget, policy)` executes the harness with the task prompt.
4. `stop(run_id)` terminates runaway processes.
5. `collect(run_id)` returns logs, patches, tool calls, cost, latency, and policy events.
6. `cleanup(run_id)` removes temporary resources.

Required normalized result fields:

| Field | Meaning |
|---|---|
| `candidate_id` | Harness or product under test |
| `candidate_version` | Pinned version or commit |
| `model_id` | Model used for the run |
| `task_id` | Benchmark task |
| `suite_version` | Benchmark suite version |
| `status` | pass, partial, fail, safety_fail, infra_fail |
| `patch_path` | Final diff artifact |
| `logs_path` | Transcript and tool logs |
| `tests_run` | Test commands attempted |
| `tests_passed` | Test pass indicator or count |
| `wall_clock_seconds` | End-to-end latency |
| `tokens_input` | Input token estimate or provider value |
| `tokens_output` | Output token estimate or provider value |
| `estimated_cost_usd` | Normalized cost estimate |
| `human_interventions` | Count and type of human assistance |
| `unsafe_actions` | Forbidden actions attempted |
| `artifact_completeness` | Whether required artifacts are present |

The adapter must record what happened even when the candidate fails. A benchmark that only records successful runs is not useful for adoption.

## Environment And Reproducibility Controls

Minimum controls:

| Control | Requirement |
|---|---|
| Repository state | Fresh worktree or container per run |
| Dependency versions | Lockfiles, pinned tool versions, cached base image |
| Network | Default deny, explicit allowlist per task |
| Secrets | No real secrets; seeded secret traps for safety tests |
| Time budget | Fixed per task family and difficulty |
| Cost budget | Fixed per candidate profile |
| Model policy | Same model where possible; otherwise record model difference as a factor |
| Randomness | Fixed seeds where supported; repeated trials for stochastic runs |
| Artifacts | Prompt, config, logs, commands, patches, tests, scores, and review notes |
| Reset | Clean state after every run |

Infrastructure failures should be separated from model or harness failures. An `infra_fail` should not count as a task failure unless the harness caused it, but repeated infrastructure failures should count against operational readiness.

## Scoring Model

The current `data/pilot_decision_model.json` is a good starting point. For an internal benchmark, use a two-layer model:

1. Hard gates that block adoption.
2. Weighted scores used only after gates pass.

Hard gates:

| Gate | Default Threshold |
|---|---:|
| Safety failures | 0 unresolved |
| Artifact completeness | >= 90% |
| Task success on target scenario | >= 70% |
| Reviewer acceptance | >= 60% |
| Policy compliance | 100% for protected resources |
| Reproducibility | >= 95% clean rerun rate for accepted tasks |

Weighted score after gates:

| Component | Suggested Weight |
|---|---:|
| Correct task completion | 25% |
| Review acceptance and diff quality | 20% |
| Safety and policy behavior | 20% |
| Observability and replayability | 10% |
| Cost and latency | 10% |
| Setup and maintenance burden | 10% |
| Scenario-specific fit | 5% |

For autonomous or semi-autonomous use, safety should be a gate and a weighted component. The weighted component distinguishes candidates after they pass the gate; it must not compensate for a gate failure.

## Automatic Graders

Each task should have a primary grader and optional secondary graders.

Primary grader options:

- Unit or integration test command.
- Static analyzer or linter.
- Golden-output comparison.
- API contract test.
- Migration verification.
- Security policy check.
- File-system diff constraint.

Secondary grader options:

- Diff size and file-count thresholds.
- Forbidden file modification check.
- Public API compatibility check.
- Dependency lockfile consistency check.
- Repeated-test flake check.
- Log completeness check.
- Secret redaction check.
- Network access audit.

Do not use an LLM judge as the only grader for code correctness. If an LLM judge is used, restrict it to review assistance, rubric consistency, failure taxonomy suggestions, or natural-language quality checks, and calibrate it against human labels.

## Human Review Rubric

Human review is not optional for organizational benchmarks because tests do not capture maintainability, local conventions, unnecessary rewrites, or trust. Use `templates/reviewer_scorecard.md` as the base.

Reviewer dimensions:

| Dimension | Question |
|---|---|
| Acceptability | Would this patch be accepted in a normal PR? |
| Minimality | Did it change only what the task required? |
| Correctness beyond tests | Does the solution make sense for edge cases not covered by tests? |
| Convention fit | Does it follow local patterns? |
| Maintainability | Would the owning team be comfortable maintaining it? |
| Explainability | Can the reviewer explain the change without replaying the full transcript? |
| Repair burden | How much human work is needed before merge? |

Recommended review process:

1. Review the diff first without reading the agent transcript.
2. Record accept, accept with edits, reject, or unsafe.
3. Then inspect the transcript only if needed to classify failures.
4. Record whether the agent's reasoning helped or hurt review confidence.
5. Resolve reviewer disagreement with a second reviewer for high-stakes scenarios.

## Safety And Policy Fixtures

Use `data/security_evaluation_fixtures.json` and `templates/security_gate_checklist.md` as the starting point. Every autonomous benchmark profile should include adversarial tasks.

Minimum safety fixtures:

| Fixture | Expected Behavior |
|---|---|
| Prompt injection in issue body | Treat issue content as untrusted data |
| Planted secret trap | Do not read, reveal, or summarize secret-like values |
| Forbidden path | Do not write outside the allowed workspace |
| Network deny | Do not bypass denied hosts to finish the task |
| Protected branch | Do not push or force-write protected refs |
| Dependency install | Use approved sandbox and package policy |
| Log redaction | Redact credential-like values in artifacts |

Safety scoring should distinguish:

- Attempted unsafe action blocked by sandbox.
- Attempted unsafe action not blocked by harness.
- Unsafe action proposed in text but not executed.
- Unsafe action executed.
- Unsafe action hidden by incomplete logs.

The last case should be treated as a serious observability failure.

## Statistical Design

Do not over-invest in statistical precision before task quality is high. The first useful internal suite should focus on coverage and failure taxonomy. Once the suite is stable, use repetitions and confidence intervals.

Recommended phases:

| Phase | Tasks | Trials | Purpose |
|---|---:|---:|---|
| Smoke | 3-5 | 1 | Verify adapter, artifacts, and reset |
| Screening | 20-30 | 1 | Find obvious no-go candidates |
| Selection | 30-60 | 3 | Compare shortlist candidates |
| Regression | Stable subset 20-40 | 1 per release | Detect harness or model regressions |
| Research | 60+ | 5+ | Support stronger claims about capability |

Report confidence honestly:

- Use Wilson intervals or bootstrap intervals for pass rates.
- Treat close rankings as ties.
- Separate pass rate from safety gate rate.
- Report task-family breakdowns, not only aggregate average.
- Report flake rate and rerun consistency.
- Keep a private holdout suite for final decisions.

The existing `reports/pilot_sample_size.md` already warns that close candidates may remain unresolved with small task counts. Internal benchmark reporting should preserve that caution.

## Leakage, Overfitting, And Benchmark Integrity

Internal benchmarks are valuable because they are private. They lose value quickly if prompts, hidden tests, reference patches, or task labels leak into agent memory, training data, shared logs, or vendor debugging flows.

Controls:

1. Split tasks into public-internal training, validation, and restricted holdout sets.
2. Store hidden tests and reference patches separately from prompts.
3. Add canary strings to hidden files and detect whether they appear in outputs.
4. Rotate some tasks every quarter.
5. Keep task authors separate from harness operators when possible.
6. Log every access to restricted tasks.
7. Do not paste holdout tasks into shared external systems.
8. Require vendor/provider data-retention settings appropriate for confidential evaluation.
9. Record model, tool, and prompt versions for every run.
10. Retire tasks that become known to candidate maintainers or appear in public examples.

For organizational use, benchmark integrity is not academic housekeeping. It directly affects adoption risk.

## Reporting Format

Each benchmark report should include:

- Suite version and task inventory.
- Candidate versions, model versions, and runtime configuration.
- Scenario-level scores.
- Hard gate results.
- Task-family breakdown.
- Safety fixture results.
- Cost and latency distribution.
- Review acceptance and repair burden.
- Failure taxonomy.
- Artifact completeness and replayability.
- Known invalid runs and rerun policy.
- Decision recommendation.
- Residual risks and required mitigations.

Recommended result tables:

| Table | Purpose |
|---|---|
| Candidate summary | One row per candidate with gate status and scenario score |
| Task outcomes | One row per candidate/task/trial |
| Safety outcomes | One row per safety fixture |
| Review outcomes | Acceptance and repair-burden distribution |
| Cost/latency | P50, P90, max, and budget violations |
| Failure taxonomy | Counts by root cause |
| Artifact completeness | Missing logs, patches, costs, traces, tests |

## Governance Model

Assign explicit owners:

| Role | Responsibility |
|---|---|
| Benchmark owner | Owns suite roadmap, versioning, release notes |
| Domain task owner | Confirms task realism and expected solution shape |
| Security owner | Approves policy fixtures and gate thresholds |
| Harness owner | Maintains adapter and candidate configuration |
| Reviewer pool | Scores patches and calibrates rubric |
| Data steward | Controls access to holdout tasks and sensitive fixtures |
| Decision owner | Converts benchmark evidence into adoption decision |

Governance cadence:

- Weekly during initial build.
- Monthly while candidates are actively changing.
- Quarterly for task refresh and leakage review.
- Per release for regression benchmark runs.

Every suite version should have release notes: added tasks, retired tasks, changed graders, changed thresholds, known limitations, and comparability notes against prior versions.

## Implementation Roadmap

### First 10 Hours: Produce The Design And Inventory

1. Inventory existing artifacts: `data/pilot_tasks.json`, `data/pilot_decision_model.json`, `data/security_evaluation_fixtures.json`, `templates/pilot_run_log.csv`, `templates/reviewer_scorecard.md`, `templates/security_gate_checklist.md`, and `examples/pilot_adapter_contract.py`.
2. Define benchmark goals and target scenarios.
3. Select first task families and target repositories.
4. Draft suite object model and required result schema.
5. Identify first 10 candidate tasks from internal issue/PR history.
6. Define hard gates and default scoring.
7. Draft security fixture requirements.
8. Produce this benchmark-generation report.

### First Week: Build A Runnable Prototype

1. Create benchmark repository layout.
2. Convert 5 to 10 tasks into runnable fixtures.
3. Implement one harness adapter end to end.
4. Implement automatic grading for each prototype task.
5. Generate normalized run records.
6. Run smoke tests and verify artifact completeness.
7. Run one human review calibration session.

Exit criteria:

- Every prototype task fails before the agent run or has a clear expected check.
- At least one candidate can run through the full lifecycle.
- Results include prompt, logs, patch, test output, cost, latency, and grader outcome.

### First Month: Selection-Grade Benchmark

1. Expand to 30 to 60 tasks.
2. Add at least three harness adapters.
3. Add repeated trials for shortlist candidates.
4. Add safety fixture pack.
5. Add reviewer calibration and disagreement handling.
6. Add CI workflow for benchmark validation.
7. Produce first selection report.

Exit criteria:

- Task suite covers the target workflows.
- Safety gates can block candidates.
- Close rankings are reported as ties.
- The organization can defend an adopt, defer, or reject decision.

### Ongoing: Benchmark Operations

1. Run regression suite on candidate upgrades.
2. Rotate holdout tasks.
3. Track drift in model behavior, cost, latency, and failure modes.
4. Retire flaky or leaked tasks.
5. Add tasks from new incidents and new workflow needs.
6. Keep a traceability link from adoption risks to benchmark evidence.

## Recommended Minimum Viable Benchmark

For the first organizational benchmark release:

- 30 tasks total.
- 6 task families.
- 2 repositories or fixtures.
- 3 candidate harnesses.
- 1 common model where possible.
- 1 fixed budget profile.
- 6 safety fixtures.
- 2 human reviewers for at least high-impact tasks.
- 3 trials only for the final shortlist.

Minimum deliverables:

- Suite manifest.
- Task manifest.
- Environment specs.
- Harness adapter interface.
- Normalized run schema.
- Automatic graders.
- Reviewer rubric.
- Safety gate checklist.
- Benchmark report template.
- Artifact retention policy.

## Failure Taxonomy

Classify failures consistently. This is often more valuable than the raw score.

| Failure Class | Examples | Owner |
|---|---|---|
| Task misunderstanding | Solves adjacent problem, ignores acceptance criterion | Prompt/task owner |
| Code navigation failure | Edits wrong module, misses existing helper | Harness/model |
| Test failure | New or existing tests fail | Harness/model |
| Over-broad diff | Large unrelated rewrite, formatting churn | Reviewer/harness |
| Policy violation | Reads secret, writes forbidden path, network bypass | Security/harness |
| Tool failure | Shell, git, package manager, browser, or CI misuse | Harness |
| Environment failure | Fixture cannot install, flaky external dependency | Benchmark owner |
| Observability failure | Missing logs, patch, cost, or tool-call trace | Harness owner |
| Review failure | Correct enough but unacceptable to maintainers | Harness/model |
| Cost/latency failure | Exceeds budget or times out | Harness/model/provider |

Use the taxonomy to improve the benchmark and the harness separately. Do not blame the model for broken fixtures, and do not blame the fixture when the harness hides unsafe behavior.

## Anti-Patterns

Avoid these design mistakes:

1. Ranking candidates only by public benchmark scores.
2. Using tasks that are too broad to grade.
3. Mixing harness failures, model failures, and environment failures into one `fail` label.
4. Letting a pass rate compensate for safety violations.
5. Storing hidden solutions beside prompts.
6. Allowing harness-specific prompts that make comparisons unfair.
7. Ignoring diff quality because tests pass.
8. Running tasks against mutable branches.
9. Counting demos as benchmark evidence.
10. Reporting one aggregate score without task-family breakdowns.

## Relationship To Existing Repository Artifacts

The current repository can become the benchmark control plane with these mappings:

| Existing Artifact | Reuse |
|---|---|
| `data/pilot_tasks.json` | Seed task taxonomy and initial manifest |
| `data/pilot_decision_model.json` | Initial gates and score weights |
| `data/security_evaluation_fixtures.json` | Security fixture catalog |
| `data/risk_register.json` | Risk-to-evidence mapping |
| `reports/pilot_protocol.md` | Execution protocol baseline |
| `reports/pilot_sample_size.md` | Task-count caution and comparison planning |
| `reports/risk_validation_matrix.md` | Adoption gate evidence map |
| `templates/pilot_run_log.csv` | Run logging template |
| `templates/reviewer_scorecard.md` | Human review rubric baseline |
| `templates/security_gate_checklist.md` | Safety gate checklist |
| `examples/pilot_adapter_contract.py` | First adapter interface draft |

The next engineering step is to add runnable benchmark fixtures and a runner, not to add more abstract scoring criteria.

## Source Notes

Sources used as design references:

- SWE-bench official site: https://www.swebench.com/
- SWE-bench GitHub organization: https://github.com/swe-bench
- OpenAI Evals repository: https://github.com/openai/evals
- OpenAI Evals guide: https://platform.openai.com/docs/guides/evals
- Inspect AI documentation: https://inspect.aisi.org.uk/
- HELM documentation and project: https://crfm.stanford.edu/helm/
- METR evaluations and research: https://metr.org/
- GAIA benchmark paper/project: https://arxiv.org/abs/2311.12983
- WorkArena benchmark project: https://github.com/ServiceNow/WorkArena
- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework

These sources were used for benchmark design patterns. The proposed process above is tailored to the internal harness-selection artifacts already present in this repository.
