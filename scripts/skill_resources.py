"""Check standalone references and linked contents using only the standard library."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit


def unfenced_lines(text: str) -> list[tuple[int, str]]:
    """Return numbered Markdown lines outside backtick and tilde fences."""
    result = []
    fence: tuple[str, int] | None = None
    for number, line in enumerate(text.splitlines(), 1):
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if match:
            marker, tail = match.groups()
            if fence is None:
                fence = (marker[0], len(marker))
            elif marker[0] == fence[0] and len(marker) >= fence[1] and not tail.strip():
                fence = None
            continue
        if fence is None:
            result.append((number, line))
    return result


def markdown_headings(text: str) -> list[tuple[int, int, str, str]]:
    """Return ATX headings with GitHub-style, duplicate-aware fragment IDs."""
    result = []
    used: set[str] = set()
    for number, line in unfenced_lines(text):
        match = re.match(r"^ {0,3}(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        marks, title = match.groups()
        plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", title)
        plain = re.sub(r"<[^>]+>", "", plain).lower()
        base = "".join(
            char
            for char in plain
            if char in "-_ " or unicodedata.category(char)[0] in {"L", "N"}
        ).replace(" ", "-")
        anchor = base
        suffix = 0
        while anchor in used:
            suffix += 1
            anchor = f"{base}-{suffix}"
        used.add(anchor)
        result.append((number, len(marks), title, anchor))
    return result


def markdown_links(text: str) -> list[str]:
    """Read inline link destinations outside fenced examples and inline code."""
    result = []
    for _, line in unfenced_lines(text):
        # Code spans are examples, not resource links.
        line = re.sub(r"(`+)(.*?)\1", lambda m: " " * len(m[0]), line)
        for match in re.finditer(r"\[[^\]\n]*\]\(([^)\n]+)\)", line):
            target = match[1].strip()
            if target.startswith("<"):
                target = target[1:].split(">", 1)[0]
            else:
                target = target.split(' "', 1)[0].split(" '", 1)[0]
            result.append(target)
    return result


def validate_contents(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if len(text.splitlines()) <= 100:
        return
    headings = markdown_headings(text)
    contents = next((h for h in headings if h[2].casefold() == "contents"), None)
    if contents is None:
        raise ValueError(
            f"{path}: references over 100 lines need a Contents section with linked headings"
        )
    end = next(
        (h[0] for h in headings if h[0] > contents[0]), len(text.splitlines()) + 1
    )
    section = "\n".join(text.splitlines()[contents[0] : end - 1])
    linked = {
        unquote(target[1:])
        for target in markdown_links(section)
        if target.startswith("#")
    }
    expected = {h[3] for h in headings if h[1] > 1 and h != contents}
    missing = expected - linked
    invalid = linked - {h[3] for h in headings}
    if missing or invalid:
        raise ValueError(
            f"{path}: Contents anchors missing={sorted(missing)}, invalid={sorted(invalid)}"
        )


def validate_reference_resources(skill_dir: Path) -> None:
    """Require direct entrypoint links, local targets, valid anchors and long-file indexes."""
    root = skill_dir.resolve()
    skill_md = skill_dir / "SKILL.md"
    references = skill_dir / "references"
    paths = sorted(references.rglob("*.md")) if references.is_dir() else []
    for path in paths:
        if path.parent != references:
            raise ValueError(f"{path}: references must stay one level deep")
    linked: set[Path] = set()
    for path in [skill_md, *paths]:
        for target in markdown_links(path.read_text(encoding="utf-8")):
            parts = urlsplit(target)
            if parts.scheme or parts.netloc:
                continue
            resolved = (
                (path.parent / unquote(parts.path)).resolve()
                if parts.path
                else path.resolve()
            )
            if not resolved.is_relative_to(root):
                raise ValueError(
                    f"{path}: link {target!r} escapes the standalone skill"
                )
            if not resolved.is_file():
                raise ValueError(f"{path}: broken local link {target!r}")
            if parts.fragment and resolved.suffix == ".md":
                anchors = {
                    h[3]
                    for h in markdown_headings(resolved.read_text(encoding="utf-8"))
                }
                if unquote(parts.fragment) not in anchors:
                    raise ValueError(f"{path}: incorrect anchor in {target!r}")
            if path == skill_md:
                linked.add(resolved)
    for path in paths:
        if path.resolve() not in linked:
            raise ValueError(
                f"{path}: reference file is never linked directly from SKILL.md"
            )
        validate_contents(path)
