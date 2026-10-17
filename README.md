# Technical Writing Skills for Engineers

This repository bundles Agent Skills for engineers and engineering teams who need help turning technical material into useful written artifacts: proposals, reports, documentation, and explanatory content.

The skills follow the Agent Skills directory model: each skill is a folder with a required `SKILL.md` and optional `references/`. See the Agent Skills specification at https://agentskills.io/specification.

## Skills

- [accessibility-inclusion-editor](skills/accessibility-inclusion-editor/SKILL.md)
- [docs-style-editor](skills/docs-style-editor/SKILL.md)
- [proposal-argument-crafter](skills/proposal-argument-crafter/SKILL.md)
- [reference-docs-writer](skills/reference-docs-writer/SKILL.md)
- [task-docs-writer](skills/task-docs-writer/SKILL.md)
- [technical-content-clarifier](skills/technical-content-clarifier/SKILL.md)
- [technical-docs-reviewer](skills/technical-docs-reviewer/SKILL.md)
- [technical-report-writer](skills/technical-report-writer/SKILL.md)
- [write-simplified-technical-english](skills/write-simplified-technical-english/SKILL.md)

## Install

Clone this repository, then copy or symlink the desired folder from `skills/` into your agent's skills directory.

```sh
npx skills add alehkot/tech-writing-skills --skill '*'
```

Each skill includes an unchanged copy of the repository `LICENSE`, so the notice
travels with a standalone folder copy. Keep it with the installed skill. Existing
source attribution and third-party notices within the skill remain unchanged.

## Maintenance

```sh
uv sync --dev
uv run python scripts/validate.py
uv run pytest -q
uv run ruff check scripts tests
```

The checker validates metadata, local resources, and the tracked bundle inventory. Update `public-files.json` deliberately when adding a distributable file.

Required skill entrypoints, UI metadata, reference documents, and parsed local
Markdown link/image targets must be ordinary files in that tracked inventory.
A file that exists only in your working directory, including an ignored file,
cannot satisfy a bundled dependency. Update the inventory and `.gitignore`
allowlist as needed, then stage new files before running the checks. Unreferenced
local caches and scratch files outside the checked reference documents do not
need to be bundled.
These checks use the current working-tree contents and Git index file membership;
they do not require a clean working tree or expand the supported Markdown syntax.

Resource links support single-line inline links and images with bare destinations
(including balanced or backslash-escaped parentheses), angle-bracket destinations,
and optional quoted or parenthesized titles. The checker uses a deliberately small
Markdown parser, not a complete CommonMark renderer: reference-style links,
multiline links, and complex inline markup are outside its supported syntax.
Fenced and inline-code examples do not count as resource links.

Metadata checks require YAML mappings and frontmatter delimiters on their own lines.
Explicit duplicate keys, including nested mappings and keys that resolve to the
same Python dictionary key, fail instead of silently overwriting a value.
YAML aliases and merge defaults remain supported: an explicit key may override
an inherited key, and earlier mappings in a merge sequence take precedence.
Use one merge key with a sequence for multiple defaults.
Skill names follow the [Agent Skills naming constraints](https://agentskills.io/specification#name-field):
1–64 characters after Unicode NFKC normalization, lowercase letters/digits and hyphens,
with no leading, trailing, or consecutive hyphens. Names must still exactly match their
directory. Invalid YAML reports its file and source location when the parser supplies one.
These checks preserve this repository’s required version and risk tier; they are not a
complete schema for every optional metadata field.

The checker also requires each skill’s `LICENSE` to be tracked and byte-for-byte
identical to the repository `LICENSE`. If the repository notice is deliberately
updated, update all bundled copies together; the validator does not rewrite them.
