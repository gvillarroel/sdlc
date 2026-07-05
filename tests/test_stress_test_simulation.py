import unittest

from scripts.simulate_alternatives import SCENARIOS, load_data
from scripts.stress_test_simulation import (
    DETERMINISTIC_STRESS_CASES,
    UNCERTAINTY_STRESS_CASES,
    deterministic_stress_results,
    uncertainty_stress_results,
)


class StressTestSimulationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _raw, cls.alternatives = load_data()

    def test_deterministic_stress_results_cover_all_cases_and_scenarios(self):
        summary_rows, ranking_rows = deterministic_stress_results(self.alternatives)
        self.assertEqual(
            len(summary_rows),
            len(DETERMINISTIC_STRESS_CASES) * len(SCENARIOS),
        )
        self.assertEqual(
            len(ranking_rows),
            len(DETERMINISTIC_STRESS_CASES) * len(SCENARIOS) * len(self.alternatives),
        )
        baseline_rows = [
            row
            for row in summary_rows
            if row["stress_case"] == "baseline"
        ]
        self.assertEqual(len(baseline_rows), len(SCENARIOS))
        for row in baseline_rows:
            self.assertFalse(row["rank1_changed"])
            self.assertEqual(row["top3_overlap"], 3)
        for row in summary_rows:
            self.assertGreaterEqual(row["top3_overlap"], 0)
            self.assertLessEqual(row["top3_overlap"], 3)
            self.assertGreaterEqual(row["rank1_margin"], 0)

    def test_uncertainty_stress_results_cover_all_cases_and_scenarios(self):
        summary_rows, detail_rows = uncertainty_stress_results(
            self.alternatives,
            trials=25,
            seed=123,
        )
        self.assertEqual(
            len(summary_rows),
            len(UNCERTAINTY_STRESS_CASES) * len(SCENARIOS),
        )
        self.assertEqual(
            len(detail_rows),
            len(UNCERTAINTY_STRESS_CASES) * len(SCENARIOS) * len(self.alternatives),
        )
        for row in summary_rows:
            self.assertGreaterEqual(row["win_rate"], 0)
            self.assertLessEqual(row["win_rate"], 1)
            self.assertGreaterEqual(row["top3_rate"], 0)
            self.assertLessEqual(row["top3_rate"], 1)
            self.assertGreaterEqual(row["trials"], 1)


if __name__ == "__main__":
    unittest.main()
