"""Offline regressions for the writing-pass report's saved-evidence boundary."""

import contextlib
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import eval_writing_passes as pilot


class WritingPassReportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.directory = self.workspace / "case/sample-1/single_pass"
        self.case = {"id": "case", "skill": "task", "split": "transfer",
                     "prompt": "Source: the command requires --safe.",
                     "assertions": ["Includes --safe", "Preserves the source limitation", "Gives a command"]}
        self.manifest = {"cases": [self.case], "samples": 1, "arms": ["single_pass"],
                         "grader": {"executor": "pi", "model": "test-model"}}
        self.answer = "Run tool --safe. The source does not specify its default."
        pilot.publish(self.directory, self.answer, "draft_only")
        self.grading = {"prompt": self.case["prompt"], "answer_sha256": pilot.digest(self.answer),
                        "assertion_results": [{"index": i, "text": text, "passed": verdict}
                                              for i, (text, verdict) in enumerate(
                                                  zip(self.case["assertions"], [True, None, False]), 1)]}
        self.write_grade()

    def write_grade(self):
        suffix = "grading.jev.json" if self.manifest["grader"]["executor"] == "jev" else "grading.json"
        pilot.save_json(self.directory / suffix, self.grading)

    def run_report(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return pilot.report(self.workspace, self.manifest)

    def assert_rejected(self, message):
        with self.assertRaisesRegex((ValueError, OSError), message):
            self.run_report()
        self.assertFalse((self.workspace / "results.json").exists())

    def use_jev(self):
        self.manifest["grader"] = {"executor": "jev", "model": "jev-test"}
        request = pilot.jev.make_request(self.grading, self.answer, "jev-test")
        self.grading.pop("prompt")
        self.grading["grader"] = {"requested_model": "jev-test"}
        self.grading["request"] = request
        self.grading["request_sha256"] = pilot.digest(json.dumps(request))
        self.write_grade()

    def test_valid_verdicts_and_workflow_status_are_separate(self):
        result = self.run_report()
        self.assertEqual(result["totals"]["single_pass"],
                         {"passed": 1, "failed": 1, "unresolved": 1, "missing": 0, "planned": 3})
        self.assertEqual(result["rows"][0]["workflow_status"], "draft_only")

    def test_jev_valid_verdicts_preserve_uncertainty(self):
        self.use_jev()
        self.assertEqual(self.run_report()["totals"]["single_pass"]["unresolved"], 1)

    def test_modified_final_answer_is_rejected(self):
        (self.directory / "outputs/answer.md").write_text("Unsafe changed answer")
        self.assert_rejected("saved final answer changed")

    def test_grade_for_another_answer_is_rejected_even_with_current_workflow(self):
        self.grading["answer_sha256"] = pilot.digest("Another answer")
        self.write_grade()
        self.assert_rejected("stale answer grading")

    def test_missing_answer_is_rejected(self):
        (self.directory / "outputs/answer.md").unlink()
        self.assert_rejected("answer.md")

    def test_grade_without_workflow_is_rejected(self):
        (self.directory / "workflow.json").unlink()
        self.assert_rejected("no saved workflow")

    def test_stale_task_is_rejected(self):
        self.case["prompt"] = "A different task"
        self.assert_rejected("stale task grading")

    def test_changed_assertion_is_rejected(self):
        self.case["assertions"][0] = "Includes --unsafe"
        self.assert_rejected("stale assertion text")

    def test_duplicate_assertion_does_not_inflate_pass_count(self):
        self.grading["assertion_results"].append(copy.deepcopy(self.grading["assertion_results"][0]))
        self.write_grade()
        self.assert_rejected("duplicate assertion index")

    def test_invalid_indices_are_rejected(self):
        for index in (0, 4, -1, True, 1.0, "1", None):
            with self.subTest(index=index):
                self.grading["assertion_results"][0]["index"] = index
                self.write_grade()
                self.assert_rejected("assertion index")

    def test_non_boolean_verdicts_are_rejected(self):
        for verdict in (1, 0, "true", "false", [], {}):
            with self.subTest(verdict=verdict):
                self.grading["assertion_results"][0]["passed"] = verdict
                self.write_grade()
                self.assert_rejected("assertion verdict")

    def test_missing_verdict_is_not_uncertain(self):
        del self.grading["assertion_results"][0]["passed"]
        self.write_grade()
        self.assert_rejected("assertion verdict")

    def test_reordered_results_are_aligned_to_assertion_order(self):
        self.grading["assertion_results"].reverse()
        self.write_grade()
        self.assertEqual(self.run_report()["rows"][0]["verdicts"], [True, None, False])

    def test_partial_valid_grades_remain_in_planned_denominator(self):
        self.grading["assertion_results"] = self.grading["assertion_results"][:1]
        self.write_grade()
        self.assertEqual(self.run_report()["totals"]["single_pass"],
                         {"passed": 1, "failed": 0, "unresolved": 0, "missing": 2, "planned": 3})

    def test_ungraded_answer_remains_missing_without_losing_workflow_status(self):
        (self.directory / "grading.json").unlink()
        row = self.run_report()["rows"][0]
        self.assertEqual((row["workflow_status"], row["missing"]), ("draft_only", 3))

    def test_unexecuted_case_remains_missing(self):
        self.manifest["samples"] = 2
        result = self.run_report()
        self.assertEqual(result["totals"]["single_pass"]["planned"], 6)
        self.assertEqual(result["totals"]["single_pass"]["missing"], 3)
        self.assertEqual(result["rows"][1]["workflow_status"], "missing")

    def test_jev_changed_task_answer_or_model_is_rejected(self):
        self.use_jev()
        original = copy.deepcopy(self.grading)
        for field in ("task", "answer", "model"):
            with self.subTest(field=field):
                self.grading = copy.deepcopy(original)
                if field == "model":
                    self.grading["grader"]["requested_model"] = "other-model"
                else:
                    self.grading["request"]["state"][field] = "Changed"
                self.write_grade()
                self.assert_rejected("stale Jev grading")

    def test_jev_request_consistency_is_verified(self):
        self.use_jev()
        original = copy.deepcopy(self.grading)
        mutations = {
            "model": lambda g: g["request"].update(model="other-model"),
            "assertion": lambda g: g["request"]["questions"]["a1"]["instructions"].update(assertion="Different"),
            "missing_question": lambda g: g["request"]["questions"].pop("a1"),
            "extra_question": lambda g: g["request"]["questions"].update(a4={}),
            "invalid_question": lambda g: g["request"]["questions"].update(a1=None),
            "invalid_instructions": lambda g: g["request"]["questions"]["a1"].update(instructions=[]),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                self.grading = copy.deepcopy(original)
                mutate(self.grading)
                # A coherent checksum alone must not hide a contradictory request.
                self.grading["request_sha256"] = pilot.digest(json.dumps(self.grading["request"]))
                self.write_grade()
                self.assert_rejected("stale Jev")

    def test_jev_request_hash_is_verified(self):
        self.use_jev()
        self.grading["request_sha256"] = "stale"
        self.write_grade()
        self.assert_rejected("stale Jev grading")

    def test_jev_partial_verdicts_allow_a_complete_original_request(self):
        self.use_jev()
        self.grading["assertion_results"] = self.grading["assertion_results"][:1]
        self.write_grade()
        self.assertEqual(self.run_report()["totals"]["single_pass"]["missing"], 2)

    def test_invalid_record_shapes_fail_cleanly(self):
        original = copy.deepcopy(self.grading)
        for invalid in (None, [], {**original, "assertion_results": {}},
                        {**original, "assertion_results": [None]}):
            with self.subTest(invalid=invalid):
                self.grading = invalid
                self.write_grade()
                self.assert_rejected("grading|assertion")

    def test_failed_report_preserves_previous_summary_and_evidence(self):
        self.run_report()
        previous = (self.workspace / "results.json").read_bytes()
        self.grading["answer_sha256"] = "stale"
        self.write_grade()
        evidence = (self.directory / "grading.json").read_bytes()
        with self.assertRaises(ValueError):
            self.run_report()
        self.assertEqual((self.workspace / "results.json").read_bytes(), previous)
        self.assertEqual((self.directory / "grading.json").read_bytes(), evidence)

    def test_report_cli_exits_nonzero_for_stale_evidence(self):
        pilot.save_json(self.workspace / "manifest.json", self.manifest | {"attempts_per_call": 2})
        self.grading["answer_sha256"] = "stale"
        self.write_grade()
        with contextlib.redirect_stderr(io.StringIO()) as errors:
            result = pilot.main(["report", "--workspace", str(self.workspace)])
        self.assertEqual(result, 1)
        self.assertIn("stale answer grading", errors.getvalue())
        self.assertFalse((self.workspace / "results.json").exists())


if __name__ == "__main__":
    unittest.main()
