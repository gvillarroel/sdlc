import csv
import json
from pathlib import Path
import tempfile
import unittest

from scripts.score_pilot_results import load_model, read_input, score_rows, write_output


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "data" / "pilot_decision_model.json"


class PilotDecisionModelTest(unittest.TestCase):
    def test_model_weights_sum_to_one(self):
        model = json.loads(MODEL.read_text(encoding="utf-8"))
        self.assertAlmostEqual(sum(model["weights"].values()), 1.0)
        for value in model["gates"].values():
            self.assertGreaterEqual(value, 0)

    def test_scoring_ranks_eligible_candidate_first(self):
        model = load_model(MODEL)
        rows = [
            {
                "candidate": "Safe Candidate",
                "attempted_tasks": "20",
                "successful_tasks": "17",
                "reviewed_diffs": "17",
                "accepted_diffs": "15",
                "safety_failures": "0",
                "artifact_complete_runs": "19",
                "cost_latency_score": "0.8",
                "setup_maintenance_score": "0.7",
                "notes": ""
            },
            {
                "candidate": "Unsafe Candidate",
                "attempted_tasks": "20",
                "successful_tasks": "20",
                "reviewed_diffs": "20",
                "accepted_diffs": "20",
                "safety_failures": "1",
                "artifact_complete_runs": "20",
                "cost_latency_score": "1.0",
                "setup_maintenance_score": "1.0",
                "notes": ""
            }
        ]
        scored = score_rows(rows, model)
        self.assertEqual(scored[0]["candidate"], "Safe Candidate")
        self.assertTrue(scored[0]["eligible"])
        self.assertFalse(scored[1]["eligible"])
        self.assertIn("safety_failures", scored[1]["gate_failures"])

    def test_write_output_round_trips_csv(self):
        model = load_model(MODEL)
        rows = score_rows([
            {
                "candidate": "Candidate",
                "attempted_tasks": "10",
                "successful_tasks": "8",
                "reviewed_diffs": "8",
                "accepted_diffs": "7",
                "safety_failures": "0",
                "artifact_complete_runs": "9",
                "cost_latency_score": "0.6",
                "setup_maintenance_score": "0.7",
                "notes": "ok"
            }
        ], model)
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "scores.csv"
            write_output(output, rows)
            with output.open("r", encoding="utf-8", newline="") as handle:
                loaded = list(csv.DictReader(handle))
            self.assertEqual(loaded[0]["candidate"], "Candidate")
            self.assertEqual(loaded[0]["rank"], "1")


if __name__ == "__main__":
    unittest.main()
