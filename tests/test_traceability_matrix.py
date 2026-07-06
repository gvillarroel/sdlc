import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TraceabilityMatrixTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(
            (ROOT / "data" / "traceability_matrix.json").read_text(
                encoding="utf-8"
            )
        )

    def test_traceability_requirements_are_well_formed(self):
        requirements = self.data["requirements"]
        self.assertGreaterEqual(len(requirements), 8)
        ids = [item["id"] for item in requirements]
        self.assertEqual(len(ids), len(set(ids)))
        for item in requirements:
            self.assertTrue(item["requirement"])
            self.assertTrue(item["primary_artifacts"])
            self.assertTrue(item["validation"])

    def test_key_original_requirements_are_covered(self):
        ids = {
            item["id"]
            for item in self.data["requirements"]
        }
        for required_id in [
            "filter_permissive_open_source",
            "python_simulations",
            "dedicated_sandbox_report",
            "simulation_factors",
            "implementation_complexity",
            "english_final_report",
            "tests_and_reproducibility",
        ]:
            self.assertIn(required_id, ids)

    def test_declared_artifacts_exist(self):
        for item in self.data["requirements"]:
            for artifact in item["primary_artifacts"]:
                path = ROOT / artifact
                self.assertTrue(path.exists(), f"missing traceability artifact: {artifact}")


if __name__ == "__main__":
    unittest.main()
