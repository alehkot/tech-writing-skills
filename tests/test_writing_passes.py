"""Exercise isolation, review bounds, and retained evidence without provider calls."""

import json
import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import eval_writing_passes as pilot


class WritingPassTests(unittest.TestCase):
    def setUp(self):
        self.case = {"id": "case", "skill": "task", "split": "transfer",
                     "prompt": "Original source", "assertions": ["SECRET ASSERTION"]}
        self.manifest = {"writer_text": {"task": "WRITER ONLY"}, "reviewer_text": "REVIEWER ONLY",
                         "generator": {}, "reviewer": {}, "max_repairs": 1, "samples": 1,
                         "grader": {"executor": "pi"}, "cases": [self.case]}

    def test_specialist_and_final_grader_are_blind(self):
        prompt = pilot.review_prompt(self.case["prompt"], "Draft", "REVIEWER ONLY", specialist=True)
        self.assertNotIn("SECRET ASSERTION", prompt)
        self.assertNotIn("WRITER ONLY", prompt)
        grade = pilot.final_grade_prompt(self.case, "Draft")
        self.assertIn("SECRET ASSERTION", grade)
        for hidden in (*pilot.ARMS, "WRITER ONLY", "REVIEWER ONLY"):
            self.assertNotIn(hidden, grade)

    def test_one_repair_is_followed_by_final_review_and_unresolved_is_retained(self):
        review = {"findings": [{"problem": "Unsupported claim"}], "limitations": [], "blocking_gaps": [], "checked": ["Sources"]}
        calls = []
        def invoke(directory, prompt, settings, manifest, schema=None):
            calls.append(directory.name)
            if schema:
                return json.dumps(review)
            return "Repaired draft" if directory.name.startswith("repair") else "Initial draft"
        with tempfile.TemporaryDirectory() as root, patch.object(pilot, "call_stage", side_effect=invoke):
            pilot.generate_case(Path(root), self.manifest, self.case, 1)
            self.assertEqual(calls, ["draft", "review-0", "repair-1", "review-1",
                                     "review-0", "repair-1", "review-1"])
            for arm in pilot.ARMS[1:]:
                state = json.loads((Path(root) / "case/sample-1" / arm / "workflow.json").read_text())
                self.assertEqual(state["status"], "review_unresolved")

    def test_clean_review_does_not_rewrite_a_valid_draft(self):
        clean = json.dumps({"findings": [], "limitations": [], "blocking_gaps": [], "checked": ["Sources"]})
        with tempfile.TemporaryDirectory() as root, patch.object(pilot, "call_stage", side_effect=["Valid", clean, clean]) as invoke:
            pilot.generate_case(Path(root), self.manifest, self.case, 1)
            self.assertEqual(invoke.call_count, 3)
            for arm in pilot.ARMS:
                self.assertEqual((Path(root) / "case/sample-1" / arm / "outputs/answer.md").read_text(), "Valid")

    def test_limited_review_cannot_be_clear(self):
        self.manifest["max_repairs"] = 0
        limited = json.dumps({"findings": [], "limitations": [], "blocking_gaps": ["Required source unavailable"], "checked": ["Scope"]})
        with tempfile.TemporaryDirectory() as root, patch.object(pilot, "call_stage", side_effect=["Draft", limited, limited]):
            pilot.generate_case(Path(root), self.manifest, self.case, 1)
            state = json.loads((Path(root) / "case/sample-1/specialist_review/workflow.json").read_text())
            self.assertEqual(state["status"], "review_unresolved")

    def test_documented_unknowns_do_not_trigger_repair(self):
        limited = json.dumps({"findings": [], "limitations": ["Default was not supplied and is marked unknown"],
                              "blocking_gaps": [], "checked": ["Source fidelity"]})
        with tempfile.TemporaryDirectory() as root, patch.object(pilot, "call_stage", side_effect=["Correct draft", limited, limited]) as invoke:
            pilot.generate_case(Path(root), self.manifest, self.case, 1)
            self.assertEqual(invoke.call_count, 3)
            state = json.loads((Path(root) / "case/sample-1/specialist_review/workflow.json").read_text())
            self.assertEqual(state["status"], "review_clear_with_limits")

    def test_missing_execution_stays_in_denominator(self):
        with tempfile.TemporaryDirectory() as root:
            result = pilot.report(Path(root), self.manifest)
        for total in result["totals"].values():
            self.assertEqual(total["planned"], 1)
            self.assertEqual(total["missing"], 1)
            self.assertEqual(total["passed"], 0)

    def test_saved_answer_cannot_be_replaced(self):
        with tempfile.TemporaryDirectory() as root:
            pilot.publish(Path(root), "Original", "draft_only")
            with self.assertRaises(ValueError):
                pilot.publish(Path(root), "Replacement", "review_clear")

    def test_failed_stage_is_not_silently_retried(self):
        manifest = {"timeout_seconds": 10, "attempts_per_call": 2}
        settings = {"executor": "pi", "model": "test", "effort": "low"}
        with tempfile.TemporaryDirectory() as root, patch.object(pilot.ew, "invoke_model", side_effect=ValueError("provider failed")) as invoke:
            with self.assertRaises(ValueError):
                pilot.call_stage(Path(root), "Prompt", settings, manifest)
            with self.assertRaisesRegex(ValueError, "recorded incomplete stage"):
                pilot.call_stage(Path(root), "Prompt", settings, manifest)
            self.assertEqual(invoke.call_count, 1)

    def test_grader_override_is_not_silently_ignored_after_init(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            pilot.main(["grade", "--workspace", "/unused", "--grader-model", "different-model"])
        self.assertEqual(error.exception.code, 2)

    def test_changed_final_answer_is_not_graded(self):
        with tempfile.TemporaryDirectory() as root:
            directory = Path(root) / "case/sample-1/single_pass"
            pilot.publish(directory, "Original", "draft_only")
            (directory / "outputs/answer.md").write_text("Changed")
            with patch.object(pilot, "call_stage") as invoke, self.assertRaisesRegex(ValueError, "saved final answer changed"):
                pilot.grade_case(Path(root), self.manifest, self.case, 1)
            invoke.assert_not_called()

    def test_changed_jev_model_does_not_reuse_previous_grade(self):
        self.manifest["grader"] = {"executor": "jev", "model": "different-jev"}
        with tempfile.TemporaryDirectory() as root:
            directory = Path(root) / "case/sample-1/single_pass"
            pilot.publish(directory, "Original", "draft_only")
            pilot.save_json(directory / "grading.jev.json", {"answer_sha256": pilot.digest("Original"),
                "grader": {"requested_model": "old-jev"}, "assertion_results": []})
            with patch.object(pilot.jev, "grade") as invoke, self.assertRaisesRegex(ValueError, "stale Jev grading"):
                pilot.grade_case(Path(root), self.manifest, self.case, 1)
            invoke.assert_not_called()

    def test_output_cap_is_local_and_credentials_are_not_written(self):
        original = pilot.ew.sanitized_pi_environment
        manifest = {role: {"executor": "pi", "model": "test-model"}
                    for role in ("generator", "reviewer", "grader")}
        manifest["max_output_tokens"] = 8192
        with tempfile.TemporaryDirectory() as root, patch.object(pilot.ew, "sanitized_pi_environment", return_value={"OPENROUTER_API_KEY": "secret-test-value"}) as base:
            with pilot.limit_pi_outputs(manifest):
                environment = pilot.ew.sanitized_pi_environment(isolated_home=Path(root))
                config = (Path(root) / ".pi/agent/models.json").read_text()
                self.assertEqual(environment["OPENROUTER_API_KEY"], "secret-test-value")
                self.assertNotIn("secret-test-value", config)
                self.assertEqual(json.loads(config)["providers"]["openrouter"]["modelOverrides"]["test-model"]["maxTokens"], 8192)
            self.assertIs(pilot.ew.sanitized_pi_environment, base)
        self.assertIs(pilot.ew.sanitized_pi_environment, original)

    def test_codex_pilot_isolates_repository_and_ambient_inputs(self):
        manifest = {role: {"executor": "codex"} for role in ("generator", "reviewer", "grader")}
        original = pilot.ew.codex_exec_command
        with pilot.isolate_codex_calls(manifest):
            command = pilot.ew.codex_exec_command(model="test-model", reasoning_effort="low",
                result_path=Path("workspaces/test-answer.md"), schema_path=None)
            working_root = Path(command[command.index("-C") + 1])
            self.assertTrue(working_root.is_dir())
            self.assertNotEqual(working_root, pilot.ROOT)
            self.assertTrue(Path(command[command.index("-o") + 1]).is_absolute())
            self.assertIn("project_doc_max_bytes=0", command)
            self.assertIn('web_search="disabled"', command)
            self.assertIn("skip_host_skill_discovery", command)
            disabled = {command[i + 1] for i, value in enumerate(command[:-1]) if value == "--disable"}
            self.assertTrue({"shell_tool", "unified_exec", "apps", "plugins", "memories", "multi_agent"} <= disabled)
        self.assertIs(pilot.ew.codex_exec_command, original)
        self.assertFalse(working_root.exists())


if __name__ == "__main__":
    unittest.main()
