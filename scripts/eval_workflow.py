#!/usr/bin/env python3
"""Create and aggregate skill evaluation workspaces."""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
WORKSPACES_DIR = ROOT / "workspaces"
DEFAULT_RUNS = ("with_skill", "without_skill")
GRADING_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "assertion_results": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "text": {"type": "string"},
                    "passed": {"type": "boolean"},
                    "evidence": {"type": "string"},
                },
                "required": ["text", "passed", "evidence"],
            },
        },
        "notes": {"type": "string"},
    },
    "required": ["assertion_results", "notes"],
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return data


def write_json(path: Path, data: dict[str, Any], *, force: bool) -> None:
    if path.exists() and not force:
        return
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def skill_dirs(skill_name: str) -> list[Path]:
    if skill_name == "all":
        skills = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    else:
        skills = [SKILLS_DIR / skill_name]
    missing = [path.name for path in skills if not path.is_dir()]
    if missing:
        raise ValueError(f"Unknown skill: {', '.join(missing)}")
    return skills


def iteration_name(iteration: str) -> str:
    if iteration.startswith("iteration-"):
        return iteration
    if not iteration.isdigit() or int(iteration) <= 0:
        raise ValueError("Iteration must be a positive number or iteration-N")
    return f"iteration-{iteration}"


def next_iteration(skill_dir: Path) -> str:
    workspace = WORKSPACES_DIR / skill_dir.name
    numbers: list[int] = []
    if workspace.exists():
        for path in workspace.iterdir():
            if path.is_dir() and path.name.startswith("iteration-"):
                suffix = path.name.removeprefix("iteration-")
                if suffix.isdigit():
                    numbers.append(int(suffix))
    return f"iteration-{max(numbers, default=0) + 1}"


def read_evals(skill_dir: Path) -> list[dict[str, Any]]:
    path = skill_dir / "evals" / "evals.json"
    data = load_json(path)
    if data.get("skill_name") != skill_dir.name:
        raise ValueError(f"{path}: skill_name must match {skill_dir.name}")
    evals = data.get("evals")
    if not isinstance(evals, list):
        raise ValueError(f"{path}: evals must be a list")
    return evals


def run_prompt(
    skill_dir: Path,
    eval_case: dict[str, Any],
    run_name: str,
    output_dir: Path,
) -> str:
    files = eval_case.get("files", [])
    if not files:
        files_text = "None"
    else:
        files_text = "\n".join(f"- {file}" for file in files)

    if run_name == "with_skill":
        setup_text = (
            f"Read and follow `{skill_dir.resolve() / 'SKILL.md'}` before drafting. "
            "Load only directly relevant referenced files from that skill."
        )
    elif run_name == "without_skill":
        setup_text = (
            "Run from general capability only. Do not read or use this repository's "
            "`skills/` files, `docs/writing-principles.md`, or generated eval grading files."
        )
    else:
        setup_text = f"Baseline run: {run_name}. Document the exact baseline used."

    return f"""# Eval Run

Skill: {skill_dir.name}
Eval ID: {eval_case["id"]}
Run: {run_name}

Setup:
{setup_text}

Task:
{eval_case["prompt"]}

Input files:
{files_text}

Save outputs to:
{output_dir.resolve()}

Return only the produced writing artifact for the task. Do not include grading,
analysis, or commentary in the final answer.
"""


def initial_grading(skill_dir: Path, eval_case: dict[str, Any], run_name: str) -> dict[str, Any]:
    assertions = eval_case.get("assertions", [])
    return {
        "skill_name": skill_dir.name,
        "eval_id": eval_case["id"],
        "run": run_name,
        "expected_output": eval_case.get("expected_output", ""),
        "assertion_results": [
            {
                "text": assertion,
                "passed": None,
                "evidence": "",
            }
            for assertion in assertions
        ],
        "summary": {
            "passed": 0,
            "failed": 0,
            "ungraded": len(assertions),
            "total": len(assertions),
            "pass_rate": None,
        },
    }


def initial_timing(skill_dir: Path, eval_case: dict[str, Any], run_name: str) -> dict[str, Any]:
    return {
        "skill_name": skill_dir.name,
        "eval_id": eval_case["id"],
        "run": run_name,
        "total_tokens": None,
        "duration_ms": None,
        "model": None,
        "command": None,
        "exit_code": None,
        "notes": "",
    }


def init_skill_workspace(
    skill_dir: Path,
    iteration: str | None,
    runs: tuple[str, ...],
    force: bool,
) -> Path:
    iter_name = iteration_name(iteration) if iteration else next_iteration(skill_dir)
    workspace = WORKSPACES_DIR / skill_dir.name / iter_name
    workspace.mkdir(parents=True, exist_ok=True)

    feedback = {
        "skill_name": skill_dir.name,
        "iteration": iter_name,
        "feedback": {},
    }

    for eval_case in read_evals(skill_dir):
        eval_id = str(eval_case["id"])
        feedback["feedback"].setdefault(
            eval_id,
            {run_name: "" for run_name in runs},
        )
        for run_name in runs:
            run_dir = workspace / eval_id / run_name
            output_dir = run_dir / "outputs"
            output_dir.mkdir(parents=True, exist_ok=True)
            prompt_text = run_prompt(skill_dir, eval_case, run_name, output_dir)
            prompt_path = run_dir / "prompt.md"
            if force or not prompt_path.exists():
                prompt_path.write_text(prompt_text, encoding="utf-8")
            write_json(
                run_dir / "timing.json",
                initial_timing(skill_dir, eval_case, run_name),
                force=force,
            )
            write_json(
                run_dir / "grading.json",
                initial_grading(skill_dir, eval_case, run_name),
                force=force,
            )

    write_json(workspace / "feedback.json", feedback, force=force)
    benchmark = aggregate_skill_workspace(skill_dir, iter_name, runs, write=False)
    write_json(workspace / "benchmark.json", benchmark, force=force)
    return workspace


def pass_rate(results: list[dict[str, Any]]) -> float | None:
    graded = [item for item in results if isinstance(item.get("passed"), bool)]
    if not graded:
        return None
    passed = sum(1 for item in graded if item["passed"])
    return passed / len(graded)


def summarise_grading(path: Path) -> dict[str, Any]:
    grading = load_json(path)
    results = grading.get("assertion_results", [])
    if not isinstance(results, list):
        raise ValueError(f"{path}: assertion_results must be a list")
    passed = sum(1 for item in results if item.get("passed") is True)
    failed = sum(1 for item in results if item.get("passed") is False)
    ungraded = sum(1 for item in results if item.get("passed") is None)
    total = len(results)
    rate = pass_rate(results)
    grading["summary"] = {
        "passed": passed,
        "failed": failed,
        "ungraded": ungraded,
        "total": total,
        "pass_rate": rate,
    }
    path.write_text(json.dumps(grading, indent=2) + "\n", encoding="utf-8")
    return grading["summary"]


def mean_std(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"mean": None, "stddev": None}
    if len(values) == 1:
        return {"mean": values[0], "stddev": None}
    return {"mean": statistics.mean(values), "stddev": statistics.pstdev(values)}


def timing_value(timing: dict[str, Any], key: str) -> float | None:
    value = timing.get(key)
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{key} must be a number or null")
    if math.isnan(float(value)):
        raise ValueError(f"{key} must not be NaN")
    return float(value)


def aggregate_skill_workspace(
    skill_dir: Path,
    iteration: str,
    runs: tuple[str, ...],
    *,
    write: bool,
) -> dict[str, Any]:
    workspace = WORKSPACES_DIR / skill_dir.name / iteration
    if not workspace.exists():
        raise ValueError(f"{workspace}: workspace does not exist")

    run_summary: dict[str, Any] = {}
    for run_name in runs:
        pass_rates: list[float] = []
        tokens: list[float] = []
        durations: list[float] = []
        raw = {
            "passed": 0,
            "failed": 0,
            "ungraded": 0,
            "total": 0,
            "graded_evals": 0,
            "total_evals": 0,
        }

        for grading_path in sorted(workspace.glob(f"*/{run_name}/grading.json")):
            raw["total_evals"] += 1
            summary = summarise_grading(grading_path) if write else load_json(grading_path).get("summary", {})
            if not isinstance(summary, dict):
                raise ValueError(f"{grading_path}: summary must be an object")
            raw["passed"] += int(summary.get("passed") or 0)
            raw["failed"] += int(summary.get("failed") or 0)
            raw["ungraded"] += int(summary.get("ungraded") or 0)
            raw["total"] += int(summary.get("total") or 0)
            rate = summary.get("pass_rate")
            if isinstance(rate, (int, float)) and not isinstance(rate, bool):
                pass_rates.append(float(rate))
                raw["graded_evals"] += 1

            timing_path = grading_path.parent / "timing.json"
            timing = load_json(timing_path)
            token_value = timing_value(timing, "total_tokens")
            duration_value = timing_value(timing, "duration_ms")
            if token_value is not None:
                tokens.append(token_value)
            if duration_value is not None:
                durations.append(duration_value / 1000)

        run_summary[run_name] = {
            "pass_rate": mean_std(pass_rates),
            "time_seconds": mean_std(durations),
            "tokens": mean_std(tokens),
            "raw_counts": raw,
        }

    delta: dict[str, float | None] = {}
    if "with_skill" in run_summary and "without_skill" in run_summary:
        for key in ("pass_rate", "time_seconds", "tokens"):
            with_mean = run_summary["with_skill"][key]["mean"]
            without_mean = run_summary["without_skill"][key]["mean"]
            delta[key] = (
                None
                if with_mean is None or without_mean is None
                else with_mean - without_mean
            )

    benchmark = {
        "skill_name": skill_dir.name,
        "iteration": iteration,
        "run_summary": run_summary,
        "delta": delta,
    }
    if write:
        (workspace / "benchmark.json").write_text(
            json.dumps(benchmark, indent=2) + "\n",
            encoding="utf-8",
        )
    return benchmark


def prompt_paths(skill_dir: Path, iteration: str, runs: tuple[str, ...]) -> list[Path]:
    workspace = WORKSPACES_DIR / skill_dir.name / iteration
    if not workspace.exists():
        raise ValueError(f"{workspace}: workspace does not exist")
    paths: list[Path] = []
    for run_name in runs:
        paths.extend(sorted(workspace.glob(f"*/{run_name}/prompt.md")))
    return paths


def grading_paths(skill_dir: Path, iteration: str, runs: tuple[str, ...]) -> list[Path]:
    workspace = WORKSPACES_DIR / skill_dir.name / iteration
    if not workspace.exists():
        raise ValueError(f"{workspace}: workspace does not exist")
    paths: list[Path] = []
    for run_name in runs:
        paths.extend(sorted(workspace.glob(f"*/{run_name}/grading.json")))
    return paths


def extract_tokens(stdout: str) -> int | None:
    match = re.search(r"tokens used\s+([0-9,]+)", stdout)
    if not match:
        return None
    return int(match.group(1).replace(",", ""))


def update_timing(
    run_dir: Path,
    *,
    model: str,
    command: list[str],
    exit_code: int,
    duration_ms: int,
    total_tokens: int | None,
) -> None:
    timing_path = run_dir / "timing.json"
    timing = load_json(timing_path)
    timing.update(
        {
            "total_tokens": total_tokens,
            "duration_ms": duration_ms,
            "model": model,
            "command": command,
            "exit_code": exit_code,
        }
    )
    timing_path.write_text(json.dumps(timing, indent=2) + "\n", encoding="utf-8")


def run_codex_prompt(
    prompt_path: Path,
    *,
    model: str,
    reasoning_effort: str,
    force: bool,
) -> None:
    run_dir = prompt_path.parent
    output_dir = run_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    answer_path = output_dir / "answer.md"
    stdout_path = output_dir / "codex_stdout.txt"
    stderr_path = output_dir / "codex_stderr.txt"
    if answer_path.exists() and not force:
        print(f"Skipping existing output: {answer_path.relative_to(ROOT)}")
        return

    command = [
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
        f'model_reasoning_effort="{reasoning_effort}"',
        "-m",
        model,
        "-C",
        str(ROOT),
        "-o",
        str(answer_path),
        "-",
    ]
    prompt = prompt_path.read_text(encoding="utf-8")
    started = time.perf_counter()
    result = subprocess.run(
        command,
        input=prompt,
        text=True,
        capture_output=True,
        check=False,
    )
    duration_ms = int((time.perf_counter() - started) * 1000)
    stdout_path.write_text(result.stdout, encoding="utf-8")
    stderr_path.write_text(result.stderr, encoding="utf-8")
    update_timing(
        run_dir,
        model=model,
        command=command,
        exit_code=result.returncode,
        duration_ms=duration_ms,
        total_tokens=extract_tokens(result.stdout + "\n" + result.stderr),
    )
    if result.returncode != 0:
        raise ValueError(f"{prompt_path}: codex exec failed with exit {result.returncode}")
    print(f"Ran {prompt_path.relative_to(ROOT)}")


def grade_prompt(grading_path: Path) -> str:
    grading = load_json(grading_path)
    answer_path = grading_path.parent / "outputs" / "answer.md"
    if not answer_path.exists():
        raise ValueError(f"{answer_path}: missing answer output")
    answer = answer_path.read_text(encoding="utf-8")
    assertions = grading.get("assertion_results", [])
    if not isinstance(assertions, list):
        raise ValueError(f"{grading_path}: assertion_results must be a list")
    assertion_text = "\n".join(
        f"{index + 1}. {item['text']}" for index, item in enumerate(assertions)
    )
    return f"""You are grading an Agent Skills evaluation output.

Grade only the answer below against the listed assertions. Do not reward intent,
hidden reasoning, or plausible unstated content. Mark an assertion as passed only
when the answer contains direct evidence for it. Use concise evidence for each
decision; for failures, state what is missing or contradicted.

Skill: {grading["skill_name"]}
Eval ID: {grading["eval_id"]}
Run: {grading["run"]}
Expected output: {grading.get("expected_output", "")}

Assertions:
{assertion_text}

Answer:
```markdown
{answer}
```
"""


def grade_codex_output(
    grading_path: Path,
    *,
    model: str,
    reasoning_effort: str,
    force: bool,
) -> None:
    grading = load_json(grading_path)
    if not force:
        results = grading.get("assertion_results", [])
        if isinstance(results, list) and all(
            isinstance(item, dict) and isinstance(item.get("passed"), bool)
            for item in results
        ):
            print(f"Skipping graded file: {grading_path.relative_to(ROOT)}")
            return

    output_dir = grading_path.parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    result_path = output_dir / "grading_result.json"
    stdout_path = output_dir / "grader_stdout.txt"
    stderr_path = output_dir / "grader_stderr.txt"

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        schema_path = Path(handle.name)
        json.dump(GRADING_SCHEMA, handle)

    command = [
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
        f'model_reasoning_effort="{reasoning_effort}"',
        "-m",
        model,
        "-C",
        str(ROOT),
        "--output-schema",
        str(schema_path),
        "-o",
        str(result_path),
        "-",
    ]
    try:
        result = subprocess.run(
            command,
            input=grade_prompt(grading_path),
            text=True,
            capture_output=True,
            check=False,
        )
    finally:
        schema_path.unlink(missing_ok=True)

    stdout_path.write_text(result.stdout, encoding="utf-8")
    stderr_path.write_text(result.stderr, encoding="utf-8")
    if result.returncode != 0:
        raise ValueError(f"{grading_path}: codex grader failed with exit {result.returncode}")

    graded = load_json(result_path)
    current_results = grading.get("assertion_results", [])
    graded_results = graded.get("assertion_results", [])
    if not isinstance(current_results, list) or not isinstance(graded_results, list):
        raise ValueError(f"{grading_path}: invalid grading result shape")
    if len(current_results) != len(graded_results):
        raise ValueError(
            f"{grading_path}: expected {len(current_results)} assertion results, "
            f"got {len(graded_results)}"
        )
    for expected, actual in zip(current_results, graded_results, strict=True):
        actual["text"] = expected["text"]
        if not isinstance(actual.get("passed"), bool):
            raise ValueError(f"{grading_path}: passed must be boolean")
        if not isinstance(actual.get("evidence"), str) or not actual["evidence"].strip():
            raise ValueError(f"{grading_path}: evidence must be nonempty")

    grading["assertion_results"] = graded_results
    grading["grader"] = {
        "model": model,
        "reasoning_effort": reasoning_effort,
        "notes": graded.get("notes", ""),
    }
    grading_path.write_text(json.dumps(grading, indent=2) + "\n", encoding="utf-8")
    summarise_grading(grading_path)
    print(f"Graded {grading_path.relative_to(ROOT)}")


def init_command(args: argparse.Namespace) -> int:
    runs = tuple(args.runs)
    for skill_dir in skill_dirs(args.skill):
        workspace = init_skill_workspace(skill_dir, args.iteration, runs, args.force)
        print(f"Created eval workspace: {workspace.relative_to(ROOT)}")
    return 0


def aggregate_command(args: argparse.Namespace) -> int:
    runs = tuple(args.runs)
    for skill_dir in skill_dirs(args.skill):
        if args.iteration:
            iterations = [iteration_name(args.iteration)]
        else:
            iterations = [
                path.name
                for path in sorted((WORKSPACES_DIR / skill_dir.name).glob("iteration-*"))
                if path.is_dir()
            ]
        if not iterations:
            raise ValueError(f"{skill_dir.name}: no eval iterations found")
        for iter_name in iterations:
            benchmark = aggregate_skill_workspace(skill_dir, iter_name, runs, write=True)
            raw = benchmark["run_summary"].get("with_skill", {}).get("raw_counts", {})
            print(
                f"Aggregated {skill_dir.name}/{iter_name}: "
                f"{raw.get('passed', 0)} passed, "
                f"{raw.get('failed', 0)} failed, "
                f"{raw.get('ungraded', 0)} ungraded"
            )
    return 0


def run_codex_command(args: argparse.Namespace) -> int:
    runs = tuple(args.runs)
    for skill_dir in skill_dirs(args.skill):
        iter_name = iteration_name(args.iteration)
        paths = prompt_paths(skill_dir, iter_name, runs)
        if args.eval_id:
            paths = [path for path in paths if path.parent.parent.name == args.eval_id]
        if not paths:
            raise ValueError(f"{skill_dir.name}/{iter_name}: no matching prompt files")
        for path in paths:
            run_codex_prompt(
                path,
                model=args.model,
                reasoning_effort=args.reasoning_effort,
                force=args.force,
            )
        aggregate_skill_workspace(skill_dir, iter_name, runs, write=True)
    return 0


def grade_codex_command(args: argparse.Namespace) -> int:
    runs = tuple(args.runs)
    for skill_dir in skill_dirs(args.skill):
        iter_name = iteration_name(args.iteration)
        paths = grading_paths(skill_dir, iter_name, runs)
        if args.eval_id:
            paths = [path for path in paths if path.parent.parent.name == args.eval_id]
        if not paths:
            raise ValueError(f"{skill_dir.name}/{iter_name}: no matching grading files")
        for path in paths:
            grade_codex_output(
                path,
                model=args.model,
                reasoning_effort=args.reasoning_effort,
                force=args.force,
            )
        aggregate_skill_workspace(skill_dir, iter_name, runs, write=True)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scaffold and aggregate Agent Skills eval workspaces."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="Create an iteration workspace")
    init.add_argument("--skill", default="all", help="Skill name, or all")
    init.add_argument("--iteration", help="Iteration number; defaults to next")
    init.add_argument(
        "--runs",
        nargs="+",
        default=list(DEFAULT_RUNS),
        help="Run labels to create, such as with_skill without_skill old_skill",
    )
    init.add_argument("--force", action="store_true", help="Overwrite template files")
    init.set_defaults(func=init_command)

    aggregate = subparsers.add_parser(
        "aggregate",
        help="Refresh grading summaries and write benchmark.json",
    )
    aggregate.add_argument("--skill", default="all", help="Skill name, or all")
    aggregate.add_argument("--iteration", help="Iteration number; defaults to all")
    aggregate.add_argument(
        "--runs",
        nargs="+",
        default=list(DEFAULT_RUNS),
        help="Run labels to aggregate",
    )
    aggregate.set_defaults(func=aggregate_command)

    run_codex = subparsers.add_parser(
        "run-codex",
        help="Run scaffolded eval prompts with Codex CLI and save outputs",
    )
    run_codex.add_argument("--skill", default="all", help="Skill name, or all")
    run_codex.add_argument("--iteration", required=True, help="Iteration number")
    run_codex.add_argument(
        "--runs",
        nargs="+",
        default=list(DEFAULT_RUNS),
        help="Run labels to execute",
    )
    run_codex.add_argument("--eval-id", help="Only run one eval id")
    run_codex.add_argument("--model", default="gpt-5.4-mini", help="Codex model")
    run_codex.add_argument(
        "--reasoning-effort",
        default="low",
        help="Codex reasoning effort",
    )
    run_codex.add_argument("--force", action="store_true", help="Overwrite outputs")
    run_codex.set_defaults(func=run_codex_command)

    grade_codex = subparsers.add_parser(
        "grade-codex",
        help="Grade saved eval outputs with Codex CLI",
    )
    grade_codex.add_argument("--skill", default="all", help="Skill name, or all")
    grade_codex.add_argument("--iteration", required=True, help="Iteration number")
    grade_codex.add_argument(
        "--runs",
        nargs="+",
        default=list(DEFAULT_RUNS),
        help="Run labels to grade",
    )
    grade_codex.add_argument("--eval-id", help="Only grade one eval id")
    grade_codex.add_argument("--model", default="gpt-5.4-mini", help="Codex model")
    grade_codex.add_argument(
        "--reasoning-effort",
        default="low",
        help="Codex reasoning effort",
    )
    grade_codex.add_argument("--force", action="store_true", help="Overwrite grading")
    grade_codex.set_defaults(func=grade_codex_command)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
