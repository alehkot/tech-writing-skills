# Accessibility Checklist

## Use When

Load this reference before checking alt text, media alternatives, visual-cue independence, or screen-reader-safe prose during an accessibility and inclusion review.

## Alt Text Rules

- Give every informative image alt text: a noun phrase or a full sentence, roughly 155 characters or fewer, with end punctuation so screen readers pause after it.
- Tune alt text to the image's role in the surrounding context, not only to its content. A chart cited for one trend gets alt text about that trend, not an inventory of every series.
- Never start alt text with `Image of`, `Picture of`, or a similar frame, and never write alt text in all caps.
- Give purely decorative or fully text-redundant images empty alt text so assistive technology skips them.
- Reuse identical alt text for repeated icons and indicators; do not vary the wording between occurrences of the same symbol.
- Move explanations longer than the alt-text budget into body text as a figure description. A caption never substitutes for alt text.
- If the source does not say what an image shows, mark the description as unverified instead of narrating plausible content.

Avoid: `IMAGE OF THE DASHBOARD` Prefer: `Dashboard with the ingest queue paused and two workers idle.`

## Information Parity

- Put nothing only in an image: state in body text everything the image conveys, so the image is never the sole carrier of information.
- Never present text, code, configuration, or terminal output as a screenshot; present it as real, selectable, copyable text.
- Provide captions or transcripts for every audio and video asset, and keep them translatable.
- Never use flashing or flickering content, and never rely on an animation as the only way to convey information.

## Color and Position Independence

- Never rely on color, size, shape, or position as the sole channel for state or meaning; pair every visual cue with a textual one.
- Name the state, not only its rendering. Avoid: `Retry the steps shown in red.` Prefer: `Retry the steps marked Failed, which appear in red.`
- Point within a document with `earlier`, `preceding`, `following`, or a named section — never `above`, `below`, or `the right-hand side` (canonical rules: docs-style-editor word-choice). Avoid: `Use the table above.` Prefer: `Use the preceding table.` or `Use the table in the section named Limits.`
- Do not describe UI locations directionally; refer to controls by their visible label or accessible name (canonical rules: task-docs-writer).

## Screen-Reader-Safe Prose

When the write-simplified-technical-english skill is also active, its stricter sentence and structure rules take precedence over these checks.

- The meaning must survive with all punctuation stripped; read each sentence without punctuation as a check.
- Give each instruction its own list item; never chain steps inside one paragraph.
- State abilities positively, and avoid double negatives and exceptions to exceptions (canonical rules: docs-style-editor grammar-and-usage).

Run the following punctuation and casing checks as well, but report each hit against its canonical home instead of re-deciding the rule:

- A semicolon that pushes two clauses into one long spoken sentence. Prefer a period, and keep a semicolon only where docs-style-editor allows one (canonical home docs-style-editor punctuation).
- An exclamation mark in technical prose (canonical home docs-style-editor word-choice).
- An `&` written for `and` in prose or headings; an ampersand is acceptable only when it mirrors a UI label or sits in a space-constrained table (canonical home docs-style-editor formatting-mechanics).
- An all-caps word or an invented camel-case coinage, which a screen reader may spell out letter by letter; reproduce literal identifiers exactly regardless (canonical home docs-style-editor formatting-mechanics).
- A forced line break inside a sentence or paragraph; start a new paragraph or list item instead (canonical home docs-style-editor formatting-mechanics).

## Verification Passes

Run every pass and record each one as complete or not applicable:

- No-image pass: with images ignored, all information is still present in text.
- No-color pass: with color ignored, every state and cue is still distinguishable.
- No-sound pass: with audio muted, captions or transcripts carry the full content.
- Keyboard-only pass: every documented interaction is described in a way a keyboard-only reader can follow, or the gap is flagged.
- No-punctuation pass: sentences keep their meaning with punctuation stripped.

## Audit Pointers

Run these checks during the review, but report violations against their canonical home, where the full rules live:

- Descriptive link text that makes sense out of context, and disclosure of unexpected link behavior: canonical home docs-style-editor.
- Heading hierarchy without skipped levels, and unique, descriptive, non-empty headings: canonical home docs-style-editor.
- Referring to UI elements by their visible label or accessible name, and flagging icon controls that have neither: canonical home task-docs-writer.
- Introducing each table in the preceding text, and never merging table cells: canonical home docs-style-editor.
- The punctuation and casing checks listed under Screen-Reader-Safe Prose: canonical home docs-style-editor.

## HTML Outputs Appendix

Apply this section only when the deliverable's output format is HTML. Skip it for Markdown, plain text, and any other format; the rest of this checklist is format-agnostic.

- Use each element for its semantic purpose: real heading elements for headings, never styled text as a fake heading and never a heading element chosen for its visual size.
- Use `em` only for genuine emphasis and `strong` only for strong importance; use `i` and `b` for italics and bold that carry no emphasis semantics.
- Do not use `br` to fake paragraph spacing; `br` is only for breaks that are part of the content, and spacing belongs to CSS.
- Prefer native interactive elements, and keep the DOM order matching the reading order.
- Give every form input a `label` element.
- Mark table headers with `th` only in the first row or column; add `scope` or `headers` attributes when the header structure is complex.
- Add an `aria-label` to menu-path separators written with `>` so screen readers announce the separator as `and then`.

## Attribution

Parts of this reference are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified.
