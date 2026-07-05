import unittest

from scripts.check_local_artifact_references import reference_rows


class LocalArtifactReferencesTest(unittest.TestCase):
    def test_all_markdown_artifact_references_exist(self):
        rows = reference_rows()
        self.assertGreater(len(rows), 100)
        missing = [
            row
            for row in rows
            if not row["exists"]
        ]
        self.assertEqual(missing, [])

    def test_core_reports_are_scanned(self):
        rows = reference_rows()
        sources = {
            row["source_file"]
            for row in rows
        }
        self.assertIn("README.md", sources)
        self.assertIn("reports/ai_orchestrator_frameworks_report.md", sources)
        self.assertIn("reports/artifact_index.md", sources)


if __name__ == "__main__":
    unittest.main()
