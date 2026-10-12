"""Offline checks that lost grade files cannot improve apparent coverage."""

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


class MissingGradeTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.skill = self.root / "skills/test"
        (self.skill / "evals").mkdir(parents=True)
        (self.skill / "SKILL.md").write_text("Preserve supplied facts.")
        self.fixture = self.skill / "evals/evals.json"
        self.fixture.write_text(json.dumps({"skill_name": "test", "evals": [
            {"id": case, "prompt": "Write supplied facts.",
             "expected_output": "Facts", "assertions": ["Preserves facts"]}
            for case in ("first", "second")
        ]}))
        for name, value in (("ROOT", self.root),
                            ("WORKSPACES_DIR", self.root / "workspaces")):
            patcher = patch.object(ew, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.runs = ("with_skill", "without_skill")
        with contextlib.redirect_stdout(io.StringIO()):
            self.workspace = ew.init_skill_workspace(
                self.skill, "1", self.runs, False
            )
        for path in self.workspace.glob("*/*/grading.json"):
            grading = ew.load_json(path)
            grading["assertion_results"][0].update(passed=True, evidence="Facts")
            path.write_text(json.dumps(grading))
        self.aggregate()

    def aggregate(self, *, write=True, runs=None):
        return ew.aggregate_skill_workspace(
            self.skill, "iteration-1", self.runs if runs is None else runs,
            write=write,
        )

    def grade(self, case="second", run="with_skill"):
        return self.workspace / case / run / "grading.json"

    def snapshot(self):
        return {str(path.relative_to(self.workspace)): path.read_bytes()
                for path in self.workspace.rglob("*") if path.is_file()}

    def assert_missing_rejected(self, *, write=True, runs=None):
        with self.assertRaisesRegex(ValueError, "grading.json: missing or invalid"):
            self.aggregate(write=write, runs=runs)

    def test_missing_grade_cannot_turn_two_cases_into_one_complete_case(self):
        self.grade().unlink()
        self.assert_missing_rejected()
        self.assertFalse((self.workspace / "benchmark.json").exists())

    def test_losing_a_failing_case_cannot_fabricate_a_positive_skill_delta(self):
        for run in self.runs:
            path = self.grade(run=run)
            grading = ew.load_json(path)
            grading["assertion_results"][0]["passed"] = False
            path.write_text(json.dumps(grading))
        baseline = self.aggregate()
        self.assertTrue(baseline["complete"])
        self.assertEqual(baseline["delta"]["pass_rate"], 0.0)
        self.assertEqual(baseline["run_summary"]["with_skill"]["pass_rate"]["mean"], 0.5)
        self.grade().unlink()
        self.assert_missing_rejected()

    def test_missing_grade_in_other_arm_is_rejected(self):
        self.grade(run="without_skill").unlink()
        self.assert_missing_rejected()

    def test_all_grades_missing_in_selected_arm_is_rejected(self):
        for case in ("first", "second"):
            self.grade(case).unlink()
        self.assert_missing_rejected()

    def test_read_only_failure_does_not_modify_existing_files(self):
        self.grade().unlink()
        before = self.snapshot()
        self.assert_missing_rejected(write=False)
        self.assertEqual(self.snapshot(), before)

    def test_preflight_checks_later_arm_before_rewriting_any_summary(self):
        first = self.grade("first")
        grading = ew.load_json(first)
        grading["assertion_results"][0]["passed"] = False
        first.write_text(json.dumps(grading))
        self.grade(run="without_skill").unlink()
        before = self.snapshot()
        self.assert_missing_rejected()
        before.pop("benchmark.json")
        self.assertEqual(self.snapshot(), before)

    def test_failure_without_old_benchmark_is_still_actionable(self):
        (self.workspace / "benchmark.json").unlink()
        self.grade().unlink()
        self.assert_missing_rejected()

    def test_grade_replaced_by_directory_is_rejected(self):
        path = self.grade()
        path.unlink()
        path.mkdir()
        self.assert_missing_rejected()

    def test_dangling_grade_symlink_is_rejected(self):
        path = self.grade()
        path.unlink()
        path.symlink_to("missing-grade.json")
        self.assert_missing_rejected()
        self.assertTrue(path.is_symlink())

    def test_unselected_arm_does_not_block_selected_arm(self):
        self.grade(run="without_skill").unlink()
        result = self.aggregate(runs=("with_skill",))
        self.assertTrue(result["complete"])
        self.assertEqual(result["run_summary"]["with_skill"]["coverage"]["total_evals"], 2)

    def test_custom_run_is_checked(self):
        for case in ("first", "second"):
            (self.workspace / case / "with_skill").rename(
                self.workspace / case / "custom_run"
            )
        self.grade(run="custom_run").unlink()
        self.assert_missing_rejected(runs=("custom_run",))

    def test_historical_workspace_does_not_depend_on_current_fixture(self):
        self.fixture.write_text('{"evals": []}')
        self.assertTrue(self.aggregate()["complete"])
        self.grade().unlink()
        self.assert_missing_rejected()

    def test_restored_grade_allows_full_coverage_again(self):
        path = self.grade()
        original = path.read_bytes()
        path.unlink()
        self.assert_missing_rejected()
        path.write_bytes(original)
        result = self.aggregate()
        self.assertTrue(result["complete"])
        for run in self.runs:
            self.assertEqual(result["run_summary"][run]["coverage"]["total_evals"], 2)

    def test_existing_null_verdict_is_partial_not_missing(self):
        path = self.grade()
        grading = ew.load_json(path)
        grading["assertion_results"][0].update(passed=None, evidence="")
        path.write_text(json.dumps(grading))
        result = self.aggregate()
        self.assertFalse(result["complete"])
        coverage = result["run_summary"]["with_skill"]["coverage"]
        self.assertEqual(coverage["total_evals"], 2)
        self.assertEqual(coverage["graded_evals"], 1)

    def test_unrelated_workspace_files_do_not_add_cases(self):
        (self.workspace / "notes").mkdir()
        (self.workspace / "notes/with_skill").write_text("Human notes")
        result = self.aggregate()
        self.assertTrue(result["complete"])
        self.assertEqual(result["run_summary"]["with_skill"]["coverage"]["total_evals"], 2)

    def test_read_only_valid_aggregation_preserves_files(self):
        before = self.snapshot()
        self.assertTrue(self.aggregate(write=False)["complete"])
        self.assertEqual(self.snapshot(), before)


if __name__ == "__main__":
    unittest.main()
