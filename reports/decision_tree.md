# Decision Tree

Date: 2026-07-05

Use this when you need a fast shortlist without reading the full scoring model first.

## Guided Selection

1. If the first priority is a quick local coding assistant, pilot **Cline**, **OpenCode**, and **Aider**.
2. If the first priority is secure autonomous PR execution, pilot **Codex CLI**, **OpenHands SDK**, and **Open SWE**.
3. If you are building a custom Python orchestration layer, pilot **OpenHands SDK** and **Deep Agents**.
4. If the implementation must be TypeScript-first, pilot **Flue**, with **Cline** or **OpenCode** as product/CLI comparators.
5. If the goal is reproducible research or harness ablation, pilot **mini-SWE-agent**, **SWE-agent**, and **Deep Agents**.
6. If the goal is a multi-team control plane or async internal coding-agent platform, pilot **OpenHands Agent Canvas**, **Open SWE**, and track **Omnigent**.
7. If none of the above dominates, use the robust default shortlist: **OpenHands SDK**, **Cline**, and **Deep Agents**.

## Guardrails

- Do not pick an alpha project as the primary production base unless the pilot proves the risk is acceptable.
- Do not pick a provider-centered option if provider neutrality is a hard requirement.
- Do not pick a control plane before a CLI/SDK pilot proves task quality.
- Do not pick a research scaffold as an enterprise platform.

The machine-readable version is `data/decision_tree.json`.
