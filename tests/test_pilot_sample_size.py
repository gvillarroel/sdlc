import unittest

from scripts.estimate_pilot_sample_sizes import (
    estimate_rows,
    load_model,
    recommended_task_counts,
    score_to_success_rate,
)
from scripts.simulate_alternatives import SCENARIOS


class PilotSampleSizeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = load_model()
        cls.rows = estimate_rows(cls.model)

    def test_score_to_success_rate_respects_bounds(self):
        floor = self.model["score_to_success_rate"]["floor"]
        ceiling = self.model["score_to_success_rate"]["ceiling"]
        self.assertEqual(score_to_success_rate(0, self.model), floor)
        self.assertEqual(score_to_success_rate(5, self.model), ceiling)
        self.assertGreater(score_to_success_rate(4, self.model), floor)
        self.assertLess(score_to_success_rate(4, self.model), ceiling)

    def test_sample_size_rows_cover_scenarios_comparisons_and_counts(self):
        expected = (
            len(SCENARIOS)
            * len(self.model["comparison_ranks"])
            * len(self.model["task_counts_per_candidate"])
        )
        self.assertEqual(len(self.rows), expected)

    def test_probabilities_are_valid(self):
        for row in self.rows:
            self.assertGreaterEqual(float(row["top_wins_probability"]), 0)
            self.assertLessEqual(float(row["top_wins_probability"]), 1)
            self.assertGreaterEqual(float(row["tie_probability"]), 0)
            self.assertLessEqual(float(row["tie_probability"]), 1)
            self.assertGreater(int(row["tasks_per_candidate"]), 0)

    def test_recommended_task_counts_cover_each_comparison(self):
        summary_rows = recommended_task_counts(self.rows)
        expected = len(SCENARIOS) * len(self.model["comparison_ranks"])
        self.assertEqual(len(summary_rows), expected)
        for row in summary_rows:
            self.assertTrue(row["recommended_tasks_per_candidate"])
            self.assertTrue(row["recommendation"])


if __name__ == "__main__":
    unittest.main()
