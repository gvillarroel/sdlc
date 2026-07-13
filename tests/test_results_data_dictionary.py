from pathlib import Path
import unittest

from scripts.build_results_data_dictionary import RESULT_SCHEMAS, build_dictionary


ROOT = Path(__file__).resolve().parents[1]


class ResultsDataDictionaryTest(unittest.TestCase):
    def test_dictionary_includes_all_schema_files(self):
        text = build_dictionary()
        for filename in RESULT_SCHEMAS:
            self.assertIn(f"## `{filename}`", text)
        self.assertNotIn("market_maintenance_source_matrix.csv", text)
        self.assertIn("Expected columns come from", text)

    def test_generated_dictionary_exists(self):
        path = ROOT / "reports" / "results_data_dictionary.md"
        self.assertTrue(path.exists())
        text = path.read_text(encoding="utf-8")
        self.assertIn("# Results Data Dictionary", text)
        self.assertIn("deterministic_rankings.csv", text)
        self.assertIn("score_driver_summary.csv", text)
        self.assertIn("scenario_playbook_summary.csv", text)
        self.assertIn("operational_cost_estimates.csv", text)
        self.assertIn("pilot_sample_size_estimates.csv", text)
        self.assertIn("risk_validation_matrix.csv", text)
        self.assertIn("markdown_table_check.csv", text)
        self.assertIn("csv_schema_check.csv", text)


if __name__ == "__main__":
    unittest.main()
