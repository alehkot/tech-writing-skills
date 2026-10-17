"""Check standalone references and linked contents using only the standard library."""

from __future__ import annotations

import re
import string
import unicodedata
from os.path import abspath
from pathlib import Path
from urllib.parse import unquote, urlsplit


def require_bundled_file(
    path: Path, skill_dir: Path, bundle_files: set[Path] | None
) -> None:
    """Check bundle membership without accepting an untracked symlink alias."""
    if bundle_files is None:
        return
    absolute = path.absolute()
    boundary = skill_dir.absolute()
    # Check original and lexically normalized prefixes before resolving links.
    # A canceled missing/non-directory prefix can otherwise hide an alias from
    # is_symlink(), while resolve() still follows it after removing dot segments.
    for component in (absolute, *absolute.parents):
        if component.is_symlink() or Path(abspath(component)).is_symlink():
            raise ValueError(f"{path}: bundle resource must not traverse a symlink")
        if component == boundary:
            break
    if Path(abspath(path)) not in bundle_files:
        raise ValueError(
            f"{path}: file is not in the tracked bundle inventory; "
            "update public-files.json and stage the file"
        )


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
        # Use the same destination boundaries as resource extraction so a
        # parenthesized target does not leak into the heading's fragment ID.
        pieces = []
        consumed = 0
        for match, _, end in inline_links(title):
            pieces.extend((title[consumed:match.start()], match[1]))
            consumed = end
        pieces.append(title[consumed:])
        plain = "".join(pieces)
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


def inline_destination(line: str, start: int) -> tuple[str, int] | None:
    """Read a single-line destination and optional title after a link's opening (."""
    position = start
    while position < len(line) and line[position] in " \t":
        position += 1
    angled = position < len(line) and line[position] == "<"
    if angled:
        position += 1
    target: list[str] = []
    depth = 0
    while position < len(line):
        char = line[position]
        if char == "\\" and position + 1 < len(line):
            following = line[position + 1]
            if following in string.punctuation:
                target.append(following)
                position += 2
                continue
        if angled:
            if char == ">":
                position += 1
                break
            if char == "<":
                return None
        else:
            if char in " \t" or (char == ")" and depth == 0):
                break
            if ord(char) < 32 or ord(char) == 127:
                return None
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
        target.append(char)
        position += 1
    else:
        return None
    if depth:
        return None

    end = position
    while end < len(line) and line[end] in " \t":
        end += 1
    if end < len(line) and line[end] == ")":
        return "".join(target), end + 1
    # A title must be separated from the destination by whitespace.
    if end == position or end >= len(line) or line[end] not in "\"'(":
        return None
    close = ")" if line[end] == "(" else line[end]
    end += 1
    while end < len(line):
        char = line[end]
        if char == "\\" and end + 1 < len(line) and line[end + 1] in string.punctuation:
            end += 2
            continue
        if char == close:
            end += 1
            break
        if close == ")" and char == "(":
            return None
        end += 1
    else:
        return None
    while end < len(line) and line[end] in " \t":
        end += 1
    if end < len(line) and line[end] == ")":
        return "".join(target), end + 1
    return None


def inline_links(line: str) -> list[tuple[re.Match[str], str, int]]:
    """Return simple inline labels with complete destinations and source bounds."""
    result = []
    position = 0
    pattern = re.compile(r"\[([^\]\n]*)\]\(")
    while match := pattern.search(line, position):
        position = match.end()
        parsed = inline_destination(line, position)
        if parsed is not None:
            target, position = parsed
            result.append((match, target, position))
    return result


def markdown_links(text: str) -> list[str]:
    """Read inline link destinations outside fenced examples and inline code."""
    result = []
    for _, line in unfenced_lines(text):
        # Code spans are examples, not resource links.
        line = re.sub(r"(`+)(.*?)\1", lambda m: " " * len(m[0]), line)
        result.extend(target for _, target, _ in inline_links(line))
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


def validate_reference_resources(
    skill_dir: Path, bundle_files: set[Path] | None = None
) -> None:
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
        require_bundled_file(path, skill_dir, bundle_files)
        for target in markdown_links(path.read_text(encoding="utf-8")):
            parts = urlsplit(target)
            if parts.scheme or parts.netloc:
                continue
            local_path = (
                path.parent / unquote(parts.path)
                if parts.path
                else path
            )
            require_bundled_file(local_path, skill_dir, bundle_files)
            resolved = local_path.resolve()
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
