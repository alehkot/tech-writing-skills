#!/usr/bin/env python3
"""Validate the technical-writing skill bundle."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"


def validate_frontmatter(skill_dir: Path) -> None:
    path = skill_dir / "SKILL.md"
    if not path.exists():
        raise ValueError(f"{skill_dir}: missing SKILL.md")
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise ValueError(f"{path}: missing YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    for field in ("name", "description"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f"{path}: {field} must be a nonempty string")
    metadata = data.get("metadata")
    if not isinstance(metadata, dict):
        raise ValueError(f"{path}: metadata must include version and risk_tier")
    if not isinstance(metadata.get("version"), str) or not metadata["version"].strip():
        raise ValueError(f"{path}: metadata.version must be a nonempty string")
    if metadata.get("risk_tier") not in {"low", "medium", "high"}:
        raise ValueError(f"{path}: metadata.risk_tier must be low, medium, or high")
    if data["name"] != skill_dir.name:
        raise ValueError(f"{path}: name must match directory name {skill_dir.name}")
    if len(data["description"]) > 1024:
        raise ValueError(f"{path}: description must be 1024 characters or fewer")


def validate_skill_files(skill_dir: Path) -> None:
    forbidden = ("README.md", "CHANGELOG.md", "INSTALLATION_GUIDE.md")
    for name in forbidden:
        if (skill_dir / name).exists():
            raise ValueError(f"{skill_dir / name}: do not include auxiliary docs in skills")
    for ref_dir in ("references", "scripts", "assets"):
        path = skill_dir / ref_dir
        if path.exists() and not path.is_dir():
            raise ValueError(f"{path}: expected a directory")


def validate_json(path: Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_output_evals(skill_dir: Path) -> None:
    path = skill_dir / "evals" / "evals.json"
    data = load_json(path)
    if not isinstance(data, dict) or data.get("skill_name") != skill_dir.name:
        raise ValueError(f"{path}: skill_name must match {skill_dir.name}")
    evals = data.get("evals")
    if not isinstance(evals, list) or len(evals) < 3:
        raise ValueError(f"{path}: expected at least 3 output-quality evals")
    for item in evals:
        if not isinstance(item, dict):
            raise ValueError(f"{path}: each eval must be an object")
        for field in ("id", "prompt", "expected_output", "assertions"):
            if field not in item:
                raise ValueError(f"{path}: eval {item.get('id')} missing {field}")
        assertions = item["assertions"]
        if not isinstance(assertions, list) or len(assertions) < 3:
            raise ValueError(
                f"{path}: eval {item.get('id')} needs at least 3 assertions"
            )


def validate_trigger_queries(skill_dir: Path) -> None:
    train_path = skill_dir / "evals" / "train_queries.json"
    validation_path = skill_dir / "evals" / "validation_queries.json"
    old_path = skill_dir / "evals" / "trigger_queries.json"
    if old_path.exists():
        raise ValueError(f"{old_path}: use train_queries.json and validation_queries.json")

    train = load_json(train_path)
    validation = load_json(validation_path)
    for path, data, expected_len in (
        (train_path, train, 12),
        (validation_path, validation, 8),
    ):
        if not isinstance(data, dict) or data.get("skill_name") != skill_dir.name:
            raise ValueError(f"{path}: skill_name must match {skill_dir.name}")
        queries = data.get("queries")
        if not isinstance(queries, list) or len(queries) != expected_len:
            raise ValueError(f"{path}: expected exactly {expected_len} queries")
        for item in queries:
            if not isinstance(item, dict):
                raise ValueError(f"{path}: each query must be an object")
            if not isinstance(item.get("query"), str) or not item["query"].strip():
                raise ValueError(f"{path}: each query must include nonempty query text")
            if not isinstance(item.get("should_trigger"), bool):
                raise ValueError(f"{path}: each query must include boolean should_trigger")

    all_queries = train["queries"] + validation["queries"]
    should = sum(1 for item in all_queries if item["should_trigger"])
    should_not = len(all_queries) - should
    if len(all_queries) != 20 or should != 10 or should_not != 10:
        raise ValueError(
            f"{skill_dir}: trigger queries must total 20 with 10 trigger and 10 non-trigger"
        )
    for path, data in ((train_path, train), (validation_path, validation)):
        positives = sum(1 for item in data["queries"] if item["should_trigger"])
        negatives = len(data["queries"]) - positives
        if positives != negatives:
            raise ValueError(f"{path}: expected a balanced trigger/non-trigger split")


def main() -> int:
    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    if not skill_dirs:
        print("No skills found.", file=sys.stderr)
        return 1

    for skill_dir in skill_dirs:
        validate_frontmatter(skill_dir)
        validate_skill_files(skill_dir)

    json_files = sorted(SKILLS_DIR.glob("*/evals/*.json"))
    for path in json_files:
        validate_json(path)

    for skill_dir in skill_dirs:
        validate_output_evals(skill_dir)
        validate_trigger_queries(skill_dir)

    print(f"Validated {len(skill_dirs)} skills and {len(json_files)} eval JSON files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
