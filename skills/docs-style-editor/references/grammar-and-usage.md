# Grammar and Usage

## Contents

- [Use When](#use-when)
- [Scope Notes](#scope-notes)
- [Articles](#articles)
- [Person](#person)
- [Tense](#tense)
- [Voice](#voice)
- [Modal Verbs](#modal-verbs)
- [Tense and Modal Review Cases](#tense-and-modal-review-cases)
- [Contractions](#contractions)
- [Pronouns](#pronouns)
- [Plurals](#plurals)
- [Possessives](#possessives)
- [Prepositions](#prepositions)
- [Sentence Mechanics](#sentence-mechanics)
- [Paragraph Mechanics](#paragraph-mechanics)
- [Global-Audience Usage](#global-audience-usage)
- [Limiter Scope Review Cases](#limiter-scope-review-cases)
- [Attribution](#attribution)


## Use When

Load this reference for the grammar pass: articles, person, tense, voice, modal verbs, contractions, pronouns, plurals, possessives, prepositions, sentence and paragraph mechanics, and global-audience usage.

## Scope Notes

- These rulings govern standard documentation prose. When the write-simplified-technical-english skill is active, its stricter rules win: no contractions, an approved-word ledger, imperatives in procedural instructions, verified vocabulary and clear pronoun references, and hard limits of 20 words per procedural sentence and 25 per descriptive sentence.
- When a documented standard defines keyword semantics, such as RFC 2119 `MUST`, `SHOULD`, and `MAY`, reproduce those keywords exactly. The modal rulings below do not override a standard's own vocabulary.

## Articles

- Keep `a`, `an`, and `the` in every sentence, heading, and title. Avoid: `Create service account.` Prefer: `Create a service account.`
- Treat a dropped article as a global-audience defect: translation and non-native comprehension both depend on articles.

## Person

- Address the reader as `you` in every topic type, not only in procedures. Never write `we` or `let's` for an action the reader performs.
- Reserve `user` for the people who use what the reader builds. The reader is always `you`.
- Describe reader actions in second person and system or end-user behavior in third person. In reference prose, state facts about elements in third person and switch to `you` only for reader instructions.
- Use `we`, `our`, and `us` only for the authoring organization, and only after naming the organization so the antecedent is unambiguous.
- Name the intended reader near the start of the document and keep the same `you` throughout.
- STE does not impose a blanket first-person ban. In descriptive text, organizational `we` can identify the authoring organization when the source establishes that actor; do not invent an actor or use `we` for the reader. Apply the STE vocabulary checks and report incomplete verification. See [ASD-STE100 Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf), active-voice Method 4 (page 1-3-8).
- Review cases: With the manufacturer explicitly identified as the speaker, `We supply replacement seals.` is not automatically a first-person defect; check the vocabulary separately. For a reader's procedural step, `We remove the cover.` becomes `Remove the cover.` only when the source confirms the reader performs that action. If the actor is unknown, flag it rather than reassigning the work.
- When imperative sentences accumulate in running text, convert them into a formatted procedure (canonical procedure rules: task-docs-writer).

## Tense

- Describe source-established general system behavior in the present tense. Avoid: `The scheduler will retry the job.` Prefer: `The scheduler retries the job.`
- Use `will` only when the action genuinely happens later than the sentence's frame, such as a scheduled backup or an asynchronous delivery.
- Recast `would` as present-tense cause and effect only when the source establishes general behavior: `If the token expires, the gateway rejects the request.` Preserve the condition. Keep proposals, counterfactuals, time-specific statements, and substantive uncertainty in their original frame; a tense edit must not turn a prediction or proposed change into an established fact.
- Do not narrate unreleased behavior in future tense, and do not describe it at all unless the source states it. Label sourced future behavior as planned.

## Voice

- Make the actor the grammatical subject by default, and rewrite a passive that names its actor with `by`. Avoid: `The manifest is validated by the controller.` Prefer: `The controller validates the manifest.`
- Keep the passive only when the actor is unknown, genuinely irrelevant, or deliberately de-emphasized, or when the object is the point: `The index was rebuilt in March.` `Forty-one conflicts were found.`

## Modal Verbs

For non-STE prose, identify the source-supported meaning before rewording a modal: an action can be required, recommended, or optional; a state or outcome can be actual, expected, or merely possible. Do not infer requiredness, certainty, or an actor from `should` alone. If the source leaves the meaning unclear, keep the wording and flag the specific question for the author.

| Meaning | Write | Avoid |
| --- | --- | --- |
| Required action | `must`, or a bare imperative | `should`, `needs to` |
| Recommended action | `We recommend that you ...` | `should`, except for a widely recognized practice such as least privilege |
| Optional action | `can`, or an `Optional:` prefix | `may`, `might`, `could` |
| Ability or permission | `can` | `is able to`, `is allowed to` |
| Possible outcome | `might` | `may`, `could`, `would` |
| Expected outcome | a declarative statement only for source-established behavior; otherwise preserve the expectation and its qualifications | replacing an unverified prediction with a fact |
| Policy or legal permission | `may` | `can` |

- For an established actual state, use a direct description. For an instruction, identify who must act. The ambiguous sentence `The flag should be true.` does not establish either: use `Set the flag to true.` only when the source requires the reader to set it, and `The installer sets the flag to true.` only when the source confirms that behavior. Otherwise, retain and flag it; do not invent an actor, required action, or troubleshooting step.
- When several approaches exist, recommend one and say why, rather than listing an unranked menu.

## Tense and Modal Review Cases

Use these original cases to check meaning preservation, not as evidence of measured model performance. The source context is part of each case.

| Source context and passage | Acceptable editorial decision | Meaning drift to reject |
| --- | --- | --- |
| The source confirms general gateway behavior: `If the token expires, the gateway would reject the request.` | `If the token expires, the gateway rejects the request.` | Dropping the token-expiry condition. |
| `The export should return 50 rows, but we have not verified it.` | Keep it, or write `The export is expected to return 50 rows, but we have not verified it.` | `The export returns 50 rows.` |
| `The flag should be true.` No other context is supplied. | Keep and flag: is this a required setting, an observed value, or an expected default? | Choosing an actor, stating a value as observed, or issuing a new instruction. |
| The source explicitly describes retrying as a recommendation, not a requirement: `You should retry the request.` | Reword it as a recommendation while preserving that status. | `You must retry the request.` |
| `The proposed cache would reduce repeated database reads.` | Preserve the proposal and its conditional outcome; leave the clear sentence unchanged. | `The cache reduces repeated database reads.` |
| `If the replica had been available, the request would have succeeded.` | Preserve the past counterfactual and the source's confidence; leave it unchanged. | Recasting it as current behavior or weakening it to mere possibility. |
| The document uses RFC-defined `SHOULD` and `MUST`. | Preserve the defined keywords exactly under Scope Notes. | Applying ordinary-prose modal substitutions. |

## Contractions

- Use common two-word contractions in standard prose to keep the register conversational.
- Prefer contracted negatives so a scanning reader cannot drop the negation. Avoid: `The endpoint does not accept query parameters.` Prefer: `The endpoint doesn't accept query parameters.`
- Spell out and emphasize `not` only when the negative itself is the point of the sentence.
- Never coin a nonstandard contraction, attach `'s` meaning `is` to an ordinary noun, or stack a three-word contraction.
- Suspend this rule whenever the STE layer is active; STE prohibits contractions.

## Pronouns

- Give every pronoun a clear antecedent, and repeat the noun when the reference could slip. Avoid: `It stays empty until the sync completes.` Prefer: `The cache stays empty until the sync completes.`
- Follow `this` and `these` with a noun: `Set this value to zero`, not `Set this to zero`.
- Keep optional relative pronouns: `the rules that you defined`, `assumes that you have`.
- Use `that` for restrictive clauses and `which` for nonrestrictive ones; do not swap them.
- Use `who` for people; `whose` may refer to people or things.
- Restrict first-person pronouns to FAQ questions, signed commentary, and the named authoring organization.
- Use singular they for a person of unknown or irrelevant gender (canonical rules: accessibility-inclusion-editor).

## Plurals

- Never form a plural with an apostrophe: `APIs` and `VMs`, not `API's` or `VM's`.
- Add `es` only when the abbreviation ends in `s`, `sh`, `ch`, or `x`: `OSes`.
- Keep a spelled-out term and its abbreviation in the same number: `virtual machines (VMs)`.
- Never write a parenthetical optional plural. Avoid: `Delete the stale file(s).` Prefer: `Delete each stale file.` or `Delete one or more stale files.`
- Use a plural verb after `one or more`, and a singular noun after `more than one`: `more than one replica`.
- Match the verb to the head noun of a long subject: `The number of retries is capped at five.`
- With a compound subject joined by `and`, use a plural verb; with `or`, match the nearer subject.
- Do not pluralize a product, feature, or company trademark, or a unit abbreviation.

## Possessives

- Add `'s` to a singular noun, including one ending in `s`: `the class's quota`. Add a bare apostrophe to a plural noun ending in `s`: `the workers' queues`.
- Rewrite an awkward possessive rather than keeping it: `the data that the FTC published`, not `the FTC's published data`.
- Do not form a possessive from a product, feature, or trademark name when describing what it does. Avoid: `Query Engine's throughput.` Prefer: `the throughput of Query Engine.`
- Do not attach a possessive to a parenthetical abbreviation pair; restructure the sentence.
- Never attach a possessive to a code element (canonical rules: formatting-mechanics for code font, reference-docs-writer for code-element grammar).

## Prepositions

- Do not contort a sentence to avoid a final preposition: `the cluster you are connected to` reads better than `the cluster to which you are connected`.
- Cut prepositional phrases that carry no information, and split a sentence that chains three or more of them.

## Sentence Mechanics

- Put the condition, goal, or circumstance before the action, in every topic type, not only in procedures. Avoid: `Click Revoke if the token is compromised.` Prefer: `If the token is compromised, click Revoke.` (canonical procedure rules: task-docs-writer)
- Put a conditional clause that governs a list before the list's lead-in sentence, never after the items.
- Order a cross-reference purpose first: `For more information about quotas, see ...`, not `See ... for more information about quotas.`
- Treat a sentence past about 26 words as a review signal, not a failure. Keep a readable sentence that expresses one connected idea; split when separate ideas or nested clauses make readers backtrack. Do not detach a condition or qualification from the claim it limits.
- Vary sentence openers, and flag a run of consecutive sentences that begin with the same phrase.
- Expand compressed running prose into sentences with explicit articles and verbs when the source establishes the relationship. `If token expires, client disconnects; no retry` can become `If the token expires, the client disconnects and does not retry`. Flag an unknown actor or relationship instead of supplying one. Preserve literal symbols, diagram notation, and concise table cells where their format makes the meaning clear.

## Paragraph Mechanics

- Keep one idea per paragraph and put the load-bearing information first.
- Treat a paragraph past five or six sentences as a signal to split or cut, but never split a paragraph that carries a single idea. One-sentence paragraphs are fine.
- Shorten sentences and paragraphs together; never merge sentences to lower the sentence count.

## Global-Audience Usage

- Prefer the plain short word and the single verb (term-by-term rulings: word-choice). Keep `set up`, `log in`, and `sign in` as accepted verb phrases.
- Keep helper words that block misparsing: `if X, then Y`, `assumes that you have`, `start the profiler, and then run the build`.
- Make the scope of `only` and similar limiters clear without choosing a new restriction. Move a limiter closer to what it modifies only when the supplied context establishes that focus. `The agent only reports failed checks to the collector.` is not enough by itself to choose between restricting the action, the reported checks, or the recipient. If the source separately establishes that successful checks are excluded, `The agent reports only failed checks to the collector.` is appropriate. Otherwise, retain the wording and flag the unresolved scope rather than guessing. Leave already clear wording unchanged; see the review cases below.
- Stack at most two nouns as modifiers of another noun; move the rest after the noun.
- Attach a category noun to a bare technical name: `the config.yaml file`, `the build command`.
- Repeat a shared word across parallel elements when dropping it creates ambiguity: `both network segmentation and identity segmentation`.
- Do not use the same word as a noun and a verb in nearby sentences, and use each word in its primary sense.
- State abilities positively and avoid double negatives. Avoid: `Nothing prevents you from disabling the check.` Prefer: `You can turn off the check.`
- Avoid humor, idioms, seasons, holidays, sports references, and country-specific cultural references.

## Limiter Scope Review Cases

These original cases are manual editorial checks, not model-performance
measurements. Treat the supplied context as the evidence boundary and accept
equivalent wording that preserves the same restriction. A style preference for
nearby modifiers does not establish a missing product rule.

| Supplied source and context | Acceptable decision | Meaning drift to reject |
| --- | --- | --- |
| `The agent only reports failed checks to the collector.` No other context is supplied. | Retain the sentence and ask what `only` restricts. | Selecting action, check type, or recipient scope without evidence. |
| The same sentence; the source separately says successful checks are excluded from these reports. | `The agent reports only failed checks to the collector.` | Changing the restriction to who reports, where reports go, or what other actions the agent can perform. |
| The same sentence; the source separately contrasts reporting failed checks with repairing them, which the agent does not do. | State the sourced contrast: the agent reports failed checks to the collector but does not repair them. | Inferring that successful checks are never reported. |
| The same sentence; the source separately says the collector is the sole recipient of failed-check reports. | `The agent reports failed checks only to the collector.` | Inferring a restriction on other actions or check types. |
| `Only administrators can delete archived snapshots.` The source establishes the role restriction. | Keep the clear subject restriction. | `Administrators can only delete archived snapshots.`, which can restrict their actions or the objects instead. |
| `Retry only if the error is transient.` The source supplies a necessary condition, not a command to retry every transient error. | Preserve `only if` and its relationship to retrying. | `If the error is transient, retry.`, which makes the condition sufficient for the instruction. |
| `The exporter saves not only metrics but also traces.` Both outputs are established. | Preserve both outputs and the correlative relationship. | Treating `only metrics` as an exclusion or dropping traces. |
| The source contains the literal flag `--failed-only` and a UI label `Only mine`. | Preserve both literals under the code-literal exception. | Moving or deleting words inside a flag or label to satisfy prose style. |

[Microsoft's modifier guidance](https://learn.microsoft.com/en-us/style-guide/grammar/dangling-misplaced-modifiers)
shows that modifier placement can change what a sentence restricts. These cases
apply the skill's source-preservation contract: clarify an established scope,
but flag ambiguity when the intended scope is not supplied.

## Attribution

The tense and modal guidance draws on [Google’s tense guidance](https://developers.google.com/style/tense) and [prescriptive-documentation guidance](https://developers.google.com/style/prescriptive-documentation). The evidence checks above apply those style defaults without changing the supplied draft’s meaning.

Parts of this reference are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified.
