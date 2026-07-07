from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PagesSiteTest(unittest.TestCase):
    def test_pages_site_contains_final_report_sections_and_assets(self):
        site = ROOT / "docs" / "index.html"
        self.assertTrue(site.exists())
        text = site.read_text(encoding="utf-8")

        for marker in [
            "Reporte final global",
            "Vista global",
            "Metodologia",
            "Hallazgos por escenario",
            "Seguridad y sandboxing",
            "Plan de piloto recomendado",
            "Artefactos fuente",
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


if __name__ == "__main__":
    unittest.main()
