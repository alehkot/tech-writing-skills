# Reference Documentation Patterns

## Use When

Load this reference for API endpoints, CLI commands, config options, schemas, data dictionaries, error codes, status codes, syntax rules, compatibility matrices, system limits, and other lookup-oriented facts.

## Source Principles

- Reference topics give quick access to facts that support tasks.
- Reference topics should be separate from task and concept topics so readers can retrieve facts without reading procedure or background material.
- Reference material benefits from repeated patterns, tables, lists, and stable ordering.
- Syntax and examples must be complete enough that readers can apply them without guessing.
- Reference headings should be static nouns, item names, or noun phrases, not gerunds that imply a task.
- Consistent terminology and parallel rows help readers compare facts without reinterpreting each entry.
- Incomplete source facts should remain visibly incomplete; a polished table must not imply that unknown defaults, values, limits, or response behavior were supplied.

## Topic Boundary Test

- Task topic: "How do I do this?"
- Concept topic: "What is this and why does it matter?"
- Reference topic: "What exactly are the allowed values, syntax, fields, messages, or limits?"

If the draft answers more than one question, split it or add links between topics.

## Retrieval Orders

Choose one:

- Alphabetical by command, property, class, or field name.
- Numerical by status code, message ID, or error code.
- Path order for REST endpoints.
- Category order for related settings or capabilities.
- Lifecycle order only when the facts are naturally consumed in sequence.

## Consistency Rules

- Use the same term for each field, option, status, and object across all entries.
- Define acronyms, aliases, and specialized terms at first use or in a glossary entry.
- Keep table cells parallel: same grammar, same level of detail, and comparable units.
- Keep lists parallel: do not mix syntax, examples, causes, and recovery actions at the same level.
- Use the same unit within a table column when values are comparable.
- Put a space between a number and a unit abbreviation, and do not pluralize the abbreviation: `64 GB`, not `64GB` or `64 GBs`.
- Wrap literal values, data types, commands, fields, parameters, headers, retry signals, and error codes in code font when they appear in prose or tables.
- If you mention a response header or field in a status-code, error-code, or recovery entry, define what it means.
- Use `Not specified` or an explicit open question when the source does not provide a type, default, valid value, limit, compatibility boundary, response field, or error behavior.
- Avoid `e.g.`, `i.e.`, `etc.`, and `and so on`; use `for example`, `that is`, or a clearly scoped non-exhaustive list.

## API Endpoint Pattern

````markdown
## `POST /workspaces`

Creates a workspace record.

### Request
| Field | Type | Required | Description |
| --- | --- | --- | --- |

### Response
| Field | Type | Description |
| --- | --- | --- |

### Status Codes
| Code | Meaning |
| --- | --- |

### Error Responses
| Status or field | Meaning | Recovery |
| --- | --- | --- |

### Example
````

## CLI Command Pattern

````markdown
## `acme workspace create`

Creates a workspace.

### Syntax
```text
acme workspace create --name <name> [--region <region>]
```

### Options
| Option | Required | Default | Description |
| --- | --- | --- | --- |

### Example
````

## Error Code Pattern

````markdown
## `E1024`

Meaning: [What happened.]

Cause: [Likely condition.]

Recovery: [Where to go next; keep procedural detail short or link to a task.]

Fields and headers: [Define any response fields, headers, or retry signals mentioned in recovery.]

Related: [API, command, or task.]
````

## Numbered Annotation Pattern

Use numbered annotations when an example has multiple fields or lines that need explanation. Keep the code copyable and put explanations below it.

````markdown
### Example
```json
{
  "name": "payments",
  "region": "us-east-1",
  "tags": {"team": "core"}
}
```

1. `name` must be unique within the account.
2. `region` defaults to `us-east-1` when omitted.
3. `tags` accepts string key-value pairs.
````

## Review Checklist

- The reference has a clear retrieval order.
- Entries use repeated headings and fields.
- Entry headings are static nouns or item names, not gerund task headings.
- Dense factual data is in tables or lists.
- Terms are consistent, and acronyms or aliases are defined.
- Tables and lists are parallel enough for quick comparison.
- Units and literal values are formatted consistently.
- Syntax distinguishes required and optional elements.
- Defaults, valid values, units, restrictions, and error behavior are present.
- Headers, fields, retry signals, and related response metadata are defined when mentioned.
- Source gaps are marked and do not look like complete facts.
- Examples are copyable and match the documented syntax; complex examples use numbered annotations.
- Long task steps and conceptual background are split out or linked.
