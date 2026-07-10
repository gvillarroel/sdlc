import assert from "node:assert/strict";
import test from "node:test";

import {
  DEFAULT_SKILLS_DIRECTORY,
  environmentForAuthMode,
  runAgent,
  runAgentChain,
} from "../src/runner.mjs";

function fakeRuntime() {
  const state = {
    configs: [],
    prompts: [],
    selected: [],
    started: 0,
    stopped: 0,
    disconnected: 0,
  };
  const client = {
    async start() {
      state.started += 1;
    },
    async createSession(config) {
      state.configs.push(config);
      const sdkAgent = config.customAgents[0];
      let activeAgent;
      let handler = () => undefined;
      const invoked = [];
      return {
        on(nextHandler) {
          handler = nextHandler;
          return () => undefined;
        },
        rpc: {
          agent: {
            async select({ name }) {
              activeAgent = name;
              state.selected.push(name);
              return {
                agent: {
                  name,
                  id: name,
                  skills: [...(sdkAgent.skills ?? [])],
                  tools: [...(sdkAgent.tools ?? [])],
                },
              };
            },
            async getCurrent() {
              return {
                agent: activeAgent
                  ? { name: activeAgent, id: activeAgent, skills: [...(sdkAgent.skills ?? [])] }
                  : null,
              };
            },
          },
          skills: {
            async ensureLoaded() {},
            async list() {
              return {
                skills: (sdkAgent.skills ?? []).map((name) => ({ name, enabled: true })),
              };
            },
            async getInvoked() {
              return { skills: invoked };
            },
          },
        },
        async sendAndWait(prompt, timeout) {
          state.prompts.push({ agent: activeAgent, prompt, timeout });
          for (const [index, name] of (sdkAgent.skills ?? []).entries()) {
            const data = {
              name,
              content: "skill-content-" + name,
              path: "/skills/" + name + "/SKILL.md",
              trigger: "agent-invoked",
            };
            invoked.push({ ...data, invokedAtTurn: index + 1 });
            handler({ type: "skill.invoked", data });
          }
          return { data: { content: activeAgent.toUpperCase() + "_OK output-" + state.selected.length } };
        },
        async disconnect() {
          state.disconnected += 1;
        },
      };
    },
    async stop() {
      state.stopped += 1;
      return [];
    },
  };
  return { client, state };
}

test("logged-in auth uses a minimal allowlist while inherited mode preserves explicit environment", () => {
  const source = {
    GITHUB_TOKEN: "bad",
    GH_TOKEN: "also-bad",
    DATABASE_URL: "secret",
    KEEP: "no",
    Path: "safe-path",
    USERPROFILE: "safe-home",
  };
  assert.deepEqual(environmentForAuthMode("logged-in", source), {
    Path: "safe-path",
    USERPROFILE: "safe-home",
  });
  assert.deepEqual(environmentForAuthMode("inherited", source), source);
});

test("creates an explicitly selected SDK agent session and cleans it up", async () => {
  const { client, state } = fakeRuntime();
  const result = await runAgent({
    agent: {
      name: "proof-agent",
      description: "Proof",
      prompt: "Start with a marker.",
      tools: [],
      permissionMode: "deny-all",
    },
    task: "Prove it",
    timeoutMs: 2_000,
    clientFactory: async () => client,
  });

  assert.equal("agent" in state.configs[0], false);
  assert.equal(state.configs[0].customAgents[0].name, "proof-agent");
  assert.deepEqual(state.configs[0].customAgents[0].tools, []);
  assert.equal(result.selectedAgent, "proof-agent");
  assert.equal(result.content, "PROOF-AGENT_OK output-1");
  assert.deepEqual(state, {
    configs: state.configs,
    prompts: state.prompts,
    selected: ["proof-agent"],
    started: 1,
    stopped: 1,
    disconnected: 1,
  });
});

test("executes skill agents in isolated sessions, verifies invocation, and passes output forward", async () => {
  const { client, state } = fakeRuntime();
  const agents = [
    {
      name: "requirements-agent",
      prompt: "Requirements",
      tools: [],
      skills: ["extract-requirements"],
      permissionMode: "deny-all",
    },
    {
      name: "risk-agent",
      prompt: "Risks",
      tools: [],
      skills: ["challenge-assumptions"],
      permissionMode: "deny-all",
    },
    {
      name: "plan-agent",
      prompt: "Plan",
      tools: [],
      skills: ["build-delivery-plan"],
      permissionMode: "deny-all",
    },
  ];

  const result = await runAgentChain({
    agents,
    task: "Build the POC",
    timeoutMs: 2_000,
    skillDirectories: [DEFAULT_SKILLS_DIRECTORY],
    clientFactory: async () => client,
  });

  assert.deepEqual(state.selected, ["requirements-agent", "risk-agent", "plan-agent"]);
  assert.equal(state.configs.length, 3);
  assert.equal(state.disconnected, 3);
  assert.deepEqual(
    state.configs.map(({ customAgents }) => customAgents[0].skills),
    [["extract-requirements"], ["challenge-assumptions"], ["build-delivery-plan"]],
  );
  assert.match(state.prompts[1].prompt, /REQUIREMENTS-AGENT_OK output-1/);
  assert.match(state.prompts[2].prompt, /RISK-AGENT_OK output-2/);
  assert.deepEqual(result.steps.map(({ selectedAgent }) => selectedAgent), state.selected);
  assert.deepEqual(
    result.steps.map(({ invokedSkills }) => invokedSkills),
    [["extract-requirements"], ["challenge-assumptions"], ["build-delivery-plan"]],
  );
  assert.equal(result.finalContent, "PLAN-AGENT_OK output-3");
});

test("mixed permission modes stay isolated per chain step", async () => {
  const { client, state } = fakeRuntime();
  await runAgentChain({
    agents: [
      { name: "locked", prompt: "Locked", tools: [], permissionMode: "deny-all" },
      { name: "reader", prompt: "Reader", tools: ["view"], permissionMode: "read-only" },
    ],
    task: "Inspect safely",
    timeoutMs: 2_000,
    clientFactory: async () => client,
  });

  assert.equal((await state.configs[0].onPermissionRequest({ kind: "read", path: "README.md" })).kind, "reject");
  assert.equal((await state.configs[1].onPermissionRequest({ kind: "read", path: "README.md" })).kind, "approve-once");
  assert.equal((await state.configs[1].onPermissionRequest({ kind: "shell", commands: [] })).kind, "reject");
});
