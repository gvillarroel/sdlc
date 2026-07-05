import unittest

from scripts.validate_markdown_tables import validation_rows


class MarkdownTableValidationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = validation_rows()

    def test_finds_markdown_tables(self):
        self.assertGreater(len(self.rows), 100)

    def test_all_tables_are_valid(self):
        failures = [
            row
            for row in self.rows
            if not row["ok"]
        ]
        self.assertEqual(failures, [])

    def test_rows_include_source_and_line(self):
        for row in self.rows:
            self.assertTrue(row["source_file"])
            self.assertGreater(int(row["start_line"]), 0)
            self.assertGreaterEqual(int(row["expected_columns"]), 1)


if __name__ == "__main__":
    unittest.main()
