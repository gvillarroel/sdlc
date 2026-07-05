import unittest

from scripts.validate_csv_schemas import SCHEMAS, schema_rows


class CsvSchemasTest(unittest.TestCase):
    def test_schema_map_covers_core_outputs(self):
        for filename in [
            "deterministic_rankings.csv",
            "monte_carlo_summary.csv",
            "stress_test_summary.csv",
            "score_driver_summary.csv",
            "criterion_spread_summary.csv",
            "scenario_playbook_summary.csv",
            "implementation_effort_estimates.csv",
            "operational_cost_estimates.csv",
            "operational_fit_rankings.csv",
            "pilot_sample_size_estimates.csv",
            "evidence_gap_analysis.csv",
            "recommendation_rationale.csv",
            "risk_validation_matrix.csv",
            "markdown_table_check.csv",
            "github_metadata_check.csv",
        ]:
            self.assertIn(filename, SCHEMAS)

    def test_generated_csv_headers_match_required_schemas(self):
        rows = schema_rows()
        self.assertGreaterEqual(len(rows), 20)
        failures = [
            row
            for row in rows
            if not row["ok"]
        ]
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
