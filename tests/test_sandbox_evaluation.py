import unittest

from scripts.simulate_sandboxes import (
    deterministic_rankings,
    load_data,
    managed_dependency_risk,
    monte_carlo_rankings,
    threat_coverage_rows,
)


class SandboxEvaluationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_data()

    def test_dataset_has_expected_shape(self):
        self.assertEqual(len(self.data["scenarios"]), 5)
        self.assertEqual(len(self.data["threats"]), 5)
        self.assertGreaterEqual(len(self.data["sandboxes"]), 15)
        for sandbox in self.data["sandboxes"]:
            self.assertTrue(sandbox["source_urls"])
            self.assertEqual(set(sandbox["scores"]), set(self.data["criteria"]))

    def test_enterprise_self_hosted_penalizes_managed_services(self):
        daytona = next(item for item in self.data["sandboxes"] if item["id"] == "daytona")
        firecracker = next(
            item for item in self.data["sandboxes"] if item["id"] == "firecracker_microvm"
        )
        self.assertGreater(managed_dependency_risk(daytona), managed_dependency_risk(firecracker))

        rankings = deterministic_rankings(self.data)
        top_three = [
            row["sandbox_id"]
            for row in rankings["enterprise_self_hosted"][:3]
        ]
        self.assertIn("kubernetes_hardened_pods", top_three)
        self.assertIn("firecracker_microvm", top_three)

    def test_monte_carlo_rates_are_valid(self):
        rows_by_scenario = monte_carlo_rankings(self.data, trials=25, seed=1234)
        for rows in rows_by_scenario.values():
            for row in rows:
                self.assertGreaterEqual(row["win_rate"], 0)
                self.assertLessEqual(row["win_rate"], 1)
                self.assertGreaterEqual(row["top3_rate"], 0)
                self.assertLessEqual(row["top3_rate"], 1)

    def test_threat_coverage_covers_every_sandbox(self):
        rows = threat_coverage_rows(self.data)
        self.assertEqual(
            len(rows),
            len(self.data["sandboxes"]) * len(self.data["threats"]),
        )
        self.assertTrue({row["coverage_band"] for row in rows} <= {
            "strong",
            "adequate",
            "partial",
            "weak",
        })


if __name__ == "__main__":
    unittest.main()
