import unittest

from scripts.estimate_implementation_effort import estimate_rows
from scripts.simulate_alternatives import load_data


class ImplementationEffortTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw, cls.alternatives = load_data()
        cls.rows = estimate_rows(cls.raw, cls.alternatives)

    def test_effort_rows_cover_all_alternatives(self):
        self.assertEqual(len(self.rows), len(self.alternatives))
        ids = [row["alternative_id"] for row in self.rows]
        self.assertEqual(len(ids), len(set(ids)))

    def test_complexity_scores_and_effort_bands_are_valid(self):
        for row in self.rows:
            self.assertGreaterEqual(row["prototype_complexity_score"], 1)
            self.assertLessEqual(row["prototype_complexity_score"], 5)
            self.assertGreaterEqual(row["hardening_complexity_score"], 1)
            self.assertLessEqual(row["hardening_complexity_score"], 5)
            self.assertTrue(row["prototype_effort"])
            self.assertTrue(row["hardening_effort"])
            self.assertTrue(row["prototype_driver"])
            self.assertTrue(row["hardening_driver"])

    def test_scope_adjustment_captures_platform_hardening_work(self):
        by_id = {
            row["alternative_id"]: row
            for row in self.rows
        }
        self.assertGreater(
            by_id["open_swe"]["hardening_complexity_score"],
            by_id["codex_cli"]["hardening_complexity_score"],
        )
        self.assertGreater(
            by_id["omnigent"]["prototype_complexity_score"],
            by_id["aider"]["prototype_complexity_score"],
        )


if __name__ == "__main__":
    unittest.main()
