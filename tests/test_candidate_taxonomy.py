import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CandidateTaxonomyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(
            (ROOT / "data" / "candidate_taxonomy.json").read_text(
                encoding="utf-8"
            )
        )

    def test_taxonomy_groups_are_well_formed(self):
        groups = self.data["groups"]
        self.assertGreaterEqual(len(groups), 5)
        ids = [group["id"] for group in groups]
        self.assertEqual(len(ids), len(set(ids)))
        for group in groups:
            self.assertTrue(group["name"])
            self.assertTrue(group["candidates"])
            self.assertTrue(group["use_when"])
            self.assertTrue(group["watch_for"])

    def test_core_candidate_groups_exist(self):
        ids = {
            group["id"]
            for group in self.data["groups"]
        }
        self.assertIn("programmable_sdk_framework", ids)
        self.assertIn("local_developer_cli", ids)
        self.assertIn("research_harness", ids)
        self.assertIn("control_plane", ids)


if __name__ == "__main__":
    unittest.main()
