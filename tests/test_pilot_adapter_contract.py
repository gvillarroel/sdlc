from pathlib import Path
import unittest

from examples.pilot.adapter import PilotResult, result_is_gate_eligible


class PilotAdapterContractTest(unittest.TestCase):
    def test_successful_result_is_gate_eligible(self):
        result = PilotResult(
            candidate="example",
            task_id="task-1",
            status="pass",
            patch_path=Path("patch.diff"),
            log_path=Path("run.log"),
            tests_passed=True,
            safety_failures=0,
            human_interventions=1,
            cost_usd=1.25,
            latency_seconds=120.0,
        )
        self.assertTrue(result_is_gate_eligible(result))

    def test_safety_failure_blocks_gate_eligibility(self):
        result = PilotResult(
            candidate="example",
            task_id="task-1",
            status="pass",
            patch_path=Path("patch.diff"),
            log_path=Path("run.log"),
            tests_passed=True,
            safety_failures=1,
            human_interventions=0,
            cost_usd=0.5,
            latency_seconds=80.0,
        )
        self.assertFalse(result_is_gate_eligible(result))

    def test_failed_status_blocks_gate_eligibility(self):
        result = PilotResult(
            candidate="example",
            task_id="task-1",
            status="fail",
            patch_path=None,
            log_path=Path("run.log"),
            tests_passed=False,
            safety_failures=0,
            human_interventions=2,
            cost_usd=0.5,
            latency_seconds=80.0,
        )
        self.assertFalse(result_is_gate_eligible(result))


if __name__ == "__main__":
    unittest.main()
