# Unslop Guide for Technical Writing

Remove words and patterns that make readers work without adding meaning. Make the existing technical point easier to find and understand. Judge observable writing defects; do not infer who or what wrote the text.

## Preserve the Meaning First

Before editing, identify the passage's actors, actions, conditions, quantities, uncertainty, and exact literals. Keep those facts intact. Apply project style and STE precedence from `SKILL.md`.

Choose one disposition for each finding:

| Disposition | Test | Action |
| --- | --- | --- |
| Edit | The source establishes the meaning, and the change affects only its expression. | Make the smallest useful change. |
| Flag | A clearer claim needs a missing fact, source, measurement, or technical decision. | Keep the claim's evidence status visible and ask for the missing information in the edit report. |
| Keep | The wording conveys a real distinction, precise term, necessary qualification, or useful navigation. | Leave it intact, even if the same words sometimes appear in poor writing. |

## Common Patterns and Safe Revisions

Treat these as diagnostic examples, not automatic search-and-replace rules. Preserve real distinctions and follow the source when context changes the meaning.

| Pattern | Draft | Safe treatment |
| --- | --- | --- |
| Conversational residue | `Happy to explain! Here is the answer you need.` | Remove the chat framing from the document. Keep any actual next action or contact information. |
| Empty lead-in | `It is worth pointing out that the build reads a manifest.` | `The build reads a manifest.` |
| Inflated expression | `The worker utilizes the cached result.` | `The worker uses the cached result.` |
| Indirect predicate | `The manifest serves as the build input.` | `The manifest is the build input.` Keep a role distinction if the longer wording conveys one. |
| Ornamental contrast | `The scheduler not only queues jobs but also records failures.` | `The scheduler queues jobs and records failures.` Keep a real contrast such as `The scheduler logs job IDs, not payloads`. |
| Artificial range | `The guide covers everything from field names to retry delays.` | `The guide covers field names and retry delays` if those are the supplied topics. Preserve actual numerical, temporal, or ordered ranges. |
| Repeated list label | `**Retention:** Retention lasts seven days.` | Use the value alone: `**Retention:** seven days`. Keep useful labels, facts, item order, and parallel formatting. Rewrite the phrase so it remains grammatical; do not merely delete its subject. See [formatting-mechanics.md](formatting-mechanics.md). |
| Repeated uncertainty | `The change might possibly reduce memory use.` | `The change might reduce memory use` if both words express the same uncertainty. Keep independent qualifiers such as `in this sample` and `under low load`. |
| Decorative labels and synonym cycling | One named check becomes a `gate`, a `barrier`, and a `sentinel` in successive sentences. | Use its established name consistently. Keep distinct names when they refer to distinct things. |
| Unmeasured benefit | `The cache dramatically improves performance.` | Flag the missing measure, scope, and evidence. Do not invent a percentage or silently change it to an unconditional speed claim. |
| Unnamed authority | `Researchers agree that this is the best approach.` | Flag the missing source and comparison basis. Do not fabricate a citation or silently delete a substantive claim. |
| Overcompressed prose | `If token expires, client disconnects; no retry.` | `If the token expires, the client disconnects and does not retry` when that relationship is established. Preserve code and diagram notation; see [grammar-and-usage.md](grammar-and-usage.md). |

## Avoid Cleanup That Damages the Document

- Keep precise technical terms, including `vector`, `primitive`, and `test harness`, when they carry their domain meaning. Preserve commands, symbols, UI labels, quoted text, and output strings exactly.
- Keep warranted uncertainty, prohibitions, exclusions, and conditions. Removing `might`, `only`, or `not` can change a technical claim. Do not turn a limited observation into a general guarantee.
- Keep standard warnings, prerequisites, and useful boilerplate. Reuse across projects does not make a sentence empty.
- Keep the natural number of facts or list items. Do not add a third item for rhythm or remove a real item to avoid a three-item list.
- Keep readable sentence variety. Split a sentence when its structure obscures the relationships; do not chop it into fragments to meet an arbitrary rhythm. STE sentence limits still apply when STE is active.
- Follow the documented punctuation and formatting rules. An em dash, a colon, a bold label, or a heading is not by itself a defect. See [punctuation.md](punctuation.md) and [formatting-mechanics.md](formatting-mechanics.md).
- Flag structural or factual repairs for the owning skill. Resolving a vague benefit belongs to technical-content-clarifier; rebuilding a procedure belongs to task-docs-writer. This pass does not add facts, reorganize sections, or change the document's purpose.

## Run the Pass

1. Read the passage for its technical point before scanning individual words.
2. Check the opening, paragraph transitions, list lead-ins, and ending for empty framing or repetition.
3. Check every applicable pattern in the table and choose edit, flag, or keep. For run-in list labels, read each label and description together: remove repeated wording and rewrite the description as a grammatical value, phrase, or sentence. Use established facts to clarify wording; flag anything that requires new evidence.
4. Compare the revision with the source for actors, conditions, negation, quantities, scope, uncertainty, literals, and structure. Restore any changed meaning.
5. Return the revised text with the skill's edit report. Separate applied edits from questions and referrals; keep the report free of the same filler you removed.

## Source Note

Comparison with Cursor's [pstack unslop skill](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md) informed this guide. The procedures and examples are written for this repository and preserve its distinction between mechanical editing and factual or structural revision.
