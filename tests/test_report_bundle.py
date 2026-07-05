from pathlib import Path
import unittest

from scripts.build_report_bundle import SOURCE_REPORTS, bundle_markdown


ROOT = Path(__file__).resolve().parents[1]


class ReportBundleTest(unittest.TestCase):
    def test_bundle_includes_all_source_reports(self):
        text = bundle_markdown()
        for filename in SOURCE_REPORTS:
            self.assertIn(f"reports/{filename}", text)
        self.assertIn("# Final Report Bundle", text)
        self.assertIn("# Executive Brief", text)
        self.assertIn("# Validation Summary", text)

    def test_generated_bundle_exists(self):
        bundle = ROOT / "reports" / "final_report_bundle.md"
        self.assertTrue(bundle.exists())
        text = bundle.read_text(encoding="utf-8")
        self.assertIn("# Final Report Bundle", text)
        self.assertIn("Source files remain authoritative", text)


if __name__ == "__main__":
    unittest.main()
