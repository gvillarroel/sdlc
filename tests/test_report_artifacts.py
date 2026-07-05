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
            "## Stress Test Findings",
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
        self.assertIn("Assumption Stress Tests", text)

    def test_simulation_assumptions_report_exists(self):
        assumptions = ROOT / "reports" / "simulation_assumptions.md"
        self.assertTrue(assumptions.exists())
        text = assumptions.read_text(encoding="utf-8")
        self.assertIn("# Simulation Assumptions And Stress Tests", text)
        self.assertIn("Observed Ranking Changes", text)
        self.assertIn("data/simulation_assumptions.json", text)

    def test_evidence_gap_report_exists(self):
        evidence = ROOT / "reports" / "evidence_gap_analysis.md"
        self.assertTrue(evidence.exists())
        text = evidence.read_text(encoding="utf-8")
        self.assertIn("# Evidence Gap Analysis", text)
        self.assertIn("results/evidence_gap_analysis.csv", text)
        self.assertIn("High", text)

    def test_github_metadata_report_exists(self):
        metadata = ROOT / "reports" / "github_metadata_check.md"
        self.assertTrue(metadata.exists())
        text = metadata.read_text(encoding="utf-8")
        self.assertIn("# GitHub Metadata Check", text)
        self.assertIn("results/github_metadata_check.csv", text)
        self.assertIn("license mismatches", text)

    def test_requirements_traceability_report_exists(self):
        traceability = ROOT / "reports" / "requirements_traceability.md"
        self.assertTrue(traceability.exists())
        text = traceability.read_text(encoding="utf-8")
        self.assertIn("# Requirements Traceability", text)
        self.assertIn("data/traceability_matrix.json", text)
        self.assertIn("python scripts/run_all_checks.py", text)

    def test_security_evaluation_fixtures_report_exists(self):
        security = ROOT / "reports" / "security_evaluation_fixtures.md"
        self.assertTrue(security.exists())
        text = security.read_text(encoding="utf-8")
        self.assertIn("# Security Evaluation Fixtures", text)
        self.assertIn("data/security_evaluation_fixtures.json", text)
        self.assertIn("prompt_injection_issue", text)

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

    def test_decision_tree_report_exists(self):
        tree = ROOT / "reports" / "decision_tree.md"
        self.assertTrue(tree.exists())
        text = tree.read_text(encoding="utf-8")
        self.assertIn("# Decision Tree", text)
        self.assertIn("Guided Selection", text)

    def test_implementation_blueprints_exist(self):
        blueprints = ROOT / "reports" / "implementation_blueprints.md"
        self.assertTrue(blueprints.exists())
        text = blueprints.read_text(encoding="utf-8")
        self.assertIn("# Implementation Blueprints", text)
        self.assertIn("OpenHands Software Agent SDK", text)
        self.assertIn("Codex CLI", text)

    def test_generated_result_files_exist(self):
        expected_files = [
            "deterministic_rankings.csv",
            "monte_carlo_summary.csv",
            "sensitivity_summary.csv",
            "category_scores.csv",
            "decision_shortlist.csv",
            "implementation_effort_estimates.csv",
            "evidence_gap_analysis.csv",
            "custom_weights_example_rankings.csv",
            "local_artifact_reference_check.csv",
            "github_metadata_check.csv",
            "csv_schema_check.csv",
            "stress_test_summary.csv",
            "uncertainty_stress_summary.csv",
            "all_results.json"
        ]
        for filename in expected_files:
            path = ROOT / "results" / filename
            self.assertTrue(path.exists(), f"missing generated result file: {path}")
            self.assertGreater(path.stat().st_size, 0)

    def test_pilot_templates_exist(self):
        expected_files = [
            "pilot_run_log.csv",
            "pilot_candidate_summary.csv",
            "reviewer_scorecard.md",
            "security_gate_checklist.md"
        ]
        for filename in expected_files:
            path = ROOT / "templates" / filename
            self.assertTrue(path.exists(), f"missing template file: {path}")
            self.assertGreater(path.stat().st_size, 0)

    def test_examples_exist(self):
        expected_files = [
            "pilot_candidate_summary.example.csv",
            "custom_weights.example.json",
        ]
        for filename in expected_files:
            example = ROOT / "examples" / filename
            self.assertTrue(example.exists())
            self.assertGreater(example.stat().st_size, 0)

    def test_generated_svg_assets_exist(self):
        expected_files = [
            "rank_stability.svg",
            "scenario_regret.svg"
        ]
        for filename in expected_files:
            path = ROOT / "reports" / "assets" / filename
            self.assertTrue(path.exists(), f"missing SVG asset: {path}")
            text = path.read_text(encoding="utf-8")
            self.assertIn("<svg", text)
            self.assertIn("</svg>", text)


if __name__ == "__main__":
    unittest.main()
