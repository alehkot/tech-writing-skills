"""Exercise metadata rejection and compatibility through helpers and the CLI."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import validate  # noqa: E402


class MetadataTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.skill = self.root / "valid-skill"
        self.skill.mkdir()
        (self.skill / "agents").mkdir()
        self.entry = self.skill / "SKILL.md"
        self.ui = self.skill / "agents" / "openai.yaml"
        self.entry.write_text(self.frontmatter(), encoding="utf-8")
        self.ui.write_text(
            "interface:\n  display_name: Useful skill\n"
            "  short_description: Help with a task.\n"
            "  default_prompt: Use $valid-skill to help.\n", encoding="utf-8"
        )

    @staticmethod
    def frontmatter(name: str = "valid-skill") -> str:
        return (
            f"---\nname: {json.dumps(name, ensure_ascii=False)}\n"
            "description: Help with a specific task.\n"
            "metadata:\n  version: '1.0.0'\n  risk_tier: low\n"
            "---\n# Instructions\n\nComplete the requested task.\n"
        )

    def check_frontmatter(self, content: str) -> None:
        self.entry.write_text(content, encoding="utf-8")
        validate.validate_frontmatter(self.skill)

    def test_existing_metadata_passes(self) -> None:
        validate.validate_frontmatter(self.skill)
        validate.validate_openai_metadata(self.skill)

    def test_boundary_and_yaml_compatibility(self) -> None:
        content = self.frontmatter()
        cases = (
            content.replace("\n", "\r\n"),
            content.replace("---\n", "--- \t\n"),
            content.split("\n# Instructions", 1)[0],
            content.replace("Help with a specific task.", "'Explain --- markers.'"),
            content.replace("description: Help with a specific task.",
                            "description: |\n  Explain a marker:\n  ---"),
            content.replace("description: Help with a specific task.",
                            "description: >\n  Help with a task\n  across two lines."),
            content + "\n---\nname: body-only-name\n",
        )
        for case in cases:
            with self.subTest(content=case):
                self.check_frontmatter(case)

    def test_invalid_opening_delimiters_are_rejected(self) -> None:
        for opening in ("", "----", "---suffix", " ---", "# Heading\n---"):
            with self.subTest(opening=opening):
                with self.assertRaisesRegex(ValueError, "must start with a --- line"):
                    self.check_frontmatter(self.frontmatter().replace("---", opening, 1))

    def test_invalid_closing_delimiters_are_rejected(self) -> None:
        for closing in ("", "----", "---suffix", " ---", "---#comment"):
            with self.subTest(closing=closing):
                with self.assertRaisesRegex(ValueError, "must close with a --- line"):
                    self.check_frontmatter(
                        self.frontmatter().replace("\n---\n#", f"\n{closing}\n#")
                    )

    def test_missing_or_empty_file_is_rejected(self) -> None:
        self.check_frontmatter(self.frontmatter())
        with self.assertRaisesRegex(ValueError, "must start"):
            self.check_frontmatter("")
        self.entry.unlink()
        with self.assertRaisesRegex(ValueError, "missing SKILL.md"):
            validate.validate_frontmatter(self.skill)

    def test_non_mapping_frontmatter_is_rejected(self) -> None:
        for content in ("", "# comment", "null", "[]", "- item", "text", "42", "true"):
            with self.subTest(content=content):
                with self.assertRaisesRegex(ValueError, "YAML root must be a mapping"):
                    self.check_frontmatter(f"---\n{content}\n---\n# Instructions\n")

    def test_invalid_yaml_has_path_and_source_line(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid YAML at line 3") as error:
            self.check_frontmatter("---\nname: [unfinished\n---\n# Instructions\n")
        self.assertIn(str(self.entry), str(error.exception))

    def test_unsafe_yaml_tags_remain_rejected(self) -> None:
        for text in ("!unknown value", "!!python/object:builtins.object {}"):
            with self.subTest(text=text):
                with self.assertRaisesRegex(ValueError, "invalid YAML"):
                    self.check_frontmatter(f"---\n{text}\n---\n# Instructions\n")

    def test_invalid_control_characters_are_not_rewritten(self) -> None:
        for control in ("\v", "\f", "\x1c", "\x1d", "\x1e"):
            with self.subTest(control=repr(control)):
                with self.assertRaisesRegex(ValueError, "invalid YAML"):
                    self.check_frontmatter(
                        self.frontmatter().replace("metadata:\n", f"metadata:{control}\n")
                    )

    def test_scalar_constructor_errors_are_path_specific(self) -> None:
        for value in ("!!timestamp not-a-date", "2026-99-99", "!!int not-an-int"):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "invalid YAML") as error:
                    self.check_frontmatter(
                        self.frontmatter().replace("metadata:\n", f"extra: {value}\nmetadata:\n")
                    )
                self.assertIn(str(self.entry), str(error.exception))

    def test_valid_scalar_extra_field_is_preserved(self) -> None:
        self.check_frontmatter(
            self.frontmatter().replace("metadata:\n", "extra: 2026-10-14\nmetadata:\n")
        )

    def test_invalid_matching_names_are_rejected(self) -> None:
        for name in (
            "Bad-Name", "bad_name", "bad.name", "bad name", "-bad", "bad-",
            "bad--name", "a" * 65, "bad😀", "Ｃａｐｉｔａｌ", "½", "ﬃ" * 22,
        ):
            with self.subTest(name=name):
                skill = self.root / name
                skill.mkdir()
                (skill / "SKILL.md").write_text(self.frontmatter(name), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "name must be 1-64"):
                    validate.validate_frontmatter(skill)

    def test_valid_name_boundaries_and_unicode_are_preserved(self) -> None:
        for name in ("a", "a" * 64, "docs-2", "écriture", "文档", "ｄｏｃｓ", "ﬃ" * 21):
            with self.subTest(name=name):
                skill = self.root / name
                skill.mkdir()
                (skill / "SKILL.md").write_text(self.frontmatter(name), encoding="utf-8")
                validate.validate_frontmatter(skill)

    def test_directory_match_remains_required(self) -> None:
        with self.assertRaisesRegex(ValueError, "name must match directory"):
            self.check_frontmatter(self.frontmatter("other-skill"))

    def test_required_string_fields_remain_checked(self) -> None:
        for field in ("name", "description"):
            for value in (None, "", " ", 1, [], {}):
                with self.subTest(field=field, value=value):
                    text = self.frontmatter()
                    original = 'name: "valid-skill"' if field == "name" else (
                        "description: Help with a specific task."
                    )
                    text = text.replace(original, f"{field}: {json.dumps(value)}")
                    with self.assertRaisesRegex(ValueError, f"{field} must be a nonempty"):
                        self.check_frontmatter(text)

    def test_description_length_boundary_is_preserved(self) -> None:
        self.check_frontmatter(self.frontmatter().replace("Help with a specific task.", "x" * 1024))
        with self.assertRaisesRegex(ValueError, "1024 characters"):
            self.check_frontmatter(self.frontmatter().replace("Help with a specific task.", "x" * 1025))

    def test_invalid_risk_tier_types_are_rejected_cleanly(self) -> None:
        for value in (None, [], {}, 1, True, "critical"):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "metadata.risk_tier"):
                    self.check_frontmatter(
                        self.frontmatter().replace("risk_tier: low", f"risk_tier: {json.dumps(value)}")
                    )

    def test_existing_required_metadata_is_preserved(self) -> None:
        for old, new, diagnostic in (
            ("metadata:\n  version: '1.0.0'\n  risk_tier: low", "metadata: []", "metadata must include"),
            ("version: '1.0.0'", "version: 1", "metadata.version"),
            ("version: '1.0.0'", "version: '1.0'", "metadata.version"),
        ):
            with self.subTest(new=new):
                with self.assertRaisesRegex(ValueError, diagnostic):
                    self.check_frontmatter(self.frontmatter().replace(old, new))

    def test_invalid_ui_yaml_is_path_specific(self) -> None:
        self.ui.write_text("interface: [unfinished\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "invalid YAML at line 2") as error:
            validate.validate_openai_metadata(self.skill)
        self.assertIn(str(self.ui), str(error.exception))

    def test_non_mapping_ui_roots_are_rejected(self) -> None:
        for text in ("", "null", "- item", "text", "42"):
            with self.subTest(text=text):
                self.ui.write_text(text, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "YAML root must be a mapping"):
                    validate.validate_openai_metadata(self.skill)

    def test_ui_interface_checks_are_preserved(self) -> None:
        for text, diagnostic in (
            ("interface: []", "interface mapping"),
            ("interface: {}", "interface.display_name"),
            ("interface: {display_name: Name, short_description: false}", "interface.short_description"),
        ):
            with self.subTest(text=text):
                self.ui.write_text(text, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, diagnostic):
                    validate.validate_openai_metadata(self.skill)

    def prepare_cli_repo(self) -> None:
        scripts = self.root / "scripts"
        scripts.mkdir()
        for name in ("validate.py", "skill_resources.py", "check_inventory.py"):
            shutil.copyfile(ROOT / "scripts" / name, scripts / name)
        skills = self.root / "skills"
        skills.mkdir()
        self.skill = self.skill.rename(skills / self.skill.name)
        self.entry = self.skill / "SKILL.md"
        self.ui = self.skill / "agents" / "openai.yaml"
        (self.root / "LICENSE").write_text("Existing license notice.\n")
        (self.skill / "LICENSE").write_text("Existing license notice.\n")
        inventory = ["public-files.json"] + [
            path.relative_to(self.root).as_posix()
            for path in sorted(self.root.rglob("*")) if path.is_file()
        ]
        (self.root / "public-files.json").write_text(json.dumps(inventory), encoding="utf-8")
        subprocess.run(["git", "init", "--quiet", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)

    def run_cli(self) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "scripts/validate.py"], cwd=self.root,
            text=True, capture_output=True, check=False,
        )

    def test_cli_success_preserves_source_files(self) -> None:
        self.prepare_cli_repo()
        before = {path: path.read_bytes() for path in (self.entry, self.ui)}
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "Validated 1 deployable skills.\n")
        self.assertEqual(result.stderr, "")
        self.assertEqual(before, {path: path.read_bytes() for path in before})

    def test_cli_reports_invalid_metadata_without_traceback_or_success(self) -> None:
        self.prepare_cli_repo()
        original_entry, original_ui = self.entry.read_text(), self.ui.read_text()
        cases = (
            (self.entry, self.frontmatter().replace("\n---\n#", "\n---suffix\n#"), "must close"),
            (self.entry, "---\nnull\n---\n", "YAML root must be a mapping"),
            (self.entry, "---\nname: [unfinished\n---\n", "invalid YAML"),
            (self.entry, self.frontmatter().replace("risk_tier: low", "risk_tier: []"), "risk_tier"),
            (self.entry, self.frontmatter().replace("metadata:\n", "extra: !!timestamp invalid\nmetadata:\n"), "invalid YAML"),
            (self.ui, "interface: [unfinished\n", "invalid YAML"),
            (self.ui, original_ui + "extra: 2026-99-99\n", "invalid YAML"),
        )
        for path, text, diagnostic in cases:
            with self.subTest(path=path.name, diagnostic=diagnostic):
                self.entry.write_text(original_entry, encoding="utf-8")
                self.ui.write_text(original_ui, encoding="utf-8")
                path.write_text(text, encoding="utf-8")
                before = path.read_bytes()
                result = self.run_cli()
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stdout, "")
                self.assertIn("validation failed:", result.stderr)
                self.assertIn(str(path), result.stderr)
                self.assertIn(diagnostic, result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(path.read_bytes(), before)

    def test_cli_rejects_invalid_matching_name(self) -> None:
        self.skill = self.skill.rename(self.root / "Bad_Name")
        self.entry = self.skill / "SKILL.md"
        self.entry.write_text(self.frontmatter("Bad_Name"), encoding="utf-8")
        self.prepare_cli_repo()
        result = self.run_cli()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("name must be 1-64", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
