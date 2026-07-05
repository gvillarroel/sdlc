import unittest

from scripts.build_scenario_playbooks import load_profiles, playbook_rows
from scripts.simulate_alternatives import SCENARIOS


class ScenarioPlaybooksTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profiles = load_profiles()
        cls.rows = playbook_rows(cls.profiles)

    def test_playbooks_cover_all_scenarios(self):
        scenarios = {
            row["scenario"]
            for row in self.rows
        }
        self.assertEqual(scenarios, set(SCENARIOS))

    def test_playbook_rows_are_actionable(self):
        for row in self.rows:
            self.assertTrue(row["primary_candidate"])
            self.assertIn(";", row["fallback_candidates"])
            self.assertTrue(row["pilot_focus"])
            self.assertTrue(row["no_go_condition"])
            self.assertIn("reports/pilot_protocol.md", row["related_artifacts"])

    def test_profiles_have_required_fields(self):
        for scenario in SCENARIOS:
            profile = self.profiles[scenario]
            self.assertTrue(profile["question"])
            self.assertGreaterEqual(len(profile["priorities"]), 4)
            self.assertTrue(profile["typical_shortlist"])


if __name__ == "__main__":
    unittest.main()
