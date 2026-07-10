import { createHash } from "node:crypto";
import { mkdir, rename, writeFile } from "node:fs/promises";
import { dirname } from "node:path";

const EXPECTED_SKILL_MARKERS = Object.freeze([
  Object.freeze({
    agent: "requirements-specialist",
    skill: "extract-requirements",
    marker: "SKILL_REQUIREMENTS_OK",
  }),
  Object.freeze({
    agent: "risk-challenger",
    skill: "challenge-assumptions",
    marker: "SKILL_RISK_OK",
  }),
  Object.freeze({
    agent: "delivery-planner",
    skill: "build-delivery-plan",
    marker: "SKILL_PLAN_OK",
  }),
]);

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

export function createSkillDemoReport({ runId, generated, result, source }) {
  const executionOrder = result.steps.map(({ agent }) => agent);
  const expectedOrder = EXPECTED_SKILL_MARKERS.map(({ agent }) => agent);
  const orderMatches = executionOrder.length === expectedOrder.length
    && executionOrder.every((agent, index) => agent === expectedOrder[index]);

  const runtimeChecks = EXPECTED_SKILL_MARKERS.map((expected) => {
    const step = result.steps.find(({ agent }) => agent === expected.agent);
    const invocation = step?.invocationEvidence.find(({ name }) => name === expected.skill);
    return {
      ...expected,
      selectedAgentMatches: step?.selectedAgent === expected.agent,
      runtimeSkillAssigned: Boolean(step?.runtimeSkills.includes(expected.skill)),
      skillInvoked: Boolean(step?.invokedSkills.includes(expected.skill)),
      skillEventObserved: Boolean(step?.skillEvents.includes(expected.skill)),
      trigger: invocation?.trigger ?? "missing",
      markerFound: Boolean(step?.content.includes(expected.marker)),
    };
  });
  const generationProved = generated.length === EXPECTED_SKILL_MARKERS.length
    && generated.every(({ action }) => action === "created");
  const runtimeProved = runtimeChecks.every((check) =>
    check.selectedAgentMatches
    && check.runtimeSkillAssigned
    && check.skillInvoked
    && check.skillEventObserved
    && check.trigger === "agent-invoked"
    && check.markerFound);
  const passed = generationProved && orderMatches && runtimeProved;

  return {
    schemaVersion: 2,
    generatedAt: new Date().toISOString(),
    runId,
    source,
    status: passed ? "passed" : "failed",
    generationProved,
    generatedAgents: generated.map(({ agent, action }) => ({
      name: agent.name,
      skills: agent.skills,
      action,
    })),
    expectedOrder,
    executionOrder,
    orderMatches,
    runtimeChecks,
    durationMs: result.durationMs,
    steps: result.steps.map((step) => {
      const expected = EXPECTED_SKILL_MARKERS.find(({ agent }) => agent === step.agent);
      return {
        index: step.index,
        agent: step.agent,
        selectedAgent: step.selectedAgent,
        configuredSkills: step.skills,
        runtimeSkills: step.runtimeSkills,
        invokedSkills: step.invokedSkills,
        invocationEvidence: step.invocationEvidence,
        marker: expected?.marker,
        markerFound: expected ? step.content.includes(expected.marker) : false,
        outputLength: step.content.length,
        outputSha256: sha256(step.content),
        durationMs: step.durationMs,
      };
    }),
  };
}

export async function writeSkillDemoReport(report, outputPath) {
  await mkdir(dirname(outputPath), { recursive: true });
  const temporaryPath = outputPath + "." + process.pid + "." + Date.now() + ".tmp";
  await writeFile(temporaryPath, JSON.stringify(report, null, 2) + "\n", "utf8");
  await rename(temporaryPath, outputPath);
  return outputPath;
}

export function compactSkillDemoReport(report, resultReference) {
  return {
    status: report.status,
    runId: report.runId,
    generationProved: report.generationProved,
    generatedAgents: report.generatedAgents,
    executionOrder: report.executionOrder,
    orderMatches: report.orderMatches,
    runtimeChecks: report.runtimeChecks,
    durationMs: report.durationMs,
    resultReference,
  };
}

export { EXPECTED_SKILL_MARKERS };
