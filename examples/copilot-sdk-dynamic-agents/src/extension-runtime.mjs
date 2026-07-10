import { randomUUID } from "node:crypto";
import { join } from "node:path";

import { normalizeAgent, SAFE_READ_ONLY_TOOLS } from "./agent-schema.mjs";
import { parseChainArguments, parseCreateArguments, parseRunArguments } from "./command-parser.mjs";
import { DEMO_SKILL_AGENTS, DEMO_SKILL_AGENT_NAMES } from "./demo-agents.mjs";
import {
  getAgent,
  listAgents,
  removeAgents,
  upsertAgentWithStatus,
} from "./registry.mjs";
import { compactSkillDemoReport, createSkillDemoReport, writeSkillDemoReport } from "./results.mjs";
import { MAX_CHAIN_LENGTH, MAX_TASK_LENGTH, runAgent, runAgentChain } from "./runner.mjs";
import { resolveAgentSkills } from "./skills.mjs";

const AGENT_NAME_PATTERN = "^[a-z][a-z0-9-]{0,63}$";
const RESULT_REFERENCE = "examples/copilot-sdk-dynamic-agents/results/copilot-skill-demo.latest.json";

const CREATE_SCHEMA = {
  type: "object",
  additionalProperties: false,
  properties: {
    name: { type: "string", pattern: AGENT_NAME_PATTERN, description: "Lowercase kebab-case agent identifier." },
    displayName: { type: "string", maxLength: 128 },
    description: { type: "string", maxLength: 1024 },
    prompt: { type: "string", maxLength: 30000, description: "System instructions for the dynamic agent." },
    tools: {
      type: "array",
      uniqueItems: true,
      items: { type: "string", enum: [...SAFE_READ_ONLY_TOOLS].sort() },
    },
    infer: { type: "boolean" },
    model: { type: "string", maxLength: 128 },
    skills: {
      type: "array",
      uniqueItems: true,
      items: { type: "string", pattern: AGENT_NAME_PATTERN },
    },
    permissionMode: { type: "string", enum: ["deny-all", "read-only"] },
  },
  required: ["name", "description", "prompt"],
};

function agentSummary(agent) {
  return {
    name: agent.name,
    displayName: agent.displayName,
    description: agent.description,
    tools: agent.tools,
    skills: agent.skills,
    permissionMode: agent.permissionMode,
  };
}

function summarizeAgents(agents) {
  if (agents.length === 0) {
    return "No dynamic agents are registered.";
  }
  return agents
    .map((agent) => "- " + agent.name + ": " + (agent.description ?? "No description")
      + " [" + agent.permissionMode + "; skills=" + (agent.skills.join(", ") || "none") + "]")
    .join("\n");
}

function presentRun(result) {
  return {
    agent: result.agent,
    selectedAgent: result.selectedAgent,
    runtimeSkills: result.runtimeSkills,
    invokedSkills: result.invokedSkills,
    invocationEvidence: result.invocationEvidence,
    durationMs: result.durationMs,
    content: result.content,
  };
}

export async function startDynamicAgentExtension({
  joinSession,
  registryPath,
  repositoryRoot,
  copilotRuntimePath = process.execPath,
  runAgentImpl = runAgent,
  runAgentChainImpl = runAgentChain,
}) {
  if (typeof joinSession !== "function") {
    throw new TypeError("joinSession must be a function.");
  }

  const skillDirectories = [join(repositoryRoot, "examples", "copilot-sdk-dynamic-agents", "skills")];
  const demoResultPath = join(repositoryRoot, RESULT_REFERENCE);
  let session;

  const saveAgent = async (candidate) => {
    const normalized = normalizeAgent(candidate);
    await resolveAgentSkills(normalized, skillDirectories);
    return upsertAgentWithStatus(normalized, registryPath);
  };

  const executeAgent = async (name, task) => runAgentImpl({
    agent: await getAgent(name, registryPath),
    task,
    workingDirectory: repositoryRoot,
    skillDirectories,
    authMode: "logged-in",
    runtimePath: copilotRuntimePath,
  });

  const executeChain = async (names, task) => runAgentChainImpl({
    agents: await Promise.all(names.map((name) => getAgent(name, registryPath))),
    task,
    workingDirectory: repositoryRoot,
    skillDirectories,
    authMode: "logged-in",
    runtimePath: copilotRuntimePath,
  });

  const generateDemoAgents = async () => {
    const existingNames = new Set((await listAgents(registryPath)).map(({ name }) => name));
    const conflicts = DEMO_SKILL_AGENT_NAMES.filter((name) => existingNames.has(name));
    if (conflicts.length > 0) {
      throw new Error(
        "Skill demo requires fresh dynamic agent names; remove stale demo entries: " + conflicts.join(", ") + ".",
      );
    }
    const generated = [];
    try {
      for (const candidate of DEMO_SKILL_AGENTS) {
        generated.push(await saveAgent(candidate));
      }
      return generated;
    } catch (error) {
      await removeAgents(generated.map(({ agent }) => agent.name), registryPath);
      throw error;
    }
  };

  const executeSkillDemo = async (task, runId) => {
    let generated = [];
    try {
      // These identifiers are reserved for the demo. Clearing a stale prior
      // run guarantees that this invocation proves fresh post-join creation.
      await removeAgents(DEMO_SKILL_AGENT_NAMES, registryPath);
      generated = await generateDemoAgents();
      const result = await executeChain(DEMO_SKILL_AGENT_NAMES, task);
      const report = createSkillDemoReport({
        runId,
        generated,
        result,
        source: "copilot-extension-tool",
      });
      await writeSkillDemoReport(report, demoResultPath);
      return report;
    } finally {
      await removeAgents(generated.map(({ agent }) => agent.name), registryPath);
    }
  };

  const logChainResult = async (result) => {
    for (const step of result.steps) {
      await session.log(
        "Skill chain step " + step.index + "/" + result.steps.length + ": "
          + step.agent + " [" + (step.skills.join(", ") || "no skills") + "]\n" + step.content,
        { level: "info" },
      );
    }
  };

  const tools = [
    {
      name: "dynamic_agents_list",
      description: "List safe summaries of the runtime-configurable agents registered by this repository.",
      defer: "never",
      parameters: { type: "object", properties: {}, additionalProperties: false },
      handler: async () => ({ agents: (await listAgents(registryPath)).map(agentSummary) }),
    },
    {
      name: "dynamic_agents_upsert",
      description: "Create or update a validated dynamic SDK agent after verifying every configured skill.",
      defer: "never",
      parameters: CREATE_SCHEMA,
      handler: async (arguments_) => {
        const saved = await saveAgent(arguments_);
        return { agent: agentSummary(saved.agent), action: saved.action, status: "ready" };
      },
    },
    {
      name: "dynamic_agent_run",
      description: "Run a registered dynamic agent in an isolated SDK session with its own permission handler and skills.",
      defer: "never",
      parameters: {
        type: "object",
        additionalProperties: false,
        properties: {
          name: { type: "string", pattern: AGENT_NAME_PATTERN },
          task: { type: "string", minLength: 1, maxLength: MAX_TASK_LENGTH },
        },
        required: ["name", "task"],
      },
      handler: async ({ name, task }) => presentRun(await executeAgent(name, task)),
    },
    {
      name: "dynamic_agent_chain",
      description: "Run registered dynamic agents strictly one after another in isolated SDK sessions.",
      defer: "never",
      parameters: {
        type: "object",
        additionalProperties: false,
        properties: {
          names: {
            type: "array",
            minItems: 1,
            maxItems: MAX_CHAIN_LENGTH,
            uniqueItems: true,
            items: { type: "string", pattern: AGENT_NAME_PATTERN },
          },
          task: { type: "string", minLength: 1, maxLength: MAX_TASK_LENGTH },
        },
        required: ["names", "task"],
      },
      handler: async ({ names, task }) => {
        const result = await executeChain(names, task);
        return {
          durationMs: result.durationMs,
          steps: result.steps.map((step) => ({ index: step.index, ...presentRun(step) })),
        };
      },
    },
    {
      name: "dynamic_agents_skill_demo",
      description: "Create three fresh agents with different skills, run them sequentially, verify runtime skill events, and remove the temporary registry entries.",
      defer: "never",
      parameters: {
        type: "object",
        additionalProperties: false,
        properties: {
          task: { type: "string", minLength: 1, maxLength: MAX_TASK_LENGTH },
          runId: { type: "string", format: "uuid" },
        },
        required: ["task", "runId"],
      },
      handler: async ({ task, runId }) =>
        compactSkillDemoReport(await executeSkillDemo(task, runId), RESULT_REFERENCE),
    },
  ];

  const commands = [
    {
      name: "dynamic-agents",
      description: "List agents in the dynamic-agent registry.",
      handler: async () => {
        await session.log(summarizeAgents(await listAgents(registryPath)), { level: "info" });
      },
    },
    {
      name: "dynamic-agent-create",
      description: "Create or update an agent from an inline JSON object.",
      handler: async ({ args }) => {
        try {
          const saved = await saveAgent(parseCreateArguments(args));
          await session.log(
            "Dynamic agent '" + saved.agent.name + "' is ready (" + saved.action + ").",
            { level: "info" },
          );
        } catch (error) {
          await session.log(error instanceof Error ? error.message : String(error), { level: "error" });
        }
      },
    },
    {
      name: "dynamic-agent-run",
      description: "Run a registered agent. Syntax: /dynamic-agent-run <name> :: <task>",
      handler: async ({ args }) => {
        try {
          const { name, task } = parseRunArguments(args);
          const result = await executeAgent(name, task);
          await session.log(JSON.stringify(presentRun(result), null, 2), { level: "info" });
        } catch (error) {
          await session.log(error instanceof Error ? error.message : String(error), { level: "error" });
        }
      },
    },
    {
      name: "dynamic-agent-chain",
      description: "Run agents sequentially. Syntax: /dynamic-agent-chain <name-1,name-2> :: <task>",
      handler: async ({ args }) => {
        try {
          const { names, task } = parseChainArguments(args);
          await logChainResult(await executeChain(names, task));
        } catch (error) {
          await session.log(error instanceof Error ? error.message : String(error), { level: "error" });
        }
      },
    },
    {
      name: "dynamic-agent-skill-demo",
      description: "Create and execute the temporary three-agent skill demo for the supplied task.",
      handler: async ({ args }) => {
        try {
          const task = args.trim();
          if (!task) {
            throw new Error("Expected a task after /dynamic-agent-skill-demo.");
          }
          const report = await executeSkillDemo(task, randomUUID());
          await session.log(
            JSON.stringify(compactSkillDemoReport(report, RESULT_REFERENCE), null, 2),
            { level: "info" },
          );
        } catch (error) {
          await session.log(error instanceof Error ? error.message : String(error), { level: "error" });
        }
      },
    },
  ];

  session = await joinSession({ skillDirectories, commands, tools });
  return session;
}

export { CREATE_SCHEMA, agentSummary, presentRun, summarizeAgents };
