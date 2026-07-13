const AGENT_NAME_PATTERN = /^[a-z][a-z0-9-]{0,63}$/;
const SKILL_NAME_PATTERN = /^[a-z][a-z0-9-]{0,63}$/;
const MAX_PROMPT_LENGTH = 30_000;
const SAFE_READ_ONLY_TOOLS = new Set(["glob", "grep", "read", "search", "view"]);
const ALLOWED_KEYS = new Set([
  "name",
  "displayName",
  "description",
  "prompt",
  "tools",
  "infer",
  "model",
  "skills",
  "permissionMode",
]);
const PERMISSION_MODES = new Set(["deny-all", "read-only"]);

function assertString(value, field, { required = false, maxLength = 1024 } = {}) {
  if (value === undefined && !required) {
    return;
  }
  if (typeof value !== "string" || (required && value.trim().length === 0)) {
    throw new TypeError(`Agent field '${field}' must be a${required ? " non-empty" : ""} string.`);
  }
  if (value.length > maxLength) {
    throw new RangeError(`Agent field '${field}' exceeds ${maxLength} characters.`);
  }
}

export function validateAgent(candidate) {
  if (!candidate || typeof candidate !== "object" || Array.isArray(candidate)) {
    throw new TypeError("Agent configuration must be a JSON object.");
  }

  const unknownKeys = Object.keys(candidate).filter((key) => !ALLOWED_KEYS.has(key));
  if (unknownKeys.length > 0) {
    throw new TypeError(`Unknown agent field(s): ${unknownKeys.join(", ")}.`);
  }

  assertString(candidate.name, "name", { required: true, maxLength: 64 });
  if (!AGENT_NAME_PATTERN.test(candidate.name)) {
    throw new TypeError("Agent name must start with a lowercase letter and contain only lowercase letters, numbers, or hyphens.");
  }

  assertString(candidate.displayName, "displayName", { maxLength: 128 });
  assertString(candidate.description, "description", { maxLength: 1024 });
  assertString(candidate.prompt, "prompt", { required: true, maxLength: MAX_PROMPT_LENGTH });
  assertString(candidate.model, "model", { maxLength: 128 });

  if (candidate.tools !== undefined) {
    if (!Array.isArray(candidate.tools) || candidate.tools.some((tool) => typeof tool !== "string" || tool.trim().length === 0)) {
      throw new TypeError("Agent field 'tools' must be an array of non-empty strings.");
    }
    if (new Set(candidate.tools).size !== candidate.tools.length) {
      throw new TypeError("Agent field 'tools' must not contain duplicates.");
    }
  }

  if (candidate.skills !== undefined) {
    if (!Array.isArray(candidate.skills) || candidate.skills.some((skill) => typeof skill !== "string" || skill.trim().length === 0)) {
      throw new TypeError("Agent field 'skills' must be an array of non-empty strings.");
    }
    if (new Set(candidate.skills).size !== candidate.skills.length) {
      throw new TypeError("Agent field 'skills' must not contain duplicates.");
    }
    if (candidate.skills.some((skill) => !SKILL_NAME_PATTERN.test(skill))) {
      throw new TypeError("Agent skill names must use lowercase kebab-case and cannot contain paths.");
    }
  }

  if (candidate.infer !== undefined && typeof candidate.infer !== "boolean") {
    throw new TypeError("Agent field 'infer' must be a boolean.");
  }

  if (candidate.permissionMode !== undefined && !PERMISSION_MODES.has(candidate.permissionMode)) {
    throw new TypeError("Agent field 'permissionMode' must be 'deny-all' or 'read-only'.");
  }

  const permissionMode = candidate.permissionMode ?? "deny-all";
  const tools = candidate.tools ?? [];
  if (permissionMode === "deny-all" && tools.length > 0) {
    throw new TypeError("Agents in 'deny-all' mode must use tools: [].");
  }
  const unsafeTools = tools.filter((tool) => !SAFE_READ_ONLY_TOOLS.has(tool));
  if (permissionMode === "read-only" && unsafeTools.length > 0) {
    throw new TypeError(`Read-only dynamic agents cannot use unsafe tool(s): ${unsafeTools.join(", ")}.`);
  }

  return candidate;
}

export function normalizeAgent(candidate) {
  validateAgent(candidate);
  return {
    name: candidate.name,
    ...(candidate.displayName ? { displayName: candidate.displayName.trim() } : {}),
    ...(candidate.description ? { description: candidate.description.trim() } : {}),
    prompt: candidate.prompt.trim(),
    tools: candidate.tools ? [...candidate.tools] : [],
    infer: candidate.infer ?? false,
    ...(candidate.model ? { model: candidate.model.trim() } : {}),
    skills: candidate.skills ? [...candidate.skills] : [],
    permissionMode: candidate.permissionMode ?? "deny-all",
  };
}

export function toCopilotAgentConfig(agent) {
  const normalized = normalizeAgent(agent);
  return {
    name: normalized.name,
    ...(normalized.displayName ? { displayName: normalized.displayName } : {}),
    ...(normalized.description ? { description: normalized.description } : {}),
    prompt: normalized.prompt,
    tools: normalized.tools,
    infer: normalized.infer,
    ...(normalized.model ? { model: normalized.model } : {}),
    ...(normalized.skills.length > 0 ? { skills: normalized.skills } : {}),
  };
}

export function validateRegistry(candidate) {
  if (!candidate || typeof candidate !== "object" || Array.isArray(candidate)) {
    throw new TypeError("Agent registry must be a JSON object.");
  }
  if (candidate.version !== 1) {
    throw new TypeError("Agent registry version must be 1.");
  }
  if (!Array.isArray(candidate.agents)) {
    throw new TypeError("Agent registry field 'agents' must be an array.");
  }

  const agents = candidate.agents.map(normalizeAgent);
  const names = agents.map((agent) => agent.name);
  const duplicates = names.filter((name, index) => names.indexOf(name) !== index);
  if (duplicates.length > 0) {
    throw new TypeError(`Agent registry contains duplicate name(s): ${[...new Set(duplicates)].join(", ")}.`);
  }

  return { version: 1, agents };
}

export { SAFE_READ_ONLY_TOOLS };
