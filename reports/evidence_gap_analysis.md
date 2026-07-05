# Evidence Gap Analysis

Date: 2026-07-05

## Objective

This appendix identifies which alternatives need more evidence before they should influence an adoption decision. It complements the license audit and source URL check: a URL can be reachable and a license can be permissive while the project is still too young, under-documented, or low-confidence for production planning.

The generated file is `results/evidence_gap_analysis.csv`, produced by:

```powershell
python scripts/analyze_evidence_gaps.py
```

## Method

The script assigns an evidence risk score using:

- Source confidence penalty
- Maturity penalty
- Missing latest release
- Low repository traction
- Single evidence URL
- Stale or missing last-push date
- Very new repository age at the 2026-07-05 retrieval date

The score is not a quality score. It is a review-priority signal: higher means the candidate needs more verification before it should be treated as a serious foundation.

## Findings

| Evidence risk | Candidates | Interpretation |
|---|---|---|
| High | Anchor, OmniAgent, Omni Agent | Do not choose as primary foundations without fresh evidence and a successful spike. |
| Medium | Omnigent | Worth tracking as a second-phase control-plane idea, but alpha status and very new repo age require a spike. |
| Low with specific caveat | Open SWE, Flue, Sandcastle, OpenHands Agent Canvas | Evidence is sufficient for screening, but verify release/package story, canonical docs, or new-repo maturity before pilot setup. |
| Low | Codex CLI, Cline, OpenCode, OpenHands SDK, Deep Agents, Aider, goose, SWE-agent, mini-SWE-agent | Evidence is sufficient for shortlist-level screening. |

## High And Medium Evidence Gaps

| Candidate | Risk band | Score | Main gaps | Adoption implication |
|---|---|---:|---|---|
| Omni Agent | High | 5.6 | Low source confidence, alpha maturity, missing release, low traction, single evidence URL, very new repository | Reference-only unless fresh evidence and a spike change the picture. |
| Anchor | High | 5.1 | Low source confidence, alpha maturity, low traction, single evidence URL, very new repository | Too narrow and low-evidence for a primary platform decision. |
| OmniAgent | High | 5.1 | Low source confidence, alpha maturity, low traction, single evidence URL, very new repository | Treat as experimental reference material. |
| Omnigent | Medium | 3.8 | Alpha maturity, single evidence URL, very new repository | Interesting meta-harness concept, but second-phase only. |

## Impact On The Recommendation

The evidence-gap analysis supports the report's main recommendation:

1. Prioritize OpenHands SDK, Deep Agents, Cline, Codex CLI, SWE-agent, mini-SWE-agent, and Flue for relevant pilot scenarios.
2. Keep Omnigent as a tracked second-phase candidate, not a first production foundation.
3. Keep Anchor, OmniAgent, and Omni Agent out of the primary pilot unless the goal is exploratory research.
4. Refresh this analysis before adoption if more than 30 days have passed or if a candidate has a major release.
