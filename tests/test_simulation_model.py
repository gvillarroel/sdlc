import unittest

from scripts.simulate_alternatives import (
    CATEGORY_GROUPS,
    CRITERIA,
    PERMISSIVE_LICENSES,
    SCENARIOS,
    category_scores,
    alternative_scorecard_rows,
    criteria_definition_rows,
    decision_shortlist,
    deterministic_rankings,
    pareto_frontier_rows,
    evidence_matrix_rows,
    load_data,
    rank_stability_rows,
    regret_analysis_rows,
    run_monte_carlo,
    scenario_weights_rows,
    validate_data,
    weighted_score
)


class SimulationModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw, cls.alternatives = load_data()

    def test_dataset_is_valid_and_permissive(self):
        validate_data(self.alternatives)
        self.assertGreaterEqual(len(self.alternatives), 10)
        for alternative in self.alternatives:
            self.assertIn(alternative.license, PERMISSIVE_LICENSES)

    def test_scores_cover_all_criteria_and_range(self):
        for alternative in self.alternatives:
            self.assertEqual(set(alternative.scores), set(CRITERIA))
            for score in alternative.scores.values():
                self.assertGreaterEqual(score, 0)
                self.assertLessEqual(score, 5)

    def test_weighted_score_bounds(self):
        weights = {criterion: 1.0 for criterion in CRITERIA}
        for alternative in self.alternatives:
            score = weighted_score(alternative.scores, weights)
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 5)

    def test_deterministic_rankings_are_sorted(self):
        rankings = deterministic_rankings(self.alternatives)
        self.assertEqual(set(rankings), set(SCENARIOS))
        for rows in rankings.values():
            scores = [row["score"] for row in rows]
            self.assertEqual(scores, sorted(scores, reverse=True))
            self.assertEqual([row["rank"] for row in rows], list(range(1, len(rows) + 1)))

    def test_monte_carlo_is_reproducible_for_fixed_seed(self):
        first = run_monte_carlo(self.alternatives, trials=50, seed=123)
        second = run_monte_carlo(self.alternatives, trials=50, seed=123)
        self.assertEqual(first, second)
        for rows in first.values():
            for row in rows:
                self.assertGreaterEqual(row["win_rate"], 0)
                self.assertLessEqual(row["win_rate"], 1)
                self.assertGreaterEqual(row["top3_rate"], 0)
                self.assertLessEqual(row["top3_rate"], 1)

    def test_monte_carlo_rejects_invalid_uncertainty_multiplier(self):
        with self.assertRaises(ValueError):
            run_monte_carlo(
                self.alternatives,
                trials=1,
                seed=123,
                score_sigma_multiplier=-0.1
            )

    def test_category_scores_are_ranked_and_bounded(self):
        rows = category_scores(self.alternatives)
        self.assertEqual(
            len(rows),
            len(self.alternatives) * len(CATEGORY_GROUPS)
        )
        for category in CATEGORY_GROUPS:
            category_rows = [row for row in rows if row["category"] == category]
            self.assertEqual(
                [row["rank"] for row in category_rows],
                list(range(1, len(self.alternatives) + 1))
            )
            scores = [row["score"] for row in category_rows]
            self.assertEqual(scores, sorted(scores, reverse=True))
            for score in scores:
                self.assertGreaterEqual(score, 0)
                self.assertLessEqual(score, 5)

    def test_decision_shortlist_combines_deterministic_and_monte_carlo(self):
        deterministic = deterministic_rankings(self.alternatives)
        monte_carlo = run_monte_carlo(self.alternatives, trials=50, seed=321)
        rows = decision_shortlist(deterministic, monte_carlo, top_n=3)
        self.assertEqual(len(rows), len(SCENARIOS) * 3)
        for row in rows:
            self.assertIn(row["scenario"], SCENARIOS)
            self.assertGreaterEqual(row["deterministic_score"], 0)
            self.assertLessEqual(row["deterministic_score"], 5)
            self.assertGreaterEqual(row["top3_rate"], 0)
            self.assertLessEqual(row["top3_rate"], 1)

    def test_audit_rows_cover_model_inputs(self):
        criteria_rows = criteria_definition_rows(self.raw)
        self.assertEqual([row["criterion"] for row in criteria_rows], CRITERIA)

        weight_rows = scenario_weights_rows()
        self.assertEqual(len(weight_rows), len(SCENARIOS) * len(CRITERIA))
        for scenario in SCENARIOS:
            normalized_sum = sum(
                row["normalized_weight"]
                for row in weight_rows
                if row["scenario"] == scenario
            )
            self.assertAlmostEqual(normalized_sum, 1.0)

        evidence_rows = evidence_matrix_rows(self.raw)
        self.assertEqual(len(evidence_rows), len(self.alternatives))
        for row in evidence_rows:
            self.assertIn(row["license"], PERMISSIVE_LICENSES)
            self.assertTrue(row["evidence_urls"])

        scorecard_rows = alternative_scorecard_rows(self.alternatives)
        self.assertEqual(len(scorecard_rows), len(self.alternatives))
        for row in scorecard_rows:
            for criterion in CRITERIA:
                self.assertIn(criterion, row)

    def test_robustness_rows_are_consistent(self):
        deterministic = deterministic_rankings(self.alternatives)
        monte_carlo = run_monte_carlo(self.alternatives, trials=50, seed=456)
        regret_rows = regret_analysis_rows(deterministic, monte_carlo)
        self.assertEqual(len(regret_rows), len(SCENARIOS) * len(self.alternatives))
        for scenario in SCENARIOS:
            scenario_regrets = [
                row["regret_vs_best"]
                for row in regret_rows
                if row["scenario"] == scenario
            ]
            self.assertEqual(min(scenario_regrets), 0)
            for regret in scenario_regrets:
                self.assertGreaterEqual(regret, 0)

        pareto_rows = pareto_frontier_rows(self.alternatives)
        self.assertEqual(len(pareto_rows), len(self.alternatives))
        self.assertTrue(any(row["is_pareto_frontier"] for row in pareto_rows))

        stability_rows = rank_stability_rows(deterministic, monte_carlo)
        self.assertEqual(len(stability_rows), len(self.alternatives))
        for row in stability_rows:
            self.assertGreaterEqual(row["top3_scenario_rate"], 0)
            self.assertLessEqual(row["top3_scenario_rate"], 1)


if __name__ == "__main__":
    unittest.main()
