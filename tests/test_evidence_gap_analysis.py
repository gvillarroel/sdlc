import unittest

from scripts.analyze_evidence_gaps import evidence_gap_rows
from scripts.simulate_alternatives import load_data


class EvidenceGapAnalysisTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw, cls.alternatives = load_data()
        cls.rows = evidence_gap_rows(cls.raw)

    def test_evidence_gap_rows_cover_all_alternatives(self):
        self.assertEqual(len(self.rows), len(self.alternatives))
        ids = [row["alternative_id"] for row in self.rows]
        self.assertEqual(len(ids), len(set(ids)))

    def test_risk_bands_and_scores_are_valid(self):
        allowed_bands = {"low", "medium", "high"}
        for row in self.rows:
            self.assertIn(row["evidence_risk_band"], allowed_bands)
            self.assertGreaterEqual(row["evidence_risk_score"], 0)
            self.assertGreaterEqual(row["gap_count"], 0)
            self.assertTrue(row["mitigation"])
            self.assertTrue(row["adoption_implication"])

    def test_low_confidence_alpha_projects_are_high_risk(self):
        high_risk_ids = {
            row["alternative_id"]
            for row in self.rows
            if row["evidence_risk_band"] == "high"
        }
        self.assertIn("anchor", high_risk_ids)
        self.assertIn("omniagent", high_risk_ids)
        self.assertIn("omni_agent", high_risk_ids)


if __name__ == "__main__":
    unittest.main()
