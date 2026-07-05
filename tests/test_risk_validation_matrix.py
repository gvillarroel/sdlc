import unittest

from scripts.build_risk_validation_matrix import load_risks, matrix_rows


class RiskValidationMatrixTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.risks = load_risks()
        cls.rows = matrix_rows(cls.risks)

    def test_matrix_covers_all_risks(self):
        self.assertEqual(len(self.rows), len(self.risks))
        risk_ids = {
            row["risk_id"]
            for row in self.rows
        }
        self.assertEqual(risk_ids, {risk["id"] for risk in self.risks})

    def test_rows_have_validation_evidence(self):
        for row in self.rows:
            self.assertTrue(row["validation_artifact"])
            self.assertTrue(row["metric_to_capture"])
            self.assertTrue(row["pass_condition"])
            self.assertGreaterEqual(int(row["severity"]), 1)

    def test_rows_are_sorted_by_severity(self):
        severities = [
            int(row["severity"])
            for row in self.rows
        ]
        self.assertEqual(severities, sorted(severities, reverse=True))


if __name__ == "__main__":
    unittest.main()
