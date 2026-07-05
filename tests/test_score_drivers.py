import unittest

from scripts.analyze_score_drivers import candidate_driver_rows, criterion_spread_rows
from scripts.simulate_alternatives import CRITERIA, load_data


class ScoreDriversTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _raw, cls.alternatives = load_data()
        cls.candidate_rows = candidate_driver_rows(cls.alternatives)
        cls.criterion_rows = criterion_spread_rows(cls.alternatives)

    def test_candidate_rows_cover_all_alternatives(self):
        self.assertEqual(len(self.candidate_rows), len(self.alternatives))
        ids = [row["alternative_id"] for row in self.candidate_rows]
        self.assertEqual(len(ids), len(set(ids)))

    def test_candidate_rows_include_strengths_and_weaknesses(self):
        for row in self.candidate_rows:
            self.assertIn("=", row["top_strengths"])
            self.assertIn("=", row["top_weaknesses"])
            self.assertGreaterEqual(int(row["best_rank"]), 1)
            self.assertGreaterEqual(int(row["worst_rank"]), int(row["best_rank"]))
            self.assertGreaterEqual(float(row["score_spread"]), 0)

    def test_criterion_rows_cover_all_criteria(self):
        criteria = {
            row["criterion"]
            for row in self.criterion_rows
        }
        self.assertEqual(criteria, set(CRITERIA))

    def test_criterion_rows_are_sorted_by_spread(self):
        spreads = [
            float(row["score_spread"])
            for row in self.criterion_rows
        ]
        self.assertEqual(spreads, sorted(spreads, reverse=True))


if __name__ == "__main__":
    unittest.main()
