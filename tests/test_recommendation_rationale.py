import unittest

from scripts.build_recommendation_rationale import (
    decision_posture,
    rationale_rows,
)


class RecommendationRationaleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = rationale_rows()

    def test_rationale_covers_each_scenario_shortlist(self):
        self.assertEqual(len(self.rows), 25)
        scenario_counts = {}
        for row in self.rows:
            scenario_counts[row["scenario"]] = scenario_counts.get(row["scenario"], 0) + 1
        self.assertEqual(set(scenario_counts.values()), {5})

    def test_each_scenario_has_actionable_candidate(self):
        actionable = {"Primary pilot candidate", "Head-to-head pilot"}
        scenarios = {row["scenario"] for row in self.rows}
        for scenario in scenarios:
            postures = {
                row["posture"]
                for row in self.rows
                if row["scenario"] == scenario
            }
            self.assertTrue(postures & actionable, scenario)

    def test_high_evidence_risk_never_becomes_primary(self):
        self.assertEqual(
            decision_posture(
                rank=1,
                win_rate=0.90,
                top3_rate=1.0,
                evidence_band="high",
            ),
            "Do not select as primary",
        )

    def test_rationale_rows_have_operational_ranks(self):
        for row in self.rows:
            self.assertGreaterEqual(int(row["pilot_operational_rank"]), 1)
            self.assertGreaterEqual(int(row["team_rollout_operational_rank"]), 1)
            self.assertGreaterEqual(int(row["autonomous_pr_operational_rank"]), 1)
            self.assertTrue(row["key_rationale"].endswith("."))


if __name__ == "__main__":
    unittest.main()
