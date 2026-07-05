import unittest

from scripts.estimate_operational_costs import (
    estimate_rows,
    load_model,
    operational_fit_rows,
)
from scripts.simulate_alternatives import SCENARIOS, load_data


class OperationalCostModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = load_model()
        _raw, cls.alternatives = load_data()
        cls.cost_rows = estimate_rows(cls.model, cls.alternatives)
        cls.fit_rows = operational_fit_rows(cls.model, cls.alternatives, cls.cost_rows)

    def test_cost_rows_cover_all_profiles_and_alternatives(self):
        expected = len(self.alternatives) * len(self.model["profiles"])
        self.assertEqual(len(self.cost_rows), expected)
        keys = {
            (row["operating_profile"], row["alternative_id"])
            for row in self.cost_rows
        }
        self.assertEqual(len(keys), expected)

    def test_cost_scores_are_in_valid_ranges(self):
        valid_bands = {"Low", "Moderate", "High", "Very high"}
        for row in self.cost_rows:
            self.assertGreater(float(row["monthly_operational_hours"]), 0)
            self.assertGreater(float(row["relative_token_pressure"]), 0)
            self.assertGreaterEqual(float(row["latency_risk_score"]), 1)
            self.assertLessEqual(float(row["latency_risk_score"]), 5)
            self.assertGreaterEqual(float(row["operational_friction_score"]), 1)
            self.assertLessEqual(float(row["operational_friction_score"]), 5)
            self.assertIn(row["cost_risk_band"], valid_bands)
            self.assertTrue(row["main_cost_driver"])

    def test_hours_scale_with_operating_profile_volume(self):
        rows_by_key = {
            (row["operating_profile"], row["alternative_id"]): row
            for row in self.cost_rows
        }
        for alt in self.alternatives:
            pilot = rows_by_key[("pilot_100_tasks", alt.id)]
            rollout = rows_by_key[("team_rollout_400_tasks", alt.id)]
            autonomous = rows_by_key[("autonomous_pr_1000_tasks", alt.id)]
            self.assertLess(
                float(pilot["monthly_operational_hours"]),
                float(rollout["monthly_operational_hours"]),
            )
            self.assertLess(
                float(rollout["monthly_operational_hours"]),
                float(autonomous["monthly_operational_hours"]),
            )

    def test_fit_rankings_cover_each_scenario_and_profile(self):
        expected = len(self.alternatives) * len(self.model["profiles"]) * len(SCENARIOS)
        self.assertEqual(len(self.fit_rows), expected)
        for scenario in SCENARIOS:
            for profile in self.model["profiles"]:
                ranks = [
                    row["rank"]
                    for row in self.fit_rows
                    if row["scenario"] == scenario
                    and row["operating_profile"] == profile["id"]
                ]
                self.assertEqual(ranks, list(range(1, len(self.alternatives) + 1)))


if __name__ == "__main__":
    unittest.main()
