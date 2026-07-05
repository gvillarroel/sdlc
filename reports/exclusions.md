# Exclusions

Date: 2026-07-05

## Purpose

This appendix documents items from the shared discussion that were not included in the permissive open-source evaluation set.

The generated license audit is `results/license_audit.csv`.

## Excluded Items

| Item | Exclusion reason | Impact |
|---|---|---|
| Claude Agent SDK | The shared discussion framed it as an official Anthropic/Claude-centric SDK rather than a permissive OSS candidate for this filter. | Not scored, not simulated, and not included in pilot recommendations. |
| Codex app | The shared discussion framed it as a closed/commercial desktop application, not the open-source Codex CLI. | Not scored. Codex CLI remains included because it is Apache-2.0. |

## Boundary Cases

| Item | Treatment |
|---|---|
| Codex CLI | Included as Apache-2.0 open source, with provider-dependence noted as a practical risk. |
| OpenHands SDK and Agent Canvas | Included as separate MIT repositories because their SDK/control-plane roles differ. |
| OpenCode | Included under the current canonical `anomalyco/opencode` repository; the older archived repo is not used as the canonical source. |
| Omnigent | Included because it is Apache-2.0, but evidence-gap analysis treats it as second-phase due to alpha maturity. |

## Rule For Future Additions

A new candidate should enter the dataset only if:

1. Its canonical repository is clear.
2. The license is MIT or Apache-2.0 at the project level.
3. Source evidence is sufficient to score every criterion.
4. It is meaningfully related to coding-agent orchestration, coding workflows, research harnesses, or agent control planes.

If a candidate fails the license rule, it can be mentioned narratively but should not enter `data/alternatives.json` or simulation outputs.
