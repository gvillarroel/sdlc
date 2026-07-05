import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PILOT_TASKS = ROOT / "data" / "pilot_tasks.json"


class PilotTasksTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(PILOT_TASKS.read_text(encoding="utf-8"))
        cls.tasks = cls.data["tasks"]

    def test_task_suite_has_expected_size_and_unique_ids(self):
        self.assertEqual(len(self.tasks), 20)
        ids = [task["id"] for task in self.tasks]
        self.assertEqual(len(ids), len(set(ids)))

    def test_task_suite_covers_required_categories(self):
        categories = {task["category"] for task in self.tasks}
        expected = {
            "bug_fix",
            "refactor",
            "test_generation",
            "dependency_update",
            "documentation",
            "security_fixture"
        }
        self.assertTrue(expected.issubset(categories))

    def test_each_task_has_reviewable_acceptance_criteria(self):
        for task in self.tasks:
            self.assertGreaterEqual(len(task["acceptance_criteria"]), 3, task["id"])
            self.assertIn(task["difficulty"], {"low", "medium", "high"})
            self.assertIsInstance(task["safety_hooks"], list)

    def test_required_metrics_include_quality_cost_and_safety(self):
        metrics = set(self.data["required_metrics"])
        for metric in {
            "task_result",
            "estimated_model_cost_usd",
            "human_intervention_count",
            "unsafe_action_attempt_count",
            "reviewer_acceptance"
        }:
            self.assertIn(metric, metrics)


if __name__ == "__main__":
    unittest.main()
