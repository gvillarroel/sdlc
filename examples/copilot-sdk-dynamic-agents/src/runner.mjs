import { createHash } from "node:crypto";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { toCopilotAgentConfig } from "./agent-schema.mjs";
import { createPermissionHandler } from "./permissions.mjs";
import { resolveAgentSkills } from "./skills.mjs";

export const DEFAULT_SKILLS_DIRECTORY = fileURLToPath(new URL("../skills", import.meta.url));
export const MAX_CHAIN_LENGTH = 8;
export const MAX_TASK_LENGTH = 10_000;

const SAFE_LOGGED_IN_ENVIRONMENT = new Set([
  "APPDATA",
  "COLORTERM",
  "COMSPEC",
  "COPILOT_HOME",
  "GH_CONFIG_DIR",
  "GITHUB_CONFIG_DIR",
  "HOME",
  "HOMEDRIVE",
  "HOMEPATH",
  "LANG",
  "LC_ALL",
  "LOCALAPPDATA",
  "NO_COLOR",
  "PATH",
  "PATHEXT",
  "SSL_CERT_DIR",
  "SSL_CERT_FILE",
  "SYSTEMDRIVE",
  "SYSTEMROOT",
  "TEMP",
  "TERM",
  "TMP",
  "TMPDIR",
  "USERPROFILE",
  "WINDIR",
  "XDG_CACHE_HOME",
  "XDG_CONFIG_HOME",
]);

function validateExecutionOptions(task, timeoutMs) {
  if (typeof task !== "string" || task.trim().length === 0) {
    throw new TypeError("A non-empty task is required.");
  }
  if (task.length > MAX_TASK_LENGTH) {
    throw new RangeError("Task exceeds " + MAX_TASK_LENGTH + " characters.");
  }
  if (!Number.isInteger(timeoutMs) || timeoutMs < 1_000) {
    throw new TypeError("timeoutMs must be an integer of at least 1000 milliseconds.");
  }
}

export function environmentForAuthMode(mode, source = process.env) {
  if (!new Set(["logged-in", "inherited"]).has(mode)) {
    throw new TypeError("Unsupported auth mode '" + mode + "'.");
  }
  if (mode === "inherited") {
    return { ...source };
  }
  return Object.fromEntries(
    Object.entries(source).filter(([name]) => SAFE_LOGGED_IN_ENVIRONMENT.has(name.toUpperCase())),
  );
}

async function createClient({ workingDirectory, authMode, runtimePath, clientFactory }) {
  const clientOptions = {
    workingDirectory: resolve(workingDirectory),
    logLevel: "error",
    env: environmentForAuthMode(authMode),
    useLoggedInUser: authMode === "logged-in",
  };
  if (clientFactory) {
    return clientFactory(clientOptions);
  }
  const { CopilotClient, RuntimeConnection } = await import("@github/copilot-sdk");
  if (runtimePath) {
    clientOptions.connection = RuntimeConnection.forStdio({ path: runtimePath });
  }
  return new CopilotClient(clientOptions);
}

function collectRuntimeEvents(session, events) {
  return session.on((event) => {
    switch (event.type) {
      case "skill.invoked":
        events.push({
          type: event.type,
          data: { name: event.data.name, trigger: event.data.trigger ?? "unknown" },
        });
        break;
      case "session.skills_loaded":
        events.push({
          type: event.type,
          data: {
            skills: event.data.skills.map(({ name, enabled }) => ({ name, enabled })),
          },
        });
        break;
      case "subagent.selected":
        events.push({
          type: event.type,
          data: {
            agentName: event.data.agentName,
            tools: event.data.tools,
          },
        });
        break;
      case "permission.requested":
        events.push({
          type: event.type,
          data: { kind: event.data.permissionRequest?.kind ?? "unknown" },
        });
        break;
      default:
        break;
    }
  });
}

function sameValues(left, right) {
  return left.length === right.length
    && [...left].sort().every((value, index) => value === [...right].sort()[index]);
}

async function executeAgentSession({
  client,
  agent,
  task,
  workingDirectory,
  timeoutMs,
  skillDirectories,
}) {
  await resolveAgentSkills(agent, skillDirectories);
  const sdkAgent = toCopilotAgentConfig(agent);
  const events = [];
  const startedAt = Date.now();
  let session;
  try {
    session = await client.createSession({
      clientName: "sdlc-dynamic-agents-poc",
      workingDirectory: resolve(workingDirectory),
      enableConfigDiscovery: false,
      infiniteSessions: { enabled: false },
      streaming: false,
      skillDirectories: skillDirectories.map((directory) => resolve(directory)),
      customAgents: [sdkAgent],
      onPermissionRequest: createPermissionHandler(agent.permissionMode ?? "deny-all", {
        allowedRoot: workingDirectory,
      }),
    });
    collectRuntimeEvents(session, events);

    const selected = await session.rpc.agent.select({ name: sdkAgent.name });
    const current = await session.rpc.agent.getCurrent();
    const runtimeSkills = [...(selected.agent.skills ?? [])];
    if (selected.agent.name !== sdkAgent.name || current.agent?.name !== sdkAgent.name) {
      throw new Error("Copilot did not select configured agent '" + sdkAgent.name + "'.");
    }
    if (!sameValues(runtimeSkills, sdkAgent.skills ?? [])) {
      throw new Error("Copilot selected agent '" + sdkAgent.name + "' with unexpected skills.");
    }
    await session.rpc.skills.ensureLoaded();

    const response = await session.sendAndWait(task.trim(), timeoutMs);
    const content = response?.data?.content;
    if (typeof content !== "string" || content.trim().length === 0) {
      throw new Error("Agent '" + sdkAgent.name + "' completed without an assistant message.");
    }
    const invoked = await session.rpc.skills.getInvoked();
    const invokedSkills = [...new Set(invoked.skills.map(({ name }) => name))];
    const skillEvents = [...new Set(
      events.filter(({ type }) => type === "skill.invoked").map(({ data }) => data.name),
    )];
    const unexpectedTriggers = events.filter(
      ({ type, data }) => type === "skill.invoked"
        && (sdkAgent.skills ?? []).includes(data.name)
        && data.trigger !== "agent-invoked",
    );
    const missingInvocations = (sdkAgent.skills ?? []).filter((skill) => !invokedSkills.includes(skill));
    const missingEvents = (sdkAgent.skills ?? []).filter((skill) => !skillEvents.includes(skill));
    if (missingInvocations.length > 0 || missingEvents.length > 0 || unexpectedTriggers.length > 0) {
      throw new Error(
        "Copilot did not prove skill invocation for agent '" + sdkAgent.name + "': "
        + [...new Set([...missingInvocations, ...missingEvents])].join(", ") + ".",
      );
    }
    const eventBySkill = new Map(
      events.filter(({ type }) => type === "skill.invoked").map(({ data }) => [data.name, data]),
    );
    const invocationEvidence = invoked.skills
      .filter(({ name }) => (sdkAgent.skills ?? []).includes(name))
      .map(({ name, content, invokedAtTurn }) => ({
        name,
        trigger: eventBySkill.get(name)?.trigger ?? "unknown",
        invokedAtTurn,
        contentSha256: createHash("sha256").update(content).digest("hex"),
      }));

    return {
      agent: sdkAgent.name,
      selectedAgent: selected.agent.name,
      skills: [...(sdkAgent.skills ?? [])],
      runtimeSkills,
      invokedSkills,
      skillEvents,
      invocationEvidence,
      content,
      durationMs: Date.now() - startedAt,
      events,
    };
  } finally {
    if (session) {
      await session.disconnect().catch(() => undefined);
    }
  }
}

export async function runAgent({
  agent,
  task,
  workingDirectory = process.cwd(),
  timeoutMs = 120_000,
  authMode = "logged-in",
  skillDirectories = [DEFAULT_SKILLS_DIRECTORY],
  runtimePath,
  clientFactory,
}) {
  validateExecutionOptions(task, timeoutMs);
  const client = await createClient({ workingDirectory, authMode, runtimePath, clientFactory });
  try {
    await client.start();
    return await executeAgentSession({
      client,
      agent,
      task,
      workingDirectory,
      timeoutMs,
      skillDirectories,
    });
  } finally {
    await client.stop().catch(() => undefined);
  }
}

export async function runAgentChain({
  agents,
  task,
  workingDirectory = process.cwd(),
  timeoutMs = 120_000,
  authMode = "logged-in",
  skillDirectories = [DEFAULT_SKILLS_DIRECTORY],
  runtimePath,
  clientFactory,
}) {
  validateExecutionOptions(task, timeoutMs);
  if (!Array.isArray(agents) || agents.length === 0) {
    throw new TypeError("Agent chain requires at least one configured agent.");
  }
  if (agents.length > MAX_CHAIN_LENGTH) {
    throw new RangeError("Agent chain exceeds the " + MAX_CHAIN_LENGTH + "-step limit.");
  }
  const names = agents.map(({ name }) => name);
  if (new Set(names).size !== names.length) {
    throw new TypeError("Agent chain must not contain duplicate agent names.");
  }

  const client = await createClient({ workingDirectory, authMode, runtimePath, clientFactory });
  const steps = [];
  const startedAt = Date.now();
  try {
    await client.start();
    let priorOutput = "";
    for (const [index, agent] of agents.entries()) {
      const prompt = index === 0
        ? "Original objective:\n" + task.trim()
          + "\n\nExecute chain step " + (index + 1) + " of " + agents.length
          + " using your assigned role and skills."
        : "Original objective:\n" + task.trim()
          + "\n\nValidated output from chain step " + index + ":\n" + priorOutput
          + "\n\nExecute chain step " + (index + 1) + " of " + agents.length
          + " using your assigned role and skills. Transform and improve the prior output; do not merely repeat it.";
      const step = await executeAgentSession({
        client,
        agent,
        task: prompt,
        workingDirectory,
        timeoutMs,
        skillDirectories,
      });
      priorOutput = step.content;
      steps.push({ index: index + 1, ...step });
    }
    return {
      durationMs: Date.now() - startedAt,
      steps,
      finalContent: priorOutput,
    };
  } finally {
    await client.stop().catch(() => undefined);
  }
}
