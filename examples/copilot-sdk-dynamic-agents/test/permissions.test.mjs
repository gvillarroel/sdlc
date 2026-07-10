import assert from "node:assert/strict";
import { mkdtemp, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import { createPermissionHandler, isReadOnlyPermissionRequest } from "../src/permissions.mjs";

async function workspaceFixture() {
  const parent = await mkdtemp(join(tmpdir(), "dynamic-agent-permissions-"));
  const workspace = join(parent, "workspace");
  const { mkdir } = await import("node:fs/promises");
  await mkdir(workspace);
  await writeFile(join(workspace, "README.md"), "proof", "utf8");
  await writeFile(join(parent, "secret.txt"), "secret", "utf8");
  return { parent, workspace };
}

test("approves only canonical reads inside the configured workspace", async () => {
  const { workspace } = await workspaceFixture();
  assert.equal(
    await isReadOnlyPermissionRequest({ kind: "read", path: "README.md" }, workspace),
    true,
  );
  assert.equal(
    await isReadOnlyPermissionRequest({ kind: "read", path: "../secret.txt" }, workspace),
    false,
  );
});

test("rejects shell, writes, MCP, and sandbox bypasses", async () => {
  const { workspace } = await workspaceFixture();
  assert.equal(await isReadOnlyPermissionRequest({ kind: "write", fileName: "x" }, workspace), false);
  assert.equal(await isReadOnlyPermissionRequest({
    kind: "shell",
    hasWriteFileRedirection: false,
    commands: [{ identifier: "git status", readOnly: true }],
    possibleUrls: [],
  }, workspace), false);
  assert.equal(await isReadOnlyPermissionRequest({ kind: "mcp", readOnly: true }, workspace), false);
  assert.equal(await isReadOnlyPermissionRequest({
    kind: "read",
    path: "README.md",
    requestSandboxBypass: true,
  }, workspace), false);
});

test("permission handler never escalates beyond its declared mode", async () => {
  const { workspace } = await workspaceFixture();
  const readOnly = createPermissionHandler("read-only", { allowedRoot: workspace });
  assert.deepEqual(await readOnly({ kind: "read", path: "README.md" }), { kind: "approve-once" });
  assert.equal((await readOnly({ kind: "shell", commands: [] })).kind, "reject");

  const denyAll = createPermissionHandler("deny-all");
  assert.equal((await denyAll({ kind: "read", path: "README.md" })).kind, "reject");
  assert.throws(() => createPermissionHandler("read-only"), /allowedRoot/);
});
