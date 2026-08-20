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

- Open every method, endpoint, or command description with a third-person present `-s` verb stating what it does: `Creates a workspace`, never the imperative `Create a workspace`. Reserve the imperative for task steps.
- Use precise technical verbs in descriptions, never anthropomorphic ones: a service `returns`, `validates`, or `detects`; it does not `know`, `see`, or `decide to tell` another component anything.
- Use the same term for each field, option, status, and object across all entries.
- Define acronyms, aliases, and specialized terms at first use or in a glossary entry.
- Keep table cells parallel: same grammar, same level of detail, and comparable units.
- Keep lists parallel: do not mix syntax, examples, causes, and recovery actions at the same level.
- Use the same unit within a table column when values are comparable.
- Put a space between a number and a unit abbreviation, and do not pluralize the abbreviation: `16 GB`, not `16GB` or `16 GBs`.
- Use the byte system the documented technology actually uses: decimal `kB`/`MB`/`GB` for powers of 1000, binary `KiB`/`MiB`/`GiB` for powers of 1024. Never substitute one for the other; a wrong byte unit is a factual error, not a style choice.
- Repeat the unit on every number in a range and join the endpoints with `to`, never a hyphen: `5 GiB to 20 GiB`, not `5-20 GiB`.
- Write version ranges as `2.2 or later` or `2.2 or earlier`, never `2.2+`, `above`, or `below`.
- Write rates with `per` in prose, such as `requests per day`; reserve the slash form for space-constrained tables.
- Never pluralize a class or type name in code font; add a plural noun instead: `Workspace objects`, never `Workspaces` or an invented inflection. The exception is a class name that is also a common term: when the doc uses it generically, in lowercase and plain font, pluralize it as an ordinary word, such as workspaces for the general concept.
- Never attach `'s` to a code element such as a method, class, field, or command. Move the possessive to a following noun (`the parseConfig function's return value`) or rewrite (`the value that parseConfig returns`).
- Match class and type name spelling exactly to the code, including capitalization and spacing.
- Follow one placeholder convention across the doc set, the house `<angle-bracket>` form by default (canonical placeholder rules: task-docs-writer).
- Wrap literal values, data types, commands, fields, parameters, headers, retry signals, and error codes in code font when they appear in prose or tables.
- If you mention a response header or field in a status-code, error-code, or recovery entry, define what it means.
- Use `Not specified` or an explicit open question when the source does not provide a type, default, valid value, limit, compatibility boundary, response field, or error behavior.
- Avoid `e.g.`, `i.e.`, `etc.`, and `and so on`; use `for example`, `that is`, or a clearly scoped non-exhaustive list (canonical Latin-abbreviation rule: docs-style-editor).

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

### Status codes
| Code | Meaning |
| --- | --- |

### Error responses
| Status or field | Meaning | Recovery |
| --- | --- | --- |

### Example
````

## API Doc-Comment Pattern

Use these rules when writing doc comments or generated API reference for classes, methods, fields, and similar code elements.

- Describe every public element: each class, interface, constant, field, enum, method, parameter, return value, and thrown exception. If the source does not state an element's behavior, mark it `Not specified` instead of inferring it.
- Write every description in present tense.
- Make the first sentence of a class description state its purpose beyond what the name and signature already say. Keep it short and unique, do not repeat the class name, and do not open with `this class`.
- Do not place a period mid-sentence in a summary; write `for example`, never `e.g.`, because doc generators truncate the summary at the first period.
- Start method descriptions with a fixed verb by kind: `Checks whether ...` for boolean getters, `Gets the ...` for other getters, `Sets the ...`, `Updates the ...`, `Deletes the ...`, or `Registers ...` for mutators, `Called by ... when ...` for callbacks, and `Creates a ...` for factory methods.
- For a boolean parameter that controls behavior, state what happens when it is true and what happens when it is false. For a boolean that reports state, use the form `True if ...; false otherwise.`
- Begin non-boolean parameter descriptions with `The` or `A`, capitalize the first word, and end with a period. State defaults with an explicit `Default:` label.
- Begin non-boolean return descriptions with `The ...`; keep them brief and move detail to the class description.
- Begin exception descriptions with `If ...` when the generator supplies the word `Throws`; otherwise begin with `Thrown when ...`.
- In a deprecation notice, name the replacement and how to migrate in the first sentence. Name the version where deprecation began only when the source states it. Never invent a replacement or a version.

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

Syntax notation for CLI syntax lines (define this legend once for the reader):

- One set of square brackets per optional argument: `[--region <region>]`, as in the pattern above.
- Curly braces with pipe separators for choose-exactly-one groups: `{--json|--yaml}`.
- Three unspaced dots for a repeatable argument: `<file>...`, never the ellipsis character.
- Keep syntax characters such as `[ ]`, `{ }`, `|`, and `...` out of any block the reader is meant to copy and run. Give a runnable common-case command, and handle variants in separate blocks, separate task sections, or with an explicit warning to remove the syntax characters before running.

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

## Code Sample Rules

- Keep code sample lines at or under 80 characters; break and re-indent longer lines.
- Indent samples the way the language's own style guide does, typically two spaces; never mix tabs and spaces within a sample.
- Show omitted code with a comment in the sample's own language, such as `# lines omitted`, never with three dots or an ellipsis character.
- Never present a block that contains an omission as copy-and-run; complete it or label it as abbreviated.
- Never fabricate elided code. If the source does not supply the omitted lines, keep the omission comment and flag the gap.
- Introduce each code sample with a lead-in sentence: end it with a colon when the sample follows immediately, and with a period when other text intervenes.

## Review Checklist

- The reference has a clear retrieval order.
- Entries use repeated headings and fields.
- Entry headings are static nouns or item names, not gerund task headings.
- Dense factual data is in tables or lists.
- Terms are consistent, and acronyms or aliases are defined.
- Tables and lists are parallel enough for quick comparison.
- Units and literal values are formatted consistently.
- Syntax distinguishes required and optional elements, and copyable blocks contain no syntax characters.
- Method, endpoint, and command descriptions open with a third-person present verb, not an imperative.
- Byte units match the technology's actual system, ranges repeat the unit and join endpoints with `to`, and version ranges use `or later` wording.
- Doc-comment entries cover every public element or mark it `Not specified`.
- Defaults, valid values, units, restrictions, and error behavior are present.
- Headers, fields, retry signals, and related response metadata are defined when mentioned.
- Source gaps are marked and do not look like complete facts.
- Examples are copyable and match the documented syntax; complex examples use numbered annotations.
- Long task steps and conceptual background are split out or linked.

## Attribution

Parts of this reference are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified.
