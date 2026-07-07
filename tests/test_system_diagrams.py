from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SystemDiagramsTest(unittest.TestCase):
    def test_system_diagrams_cover_all_scripts_and_core_artifacts(self):
        text = (ROOT / "reports" / "system_diagrams.md").read_text(encoding="utf-8")

        self.assertIn("# System Diagrams", text)
        self.assertIn("```mermaid", text)

        for script in sorted((ROOT / "scripts").glob("*")):
            if script.suffix in {".py", ".ps1"}:
                self.assertIn(f"`scripts/{script.name}`", text)

        for path in [
            "data/alternatives.json",
            "data/scoring_rubric.json",
            "data/scenario_profiles.json",
            "data/sandbox_evaluation.json",
            "data/risk_register.json",
            "results/all_results.json",
            "reports/artifact_index.md",
            "reports/final_report_bundle.md",
            "templates/pilot_run_log.csv",
            "examples/custom_weights.example.json",
            "ci/validate-workflow.example.yml",
        ]:
            self.assertIn(path, text)


if __name__ == "__main__":
    unittest.main()
