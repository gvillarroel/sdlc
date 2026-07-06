from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ReleaseNotesTest(unittest.TestCase):
    def test_release_notes_validation_snapshot_matches_summary(self):
        release_notes = (ROOT / "reports" / "release_notes.md").read_text(
            encoding="utf-8"
        )
        validation_summary = (ROOT / "reports" / "validation_summary.md").read_text(
            encoding="utf-8"
        )

        for fragment in [
            "141 tests passed",
            "41 schemas checked",
            "853 references checked",
            "313 tables checked",
        ]:
            self.assertIn(fragment, release_notes)

        for fragment in [
            "141 tests passed",
            "41 CSV schemas checked",
            "853 local references checked",
            "313 tables checked",
        ]:
            self.assertIn(fragment, validation_summary)

    def test_release_notes_points_to_operational_refresh_guidance(self):
        release_notes = (ROOT / "reports" / "release_notes.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("reports/maintenance_guide.md", release_notes)
        self.assertIn("results/github_metadata_check.csv", release_notes)


if __name__ == "__main__":
    unittest.main()
