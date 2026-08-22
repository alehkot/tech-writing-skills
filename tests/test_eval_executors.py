"""Tests for the executor layer of scripts/eval_workflow.py.

Written with unittest so they run under `python -m unittest discover -s tests`
in repositories without pytest, and under pytest where it is installed. No test
here launches pi or codex; the process boundary is replaced with fakes.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Callable
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import eval_workflow as ew

FAKE_KEY = "TEST_PI_KEY_MUST_NOT_LEAK_9A1B7"
FAKE_PI = Path("/opt/fake/bin/pi")


def sample_stream(
    text: str = "Hello answer.",
    total_tokens: int | None = 635,
    *,
    include_assistant: bool = True,
    stop_reason: str = "stop",
    error_message: str | None = None,
) -> str:
    events: list[dict[str, object]] = [
        {"type": "session", "version": 3, "id": "abc"},
        {"type": "agent_start"},
        {"type": "turn_start"},
        {
            "type": "message_end",
            "message": {"role": "user", "content": [{"type": "text", "text": "hi"}]},
        },
    ]
    if include_assistant:
        message: dict[str, object] = {
            "role": "assistant",
            "content": [
                {"type": "thinking", "thinking": "hidden"},
                {"type": "text", "text": text},
            ],
            "stopReason": stop_reason,
        }
        if total_tokens is not None:
            message["usage"] = {"input": 629, "output": 6, "totalTokens": total_tokens}
        if error_message is not None:
            message["errorMessage"] = error_message
        events.append({"type": "message_end", "message": message})
    events.append({"type": "agent_end"})
    return "\n".join(json.dumps(event) for event in events)


def grading_payload(*assertions: str) -> dict[str, object]:
    return {
        "assertion_results": [
            {"index": i + 1, "text": text, "passed": True, "evidence": "seen"}
            for i, text in enumerate(assertions)
        ],
        "notes": "",
    }


class CommandContractTests(unittest.TestCase):
    def test_pi_command_shape_is_exact_and_credential_free(self) -> None:
        command = ew.pi_exec_command(
            FAKE_PI, provider="openrouter", model="~google/gemini-flash-latest", thinking="low"
        )
        self.assertEqual(
            command,
            [
                str(FAKE_PI),
                "--provider",
                "openrouter",
                "--model",
                "~google/gemini-flash-latest",
                "--thinking",
                "low",
                "-p",
                "--no-session",
                "--no-extensions",
                "--no-skills",
                "--no-context-files",
                "--no-prompt-templates",
                "--no-tools",
                "--mode",
                "json",
                "--offline",
            ],
        )
        self.assertFalse(any("--api-key" in item or ew.PI_AUTH_ENV_VAR in item for item in command))

    def test_pi_rejects_unknown_thinking_level(self) -> None:
        with self.assertRaises(ValueError):
            ew.pi_exec_command(FAKE_PI, provider="openrouter", model="m", thinking="extreme")

    def test_codex_command_matches_the_legacy_invocation(self) -> None:
        result = Path("/opt/work/outputs/answer.md")
        command = ew.codex_exec_command(
            model="gpt-5.4-mini", reasoning_effort="low", result_path=result, schema_path=None
        )
        self.assertEqual(
            command,
            [
                "codex",
                "exec",
                "--ephemeral",
                "--ignore-rules",
                "--ignore-user-config",
                "-s",
                "read-only",
                "-c",
                'approval_policy="never"',
                "-c",
                'model_reasoning_effort="low"',
                "-m",
                "gpt-5.4-mini",
                "-C",
                str(ew.ROOT),
                "-o",
                str(result),
                "-",
            ],
        )
        structured = ew.codex_exec_command(
            model="gpt-5.4",
            reasoning_effort="medium",
            result_path=result,
            schema_path=Path("/opt/work/schema.json"),
        )
        self.assertEqual(
            structured[-5:], ["--output-schema", "/opt/work/schema.json", "-o", str(result), "-"]
        )

    def test_sanitized_environment_carries_only_the_contract(self) -> None:
        env = ew.sanitized_pi_environment(
            executable=FAKE_PI,
            node_bin_dir=Path("/opt/node/bin"),
            isolated_home=Path("/opt/iso/home"),
            isolated_tmpdir=Path("/opt/iso/tmp"),
            api_key=FAKE_KEY,
        )
        self.assertEqual(
            set(env), {"HOME", "LANG", "LC_ALL", "NO_COLOR", "PATH", "TMPDIR", ew.PI_AUTH_ENV_VAR}
        )
        self.assertEqual(env["HOME"], "/opt/iso/home")
        self.assertTrue(env["PATH"].startswith("/opt/fake/bin:/opt/node/bin"))


class StreamExtractionTests(unittest.TestCase):
    def test_extracts_last_assistant_text_and_tokens(self) -> None:
        stream = sample_stream("First.", 10) + "\n" + sample_stream("The answer.", 700)
        text, stop_reason = ew.extract_pi_assistant_text(stream)
        self.assertEqual(text, "The answer.")
        self.assertEqual(stop_reason, "stop")
        self.assertEqual(ew.extract_pi_usage_tokens(stream), 700)

    def test_missing_assistant_message_is_unusable(self) -> None:
        with self.assertRaises(ew.PiReplyError):
            ew.extract_pi_assistant_text(sample_stream(include_assistant=False))
        self.assertIsNone(ew.extract_pi_usage_tokens(sample_stream(include_assistant=False)))

    def test_error_stop_reason_is_unusable_even_with_exit_zero(self) -> None:
        stream = sample_stream("", 0, stop_reason="error", error_message="429 rate limited")
        with self.assertRaises(ew.PiReplyError) as caught:
            ew.extract_pi_assistant_text(stream)
        self.assertIn("429 rate limited", str(caught.exception))

    def test_empty_text_is_unusable_but_tokens_still_count(self) -> None:
        stream = sample_stream("   ", 42)
        with self.assertRaises(ew.PiReplyError):
            ew.extract_pi_assistant_text(stream)
        self.assertEqual(ew.extract_pi_usage_tokens(stream), 42)

    def test_garbage_lines_are_skipped(self) -> None:
        stream = "not json\n{broken\n" + sample_stream("ok", 5) + "\ntrailing"
        self.assertEqual(ew.extract_pi_assistant_text(stream)[0], "ok")

    def test_normalize_structured_accepts_plain_and_fenced_json(self) -> None:
        self.assertEqual(ew.normalize_pi_structured_text(' {"a": 1} '), '{"a": 1}')
        self.assertEqual(ew.normalize_pi_structured_text('```json\n{"a": 1}\n```'), '{"a": 1}')
        self.assertEqual(ew.normalize_pi_structured_text('```\n{"a": 1}```'), '{"a": 1}')

    def test_normalize_structured_rejects_prose_and_non_objects(self) -> None:
        for text in ("The answer is {}", "[1, 2]", "", '```json\n{"a": 1}\n```\ntrailing prose'):
            with self.assertRaises(ew.PiReplyError):
                ew.normalize_pi_structured_text(text)

    def test_structured_prompt_is_deterministic_and_carries_the_schema(self) -> None:
        first = ew.pi_structured_prompt("base", ew.GRADING_SCHEMA)
        second = ew.pi_structured_prompt("base", json.loads(json.dumps(ew.GRADING_SCHEMA)))
        self.assertEqual(first, second)
        self.assertTrue(first.startswith("base\n\n---\n"))
        self.assertIn(ew.PI_STRUCTURED_OUTPUT_HEADER, first)
        self.assertIn('"assertion_results"', first)


class SchemaIssuesTests(unittest.TestCase):
    def test_valid_grading_payload_has_no_issues(self) -> None:
        self.assertEqual(ew.schema_issues(grading_payload("a", "b"), ew.GRADING_SCHEMA), [])

    def test_missing_required_extra_keys_and_wrong_types_are_reported(self) -> None:
        payload = grading_payload("a")
        payload["assertion_results"][0]["passed"] = "yes"
        payload["assertion_results"][0]["surprise"] = 1
        del payload["notes"]
        issues = ew.schema_issues(payload, ew.GRADING_SCHEMA)
        self.assertTrue(any("notes: missing" in issue for issue in issues))
        self.assertTrue(any("surprise: unexpected key" in issue for issue in issues))
        self.assertTrue(any("passed: expected a boolean" in issue for issue in issues))

    def test_booleans_are_not_integers(self) -> None:
        payload = {"results": [{"index": True, "skill": "x"}]}
        issues = ew.schema_issues(payload, ew.TRIGGER_SCHEMA)
        self.assertTrue(any("expected an integer" in issue for issue in issues))

    def test_top_level_type_mismatch(self) -> None:
        self.assertEqual(ew.schema_issues([], ew.RECHECK_SCHEMA), ["$: expected an object"])


class ArgumentResolutionTests(unittest.TestCase):
    def test_model_defaults_follow_the_executor(self) -> None:
        self.assertEqual(
            ew.resolve_executor_model("pi", None, ew.DEFAULT_MODEL), ew.DEFAULT_PI_MODEL
        )
        self.assertEqual(ew.resolve_executor_model("codex", None, "gpt-5.4"), "gpt-5.4")
        self.assertEqual(
            ew.resolve_executor_model("pi", "openai/gpt-4o", ew.DEFAULT_MODEL), "openai/gpt-4o"
        )
        with self.assertRaises(ValueError):
            ew.resolve_executor_model("claude", None, ew.DEFAULT_MODEL)

    def test_pi_effort_is_a_closed_set_and_codex_passes_through(self) -> None:
        self.assertEqual(ew.check_reasoning_effort("pi", "medium"), "medium")
        with self.assertRaises(ValueError):
            ew.check_reasoning_effort("pi", "extreme")
        self.assertEqual(ew.check_reasoning_effort("codex", "extreme"), "extreme")

    def test_parser_defaults_to_pi_on_every_model_calling_command(self) -> None:
        parser = ew.build_parser()
        for argv in (
            ["run-codex"],
            ["grade-codex"],
            ["recheck"],
            ["sample"],
            ["trigger-eval"],
        ):
            args = parser.parse_args(argv)
            self.assertEqual(args.executor, "pi", argv)
            self.assertIsNone(args.model, argv)
            self.assertEqual(args.timeout_seconds, ew.DEFAULT_TIMEOUT_SECONDS, argv)
        self.assertEqual(parser.parse_args(["run-codex"]).reasoning_effort, "low")
        self.assertEqual(parser.parse_args(["grade-codex"]).reasoning_effort, "medium")
        self.assertIsNone(parser.parse_args(["sample"]).grader_model)
        codex = parser.parse_args(["recheck", "--executor", "codex"])
        self.assertEqual(
            ew.resolve_executor_model(codex.executor, codex.model, ew.DEFAULT_RECHECK_MODEL),
            "gpt-5.4",
        )


class PromptDeliveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.skill = Path(self.tmp.name) / "sample-skill"
        (self.skill / "references").mkdir(parents=True)
        (self.skill / "SKILL.md").write_text(
            "---\nname: sample-skill\ndescription: >-\n  Sample.\n---\n\nRULE_ALPHA applies.\n",
            encoding="utf-8",
        )
        (self.skill / "references" / "guide.md").write_text(
            "RULE_BETA lives here.\n", encoding="utf-8"
        )
        (self.skill / "references" / "notes.txt").write_text("not markdown\n", encoding="utf-8")
        self.case = {"id": "case-1", "prompt": "Draft a reply."}

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_with_skill_inlines_skill_md_and_markdown_references(self) -> None:
        text = ew.run_prompt(self.skill, self.case, "with_skill")
        self.assertIn("<trusted_skill_instructions>", text)
        self.assertIn("--- SKILL.md ---", text)
        self.assertIn("RULE_ALPHA applies.", text)
        self.assertIn("--- references/guide.md ---", text)
        self.assertIn("RULE_BETA lives here.", text)
        self.assertNotIn("not markdown", text)
        self.assertIn("Draft a reply.", text)
        self.assertLess(text.index("</trusted_skill_instructions>"), text.index("Draft a reply."))

    def test_baseline_carries_no_skill_text_and_names_the_doctrine_paths(self) -> None:
        text = ew.run_prompt(self.skill, self.case, "without_skill")
        self.assertNotIn("RULE_ALPHA", text)
        self.assertNotIn("RULE_BETA", text)
        self.assertNotIn("trusted_skill_instructions", text)
        for path in ("skills/", "README.md", "AGENTS.md", "docs/", "workspaces/"):
            self.assertIn(path, text)

    def test_no_unwritable_output_instruction(self) -> None:
        for run in ("with_skill", "without_skill"):
            self.assertNotIn("Save outputs to", ew.run_prompt(self.skill, self.case, run))

    def test_stale_with_skill_prompt_is_refused_and_current_one_passes(self) -> None:
        expected = {("case-1", "with_skill"): ew.run_prompt(self.skill, self.case, "with_skill")}
        run_dir = Path(self.tmp.name) / "iteration-1" / "case-1" / "with_skill"
        run_dir.mkdir(parents=True)
        prompt_path = run_dir / "prompt.md"
        prompt_path.write_text(expected[("case-1", "with_skill")], encoding="utf-8")
        ew.check_prompt_current(prompt_path, expected)

        (self.skill / "SKILL.md").write_text(
            "---\nname: sample-skill\n---\nRULE_GAMMA\n", encoding="utf-8"
        )
        fresh = {("case-1", "with_skill"): ew.run_prompt(self.skill, self.case, "with_skill")}
        with self.assertRaises(ValueError) as caught:
            ew.check_prompt_current(prompt_path, fresh)
        self.assertIn("does not match the current skill text", str(caught.exception))

        baseline = run_dir.parent / "without_skill" / "prompt.md"
        baseline.parent.mkdir()
        baseline.write_text("anything", encoding="utf-8")
        ew.check_prompt_current(baseline, fresh)  # only with_skill is bound to the skill text

        with self.assertRaises(ValueError):
            ew.check_prompt_current(prompt_path, {})


class DeterministicChecksTests(unittest.TestCase):
    def test_required_is_case_sensitive_and_forbidden_is_not(self) -> None:
        checks = {
            "required_regex": ["^## Codex Goal", "verified by"],
            "forbidden_regex": ["T[O]DO"],
        }
        answer = "## Codex Goal\nverified by tests\nnothing pending here\n"
        result = ew.deterministic_checks(answer, checks)
        assert result is not None
        self.assertEqual((result["passed"], result["failed"], result["total"]), (3, 0, 3))
        lowered = ew.deterministic_checks("## codex goal\nverified by x\ntodo later", checks)
        assert lowered is not None
        verdicts = {item["pattern"]: item["passed"] for item in lowered["results"]}
        self.assertFalse(verdicts["^## Codex Goal"])
        self.assertFalse(verdicts["T[O]DO"])
        self.assertTrue(verdicts["verified by"])

    def test_absent_or_empty_checks_yield_none(self) -> None:
        self.assertIsNone(ew.deterministic_checks("text", None))
        self.assertIsNone(
            ew.deterministic_checks("text", {"required_regex": [], "forbidden_regex": []})
        )


class FakePiProcess:
    """Feeds canned stdout streams to invoke_pi in place of real processes."""

    def __init__(self, streams: list[str | Exception], test: unittest.TestCase) -> None:
        self.streams = list(streams)
        self.calls: list[dict[str, object]] = []
        self.test = test

    def __call__(self, command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        self.calls.append({"command": command, **kwargs})
        env = kwargs.get("env")
        self.test.assertIsInstance(env, dict)
        assert isinstance(env, dict)
        self.test.assertEqual(env.get(ew.PI_AUTH_ENV_VAR), FAKE_KEY)
        self.test.assertNotIn(ew.PI_AUTH_ENV_VAR, command)
        item = self.streams.pop(0)
        if isinstance(item, Exception):
            raise item
        if item.startswith("EXIT:"):
            return subprocess.CompletedProcess(command, int(item[5:]), "", "boom")
        return subprocess.CompletedProcess(command, 0, item, "")


class PiRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name) / "outputs"
        self.out.mkdir()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def invoke(
        self,
        streams: list[str | Exception],
        *,
        schema: dict[str, object] | None = None,
    ) -> tuple[Callable[[], ew.ModelReply], FakePiProcess]:
        fake = FakePiProcess(streams, self)

        def run() -> ew.ModelReply:
            with (
                patch.object(ew, "resolve_pi_executable", return_value=FAKE_PI),
                patch.object(ew, "resolve_node_bin_dir", return_value=Path("/opt/node/bin")),
                patch.object(ew, "source_pi_api_key", return_value=FAKE_KEY),
                patch.object(ew, "probe_pi_cli_version", return_value="0.84.2"),
                patch.object(ew, "pi_transient_backoff", lambda failed: None),
                patch.object(ew, "run_process", fake),
            ):
                return ew.invoke_model(
                    "prompt text",
                    executor="pi",
                    model=ew.DEFAULT_PI_MODEL,
                    reasoning_effort="low",
                    result_path=self.out / "answer.md",
                    stream_stem=self.out / "pi",
                    schema=schema,
                    timeout_seconds=60.0,
                )

        return run, fake

    def assert_no_key_in_artifacts(self) -> None:
        for path in Path(self.tmp.name).rglob("*"):
            if path.is_file():
                self.assertNotIn(FAKE_KEY, path.read_text(encoding="utf-8"), path)

    def test_success_writes_answer_and_records_one_attempt(self) -> None:
        run, fake = self.invoke([sample_stream("The extracted answer.", 700)])
        reply = run()
        self.assertEqual(reply.text, "The extracted answer.")
        self.assertEqual(
            (self.out / "answer.md").read_text(encoding="utf-8"), "The extracted answer.\n"
        )
        self.assertEqual(reply.total_tokens, 700)
        self.assertEqual(reply.exit_code, 0)
        self.assertEqual([a["outcome"] for a in reply.attempts], ["success"])
        self.assertEqual(reply.details["pi_cli_version"], "0.84.2")
        self.assertTrue((self.out / "pi_stdout.jsonl").is_file())
        self.assertEqual(fake.calls[0]["input_text"], "prompt text")
        self.assertEqual(fake.calls[0]["command"], reply.command)
        self.assert_no_key_in_artifacts()

    def test_structured_success_normalizes_fenced_json(self) -> None:
        payload = grading_payload("a")
        run, fake = self.invoke(
            [sample_stream("```json\n" + json.dumps(payload) + "\n```", 90)],
            schema=ew.GRADING_SCHEMA,
        )
        reply = run()
        self.assertEqual(json.loads(reply.text), payload)
        self.assertEqual(json.loads((self.out / "answer.md").read_text(encoding="utf-8")), payload)
        self.assertIn("JSON Schema:", str(fake.calls[0]["input_text"]))

    def test_prose_in_structured_phase_is_retried_then_fails(self) -> None:
        run, fake = self.invoke(
            [sample_stream("prose", 5)] * ew.PI_TRANSIENT_ATTEMPTS, schema=ew.GRADING_SCHEMA
        )
        with self.assertRaises(ew.InvocationError) as caught:
            run()
        self.assertEqual(len(fake.calls), ew.PI_TRANSIENT_ATTEMPTS)
        reply = caught.exception.reply
        assert reply is not None
        self.assertEqual(
            [a["outcome"] for a in reply.attempts], ["unusable_reply"] * ew.PI_TRANSIENT_ATTEMPTS
        )
        self.assertTrue((self.out / "pi_stdout.attempt-1.jsonl").is_file())
        self.assertFalse((self.out / "answer.md").exists())

    def test_off_schema_json_is_retried(self) -> None:
        wrong = {"assertion_results": [], "notes": "x", "extra": 1}
        run, fake = self.invoke(
            [sample_stream(json.dumps(wrong), 5), sample_stream(json.dumps(grading_payload()), 6)],
            schema=ew.GRADING_SCHEMA,
        )
        reply = run()
        self.assertEqual(len(fake.calls), 2)
        self.assertEqual([a["outcome"] for a in reply.attempts], ["unusable_reply", "success"])
        self.assertIn("extra: unexpected key", reply.attempts[0]["detail"])

    def test_error_stop_reason_is_retried_and_recovers(self) -> None:
        run, fake = self.invoke(
            [
                sample_stream("", 12, stop_reason="error", error_message="503 upstream"),
                sample_stream("Recovered.", 40),
            ]
        )
        reply = run()
        self.assertEqual(reply.text, "Recovered.")
        self.assertEqual(len(fake.calls), 2)
        self.assertEqual(reply.attempts[0]["total_tokens"], 12)
        self.assertIn("503 upstream", reply.attempts[0]["detail"])

    def test_nonzero_exit_is_not_retried(self) -> None:
        run, fake = self.invoke(["EXIT:2", sample_stream("never used")])
        with self.assertRaises(ew.InvocationError):
            run()
        self.assertEqual(len(fake.calls), 1)
        self.assertEqual((self.out / "pi_stderr.txt").read_text(encoding="utf-8"), "boom")

    def test_timeout_is_recorded(self) -> None:
        run, _ = self.invoke([ew.InvocationTimeout("partial", "")])
        with self.assertRaises(ew.InvocationError) as caught:
            run()
        reply = caught.exception.reply
        assert reply is not None
        self.assertEqual(reply.attempts[0]["outcome"], "timeout")
        self.assertIsNone(reply.exit_code)

    def test_version_gate_refuses_other_series_unless_overridden(self) -> None:
        executable = Path(self.tmp.name) / "pi"
        executable.write_text("#!/bin/sh\n", encoding="utf-8")
        stat = executable.stat()
        key = (str(executable), stat.st_mtime_ns, stat.st_size)
        cwd = Path(self.tmp.name)

        def probe() -> str:
            return ew.probe_pi_cli_version(executable=executable, clean_cwd=cwd, environment={})

        with (
            patch.dict(ew._PI_VERSION_PROBE, {key: "0.99.0"}),
            patch.dict(os.environ, {ew.ALLOW_UNVERIFIED_PI_CLI_ENV: ""}),
        ):
            with self.assertRaises(ValueError) as caught:
                probe()
            self.assertIn("0.99.0", str(caught.exception))
        with (
            patch.dict(ew._PI_VERSION_PROBE, {key: "0.99.0"}),
            patch.dict(os.environ, {ew.ALLOW_UNVERIFIED_PI_CLI_ENV: "1"}),
        ):
            self.assertEqual(probe(), "0.99.0")
        with patch.dict(ew._PI_VERSION_PROBE, {key: "0.84.7"}):
            self.assertEqual(probe(), "0.84.7")


def fake_reply(text: str, **overrides: object) -> ew.ModelReply:
    fields: dict[str, object] = {
        "executor": "pi",
        "model": ew.DEFAULT_PI_MODEL,
        "reasoning_effort": "low",
        "command": [str(FAKE_PI)],
        "exit_code": 0,
        "duration_ms": 1234,
        "total_tokens": 55,
        "text": text,
        "attempts": [{"attempt": 1, "outcome": "success"}],
        "details": {"provider": "openrouter"},
    }
    fields.update(overrides)
    return ew.ModelReply(**fields)  # type: ignore[arg-type]


class RunAndGradeFlowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.run_dir = Path(self.tmp.name) / "iteration-1" / "case-1" / "with_skill"
        (self.run_dir / "outputs").mkdir(parents=True)
        (self.run_dir / "prompt.md").write_text("prompt", encoding="utf-8")
        (self.run_dir / "timing.json").write_text(
            json.dumps({"skill_name": "s", "eval_id": "case-1", "run": "with_skill", "notes": ""}),
            encoding="utf-8",
        )
        self.root_patch = patch.object(ew, "ROOT", Path(self.tmp.name))
        self.root_patch.start()

    def tearDown(self) -> None:
        self.root_patch.stop()
        self.tmp.cleanup()

    def test_run_records_executor_fields_in_timing(self) -> None:
        def fake_invoke(prompt: str, **kwargs: object) -> ew.ModelReply:
            result_path = kwargs["result_path"]
            assert isinstance(result_path, Path)
            result_path.write_text("answer\n", encoding="utf-8")
            return fake_reply("answer")

        with patch.object(ew, "invoke_model", fake_invoke):
            ew.run_eval_prompt(
                self.run_dir / "prompt.md",
                executor="pi",
                model=ew.DEFAULT_PI_MODEL,
                reasoning_effort="low",
                force=False,
            )
        timing = json.loads((self.run_dir / "timing.json").read_text(encoding="utf-8"))
        self.assertEqual(timing["executor"], "pi")
        self.assertEqual(timing["model"], ew.DEFAULT_PI_MODEL)
        self.assertEqual(timing["total_tokens"], 55)
        self.assertEqual(timing["attempts"][0]["outcome"], "success")
        self.assertEqual(timing["executor_details"]["provider"], "openrouter")

    def test_failed_run_still_records_timing_then_raises(self) -> None:
        failed = fake_reply(
            "", exit_code=1, total_tokens=None, attempts=[{"attempt": 1, "outcome": "nonzero_exit"}]
        )

        def fake_invoke(prompt: str, **kwargs: object) -> ew.ModelReply:
            raise ew.InvocationError("pi exited with 1", failed)

        with (
            patch.object(ew, "invoke_model", fake_invoke),
            self.assertRaises(ValueError) as caught,
        ):
            ew.run_eval_prompt(
                self.run_dir / "prompt.md",
                executor="pi",
                model=ew.DEFAULT_PI_MODEL,
                reasoning_effort="low",
                force=False,
            )
        self.assertIn("pi generation failed", str(caught.exception))
        timing = json.loads((self.run_dir / "timing.json").read_text(encoding="utf-8"))
        self.assertEqual(timing["exit_code"], 1)
        self.assertEqual(timing["attempts"][0]["outcome"], "nonzero_exit")

    def test_grade_aligns_results_and_records_grader_and_checks(self) -> None:
        grading_path = self.run_dir / "grading.json"
        grading_path.write_text(
            json.dumps(
                {
                    "skill_name": "s",
                    "eval_id": "case-1",
                    "run": "with_skill",
                    "prompt": "do the thing",
                    "expected_output": "a thing",
                    "assertion_results": [
                        {"text": "has a heading", "passed": None, "evidence": ""},
                        {"text": "says hello", "passed": None, "evidence": ""},
                    ],
                }
            ),
            encoding="utf-8",
        )
        (self.run_dir / "outputs" / "answer.md").write_text("## Heading\nhello\n", encoding="utf-8")
        (self.run_dir / "timing.json").write_text(
            json.dumps({"model": ew.DEFAULT_PI_MODEL}), encoding="utf-8"
        )
        reordered = {
            "assertion_results": [
                {"index": 2, "text": "says hello", "passed": True, "evidence": "hello"},
                {"index": 1, "text": "has a heading", "passed": False, "evidence": "none"},
            ],
            "notes": "fine",
        }
        fixture = {
            "id": "case-1",
            "checks": {"required_regex": ["^## Heading"], "forbidden_regex": ["goodbye"]},
        }
        with (
            patch.object(
                ew, "invoke_model", lambda prompt, **kwargs: fake_reply(json.dumps(reordered))
            ),
            patch.object(ew, "eval_fixture", lambda skill, eval_id: fixture),
        ):
            ew.grade_eval_output(
                grading_path,
                executor="pi",
                model=ew.DEFAULT_PI_MODEL,
                reasoning_effort="medium",
                force=False,
            )
        grading = json.loads(grading_path.read_text(encoding="utf-8"))
        self.assertEqual([r["passed"] for r in grading["assertion_results"]], [False, True])
        self.assertEqual(grading["grader"]["executor"], "pi")
        self.assertTrue(grading["grader"]["self_graded"])
        self.assertEqual(grading["grader"]["notes"], "fine")
        self.assertEqual(grading["deterministic_checks"]["passed"], 2)
        self.assertEqual(grading["summary"]["passed"], 1)


class RepoFixtureTests(unittest.TestCase):
    """Checks that hold in every repository this harness is shared with."""

    def test_descriptions_parse_for_every_skill(self) -> None:
        skills = ew.skill_dirs("all")
        descriptions = ew.skill_descriptions()
        self.assertEqual(sorted(descriptions), [d.name for d in skills])
        self.assertTrue(all(len(v) > 60 for v in descriptions.values()))

    def test_trigger_pool_is_complete_balanced_and_mixed(self) -> None:
        skills = ew.skill_dirs("all")
        pool = ew.trigger_pool("all")
        self.assertEqual(len(pool), 20 * len(skills))
        self.assertEqual(sum(1 for item in pool if item["should_trigger"]), 10 * len(skills))
        self.assertEqual(len({item["skill"] for item in pool[: len(skills)]}), len(skills))

    def test_every_eval_scaffolds_both_arms(self) -> None:
        for skill_dir in ew.skill_dirs("all"):
            for case in ew.read_evals(skill_dir):
                with_skill = ew.run_prompt(skill_dir, case, "with_skill")
                self.assertIn("--- SKILL.md ---", with_skill)
                self.assertIn(str(case["prompt"]), with_skill)
                self.assertNotIn(
                    "--- SKILL.md ---", ew.run_prompt(skill_dir, case, "without_skill")
                )


if __name__ == "__main__":
    unittest.main()
