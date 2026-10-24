# Punctuation

## Contents

- [Use When](#use-when)
- [Scope Notes](#scope-notes)
- [Commas](#commas)
- [Colons](#colons)
- [Semicolons](#semicolons)
- [Dashes](#dashes)
- [Hyphens](#hyphens)
- [Quotation Marks](#quotation-marks)
- [Parentheses](#parentheses)
- [Periods and Other End Punctuation](#periods-and-other-end-punctuation)
- [Ellipses](#ellipses)
- [Slashes](#slashes)
- [Slash Connective Review Cases](#slash-connective-review-cases)
- [Punctuating Examples](#punctuating-examples)
- [Attribution](#attribution)


## Use When

Load this reference for the punctuation pass: commas, colons, semicolons, dashes, hyphens, quotation marks, parentheses, end punctuation, ellipses, slashes, and the punctuation around examples.

## Scope Notes

- Punctuate the prose, never the literals inside it. Reproduce commands, syntax notation, sample output, error strings, and quoted identifiers exactly, including their punctuation.
- When the write-simplified-technical-english skill is active, its stricter rules win: STE bans semicolons outright and forbids contractions, so the allowances below do not apply to STE output.

## Commas

- Put a serial comma before the final conjunction in every series of three or more. Avoid: `Retries, backoff and jitter reduce load.` Prefer: `Retries, backoff, and jitter reduce load.`
- Follow every introductory word or phrase with a comma: `After the migration finishes, restart the workers.`
- Put a comma before `and`, `but`, `or`, `nor`, `for`, `so`, or `yet` when it joins two clauses that could each stand alone. Drop it only when both clauses are very short: `Save the file and close the editor.`
- Do not put a comma before a conjunction when the second part cannot stand alone, unless the sentence misreads without one.
- Use `that` with no comma for a restrictive clause and `, which` for a nonrestrictive one. Avoid: `The queue which fills first blocks the pipeline.` Prefer: `The queue that fills first blocks the pipeline.`
- Put a period or a semicolon before a conjunctive adverb such as `however`, `therefore`, or `otherwise`, and a comma after it.
- Do not put a comma before `because` unless the clause it introduces is nonessential.
- Separate items of an in-paragraph list with commas, including the serial comma.

## Colons

- Introduce a list, a table, or an example with text that reads as a complete sentence on its own. Avoid: `The supported formats are:` Prefer: `The importer accepts the following formats:`
- Lowercase the first word after a mid-sentence colon unless it starts a proper noun, a complete quoted sentence, or a heading, or unless it follows a notice label.
- Use a colon only when what follows expands or specifies what precedes it.
- Use a colon, not a dash, between a term and its definition, and use a colon after a run-in list label.

## Semicolons

- Prefer a period. Two short sentences read faster than one joined sentence.
- Keep a semicolon only to join two tightly coupled independent clauses, to precede a connective such as `therefore` or `that is`, or to separate series items that carry their own commas.

## Dashes

- Use an unspaced em dash for an abrupt break: `The job restarts once—twice at most—before it fails.`
- Do not substitute a hyphen, a double hyphen, or a spaced en dash for an em dash.
- Do not use en dashes at all. Write a range with a hyphen or with `to`.
- Never separate a term from its definition with a spaced dash. Avoid: `Backoff - the wait between retries.` Prefer: `Backoff: the wait between retries.` Format a run of such pairs as a description list.

## Hyphens

Resolve an unlisted compound in this order: the doc set's established form, then the word-choice rulings, then the named dictionary. Keep one form per term across the document.

- Hyphenate a two-word modifier before a noun when the pairing could misread: `a read-heavy workload`, `an event-driven pipeline`.
- Leave the same words open after a verb: `the workload is read heavy`. Exceptions stay hyphenated everywhere: `cloud-based`, `user-friendly`, `on-premises`, `customer-facing`, `read-only`.
- Do not hyphenate an adverb ending in `-ly`: `a publicly reachable endpoint`.
- Do not hyphenate a conventionally open compound: `a machine learning model`.
- Do not hyphenate a prefix onto its base: `metadata`, `preprocessing`, `pseudocode`. Hyphenate after `self-` and `cross-`, before a capitalized word or a number (`non-UTF8`, `post-2019`), before a term that already contains a hyphen or a space, and where the closed form misreads (`re-create`, `de-escalate`).
- Hyphenate a number joined to a spelled-out unit before a noun: `a 64-bit build`, `a five-minute timeout`. With an abbreviated unit, use a space instead: `a 200 GB volume`.
- Avoid modifiers of three or more words. Avoid: `a 2024-edition-specific test case.` Prefer: `a test case specific to the 2024 edition.`
- Write ranges as `4-8 replicas` or `from 4 to 8 replicas`. Never mix the two, and never use an en dash.
- Leave no space beside a hyphen, except after a suspended hyphen: `one- or two-hour windows`.

## Quotation Marks

- Prefer the straight forms of the quotation mark and the apostrophe, and convert any curly ones you find.
- Put commas and periods inside the closing quotation mark in ordinary prose.
- When the quoted text is a string the reader must type or match exactly, keep every other punctuation mark outside the quotes, and prefer code font over quotation marks. Avoid: Type "retry-after," in the header field. Prefer: Type `retry-after` in the header field.
- Do not wrap code-font text in quotation marks unless the quotation marks belong to the literal.
- Reserve single quotation marks for code that uses them and for a quote nested inside a quote.
- Quote the title of a short work, such as an article or an episode, unless the title is a link. Keep quotation marks and end punctuation outside link text.
- Quote a metaphorical term only at first use, and only when it is not established vocabulary in the domain.

## Parentheses

- Do not put information the reader must act on inside parentheses; some readers skip parenthetical text.
- Replace parentheses with commas, an em dash, or a second sentence when either reads as well, and keep any remaining parenthetical short.
- Put the period inside the parentheses only when they enclose a complete standalone sentence; otherwise put it after the closing parenthesis.

## Periods and Other End Punctuation

- End every complete sentence with a period, and leave one space between sentences.
- Never end a heading, a title, or a table column head with a period.
- Keep a URL or a file path out of sentence-final position; move it to its own line, or drop the period that would follow it.
- Write acronyms and initialisms without internal periods. Put a period after a truncated word, but not after a unit, a date or time abbreviation, or a country or state abbreviation.
- Use a period as the decimal mark.
- Do not use exclamation marks in reference or concept material, and end procedural outcomes with a period. Reproduce an exclamation mark exactly when it belongs to code syntax, an error string, or another literal.

## Ellipses

- Do not use ellipses in prose. State the information or cut it, and never use them for hesitation.
- Drop a trailing ellipsis from a UI label when you document the control: for the label `Export...`, write `click Export`, unless dropping it makes the control ambiguous.
- Allow an ellipsis only inside a quotation to mark omitted material, never at the start or end of the quote. Build it from three periods with a space on each side, and use four when the omission crosses a sentence boundary.
- Reproduce an ellipsis that is part of command syntax or sample output exactly as the source shows it.

## Slashes

- Replace a prose slash used as a connective only after the supplied context establishes the relationship: `and` when the source means both, `or` for alternatives, or `X, Y, or both` when either or both are allowed. Preserve any explicit exactly-one restriction, negation, and actor. Do not infer the relationship from the slash itself.
- For `authored/reviewed by the on-call engineer`, use `authored and reviewed` only if the source establishes both, and `authored or reviewed` only if the source permits alternatives. With no such context, retain the wording and flag which relationship the author intends instead of choosing one.
- Avoid `and/or` outside a space-constrained table, but preserve its inclusive meaning when expanding it. Do not turn permission to do either or both into a requirement to do both or an exactly-one choice.
- Use forward slashes in paths and URLs, and backslashes only in Windows-specific paths. Do not mix slash directions for one platform.
- Break an overlong URL immediately after a slash, and never insert a hyphen into it.
- Do not write fractions or dates with slashes.
- Spell out slash abbreviations such as `w/` and `c/o`.

## Slash Connective Review Cases

These original cases check source-preserving editorial decisions, not measured model performance. Apply the literal and project-style exceptions before replacing punctuation.

| Supplied context and passage | Acceptable editorial decision | Meaning drift to reject |
| --- | --- | --- |
| `The release note must be authored/reviewed by the on-call engineer.` No other context is supplied. | Retain and flag whether both duties or alternatives are intended. | Choosing `and` or `or` without evidence. |
| The source requires the on-call engineer to do both duties: `The release note must be authored/reviewed by the on-call engineer.` | `The release note must be authored and reviewed by the on-call engineer.` | Letting either duty satisfy the requirement, or assigning review to a different actor. |
| The source says either duty satisfies the requirement but says nothing about doing both: `The release note must be authored/reviewed by the on-call engineer.` | `The release note must be authored or reviewed by the on-call engineer.` | Requiring both duties or inventing a prohibition on doing both. |
| The source permits exactly one export format per request: `Export CSV/JSON.` | `Export either CSV or JSON, but not both.` | Allowing both formats in one request or requiring both. |
| The source permits either or both inputs: `You can import logs/metrics.` | `You can import logs, metrics, or both.` | Requiring both inputs or prohibiting their combination. |
| The source prohibits deletion and separately prohibits archiving: `Do not delete/archive the records.` | `Do not delete or archive the records.` | `Do not delete and archive the records`, which can prohibit only the combination. |
| The prose says `You can export raw and/or processed events.` | `You can export raw events, processed events, or both.` | Turning the permission into an instruction to export both. |
| A UI label is `Read/Write`, a command contains `/var/log`, an established technical term is `TCP/IP`, or a quoted string includes `and/or`. | Preserve the exact literal; edit surrounding prose only. | Applying connective expansion inside the label, path, technical term, or quotation. |

Basis: [Google's slash guidance](https://developers.google.com/style/slashes) presents both conjunction and disjunction as possible rewrites of one ambiguous slash construction; [Microsoft's slash guidance](https://learn.microsoft.com/en-us/style-guide/punctuation/slashes) also distinguishes combinations and literal technical uses. The cases apply this skill's existing source-fidelity constraint: a style preference cannot establish the missing relationship.

## Punctuating Examples

- Introduce an example with `such as`, `like`, or `for example`, and put a comma after `for example`.
- Set a trailing example off with a comma, parentheses, or an em dash, never with a semicolon before `for example`.
- Keep an embedded example short: `Enter a six-character build tag (for example, r24b07), and then submit the job.`
- Move a longer example into its own sentence that starts `For example,`.

## Attribution

Parts of this reference are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified.
