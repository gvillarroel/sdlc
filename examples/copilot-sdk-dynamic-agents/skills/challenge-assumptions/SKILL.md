---
name: challenge-assumptions
description: Challenge an earlier analysis and prioritize concrete failure modes and mitigations.
allowed-tools: []
user-invocable: false
---

Start the response with the exact line `SKILL_RISK_OK`.

Review the prior agent's output in order:

1. Preserve requirements that are supported by the original objective.
2. Identify hidden assumptions, ambiguous evidence, unsafe escalation, and sequencing failures.
3. Rank each risk as high, medium, or low.
4. Pair every high or medium risk with a concrete mitigation and validation check.

Do not replace the objective with a smaller scope.
