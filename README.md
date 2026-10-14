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

## Maintenance

```sh
uv sync --dev
uv run python scripts/validate.py
uv run pytest -q
uv run ruff check scripts tests
```

The checker validates metadata, local resources, and the tracked bundle inventory. Update `public-files.json` deliberately when adding a distributable file.

Metadata checks require YAML mappings and frontmatter delimiters on their own lines.
Skill names follow the [Agent Skills naming constraints](https://agentskills.io/specification#name-field):
1–64 characters after Unicode NFKC normalization, lowercase letters/digits and hyphens,
with no leading, trailing, or consecutive hyphens. Names must still exactly match their
directory. Invalid YAML reports its file and source location when the parser supplies one.
These checks preserve this repository’s required version and risk tier; they are not a
complete schema for every optional metadata field.
