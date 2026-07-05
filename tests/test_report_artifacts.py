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
            "## Operational Cost Model",
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

    def test_release_notes_exist(self):
        notes = ROOT / "reports" / "release_notes.md"
        self.assertTrue(notes.exists())
        text = notes.read_text(encoding="utf-8")
        self.assertIn("# Release Notes", text)
        self.assertIn("Current Validation Snapshot", text)
        self.assertIn("reports/final_report_bundle.md", text)

    def test_adoption_decision_record_exists(self):
        adr = ROOT / "reports" / "adoption_decision_record.md"
        self.assertTrue(adr.exists())
        text = adr.read_text(encoding="utf-8")
        self.assertIn("# Adoption Decision Record", text)
        self.assertIn("No-Go Conditions", text)
        self.assertIn("Status: Proposed", text)

    def test_final_report_bundle_exists(self):
        bundle = ROOT / "reports" / "final_report_bundle.md"
        self.assertTrue(bundle.exists())
        text = bundle.read_text(encoding="utf-8")
        self.assertIn("# Final Report Bundle", text)
        self.assertIn("reports/ai_orchestrator_frameworks_report.md", text)
        self.assertIn("# Executive Brief", text)

    def test_faq_exists(self):
        faq = ROOT / "reports" / "faq.md"
        self.assertTrue(faq.exists())
        text = faq.read_text(encoding="utf-8")
        self.assertIn("# FAQ", text)
        self.assertIn("Why is there no single winner?", text)
        self.assertIn("rank_with_custom_weights.py", text)

    def test_candidate_taxonomy_report_exists(self):
        taxonomy = ROOT / "reports" / "candidate_taxonomy.md"
        self.assertTrue(taxonomy.exists())
        text = taxonomy.read_text(encoding="utf-8")
        self.assertIn("# Candidate Taxonomy", text)
        self.assertIn("data/candidate_taxonomy.json", text)
        self.assertIn("Programmable SDK or framework", text)

    def test_environment_prerequisites_exists(self):
        prerequisites = ROOT / "reports" / "environment_prerequisites.md"
        self.assertTrue(prerequisites.exists())
        text = prerequisites.read_text(encoding="utf-8")
        self.assertIn("# Environment Prerequisites", text)
        self.assertIn("Python 3.12", text)
        self.assertIn("run_all_checks.ps1", text)

    def test_exclusions_report_exists(self):
        exclusions = ROOT / "reports" / "exclusions.md"
        self.assertTrue(exclusions.exists())
        text = exclusions.read_text(encoding="utf-8")
        self.assertIn("# Exclusions", text)
        self.assertIn("Claude Agent SDK", text)
        self.assertIn("Codex app", text)

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

    def test_glossary_exists(self):
        glossary = ROOT / "reports" / "glossary.md"
        self.assertTrue(glossary.exists())
        text = glossary.read_text(encoding="utf-8")
        self.assertIn("# Glossary", text)
        self.assertIn("Monte Carlo stability", text)
        self.assertIn("Provider portability", text)

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

    def test_validation_summary_report_exists(self):
        summary = ROOT / "reports" / "validation_summary.md"
        self.assertTrue(summary.exists())
        text = summary.read_text(encoding="utf-8")
        self.assertIn("# Validation Summary", text)
        self.assertIn("python scripts/run_all_checks.py", text)
        self.assertIn("131 tests passed", text)

    def test_results_data_dictionary_exists(self):
        dictionary = ROOT / "reports" / "results_data_dictionary.md"
        self.assertTrue(dictionary.exists())
        text = dictionary.read_text(encoding="utf-8")
        self.assertIn("# Results Data Dictionary", text)
        self.assertIn("monte_carlo_summary.csv", text)
        self.assertIn("github_metadata_check.csv", text)

    def test_operational_cost_model_exists(self):
        model = ROOT / "reports" / "operational_cost_model.md"
        self.assertTrue(model.exists())
        text = model.read_text(encoding="utf-8")
        self.assertIn("# Operational Cost Model", text)
        self.assertIn("results/operational_cost_estimates.csv", text)
        self.assertIn("Largest Operation-Adjusted Rank Shifts", text)

    def test_score_driver_summary_exists(self):
        summary = ROOT / "reports" / "score_driver_summary.md"
        self.assertTrue(summary.exists())
        text = summary.read_text(encoding="utf-8")
        self.assertIn("# Score Driver Summary", text)
        self.assertIn("results/score_driver_summary.csv", text)
        self.assertIn("Highest-Spread Criteria", text)

    def test_scenario_playbooks_exist(self):
        playbooks = ROOT / "reports" / "scenario_playbooks.md"
        self.assertTrue(playbooks.exists())
        text = playbooks.read_text(encoding="utf-8")
        self.assertIn("# Scenario Playbooks", text)
        self.assertIn("results/scenario_playbook_summary.csv", text)
        self.assertIn("No-go condition", text)

    def test_recommendation_rationale_exists(self):
        rationale = ROOT / "reports" / "recommendation_rationale.md"
        self.assertTrue(rationale.exists())
        text = rationale.read_text(encoding="utf-8")
        self.assertIn("# Recommendation Rationale", text)
        self.assertIn("results/recommendation_rationale.csv", text)
        self.assertIn("Scenario Rationale", text)

    def test_risk_validation_matrix_exists(self):
        matrix = ROOT / "reports" / "risk_validation_matrix.md"
        self.assertTrue(matrix.exists())
        text = matrix.read_text(encoding="utf-8")
        self.assertIn("# Risk Validation Matrix", text)
        self.assertIn("results/risk_validation_matrix.csv", text)
        self.assertIn("Pass condition", text)

    def test_pilot_sample_size_exists(self):
        sample_size = ROOT / "reports" / "pilot_sample_size.md"
        self.assertTrue(sample_size.exists())
        text = sample_size.read_text(encoding="utf-8")
        self.assertIn("# Pilot Sample Size Estimate", text)
        self.assertIn("results/pilot_sample_size_estimates.csv", text)
        self.assertIn("Recommended Task Counts", text)

    def test_maintenance_guide_exists(self):
        guide = ROOT / "reports" / "maintenance_guide.md"
        self.assertTrue(guide.exists())
        text = guide.read_text(encoding="utf-8")
        self.assertIn("# Maintenance Guide", text)
        self.assertIn("Standard Refresh Procedure", text)
        self.assertIn("python scripts/run_all_checks.py", text)

    def test_residual_risks_exists(self):
        risks = ROOT / "reports" / "residual_risks.md"
        self.assertTrue(risks.exists())
        text = risks.read_text(encoding="utf-8")
        self.assertIn("# Residual Risks", text)
        self.assertIn("Simulated rankings may not predict live task success", text)
        self.assertIn("security fixtures", text)

    def test_presentation_outline_exists(self):
        outline = ROOT / "reports" / "presentation_outline.md"
        self.assertTrue(outline.exists())
        text = outline.read_text(encoding="utf-8")
        self.assertIn("# Presentation Outline", text)
        self.assertIn("No-Go Conditions", text)
        self.assertIn("Ask From Stakeholders", text)

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
            "scenario_playbook_summary.csv",
            "score_driver_summary.csv",
            "criterion_spread_summary.csv",
            "implementation_effort_estimates.csv",
            "operational_cost_estimates.csv",
            "operational_fit_rankings.csv",
            "pilot_sample_size_estimates.csv",
            "evidence_gap_analysis.csv",
            "recommendation_rationale.csv",
            "risk_validation_matrix.csv",
            "custom_weights_example_rankings.csv",
            "local_artifact_reference_check.csv",
            "markdown_table_check.csv",
            "github_metadata_check.csv",
            "csv_schema_check.csv",
            "artifact_manifest.csv",
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
            "security_gate_checklist.md",
            "scenario_selection_workshop.md"
        ]
        for filename in expected_files:
            path = ROOT / "templates" / filename
            self.assertTrue(path.exists(), f"missing template file: {path}")
            self.assertGreater(path.stat().st_size, 0)

    def test_examples_exist(self):
        expected_files = [
            "pilot_candidate_summary.example.csv",
            "custom_weights.example.json",
            "pilot_adapter_contract.py",
        ]
        for filename in expected_files:
            example = ROOT / "examples" / filename
            self.assertTrue(example.exists())
            self.assertGreater(example.stat().st_size, 0)

    def test_generated_svg_assets_exist(self):
        expected_files = [
            "rank_stability.svg",
            "scenario_regret.svg",
            "operational_hours.svg",
            "criterion_spread.svg"
        ]
        for filename in expected_files:
            path = ROOT / "reports" / "assets" / filename
            self.assertTrue(path.exists(), f"missing SVG asset: {path}")
            text = path.read_text(encoding="utf-8")
            self.assertIn("<svg", text)
            self.assertIn("</svg>", text)

    def test_powershell_runner_exists(self):
        runner = ROOT / "scripts" / "run_all_checks.ps1"
        self.assertTrue(runner.exists())
        text = runner.read_text(encoding="utf-8")
        self.assertIn("run_all_checks.py", text)
        self.assertIn("$ErrorActionPreference", text)


if __name__ == "__main__":
    unittest.main()
