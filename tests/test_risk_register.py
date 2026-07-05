import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
RISK_REGISTER = ROOT / "data" / "risk_register.json"


class RiskRegisterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(RISK_REGISTER.read_text(encoding="utf-8"))
        cls.risks = cls.data["risks"]

    def test_risk_register_has_unique_ids_and_enough_coverage(self):
        self.assertGreaterEqual(len(self.risks), 10)
        ids = [risk["id"] for risk in self.risks]
        self.assertEqual(len(ids), len(set(ids)))

    def test_risk_categories_cover_security_operations_and_quality(self):
        categories = {risk["category"] for risk in self.risks}
        for expected in {"security", "operational", "quality", "evaluation", "cost"}:
            self.assertIn(expected, categories)

    def test_each_risk_has_actionable_mitigation_and_evidence(self):
        for risk in self.risks:
            self.assertGreaterEqual(risk["likelihood"], 1)
            self.assertLessEqual(risk["likelihood"], 3)
            self.assertGreaterEqual(risk["impact"], 1)
            self.assertLessEqual(risk["impact"], 3)
            self.assertTrue(risk["trigger"])
            self.assertTrue(risk["mitigation"])
            self.assertTrue(risk["evidence_required"])
            self.assertTrue(risk["affected_candidates"])


if __name__ == "__main__":
    unittest.main()
