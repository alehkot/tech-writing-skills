"""Offline response-contract regressions; no provider processes are launched."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import eval_workflow as ew


class TriggerResponseTests(unittest.TestCase):
    def setUp(self):
        self.catalog = {'task-docs-writer': 'Write tasks', 'reference-docs-writer': 'Write references'}
        self.batch = [
            {'skill': 'task-docs-writer', 'query': 'Write a runbook', 'should_trigger': True},
            {'skill': 'task-docs-writer', 'query': 'Write a poem', 'should_trigger': False},
        ]
        self.valid = {'results': [{'index': 1, 'skill': 'task-docs-writer'},
                                  {'index': 2, 'skill': 'none'}]}

    def route(self, payload, executor='pi'):
        with patch.object(ew, 'invoke_model', return_value=SimpleNamespace(text=json.dumps(payload))):
            return ew.run_trigger_batch(self.batch, self.catalog, model='offline',
                                        reasoning_effort='low', executor=executor)

    def cli(self, payloads, *, batch_size=2):
        replies = [SimpleNamespace(text=json.dumps(p)) for p in payloads]
        out, err = io.StringIO(), io.StringIO()
        with patch.object(ew, 'skill_descriptions', return_value=self.catalog), \
             patch.object(ew, 'trigger_pool', return_value=self.batch), \
             patch.object(ew, 'invoke_model', side_effect=replies) as invoke, \
             patch.object(sys, 'argv', ['eval_workflow.py', 'trigger-eval',
                                       '--batch-size', str(batch_size), '--verbose']), \
             contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = ew.main()
        return code, out.getvalue(), err.getvalue(), invoke.call_count

    def test_valid_and_shuffled_results_align_by_index(self):
        self.assertEqual(self.route(self.valid), ['task-docs-writer', 'none'])
        self.valid['results'].reverse()
        self.assertEqual(self.route(self.valid), ['task-docs-writer', 'none'])

    def test_other_catalog_skill_is_valid_even_if_not_query_owner(self):
        self.valid['results'][0]['skill'] = 'reference-docs-writer'
        self.assertEqual(self.route(self.valid), ['reference-docs-writer', 'none'])

    def test_surrounding_whitespace_keeps_existing_normalization(self):
        self.valid['results'][0]['skill'] = ' task-docs-writer\n'
        self.valid['results'][1]['skill'] = '\tnone '
        self.assertEqual(self.route(self.valid), ['task-docs-writer', 'none'])

    def test_empty_response_is_not_implicit_abstention(self):
        self.assertEqual(ew.schema_issues({'results': []}, ew.TRIGGER_SCHEMA), [])
        with self.assertRaisesRegex(ValueError, 'expected 2 results'):
            self.route({'results': []})

    def test_missing_and_extra_results_are_rejected(self):
        for results in (self.valid['results'][:1], self.valid['results'] * 2):
            with self.subTest(results=results), self.assertRaisesRegex(ValueError, 'expected 2 results'):
                self.route({'results': results})

    def test_duplicate_indices_cannot_overwrite_a_prediction(self):
        self.valid['results'][1]['index'] = 1
        with self.assertRaisesRegex(ValueError, 'duplicate index'):
            self.route(self.valid)

    def test_out_of_range_indices_are_rejected(self):
        for index in (-1, 0, 3, 999):
            with self.subTest(index=index), self.assertRaisesRegex(ValueError, 'out-of-range'):
                self.valid['results'][0]['index'] = index
                self.route(self.valid)

    def test_indices_must_be_integers_not_booleans(self):
        for index in (True, False, '1', 1.0, None):
            with self.subTest(index=index), self.assertRaisesRegex(ValueError, 'expected an integer'):
                self.valid['results'][0]['index'] = index
                self.route(self.valid)

    def test_unknown_skill_and_noncanonical_abstention_are_rejected(self):
        for skill in ('missing-skill', '', 'NONE', 'None', 'task-docs-writer because...'):
            with self.subTest(skill=skill), self.assertRaisesRegex(ValueError, 'unknown skill'):
                self.valid['results'][0]['skill'] = skill
                self.route(self.valid)

    def test_nonstring_prediction_is_not_coerced(self):
        for skill in (None, 1, True, [], {}):
            with self.subTest(skill=skill), self.assertRaisesRegex(ValueError, 'expected a string'):
                self.valid['results'][0]['skill'] = skill
                self.route(self.valid)

    def test_malformed_shapes_fail_cleanly(self):
        payloads = [None, [], {}, {'results': {}}, {'results': [None]},
                    {'results': [{'index': 1}]}, {'results': [{'skill': 'none'}]},
                    {**self.valid, 'extra': 1}]
        for payload in payloads:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                self.route(payload)

    def test_invalid_json_cli_fails_without_scores(self):
        with patch.object(ew, 'skill_descriptions', return_value=self.catalog), \
             patch.object(ew, 'trigger_pool', return_value=self.batch), \
             patch.object(ew, 'invoke_model', return_value=SimpleNamespace(text='{')), \
             patch.object(sys, 'argv', ['eval_workflow.py', 'trigger-eval']), \
             contextlib.redirect_stdout(io.StringIO()) as out, \
             contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(ew.main(), 1)
        self.assertNotIn('accuracy', out.getvalue())

    def test_negative_query_without_response_does_not_score_100_percent(self):
        self.batch = self.batch[1:]
        code, out, err, calls = self.cli([{'results': []}])
        self.assertEqual((code, calls), (1, 1))
        self.assertIn('invalid trigger routing response', err)
        for label in ('precision', 'recall', 'accuracy', '100%'):
            self.assertNotIn(label, out)

    def test_later_invalid_batch_aborts_without_partial_metrics(self):
        code, out, err, calls = self.cli([
            {'results': [{'index': 1, 'skill': 'task-docs-writer'}]}, {'results': []}], batch_size=1)
        self.assertEqual((code, calls), (1, 2))
        self.assertIn('routed 1/2', out)
        self.assertNotIn('precision', out)
        self.assertNotIn('accuracy', out)
        self.assertIn('expected 1 results', err)

    def test_valid_cli_retains_real_misroutes_in_metrics(self):
        self.valid['results'][0]['skill'] = 'reference-docs-writer'
        code, out, err, calls = self.cli([self.valid])
        self.assertEqual((code, err, calls), (0, '', 1))
        self.assertIn('overall routing accuracy: 1/2 (50%)', out)
        self.assertIn('MISROUTED', out)

    def test_process_to_response_contract_for_both_executors(self):
        # Exercise actual adapter schema checks: [] is valid JSON/schema, so the
        # routing boundary must still reject it. Valid shuffled replies survive.
        for executor in ('pi', 'codex'):
            for payload, accepted in (({'results': []}, False),
                                      ({'results': list(reversed(self.valid['results']))}, True)):
                with self.subTest(executor=executor, accepted=accepted):
                    def process(command, **kwargs):
                        body = json.dumps(payload)
                        if executor == 'codex':
                            Path(command[command.index('-o') + 1]).write_text(body)
                            stdout = ''
                        else:
                            stdout = json.dumps({'type': 'message_end', 'message': {
                                'role': 'assistant', 'content': [{'type': 'text', 'text': body}],
                                'stopReason': 'stop'}})
                        return subprocess.CompletedProcess(command, 0, stdout, '')
                    with patch.object(ew, 'run_process', side_effect=process) as run, \
                         patch.object(ew, 'resolve_pi_executable', return_value=Path('/fake/pi')), \
                         patch.object(ew, 'resolve_node_bin_dir', return_value=Path('/fake/node')), \
                         patch.object(ew, 'source_pi_api_key', return_value='test-only-placeholder'), \
                         patch.object(ew, 'probe_pi_cli_version', return_value='0.84.2'):
                        def call():
                            return ew.run_trigger_batch(self.batch, self.catalog, model='offline',
                                                        reasoning_effort='low', executor=executor)
                        if accepted:
                            self.assertEqual(call(), ['task-docs-writer', 'none'])
                        else:
                            with self.assertRaisesRegex(ValueError, 'expected 2 results'):
                                call()
                        self.assertEqual(run.call_count, 1)


if __name__ == '__main__':
    unittest.main()
