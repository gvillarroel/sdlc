import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SecurityFixturesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(
            (ROOT / "data" / "security_evaluation_fixtures.json").read_text(
                encoding="utf-8"
            )
        )

    def test_security_fixtures_are_well_formed(self):
        fixtures = self.data["fixtures"]
        self.assertGreaterEqual(len(fixtures), 8)
        ids = [item["id"] for item in fixtures]
        self.assertEqual(len(ids), len(set(ids)))
        required_fields = {
            "id",
            "category",
            "threat",
            "setup",
            "expected_behavior",
            "pass_condition",
            "applies_to",
        }
        for item in fixtures:
            self.assertEqual(set(item), required_fields)
            self.assertTrue(item["pass_condition"])
            self.assertTrue(item["applies_to"])

    def test_critical_security_categories_are_covered(self):
        categories = {
            item["category"]
            for item in self.data["fixtures"]
        }
        for category in [
            "sandbox",
            "secrets",
            "prompt_injection",
            "network",
            "human_control",
        ]:
            self.assertIn(category, categories)


if __name__ == "__main__":
    unittest.main()
