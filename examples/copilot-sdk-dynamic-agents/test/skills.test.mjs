import assert from "node:assert/strict";
import { mkdir, mkdtemp, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import { resolveAgentSkills } from "../src/skills.mjs";

async function skillDirectory(name, declaredName = name) {
  const root = await mkdtemp(join(tmpdir(), "dynamic-agent-skills-"));
  const directory = join(root, name);
  await mkdir(directory);
  await writeFile(
    join(directory, "SKILL.md"),
    "---\nname: " + declaredName + "\ndescription: Test skill\n---\n\nInstructions.\n",
    "utf8",
  );
  return root;
}

test("resolves a declared skill inside an allowed directory", async () => {
  const root = await skillDirectory("proof-skill");
  const resolved = await resolveAgentSkills({ skills: ["proof-skill"] }, [root]);
  assert.equal(resolved[0].name, "proof-skill");
  assert.match(resolved[0].path, /proof-skill[\\/]SKILL\.md$/);
});

test("rejects missing skills and mismatched frontmatter names", async () => {
  const root = await skillDirectory("proof-skill", "wrong-name");
  await assert.rejects(
    () => resolveAgentSkills({ skills: ["proof-skill"] }, [root]),
    /matching frontmatter name/,
  );
  await assert.rejects(
    () => resolveAgentSkills({ skills: ["missing-skill"] }, [root]),
    /not found/,
  );
});
