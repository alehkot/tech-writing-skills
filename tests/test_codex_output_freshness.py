"""Offline Codex output freshness and publication regressions; no model calls."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import eval_workflow as ew


class CodexOutputTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.output = self.root / 'grading_result.json'
        self.old = json.dumps(self.payload('old evidence'))
        self.output.write_text(self.old)
        self.destinations = []

    @staticmethod
    def payload(evidence):
        return {'assertion_results': [
            {'index': 1, 'text': 'A heading', 'passed': True, 'evidence': evidence}], 'notes': ''}

    def process(self, content=None, code=0, timeout=False):
        def run(command, **kwargs):
            destination = Path(command[command.index('-o') + 1])
            self.destinations.append(destination)
            if content is not None:
                destination.write_text(content)
            if timeout:
                raise ew.InvocationTimeout('partial stdout', 'partial stderr')
            return subprocess.CompletedProcess(command, code, 'tokens used\n42', 'diagnostic')
        return run

    def invoke(self, process, *, destination=True, schema=True):
        with patch.object(ew, 'run_process', process):
            return ew.invoke_codex('Grade this answer', model='test-model', reasoning_effort='low',
                result_path=self.output if destination else None, stream_stem=self.root / 'grader',
                schema=ew.GRADING_SCHEMA if schema else None, timeout_seconds=5)

    def assert_clean(self):
        for path in self.destinations:
            self.assertFalse(path.exists())
            self.assertFalse(path.parent.exists())

    def test_silent_success_never_accepts_old_output(self):
        with self.assertRaises(ew.InvocationError) as caught:
            self.invoke(self.process())
        self.assertEqual(caught.exception.reply.attempts[0]['outcome'], 'missing_output')
        self.assertEqual(self.output.read_text(), self.old)
        self.assert_clean()

    def test_fresh_valid_output_replaces_old_after_validation(self):
        fresh = json.dumps(self.payload('fresh evidence'))
        fake = self.process(fresh)
        def inspect(command, **kwargs):
            destination = Path(command[command.index('-o') + 1])
            self.assertNotEqual(destination, self.output)
            self.assertFalse(destination.exists())
            self.assertEqual(self.output.read_text(), self.old)
            result = fake(command, **kwargs)
            self.assertEqual(self.output.read_text(), self.old)
            return result
        reply = self.invoke(inspect)
        self.assertEqual(reply.text, fresh)
        self.assertEqual(self.output.read_text(), fresh)
        self.assertEqual(reply.attempts[0]['outcome'], 'success')
        self.assert_clean()

    def test_failure_preserves_previous_output(self):
        for kind, content, code, timeout, outcome in (
            ('exit', json.dumps(self.payload('partial')), 1, False, 'nonzero_exit'),
            ('timeout', '{partial', 0, True, 'timeout'),
            ('invalid-json', '{', 0, False, 'off_schema'),
            ('off-schema', '{}', 0, False, 'off_schema'),
        ):
            with self.subTest(kind=kind):
                self.output.write_text(self.old)
                with self.assertRaises(ew.InvocationError) as caught:
                    self.invoke(self.process(content, code, timeout))
                self.assertEqual(caught.exception.reply.attempts[0]['outcome'], outcome)
                self.assertEqual(self.output.read_text(), self.old)
                self.assertTrue((self.root / 'grader_stdout.txt').exists())
                self.assertTrue((self.root / 'grader_stderr.txt').exists())
                self.assert_clean()

    def test_failed_first_attempt_does_not_publish_output(self):
        self.output.unlink()
        with self.assertRaises(ew.InvocationError):
            self.invoke(self.process('{}'))
        self.assertFalse(self.output.exists())
        self.assert_clean()

    def test_same_content_is_allowed_when_freshly_written(self):
        reply = self.invoke(self.process(self.old))
        self.assertEqual(reply.text, self.old)
        self.assertEqual(self.output.read_text(), self.old)
        self.assert_clean()

    def test_no_destination_returns_validated_text_and_cleans_scratch(self):
        fresh = json.dumps(self.payload('fresh evidence'))
        reply = self.invoke(self.process(fresh), destination=False)
        self.assertEqual(reply.text, fresh)
        self.assertEqual(self.output.read_text(), self.old)
        self.assert_clean()

    def test_unstructured_generation_still_publishes_text(self):
        reply = self.invoke(self.process('Fresh plain text'), schema=False)
        self.assertEqual(reply.text, 'Fresh plain text')
        self.assertEqual(self.output.read_text(), reply.text)
        self.assert_clean()

    def test_result_named_schema_does_not_reuse_schema_as_output(self):
        self.output = self.root / 'schema.json'
        self.output.write_text(self.old)
        with self.assertRaises(ew.InvocationError) as caught:
            self.invoke(self.process())
        self.assertEqual(caught.exception.reply.attempts[0]['outcome'], 'missing_output')
        self.assertEqual(self.output.read_text(), self.old)
        self.assert_clean()

    def test_publication_failure_preserves_old_result(self):
        fresh = json.dumps(self.payload('fresh evidence'))
        with patch.object(Path, 'replace', side_effect=OSError('disk failure')):
            with self.assertRaisesRegex(OSError, 'disk failure'):
                self.invoke(self.process(fresh))
        self.assertEqual(self.output.read_text(), self.old)
        self.assert_clean()

    def test_forced_regrading_does_not_commit_stale_verdict(self):
        run = self.root / 'case/with_skill'
        outputs = run / 'outputs'
        outputs.mkdir(parents=True)
        grading = run / 'grading.json'
        grading.write_text(json.dumps({
            'skill_name': 'test', 'eval_id': 'case', 'run': 'with_skill',
            'prompt': 'Write a heading', 'expected_output': 'A heading',
            'assertion_results': [{'text': 'A heading', 'passed': None, 'evidence': ''}],
            'notes': 'Human note',
        }))
        (outputs / 'answer.md').write_text('Changed answer without heading')
        self.output = outputs / 'grading_result.json'
        self.output.write_text(self.old)
        before = grading.read_bytes()
        with patch.object(ew, 'ROOT', self.root), patch.object(ew, 'run_process', self.process()):
            with self.assertRaisesRegex(ValueError, 'without writing'):
                ew.grade_eval_output(grading, executor='codex', model='test-model',
                    reasoning_effort='low', force=True, timeout_seconds=5)
        self.assertEqual(grading.read_bytes(), before)
        self.assertEqual(self.output.read_text(), self.old)
        self.assert_clean()


if __name__ == '__main__':
    unittest.main()
