import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { joinSession } from "@github/copilot-sdk/extension";

import { startDynamicAgentExtension } from "../../../examples/copilot-sdk-dynamic-agents/src/extension-runtime.mjs";

const extensionDirectory = dirname(fileURLToPath(import.meta.url));
const repositoryRoot = resolve(extensionDirectory, "../../..");
const registryPath = resolve(repositoryRoot, "examples/copilot-sdk-dynamic-agents/agents/registry.json");

await startDynamicAgentExtension({ joinSession, registryPath, repositoryRoot });
