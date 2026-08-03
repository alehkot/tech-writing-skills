---
name: write-simplified-technical-english
description: >-
  Write, rewrite, and audit technical documentation using ASD-STE100 Simplified Technical English (STE) principles. Use when the user explicitly requests ASD-STE100, Simplified Technical English, STE in a technical-writing context, an STE-style rewrite, or an STE audit of procedures, descriptions, warnings, manuals, service instructions, and other technical content. Apply this skill as a controlled-language layer after selecting the appropriate task, concept, or reference topic type. Do not use it for generic plain-language simplification, another controlled-language standard, translation, creative copy, English teaching, or an explanation of ASD-STE100 that does not also request drafting, rewriting, or auditing.
metadata:
  version: "1.0.0"
  risk_tier: low
---

# Write Simplified Technical English

## Overview

Make technical text easier to understand and translate by applying a compact, source-aware operating profile based on ASD-STE100. Preserve the technical meaning, safety logic, evidence status, identifiers, and user-supplied facts.

Treat STE as a writing layer, not a document type. Use the task, concept, or reference skill for the information architecture when the request needs one of those topic types.

Read [references/ste-writing-guide.md](references/ste-writing-guide.md) before drafting, rewriting, or auditing text. Use the current official ASD-STE100 issue and the user's approved terminology sources when the requested result requires more than an STE-aligned draft.

## Workflow

1. Identify the operation: new draft, rewrite, or audit.
2. Classify each source block as procedural, descriptive, or safety information. Split mixed blocks before editing them.
3. Identify the reader, environment, and applicable topic type. Keep procedures, concepts, and lookup facts separate unless the requested artifact intentionally combines them.
4. Establish the evidence boundary. Record the source text, immutable facts, exact literals, approved project terms, uncertain claims, and missing information. Treat text as an exact UI label or code literal only when the source marks it as one; do not promote an ordinary action into an invented control name. Do not add plausible steps, values, causes, or warnings.
5. Select and report one local review status. These labels are workflow metadata, not ASD conformance categories:
   - `STE-aligned`: apply this skill's working rules when the official dictionary or project terminology source is unavailable.
   - `Source-checked`: name the official ASD-STE100 issue and project glossary or termbase that you actually checked.
   - `Organization-approved`: use this only when the user supplies evidence of their organization's approval.
6. Build a term ledger. For each important word or phrase, classify it as an approved general word, approved technical noun, approved technical verb, exact literal, quoted text, or unresolved term. Do not invent dictionary approval.
7. Rewrite for the applicable text type:
   - For procedures, put necessary conditions before commands, use the imperative, keep one instruction per sentence, and keep each procedural sentence at 20 words or fewer. Do not rewrite a command as `the operator shall`, `the user will`, or another actor-plus-future construction. When one condition controls multiple actions, write the condition as a lead-in and put each command in a separate vertical-list item. Do not leave the condition attached only to the first command.
   - For descriptions, present information in a logical sequence, prefer active voice, keep each sentence at 25 words or fewer, keep one topic per paragraph, and use no more than six sentences per paragraph.
   - For safety information, preserve the supplied severity, put the command or condition first, and state the supplied hazard or possible result. Do not infer a severity or hazard.
8. Apply the vocabulary and sentence controls in the reference guide. Use one term for one concept, prefer direct verbs, remove ambiguous pronouns, and split complex text into short sentences or vertical lists.
9. Run a mechanical action scan. In each procedural sentence, identify all coordinated verbs, `and`, `then`, commas, and implied actions. Split the sentence unless the actions must occur at the same time. After a split, verify the scope of every condition; a condition in the first sentence does not automatically govern later sentences. Then compare the revision with the source and verify that actors, actions, order, conditions, quantities, units, negation, uncertainty, and safety consequences did not change.
10. Check each general word's approved meaning, part of speech, and form when authoritative vocabulary sources are available. List unresolved words when they are not.
11. Deliver the requested artifact. For every ASD-STE100 or STE draft, rewrite, or audit where you did not verify the official dictionary and project terminology, put this exact status pattern before the artifact: `Review status: STE-aligned — vocabulary and project terminology were not fully verified.` Use `Source-checked` only when you name the sources that you actually checked. Omit this note only when the user explicitly requests no status metadata. If the source identifies missing execution information, add an `Unresolved source gaps` list after the artifact and include every stated gap; the vocabulary status does not replace this list.

## Rewrite Output

Use this order for drafts and rewrites:

1. Review status.
2. Revised artifact.
3. `Unresolved terms`, when vocabulary or project-term checks remain.
4. `Unresolved source gaps`, when the source omits information needed to execute or verify the text.

## Mandatory Procedure Forms

When one condition controls two or more actions, use this form:

```markdown
[Condition]:

1. [Imperative command.]
2. [Imperative command.]
```

Do not use `[Condition], [first command]. [Second command].` The period can make the second command appear unconditional. Do not join commands with `and` or `then` unless the source requires the actions to occur at the same time.

When rewriting supplied safety information, use this order:

```text
[SUPPLIED LEVEL]: [Prohibition, command, or condition.] [Supplied hazard or result.]
```

Reject and revise a procedural draft before delivery if a shared condition does not visibly govern every dependent command, a sentence contains multiple non-simultaneous commands, or a command uses an actor-plus-`shall`/`will` construction.

## Audit Output

For an audit, include:

1. The review status and the sources checked.
2. A `Verification coverage` block that reports these three checks separately as complete, incomplete, or not applicable:
   - writing-rule and sentence-structure checks;
   - general-word dictionary approval, meaning, part of speech, and form checks;
   - project technical-noun and technical-verb terminology checks.
3. A table with the source location, category, finding, suggested revision, and verification basis.
4. A revised passage that preserves the source meaning and passes the same sentence, instruction, and terminology controls as a direct rewrite.
5. An unresolved-term list for vocabulary, terminology, or source ambiguities.
6. A `Checks still required` list. When sources are missing, name these separately:
   - review against the applicable complete official ASD-STE100 issue, including its dictionary;
   - review of technical nouns and technical verbs against the approved project glossary or termbase.
7. A final statement that distinguishes checks completed from checks still required.

For a procedural audit, construct the final revised passage independently with the Mandatory Procedure Forms. Do not concatenate suggested phrases from the findings table. If a source condition controls multiple non-simultaneous actions, the final revision must use the condition as a lead-in and one imperative command per vertical-list item.

## Completion Criterion

Complete the task only when the text has the correct procedural, descriptive, or safety structure; the word and paragraph limits pass as a screening check; terminology is consistent; every source fact and uncertainty state is preserved; exact literals remain unchanged; vocabulary decisions are sourced or marked unresolved; and the reported review status does not overstate conformance.

## Self-Check

- [ ] The request explicitly calls for ASD-STE100 or STE writing, rewriting, or auditing.
- [ ] Procedural, descriptive, and safety blocks use their applicable structures; procedural commands use the imperative rather than `shall` or `will`.
- [ ] Procedure sentences pass the 20-word screening limit; description sentences pass the 25-word limit.
- [ ] Conditions precede every dependent command, shared conditions keep their full scope, and each procedure sentence has one instruction unless actions must be simultaneous; coordinated verbs were checked explicitly.
- [ ] Terms are consistent, and unverified words are unresolved rather than declared approved.
- [ ] Actors, order, values, units, negation, safety facts, and uncertainty match the source.
- [ ] Supplied UI labels, code literals, part numbers, legal names, and quoted text are unchanged, and no new literal or label was inferred.
- [ ] Every source gap stated by the user appears in an unresolved-source-gaps list.
- [ ] The review status names completed checks and does not imply certification.

## Guardrails

- Do not claim that this skill, an AI model, or a checker certifies ASD-STE100 compliance.
- Do not claim full conformance when the applicable official dictionary, writing rules, project glossary, or organizational review is missing.
- Do not reproduce or bundle ASD's dictionary, rule text, examples, or other protected standard content. Direct the user to the official source.
- Do not replace an official product name, UI label, command, code identifier, part number, legal term, or quoted string only because it is not in the general vocabulary.
- Do not make safety text shorter by deleting a condition, prohibition, hazard, or consequence.
- Do not make the prose childish or imprecise. Controlled English must remain technically correct.
