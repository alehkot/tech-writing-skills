"""Offline sample-command regressions using real scaffolds and mocked model replies."""

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


class SampleCohortTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for name, value in (("ROOT", self.root), ("SKILLS_DIR", self.root / "skills"),
                            ("WORKSPACES_DIR", self.root / "workspaces")):
            patcher = patch.object(ew, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.verdicts = {}
        self.model_calls = []

    def seed_skill(self, name, iterations, cases=("case",)):
        skill = ew.SKILLS_DIR / name
        (skill / "evals").mkdir(parents=True)
        (skill / "SKILL.md").write_text("Write honestly.", encoding="utf-8")
        fixture = {"skill_name": name, "evals": [
            {"id": case, "prompt": "Say hello.", "assertions": ["Says hello"]}
            for case in cases
        ]}
        (skill / "evals/evals.json").write_text(json.dumps(fixture), encoding="utf-8")
        for number in range(1, iterations + 1):
            workspace = ew.init_skill_workspace(skill, str(number), ("with_skill",), False)
            for path in workspace.glob("*/with_skill/grading.json"):
                grading = ew.load_json(path)
                grading["assertion_results"][0].update(passed=False, evidence="Historical failure")
                path.write_text(json.dumps(grading), encoding="utf-8")
        return skill

    def fake_model(self, prompt, **kwargs):
        """Replace only the external model boundary, retaining generation and grading."""
        result_path = kwargs["result_path"]
        self.model_calls.append(result_path)
        if kwargs.get("schema") == ew.GRADING_SCHEMA:
            run_dir = result_path.parent.parent
            grading = ew.load_json(run_dir / "grading.json")
            iteration = run_dir.parent.parent.name
            verdict = self.verdicts.get((grading["skill_name"], iteration, grading["eval_id"]), True)
            text = json.dumps({"assertion_results": [{
                "index": 1, "text": "Says hello", "passed": verdict, "evidence": "Offline evidence",
            }], "notes": "Offline grader"})
        else:
            text = "Hello."
        result_path.write_text(text, encoding="utf-8")
        return ew.ModelReply(
            executor=kwargs["executor"], model=kwargs["model"],
            reasoning_effort=kwargs["reasoning_effort"], command=["offline"], exit_code=0,
            duration_ms=1, total_tokens=1, text=text,
            attempts=[{"attempt": 1, "outcome": "success"}], details={},
        )

    def sample(self, *options):
        args = ew.build_parser().parse_args([
            "sample", "--model", "offline-generator", "--grader-model", "offline-grader",
            *options,
        ])
        output = io.StringIO()
        with patch.object(ew, "invoke_model", side_effect=self.fake_model), contextlib.redirect_stdout(output):
            self.assertEqual(ew.sample_command(args), 0)
        return output.getvalue()

    def assert_cohort(self, output, name, count, *, failures=None):
        self.assertIn(f"\n{name}  ({count} iterations)\n", output)
        section = output.split(f"\n{name}  (", 1)[1].split("\n\n", 1)[0]
        failures = [0] * count if failures is None else failures
        self.assertIn(f"n={count} fails={failures}", section)
        return section

    def test_one_sample_does_not_include_other_skills_historical_iteration(self):
        self.seed_skill("alpha", 1)
        self.seed_skill("beta", 2)
        output = self.sample("--samples", "1")
        self.assertIn("Created: alpha/iteration-2, beta/iteration-3", output)
        for name in ("alpha", "beta"):
            self.assert_cohort(output, name, 1)
        self.assertNotIn("FLAKY", output)
        self.assertEqual(len(self.model_calls), 4)

    def test_multiple_samples_with_partly_overlapping_iteration_numbers(self):
        self.seed_skill("alpha", 1)
        self.seed_skill("beta", 2)
        output = self.sample("--samples", "3")
        for name in ("alpha", "beta"):
            self.assert_cohort(output, name, 3)
        self.assertNotIn("FLAKY", output)
        self.assertEqual(len(self.model_calls), 12)

    def test_multiple_samples_with_disjoint_iteration_numbers(self):
        self.seed_skill("alpha", 1)
        self.seed_skill("beta", 10)
        output = self.sample("--samples", "2")
        for name in ("alpha", "beta"):
            self.assert_cohort(output, name, 2)
        self.assertNotIn("FLAKY", output)

    def test_equal_iteration_numbers_keep_existing_statistics(self):
        self.seed_skill("alpha", 2)
        self.seed_skill("beta", 2)
        output = self.sample("--samples", "2")
        for name in ("alpha", "beta"):
            self.assert_cohort(output, name, 2)
        self.assertEqual(output.count("No assertion flipped"), 1)

    def test_different_eval_ids_are_not_filtered_by_previous_skill(self):
        self.seed_skill("alpha", 1, cases=("alpha_case",))
        self.seed_skill("beta", 2, cases=("beta_case",))
        output = self.sample("--samples", "1")
        self.assertIn("alpha_case", self.assert_cohort(output, "alpha", 1))
        self.assertIn("beta_case", self.assert_cohort(output, "beta", 1))

    def test_selected_run_is_used_for_generation_and_statistics(self):
        self.seed_skill("alpha", 1)
        self.seed_skill("beta", 2)
        output = self.sample("--samples", "1", "--run", "without_skill")
        for name in ("alpha", "beta"):
            self.assert_cohort(output, name, 1)
        for path in self.model_calls:
            self.assertIn("without_skill", path.parts)
            self.assertNotIn("with_skill", path.parts)

    def test_single_skill_does_not_read_or_change_other_skills(self):
        self.seed_skill("alpha", 1)
        self.seed_skill("beta", 2)
        beta = ew.WORKSPACES_DIR / "beta"
        before = {p.relative_to(beta): p.read_bytes() for p in beta.rglob("*") if p.is_file()}
        output = self.sample("--skill", "alpha", "--samples", "2")
        self.assert_cohort(output, "alpha", 2)
        self.assertNotIn("beta", output)
        self.assertEqual(before, {p.relative_to(beta): p.read_bytes() for p in beta.rglob("*") if p.is_file()})
        self.assertEqual(len(self.model_calls), 4)

    def test_eval_filter_reports_only_requested_case_and_new_iterations(self):
        for name, count in (("alpha", 1), ("beta", 2)):
            self.seed_skill(name, count, cases=("selected", "untouched"))
        output = self.sample("--samples", "2", "--eval-id", "selected")
        for name in ("alpha", "beta"):
            section = self.assert_cohort(output, name, 2)
            self.assertIn("selected", section)
            self.assertNotIn("untouched", section)
            latest = ew.WORKSPACES_DIR / name / ew.resolve_iteration(ew.SKILLS_DIR / name, "latest")
            untouched = ew.load_json(latest / "untouched/with_skill/grading.json")
            self.assertIsNone(untouched["assertion_results"][0]["passed"])
            self.assertFalse((latest / "untouched/with_skill/outputs/answer.md").exists())
        self.assertNotIn("FLAKY", output)
        self.assertEqual(len(self.model_calls), 8)

    def test_genuine_new_flips_are_reported_once_across_skills(self):
        self.seed_skill("alpha", 1)
        self.seed_skill("beta", 2)
        self.verdicts[("alpha", "iteration-2", "case")] = False
        self.verdicts[("beta", "iteration-4", "case")] = False
        output = self.sample("--samples", "2")
        self.assert_cohort(output, "alpha", 2, failures=[1, 0])
        self.assert_cohort(output, "beta", 2, failures=[0, 1])
        self.assertEqual(output.count("2 assertions flipped across samples."), 1)
        self.assertNotIn("No assertion flipped", output)

    def test_new_samples_keep_chronological_order_across_digit_boundary(self):
        self.seed_skill("alpha", 8)
        self.verdicts[("alpha", "iteration-9", "case")] = False
        self.verdicts[("alpha", "iteration-11", "case")] = False
        output = self.sample("--samples", "3")
        self.assert_cohort(output, "alpha", 3, failures=[1, 0, 1])

    def test_default_stats_still_uses_all_saved_iterations_per_skill(self):
        self.seed_skill("alpha", 1)
        self.seed_skill("beta", 2)
        args = ew.build_parser().parse_args(["stats"])
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(ew.stats_command(args), 0)
        self.assert_cohort(output.getvalue(), "alpha", 1, failures=[1])
        self.assert_cohort(output.getvalue(), "beta", 2, failures=[1, 1])
        self.assertEqual(output.getvalue().count("No assertion flipped"), 1)

    def test_explicit_stats_iterations_remain_user_selected(self):
        skill = self.seed_skill("alpha", 2)
        path = ew.WORKSPACES_DIR / skill.name / "iteration-2/case/with_skill/grading.json"
        grading = ew.load_json(path)
        grading["assertion_results"][0]["passed"] = True
        path.write_text(json.dumps(grading), encoding="utf-8")
        args = ew.build_parser().parse_args(["stats", "--iterations", "1,2"])
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(ew.stats_command(args), 0)
        self.assert_cohort(output.getvalue(), "alpha", 2, failures=[1, 0])
        self.assertIn("1 assertions flipped", output.getvalue())


if __name__ == "__main__":
    unittest.main()
