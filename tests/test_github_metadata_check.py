import csv
from pathlib import Path
import unittest

from scripts.build_github_metadata_report import build_report, read_rows, top_star_deltas
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

    def test_metadata_report_matches_latest_csv(self):
        rows = read_rows()
        expected = build_report(rows)
        actual = (ROOT / "reports" / "github_metadata_check.md").read_text(
            encoding="utf-8"
        )
        self.assertEqual(actual, expected)

    def test_metadata_report_top_star_deltas_are_sorted(self):
        rows = [
            {
                "alternative": "Small",
                "dataset_stars": "10",
                "live_stars": "11",
                "star_delta": "1",
            },
            {
                "alternative": "Largest",
                "dataset_stars": "20",
                "live_stars": "9",
                "star_delta": "-11",
            },
            {
                "alternative": "Middle",
                "dataset_stars": "30",
                "live_stars": "37",
                "star_delta": "7",
            },
            {
                "alternative": "Skipped",
                "dataset_stars": "",
                "live_stars": "",
                "star_delta": "",
            },
        ]

        ranked = top_star_deltas(rows, count=2)

        self.assertEqual([row["alternative"] for row in ranked], ["Largest", "Middle"])


if __name__ == "__main__":
    unittest.main()
