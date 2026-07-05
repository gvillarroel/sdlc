import json
from pathlib import Path
import unittest

from scripts.simulate_alternatives import CRITERIA


ROOT = Path(__file__).resolve().parents[1]
RUBRIC = ROOT / "data" / "scoring_rubric.json"


class ScoringRubricTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(RUBRIC.read_text(encoding="utf-8"))

    def test_rubric_covers_all_model_criteria(self):
        self.assertEqual(set(self.data["criteria"]), set(CRITERIA))

    def test_each_criterion_has_low_mid_high_anchors(self):
        for criterion, anchors in self.data["criteria"].items():
            for anchor in ("0", "3", "5"):
                self.assertIn(anchor, anchors, criterion)
                self.assertTrue(anchors[anchor])

    def test_global_scale_is_complete(self):
        self.assertEqual(set(self.data["scale"]), {"0", "1", "2", "3", "4", "5"})


if __name__ == "__main__":
    unittest.main()
