import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DECISION_TREE = ROOT / "data" / "decision_tree.json"


class DecisionTreeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(DECISION_TREE.read_text(encoding="utf-8"))
        cls.questions = cls.data["questions"]

    def test_questions_are_unique_and_linked(self):
        ids = [question["id"] for question in self.questions]
        self.assertEqual(len(ids), len(set(ids)))
        id_set = set(ids)
        for question in self.questions:
            next_id = question.get("no_next")
            if next_id:
                self.assertIn(next_id, id_set)

    def test_each_terminal_recommendation_has_candidates(self):
        for question in self.questions:
            for branch in ("yes", "no"):
                value = question.get(branch)
                if isinstance(value, dict):
                    self.assertGreaterEqual(len(value["recommendation"]), 2)
                    self.assertTrue(value["reason"])


if __name__ == "__main__":
    unittest.main()
