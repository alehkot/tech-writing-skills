---
name: accessibility-inclusion-editor
description: >-
  Accessibility and inclusive-language review layer for documentation: alt text, text alternatives for
  media, independence from color, size, and position cues, screen-reader-safe wording, singular they and
  gender-neutral wording, replacement of ableist, violent, or charged terms (blacklist/whitelist,
  master/slave, sanity check), respectful disability language, and globally diverse example names and
  personas. Use when the user asks for an accessibility review or audit of docs, an inclusive-language or
  bias check, alt-text writing, or replacement of non-inclusive terms, including how prose should name a
  banned term that is a literal flag or keyword. Apply over an existing draft. Do not use it to write new
  docs, to audit application UI code or WCAG compliance, or to rename identifiers in code or config:
  literals stay exactly as written. Link text, headings, tables, punctuation, and casing stay with
  docs-style-editor. When Simplified Technical English is requested, the STE skill's rules win.
metadata:
  version: "1.0.0"
  risk_tier: low
---

# Accessibility and Inclusion Editor

## Overview

Review documentation so its information reaches every reader: readers who use screen readers, readers who cannot perceive color or spatial layout, readers of translations, and readers whom careless terminology would push away. Fix wording and structure; never change the technical meaning, and never rewrite literal identifiers.

Treat this skill as a review layer, not a document type. Use the task, concept, reference, or report skill for the information architecture, then run this pass over the resulting draft.

Read [references/inclusive-terms.md](references/inclusive-terms.md) before scanning or replacing terminology, and [references/accessibility-checklist.md](references/accessibility-checklist.md) before checking alt text, media, visual cues, and prose structure.

When the write-simplified-technical-english skill is also active, its stricter controlled-language rules take precedence. For example, STE prose avoids pronouns entirely, so the singular-they rule applies only to non-STE text; where the two skills overlap, apply the STE rule and note the scope in the review output.

## Workflow

1. Confirm the operation: review an existing draft for accessibility and inclusive language, or apply the same checks while producing a requested revision. Record the draft's output format; the HTML appendix in the checklist applies only when the output format is HTML.
2. Establish the evidence boundary. List the exact literals in the draft — commands, flags, keywords, branch names, field names, UI labels, and quoted strings — plus every supplied statement about what an image, audio track, or video shows. Do not add or infer content beyond this boundary.
3. Scan terms. Run the draft against every replacement family in [references/inclusive-terms.md](references/inclusive-terms.md): gendered language, ableist terms, violent and figurative terms, socially charged terms, disability language, older adults, and example names and personas. Record each hit with its location and family.
4. Classify each hit before replacing it. If the term is a literal identifier, apply the code-literal exception: keep the literal exactly as-is in code font, use the preferred term in the surrounding prose, and flag the literal for maintainers. Otherwise replace the term with the precise wording for its intended meaning; prefer rewriting the sentence over a one-for-one swap, and introduce the legacy term once, in parentheses at first use, only when readers need it for recognition or search.
5. Check alt text and media parity against [references/accessibility-checklist.md](references/accessibility-checklist.md): alt text on every informative image, empty alt text only on decorative images, identical alt text on repeated icons, no information carried only by an image, no screenshots of text, code, or terminal output, and captions or transcripts for audio and video. Mark any image description the source does not support as unverified.
6. Check color and position independence: pair every color, size, or position cue with a textual cue, and replace document-position words such as `above` and `below` with `earlier`, `preceding`, or `following`.
7. Check screen-reader-safe prose: confirm the meaning survives with punctuation stripped, give each instruction its own list item, and state abilities positively rather than as double negatives. Run the punctuation and casing checks in the checklist — semicolons, exclamation marks, ampersand-as-`and`, all-caps words, and forced mid-paragraph line breaks — and report each hit against its canonical home in docs-style-editor instead of re-deciding the rule.
8. Run the verification passes in the checklist, and run the audit-pointer checks, reporting each audit-pointer violation against its canonical home skill.
9. Flag unknowns instead of guessing. Put unknown community terminology preferences, image content the source does not describe, and icon controls without an accessible name on the flagged list for human verification; never fabricate a preference, a description, or a name.
10. Deliver the review output.

## Review Output

Use this order for reviews and revisions:

1. The revised draft, or a findings table with location, family, finding, and suggested revision when the user asks for findings only.
2. `Code literals kept as-is`: each flagged literal, where it appears, and the prose alternative suggested for maintainers.
3. `Flagged for human verification`: unknown terminology preferences, unverified image descriptions, and missing accessible names.

Omit an empty list rather than inventing entries for it.

## Completion Criterion

Complete the task only when every replacement-table family has been scanned; every hit is replaced with meaning-precise wording, kept as a flagged code-font literal, or flagged as an unknown; alt text, media parity, color and position independence, and screen-reader-safe prose pass the checklist; the verification passes are recorded; and no literal identifier, technical fact, quantity, or safety statement changed meaning.

## Self-Check

- [ ] Every family in the replacement tables was scanned, and each hit is replaced, kept as a code-font literal, or flagged.
- [ ] Replacements preserve the technical meaning, and sentence rewrites were preferred over coined one-for-one substitute verbs.
- [ ] Each legacy term appears at most once, in parentheses at first use, and only because readers need it for recognition or search.
- [ ] Literal commands, flags, keywords, branch names, and fields are unchanged, in code font, with the preferred term in the surrounding prose and each literal flagged for maintainers.
- [ ] Every informative image has context-tuned alt text within the length budget; decorative images have empty alt text; repeated icons share identical alt text.
- [ ] No information is carried only by an image, color, size, or position; audio and video have captions or transcripts; no screenshot stands in for text, code, or terminal output.
- [ ] Document positions use `earlier`, `preceding`, or `following`, never `above`, `below`, or a layout direction.
- [ ] The prose keeps its meaning with punctuation stripped, each instruction is its own list item, and abilities are stated positively.
- [ ] Punctuation and casing hits — semicolons, exclamation marks, ampersand-as-`and`, all-caps words, forced mid-paragraph line breaks — are reported against docs-style-editor, not re-decided here.
- [ ] Disability language uses the terms communities prefer, never a `normal` or `healthy` contrast class, a judgment framing, or a euphemism; older people are `older adults`.
- [ ] Example people have globally diverse names and default to singular they, and no example rests on a gender binary, a stereotyped persona, or a single country's cultural references.
- [ ] Unknown community preferences, unverified image content, and missing accessible names are on the flagged list, not guessed.
- [ ] Audit-pointer checks ran, and each reported violation names its canonical home (docs-style-editor or task-docs-writer).
- [ ] The HTML appendix was applied only to HTML output.
- [ ] When STE is active, its stricter rules took precedence and none was relaxed.

## Guardrails

- Do not rewrite, rename, or sanitize a literal command, flag, keyword, branch name, field, or quoted string; reproduce it exactly in code font and flag it for maintainers.
- Do not fabricate a community's terminology preference, an image description, or an accessible name; flag unknowns for human verification.
- Do not change the technical meaning, quantities, severity, or evidence status of a sentence while replacing its terms.
- Do not delete a condition, prohibition, hazard, or consequence from safety text while rewording it.
- Do not audit application UI code, test software against WCAG, or claim WCAG conformance for anything; this skill reviews documentation prose and structure.
- Do not apply the HTML appendix to non-HTML output; the rest of the checklist is format-agnostic.
- Do not relax a rule of the write-simplified-technical-english skill when it is active; the stricter STE rule wins.

## Attribution

Parts of this skill are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified. This skill is not affiliated with or endorsed by Google.
