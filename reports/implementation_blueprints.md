# Implementation Blueprints

Date: 2026-07-05

These blueprints describe what to build first for the highest-priority candidates. They are not installation docs; they are pilot architecture notes.

For a generated candidate-by-candidate estimate of prototype effort, hardening effort, first slice, and adoption caution, see `results/implementation_effort_estimates.csv`.

## OpenHands Software Agent SDK

Best use: Python foundation for a custom software-agent system.

First prototype:

1. Wrap one repository fixture in a disposable workspace.
2. Define tools for read, edit, shell, tests, and patch export.
3. Add policy checks for workspace boundary, network access, and secret paths.
4. Capture prompts, tool calls, shell output, diff, tests, and final status.
5. Run 5 pilot tasks before adding subagents or custom memory.

Instrumentation:

- Task ID and trial ID
- Workspace ID
- Tool call trace
- Test command output
- Diff stats
- Reviewer scorecard

Avoid:

- Building a broad UI before proving task quality
- Giving the agent unrestricted shell/network access
- Hiding failed intermediate attempts from reviewers

## Deep Agents

Best use: custom Python orchestration where tools, state, memory, and subagents matter.

First prototype:

1. Implement a small toolset with explicit permission boundaries.
2. Run the same tasks with a single-agent graph and a subagent-enabled graph.
3. Compare context length, task success, trace readability, and intervention count.
4. Add memory only after identifying a task that genuinely benefits from it.

Instrumentation:

- Graph step trace
- Tool-level latency
- Context growth per turn
- Subagent invocation count
- Human interruption points

Avoid:

- Treating the framework as a turnkey coding product
- Adding memory before there is a measured need
- Mixing model changes with harness changes in the same experiment

## Flue

Best use: TypeScript-first product agent framework.

First prototype:

1. Create a minimal agent server with one coding or triage workflow.
2. Configure a virtual sandbox first.
3. Add durable state only after the in-memory path is proven.
4. Repeat the same task with a container or remote sandbox if needed.
5. Export logs into the common pilot run log.

Instrumentation:

- Session ID
- Tool calls
- Sandbox mode
- Deployment target
- State adapter choice
- Trace/log URL

Avoid:

- Adopting beta APIs without a version pin
- Combining deployment, durable state, and sandbox migration in the first prototype
- Assuming TypeScript ergonomics solve security policy

## Codex CLI

Best use: OpenAI-centered secure local/CI coding runner.

First prototype:

1. Run one task in read-only mode to inspect behavior.
2. Run one task in workspace-write mode.
3. Run one task with network disabled, then with the minimal allowlist if needed.
4. Capture approval prompts and denied actions.
5. Add CI only after the local policy profile is proven.

Instrumentation:

- Sandbox mode
- Approval decisions
- Denied commands
- Network policy state
- Test command output
- Final patch

Avoid:

- Starting with broad network access
- Treating provider lock-in as a non-issue if procurement requires neutrality
- Letting the agent push directly to protected branches

## Cline / Cline SDK

Best use: developer workflow with strong human control and broad surfaces.

First prototype:

1. Run one interactive IDE/CLI task and one headless SDK task.
2. Compare intervention count and reviewer acceptance.
3. Define default approval rules for low, medium, and high-risk actions.
4. Capture checkpoints and final diffs.

Instrumentation:

- Approval count
- Checkpoint count
- Human repair count
- Reviewer acceptance
- Runtime mode: IDE, CLI, or SDK

Avoid:

- Treating approvals as equivalent to hard sandboxing
- Measuring only successful interactive demos
- Letting auto-approve expand without task-level safety evidence

## mini-SWE-agent

Best use: minimal reproducible research baseline.

First prototype:

1. Run a small task suite with fixed seed, model, and timeout.
2. Record every trajectory and patch.
3. Modify one harness behavior at a time.
4. Compare pass rate, trajectory length, and cost.

Instrumentation:

- Seed
- Model
- Trajectory length
- Patch size
- Pass/fail reason
- Cost and latency

Avoid:

- Expecting enterprise controls out of the box
- Adding platform features before preserving minimal reproducibility
- Comparing against larger frameworks without noting feature-scope differences

## Open SWE

Best use: async issue-to-PR internal coding-agent platform.

First prototype:

1. Connect one sandbox provider.
2. Run 5 issue-to-PR tasks.
3. Measure queue time, sandbox startup time, task time, and PR review acceptance.
4. Add Slack/Linear/GitHub workflow integration only after core PR quality is credible.

Instrumentation:

- Queue latency
- Sandbox provider and startup time
- PR URL
- Test logs
- Human intervention count
- Trace URL

Avoid:

- Starting with too many integrations
- Treating cloud sandbox reliability as a given
- Skipping human review because the PR was created automatically
