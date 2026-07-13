from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

EXPECTED_SECTIONS = [
    "Start Here",
    "Evaluation at a Glance",
    "Key Finding",
    "How the Repository Works",
    "Repository Structure",
    "Quick Start",
    "Validation and CI",
    "Customize the Decision Model",
    "Copilot SDK Dynamic-Agent Proof of Concept",
    "Maintenance",
    "Limitations",
    "Repository License",
]

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class ReadmeStructureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = README.read_text(encoding="utf-8")

    def test_readme_has_one_title_and_an_ordered_section_hierarchy(self):
        title_lines = [line for line in self.text.splitlines() if line.startswith("# ")]
        section_lines = [line[3:] for line in self.text.splitlines() if line.startswith("## ")]

        self.assertEqual(title_lines, ["# AI Coding-Agent Orchestrator Evaluation"])
        self.assertEqual(section_lines, EXPECTED_SECTIONS)

    def test_all_relative_markdown_links_resolve(self):
        relative_targets = [
            target
            for target in MARKDOWN_LINK_RE.findall(self.text)
            if not target.startswith(("#", "http://", "https://", "mailto:"))
        ]

        self.assertGreaterEqual(len(relative_targets), 10)
        missing = [target for target in relative_targets if not (ROOT / target).exists()]
        self.assertEqual(missing, [])

    def test_readme_states_the_evidence_boundary_and_generated_file_policy(self):
        self.assertIn("not a live head-to-head benchmark", self.text)
        self.assertIn("Generated machine-readable outputs live in `results/`", self.text)
        self.assertIn("should not be edited manually", self.text)
        self.assertIn("does not declare a project license", self.text)


if __name__ == "__main__":
    unittest.main()
