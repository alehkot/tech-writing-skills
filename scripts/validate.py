from __future__ import annotations
import re
import sys
import unicodedata
from pathlib import Path

import yaml
try:
    from scripts.skill_resources import require_bundled_file, validate_reference_resources
    from scripts.check_inventory import check_inventory
except ModuleNotFoundError:
    from skill_resources import require_bundled_file, validate_reference_resources
    from check_inventory import check_inventory

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"


def load_yaml_mapping(text: str, path: Path, line_offset: int = 0) -> dict:
    """Turn malformed metadata into path-specific validation failures."""
    try:
        data = yaml.safe_load(text)
    except (yaml.YAMLError, ValueError, TypeError, AttributeError, OverflowError) as error:
        # SafeLoader's scalar constructors can raise native errors (for example,
        # invalid timestamps) rather than a YAMLError. Keep this catch scoped to
        # parsing, so bugs in the validation checks are not hidden.
        mark = getattr(error, "problem_mark", None)
        location = (
            f" at line {mark.line + line_offset + 1}, column {mark.column + 1}"
            if mark is not None else ""
        )
        problem = getattr(error, "problem", None) or str(error)
        raise ValueError(f"{path}: invalid YAML{location}: {problem}") from error
    if not isinstance(data, dict):
        raise ValueError(f"{path}: YAML root must be a mapping")
    return data


def validate_frontmatter(skill_dir: Path) -> None:
    path = skill_dir / "SKILL.md"
    if not path.exists():
        raise ValueError(f"{skill_dir}: missing SKILL.md")
    content = path.read_text(encoding="utf-8")
    # read_text normalizes CRLF/CR; do not rewrite other YAML characters.
    lines = content.split("\n")
    if not lines or lines[0].rstrip(" \t") != "---":
        raise ValueError(f"{path}: YAML frontmatter must start with a --- line")
    end = next(
        (index for index, line in enumerate(lines[1:], 1)
         if line.rstrip(" \t") == "---"), None
    )
    if end is None:
        raise ValueError(f"{path}: YAML frontmatter must close with a --- line")
    data = load_yaml_mapping("\n".join(lines[1:end]) + "\n", path, line_offset=1)
    for field in ("name", "description"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f"{path}: {field} must be a nonempty string")
    metadata = data.get("metadata")
    if not isinstance(metadata, dict):
        raise ValueError(f"{path}: metadata must include version and risk_tier")
    version = metadata.get("version")
    if not isinstance(version, str) or not re.match(r"^\d+\.\d+\.\d+$", version.strip()):
        raise ValueError(f"{path}: metadata.version must be a semver string (e.g. 1.0.0)")
    risk_tier = metadata.get("risk_tier")
    if not isinstance(risk_tier, str) or risk_tier not in {"low", "medium", "high"}:
        raise ValueError(f"{path}: metadata.risk_tier must be low, medium, or high")
    # Match the reference validator's Unicode-compatible name constraints.
    name = unicodedata.normalize("NFKC", data["name"])
    if (
        not 1 <= len(name) <= 64
        or name != name.lower()
        or not all(char.isalnum() or char == "-" for char in name)
        or name.startswith("-")
        or name.endswith("-")
        or "--" in name
    ):
        raise ValueError(
            f"{path}: name must be 1-64 lowercase alphanumeric characters or hyphens, "
            "without leading, trailing, or consecutive hyphens"
        )
    if data["name"] != skill_dir.name:
        raise ValueError(f"{path}: name must match directory name {skill_dir.name}")
    if len(data["description"]) > 1024:
        raise ValueError(f"{path}: description must be 1024 characters or fewer")


def validate_openai_metadata(skill_dir: Path) -> None:
    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        raise ValueError(f"{skill_dir}: missing agents/openai.yaml")
    data = load_yaml_mapping(openai_yaml.read_text(encoding="utf-8"), openai_yaml)
    interface = data.get("interface")
    if not isinstance(interface, dict):
        raise ValueError(f"{openai_yaml}: missing interface mapping")
    for key in ("display_name", "short_description", "default_prompt"):
        val = interface.get(key)
        if not isinstance(val, str) or not val.strip():
            raise ValueError(f"{openai_yaml}: interface.{key} must be a nonempty string")


def validate_markdown_references(
    skill_dir: Path, bundle_files: set[Path] | None = None
) -> None:
    validate_reference_resources(skill_dir, bundle_files)


def validate_skill_files(skill_dir: Path) -> None:
    forbidden = ("README.md", "CHANGELOG.md", "INSTALLATION_GUIDE.md")
    for name in forbidden:
        if (skill_dir / name).exists():
            raise ValueError(f"{skill_dir / name}: do not include auxiliary docs in skills")
    for ref_dir in ("references", "scripts", "assets"):
        path = skill_dir / ref_dir
        if path.exists() and not path.is_dir():
            raise ValueError(f"{path}: expected a directory")


def validate_skill_license(skill_dir: Path, root_license: bytes) -> None:
    """Keep the existing repository notice with independently copied skills."""
    path = skill_dir / "LICENSE"
    if path.read_bytes() != root_license:
        raise ValueError(f"{path}: must match the repository LICENSE exactly")


def run_checks() -> int:
    bundle_files = check_inventory()
    require_bundled_file(ROOT / "LICENSE", ROOT, bundle_files)
    root_license = (ROOT / "LICENSE").read_bytes()
    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir() and not path.name.startswith("."))
    if not skill_dirs:
        raise ValueError("No skills found")
    for skill_dir in skill_dirs:
        for required in (skill_dir / "SKILL.md", skill_dir / "agents" / "openai.yaml", skill_dir / "LICENSE"):
            require_bundled_file(required, skill_dir, bundle_files)
        validate_skill_license(skill_dir, root_license)
        validate_frontmatter(skill_dir)
        validate_markdown_references(skill_dir, bundle_files)
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
