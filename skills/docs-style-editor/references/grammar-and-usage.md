# Grammar and Usage

## Use When

Load this reference for the grammar pass: articles, person, tense, voice, modal verbs, contractions, pronouns, plurals, possessives, prepositions, sentence and paragraph mechanics, and global-audience usage.

## Scope Notes

- These rulings govern standard documentation prose. When the write-simplified-technical-english skill is active, its stricter rules win: no contractions, an approved-word ledger, imperatives in place of actor-plus-modal constructions, no first person, and hard limits of 20 words per procedural sentence and 25 per descriptive sentence.
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
- When imperative sentences accumulate in running text, convert them into a formatted procedure (canonical procedure rules: task-docs-writer).

## Tense

- Describe system behavior in the present tense. Avoid: `The scheduler will retry the job.` Prefer: `The scheduler retries the job.`
- Use `will` only when the action genuinely happens later than the sentence's frame, such as a scheduled backup or an asynchronous delivery.
- Replace hypothetical `would` with present-tense cause and effect: `If the token expires, the gateway rejects the request.`
- Do not narrate unreleased behavior in future tense, and do not describe it at all unless the source states it. Label sourced future behavior as planned.

## Voice

- Make the actor the grammatical subject by default, and rewrite a passive that names its actor with `by`. Avoid: `The manifest is validated by the controller.` Prefer: `The controller validates the manifest.`
- Keep the passive only when the actor is unknown, genuinely irrelevant, or deliberately de-emphasized, or when the object is the point: `The index was rebuilt in March.` `Forty-one conflicts were found.`

## Modal Verbs

Classify every `should` as required, recommended, or optional, and then reword it. Applies to non-STE prose only.

| Meaning | Write | Avoid |
| --- | --- | --- |
| Required action | `must`, or a bare imperative | `should`, `needs to` |
| Recommended action | `We recommend that you ...` | `should`, except for a widely recognized practice such as least privilege |
| Optional action | `can`, or an `Optional:` prefix | `may`, `might`, `could` |
| Ability or permission | `can` | `is able to`, `is allowed to` |
| Possible outcome | `might` | `may`, `could`, `would` |
| Expected outcome | a declarative statement: `The export returns 50 rows.` | `should return` |
| Policy or legal permission | `may` | `can` |

- Never describe an actual state with `should`. Avoid: The flag should be true. Prefer, depending on who acts: `Set the flag to true.`, `The installer sets the flag to true.`, or `If the flag is false, do the following:`
- When several approaches exist, recommend one and say why, rather than listing an unranked menu.

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
- Treat a sentence past about 26 words as a split signal, not a failure. Split at a conjunction or move a qualifier into its own sentence.
- Vary sentence openers, and flag a run of consecutive sentences that begin with the same phrase.

## Paragraph Mechanics

- Keep one idea per paragraph and put the load-bearing information first.
- Treat a paragraph past five or six sentences as a signal to split or cut, but never split a paragraph that carries a single idea. One-sentence paragraphs are fine.
- Shorten sentences and paragraphs together; never merge sentences to lower the sentence count.

## Global-Audience Usage

- Prefer the plain short word and the single verb (term-by-term rulings: word-choice). Keep `set up`, `log in`, and `sign in` as accepted verb phrases.
- Keep helper words that block misparsing: `if X, then Y`, `assumes that you have`, `start the profiler, and then run the build`.
- Place `only` and similar limiters directly before what they limit. Avoid: `The agent only reports failed checks to the collector.` Prefer: `The agent reports only failed checks to the collector.`
- Stack at most two nouns as modifiers of another noun; move the rest after the noun.
- Attach a category noun to a bare technical name: `the config.yaml file`, `the build command`.
- Repeat a shared word across parallel elements when dropping it creates ambiguity: `both network segmentation and identity segmentation`.
- Do not use the same word as a noun and a verb in nearby sentences, and use each word in its primary sense.
- State abilities positively and avoid double negatives. Avoid: `Nothing prevents you from disabling the check.` Prefer: `You can turn off the check.`
- Avoid humor, idioms, seasons, holidays, sports references, and country-specific cultural references.

## Attribution

Parts of this reference are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified.
