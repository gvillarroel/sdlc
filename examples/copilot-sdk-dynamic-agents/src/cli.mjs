#!/usr/bin/env node
import { dirname, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

import { DEMO_SKILL_AGENTS, DEMO_SKILL_AGENT_NAMES } from "./demo-agents.mjs";
import { runAgent, runAgentChain } from "./runner.mjs";
import { getAgent, listAgents, upsertAgent, DEFAULT_REGISTRY_PATH } from "./registry.mjs";

const REPOSITORY_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../..");

function usage() {
  return `Usage:
  npm run agent -- list
  npm run agent -- validate
  npm run agent -- upsert '<agent-json>'
  npm run agent -- run <agent-name> --task <task> [--auth logged-in|inherited] [--timeout-ms 120000]
  npm run agent -- chain <agent-1,agent-2> --task <task> [--auth logged-in|inherited] [--timeout-ms 120000]
  npm run agent -- demo --task <task> [--auth logged-in|inherited] [--timeout-ms 120000]
`;
}

function optionValue(arguments_, option, fallback) {
  const index = arguments_.indexOf(option);
  return index >= 0 ? arguments_[index + 1] : fallback;
}

function taskFromArguments(arguments_) {
  const taskIndex = arguments_.indexOf("--task");
  if (taskIndex < 0 || !arguments_[taskIndex + 1]) {
    throw new Error("A non-empty --task value is required.");
  }
  const taskEndOptions = ["--auth", "--timeout-ms"]
    .map((option) => arguments_.indexOf(option))
    .filter((index) => index > taskIndex)
    .sort((left, right) => left - right);
  const taskEnd = taskEndOptions[0] ?? arguments_.length;
  return arguments_.slice(taskIndex + 1, taskEnd).join(" ");
}

async function executeConfiguredChain(agents, taskArguments) {
  const result = await runAgentChain({
    agents,
    task: taskFromArguments(taskArguments),
    workingDirectory: REPOSITORY_ROOT,
    timeoutMs: Number(optionValue(taskArguments, "--timeout-ms", "120000")),
    authMode: optionValue(taskArguments, "--auth", "logged-in"),
  });
  for (const step of result.steps) {
    console.log(`\n=== STEP ${step.index}: ${step.agent} [${step.skills.join(", ") || "no skills"}] ===`);
    console.log(step.content);
  }
  return result;
}

async function executeChain(names, taskArguments) {
  return executeConfiguredChain(
    await Promise.all(names.map((name) => getAgent(name))),
    taskArguments,
  );
}

export async function main(arguments_ = process.argv.slice(2)) {
  const [command, ...rest] = arguments_;
  switch (command) {
    case "list": {
      for (const agent of await listAgents()) {
        console.log(`${agent.name}\t${agent.description ?? ""}\t${agent.permissionMode}`);
      }
      return;
    }
    case "validate": {
      const agents = await listAgents();
      console.log(`Valid registry: ${agents.length} dynamic agent(s) in ${DEFAULT_REGISTRY_PATH}`);
      return;
    }
    case "upsert": {
      if (!rest[0]) {
        throw new Error("The upsert command requires an inline JSON object.");
      }
      const agent = await upsertAgent(JSON.parse(rest.join(" ")));
      console.log(`Saved dynamic agent '${agent.name}'.`);
      return;
    }
    case "run": {
      const name = rest[0];
      if (!name) {
        throw new Error("The run command requires '<agent-name> --task <task>'.");
      }
      const timeoutMs = Number(optionValue(rest, "--timeout-ms", "120000"));
      const result = await runAgent({
        agent: await getAgent(name),
        task: taskFromArguments(rest),
        workingDirectory: REPOSITORY_ROOT,
        timeoutMs,
        authMode: optionValue(rest, "--auth", "logged-in"),
      });
      console.log(result.content);
      return;
    }
    case "chain": {
      const names = (rest[0] ?? "").split(",").map((name) => name.trim()).filter(Boolean);
      if (names.length === 0) {
        throw new Error("The chain command requires a comma-separated agent list.");
      }
      await executeChain(names, rest.slice(1));
      return;
    }
    case "demo": {
      console.log(`Prepared ephemeral dynamic skill agents: ${DEMO_SKILL_AGENT_NAMES.join(" -> ")}`);
      await executeConfiguredChain(DEMO_SKILL_AGENTS, rest);
      return;
    }
    case "help":
    case "--help":
    case "-h":
    case undefined:
      console.log(usage());
      return;
    default:
      throw new Error(`Unknown command '${command}'.\n${usage()}`);
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  main().catch((error) => {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  });
}
