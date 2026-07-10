import assert from "node:assert/strict";
import test from "node:test";

import { compactSkillDemoReport, createSkillDemoReport } from "../src/results.mjs";

const definitions = [
  ["requirements-specialist", "extract-requirements", "SKILL_REQUIREMENTS_OK"],
  ["risk-challenger", "challenge-assumptions", "SKILL_RISK_OK"],
  ["delivery-planner", "build-delivery-plan", "SKILL_PLAN_OK"],
];

function passingFixture() {
  const generated = definitions.map(([name, skill]) => ({
    agent: { name, skills: [skill] },
    action: "created",
  }));
  const steps = definitions.map(([agent, skill, marker], index) => ({
    index: index + 1,
    agent,
    selectedAgent: agent,
    skills: [skill],
    runtimeSkills: [skill],
    invokedSkills: [skill],
    skillEvents: [skill],
    invocationEvidence: [{
      name: skill,
      trigger: "agent-invoked",
      invokedAtTurn: 1,
      contentSha256: "a".repeat(64),
    }],
    content: marker + "\nproof",
    durationMs: 1,
  }));
  return { generated, result: { durationMs: 10, steps } };
}

test("requires fresh generation plus selected-agent and runtime skill evidence", () => {
  const fixture = passingFixture();
  const report = createSkillDemoReport({
    runId: "run-1",
    generated: fixture.generated,
    source: "test",
    result: fixture.result,
  });

  assert.equal(report.status, "passed");
  assert.equal(report.generationProved, true);
  assert.equal(report.orderMatches, true);
  assert.equal(report.runtimeChecks.every(({ skillInvoked }) => skillInvoked), true);
  assert.equal("content" in report.steps[0], false);
  assert.equal("sessionId" in report, false);
  assert.equal(report.steps[0].outputSha256.length, 64);

  const compact = compactSkillDemoReport(report, "result.json");
  assert.equal(compact.resultReference, "result.json");
  assert.equal("steps" in compact, false);
});

test("fails when generation, runtime selection, trigger, marker, or order is unproved", () => {
  const fixture = passingFixture();
  fixture.generated[0].action = "updated";
  fixture.result.steps[0].selectedAgent = "wrong-agent";
  fixture.result.steps[1].invocationEvidence[0].trigger = "context-load";
  fixture.result.steps[2].content = "no marker";
  fixture.result.steps.reverse();

  const report = createSkillDemoReport({
    runId: "run-2",
    generated: fixture.generated,
    source: "test",
    result: fixture.result,
  });
  assert.equal(report.status, "failed");
  assert.equal(report.generationProved, false);
  assert.equal(report.orderMatches, false);
});
