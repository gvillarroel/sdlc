import { mkdir, readFile, rename, writeFile } from "node:fs/promises";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

import { normalizeAgent, validateRegistry } from "./agent-schema.mjs";

export const DEFAULT_REGISTRY_PATH = fileURLToPath(new URL("../agents/registry.json", import.meta.url));

let mutationQueue = Promise.resolve();

function serializeMutation(operation) {
  const pending = mutationQueue.then(operation, operation);
  mutationQueue = pending.then(() => undefined, () => undefined);
  return pending;
}

async function writeRegistry(registry, registryPath) {
  await mkdir(dirname(registryPath), { recursive: true });
  const temporaryPath = registryPath + "." + process.pid + "." + Date.now() + ".tmp";
  await writeFile(temporaryPath, JSON.stringify(registry, null, 2) + "\n", "utf8");
  await rename(temporaryPath, registryPath);
}

export async function loadRegistry(registryPath = DEFAULT_REGISTRY_PATH) {
  let parsed;
  try {
    parsed = JSON.parse(await readFile(registryPath, "utf8"));
  } catch (error) {
    if (error instanceof SyntaxError) {
      throw new SyntaxError("Invalid JSON in agent registry '" + registryPath + "': " + error.message);
    }
    throw error;
  }
  return validateRegistry(parsed);
}

export async function listAgents(registryPath = DEFAULT_REGISTRY_PATH) {
  return (await loadRegistry(registryPath)).agents;
}

export async function getAgent(name, registryPath = DEFAULT_REGISTRY_PATH) {
  const agent = (await loadRegistry(registryPath)).agents.find((candidate) => candidate.name === name);
  if (!agent) {
    throw new Error("Unknown dynamic agent '" + name + "'.");
  }
  return agent;
}

export async function upsertAgentWithStatus(candidate, registryPath = DEFAULT_REGISTRY_PATH) {
  const agent = normalizeAgent(candidate);
  return serializeMutation(async () => {
    const registry = await loadRegistry(registryPath);
    const existingIndex = registry.agents.findIndex((current) => current.name === agent.name);
    const action = existingIndex >= 0 ? "updated" : "created";
    if (existingIndex >= 0) {
      registry.agents[existingIndex] = agent;
    } else {
      registry.agents.push(agent);
    }
    registry.agents.sort((left, right) => left.name.localeCompare(right.name));
    await writeRegistry(registry, registryPath);
    return { agent, action };
  });
}

export async function upsertAgent(candidate, registryPath = DEFAULT_REGISTRY_PATH) {
  return (await upsertAgentWithStatus(candidate, registryPath)).agent;
}

export async function removeAgents(names, registryPath = DEFAULT_REGISTRY_PATH) {
  const requested = new Set(names);
  return serializeMutation(async () => {
    const registry = await loadRegistry(registryPath);
    const removed = registry.agents
      .filter(({ name }) => requested.has(name))
      .map(({ name }) => name);
    registry.agents = registry.agents.filter(({ name }) => !requested.has(name));
    await writeRegistry(registry, registryPath);
    return removed;
  });
}
