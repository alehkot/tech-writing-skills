---
name: reference-docs-writer
description: >-
  Reference documentation for lookup-oriented technical facts: API endpoint references, CLI command references, configuration options, parameters, schemas, data dictionaries, error codes, status codes, syntax rules, system limits, and compatibility tables. Use for separating reference material from tasks and concepts, organizing facts for retrieval, and keeping examples complete and accurate.
metadata:
  version: "1.0.0"
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
6. Use consistent names for fields, parameters, commands, statuses, and errors. Define acronyms, aliases, and specialized terms at first use or in a glossary-style entry.
7. Present dense facts in tables or definition lists. Keep prose short and only where it clarifies constraints, defaults, or usage boundaries.
8. Keep list items and table rows parallel so readers can compare facts quickly. Use consistent units within a column and format numbers with a space before unit abbreviations, such as `64 GB`.
9. Make syntax complete: document required and optional elements, defaults, valid values, data types, units, constraints, return values, and error behavior. Put literal values, data types, commands, fields, parameters, headers, and error codes in code font.
10. Add examples that match the documented syntax. Use copyable snippets for API/CLI/config references; if an example is complex, use numbered annotations below the code instead of inline explanation.
11. For API endpoints, include error response information when status codes or failure modes appear. For error-code references, define any headers, fields, or retry signals you mention, such as `Retry-After`.
12. Add cross-links or "Related topics" only when they help the reader move to a task or concept without cluttering the lookup surface.

## Completion Criterion

Complete the task only when the reference surface is lookup-ready: all sourced items use the chosen retrieval order and repeated item pattern, required and optional facts are captured where present, examples match the documented syntax, and task or concept material is split out or linked; every applicable self-check item passes.

## Output Shape

Use this default item pattern unless the repo or product already has a reference template:

````markdown
# [Reference Family]

Use this reference to look up [item type].

## [Item Name]

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

Usage Notes:
- [Constraint, restriction, compatibility, or gotcha.]

Related:
- [Task or concept topic, if useful.]
````

## Self-Check

- [ ] The topic is lookup-oriented and does not read like a procedure or explainer.
- [ ] The entries follow a consistent repeated pattern.
- [ ] Entry headings are static nouns or item names, not gerund task headings.
- [ ] Items are ordered for quick retrieval.
- [ ] Tables or lists carry dense facts instead of long paragraphs.
- [ ] Terms, field names, parameter names, and statuses are consistent across entries.
- [ ] Tables and lists use parallel wording and comparable detail.
- [ ] Units are formatted consistently, and comparable table columns use comparable units.
- [ ] Required, optional, default, valid values, types, units, restrictions, and error behavior are documented where relevant.
- [ ] Error fields, status codes, and retry signals are documented where relevant.
- [ ] Literal values, data types, commands, fields, parameters, headers, and error codes use code font where needed.
- [ ] Examples match the documented syntax and use defined placeholders; complex examples use numbered annotations.
- [ ] Acronyms and specialized terms are defined at first use or in a glossary-style entry.
- [ ] Related task or concept links are helpful and not used as a substitute for missing facts.

## Gotchas

- Do not use gerund or task-style headings such as `Creating a workspace` for reference entries; use item names such as `POST /workspaces` or `workspace create`.
- Do not mix step-by-step instructions into a reference entry. Link to a task topic instead.
- Do not explain broad architecture in a reference entry. Link to a concept topic instead.
- Do not sort arbitrarily. If the order is not alphabetical or numerical, state the organizing principle.
