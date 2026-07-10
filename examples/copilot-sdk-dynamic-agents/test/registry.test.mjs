import assert from "node:assert/strict";
import { mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  getAgent,
  listAgents,
  removeAgents,
  upsertAgent,
  upsertAgentWithStatus,
} from "../src/registry.mjs";

async function temporaryRegistry() {
  const directory = await mkdtemp(join(tmpdir(), "dynamic-agent-registry-"));
  const registryPath = join(directory, "registry.json");
  await writeFile(registryPath, '{"version":1,"agents":[]}\n', "utf8");
  return registryPath;
}

test("upserts, sorts, and retrieves dynamic agents", async () => {
  const registryPath = await temporaryRegistry();
  await upsertAgent({ name: "z-agent", prompt: "Z" }, registryPath);
  await upsertAgent({ name: "a-agent", prompt: "A" }, registryPath);
  await upsertAgent({ name: "z-agent", prompt: "Updated" }, registryPath);

  assert.deepEqual((await listAgents(registryPath)).map(({ name }) => name), ["a-agent", "z-agent"]);
  assert.equal((await getAgent("z-agent", registryPath)).prompt, "Updated");
  assert.equal(JSON.parse(await readFile(registryPath, "utf8")).agents.length, 2);
});

test("reports unknown agents", async () => {
  const registryPath = await temporaryRegistry();
  await assert.rejects(() => getAgent("missing", registryPath), /Unknown dynamic agent/);
});

test("serializes concurrent mutations and reports create/update/remove actions", async () => {
  const registryPath = await temporaryRegistry();
  const created = await Promise.all(
    Array.from({ length: 12 }, (_, index) =>
      upsertAgentWithStatus({
        name: "agent-" + String(index).padStart(2, "0"),
        prompt: "Agent " + index,
      }, registryPath)),
  );
  assert.equal(created.every(({ action }) => action === "created"), true);
  assert.equal((await listAgents(registryPath)).length, 12);

  const updated = await upsertAgentWithStatus({ name: "agent-00", prompt: "Updated" }, registryPath);
  assert.equal(updated.action, "updated");
  assert.deepEqual(await removeAgents(["agent-00", "agent-01"], registryPath), ["agent-00", "agent-01"]);
  assert.equal((await listAgents(registryPath)).length, 10);
});
