import assert from "node:assert/strict";
import test from "node:test";

import { parseChainArguments, parseCreateArguments, parseRunArguments } from "../src/command-parser.mjs";

test("parses a slash-command agent run without losing task separators", () => {
  assert.deepEqual(
    parseRunArguments(" repository-analyst :: compare A :: B "),
    { name: "repository-analyst", task: "compare A :: B" },
  );
});

test("rejects incomplete run arguments", () => {
  assert.throws(() => parseRunArguments("repository-analyst"), /Expected/);
  assert.throws(() => parseRunArguments(" :: task"), /Both/);
});

test("parses and diagnoses inline agent JSON", () => {
  assert.equal(parseCreateArguments('{"name":"proof"}').name, "proof");
  assert.throws(() => parseCreateArguments("{"), /Invalid agent JSON/);
});

test("parses an ordered agent chain and rejects duplicate steps", () => {
  assert.deepEqual(
    parseChainArguments("requirements-specialist, risk-challenger, delivery-planner :: ship safely"),
    {
      names: ["requirements-specialist", "risk-challenger", "delivery-planner"],
      task: "ship safely",
    },
  );
  assert.throws(() => parseChainArguments("same,same :: task"), /duplicate/);
});
