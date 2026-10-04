import copy
import importlib.util
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("jev_grader", Path(__file__).parents[1] / "scripts/grade_with_jev.py")
jev = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(jev)


class JevGraderTests(unittest.TestCase):
    def setUp(self):
        self.grading = {"prompt": "Source facts", "run": "with_skill", "grader": "old",
                        "assertion_results": [{"text": "No invented facts", "passed": True}]}
        self.request = jev.make_request(self.grading, "Candidate answer", "jev-latest")
        self.response = {"model": "jev-test", "answers": {"a1": {"type": "choice", "choice": "uncertain",
                         "probabilities": {"pass": 0.2, "fail": 0.3, "uncertain": 0.5}, "confidence": 0.25}}}

    def test_input_is_blind_and_preserves_source(self):
        self.assertEqual(self.request["state"], {"task": "Source facts", "answer": "Candidate answer"})
        self.assertNotIn("with_skill", str(self.request))
        self.assertNotIn("passed", str(self.request))
        self.assertEqual(len(self.request["questions"]), 1)

    def test_uncertainty_is_valid(self):
        jev.validate_response(self.response, self.request)

    def test_missing_assertion_is_rejected(self):
        bad = copy.deepcopy(self.response)
        bad["answers"] = {}
        with self.assertRaises(ValueError):
            jev.validate_response(bad, self.request)

    def test_malformed_probabilities_are_rejected(self):
        for value in (True, float("nan"), 1.3):
            bad = copy.deepcopy(self.response)
            bad["answers"]["a1"]["probabilities"]["pass"] = value
            with self.assertRaises(ValueError):
                jev.validate_response(bad, self.request)


if __name__ == "__main__":
    unittest.main()
