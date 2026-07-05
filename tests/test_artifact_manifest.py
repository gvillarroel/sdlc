import csv
from pathlib import Path
import unittest

from scripts.generate_artifact_manifest import EXCLUDED_PATHS, manifest_rows


ROOT = Path(__file__).resolve().parents[1]


class ArtifactManifestTest(unittest.TestCase):
    def test_manifest_rows_include_core_artifacts(self):
        rows = manifest_rows()
        paths = {
            row["path"]
            for row in rows
        }
        self.assertIn("README.md", paths)
        self.assertIn("reports/ai_orchestrator_frameworks_report.md", paths)
        self.assertIn("results/deterministic_rankings.csv", paths)
        self.assertNotIn("results/artifact_manifest.csv", paths)
        self.assertIn("results/artifact_manifest.csv", EXCLUDED_PATHS)

    def test_generated_manifest_has_valid_hashes(self):
        with (ROOT / "results" / "artifact_manifest.csv").open(
            newline="",
            encoding="utf-8",
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertGreater(len(rows), 100)
        for row in rows:
            self.assertGreater(int(row["size_bytes"]), 0)
            self.assertEqual(len(row["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
