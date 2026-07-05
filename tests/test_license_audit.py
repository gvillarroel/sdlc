import unittest

from scripts.license_audit import PERMISSIVE, license_audit_rows


class LicenseAuditTest(unittest.TestCase):
    def test_included_rows_are_permissive(self):
        rows = license_audit_rows()
        included = [row for row in rows if row["status"] == "included"]
        self.assertGreaterEqual(len(included), 10)
        for row in included:
            self.assertIn(row["license"], PERMISSIVE)
            self.assertTrue(row["is_permissive"])

    def test_excluded_rows_include_original_non_matching_entries(self):
        rows = license_audit_rows()
        excluded_names = {
            row["alternative"]
            for row in rows
            if row["status"] == "excluded"
        }
        self.assertIn("Claude Agent SDK", excluded_names)
        self.assertIn("Codex app", excluded_names)


if __name__ == "__main__":
    unittest.main()
