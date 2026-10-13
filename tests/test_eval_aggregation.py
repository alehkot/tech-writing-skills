"""Offline regressions for summaries derived from saved assertion verdicts."""

import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import eval_workflow as ew


class SavedVerdictTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.skill = self.root / "skills/test"
        self.workspace = self.root / "workspaces/test/iteration-1"
        self.runs = ("with_skill", "without_skill")
        for name, value in (("ROOT", self.root), ("SKILLS_DIR", self.root / "skills"),
                            ("WORKSPACES_DIR", self.root / "workspaces")):
            patcher = patch.object(ew, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.skill.mkdir(parents=True)
        (self.skill / "SKILL.md").write_text("Test skill")
        for case in ("first", "second"):
            for run in self.runs:
                path = self.grade(case, run)
                path.parent.mkdir(parents=True)
                self.save(path, {"assertion_results": [{"passed": True}, {"passed": False}],
                                 "summary": {"passed": 77, "pass_rate": 1.0},
                                 "notes": "Keep my notes", "grader": {"model": "offline"}})
                (path.parent / "timing.json").write_text("{}")
        self.aggregate()

    def grade(self, case="second", run="with_skill"):
        return self.workspace / case / run / "grading.json"

    def save(self, path, value):
        path.write_text(json.dumps(value))

    def replace_results(self, results, *, case="second", run="with_skill"):
        path = self.grade(case, run)
        grading = ew.load_json(path)
        grading["assertion_results"] = results
        self.save(path, grading)
        return path

    def aggregate(self, *, write=True, runs=None):
        return ew.aggregate_skill_workspace(self.skill, "iteration-1",
                                            self.runs if runs is None else runs, write=write)

    def snapshot(self):
        return {str(path.relative_to(self.workspace)): path.read_bytes()
                for path in self.workspace.rglob("*") if path.is_file()}

    def assert_invalid(self, *, write=True):
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "grading.json:.*assertion"):
            self.aggregate(write=write)
        if write:
            before.pop("benchmark.json", None)
        self.assertEqual(self.snapshot(), before)

    def test_string_false_cannot_fabricate_complete_perfect_score(self):
        self.replace_results([{"passed": True}, {"passed": "false"}])
        self.assert_invalid()

    def test_only_actual_booleans_or_null_are_valid_verdicts(self):
        for verdict in (0, 1, -1, 0.0, 1.0, "", "true", "false", [], [False], {}, {"x": True}):
            with self.subTest(verdict=verdict):
                self.replace_results([{"passed": True}, {"passed": verdict}])
                self.assert_invalid()

    def test_invalid_results_container_is_rejected(self):
        for results in (None, {}, "results", 1, True):
            with self.subTest(results=results):
                self.replace_results(results)
                self.assert_invalid()

    def test_non_object_rows_have_actionable_error(self):
        for row in (None, [], "false", 1, True):
            with self.subTest(row=row):
                self.replace_results([{"passed": True}, row])
                self.assert_invalid()

    def test_error_identifies_path_and_assertion_position(self):
        path = self.replace_results([{"passed": True}, {"passed": 1}])
        with self.assertRaises(ValueError) as caught:
            self.aggregate()
        self.assertIn(str(path), str(caught.exception))
        self.assertIn("assertion result 2", str(caught.exception))

    def test_valid_null_and_missing_verdicts_remain_ungraded(self):
        path = self.replace_results([{"passed": True}, {"passed": False}, {"passed": None}, {}])
        self.assertEqual(ew.summarise_grading(path), {
            "passed": 1, "failed": 1, "ungraded": 2, "total": 4, "pass_rate": 0.5})
        result = self.aggregate()
        self.assertFalse(result["complete"])
        self.assertEqual(result["run_summary"]["with_skill"]["coverage"]["total_assertions"], 6)

    def test_all_ungraded_is_partial_with_null_rate(self):
        for case in ("first", "second"):
            self.replace_results([{"passed": None}, {}], case=case)
        result = self.aggregate()
        self.assertFalse(result["complete"])
        self.assertIsNone(result["run_summary"]["with_skill"]["pass_rate"]["mean"])

    def test_empty_results_remain_incomplete(self):
        self.replace_results([])
        self.assertFalse(self.aggregate()["complete"])

    def test_missing_results_remain_incomplete_for_legacy_files(self):
        self.save(self.grade(), {"notes": "Legacy metadata"})
        self.assertFalse(self.aggregate()["complete"])

    def test_read_only_rejects_malformed_verdict_without_mutation(self):
        self.replace_results([{"passed": "false"}])
        self.assert_invalid(write=False)

    def test_valid_read_and_write_results_agree_without_trusting_cache(self):
        self.replace_results([{"passed": False}, {"passed": False}])
        before = self.snapshot()
        readonly = self.aggregate(write=False)
        self.assertEqual(self.snapshot(), before)
        written = self.aggregate()
        self.assertEqual(readonly, written)
        self.assertEqual(written["run_summary"]["with_skill"]["pass_rate"]["mean"], 0.25)

    def test_invalid_cached_summary_is_ignored(self):
        for cached in (None, [], "invalid", {"pass_rate": 100, "passed": "all"}):
            with self.subTest(cached=cached):
                grading = ew.load_json(self.grade())
                grading["summary"] = cached
                self.save(self.grade(), grading)
                before = self.snapshot()
                result = self.aggregate(write=False)
                self.assertEqual(self.snapshot(), before)
                self.assertTrue(result["complete"])
                self.assertEqual(result["run_summary"]["with_skill"]["pass_rate"]["mean"], 0.5)

    def test_later_arm_failure_does_not_rewrite_earlier_grades(self):
        self.replace_results([{"passed": True}, {"passed": True}], case="first")
        self.replace_results([{"passed": 1}], run="without_skill")
        self.assert_invalid()

    def test_invalid_json_does_not_rewrite_any_grade(self):
        self.grade(run="without_skill").write_text("{bad json")
        before = self.snapshot()
        with self.assertRaises(ValueError):
            self.aggregate()
        before.pop("benchmark.json")
        self.assertEqual(self.snapshot(), before)

    def test_non_object_grade_does_not_rewrite_any_grade(self):
        self.save(self.grade(), [])
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "expected a JSON object"):
            self.aggregate()
        before.pop("benchmark.json")
        self.assertEqual(self.snapshot(), before)

    def test_invalid_grade_in_unselected_arm_is_not_evaluated(self):
        self.replace_results([{"passed": "false"}], run="without_skill")
        self.assertTrue(self.aggregate(runs=("with_skill",))["complete"])

    def test_custom_run_gets_same_validation(self):
        for case in ("first", "second"):
            self.grade(case).parent.rename(self.workspace / case / "custom")
        self.replace_results([{"passed": 1}], run="custom")
        with self.assertRaisesRegex(ValueError, "passed must be boolean or null"):
            self.aggregate(runs=("custom",))

    def test_summarise_rejects_invalid_without_modifying_original(self):
        path = self.replace_results([{"passed": "false"}])
        before = path.read_bytes()
        with self.assertRaises(ValueError):
            ew.summarise_grading(path)
        self.assertEqual(path.read_bytes(), before)

    def test_refresh_preserves_all_non_summary_metadata(self):
        path = self.grade()
        before = ew.load_json(path)
        ew.summarise_grading(path)
        after = ew.load_json(path)
        before.pop("summary")
        after.pop("summary")
        self.assertEqual(after, before)

    def test_restore_valid_verdict_allows_recovery(self):
        self.replace_results([{"passed": "false"}])
        self.assert_invalid()
        self.replace_results([{"passed": False}])
        result = self.aggregate()
        self.assertTrue(result["complete"])
        self.assertTrue((self.workspace / "benchmark.json").is_file())

    def test_cli_reports_validation_error_without_success_output(self):
        self.replace_results([{"passed": True}, {"passed": "false"}])
        out, err = io.StringIO(), io.StringIO()
        with patch.object(sys, "argv", ["eval_workflow.py", "aggregate", "--skill", "test", "--iteration", "1"]), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            self.assertEqual(ew.main(), 1)
        self.assertNotIn("Aggregated", out.getvalue())
        self.assertIn("passed must be boolean or null", err.getvalue())


if __name__ == "__main__":
    unittest.main()
