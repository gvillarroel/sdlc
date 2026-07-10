---
name: extract-requirements
description: Extract explicit requirements, constraints, and acceptance evidence from a task.
allowed-tools: []
user-invocable: false
---

Start the response with the exact line `SKILL_REQUIREMENTS_OK`.

Produce these sections:

1. Objective — one sentence that preserves the user's full scope.
2. Requirements — numbered, independently verifiable statements.
3. Constraints — explicit safety, platform, compatibility, and sequencing constraints.
4. Acceptance evidence — the concrete command output or runtime behavior that would prove each requirement.

Do not design the implementation yet and do not invent missing business requirements.
