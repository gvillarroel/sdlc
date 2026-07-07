from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PagesSiteTest(unittest.TestCase):
    def test_pages_site_contains_final_report_sections_and_assets(self):
        site = ROOT / "docs" / "index.html"
        self.assertTrue(site.exists())
        text = site.read_text(encoding="utf-8")

        for marker in [
            "Final global report",
            "Global View",
            "Visual Evidence Map",
            "Rendered Diagrams",
            "Methodology",
            "Scenario Findings",
            "Security And Sandboxing",
            "Recommended Pilot Plan",
            "Download The Data",
            "Complete Data And Results Index",
            "Complete report library",
            "Source Artifacts",
        ]:
            self.assertIn(marker, text)

        for asset in [
            "final-report-evidence-pipeline.svg",
            "final-report-decision-lanes.svg",
            "final-report-artifact-coverage.svg",
            "rank_stability.svg",
            "scenario_regret.svg",
            "operational_hours.svg",
            "criterion_spread.svg",
        ]:
            self.assertIn(f"assets/{asset}", text)
            asset_path = ROOT / "docs" / "assets" / asset
            self.assertTrue(asset_path.exists())
            self.assertIn("<svg", asset_path.read_text(encoding="utf-8"))

    def test_pages_source_has_nojekyll_marker(self):
        self.assertTrue((ROOT / "docs" / ".nojekyll").exists())

    def test_pages_site_links_to_raw_downloads(self):
        text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

        self.assertIn('lang="en"', text)
        self.assertNotIn("Reporte final global", text)
        self.assertNotIn("Vista global", text)

        for path in [
            "data/alternatives.json",
            "data/candidate_taxonomy.json",
            "data/decision_tree.json",
            "data/operational_cost_model.json",
            "data/pilot_decision_model.json",
            "data/pilot_sample_size_model.json",
            "data/scoring_rubric.json",
            "data/scenario_profiles.json",
            "data/sandbox_evaluation.json",
            "data/pilot_tasks.json",
            "data/risk_register.json",
            "data/security_evaluation_fixtures.json",
            "data/simulation_assumptions.json",
            "data/traceability_matrix.json",
            "results/all_results.json",
            "results/alternative_scorecards.csv",
            "results/artifact_manifest.csv",
            "results/category_scores.csv",
            "results/criteria_definitions.csv",
            "results/criterion_spread_summary.csv",
            "results/csv_schema_check.csv",
            "results/custom_weights_example_rankings.csv",
            "results/decision_shortlist.csv",
            "results/deterministic_rankings.csv",
            "results/evidence_gap_analysis.csv",
            "results/evidence_matrix.csv",
            "results/github_metadata_check.csv",
            "results/implementation_effort_estimates.csv",
            "results/license_audit.csv",
            "results/local_artifact_reference_check.csv",
            "results/markdown_table_check.csv",
            "results/market_maintenance_source_matrix.csv",
            "results/monte_carlo_summary.csv",
            "results/operational_cost_estimates.csv",
            "results/operational_fit_rankings.csv",
            "results/pareto_frontier.csv",
            "results/pilot_decision_scores.example.csv",
            "results/pilot_sample_size_estimates.csv",
            "results/rank_stability.csv",
            "results/recommendation_rationale.csv",
            "results/regret_analysis.csv",
            "results/sandbox_decision_matrix.csv",
            "results/sandbox_deterministic_rankings.csv",
            "results/sandbox_monte_carlo_summary.csv",
            "results/sandbox_source_matrix.csv",
            "results/sandbox_threat_coverage.csv",
            "results/scenario_playbook_summary.csv",
            "results/scenario_weights.csv",
            "results/score_driver_summary.csv",
            "results/sensitivity_summary.csv",
            "results/source_check.csv",
            "results/stress_test_rankings.csv",
            "results/stress_test_summary.csv",
            "results/uncertainty_stress_details.csv",
            "results/uncertainty_stress_summary.csv",
            "results/risk_validation_matrix.csv",
        ]:
            self.assertIn(f"https://raw.githubusercontent.com/gvillarroel/sdlc/main/{path}", text)


if __name__ == "__main__":
    unittest.main()
