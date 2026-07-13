from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.check_english_content import (
    analyze_line,
    is_repository_text_path,
    scan_file,
)


def decoded_fixture(hex_value: str) -> str:
    """Decode a non-English fixture without embedding that prose in repository text."""
    return bytes.fromhex(hex_value).decode("utf-8")


class EnglishContentCheckTest(unittest.TestCase):
    def test_detects_sustained_non_english_prose(self):
        line = decoded_fixture(
            "4573746520504f432067656e657261206167656e74657320636f6e666967757261626c65732c20"
            "6c657320617369676e612068657272616d69656e7461732064697374696e7461732079206c6f73"
            "20656a656375746120756e6f2074726173206f74726f2e"
        )

        finding = analyze_line(Path("example.md"), 7, line)

        self.assertIsNotNone(finding)
        self.assertEqual(7, finding.line_number)
        self.assertGreaterEqual(len(finding.markers), 3)

    def test_detects_former_short_interface_labels(self):
        first = decoded_fixture("5265706f7274652066696e616c20676c6f62616c")
        second = decoded_fixture("566973746120676c6f62616c")

        self.assertIsNotNone(analyze_line(Path("site_test.py"), 1, first))
        self.assertIsNotNone(analyze_line(Path("site_test.py"), 2, second))

    def test_detects_non_english_markdown_heading(self):
        heading = decoded_fixture(
            "232050617065727320506172612042656e63686d61726b7320496e7465726e6f73204465204861"
            "726e6573736573"
        )

        finding = analyze_line(Path("report.md"), 1, heading)

        self.assertIsNotNone(finding)
        self.assertEqual("Spanish heading marker", finding.reason)

    def test_ignores_urls_paths_and_technical_identifiers(self):
        lines = [
            decoded_fixture(
                "5365652068747470733a2f2f6578616d706c652e636f6d2f636f6e66696775726163696f6e2f"
                "706172612f6167656e74657320666f722074686520757073747265616d207265666572656e63652e"
            ),
            decoded_fixture(
                "546865206669656c6473207265706f7274655f66696e616c2c206167656e7465735f64696e616d"
                "69636f732c20616e642076616c69646163696f6e5f726573756c7461646f20617265206964656e"
                "746966696572732e"
            ),
            decoded_fixture(
                "52756e2060746f6f6c202d2d70657266696c2073656775726f6020616e6420696e737065637420"
                "7265706f7274732f6d6f64656c6f2f726573756c7461646f732e6a736f6e2e"
            ),
            decoded_fixture(
                "54686520706172736572206163636570747320746865206964656e746966696572732022706172"
                "61222c2022636f6e222c20616e64202273696e222e"
            ),
        ]

        for line_number, line in enumerate(lines, start=1):
            with self.subTest(line=line):
                self.assertIsNone(analyze_line(Path("technical.md"), line_number, line))

    def test_english_prose_has_no_false_positive(self):
        lines = [
            "This repository evaluates permissively licensed coding-agent orchestrators.",
            "Run the same task suite with a fixed model policy and review every generated patch.",
            "The report links scoring evidence, uncertainty analysis, and pilot guidance.",
        ]

        for line_number, line in enumerate(lines, start=1):
            with self.subTest(line=line):
                self.assertIsNone(analyze_line(Path("README.md"), line_number, line))

    def test_path_filter_skips_locks_vendor_trees_and_binary_assets(self):
        included = [
            Path("README.md"),
            Path("scripts/check.py"),
            Path("data/input.json"),
            Path("results/output.csv"),
            Path("docs/index.html"),
        ]
        excluded = [
            Path("package-lock.json"),
            Path("vendor/reference.md"),
            Path("node_modules/package/readme.md"),
            Path("docs/assets/chart.svg"),
            Path("docs/assets/image.png"),
            Path("dist/bundle.js"),
            Path("generated.min.js"),
        ]

        for path in included:
            with self.subTest(path=path):
                self.assertTrue(is_repository_text_path(path))
        for path in excluded:
            with self.subTest(path=path):
                self.assertFalse(is_repository_text_path(path))

    def test_binary_data_with_text_extension_is_skipped(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "generated.md"
            path.write_bytes(b"generated\0binary\xffcontent")

            findings, scanned = scan_file(path, Path("generated.md"))

        self.assertFalse(scanned)
        self.assertEqual([], findings)


if __name__ == "__main__":
    unittest.main()
