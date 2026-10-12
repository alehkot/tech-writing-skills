"""Offline pruning regressions using real temporary workspaces; no model calls."""
import argparse
import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import eval_workflow as ew


class PruningTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.skills = self.root / "skills"
        self.workspaces = self.root / "workspaces"
        self.skill = self.skills / "test-skill"
        (self.skill / "evals").mkdir(parents=True)
        (self.skill / "SKILL.md").write_text("Write accurately.\n")
        self.fixture = self.skill / "evals/evals.json"
        self.fixture.write_text(json.dumps({
            "skill_name": self.skill.name,
            "evals": [{"id": "case", "prompt": "Explain the supplied facts.",
                       "expected_output": "An explanation", "assertions": ["A", "B"]}],
        }))
        for name, value in (("ROOT", self.root), ("SKILLS_DIR", self.skills),
                            ("WORKSPACES_DIR", self.workspaces)):
            patcher = patch.object(ew, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def create(self, number, runs=ew.DEFAULT_RUNS):
        return ew.init_skill_workspace(self.skill, str(number), runs, force=False)

    def run_dir(self, workspace, run="with_skill"):
        return workspace / "case" / run

    def change_json(self, path, change):
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data))

    def snapshot(self):
        result = {}
        for path in self.root.rglob("*"):
            relative = str(path.relative_to(self.root))
            if path.is_symlink():
                result[relative] = ("link", os.readlink(path))
            elif path.is_dir():
                result[relative] = ("dir", None)
            else:
                result[relative] = ("file", path.read_bytes())
        return result

    def prune(self, *, keep=3, apply=False):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(ew.prune_command(argparse.Namespace(
                skill=self.skill.name, keep=keep, apply=apply,
            )), 0)
        return output.getvalue()

    def assert_meaningful(self, number):
        before = self.snapshot()
        self.assertTrue(ew.iteration_has_results(self.skill, number))
        self.assertEqual(self.snapshot(), before)

    def test_pristine_scaffolds_are_disposable_including_single_arm(self):
        for number, runs in enumerate((ew.DEFAULT_RUNS, ("with_skill",), ("without_skill",)), 1):
            self.create(number, runs)
            self.assertFalse(ew.iteration_has_results(self.skill, number))
        before = self.snapshot()
        output = self.prune()
        self.assertEqual(output.count("Would remove"), 3)
        self.assertEqual(self.snapshot(), before)
        self.prune(apply=True)
        self.assertEqual(ew.iteration_numbers(self.skill), [])

    def test_new_generated_answer_survives_with_fewer_than_keep_iterations(self):
        workspace = self.create(1)
        answer = self.run_dir(workspace) / "outputs/answer.md"
        answer.write_text("Paid generated answer, not yet graded.\n")
        before = self.snapshot()
        self.assertNotIn("Would remove", self.prune())
        self.prune(apply=True)
        self.assertEqual(self.snapshot(), before)

    def test_newest_meaningful_retention_and_dry_apply_parity(self):
        paths = {n: self.create(n) for n in range(1, 6)}
        # 1: completed old result; 2: paid but ungraded; 3: incomplete grade;
        # 4: newest human evidence; 5: newer pristine scaffold.
        self.change_json(self.run_dir(paths[1]) / "grading.json", lambda d: [
            item.update(passed=True, evidence="Observed") for item in d["assertion_results"]
        ])
        (self.run_dir(paths[2]) / "outputs/answer.md").write_text("Generated answer")
        self.change_json(self.run_dir(paths[3]) / "grading.json", lambda d:
                         d["assertion_results"][0].update(passed=False, evidence="Missing"))
        self.change_json(paths[4] / "feedback.json", lambda d:
                         d["feedback"]["case"].update(with_skill="Human observation"))
        before = self.snapshot()
        dry = self.prune(keep=3)
        self.assertIn("iteration-1 (results or other evidence)", dry)
        self.assertIn("iteration-5 (empty scaffold)", dry)
        self.assertEqual(dry.count("Would remove"), 2)
        self.assertEqual(self.snapshot(), before)
        applied = self.prune(keep=3, apply=True)
        self.assertEqual([line.replace("Would remove", "Removed") for line in dry.splitlines()
                          if line.startswith("Would remove")], applied.splitlines())
        self.assertEqual(ew.iteration_numbers(self.skill), [2, 3, 4])
        after = self.snapshot()
        for path, data in before.items():
            if any(f"iteration-{n}/" in path for n in (2, 3, 4)):
                self.assertEqual(after[path], data)

    def test_output_attempts_and_unknown_files_are_meaningful_even_when_empty(self):
        for number, relative in enumerate((
            "case/with_skill/outputs/answer.md", "case/with_skill/outputs/pi_stdout.jsonl",
            "case/with_skill/outputs/failed_run.json", "case/with_skill/grading.jev.json",
            "notes.md", "case/with_skill/outputs/.generation-interrupted/partial.txt",
        ), 1):
            with self.subTest(relative=relative):
                workspace = self.create(number)
                path = workspace / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("")
                self.assert_meaningful(number)

    def test_partial_uncertain_and_human_grading_evidence_is_meaningful(self):
        changes = (
            lambda d: d["assertion_results"][0].update(passed=True, evidence="Observed"),
            lambda d: d["assertion_results"][0].update(evidence="Cannot resolve from source"),
            lambda d: d.update(notes="Human review note"),
            lambda d: d["assertion_results"][0].update(passed="uncertain"),
        )
        for number, change in enumerate(changes, 1):
            with self.subTest(number=number):
                workspace = self.create(number)
                self.change_json(self.run_dir(workspace) / "grading.json", change)
                self.assert_meaningful(number)

    def test_timing_attempts_or_notes_are_meaningful(self):
        for number, change in enumerate((
            {"exit_code": 1}, {"duration_ms": 1}, {"total_tokens": 30},
            {"attempts": [{"outcome": "timeout"}]}, {"notes": "Human timing note"},
        ), 1):
            with self.subTest(change=change):
                workspace = self.create(number)
                self.change_json(self.run_dir(workspace) / "timing.json", lambda d: d.update(change))
                self.assert_meaningful(number)

    def test_malformed_json_duplicate_keys_and_nonfinite_values_are_meaningful(self):
        number = 0
        for relative in ("feedback.json", "benchmark.json", "case/with_skill/grading.json",
                         "case/with_skill/timing.json"):
            for corruption in ("malformed", "duplicate", "nonfinite"):
                number += 1
                with self.subTest(relative=relative, corruption=corruption):
                    workspace = self.create(number)
                    path = workspace / relative
                    original = path.read_text()
                    if corruption == "malformed":
                        path.write_text("{")
                    elif corruption == "duplicate":
                        # Last-key-wins loading would reproduce the initial value.
                        key = next(iter(json.loads(original)))
                        path.write_text('{"' + key + '": "hidden evidence", ' + original.lstrip()[1:])
                    else:
                        path.write_text('{"value": NaN}')
                    self.assert_meaningful(number)

    def test_json_type_changes_are_not_equal_to_scaffold(self):
        workspace = self.create(1)
        self.change_json(self.run_dir(workspace) / "grading.json", lambda d:
                         d["summary"].update(passed=False))
        self.assert_meaningful(1)

    def test_custom_prompts_runs_and_changed_fixtures_are_meaningful(self):
        workspace = self.create(1)
        prompt = self.run_dir(workspace) / "prompt.md"
        prompt.write_text(prompt.read_text() + "Custom instruction\n")
        self.assert_meaningful(1)
        self.create(2, ("old_skill",))
        self.assert_meaningful(2)
        self.create(3)
        (self.skill / "SKILL.md").write_text("Changed skill version\n")
        self.assert_meaningful(3)
        self.create(4)
        self.change_json(self.fixture, lambda d: d["evals"][0].update(prompt="Changed task"))
        self.assert_meaningful(4)

    def test_malformed_fixture_preserves_existing_workspace(self):
        self.create(1)
        self.fixture.write_text("{")
        self.assert_meaningful(1)
        before = self.snapshot()
        self.prune(apply=True)
        self.assertEqual(self.snapshot(), before)

    def test_missing_scaffold_file_and_unknown_directory_are_meaningful(self):
        workspace = self.create(1)
        (workspace / "benchmark.json").unlink()
        self.assert_meaningful(1)
        workspace = self.create(2)
        (workspace / "unknown-empty-directory").mkdir()
        self.assert_meaningful(2)

    def test_unreadable_output_directory_is_not_an_empty_scaffold(self):
        workspace = self.create(1)
        outputs = self.run_dir(workspace) / "outputs"
        original = Path.iterdir

        def unreadable(path):
            if path == outputs:
                raise PermissionError("Cannot inspect saved outputs")
            return original(path)

        before = self.snapshot()
        with patch.object(Path, "iterdir", unreadable):
            self.assertTrue(ew.iteration_has_results(self.skill, 1))
            self.prune(apply=True)
        self.assertEqual(self.snapshot(), before)

    def test_symlinks_are_evidence_and_targets_are_never_traversed(self):
        target = self.root / "outside"
        target.mkdir()
        (target / "valuable.md").write_text("Do not touch")
        workspace = self.create(1)
        (self.run_dir(workspace) / "outputs/linked-directory").symlink_to(target, target_is_directory=True)
        self.assert_meaningful(1)
        workspace = self.create(2)
        (workspace / "broken-link").symlink_to(self.root / "missing")
        self.assert_meaningful(2)
        workspace = self.create(3)
        grading = self.run_dir(workspace) / "grading.json"
        saved = target / "grading.json"
        saved.write_bytes(grading.read_bytes())
        grading.unlink()
        grading.symlink_to(saved)
        self.assert_meaningful(3)
        before = self.snapshot()
        self.prune(keep=3)
        self.assertEqual(self.snapshot(), before)
        self.prune(keep=3, apply=True)
        self.assertEqual(self.snapshot(), before)
        # An older evidence-bearing iteration is still intentionally prunable;
        # deleting its symlink must leave the destination unchanged.
        self.prune(keep=2, apply=True)
        self.assertFalse((self.workspaces / self.skill.name / "iteration-1").exists())
        self.assertEqual((target / "valuable.md").read_text(), "Do not touch")

    def test_symlinked_iteration_root_is_meaningful(self):
        target = self.root / "external-iteration"
        target.mkdir()
        (target / "note.md").write_text("External evidence")
        parent = self.workspaces / self.skill.name
        parent.mkdir(parents=True)
        (parent / "iteration-1").symlink_to(target, target_is_directory=True)
        self.assert_meaningful(1)
        before = self.snapshot()
        self.prune(apply=True)
        self.assertEqual(self.snapshot(), before)

    def test_nonpositive_keep_still_rejected(self):
        self.create(1)
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "at least 1"):
            self.prune(keep=0, apply=True)
        self.assertEqual(self.snapshot(), before)


if __name__ == "__main__":
    unittest.main()
