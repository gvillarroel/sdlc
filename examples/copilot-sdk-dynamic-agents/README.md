# Proof of Concept: Dynamic Agents with GitHub Copilot SDK

This proof of concept generates configurable agents, assigns distinct skills to them, and runs them sequentially through GitHub Copilot CLI. The live acceptance test is recorded as sanitized evidence in [copilot-skill-demo.latest.json](results/copilot-skill-demo.latest.json).

## What It Demonstrates

- A JSON registry creates or updates agents at runtime.
- The project extension uses `@github/copilot-sdk/extension` and exposes tools and slash commands inside Copilot CLI.
- The runner uses `@github/copilot-sdk` with `customAgents`, `skills`, `skillDirectories`, and explicit agent selection.
- Each step opens an isolated SDK session with its own permission handler; a mixed chain neither shares nor elevates permissions.
- The demo reserves its three names, removes remnants of interrupted runs, creates the agents after starting the extension, runs the chain, and deletes its temporary entries.
- The chain passes each agent's output to the next agent in this order:

```text
Prompt in Copilot
  → dynamic_agents_skill_demo
  → requirements-specialist  [extract-requirements]
  → risk-challenger          [challenge-assumptions]
  → delivery-planner         [build-delivery-plan]
  → verifiable JSON report
```

Each skill requires a distinct marker. The marker alone is insufficient: acceptance also verifies the agent returned by `agent.select/getCurrent`, the skills assigned by the runtime, `skills.getInvoked()`, and `skill.invoked` events with the `agent-invoked` trigger.

| Step | Agent | Skill | Evidence |
|---:|---|---|---|
| 1 | `requirements-specialist` | `extract-requirements` | `SKILL_REQUIREMENTS_OK` |
| 2 | `risk-challenger` | `challenge-assumptions` | `SKILL_RISK_OK` |
| 3 | `delivery-planner` | `build-delivery-plan` | `SKILL_PLAN_OK` |

## Project Structure

- `agents/registry.json`: dynamic configurations shared by the CLI and the extension.
- `skills/*/SKILL.md`: skills loaded through the official `skillDirectories` mechanism.
- `src/runner.mjs`: standalone SDK execution and a sequential chain with one session per step.
- `src/extension-runtime.mjs`: tools and commands registered in the active session.
- `.github/extensions/dynamic-agents/extension.mjs`: entry point discovered by Copilot CLI.
- `.github/agents/dynamic-agent-orchestrator.agent.md`: agent that operates the extension.
- `results/copilot-skill-demo.latest.json`: sanitized evidence from the latest acceptance run inside Copilot.

## Requirements

- Node.js `^20.19.0` or `>=22.12.0`, matching the pinned SDK requirements.
- An up-to-date, authenticated GitHub Copilot CLI.
- Access to GitHub Copilot or an SDK-compatible BYOK configuration.
- Experimental extensions enabled with `--experimental`.

The validated combination was Copilot CLI `1.0.70` with `@github/copilot-sdk` `1.0.5`.

## Offline Installation and Testing

From this directory:

```powershell
npm ci
npm test
npm run validate
```

The unit tests do not consume Copilot requests. They cover validation, missing skills, serialized registry mutations, canonical read scope, per-step permission isolation, chain order, result propagation, and runtime behavior.

Run the SDK smoke tests directly:

```powershell
npm run smoke:sdk
npm run smoke:skills
```

## Testing Inside Copilot

The recommended reproducible test grants the minimum permission required for a single extension tool:

```powershell
.\scripts\smoke-in-copilot.ps1
```

The script:

1. runs `copilot --experimental` with the `dynamic-agent-orchestrator` agent;
2. authorizes only `custom-tool(dynamic_agents_skill_demo)`;
3. requires three new names and generates agents with distinct skills after `joinSession`;
4. runs each step in an independent SDK session;
5. verifies the actual selection, assignment, and invocation of each skill, as well as the expected order and markers;
6. correlates the report with a unique `runId` and deletes the temporary agents;
7. updates `results/copilot-skill-demo.latest.json` without prompts, responses, local paths, or session IDs.

You can also test interactively from the repository root:

```powershell
copilot --experimental
```

Commands available in the TUI:

```text
/dynamic-agents
/dynamic-agent-create {"name":"my-agent","description":"...","prompt":"...","tools":[],"skills":["extract-requirements"],"permissionMode":"deny-all"}
/dynamic-agent-run my-agent :: Run this task
/dynamic-agent-chain requirements-specialist,risk-challenger,delivery-planner :: Design a secure proof of concept
/dynamic-agent-skill-demo Design a secure proof of concept
```

In prompt mode, project extensions require `GITHUB_COPILOT_PROMPT_MODE_EXTENSIONS=true`; the script sets it only for its own process.

## Proof-of-Concept Security

- Names and skills use a `lowercase-kebab-case` allowlist; every `SKILL.md` must exist inside an allowed directory and declare the same name.
- Registry writes are atomic, and in-process mutations are serialized to prevent lost updates.
- Dynamic agents support only `deny-all` and `read-only`; there is no `approve-all` mode.
- The default is `deny-all`, which requires `tools: []`.
- `read-only` accepts only `glob`, `grep`, `read`, `search`, and `view`; its handler approves only reads whose canonical path is inside the repository. Shell access, network access, MCP, writes, and sandbox bypasses are denied.
- Authenticated mode reduces the inherited environment to an operational allowlist and removes tokens and other arbitrary variables. `--auth inherited` exists only for explicit, trusted scenarios.
- The demo agents use `tools: []`; their skills transform text and do not run system commands.
- The publishable report retains hashes, lengths, and runtime evidence, but excludes generated content, prompts, user paths, and session IDs.
- Copilot CLI extensions are experimental and execute local code with the user's privileges. Load only trusted code.

This is a proof of concept, not a production sandbox. The allowlist and handlers restrict SDK capabilities, but they do not replace process or VM isolation, egress controls, secret management, or corporate policies.

## Official Sources

- [GitHub Copilot SDK](https://github.com/github/copilot-sdk)
- [Custom agents and sub-agent orchestration](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/custom-agents)
- [Custom skills](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/skills)
- [Streaming events in the Copilot SDK](https://docs.github.com/en/copilot/how-tos/copilot-sdk/use-copilot-sdk/streaming-events)
- [Creating extensions for GitHub Copilot CLI](https://docs.github.com/en/copilot/tutorials/create-an-extension)
- [Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference)

Legacy Copilot Extensions based on GitHub Apps are not used: GitHub retired them in November 2025. This proof of concept uses the current local Copilot CLI extension model.
