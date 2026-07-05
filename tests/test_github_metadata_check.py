import csv
from pathlib import Path
import unittest

from scripts.simulate_alternatives import load_data


ROOT = Path(__file__).resolve().parents[1]


class GitHubMetadataCheckTest(unittest.TestCase):
    def test_generated_metadata_check_covers_all_alternatives(self):
        _raw, alternatives = load_data()
        with (ROOT / "results" / "github_metadata_check.csv").open(
            newline="",
            encoding="utf-8",
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), len(alternatives))
        self.assertTrue(all(row["ok"] == "True" for row in rows))
        self.assertTrue(all(row["license_matches"] == "True" for row in rows))
        self.assertTrue(all(row["archived"] == "False" for row in rows))


if __name__ == "__main__":
    unittest.main()
