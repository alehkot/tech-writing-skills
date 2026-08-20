---
name: reference-docs-writer
description: >-
  Reference documentation for lookup-oriented technical facts: API endpoint references, CLI command references, configuration options, parameters, schemas, data dictionaries, error codes, status codes, syntax rules, system limits, and compatibility tables. Use for separating reference material from tasks and concepts, organizing facts for retrieval, and keeping examples complete and accurate.
  Use when incomplete source facts must be represented as unknowns instead of filled with plausible values.
metadata:
  version: "1.1.0"
  risk_tier: low
---

# Reference Docs Writer

## Overview

Create reference topics that let readers quickly find exact facts. Optimize for retrievability, consistent item patterns, complete syntax, accurate examples, and clear boundaries between facts, tasks, and concepts.

Read [references/reference-patterns.md](references/reference-patterns.md) when drafting or revising API, CLI, configuration, schema, error-code, syntax, limits, or compatibility reference material.

## Workflow

1. Identify the reference family: API, CLI, config, schema, error code, status code, syntax, limit, compatibility, or data dictionary.
2. Extract objective facts from the source material. Move procedures to task topics and extended explanation to concept topics instead of burying them in the reference.
3. Choose a retrieval order: alphabetical, numerical, lifecycle order, endpoint path order, or category grouping. Use one order consistently.
4. Define the repeated item pattern before writing entries. Each item should have the same headings unless a field is truly not applicable.
5. Use static item names for headings. Do not use gerund headings such as `Creating a workspace`; gerunds signal task topics.
6. Open every method, endpoint, or command description with a third-person present verb stating what it does, such as `Creates`, `Lists`, or `Returns`. Never open with an imperative; the imperative belongs in task steps. Use precise technical verbs, not anthropomorphic ones such as `knows` or `sees`.
7. Use consistent names for fields, parameters, commands, statuses, and errors. Define acronyms, aliases, and specialized terms at first use or in a glossary-style entry.
8. Present dense facts in tables or definition lists. Keep prose short and only where it clarifies constraints, defaults, or usage boundaries.
9. Keep list items and table rows parallel so readers can compare facts quickly. Use consistent units within a column and format numbers with a space before unit abbreviations, such as `16 GB`. Use the byte system the documented technology actually uses: decimal `kB`/`MB`/`GB` for powers of 1000, binary `KiB`/`MiB`/`GiB` for powers of 1024. Repeat the unit on every range endpoint and join endpoints with `to`, not a hyphen. Write version ranges as `2.2 or later`, never `2.2+` or `above`, and write rates with `per` in prose.
10. Make syntax complete: document required and optional elements, defaults, valid values, data types, units, constraints, return values, and error behavior. Put literal values, data types, commands, fields, parameters, headers, and error codes in code font.
11. Add examples that match the documented syntax. Use copyable snippets for API/CLI/config references; if an example is complex, use numbered annotations below the code instead of inline explanation.
12. For API endpoints, include error response information when status codes or failure modes appear. For error-code references, define any headers, fields, or retry signals you mention, such as `Retry-After`.
13. Track unknown facts while drafting. If the source omits a default, valid value, field type, status behavior, limit, or compatibility boundary, mark it as `Not specified` or an open question instead of inventing it.
14. Add cross-links or "Related topics" only when they help the reader move to a task or concept without cluttering the lookup surface.

## Completion Criterion

Complete the task only when the reference surface is lookup-ready: all sourced items use the chosen retrieval order and repeated item pattern, required and optional facts are captured where present, unknown values are explicitly marked, examples match the documented syntax, and task or concept material is split out or linked; every applicable self-check item passes.

## Output Shape

Use this default item pattern unless the repo or product already has a reference template:

````markdown
# [Reference family]

Use this reference to look up [item type].

## [Item name]

Purpose: [One-sentence factual purpose.]

Syntax:
```text
[syntax]
```

Parameters:
| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| [name] | [type] | [yes/no] | [default] | [description] |

Returns:
[Return value, response shape, output, or side effect.]

Example:
```text
[copyable example]
```

Usage notes:
- [Constraint, restriction, compatibility, or gotcha.]

Related:
- [Task or concept topic, if useful.]
````

## Self-Check

- [ ] The topic is lookup-oriented and does not read like a procedure or explainer.
- [ ] The entries follow a consistent repeated pattern.
- [ ] Entry headings are static nouns or item names, not gerund task headings.
- [ ] Method, endpoint, and command descriptions open with a third-person present verb, not an imperative.
- [ ] Items are ordered for quick retrieval.
- [ ] Tables or lists carry dense facts instead of long paragraphs.
- [ ] Terms, field names, parameter names, and statuses are consistent across entries.
- [ ] Tables and lists use parallel wording and comparable detail.
- [ ] Units are formatted consistently, and comparable table columns use comparable units.
- [ ] Byte units match the technology's actual system (`GB` vs `GiB`), ranges repeat the unit and join endpoints with `to`, and version ranges use `or later` wording.
- [ ] Required, optional, default, valid values, types, units, restrictions, and error behavior are documented where relevant.
- [ ] Error fields, status codes, and retry signals are documented where relevant.
- [ ] Literal values, data types, commands, fields, parameters, headers, and error codes use code font where needed.
- [ ] Examples match the documented syntax and use defined placeholders; complex examples use numbered annotations.
- [ ] Placeholders follow one convention across the doc set (canonical placeholder rules: task-docs-writer).
- [ ] Unknown defaults, valid values, limits, compatibility rules, and response behavior are marked rather than invented.
- [ ] Acronyms and specialized terms are defined at first use or in a glossary-style entry.
- [ ] Related task or concept links are helpful and not used as a substitute for missing facts.
- [ ] Produced-doc headings use sentence case, except entry headings that are literal item names such as `POST /workspaces` (canonical capitalization rules: docs-style-editor).

## Gotchas

- Do not use gerund or task-style headings such as `Creating a workspace` for reference entries; use item names such as `POST /workspaces` or `workspace create`.
- Do not mix step-by-step instructions into a reference entry. Link to a task topic instead.
- Do not explain broad architecture in a reference entry. Link to a concept topic instead.
- Do not sort arbitrarily. If the order is not alphabetical or numerical, state the organizing principle.
- Do not turn partial source data into complete-looking tables without marking gaps.
- Do not open a reference description with an imperative: `Creates a task` describes what the API does; `Create a task` belongs in a task step.
- Do not substitute `GB` for `GiB` or the reverse; a wrong byte unit is a factual error, not a style preference.

## Attribution

Parts of this skill are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified. This skill is not affiliated with or endorsed by Google.
