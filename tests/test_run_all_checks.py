import unittest

from scripts.run_all_checks import COMMANDS


class RunAllChecksTest(unittest.TestCase):
    def test_runner_includes_required_steps(self):
        joined = [" ".join(command) for command in COMMANDS]
        required_fragments = [
            "unittest discover",
            "simulate_alternatives.py",
            "stress_test_simulation.py",
            "analyze_score_drivers.py",
            "build_scenario_playbooks.py",
            "estimate_implementation_effort.py",
            "estimate_operational_costs.py",
            "estimate_pilot_sample_sizes.py",
            "analyze_evidence_gaps.py",
            "build_risk_validation_matrix.py",
            "rank_with_custom_weights.py",
            "license_audit.py",
            "generate_charts.py",
            "build_results_data_dictionary.py",
            "build_report_bundle.py",
            "check_local_artifact_references.py",
            "validate_markdown_tables.py",
            "generate_artifact_manifest.py",
            "validate_csv_schemas.py",
            "score_pilot_results.py",
            "validate_artifacts.py"
        ]
        for fragment in required_fragments:
            self.assertTrue(any(fragment in command for command in joined), fragment)


if __name__ == "__main__":
    unittest.main()
