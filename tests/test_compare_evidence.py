"""Offline regressions for complete, matched comparison observations."""

import contextlib
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import eval_workflow as ew


class ComparisonEvidenceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for name, value in (("ROOT", self.root), ("SKILLS_DIR", self.root / "skills"),
                            ("WORKSPACES_DIR", self.root / "workspaces")):
            patcher = patch.object(ew, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        model = patch.object(ew, "invoke_model", side_effect=AssertionError("No model calls"))
        model.start()
        self.addCleanup(model.stop)
        self.seed("alpha")

    def seed(self, name, iterations=(1, 2), cases=("first", "second")):
        skill = ew.SKILLS_DIR / name
        (skill / "evals").mkdir(parents=True)
        (skill / "SKILL.md").write_text("Write honestly.")
        (skill / "evals/evals.json").write_text(json.dumps({
            "skill_name": name, "evals": [
                {"id": case, "prompt": "Use the facts.", "assertions": ["Accurate", "Clear"]}
                for case in cases
            ],
        }))
        with contextlib.redirect_stdout(io.StringIO()):
            for number in iterations:
                workspace = ew.init_skill_workspace(skill, str(number), ("with_skill", "without_skill"), False)
                for path in workspace.glob("*/*/grading.json"):
                    grading = ew.load_json(path)
                    for item in grading["assertion_results"]:
                        item.update(passed=True, evidence="Offline evidence")
                    path.write_text(json.dumps(grading))
        return skill

    def grade(self, iteration=2, case="first", skill="alpha", run="with_skill"):
        return ew.WORKSPACES_DIR / skill / f"iteration-{iteration}" / case / run / "grading.json"

    def change(self, update, **options):
        path = self.grade(**options)
        data = ew.load_json(path)
        update(data)
        path.write_text(json.dumps(data))

    def compare(self, *options):
        args = ew.build_parser().parse_args(["compare", "--baseline", "1", "--candidate", "2", *options])
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = ew.compare_command(args)
        self.assertEqual(result, 0)
        return output.getvalue()

    def rejected(self, *options, match=None):
        args = ew.build_parser().parse_args(["compare", "--baseline", "1", "--candidate", "2", *options])
        output = io.StringIO()
        with contextlib.redirect_stdout(output), self.assertRaises(ValueError) as raised:
            ew.compare_command(args)
        self.assertEqual(output.getvalue(), "")
        if match:
            self.assertIn(match, str(raised.exception))

    def snapshot(self):
        return {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def test_missing_candidate_workspace_is_not_zero_failures(self):
        self.rejected("--candidate", "999", match="workspace does not exist")

    def test_missing_baseline_workspace_is_not_zero_failures(self):
        self.rejected("--baseline", "999", match="workspace does not exist")

    def test_empty_iteration_lists_rejected(self):
        for option in ("--baseline", "--candidate"):
            with self.subTest(option=option):
                self.rejected(option, " , ", match="at least one iteration")

    def test_duplicate_resolved_iterations_rejected(self):
        for option, value in (("--baseline", "1,iteration-1"),
                              ("--candidate", "2,latest")):
            with self.subTest(option=option):
                self.rejected(option, value, match="duplicate resolved")

    def test_empty_workspace_rejected(self):
        shutil.rmtree(self.grade().parents[2])
        self.grade().parents[2].mkdir()
        self.rejected(match="no saved evals")

    def test_missing_grade_rejected(self):
        self.grade().unlink()
        self.rejected(match="requires a saved grading file")

    def test_missing_selected_run_rejected(self):
        shutil.rmtree(self.grade().parent)
        self.rejected(match="requires a saved grading file")

    def test_directory_instead_of_grade_rejected(self):
        self.grade().unlink()
        self.grade().mkdir()
        self.rejected(match="requires a saved grading file")

    def test_missing_empty_null_or_malformed_results_rejected(self):
        for value in ([], None, "bad", {}, [None], [1]):
            with self.subTest(value=value):
                self.change(lambda data: data.update(assertion_results=value))
                self.rejected()
        self.change(lambda data: data.pop("assertion_results"))
        self.rejected()

    def test_null_missing_and_nonboolean_verdicts_rejected(self):
        for value in (None, 0, 1, "true", [], {}):
            with self.subTest(value=value):
                self.change(lambda data: data["assertion_results"][0].update(passed=value))
                self.rejected()
        self.change(lambda data: data["assertion_results"][0].pop("passed"))
        self.rejected()

    def test_invalid_or_duplicate_assertion_text_rejected(self):
        for value in (None, "", " ", 3, [], "Clear"):
            with self.subTest(value=value):
                self.change(lambda data: data["assertion_results"][0].update(text=value))
                self.rejected()

    def test_saved_eval_id_must_match_directory(self):
        self.change(lambda data: data.update(eval_id="second"))
        self.rejected(match="eval_id does not match")

    def test_added_removed_or_changed_assertions_rejected_on_either_side(self):
        for iteration in (1, 2):
            path = self.grade(iteration=iteration)
            original = path.read_bytes()
            for operation in (lambda rows: rows.pop(),
                              lambda rows: rows.append({"text": "New", "passed": True}),
                              lambda rows: rows[0].update(text="Changed")):
                with self.subTest(iteration=iteration, operation=operation):
                    path.write_bytes(original)
                    self.change(lambda data: operation(data["assertion_results"]), iteration=iteration)
                    self.rejected(match="sets differ")
            path.write_bytes(original)

    def test_removed_eval_rejected_on_either_side(self):
        for iteration in (1, 2):
            case = self.grade(iteration=iteration).parent.parent
            backup = self.root / "backup"
            shutil.copytree(case, backup)
            shutil.rmtree(case)
            self.rejected(match="sets differ")
            shutil.move(backup, case)

    def test_incomplete_repeated_sample_cannot_be_skipped(self):
        shutil.copytree(self.grade().parents[2], self.grade(iteration=3).parents[2])
        self.change(lambda data: data["assertion_results"][0].update(passed=None), iteration=3)
        self.rejected("--candidate", "2,3", match="fully graded")

    def test_mismatched_repeated_sample_rejected(self):
        shutil.copytree(self.grade().parents[2], self.grade(iteration=3).parents[2])
        self.change(lambda data: data["assertion_results"].pop(), iteration=3)
        self.rejected("--candidate", "2,3", match="across selected iterations")

    def test_complete_results_preserve_fixed_regressed_still_and_passed(self):
        self.change(lambda data: data["assertion_results"][0].update(passed=False), iteration=1)
        self.change(lambda data: data["assertion_results"][1].update(passed=False))
        for iteration in (1, 2):
            self.change(lambda data: data["assertion_results"][0].update(passed=False), iteration=iteration, case="second")
        output = self.compare()
        self.assertIn("failing assertions: 2 -> 2 (+0)", output)
        self.assertIn("fixed 1   regressed 1   still failing 1", output)
        self.assertNotIn("FIXED", output)
        self.assertIn("FIXED", self.compare("--verbose"))

    def test_repeated_samples_preserve_any_failure_and_allow_unequal_counts(self):
        shutil.copytree(self.grade().parents[2], self.grade(iteration=3).parents[2])
        self.change(lambda data: data["assertion_results"][0].update(passed=False), iteration=3)
        output = self.compare("--candidate", "2,3")
        self.assertIn("failing assertions: 0 -> 1 (+1)", output)
        self.assertNotIn("Single sample", output)

    def test_assertion_order_does_not_affect_matching(self):
        self.change(lambda data: data["assertion_results"].reverse())
        self.assertIn("0 -> 0 (+0)", self.compare())

    def test_unselected_eval_and_run_do_not_block_target(self):
        self.grade(case="second").write_text("not json")
        self.grade(run="without_skill").unlink()
        self.assertIn("0 -> 0 (+0)", self.compare("--eval-id", "first"))

    def test_filter_skips_nonmatching_skills_but_rejects_zero_global_matches(self):
        self.seed("beta", cases=("other",))
        self.grade(skill="beta", case="other").write_text("not json")
        self.assertIn("0 -> 0 (+0)", self.compare("--eval-id", "first"))
        self.rejected("--eval-id", "unknown", match="no matching saved evals")

    def test_filter_skips_never_sampled_skills_before_resolving_latest(self):
        self.seed("beta", iterations=(), cases=("other",))
        self.assertIn("0 -> 0 (+0)", self.compare("--eval-id", "first", "--candidate", "latest"))
        self.rejected("--skill", "beta", "--eval-id", "first", "--candidate", "latest")

    def test_filter_skips_nonmatching_skill_before_duplicate_alias_validation(self):
        self.seed("beta", iterations=(1,), cases=("other",))
        self.assertIn("0 -> 0 (+0)", self.compare("--eval-id", "first", "--baseline", "1,latest"))

    def test_filter_missing_from_one_participating_iteration_rejected(self):
        shutil.rmtree(self.grade().parent.parent)
        self.rejected("--eval-id", "first", match="requires a saved grading file")

    def test_explicit_skill_missing_filter_rejected(self):
        self.rejected("--skill", "alpha", "--eval-id", "unknown")

    def test_latest_resolves_per_skill(self):
        self.seed("beta", iterations=(1, 3))
        self.change(lambda data: data["assertion_results"][0].update(passed=False), skill="beta", iteration=3)
        self.assertIn("0 -> 1 (+1)", self.compare("--candidate", "latest"))

    def test_later_invalid_skill_does_not_publish_partial_metrics(self):
        self.seed("beta")
        self.grade(skill="beta").unlink()
        self.rejected()

    def test_current_fixture_changes_do_not_change_historical_comparison(self):
        (ew.SKILLS_DIR / "alpha/evals/evals.json").write_text("invalid current fixture")
        self.assertIn("0 -> 0 (+0)", self.compare())

    def test_success_and_failure_leave_artifacts_unchanged(self):
        before = self.snapshot()
        self.compare()
        self.assertEqual(before, self.snapshot())
        self.grade().unlink()
        before = self.snapshot()
        self.rejected()
        self.assertEqual(before, self.snapshot())

    def test_cli_returns_nonzero_without_summary_for_missing_evidence(self):
        argv = ["eval_workflow.py", "compare", "--baseline", "1", "--candidate", "999"]
        output, errors = io.StringIO(), io.StringIO()
        with patch.object(sys, "argv", argv), contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            self.assertEqual(ew.main(), 1)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("workspace does not exist", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
