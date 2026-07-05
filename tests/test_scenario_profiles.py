import json
from pathlib import Path
import unittest

from scripts.simulate_alternatives import SCENARIOS


ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PROFILES = ROOT / "data" / "scenario_profiles.json"


class ScenarioProfilesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(SCENARIO_PROFILES.read_text(encoding="utf-8"))
        cls.profiles = cls.data["scenarios"]

    def test_profiles_cover_all_simulation_scenarios(self):
        self.assertEqual({profile["id"] for profile in self.profiles}, set(SCENARIOS))

    def test_profiles_are_actionable(self):
        for profile in self.profiles:
            self.assertTrue(profile["label"])
            self.assertTrue(profile["question"])
            self.assertGreaterEqual(len(profile["priorities"]), 4)
            self.assertGreaterEqual(len(profile["not_optimized_for"]), 3)
            self.assertGreaterEqual(len(profile["typical_shortlist"]), 3)


if __name__ == "__main__":
    unittest.main()
