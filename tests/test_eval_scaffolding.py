"""Offline regressions for preserving populated evaluation input snapshots."""
import contextlib
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import eval_workflow as ew


class ScaffoldingEvidenceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.skill = self.root / 'skills/test'
        (self.skill / 'evals').mkdir(parents=True)
        (self.skill / 'references').mkdir()
        (self.skill / 'SKILL.md').write_text('Trusted writing instructions')
        (self.skill / 'references/rules.md').write_text('Preserve source facts')
        self.case = {'id': 'case', 'prompt': 'Write ALPHA', 'expected_output': 'ALPHA',
                     'assertions': ['Says ALPHA', 'Does not invent facts']}
        self.cases = [self.case]
        self.save_fixture()
        for name, value in [('ROOT', self.root), ('SKILLS_DIR', self.root / 'skills'),
                            ('WORKSPACES_DIR', self.root / 'workspaces')]:
            patcher = patch.object(ew, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.workspace = self.init()
        self.run = self.workspace / 'case/with_skill'

    def save_fixture(self):
        (self.skill / 'evals/evals.json').write_text(json.dumps({'skill_name': 'test', 'evals': self.cases}))

    def init(self, *, force=False, reset=False, iteration='1', runs=('with_skill', 'without_skill')):
        with contextlib.redirect_stdout(io.StringIO()):
            return ew.init_skill_workspace(self.skill, iteration, runs, force, reset)

    def populate(self, run=None, *, graded=True):
        run = run or self.run
        (run / 'outputs/answer.md').write_text('ALPHA')
        if graded:
            grading = ew.load_json(run / 'grading.json')
            for result in grading['assertion_results']:
                result.update(passed=True, evidence='Seen in ALPHA')
            grading['grader'] = {'model': 'offline'}
            grading['notes'] = 'Keep this human note'
            (run / 'grading.json').write_text(json.dumps(grading))
            ew.summarise_grading(run / 'grading.json')

    def snapshot(self):
        return {str(p.relative_to(self.workspace)): p.read_bytes()
                for p in self.workspace.rglob('*') if p.is_file()}

    def assert_rejected_unchanged(self, **kwargs):
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'fresh iteration'):
            self.init(**kwargs)
        self.assertEqual(self.snapshot(), before)

    def test_task_change_cannot_pair_new_prompt_with_old_grading(self):
        self.populate()
        self.case['prompt'] = 'Write BETA'
        self.save_fixture()
        self.assert_rejected_unchanged(force=True)
        self.assertIn('Write ALPHA', ew.grade_prompt(self.run / 'grading.json'))

    def test_assertion_only_change_is_rejected_for_an_ungraded_answer(self):
        self.populate(graded=False)
        self.case['assertions'][0] = 'Says BETA'
        self.save_fixture()
        self.assert_rejected_unchanged(force=True)

    def test_expected_output_only_change_is_rejected(self):
        self.populate()
        self.case['expected_output'] = 'BETA'
        self.save_fixture()
        self.assert_rejected_unchanged(force=True)

    def test_assertion_reordering_is_not_the_same_rubric(self):
        self.populate()
        self.case['assertions'].reverse()
        self.save_fixture()
        self.assert_rejected_unchanged(force=True)

    def test_skill_or_reference_changes_preserve_existing_generation_inputs(self):
        self.populate()
        for path in (self.skill / 'SKILL.md', self.skill / 'references/rules.md'):
            with self.subTest(path=path):
                original = path.read_text()
                path.write_text('Different trusted instructions')
                self.assert_rejected_unchanged(force=True)
                path.write_text(original)

    def test_input_file_list_change_is_rejected(self):
        self.populate()
        self.case['files'] = ['other-source.md']
        self.save_fixture()
        self.assert_rejected_unchanged(force=True)

    def test_reset_results_cannot_retask_a_saved_answer(self):
        self.populate()
        self.case['prompt'] = 'Write BETA'
        self.save_fixture()
        self.assert_rejected_unchanged(force=True, reset=True)

    def test_nonforced_init_cannot_fill_missing_metadata_with_another_task(self):
        self.populate()
        (self.run / 'grading.json').unlink()
        self.case['prompt'] = 'Write BETA'
        self.save_fixture()
        self.assert_rejected_unchanged()

    def test_jev_only_evidence_is_protected(self):
        (self.run / 'grading.jev.json').write_text('{"assertion_results": []}')
        self.case['prompt'] = 'Write BETA'
        self.save_fixture()
        self.assert_rejected_unchanged(force=True)

    def test_recorded_failed_timing_is_protected_without_an_answer(self):
        timing = ew.load_json(self.run / 'timing.json')
        timing['exit_code'] = 1
        (self.run / 'timing.json').write_text(json.dumps(timing))
        self.case['prompt'] = 'Write BETA'
        self.save_fixture()
        self.assert_rejected_unchanged(force=True)

    def test_recorded_verdict_is_protected_without_an_answer(self):
        self.populate()
        (self.run / 'outputs/answer.md').unlink()
        self.case['prompt'] = 'Write BETA'
        self.save_fixture()
        self.assert_rejected_unchanged(force=True)

    def test_uncertain_grades_and_recheck_evidence_are_preserved(self):
        original = ew.load_json(self.run / 'grading.json')
        for evidence in ('grader', 'deterministic_checks', 'evidence', 'recheck'):
            with self.subTest(evidence=evidence):
                grading = copy.deepcopy(original)
                if evidence in ('grader', 'deterministic_checks'):
                    grading[evidence] = {}
                else:
                    grading['assertion_results'][0][evidence] = 'Unresolved evidence'
                (self.run / 'grading.json').write_text(json.dumps(grading))
                before = (self.run / 'grading.json').read_bytes()
                self.init(force=True)
                self.assertEqual((self.run / 'grading.json').read_bytes(), before)
                self.case['prompt'] = 'Write BETA'
                self.save_fixture()
                self.assert_rejected_unchanged(force=True)
                self.case['prompt'] = 'Write ALPHA'
                self.save_fixture()

    def test_missing_or_malformed_snapshot_fails_closed(self):
        self.populate()
        grading_path = self.run / 'grading.json'
        saved = grading_path.read_bytes()
        for invalid in (None, '{', '[]', '{"assertion_results": [null]}'):
            with self.subTest(invalid=invalid):
                if invalid is None:
                    grading_path.unlink()
                else:
                    grading_path.write_text(invalid)
                self.assert_rejected_unchanged(force=True)
                grading_path.write_bytes(saved)
        (self.run / 'prompt.md').unlink()
        self.assert_rejected_unchanged(force=True)

    def test_saved_identity_fields_cannot_be_relabelled(self):
        self.populate()
        original = ew.load_json(self.run / 'grading.json')
        for field in ('skill_name', 'eval_id', 'run', 'prompt', 'expected_output'):
            with self.subTest(field=field):
                changed = copy.deepcopy(original)
                changed[field] = 'wrong'
                (self.run / 'grading.json').write_text(json.dumps(changed))
                self.assert_rejected_unchanged(force=True)
        (self.run / 'grading.json').write_text(json.dumps(original))

    def test_later_conflict_does_not_modify_earlier_empty_case_or_summaries(self):
        self.populate()
        self.cases.insert(0, {**copy.deepcopy(self.case), 'id': 'earlier'})
        self.init()
        (self.workspace / 'feedback.json').write_text('{"human": "keep"}')
        (self.workspace / 'benchmark.json').write_text('{"old": "summary"}')
        for case in self.cases:
            case['prompt'] = 'Changed task'
        self.save_fixture()
        self.assert_rejected_unchanged(force=True)

    def test_non_with_skill_runs_are_protected(self):
        for run_name in ('without_skill', 'custom_baseline'):
            with self.subTest(run=run_name):
                self.init(runs=(run_name,))
                self.populate(self.workspace / f'case/{run_name}')
                self.case['prompt'] = 'Write BETA'
                self.save_fixture()
                self.assert_rejected_unchanged(force=True, runs=(run_name,))
                self.case['prompt'] = 'Write ALPHA'
                self.save_fixture()

    def test_identical_inputs_keep_recorded_grades_and_answer(self):
        self.populate()
        paths = [self.run / 'prompt.md', self.run / 'grading.json', self.run / 'outputs/answer.md']
        before = {path: path.read_bytes() for path in paths}
        self.init(force=True)
        self.assertEqual({path: path.read_bytes() for path in paths}, before)

    def test_identical_inputs_can_explicitly_reset_grading(self):
        self.populate()
        self.init(force=True, reset=True)
        self.assertEqual((self.run / 'outputs/answer.md').read_text(), 'ALPHA')
        self.assertTrue(all(x['passed'] is None for x in ew.load_json(self.run / 'grading.json')['assertion_results']))

    def test_empty_scaffolds_can_refresh(self):
        self.case.update(prompt='Write BETA', expected_output='BETA', assertions=['Says BETA'])
        self.save_fixture()
        self.init(force=True)
        self.assertIn('Write BETA', (self.run / 'prompt.md').read_text())
        self.assertEqual(ew.load_json(self.run / 'grading.json')['prompt'], 'Write BETA')

    def test_cli_reports_changed_evidence_without_writing(self):
        self.populate()
        self.case['prompt'] = 'Write BETA'
        self.save_fixture()
        before = self.snapshot()
        with patch.object(sys, 'argv', ['eval_workflow.py', 'init', '--skill', 'test',
                                       '--iteration', '1', '--force']), \
             contextlib.redirect_stderr(io.StringIO()) as errors:
            result = ew.main()
        self.assertEqual(result, 1)
        self.assertIn('fresh iteration', errors.getvalue())
        self.assertEqual(self.snapshot(), before)

    def test_fresh_iteration_uses_new_inputs_and_preserves_old_evidence(self):
        self.populate()
        before = self.snapshot()
        self.case['prompt'] = 'Write BETA'
        self.save_fixture()
        fresh = self.init(iteration=None)
        self.assertEqual(fresh.name, 'iteration-2')
        self.assertIn('Write BETA', (fresh / 'case/with_skill/prompt.md').read_text())
        self.assertEqual(self.snapshot(), before)


if __name__ == '__main__':
    unittest.main()
