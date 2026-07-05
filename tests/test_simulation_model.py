import unittest

from scripts.simulate_alternatives import (
    CRITERIA,
    PERMISSIVE_LICENSES,
    SCENARIOS,
    deterministic_rankings,
    load_data,
    run_monte_carlo,
    validate_data,
    weighted_score
)


class SimulationModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw, cls.alternatives = load_data()

    def test_dataset_is_valid_and_permissive(self):
        validate_data(self.alternatives)
        self.assertGreaterEqual(len(self.alternatives), 10)
        for alternative in self.alternatives:
            self.assertIn(alternative.license, PERMISSIVE_LICENSES)

    def test_scores_cover_all_criteria_and_range(self):
        for alternative in self.alternatives:
            self.assertEqual(set(alternative.scores), set(CRITERIA))
            for score in alternative.scores.values():
                self.assertGreaterEqual(score, 0)
                self.assertLessEqual(score, 5)

    def test_weighted_score_bounds(self):
        weights = {criterion: 1.0 for criterion in CRITERIA}
        for alternative in self.alternatives:
            score = weighted_score(alternative.scores, weights)
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 5)

    def test_deterministic_rankings_are_sorted(self):
        rankings = deterministic_rankings(self.alternatives)
        self.assertEqual(set(rankings), set(SCENARIOS))
        for rows in rankings.values():
            scores = [row["score"] for row in rows]
            self.assertEqual(scores, sorted(scores, reverse=True))
            self.assertEqual([row["rank"] for row in rows], list(range(1, len(rows) + 1)))

    def test_monte_carlo_is_reproducible_for_fixed_seed(self):
        first = run_monte_carlo(self.alternatives, trials=50, seed=123)
        second = run_monte_carlo(self.alternatives, trials=50, seed=123)
        self.assertEqual(first, second)
        for rows in first.values():
            for row in rows:
                self.assertGreaterEqual(row["win_rate"], 0)
                self.assertLessEqual(row["win_rate"], 1)
                self.assertGreaterEqual(row["top3_rate"], 0)
                self.assertLessEqual(row["top3_rate"], 1)


if __name__ == "__main__":
    unittest.main()
