import unittest

from scripts.run_all_checks import COMMANDS


class RunAllChecksTest(unittest.TestCase):
    def test_runner_includes_required_steps(self):
        joined = [" ".join(command) for command in COMMANDS]
        required_fragments = [
            "unittest discover",
            "simulate_alternatives.py",
            "stress_test_simulation.py",
            "estimate_implementation_effort.py",
            "analyze_evidence_gaps.py",
            "rank_with_custom_weights.py",
            "license_audit.py",
            "generate_charts.py",
            "check_local_artifact_references.py",
            "score_pilot_results.py",
            "validate_artifacts.py"
        ]
        for fragment in required_fragments:
            self.assertTrue(any(fragment in command for command in joined), fragment)


if __name__ == "__main__":
    unittest.main()
