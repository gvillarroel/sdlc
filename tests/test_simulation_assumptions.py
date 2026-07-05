import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SimulationAssumptionsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(
            (ROOT / "data" / "simulation_assumptions.json").read_text(
                encoding="utf-8"
            )
        )

    def test_assumption_register_has_required_fields(self):
        assumptions = self.data["assumptions"]
        self.assertGreaterEqual(len(assumptions), 10)
        ids = [item["id"] for item in assumptions]
        self.assertEqual(len(ids), len(set(ids)))
        required_fields = {
            "id",
            "category",
            "assumption",
            "impact",
            "ranking_effect",
            "how_to_detect",
            "mitigation",
            "covered_by",
        }
        for item in assumptions:
            self.assertEqual(set(item), required_fields)
            self.assertGreaterEqual(item["impact"], 1)
            self.assertLessEqual(item["impact"], 5)
            self.assertTrue(item["covered_by"])

    def test_high_impact_assumptions_cover_security_and_execution(self):
        high_impact = [
            item
            for item in self.data["assumptions"]
            if item["impact"] >= 5
        ]
        categories = {item["category"] for item in high_impact}
        self.assertIn("security", categories)
        self.assertIn("execution", categories)
        self.assertIn("evaluation", categories)


if __name__ == "__main__":
    unittest.main()
