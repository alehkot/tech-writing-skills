---
name: docs-style-editor
description: >-
  Copyediting and style layer for technical documentation prose: punctuation, capitalization, hyphenation,
  grammar and usage, word choice and term rulings, numbers, dates, units, link text, code font, lists,
  tables, timeless wording, and safe fictional example values. Use when the user asks to copyedit,
  proofread, style-check, or apply a style guide to an existing draft, or asks a specific style or usage
  question (serial comma, sentence case, since vs because, login vs log in). Apply after the draft exists:
  it corrects mechanics, never meaning, facts, or structure. Do not use it to write or restructure task,
  concept, reference, proposal, or report content; inclusive terminology, ableist or socially charged term
  replacement, example people and personas, alt text, media alternatives, and color or position cues belong
  to accessibility-inclusion-editor, so report them and name that skill; and do not use it for ASD-STE100
  work, where the STE skill's stricter rules win.
metadata:
  version: "1.0.0"
  risk_tier: low
---

# Docs Style Editor

## Overview

Run a mechanical editing pass over an existing draft: punctuation, grammar and usage, word choice, formatting mechanics, numbers and units, and example values. Change how the text is written; never change what it says.

Treat this skill as an editing layer, not a document type. Use the task, concept, reference, proposal, or report skill for the information architecture, then run this pass over the resulting draft.

Load the reference for each pass you run:

- [references/punctuation.md](references/punctuation.md): commas, colons, semicolons, dashes, hyphens, quotation marks, parentheses, periods, ellipses, slashes, example punctuation.
- [references/grammar-and-usage.md](references/grammar-and-usage.md): articles, person, tense, voice, modal verbs, contractions, pronouns, plurals, possessives, prepositions, sentence and paragraph mechanics, global-audience usage.
- [references/word-choice.md](references/word-choice.md): term-by-term rulings, register rules, timeless wording, abbreviations, spelling policy, product and trademark names.
- [references/formatting-mechanics.md](references/formatting-mechanics.md): capitalization, headings, lists, tables, notices, text and code font, links, figures, footnotes.
- [references/numbers-dates-units.md](references/numbers-dates-units.md): numbers, dates, times, units, mathematical notation, phone-number formatting.
- [references/safe-example-values.md](references/safe-example-values.md): reserved domains, IP ranges, phone range, example names, organizations, project names.

## Precedence

Apply rules in this order, and stop at the first level that answers the question:

1. The project's own documented style conventions, including an existing doc set's established usage. A project rule overrides any default in this skill; report every place where it changed a check result.
2. These house defaults.
3. The house spelling and hyphenation forms in [references/word-choice.md](references/word-choice.md). When those tables do not cover a variant, flag it as an open question and name the dictionary the author should check — Merriam-Webster unless the project's locale or style guide names another authority — instead of settling it from memory.

Three constraints sit above all three levels:

- When the write-simplified-technical-english skill is active, its stricter controlled-language rules win. STE bans contractions and semicolons outright, sets hard sentence limits, and replaces actor-plus-modal constructions with imperatives; apply the STE rule and note the scope in the report.
- When the draft documents a standard that defines keyword semantics, such as RFC 2119 `MUST`, `SHOULD`, and `MAY`, reproduce those keywords exactly. Modal rulings do not apply to them.
- When a rule's canonical home is another skill, report the defect and name that skill instead of restating or re-deciding its rules.

Apply a deliberate deviation from any default consistently across the whole document, and record it once in the report.

## Workflow

1. Confirm the operation: a full copyedit pass, a targeted pass over one category, or an answer to a specific style question. Edit mechanics only; do not add, remove, reorder, or reframe content.
2. Record the precedence inputs: the project's style guide, the doc set's established conventions (heading case, placeholder form, spelling locale, byte units, date format), and the dictionary the project names as its tie-breaker for spelling variants. When the draft's own usage is internally inconsistent and no project rule exists, pick the form that appears most often, apply it everywhere, and report the choice.
3. Establish the evidence boundary. List every exact literal in the draft: commands, flags, paths, filenames, environment variables, identifiers, UI labels, error strings, code output, quoted text, versions, quantities, and severities. These are unchangeable. Style rules apply to the prose around them.
4. Run the passes in this order, one category at a time, and record each hit with its location: punctuation; grammar and usage; word choice; formatting mechanics; numbers, dates, and units; example values.
5. Classify each hit before touching it. Change it only when the fix is mechanical and the meaning, facts, and emphasis survive intact. Flag it instead when the fix could change meaning, when the correct wording depends on a fact the source does not state, or when a value may be real rather than illustrative.
6. Apply the code-literal exception to every rule. When a banned or disfavored term is a literal command, flag, keyword, field, or label, keep the literal exactly as-is in code font, use the preferred term in the surrounding prose, and flag the literal for maintainers.
7. Report, rather than re-decide, defects whose canonical home is another skill: inclusive terminology, alt text, media alternatives, and color or position cues belong to accessibility-inclusion-editor; UI interaction verbs, placeholder conventions, and required-information-in-notes belong to task-docs-writer; reference-entry heading style, code-element grammar, byte systems, and version-range wording belong to reference-docs-writer; anthropomorphism and excessive claims belong to technical-content-clarifier.
8. Verify that no meaning drifted. Compare the revision against the source for actors, order, conditions, quantities, units, negation, severity, uncertainty, and literals. Restore anything that changed.
9. Deliver the edit report.

## Edit Report

Use this order, and omit a section that has no entries rather than inventing entries for it:

1. The revised draft, or a findings table alone when the user asks for findings only.
2. `Changes applied`: a table with the location, the change, and the rule that required it.
3. `Flagged, not changed`: the passage or value, why it was not edited (possible real value, meaning at risk, missing source fact), and the question the author must answer.
4. `Project style overrides`: each house default that the project's documented style replaced, and the rule that replaced it.
5. `Canonical home elsewhere`: defects reported for another skill, each with the skill named.

## Completion Criterion

Complete the task only when every requested pass has run against its reference; each hit is corrected, flagged with a question, or reported against its canonical home; the precedence order and any project overrides are recorded; example values are documentation-reserved or flagged as possibly real; and no fact, quantity, unit, severity, condition, structure, or exact literal changed.

## Self-Check

- [ ] The request asks for editing, proofreading, style checking, or a style ruling on existing text, not for new or restructured content.
- [ ] Precedence ran in order: project style, then these defaults, then the house spelling forms, with every override recorded and every uncovered variant flagged instead of settled from memory.
- [ ] Each requested pass ran against its reference file, and each hit is listed with its location and rule.
- [ ] Exact literals are unchanged: commands, flags, paths, filenames, identifiers, UI labels, error strings, code output, quoted text, versions, and quantities.
- [ ] Banned terms that are literal identifiers stayed in code font, with the preferred term used only in surrounding prose.
- [ ] Headings, list items, table headers, and captions use sentence case, and no heading ends with a period.
- [ ] Changes are mechanical: no fact, condition, actor, number, unit, severity, hedge, or caveat was added, deleted, or reweighted.
- [ ] Values that may be real rather than illustrative are flagged as questions, never swapped for reserved example values.
- [ ] Time-anchored, ease-claim, and register fillers are gone, except in the exempted time-stamped genres.
- [ ] Defects owned by another skill are reported with that skill named, not re-decided here.
- [ ] When STE is active, its stricter rules took precedence and none was relaxed.
- [ ] The report separates applied changes from flagged questions.

## Guardrails

- Do not change meaning. Rewording is allowed only when the technical claim, its scope, its hedging, and its evidence status stay identical.
- Do not edit inside code blocks, command syntax, sample output, configuration snippets, error strings, or quoted text; correct the prose around them instead.
- Do not substitute a value that may be real. A resolver IP, a product's actual domain, a documented support number, or a real account identifier stays exactly as written and goes on the flagged list as a question.
- Do not invent a fact to satisfy a rule: not a notice severity, not an expansion for an unknown abbreviation, not a version or date to replace a time-anchored word, and not a description of an image the source does not describe.
- Do not restructure the document, merge or split sections, or change the topic type; recommend the owning skill instead.
- Do not delete a condition, prohibition, hazard, consequence, caveat, or limitation while tightening a sentence.
- Do not enforce a house default against a project's documented style, or against an established convention already consistent across the doc set.
- Do not state what a dictionary lists without consulting it. When the house spelling forms do not cover a variant, flag it as an open question, name the dictionary to check, and leave the draft's form in place.
- Do not relax a rule of the write-simplified-technical-english skill when it is active; the stricter STE rule wins.

## Attribution

Parts of this skill are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified. This skill is not affiliated with or endorsed by Google.
