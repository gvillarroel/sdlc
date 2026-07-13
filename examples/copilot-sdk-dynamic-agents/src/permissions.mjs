import { realpath } from "node:fs/promises";
import { isAbsolute, relative, resolve } from "node:path";

function requestsSandboxBypass(request) {
  return request?.requestSandboxBypass === true;
}

async function resolvesInside(path, allowedRoot) {
  if (typeof path !== "string" || path.trim().length === 0 || !allowedRoot) {
    return false;
  }
  try {
    const [canonicalRoot, canonicalPath] = await Promise.all([
      realpath(resolve(allowedRoot)),
      realpath(resolve(allowedRoot, path)),
    ]);
    const relation = relative(canonicalRoot, canonicalPath);
    return relation === "" || (!relation.startsWith("..") && !isAbsolute(relation));
  } catch {
    return false;
  }
}

export async function isReadOnlyPermissionRequest(request, allowedRoot) {
  if (!request || typeof request !== "object" || requestsSandboxBypass(request)) {
    return false;
  }
  // Shell, URL, MCP, memory, custom-tool, hook, and write requests are always
  // denied. Read-only approves only canonical filesystem reads in the workspace.
  return request.kind === "read" && resolvesInside(request.path, allowedRoot);
}

export function createPermissionHandler(mode = "deny-all", { allowedRoot } = {}) {
  if (!new Set(["deny-all", "read-only"]).has(mode)) {
    throw new TypeError("Unsupported permission mode '" + mode + "'.");
  }
  if (mode === "read-only" && !allowedRoot) {
    throw new TypeError("read-only permission mode requires an allowedRoot.");
  }

  return async (request) => {
    if (mode === "read-only" && await isReadOnlyPermissionRequest(request, allowedRoot)) {
      return { kind: "approve-once" };
    }
    return {
      kind: "reject",
      feedback: "The dynamic-agent POC denied '" + (request?.kind ?? "unknown")
        + "' under permission mode '" + mode + "'.",
    };
  };
}
