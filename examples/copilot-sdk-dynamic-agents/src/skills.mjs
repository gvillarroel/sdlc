import { readFile, realpath } from "node:fs/promises";
import { isAbsolute, relative, resolve } from "node:path";

function inside(root, candidate) {
  const relation = relative(root, candidate);
  return relation === "" || (!relation.startsWith("..") && !isAbsolute(relation));
}

function declaredSkillName(content) {
  const frontmatter = content.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  if (!frontmatter) {
    return undefined;
  }
  return frontmatter[1].match(/^name:\s*([a-z][a-z0-9-]{0,63})\s*$/m)?.[1];
}

export async function resolveAgentSkills(agent, skillDirectories) {
  if (!Array.isArray(skillDirectories) || skillDirectories.length === 0) {
    if ((agent.skills ?? []).length > 0) {
      throw new Error("At least one skill directory is required for skill-configured agents.");
    }
    return [];
  }

  const roots = await Promise.all(skillDirectories.map((directory) => realpath(resolve(directory))));
  const resolvedSkills = [];
  for (const skill of agent.skills ?? []) {
    let match;
    for (const root of roots) {
      const candidate = resolve(root, skill, "SKILL.md");
      if (!inside(root, candidate)) {
        continue;
      }
      try {
        const canonicalPath = await realpath(candidate);
        if (!inside(root, canonicalPath)) {
          continue;
        }
        const content = await readFile(canonicalPath, "utf8");
        if (declaredSkillName(content) !== skill) {
          throw new Error("Skill '" + skill + "' must declare matching frontmatter name.");
        }
        match = { name: skill, path: canonicalPath };
        break;
      } catch (error) {
        if (error?.code !== "ENOENT") {
          throw error;
        }
      }
    }
    if (!match) {
      throw new Error("Configured skill '" + skill + "' was not found in the allowed skill directories.");
    }
    resolvedSkills.push(match);
  }
  return resolvedSkills;
}
