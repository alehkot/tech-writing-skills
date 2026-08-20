# Formatting Mechanics

## Use When

Load this reference for the formatting pass: capitalization, headings, lists, tables, notices, bold and italics, code font, links and cross-references, figures and captions, footnotes, and markup mechanics.

## Scope Notes

- Sentence case is the house rule for produced documentation. A project's documented style or an RFP's mandated headings override it; record the override in the report.
- Rulings that live elsewhere: alt text, media alternatives, and color or position independence in accessibility-inclusion-editor; UI interaction verbs, bold UI labels, and placeholder naming in task-docs-writer; reference-entry patterns in reference-docs-writer.
- Never restyle a literal. Code fences, sample output, syntax notation, and quoted strings keep the source's exact characters.

## Capitalization

- Use sentence case for every title, heading, list item, table header, table cell, caption, and label inside a figure. Capitalize the first word, the first word after a colon in a heading, and proper nouns.
- Never end a heading or a title with a period.
- Do not capitalize a word without a reason, and never rely on capitalization alone to distinguish two meanings of one word.
- Do not write in all caps or camel case except to reproduce an official name, an always-capitalized abbreviation, or literal code.
- Lowercase glossary and index terms unless they are proper nouns, and write glossary definitions in sentence case.
- When a hyphenated compound starts a sentence or heading, capitalize only its first element unless a later element is a proper noun: `Read-only access is granted per project.`
- Restate a heading from your own doc set in sentence case when you cite it; keep the original capitalization of an external work's title.
- Never name a casing style in an instruction, because the name does not translate. Avoid: Enter the ID in camel case. Prefer: Enter the ID with no spaces and a capital letter starting each word after the first, such as `buildStepName`.
- Reproduce product and feature names with their official capitalization (rulings: [word-choice.md](word-choice.md)).

## Headings and Titles

- Make every heading descriptive and unique so readers can navigate between sections and pages.
- Head a task section with a base-form verb and a concept section with a noun phrase that does not start with an `-ing` word (canonical heading grammar: task-docs-writer for tasks, technical-content-clarifier for concepts).
- Prefix a heading that applies only to some readers with `Optional:`.
- Give a page exactly one top-level heading, and never repeat the page title verbatim as a section heading.
- Never skip a heading level; nest each level directly under the level above it.
- Follow every heading with at least one sentence of content before the next heading.
- Keep heading punctuation simple. A heading that needs complex punctuation needs rewriting.
- Use only a commonly known abbreviation in a heading, and expand it in the first paragraph below.
- Do not number headings to show sequence, put a link inside a heading, or use a bare code item as a heading without a descriptive noun.
- Introduce a run of subsections as `the following sections`, not `this section` or `these sections`.

### Reference-Template Exceptions

These exceptions apply only inside reference topics that follow a repeated item pattern. Reference-docs-writer is the canonical owner of reference-entry structure:

- A reference-entry heading can be the bare code item name, such as an endpoint path or a command name.
- Repeated subheadings inside a repeated item pattern are expected; the uniqueness rule does not apply to them.
- A reference item template can use run-in labels such as `Parameters:` in place of full introductory sentences.

## Lists

- Choose the form from the content: numbered when order matters, bulleted when it does not, description list when every item pairs a term with an explanation.
- Never format a single item as a one-entry list; set it off another way.
- Lead into a list with a sentence that stands on its own, never a fragment the items finish. Close that lead-in with a colon when the list comes next, or with a period when something else sits between them.
- Keep items parallel in grammar, structure, and level of detail.
- Capitalize the first word of every item unless the item's casing carries meaning.
- End an item with a period only when it contains a verb or reads as a sentence. Leave bare words, verbless fragments, code-only items, and link-only items unpunctuated, and never mix the two styles in one list.
- When only one item needs an explanatory tail, convert the whole list to a description list so every item carries one.
- In a description list, capitalize the term, use one separator for the whole list, and never use a dash. After a colon the description starts lowercase; after a period it starts uppercase and ends with a period.
- Label nested levels with lowercase letters, then lowercase Roman numerals.
- Use real paragraphs for multi-paragraph list items, never forced line breaks.
- In running prose, separate listed items with serial commas and never trail off with `etc.`; signal a non-exhaustive list in the lead-in with `such as` or `including`.

## Tables

- Choose the structure by item shape: one fact per item is a list, a term plus its definition is a description list, three or more facts per item is a table.
- Turn a one-column table into a list. Never use a table to lay out a page, hold a code sample, or fold a long flat list into columns.
- Do not drop a table into the middle of a numbered procedure; move it before or after the steps.
- Introduce every table with a full sentence stating what it shows, and refer to it as `the following table`. Never split a sentence around a table.
- Mark the first row, and the first column when it labels rows, as true headers. Never signal header status with styling alone, and never merge cells.
- Write column heads in sentence case, short, with no end punctuation.
- Sort rows in a stated logical order, or alphabetically when no natural order exists.
- When a page has several tables, caption each as `Table N. Description` in sentence case and cite it by number with a lowercase `table` mid-sentence, rather than linking to it.
- Split a table that needs multiple header rows or that has grown hard to scan.

## Notices

- Grade a callout by severity, and never inflate or deflate the level: a note carries helpful but skippable information; a caution tells the reader to proceed carefully; a warning flags irreversible harm such as lost data, lost money, or a security exposure. Reserve a success notice for interactive content.
- Draft the content as plain text first, and promote it to a callout only when it genuinely sits outside the flow.
- Never place two callouts back-to-back, and never nest one inside another. Restructure the content instead.
- Never use a note as a wrapper for a cross-reference.
- Never hide required information in a note (canonical content rules: task-docs-writer).
- Never choose a severity the source does not state. Mark the level as missing and flag it.

## Text Formatting

- Use bold only for UI element names and run-in headings, including notice labels. Never bold for emphasis or to introduce a term.
- Use italics only to introduce a term you define at first mention, to mention a word as a word, for sparing emphasis, for full-length work titles, and for mathematical or version variables. Avoid: **backoff** is the wait between retries. Prefer: *backoff* is the wait between retries.
- Underline nothing except links.
- Write `and`, never `&`, in prose, headings, and navigation, unless you are reproducing a UI label that contains an ampersand.
- Convey structure with semantic markup — real headings, list markup, code fences, emphasis elements — never with manual font, size, color, or alignment changes. A bold line is not a heading.
- Left-align body text. Never center, right-align, or justify it, and never force a line break inside a sentence or paragraph.
- Fence multi-line code with a language hint, and keep the doc set's existing format conventions when it already has them.
- Use one placeholder convention across a doc set (canonical placeholder rules: task-docs-writer).

## Code Font

Put these in code font when they appear in prose: attribute names and values, class names, command output, command-line utility names, constants, data types, database column and row names, DNS record types, element and attribute names, enum values, environment variables, filenames, file extensions, paths, directories, HTTP content types, HTTP verbs, HTTP status codes, IP addresses, language keywords, method and function names, namespaces, package names, port numbers, query parameter names and values, role names, strings used in commands, placeholder variables, and any text the reader types.

Keep these in plain font: product, service, and organization names; a domain name referenced as an organization; and a URL the reader visits in a browser, which should appear as descriptive link text instead.

- Never inflect a code element. Do not pluralize it, make it possessive, or use it as a verb; attach an ordinary noun and inflect that noun. Avoid: The agent DELETEs the stale record and reads INT64s. Prefer: The agent sends a `DELETE` request and reads `INT64` values.
- Format a code-formatted value that appears as a UI label in both code font and bold.
- Use code font for a boolean literal referenced as a value, and plain font when describing whether a condition is true.
- When a command shares its name with its product, put the command in code font and the product name in plain font.
- Use code font for an email address that is program input or output; link a contact address in plain font.
- Drop the class prefix when naming a method in prose unless it is needed to disambiguate.
- Call an HTTP code a status code, and put the number and name in code font: an HTTP `404 Not Found` status code. Write a range as `2xx` or as an explicit numeric range in code font.
- Do not wrap code font in quotation marks unless the quotation marks belong to the literal.

## Links and Cross-References

- Write link text that a reader can judge with no surrounding context: the destination's title or a short description with the informative words first.
- Never use `click here`, `this page`, `this document`, `read more`, or a bare URL as link text.
- Never use one phrase as the link text for two destinations in the same document, and never link one phrase to two destinations.
- Link a term together with its parenthesized acronym as one unit, and link a code element together with its descriptor noun, such as the `--max-retries` flag.
- Introduce a standalone cross-reference with `For more information about X, see Y`. Use `about`, never `on`, and `see` for links.
- Prefer a sentence of in-page context — a definition, a short explanation, two steps — over sending the reader away. When you do link, pick the single most relevant destination and drop redundant links.
- Link a destination once per page, unless the page is long or has independent entry points.
- Disclose surprising link behavior in the link text: a file download and its type, an email link, a same-page jump, an off-site destination, and a target that opens in a new tab.
- Never force a link to open in a new tab. If a platform requires it, append `(opens in a new tab)` to the link text.
- Add the destination page's name when a section title alone would be ambiguous, and use HTTPS wherever the destination supports it.
- Never add a link in place of a missing fact. State the fact or flag it as unknown.

## Figures and Images

Alt text, media alternatives, and screenshots of text are canonical in accessibility-inclusion-editor. The mechanics below stay here:

- Add an image only when it shows something prose cannot, and state in body text everything the image conveys.
- Introduce an image with a full sentence ending in a colon, except a screenshot that directly follows the UI step it illustrates.
- Caption a figure as `Figure N. Description.` — a complete sentence with end punctuation — and cite it by number with a lowercase `figure` mid-sentence. Never point at an image spatially.
- Crop a screenshot to the relevant control or region, and keep operating system and window styling consistent across a doc set.
- Remove personal data from a screenshot with a fully opaque block, never with blur or pixelation, which can be reversed.
- Prefer SVG for diagrams and PNG otherwise, avoid transparent backgrounds, and use MP4 rather than an animated GIF for motion.
- Keep text inside a figure terse and in sentence case, expand no abbreviations there, use numbered callouts only as pointers, and repeat the information in accessible body text.
- Replace an image map with a plain list of the references after the image.
- Give image files descriptive names.
- If the source does not say what a figure shows, mark the description as unverified rather than narrating plausible content.

## Footnotes

- Avoid footnotes. Move the content into a cross-reference, an inline note, or a parenthetical.
- When a footnote is unavoidable, such as a caveat on a benchmark table, mark it with a superscript number and place the note directly after the table.
- Never drop the caveat itself to avoid the footnote; a caveat is load-bearing evidence.

## Attribution

Parts of this reference are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified.
