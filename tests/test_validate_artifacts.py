import unittest

from scripts.validate_artifacts import validate_all


class ValidateArtifactsTest(unittest.TestCase):
    def test_generated_artifacts_validate(self):
        validate_all()


if __name__ == "__main__":
    unittest.main()
