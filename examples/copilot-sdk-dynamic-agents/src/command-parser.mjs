export function parseRunArguments(rawArguments) {
  const separator = "::";
  const separatorIndex = rawArguments.indexOf(separator);
  if (separatorIndex < 0) {
    throw new Error("Expected '<agent-name> :: <task>'.");
  }

  const name = rawArguments.slice(0, separatorIndex).trim();
  const task = rawArguments.slice(separatorIndex + separator.length).trim();
  if (!name || !task) {
    throw new Error("Both an agent name and a task are required.");
  }
  return { name, task };
}

export function parseCreateArguments(rawArguments) {
  const value = rawArguments.trim();
  if (!value) {
    throw new Error("Expected an agent configuration as JSON.");
  }
  try {
    return JSON.parse(value);
  } catch (error) {
    throw new SyntaxError(`Invalid agent JSON: ${error.message}`);
  }
}

export function parseChainArguments(rawArguments) {
  const { name: rawNames, task } = parseRunArguments(rawArguments);
  const names = rawNames.split(",").map((name) => name.trim()).filter(Boolean);
  if (names.length === 0) {
    throw new Error("At least one agent name is required.");
  }
  if (new Set(names).size !== names.length) {
    throw new Error("Agent chain must not contain duplicate names.");
  }
  return { names, task };
}
