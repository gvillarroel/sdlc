from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ReportArtifactsTest(unittest.TestCase):
    def test_report_contains_decision_sections(self):
        report = (ROOT / "reports" / "ai_orchestrator_frameworks_report.md").read_text(
            encoding="utf-8"
        )
        required_sections = [
            "## Implementation Effort Estimates",
            "## Category Scorecards",
            "## Decision Shortlist",
            "## Candidate Deep Dives",
            "## Recommended Pilot Plan",
            "## Security Checklist",
            "## From This Simulation To A Real Evaluation"
        ]
        for section in required_sections:
            self.assertIn(section, report)

    def test_executive_brief_exists(self):
        brief = ROOT / "reports" / "executive_brief.md"
        self.assertTrue(brief.exists())
        text = brief.read_text(encoding="utf-8")
        self.assertIn("# Executive Brief", text)
        self.assertIn("Recommended Next Step", text)

    def test_methodology_appendix_exists(self):
        appendix = ROOT / "reports" / "methodology_appendix.md"
        self.assertTrue(appendix.exists())
        text = appendix.read_text(encoding="utf-8")
        self.assertIn("# Methodology Appendix", text)
        self.assertIn("Weighted Scenario Score", text)
        self.assertIn("Monte Carlo Model", text)

    def test_artifact_index_exists(self):
        index = ROOT / "reports" / "artifact_index.md"
        self.assertTrue(index.exists())
        text = index.read_text(encoding="utf-8")
        self.assertIn("# Artifact Index", text)
        self.assertIn("Generated Results", text)
        self.assertIn("Pilot Execution", text)

    def test_pilot_protocol_exists(self):
        protocol = ROOT / "reports" / "pilot_protocol.md"
        self.assertTrue(protocol.exists())
        text = protocol.read_text(encoding="utf-8")
        self.assertIn("# Pilot Protocol", text)
        self.assertIn("Decision Rule", text)
        self.assertIn("Safety gate", text)

    def test_generated_result_files_exist(self):
        expected_files = [
            "deterministic_rankings.csv",
            "monte_carlo_summary.csv",
            "sensitivity_summary.csv",
            "category_scores.csv",
            "decision_shortlist.csv",
            "all_results.json"
        ]
        for filename in expected_files:
            path = ROOT / "results" / filename
            self.assertTrue(path.exists(), f"missing generated result file: {path}")
            self.assertGreater(path.stat().st_size, 0)

    def test_pilot_templates_exist(self):
        expected_files = [
            "pilot_run_log.csv",
            "reviewer_scorecard.md",
            "security_gate_checklist.md"
        ]
        for filename in expected_files:
            path = ROOT / "templates" / filename
            self.assertTrue(path.exists(), f"missing template file: {path}")
            self.assertGreater(path.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
