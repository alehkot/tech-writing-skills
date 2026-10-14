from __future__ import annotations
import re
import sys
from pathlib import Path

import yaml
try:
    from scripts.skill_resources import validate_reference_resources
    from scripts.check_inventory import check_inventory
except ModuleNotFoundError:
    from skill_resources import validate_reference_resources
    from check_inventory import check_inventory

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
    version = metadata.get("version")
    if not isinstance(version, str) or not re.match(r"^\d+\.\d+\.\d+$", version.strip()):
        raise ValueError(f"{path}: metadata.version must be a semver string (e.g. 1.0.0)")
    if metadata.get("risk_tier") not in {"low", "medium", "high"}:
        raise ValueError(f"{path}: metadata.risk_tier must be low, medium, or high")
    if data["name"] != skill_dir.name:
        raise ValueError(f"{path}: name must match directory name {skill_dir.name}")
    if len(data["description"]) > 1024:
        raise ValueError(f"{path}: description must be 1024 characters or fewer")


def validate_openai_metadata(skill_dir: Path) -> None:
    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        raise ValueError(f"{skill_dir}: missing agents/openai.yaml")
    data = yaml.safe_load(openai_yaml.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{openai_yaml}: root must be a YAML object")
    interface = data.get("interface")
    if not isinstance(interface, dict):
        raise ValueError(f"{openai_yaml}: missing interface mapping")
    for key in ("display_name", "short_description", "default_prompt"):
        val = interface.get(key)
        if not isinstance(val, str) or not val.strip():
            raise ValueError(f"{openai_yaml}: interface.{key} must be a nonempty string")


def validate_markdown_references(skill_dir: Path) -> None:
    validate_reference_resources(skill_dir)


def validate_skill_files(skill_dir: Path) -> None:
    forbidden = ("README.md", "CHANGELOG.md", "INSTALLATION_GUIDE.md")
    for name in forbidden:
        if (skill_dir / name).exists():
            raise ValueError(f"{skill_dir / name}: do not include auxiliary docs in skills")
    for ref_dir in ("references", "scripts", "assets"):
        path = skill_dir / ref_dir
        if path.exists() and not path.is_dir():
            raise ValueError(f"{path}: expected a directory")


def run_checks() -> int:
    check_inventory()
    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir() and not path.name.startswith("."))
    if not skill_dirs:
        raise ValueError("No skills found")
    for skill_dir in skill_dirs:
        validate_frontmatter(skill_dir)
        validate_markdown_references(skill_dir)
        validate_openai_metadata(skill_dir)
        validate_skill_files(skill_dir)
    print(f"Validated {len(skill_dirs)} deployable skills.")
    return 0


def main() -> int:
    try:
        return run_checks()
    except (ValueError, OSError) as error:
        print(f"validation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
