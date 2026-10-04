"""Exercise resource reachability, index boundaries, anchors, and fenced examples."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "scripts" / "skill_resources.py"
if not HELPER.exists():
    HELPER = ROOT / "scripts" / "validate_public.py"
SPEC = importlib.util.spec_from_file_location("resource_gate", HELPER)
resources = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(resources)


class ReferenceResourceTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.skill = Path(directory.name) / "standalone-skill"
        (self.skill / "references").mkdir(parents=True)
        self.entry = self.skill / "SKILL.md"
        self.entry.write_text("# Skill\n\nRead [guide](references/guide.md).\n")
        self.guide = self.skill / "references" / "guide.md"

    def check(self) -> None:
        resources.validate_reference_resources(self.skill)

    def write_lines(self, count: int, prefix: str) -> None:
        lines = prefix.splitlines()
        self.guide.write_text("\n".join(lines + ["body"] * (count - len(lines))) + "\n")
        self.assertEqual(len(self.guide.read_text().splitlines()), count)

    def test_100_lines_does_not_require_contents(self) -> None:
        self.write_lines(100, "# Guide\n\n## Steps\n")
        self.check()

    def test_101_lines_requires_contents(self) -> None:
        self.write_lines(101, "# Guide\n\n## Steps\n")
        with self.assertRaisesRegex(ValueError, "Contents section"):
            self.check()

    def test_101_lines_with_linked_contents_passes(self) -> None:
        self.write_lines(
            101, "# Guide\n\n## Contents\n\n- [Steps](#steps)\n\n## Steps\n"
        )
        self.check()

    def test_contents_heading_without_links_is_rejected(self) -> None:
        self.write_lines(101, "# Guide\n\n## Contents\n\n- Steps\n\n## Steps\n")
        with self.assertRaisesRegex(ValueError, "Contents anchors"):
            self.check()

    def test_incorrect_contents_anchor_is_rejected(self) -> None:
        self.write_lines(
            101, "# Guide\n\n## Contents\n\n- [Steps](#step)\n\n## Steps\n"
        )
        with self.assertRaisesRegex(ValueError, "incorrect anchor"):
            self.check()

    def test_missing_subheading_is_rejected(self) -> None:
        self.write_lines(
            101,
            "# Guide\n\n## Contents\n\n- [Steps](#steps)\n\n## Steps\n\n### Retry\n",
        )
        with self.assertRaisesRegex(ValueError, "Contents anchors.*retry"):
            self.check()

    def test_example_headings_are_excluded_from_contents(self) -> None:
        for marker in ("```", "~~~", "````"):
            with self.subTest(marker=marker):
                prefix = (
                    "# Guide\n\n## Contents\n\n- [Steps](#steps)\n\n## Steps\n\n"
                    f"{marker}markdown\n## Example-only heading\n{marker}\n"
                )
                self.write_lines(101, prefix)
                self.check()

    def test_shorter_inner_fence_does_not_close_outer_example(self) -> None:
        self.write_lines(
            101,
            "# Guide\n\n## Contents\n\n- [Steps](#steps)\n\n## Steps\n\n"
            "````markdown\n```python\n## Example\n```\n## Still example\n````\n",
        )
        self.check()

    def test_fenced_contents_is_not_an_index(self) -> None:
        self.write_lines(
            101,
            "# Guide\n\n```markdown\n## Contents\n- [Steps](#steps)\n```\n\n## Steps\n",
        )
        with self.assertRaisesRegex(ValueError, "Contents section"):
            self.check()

    def test_nested_only_reference_is_rejected(self) -> None:
        self.guide.write_text("# Guide\n\nRead [more](more.md).\n")
        (self.skill / "references" / "more.md").write_text("# More\n")
        with self.assertRaisesRegex(ValueError, "linked directly from SKILL.md"):
            self.check()

    def test_orphaned_reference_is_rejected(self) -> None:
        self.guide.write_text("# Guide\n")
        (self.skill / "references" / "orphan.md").write_text("# Orphan\n")
        with self.assertRaisesRegex(ValueError, "linked directly from SKILL.md"):
            self.check()

    def test_fenced_and_inline_example_links_do_not_reach_resources(self) -> None:
        self.guide.write_text("# Guide\n")
        for example in (
            "```markdown\n[Guide](references/guide.md)\n```",
            "`[Guide](references/guide.md)`",
        ):
            with self.subTest(example=example):
                self.entry.write_text("# Skill\n\n" + example + "\n")
                with self.assertRaisesRegex(
                    ValueError, "linked directly from SKILL.md"
                ):
                    self.check()

    def test_nested_reference_folder_is_rejected(self) -> None:
        self.guide.write_text("# Guide\n")
        nested = self.skill / "references" / "deep"
        nested.mkdir()
        (nested / "more.md").write_text("# More\n")
        self.entry.write_text(
            self.entry.read_text() + "\n[More](references/deep/more.md)\n"
        )
        with self.assertRaisesRegex(ValueError, "one level deep"):
            self.check()

    def test_direct_reference_with_section_anchor_passes(self) -> None:
        self.guide.write_text("# Guide\n\n## Retry\n\nCheck the result.\n")
        self.entry.write_text("# Skill\n\nRead [retry](references/guide.md#retry).\n")
        self.check()

    def test_cross_reference_anchor_is_checked(self) -> None:
        self.guide.write_text("# Guide\n\n[Missing](#missing)\n")
        with self.assertRaisesRegex(ValueError, "incorrect anchor"):
            self.check()

    def test_duplicate_and_punctuated_heading_anchors(self) -> None:
        self.write_lines(
            101,
            "# Guide\n\n## Contents\n\n- [First](#post-jobs)\n- [Second](#post-jobs-1)\n"
            "- [Café](#café)\n\n## `POST /jobs`\n\nfirst\n\n## `POST /jobs`\n\nsecond\n\n## Café\n",
        )
        self.check()

    def test_reference_to_sibling_installation_is_rejected(self) -> None:
        self.guide.write_text("# Guide\n\n[Sibling](../../sibling/SKILL.md)\n")
        with self.assertRaisesRegex(ValueError, "escapes the standalone skill"):
            self.check()


if __name__ == "__main__":
    unittest.main()
