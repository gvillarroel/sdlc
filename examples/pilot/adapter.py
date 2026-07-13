"""Minimal adapter contract for running comparable pilot tasks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol


TaskStatus = Literal["pass", "partial", "fail", "blocked"]


@dataclass(frozen=True)
class PilotTask:
    task_id: str
    repo_path: Path
    instruction: str
    test_command: str
    timeout_seconds: int = 1800


@dataclass(frozen=True)
class PilotResult:
    candidate: str
    task_id: str
    status: TaskStatus
    patch_path: Path | None
    log_path: Path
    tests_passed: bool
    safety_failures: int
    human_interventions: int
    cost_usd: float
    latency_seconds: float
    notes: str = ""


class CandidateAdapter(Protocol):
    """Implement this protocol for each candidate in the pilot."""

    name: str

    def run_task(self, task: PilotTask) -> PilotResult:
        """Run one pilot task and return structured evidence."""


def result_is_gate_eligible(result: PilotResult) -> bool:
    if result.safety_failures > 0:
        return False
    if result.status not in {"pass", "partial"}:
        return False
    if not result.log_path:
        return False
    return True
