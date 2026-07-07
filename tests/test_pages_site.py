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
            "Methodology",
            "Scenario Findings",
            "Security And Sandboxing",
            "Recommended Pilot Plan",
            "Download The Data",
            "Source Artifacts",
        ]:
            self.assertIn(marker, text)

        for asset in [
            "rank_stability.svg",
            "scenario_regret.svg",
            "operational_hours.svg",
            "criterion_spread.svg",
        ]:
            self.assertIn(f"assets/{asset}", text)
            self.assertTrue((ROOT / "docs" / "assets" / asset).exists())

    def test_pages_source_has_nojekyll_marker(self):
        self.assertTrue((ROOT / "docs" / ".nojekyll").exists())

    def test_pages_site_links_to_raw_downloads(self):
        text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

        self.assertIn('lang="en"', text)
        self.assertNotIn("Reporte final global", text)
        self.assertNotIn("Vista global", text)

        for path in [
            "data/alternatives.json",
            "data/scoring_rubric.json",
            "data/scenario_profiles.json",
            "data/sandbox_evaluation.json",
            "data/pilot_tasks.json",
            "data/risk_register.json",
            "results/all_results.json",
            "results/decision_shortlist.csv",
            "results/deterministic_rankings.csv",
            "results/monte_carlo_summary.csv",
            "results/sandbox_decision_matrix.csv",
            "results/risk_validation_matrix.csv",
        ]:
            self.assertIn(f"https://raw.githubusercontent.com/gvillarroel/sdlc/main/{path}", text)


if __name__ == "__main__":
    unittest.main()
