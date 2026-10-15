"""Exercise the distributable file boundary."""

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "bundle_inventory", Path(__file__).resolve().parents[1] / "scripts/check_inventory.py"
)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class InventoryTests(unittest.TestCase):
    def test_rejects_unlisted_files_and_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "public-files.json").write_text(json.dumps(["allowed.md"]))
            (root / "allowed.md").write_text("content")
            with (
                patch.object(checker, "ROOT", root),
                patch.object(checker.subprocess, "check_output") as git,
            ):
                git.return_value = "100644 abc 0\tallowed.md\0"
                self.assertEqual(checker.check_inventory(), {(root / "allowed.md").resolve()})
                git.return_value += "100644 def 0\tunexpected.md\0"
                with self.assertRaisesRegex(ValueError, "unexpected"):
                    checker.check_inventory()
                git.return_value = "120000 abc 0\tallowed.md\0"
                with self.assertRaisesRegex(ValueError, "ordinary"):
                    checker.check_inventory()


class BundleDependencyTests(unittest.TestCase):
    """Exercise the real CLI against isolated Git indexes and tracked exports."""

    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.temporary = Path(directory.name)
        self.root = self.temporary / "repo"
        self.root.mkdir()
        self.skill = self.root / "skills" / "valid-skill"
        self.entry = self.skill / "SKILL.md"
        self.ui = self.skill / "agents" / "openai.yaml"
        self.guide = self.skill / "references" / "guide.md"
        self.write(self.entry, self.frontmatter("valid-skill"))
        self.write(self.ui, "interface:\n  display_name: Valid skill\n"
                   "  short_description: Help with a task.\n"
                   "  default_prompt: Use $valid-skill to help.\n")
        self.write(self.guide, "# Guide\n\nUse the instructions.\n")
        self.write(self.root / ".gitignore", "**/ignored-*\n**/__pycache__/\n")
        source = Path(__file__).resolve().parents[1] / "scripts"
        (self.root / "scripts").mkdir()
        for name in ("validate.py", "check_inventory.py", "skill_resources.py"):
            shutil.copyfile(source / name, self.root / "scripts" / name)
        self.inventory = self.root / "public-files.json"
        self.listed = {"public-files.json"} | {
            path.relative_to(self.root).as_posix()
            for path in self.root.rglob("*") if path.is_file()
        }
        self.save_inventory()
        self.git("init", "--quiet")
        self.git("add", ".")

    @staticmethod
    def frontmatter(name):
        return (
            f"---\nname: {name}\ndescription: Help with a specific task.\n"
            "metadata:\n  version: '1.0.0'\n  risk_tier: low\n---\n"
            "# Instructions\n\nRead [guide](references/guide.md).\n"
        )

    @staticmethod
    def write(path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def git(self, *args, root=None):
        return subprocess.run(
            ["git", "-C", str(root or self.root), *args],
            check=True, text=True, capture_output=True,
        )

    def save_inventory(self):
        self.inventory.write_text(json.dumps(sorted(self.listed)), encoding="utf-8")

    def link(self, target, source=None):
        path = source or self.entry
        path.write_text(path.read_text(encoding="utf-8") + f"\n[Resource]({target})\n",
                        encoding="utf-8")

    def run_cli(self, root=None):
        return subprocess.run(
            [sys.executable, "scripts/validate.py"], cwd=root or self.root,
            text=True, capture_output=True, check=False,
        )

    def assert_success(self, root=None):
        result = self.run_cli(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "Validated 1 deployable skills.\n")
        self.assertEqual(result.stderr, "")

    def assert_rejected(self, diagnostic, root=None):
        result = self.run_cli(root)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertIn("validation failed:", result.stderr)
        self.assertIn(diagnostic, result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        return result

    def tracked_export(self):
        destination = self.temporary / "export"
        destination.mkdir()
        self.git("checkout-index", "--all", f"--prefix={destination}/")
        self.git("init", "--quiet", root=destination)
        self.git("add", ".", root=destination)
        return destination

    def test_valid_bundle_passes_locally_and_from_tracked_export(self):
        self.assert_success()
        self.assert_success(self.tracked_export())

    def test_ignored_reference_cannot_make_local_and_export_checks_disagree(self):
        path = self.skill / "references" / "ignored-guide.md"
        self.write(path, "# Extra guide\n")
        self.link("references/ignored-guide.md")
        self.git("add", str(self.entry))
        self.git("check-ignore", str(path))
        before = {item: item.read_bytes() for item in (self.entry, path, self.inventory)}
        result = self.assert_rejected("not in the tracked bundle inventory")
        self.assertIn(str(path), result.stderr)
        exported = self.tracked_export()
        self.assertFalse((exported / path.relative_to(self.root)).exists())
        self.assert_rejected("not in the tracked bundle inventory", exported)
        self.assertEqual(before, {item: item.read_bytes() for item in before})

    def test_untracked_reference_is_rejected(self):
        path = self.skill / "references" / "extra.md"
        self.write(path, "# Extra guide\n")
        self.link("references/extra.md")
        self.assert_rejected("not in the tracked bundle inventory")

    def test_ignored_assets_scripts_and_images_are_rejected(self):
        original = self.entry.read_text(encoding="utf-8")
        for target, image in (("assets/ignored-template.txt", False),
                              ("scripts/ignored-example.py", False),
                              ("assets/ignored-diagram.png", True)):
            with self.subTest(target=target):
                path = self.skill / target
                self.write(path, "example resource")
                self.entry.write_text(original, encoding="utf-8")
                self.link(target)
                if image:
                    self.entry.write_text(self.entry.read_text().replace("[Resource]", "![Resource]"))
                self.git("check-ignore", str(path))
                result = self.assert_rejected("not in the tracked bundle inventory")
                self.assertIn(str(path), result.stderr)

    def test_reference_links_also_require_bundled_targets(self):
        path = self.skill / "assets" / "untracked.txt"
        self.write(path, "resource")
        self.link("../assets/untracked.txt", self.guide)
        self.assert_rejected("not in the tracked bundle inventory")

    def test_untracked_skill_entrypoint_is_rejected(self):
        skill = self.root / "skills" / "local-skill"
        self.write(skill / "SKILL.md", self.frontmatter("local-skill"))
        self.write(skill / "agents" / "openai.yaml", self.ui.read_text())
        self.write(skill / "references" / "guide.md", "# Guide\n")
        result = self.assert_rejected("not in the tracked bundle inventory")
        self.assertIn(str(skill / "SKILL.md"), result.stderr)

    def test_required_metadata_cannot_be_kept_only_in_worktree(self):
        for path in (self.entry, self.ui):
            with self.subTest(path=path.name):
                relative = path.relative_to(self.root).as_posix()
                self.git("rm", "--cached", "--", relative)
                self.listed.remove(relative)
                self.save_inventory()
                self.git("add", "public-files.json")
                result = self.assert_rejected("not in the tracked bundle inventory")
                self.assertIn(str(path), result.stderr)
                self.listed.add(relative)
                self.save_inventory()
                self.git("add", "public-files.json", relative)

    def test_new_dependency_needs_both_inventory_and_index_membership(self):
        path = self.skill / "assets" / "template.txt"
        relative = path.relative_to(self.root).as_posix()
        self.write(path, "resource")
        self.link("assets/template.txt")
        self.listed.add(relative)
        self.save_inventory()
        self.assert_rejected("Bundle inventory differs: missing=")
        self.listed.remove(relative)
        self.save_inventory()
        self.git("add", relative)
        self.assert_rejected("unexpected=")
        self.listed.add(relative)
        self.save_inventory()
        self.git("add", ".")
        self.assert_success()
        self.assert_success(self.tracked_export())

    def test_unreferenced_caches_and_scratch_assets_remain_allowed(self):
        for target in ("assets/ignored-scratch.txt", "scripts/__pycache__/example.pyc",
                       "local-notes.txt"):
            self.write(self.skill / target, "local data")
        self.assert_success()

    def test_local_link_normalization_and_fragments_remain_supported(self):
        path = self.skill / "assets" / "café template.txt"
        relative = path.relative_to(self.root).as_posix()
        self.write(path, "resource")
        self.listed.add(relative)
        self.save_inventory()
        self.git("add", relative, "public-files.json")
        self.link("./references/../references/guide.md#guide")
        self.link("../SKILL.md#instructions", self.guide)
        self.link("assets/caf%C3%A9%20template.txt?download=1")
        self.assert_success()

    def test_external_and_example_links_do_not_require_bundle_membership(self):
        self.link("https://example.com/missing.md")
        self.link("mailto:docs@example.com")
        self.entry.write_text(self.entry.read_text() +
                              "\n`[Example](assets/missing.txt)`\n\n"
                              "```markdown\n[Example](assets/missing.txt)\n```\n")
        self.assert_success()

    def test_untracked_symlink_aliases_to_bundled_files_are_rejected(self):
        original = self.entry.read_text()
        aliases = (
            (self.skill / "alias.md", self.guide, "alias.md"),
            (self.skill / "alias-dir", self.guide.parent, "alias-dir/guide.md"),
            (self.skill / "alias-parent", self.guide.parent,
             "alias-parent/../references/guide.md"),
        )
        for alias, target, link in aliases:
            alias.symlink_to(target, target_is_directory=target.is_dir())
            for prefix in ("", "missing/../", "SKILL.md/../"):
                with self.subTest(link=prefix + link):
                    self.entry.write_text(original)
                    self.link(prefix + link)
                    self.assert_rejected("bundle resource must not traverse a symlink")
            alias.unlink()

    def test_symlink_loop_is_rejected_before_path_resolution(self):
        alias = self.skill / "alias-loop"
        alias.symlink_to(alias.name)
        original = self.entry.read_text()
        for prefix in ("", "missing/../", "SKILL.md/../"):
            with self.subTest(prefix=prefix):
                self.entry.write_text(original)
                self.link(prefix + "alias-loop")
                self.assert_rejected("bundle resource must not traverse a symlink")


if __name__ == "__main__":
    unittest.main()
