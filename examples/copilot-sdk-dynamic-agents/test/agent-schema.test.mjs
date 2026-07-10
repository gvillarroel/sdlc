import assert from "node:assert/strict";
import test from "node:test";

import {
  normalizeAgent,
  toCopilotAgentConfig,
  validateAgent,
  validateRegistry,
} from "../src/agent-schema.mjs";

const minimal = {
  name: "proof-agent",
  description: "A proof agent",
  prompt: "Return a proof marker.",
};

test("normalizes safe defaults and strips POC-only fields from SDK config", () => {
  const normalized = normalizeAgent(minimal);
  assert.deepEqual(normalized.tools, []);
  assert.deepEqual(normalized.skills, []);
  assert.equal(normalized.infer, false);
  assert.equal(normalized.permissionMode, "deny-all");

  assert.deepEqual(toCopilotAgentConfig(normalized), {
    name: "proof-agent",
    description: "A proof agent",
    prompt: "Return a proof marker.",
    tools: [],
    infer: false,
  });
});

test("rejects traversal-like names, unknown fields, and invalid permissions", () => {
  assert.throws(() => validateAgent({ ...minimal, name: "../escape" }), /Agent name/);
  assert.throws(() => validateAgent({ ...minimal, surprise: true }), /Unknown agent field/);
  assert.throws(() => validateAgent({ ...minimal, permissionMode: "approve-all" }), /permissionMode/);
  assert.throws(() => validateAgent({ ...minimal, skills: ["one", "one"] }), /skills.*duplicates/);
  assert.throws(() => validateAgent({ ...minimal, skills: ["../escape"] }), /cannot contain paths/);
  assert.throws(
    () => validateAgent({ ...minimal, permissionMode: "read-only", tools: ["bash"] }),
    /unsafe tool/,
  );
  assert.throws(
    () => validateAgent({ ...minimal, permissionMode: "deny-all", tools: ["view"] }),
    /deny-all.*tools/,
  );
});

test("rejects duplicate registry names", () => {
  assert.throws(
    () => validateRegistry({ version: 1, agents: [minimal, minimal] }),
    /duplicate name/,
  );
});
