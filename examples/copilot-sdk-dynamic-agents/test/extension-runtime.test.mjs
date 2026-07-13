import assert from "node:assert/strict";
import { mkdir, mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import { startDynamicAgentExtension } from "../src/extension-runtime.mjs";

test("registers Copilot commands/tools and runs agents through an isolated SDK session", async () => {
  const repositoryRoot = await mkdtemp(join(tmpdir(), "dynamic-agent-extension-"));
  const registryPath = join(repositoryRoot, "registry.json");
  await mkdir(join(repositoryRoot, "examples", "copilot-sdk-dynamic-agents", "skills"), { recursive: true });
  await writeFile(registryPath, JSON.stringify({
    version: 1,
    agents: [{
      name: "proof-agent",
      description: "Proof",
      prompt: "Start with a marker.",
      tools: [],
      permissionMode: "deny-all",
    }],
  }), "utf8");

  const state = { logs: [], joinedConfig: null, runs: [] };
  const fakeSession = {
    async log(message, options) {
      state.logs.push({ message, options });
    },
  };
  const fakeRunAgent = async (options) => {
    state.runs.push(options);
    return {
      agent: options.agent.name,
      selectedAgent: options.agent.name,
      runtimeSkills: options.agent.skills ?? [],
      invokedSkills: options.agent.skills ?? [],
      invocationEvidence: [],
      durationMs: 1,
      content: "DYNAMIC_AGENT_OK",
    };
  };

  await startDynamicAgentExtension({
    joinSession: async (config) => {
      state.joinedConfig = config;
      return fakeSession;
    },
    registryPath,
    repositoryRoot,
    runAgentImpl: fakeRunAgent,
  });

  assert.equal("customAgents" in state.joinedConfig, false);
  assert.deepEqual(state.joinedConfig.tools.map(({ name }) => name), [
    "dynamic_agents_list",
    "dynamic_agents_upsert",
    "dynamic_agent_run",
    "dynamic_agent_chain",
    "dynamic_agents_skill_demo",
  ]);
  assert.equal(state.joinedConfig.skillDirectories.length, 1);

  const runCommand = state.joinedConfig.commands.find(({ name }) => name === "dynamic-agent-run");
  await runCommand.handler({ args: "proof-agent :: demonstrate the POC" });
  assert.equal(state.runs[0].agent.name, "proof-agent");
  assert.equal(state.runs[0].task, "demonstrate the POC");
  assert.match(state.logs.at(-1).message, /DYNAMIC_AGENT_OK/);

  const runTool = state.joinedConfig.tools.find(({ name }) => name === "dynamic_agent_run");
  const toolResult = await runTool.handler({ name: "proof-agent", task: "prove tool routing" });
  assert.equal(toolResult.selectedAgent, "proof-agent");
  assert.equal(state.runs.length, 2);

  const listTool = state.joinedConfig.tools.find(({ name }) => name === "dynamic_agents_list");
  const summary = (await listTool.handler({})).agents[0];
  assert.equal(summary.name, "proof-agent");
  assert.equal("prompt" in summary, false);
});

test("upsert validates configured skills before persisting", async () => {
  const repositoryRoot = await mkdtemp(join(tmpdir(), "dynamic-agent-extension-skills-"));
  const registryPath = join(repositoryRoot, "registry.json");
  await mkdir(join(repositoryRoot, "examples", "copilot-sdk-dynamic-agents", "skills"), { recursive: true });
  await writeFile(registryPath, '{"version":1,"agents":[]}\n', "utf8");
  let joinedConfig;
  await startDynamicAgentExtension({
    joinSession: async (config) => {
      joinedConfig = config;
      return { async log() {} };
    },
    registryPath,
    repositoryRoot,
  });

  const upsert = joinedConfig.tools.find(({ name }) => name === "dynamic_agents_upsert");
  await assert.rejects(
    () => upsert.handler({
      name: "missing-skill-agent",
      description: "Proof",
      prompt: "Proof",
      skills: ["does-not-exist"],
      tools: [],
      permissionMode: "deny-all",
    }),
    /not found/,
  );
});

test("skill demo replaces stale reserved entries, proves fresh creation, and cleans up", async () => {
  const repositoryRoot = await mkdtemp(join(tmpdir(), "dynamic-agent-extension-demo-"));
  const registryPath = join(repositoryRoot, "registry.json");
  const skillsRoot = join(repositoryRoot, "examples", "copilot-sdk-dynamic-agents", "skills");
  const definitions = [
    ["requirements-specialist", "extract-requirements", "SKILL_REQUIREMENTS_OK"],
    ["risk-challenger", "challenge-assumptions", "SKILL_RISK_OK"],
    ["delivery-planner", "build-delivery-plan", "SKILL_PLAN_OK"],
  ];
  for (const [, skill] of definitions) {
    await mkdir(join(skillsRoot, skill), { recursive: true });
    await writeFile(
      join(skillsRoot, skill, "SKILL.md"),
      "---\nname: " + skill + "\ndescription: Demo\n---\n\nProof.\n",
      "utf8",
    );
  }
  await writeFile(registryPath, JSON.stringify({
    version: 1,
    agents: [{
      name: "requirements-specialist",
      prompt: "stale",
      tools: [],
      skills: ["extract-requirements"],
      permissionMode: "deny-all",
    }],
  }), "utf8");

  let joinedConfig;
  await startDynamicAgentExtension({
    joinSession: async (config) => {
      joinedConfig = config;
      return { async log() {} };
    },
    registryPath,
    repositoryRoot,
    runAgentChainImpl: async ({ agents }) => ({
      durationMs: 3,
      steps: definitions.map(([agent, skill, marker], index) => ({
        index: index + 1,
        agent,
        selectedAgent: agent,
        skills: [skill],
        runtimeSkills: [skill],
        invokedSkills: [skill],
        skillEvents: [skill],
        invocationEvidence: [{
          name: skill,
          trigger: "agent-invoked",
          invokedAtTurn: 1,
          contentSha256: "b".repeat(64),
        }],
        content: marker,
        durationMs: 1,
      })),
      finalContent: "SKILL_PLAN_OK",
    }),
  });

  const demo = joinedConfig.tools.find(({ name }) => name === "dynamic_agents_skill_demo");
  const result = await demo.handler({ task: "prove", runId: "00000000-0000-4000-8000-000000000001" });
  assert.equal(result.status, "passed");
  assert.equal(result.generationProved, true);
  assert.equal(result.generatedAgents.every(({ action }) => action === "created"), true);
  assert.deepEqual(JSON.parse(await readFile(registryPath, "utf8")).agents, []);
});
