# Reference Documentation Patterns

## Contents

- [Use When](#use-when)
- [Source Principles](#source-principles)
- [Topic Boundary Test](#topic-boundary-test)
- [Source Verification](#source-verification)
- [Retrieval Orders](#retrieval-orders)
- [Consistency Rules](#consistency-rules)
- [Version Ranges](#version-ranges)
- [Version-Range Review Cases](#version-range-review-cases)
- [API Endpoint Pattern](#api-endpoint-pattern)
- [API Doc-Comment Pattern](#api-doc-comment-pattern)
- [CLI Command Pattern](#cli-command-pattern)
- [Error Code Pattern](#error-code-pattern)
- [Numbered Annotation Pattern](#numbered-annotation-pattern)
- [Code Sample Rules](#code-sample-rules)
- [Copyable Example Review Cases](#copyable-example-review-cases)
  - [Line-Wrapping Review Cases](#line-wrapping-review-cases)
- [Review Checklist](#review-checklist)
- [Attribution](#attribution)


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

## Source Verification

- Identify the authoritative source for the documented version: a schema, public command registry, code declarations, captured help output, or supplied specification. Resolve conflicts against that source; if authority or version is unclear, flag the conflict instead of silently choosing.
- Keep actual identifiers and paths. Organize entries around public command groups, endpoint families, or schema sections when that makes lookup easier; do not expose internal implementation details merely to mirror the code tree.
- Prefer an existing generator or read-only inspection command for inventories when available. Check its version, scope, and output before relying on it, and review generated facts for missing descriptions or constraints. Do not run commands that modify the product merely to write its reference.
- Distinguish declarations from examples. A schema or formal syntax declaration can establish types, requiredness, defaults, and valid values; a selected invocation only shows one use. Do not infer those schema facts from argument names, sample values, or the presence of an argument in an example. Label selected invocations as examples instead of promoting them to complete syntax declarations.
- Treat an inventory as evidence only for the facts it contains. A command name or brief description does not establish accepted states, return fields, or the absence of additional options; leave those details unspecified unless the source establishes them.
- For counts and directory trees, state what is included and excluded and tie the claim to the inspected version or snapshot. Include the regeneration command or source location in a short maintenance note. If a fresh check is unavailable, label the snapshot or verification gap; never imply that supplied output was executed during the writing task.

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
- Preserve the complete set of versions established by the source; apply the [version-range guidance](#version-ranges), not a blanket `or later` rewrite.
- Write rates with `per` in prose, such as `requests per day`; reserve the slash form for space-constrained tables.
- Never pluralize a class or type name in code font; add a plural noun instead: `Workspace objects`, never `Workspaces` or an invented inflection. The exception is a class name that is also a common term: when the doc uses it generically, in lowercase and plain font, pluralize it as an ordinary word, such as workspaces for the general concept.
- Never attach `'s` to a code element such as a method, class, field, or command. Move the possessive to a following noun (`the parseConfig function's return value`) or rewrite (`the value that parseConfig returns`).
- Match class and type name spelling exactly to the code, including capitalization and spacing.
- Follow one placeholder convention across the doc set, the house `<angle-bracket>` form by default (canonical placeholder rules: task-docs-writer).
- Wrap literal values, data types, commands, fields, parameters, headers, retry signals, and error codes in code font when they appear in prose or tables.
- If you mention a response header or field in a status-code, error-code, or recovery entry, define what it means.
- Use `Not specified` or an explicit open question when the source does not provide a type, default, valid value, limit, compatibility boundary, response field, or error behavior. An empty template field is not evidence of absence: use `None` or `No options` only when the source explicitly says so.
- Avoid `e.g.`, `i.e.`, `etc.`, and `and so on`; use `for example`, `that is`, or a clearly scoped non-exhaustive list (canonical Latin-abbreviation rule: docs-style-editor).

## Version Ranges

Compatibility requirements and affected-version ranges are facts, not just wording choices.

- Use `2.2 or later` for a source-established inclusive lower bound and `2.2 or earlier` for an inclusive upper bound. For a strict bound, use `later than 2.2` or `earlier than 2.2`; do not add the boundary version to the range.
- Keep both endpoints of a bounded range, and state whether each is included. Preserve exclusions and alternatives as well. Do not turn `2.2 or later, but earlier than 3.0` into `2.2 or later`.
- Keep machine-readable constraints, version strings, and configuration literals unchanged. If prose would be ambiguous or cumbersome, reproduce the sourced constraint and explain it without replacing it.
- Use the documented product or ecosystem's ordering and range semantics. Do not assume every version scheme is SemVer, infer support for prereleases, expand shorthand from memory, or replace a strict bound with a guessed next release. A later publication date does not necessarily mean a higher version number.
- When the source leaves a bound, its inclusivity, or a range's meaning unclear, preserve the supplied wording and flag the specific uncertainty. Do not invent compatibility to make the prose smoother.

The [Google word list](https://developers.google.com/style/word-list#later) supplies the prose preference for `later` and `earlier`; that preference does not change which versions are included. The [npm range documentation](https://github.com/npm/node-semver#ranges) illustrates why strict and inclusive bounds, combined constraints, and prerelease handling must remain distinct. Apply npm semantics only when npm is the documented context.

## Version-Range Review Cases

These original editorial cases check source preservation. They are not model-behavior evaluations or proof that a product supports any example version. For the comparator cases, the source explicitly uses npm ranges and stable releases; retain the literal constraint alongside any prose explanation.

| Supplied source and context | Expected decision | Rewrite to reject |
| --- | --- | --- |
| `>=2.2.0` | `2.2.0 or later`, retaining npm's prerelease rules. | Excluding `2.2.0` or claiming every prerelease is included. |
| `>2.2.0` | `Later than 2.2.0`; preserve the exclusive bound. | `2.2.0 or later` or an invented next release. |
| `<=3.0.0` | `3.0.0 or earlier`. | `Earlier than 3.0.0`. |
| `<3.0.0` | `Earlier than 3.0.0`. | `3.0.0 or earlier`. |
| `>=2.2.0 <3.0.0` | `2.2.0 or later, but earlier than 3.0.0`; keep both bounds. | An unbounded `2.2.0 or later` or including `3.0.0`. |
| `>=2.2.0 <2.3.0` or `>=2.4.0 <3.0.0` | Keep the alternatives and the gap between them. | Collapsing them to `>=2.2.0 <3.0.0`. |
| A manifest contains `^2.2.0`, and no interpretation is requested. | Preserve the literal; if an explanation is needed, verify the ecosystem semantics first. | Replacing the manifest value with prose or assuming it means every later major release. |
| `Supports versions after 2.2`, with no stated version scheme or boundary clarification. | Preserve and flag the intended ordering and bound; do not guess a complete supported-version set. | Treating `2.2` as included or inventing an upper bound. |

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
- Separate command-synopsis notation from executable syntax. Optional-argument markers (`[--verbose]`), choice groups (`{--json|--yaml}`), and repetition markers (`<file>...`) belong in a labeled syntax block, not a copy-and-run example. Select a source-supported invocation for the task or show alternatives separately; do not tell readers to delete punctuation indiscriminately. Preserve characters that are part of the actual language or data, including shell pipes, test brackets, variable-expansion braces, JSON objects and arrays, and literal strings containing `...`.

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

- Aim for code sample lines of 80 characters or fewer only when the actual language or shell permits an equivalent wrap. Preserve literal values, quoting, argument boundaries, and meaningful newlines. Use valid syntax break points and verify that the result behaves identically; when that cannot be verified, keep the original long line and flag the gap. Never split a URL, path, or string value merely to meet the width target.
- For shell examples, identify the shell and version from the source, not the operating system. Bash backslash continuation, cmd.exe caret continuation, and PowerShell backtick continuation are not interchangeable. Prefer supported natural syntax breaks and keep explicit continuation characters immediately before the newline, without trailing spaces. An unspecified shell is a reason to leave the command intact. See the [shell comparison](https://learn.microsoft.com/en-us/cli/azure/get-started-tutorial-2-environment-syntax?view=azure-cli-latest#be-aware-of-line-continuation-characters), [Bash escaping rules](https://www.gnu.org/s/bash/manual/html_node/Escape-Character.html) and [PowerShell parsing guidance](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_parsing?view=powershell-7.5#line-continuation).
- Indent samples the way the language's own style guide does, typically two spaces; never mix tabs and spaces within a sample.
- Show omitted code with a comment in the sample's own language, such as `# lines omitted`, never with three dots or an ellipsis character.
- Never present a block that contains an omission as copy-and-run; complete it or label it as abbreviated.
- Keep prompt prefixes out of copyable commands. Label any prompt-bearing interactive session as a transcript, unless the rendered copy action is verified to exclude the prompts. Preserve executable syntax such as `$HOME`.
- Never fabricate elided code. If the source does not supply the omitted lines, keep the omission comment and flag the gap.
- Introduce each code sample with a lead-in sentence: end it with a colon when the sample follows immediately, and with a period when other text intervenes.

## Copyable Example Review Cases

Use these cases to check the distinction when reviewing a draft. They are editorial
checks, not evidence that a model followed the skill or that an example was run.
Only claim execution when the relevant command was actually tested.

| Supplied example and context | Expected decision |
| --- | --- |
| POSIX shell command: `printf '%s\n' ready \| tr a-z A-Z` | Preserve the pipe; it connects two commands and is not a choice marker. |
| JSON body: `{"labels":["docs"],"message":"Waiting..."}` | Preserve the braces, brackets, and dots; they are data syntax and string content. |
| POSIX shell command: `[ -n "${HOME}" ]` | Preserve test brackets, variable expansion, and quoting. |
| Declared synopsis: `acme list [--verbose] {--json\|--yaml} <file>...` | Keep it labeled as syntax. Give a separate sourced invocation for copying; do not guess an option or filename. |
| Two input commands prefixed with `$ ` | Remove only the prompt prefixes in the copyable version; preserve commands and line boundaries. Label a retained prompt-bearing version as a transcript. |
| A command containing `<project-id>` | Define the placeholder and require replacement before execution. Do not claim it runs unchanged or invent a real project identifier. |
| A sample containing an omitted-code comment | Keep it labeled as abbreviated; do not fabricate the missing code or present it as complete. |

### Line-Wrapping Review Cases

Apply the same editorial-check limitation above; these cases do not establish execution or model behavior.

| Supplied example and context | Expected decision |
| --- | --- |
| A long JSON string contains a URL | Preserve the complete value; wrap only at valid structural boundaries after checking equivalence, or leave the line long. |
| A long quoted string or indentation-sensitive code sample | Follow the actual language and preserve semantics; a width target does not authorize arbitrary newlines or re-indentation. |
| A command labeled only `Windows` | Keep it intact and flag the missing shell rather than inserting carets. |
| A PowerShell command runs on Windows or Linux | Apply verified PowerShell syntax, not cmd.exe caret or Bash backslash continuation. |
| A Bash command runs on Windows | Apply verified Bash syntax rather than choosing caret from the operating system. |
| A sample already has valid multi-line syntax, or equivalence cannot be verified | Keep valid existing breaks; leave unverified long lines intact and make the gap visible. |

## Review Checklist

- The reference has a clear retrieval order.
- Entries use repeated headings and fields.
- Entry headings are static nouns or item names, not gerund task headings.
- Dense factual data is in tables or lists.
- Terms are consistent, and acronyms or aliases are defined.
- Tables and lists are parallel enough for quick comparison.
- Units and literal values are formatted consistently.
- Syntax distinguishes required and optional elements, and copyable blocks contain no unresolved synopsis notation and preserve executable syntax.
- Method, endpoint, and command descriptions open with a third-person present verb, not an imperative.
- Byte units match the technology's actual system, ranges repeat the unit and join endpoints with `to`, and version ranges preserve the source's complete constraints, including inclusive or exclusive endpoints.
- Doc-comment entries cover every public element or mark it `Not specified`.
- Defaults, valid values, units, restrictions, and error behavior are present.
- Headers, fields, retry signals, and related response metadata are defined when mentioned.
- Source gaps are marked and do not look like complete facts.
- Line wrapping preserves the actual language or shell semantics and literal values; unverified wrapping is left unchanged with a gap noted.
- Examples are copyable and match the documented syntax; complex examples use numbered annotations.
- Long task steps and conceptual background are split out or linked.

## Attribution

Parts of this reference are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified.
