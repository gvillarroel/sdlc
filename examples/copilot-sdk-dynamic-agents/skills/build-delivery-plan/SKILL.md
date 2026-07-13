---
name: build-delivery-plan
description: Convert reviewed requirements and risks into an ordered implementation and validation plan.
allowed-tools: []
user-invocable: false
---

Start the response with the exact line `SKILL_PLAN_OK`.

Return an execution plan that:

1. Orders dependent work before downstream work.
2. Names the artifact or command produced by every step.
3. Includes a validation immediately after each meaningful implementation stage.
4. Ends with an end-to-end acceptance test mapped to the original objective.

Keep the plan concrete enough that another coding agent can execute it without clarification.
