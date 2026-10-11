import copy
import importlib.util
import io
import json
import os
import tempfile
from unittest.mock import patch
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


class JevReportBoundaryTests(unittest.TestCase):
    """Exercise the real HTTP-to-report boundary without a paid provider call."""

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.path = self.root / "grading.json"
        self.grading = {"prompt": "Source: keep the limit of 10.", "assertion_results": [
            {"text": "Preserves 10", "passed": None},
            {"text": "No invented defaults", "passed": None},
            {"text": "States uncertainty", "passed": None},
        ]}
        self.path.write_text(json.dumps(self.grading))
        (self.root / "outputs").mkdir()
        (self.root / "outputs/answer.md").write_text("Limit: 10. Default unknown.")
        self.response = {"model": "jev-test", "usage": {"input_tokens": 12}, "answers": {}}
        for index, choice in enumerate(("pass", "fail", "uncertain"), 1):
            self.response["answers"][f"a{index}"] = {
                "type": "choice", "choice": choice, "confidence": 0.8,
                "probabilities": {label: 0.8 if label == choice else 0.1
                                  for label in ("pass", "fail", "uncertain")},
            }

    def grade(self, force=False):
        with patch.dict(os.environ, {"TYPESAFE_API_KEY": "offline-test"}), patch.object(
            jev.urllib.request, "urlopen", return_value=io.StringIO(json.dumps(self.response))
        ):
            destination = jev.grade(self.path, model="jev-latest", timeout=1, force=force)
        return json.loads(destination.read_text())

    def assert_normalized(self, report):
        rows = report["assertion_results"]
        self.assertEqual([row["index"] for row in rows], [1, 2, 3])
        self.assertEqual([row["text"] for row in rows],
                         [row["text"] for row in self.grading["assertion_results"]])
        self.assertEqual([row["passed"] for row in rows], [True, False, None])
        self.assertEqual(report["summary"], {"passed": 1, "failed": 1, "unresolved": 1, "total": 3})

    def test_response_cannot_override_normalized_identity_or_verdict(self):
        for result in self.response["answers"].values():
            result.update(index=99, text="Different assertion", passed=True)
        self.assert_normalized(self.grade())

    def test_additional_provider_metadata_is_preserved(self):
        for result in self.response["answers"].values():
            result["provider_metadata"] = {"version": 2}
        report = self.grade()
        self.assert_normalized(report)
        for result in report["assertion_results"]:
            self.assertEqual(result["provider_metadata"], {"version": 2})

    def test_nonboolean_verdict_extras_cannot_break_summary_accounting(self):
        for supplied in ("yes", 1, [], {}, None):
            with self.subTest(supplied=supplied):
                for result in self.response["answers"].values():
                    result["passed"] = supplied
                self.assert_normalized(self.grade(force=True))

    def test_choice_metadata_and_usage_are_preserved(self):
        report = self.grade()
        self.assert_normalized(report)
        for index, result in enumerate(report["assertion_results"], 1):
            for key, value in self.response["answers"][f"a{index}"].items():
                self.assertEqual(result[key], value)
        self.assertEqual(report["usage"], self.response["usage"])
        self.assertEqual(report["grader"]["model"], "jev-test")
        self.assertEqual(json.loads(self.path.read_text()), self.grading)

    def test_reordered_answers_still_follow_request_order(self):
        self.response["answers"] = dict(reversed(list(self.response["answers"].items())))
        self.assert_normalized(self.grade())

    def test_invalid_choices_are_validation_errors_and_preserve_previous_report(self):
        destination = self.root / "grading.jev.json"
        destination.write_text("previous report")
        for choice in ([], {}, None, True, 0, "unknown"):
            with self.subTest(choice=choice):
                self.response["answers"]["a1"]["choice"] = choice
                with self.assertRaisesRegex(ValueError, "invalid Jev choice"):
                    self.grade(force=True)
                self.assertEqual(destination.read_text(), "previous report")

    def test_missing_or_extra_answers_do_not_publish_a_report(self):
        for answers in ({}, {**self.response["answers"], "extra": self.response["answers"]["a1"]}):
            with self.subTest(answers=list(answers)):
                self.response["answers"] = answers
                with self.assertRaisesRegex(ValueError, "exactly"):
                    self.grade()
                self.assertFalse((self.root / "grading.jev.json").exists())


if __name__ == "__main__":
    unittest.main()
