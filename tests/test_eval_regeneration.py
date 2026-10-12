"""Offline answer publication and grade-invalidation regressions; no model calls."""
import copy
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import eval_workflow as ew


class RegenerationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.workspace = self.root / 'iteration-1'
        self.run = self.workspace / 'case/with_skill'
        self.outputs = self.run / 'outputs'
        self.outputs.mkdir(parents=True)
        self.prompt = self.run / 'prompt.md'
        self.prompt.write_text('Original task and sources')
        self.answer = self.outputs / 'answer.md'
        self.answer.write_text('old answer')
        self.grading = self.run / 'grading.json'
        self.rubric = {
            'skill_name': 'test', 'eval_id': 'case', 'run': 'with_skill',
            'prompt': 'Original task and sources', 'expected_output': 'Expected',
            'assertion_results': [{'text': 'A heading', 'passed': True, 'evidence': 'old evidence',
                                   'recheck': {'passed': True}}],
            'summary': {'passed': 1, 'failed': 0, 'ungraded': 0, 'total': 1, 'pass_rate': 1},
            'grader': {'model': 'old grader'}, 'deterministic_checks': {'passed': True},
            'notes': 'Keep this human note',
        }
        self.grading.write_text(json.dumps(self.rubric))
        self.timing = self.run / 'timing.json'
        self.timing.write_text(json.dumps({'model': 'old model', 'total_tokens': 33, 'notes': 'keep'}))
        self.benchmark = self.workspace / 'benchmark.json'
        self.benchmark.write_text('old benchmark')
        self.jev = self.run / 'grading.jev.json'
        self.jev.write_text('old jev')
        for name in ('grading_result.json', 'grader_stdout.jsonl', 'grader_stderr.txt',
                     'grader_stdout.attempt-2.jsonl', 'grader_stderr.attempt-2.txt', 'grader_stdout.txt'):
            (self.outputs / name).write_text('old grade artifact')
        (self.outputs / 'user-notes.md').write_text('retain')
        root_patch = patch.object(ew, 'ROOT', self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)

    def reply(self, text='new answer', **overrides):
        fields = dict(executor='pi', model='new model', reasoning_effort='low', command=['fake'],
                      exit_code=0, duration_ms=10, total_tokens=12, text=text,
                      attempts=[{'attempt': 1, 'outcome': 'success'}], details={})
        fields.update(overrides)
        return ew.ModelReply(**fields)

    def generate(self, *, executor='pi', force=True):
        ew.run_eval_prompt(self.prompt, executor=executor, model='new model', reasoning_effort='low', force=force)

    def success(self, prompt, **kwargs):
        target = kwargs['result_path']
        target.write_text('new answer')
        return self.reply()

    def snapshot(self):
        paths = [self.answer, self.grading, self.timing, self.benchmark, self.jev,
                 self.outputs / 'grading_result.json']
        return {p: p.read_bytes() for p in paths if p.exists()}

    def assert_preserved(self, before):
        for path, data in before.items():
            self.assertEqual(path.read_bytes(), data, str(path))
        self.assertEqual(list(self.outputs.glob('.generation-*')), [])

    def test_success_invalidates_both_graders_and_benchmark_but_preserves_rubric(self):
        with patch.object(ew, 'invoke_model', self.success):
            self.generate()
        grade = json.loads(self.grading.read_text())
        expected = copy.deepcopy(self.rubric)
        expected['assertion_results'] = [{'text': 'A heading', 'passed': None, 'evidence': ''}]
        expected['summary'] = {'passed': 0, 'failed': 0, 'ungraded': 1, 'total': 1, 'pass_rate': None}
        expected.pop('grader'); expected.pop('deterministic_checks')
        self.assertEqual(grade, expected)
        self.assertEqual(self.answer.read_text(), 'new answer')
        self.assertEqual(json.loads(self.timing.read_text())['model'], 'new model')
        self.assertFalse(self.jev.exists())
        self.assertFalse(self.benchmark.exists())
        self.assertEqual(sorted(p.name for p in self.outputs.iterdir()), ['answer.md', 'user-notes.md'])

    def test_regenerated_answer_is_not_skipped_by_default_grading(self):
        with patch.object(ew, 'invoke_model', self.success):
            self.generate()
        payload = {'assertion_results': [{'index': 1, 'text': 'A heading', 'passed': False, 'evidence': 'Absent'}]}
        with patch.object(ew, 'invoke_model', return_value=self.reply(json.dumps(payload))) as invoke:
            ew.grade_eval_output(self.grading, executor='pi', model='other', reasoning_effort='low', force=False)
        invoke.assert_called_once()
        self.assertIs(json.loads(self.grading.read_text())['assertion_results'][0]['passed'], False)

    def test_failed_forced_regeneration_preserves_current_evidence(self):
        for executor in ('pi', 'codex'):
            with self.subTest(executor=executor):
                before = self.snapshot()
                def failed(prompt, **kwargs):
                    kwargs['result_path'].write_text('partial answer')
                    raise ew.InvocationError('failed attempt', self.reply(exit_code=1))
                with patch.object(ew, 'invoke_model', failed), self.assertRaises(ValueError):
                    self.generate(executor=executor)
                self.assert_preserved(before)
                self.assertEqual(json.loads((self.outputs / 'failed_run.json').read_text())['exit_code'], 1)

    def test_missing_or_empty_output_does_not_reuse_old_answer(self):
        for content in (None, '', '  \n\t'):
            with self.subTest(content=content):
                before = self.snapshot()
                def no_output(prompt, **kwargs):
                    if content is not None:
                        kwargs['result_path'].write_text(content)
                    return self.reply()
                with patch.object(ew, 'invoke_model', no_output), self.assertRaisesRegex(ValueError, 'nonempty'):
                    self.generate(executor='codex')
                self.assert_preserved(before)

    def test_initial_failure_never_publishes_partial_answer(self):
        self.answer.unlink()
        def failed(prompt, **kwargs):
            kwargs['result_path'].write_text('partial')
            raise ew.InvocationError('failed', self.reply(exit_code=1))
        with patch.object(ew, 'invoke_model', failed), self.assertRaises(ValueError):
            self.generate(force=False)
        self.assertFalse(self.answer.exists())
        self.assertEqual(json.loads(self.timing.read_text())['exit_code'], 1)
        self.assertEqual(list(self.outputs.glob('.generation-*')), [])

    def test_success_removes_previous_attempt_failure(self):
        (self.outputs / 'failed_run.json').write_text('old failure')
        with patch.object(ew, 'invoke_model', self.success):
            self.generate()
        self.assertFalse((self.outputs / 'failed_run.json').exists())

    def test_nonforced_existing_output_is_unchanged_without_invocation(self):
        before = self.snapshot()
        with patch.object(ew, 'invoke_model') as invoke:
            self.generate(force=False)
        invoke.assert_not_called()
        self.assert_preserved(before)

    def test_invalid_metadata_is_rejected_before_invocation(self):
        for path, content in ((self.timing, '{'), (self.grading, '{'),
                              (self.grading, '{"assertion_results": [null]}')):
            with self.subTest(path=path, content=content):
                original = path.read_bytes()
                path.write_text(content)
                before = self.snapshot()
                with patch.object(ew, 'invoke_model') as invoke, self.assertRaises(ValueError):
                    self.generate()
                invoke.assert_not_called()
                self.assert_preserved(before)
                path.write_bytes(original)

    def test_filesystem_error_during_generation_preserves_evidence(self):
        before = self.snapshot()
        with patch.object(ew, 'invoke_model', side_effect=OSError('disk error')), self.assertRaises(OSError):
            self.generate()
        self.assert_preserved(before)

    def test_interruption_preserves_current_evidence(self):
        before = self.snapshot()
        with patch.object(ew, 'invoke_model', side_effect=KeyboardInterrupt), self.assertRaises(KeyboardInterrupt):
            self.generate()
        self.assert_preserved(before)

    def test_invalidation_failure_prevents_answer_replacement(self):
        # A path-type conflict must fail closed rather than retain a grade for a new answer.
        self.jev.unlink(); self.jev.mkdir()
        with patch.object(ew, 'invoke_model', self.success), self.assertRaises(OSError):
            self.generate()
        self.assertEqual(self.answer.read_text(), 'old answer')
        self.assertEqual(list(self.outputs.glob('.generation-*')), [])

    def test_both_executors_receive_a_fresh_staging_path(self):
        for executor in ('pi', 'codex'):
            with self.subTest(executor=executor):
                def fresh(prompt, **kwargs):
                    self.assertNotEqual(kwargs['result_path'], self.answer)
                    self.assertFalse(kwargs['result_path'].exists())
                    return self.success(prompt, **kwargs)
                with patch.object(ew, 'invoke_model', fresh):
                    self.generate(executor=executor)

    def test_codex_exit_zero_without_output_cannot_accept_old_answer(self):
        before = self.snapshot()
        completed = subprocess.CompletedProcess(['codex'], 0, 'tokens used: 12', '')
        with patch.object(ew, 'run_process', return_value=completed), self.assertRaisesRegex(ValueError, 'without writing'):
            self.generate(executor='codex')
        self.assert_preserved(before)

    def test_codex_partial_file_then_nonzero_is_not_published(self):
        before = self.snapshot()
        def process(command, **kwargs):
            Path(command[command.index('-o') + 1]).write_text('partial output')
            return subprocess.CompletedProcess(command, 1, '', 'failed')
        with patch.object(ew, 'run_process', process), self.assertRaises(ValueError):
            self.generate(executor='codex')
        self.assert_preserved(before)

    def test_initial_success_resets_orphaned_grades(self):
        self.answer.unlink()
        with patch.object(ew, 'invoke_model', self.success):
            self.generate(force=False)
        self.assertIsNone(json.loads(self.grading.read_text())['assertion_results'][0]['passed'])
        self.assertFalse(self.jev.exists())

    def test_failure_without_reply_keeps_timing_and_records_attempt(self):
        before = self.snapshot()
        with patch.object(ew, 'invoke_model', side_effect=ew.InvocationError('no reply')), self.assertRaises(ValueError):
            self.generate()
        self.assert_preserved(before)
        failure = json.loads((self.outputs / 'failed_run.json').read_text())
        self.assertEqual(failure['model'], 'new model')
        self.assertEqual(failure['error'], 'no reply')

    def test_staging_timing_failure_preserves_current_evidence(self):
        before = self.snapshot()
        original = ew.write_json
        def fail_timing(path, data, *, force):
            if path.name == 'timing.json':
                raise OSError('no space')
            return original(path, data, force=force)
        with patch.object(ew, 'invoke_model', self.success), patch.object(ew, 'write_json', fail_timing), self.assertRaises(OSError):
            self.generate()
        self.assert_preserved(before)

    def test_stale_prompt_prevents_invocation_or_invalidation(self):
        before = self.snapshot()
        with patch.object(ew, 'invoke_model') as invoke, self.assertRaises(ValueError):
            ew.run_eval_prompt(self.prompt, executor='pi', model='m', reasoning_effort='low',
                               force=True, expected={('case', 'with_skill'): 'different'})
        invoke.assert_not_called()
        self.assert_preserved(before)


if __name__ == '__main__':
    unittest.main()
