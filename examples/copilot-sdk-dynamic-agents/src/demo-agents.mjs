export const DEMO_SKILL_AGENTS = Object.freeze([
  Object.freeze({
    name: "requirements-specialist",
    displayName: "Requirements Specialist",
    description: "Extracts explicit requirements and acceptance criteria before downstream review.",
    prompt: "Analyze the objective using your assigned requirements skill. Be precise, preserve scope, and hand a structured result to the next agent.",
    tools: [],
    skills: ["extract-requirements"],
    infer: false,
    permissionMode: "deny-all",
  }),
  Object.freeze({
    name: "risk-challenger",
    displayName: "Risk Challenger",
    description: "Challenges assumptions and identifies failure modes in the prior requirements analysis.",
    prompt: "Critique the prior result using your assigned risk skill. Keep valid requirements, expose gaps, and hand prioritized mitigations to the next agent.",
    tools: [],
    skills: ["challenge-assumptions"],
    infer: false,
    permissionMode: "deny-all",
  }),
  Object.freeze({
    name: "delivery-planner",
    displayName: "Delivery Planner",
    description: "Converts reviewed requirements and risks into an executable, verifiable delivery plan.",
    prompt: "Use your assigned delivery-planning skill to turn the prior result into an ordered implementation and validation plan.",
    tools: [],
    skills: ["build-delivery-plan"],
    infer: false,
    permissionMode: "deny-all",
  }),
]);

export const DEMO_SKILL_AGENT_NAMES = Object.freeze(DEMO_SKILL_AGENTS.map(({ name }) => name));
