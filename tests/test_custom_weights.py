import json
import tempfile
from pathlib import Path
import unittest

from scripts.rank_with_custom_weights import (
    DEFAULT_WEIGHTS,
    custom_ranking_rows,
    load_custom_scenarios,
)
from scripts.simulate_alternatives import CRITERIA, DEFAULT_DATA, load_data


class CustomWeightsTest(unittest.TestCase):
    def test_example_weights_are_valid(self):
        scenarios = load_custom_scenarios(DEFAULT_WEIGHTS)
        self.assertEqual(set(scenarios), {"security_first_custom", "fast_local_custom"})
        for weights in scenarios.values():
            self.assertEqual(set(weights), set(CRITERIA))
            self.assertGreater(sum(weights.values()), 0)

    def test_custom_rankings_cover_all_alternatives(self):
        _raw, alternatives = load_data()
        rows = custom_ranking_rows(DEFAULT_DATA, DEFAULT_WEIGHTS)
        self.assertEqual(len(rows), len(alternatives) * 2)
        for scenario in {"security_first_custom", "fast_local_custom"}:
            scenario_rows = [row for row in rows if row["scenario"] == scenario]
            self.assertEqual(
                [row["rank"] for row in scenario_rows],
                list(range(1, len(alternatives) + 1)),
            )

    def test_missing_weight_is_rejected(self):
        weights = {
            criterion: 1.0
            for criterion in CRITERIA
            if criterion != "implementation_ease"
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "weights.json"
            path.write_text(
                json.dumps({"scenarios": {"broken": weights}}),
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                load_custom_scenarios(path)


if __name__ == "__main__":
    unittest.main()
