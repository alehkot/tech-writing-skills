# Clarity Patterns

## Use When

Load this reference for conceptual documentation, architecture explainers, engineering blog posts, onboarding overviews, executive technical summaries, release narratives, and educational technical content.

## Source Principles

- Audience fit controls vocabulary, depth, examples, and pacing.
- Concrete examples make abstract technical ideas easier to understand.
- Good examples are focused, easy to adapt, and close to the reader's situation.
- Terms, acronyms, and categories need definitions when readers may interpret them differently.
- Global and cross-team readers benefit from direct language without idioms, slang, sports metaphors, or culture-specific references.
- Honest simplification preserves uncertainty: confirmed facts, suspected causes, caveats, and assumptions must stay distinguishable.

## Audience Snapshot

Before drafting, capture:

```markdown
Audience:
Reader goal:
Likely prior knowledge:
Proximity to this system:
Likely confusion:
Required depth:
Tone:
Confirmed facts:
Assumptions or suspected causes:
Open questions:
```

## Explanation Moves

- Use a small scenario before a general rule when the idea is abstract.
- Use a nonexample when the boundary of a concept matters.
- Label examples and nonexamples so readers can tell where the case starts and stops.
- Use a sequence when the process is temporal.
- Use a compare/contrast table when two ideas are easily confused.
- Use an analogy only when it preserves the key technical distinction; state where the analogy stops if the comparison could mislead.

## Jargon Decision Tree

Apply these steps in order to every jargon term, in-group shorthand, or figurative label in the draft:

1. Write around the term or substitute a more specific plain term. Avoid: "hold a retro on the ingest failure." Prefer: "review why the data import failed." Keep the jargon term only when readers search for it or no accurate synonym exists.
2. If the term appears once, explain it in plain words on the spot, keeping the term itself in parentheses, or point the reader to a definition you trust.
3. If the term recurs, define it briefly in parentheses at first mention and use it consistently afterward.
4. Treat overloaded words such as "solution", "support", and "workload" as undefined until the text pins their meaning in context or replaces them with a precise term.
5. When a jargon or legacy term is a literal command, keyword, or identifier, write it only in code font when referring to that code item, and pair the first mention with the preferred plain term. Example: "add the host to the exception list (run `allowlist add <host>`)."

## Anthropomorphism

- Do not give software or hardware human faculties: no component "sees", "thinks", "knows", "wants", "decides", or "tells" another component what to do.
- Replace human verbs with precise technical verbs such as specifies, detects, sends, returns, sets, and reads. Avoid: "the scheduler decides which node it likes best." Prefer: "the scheduler selects the node with the most free memory."
- Treat anthropomorphism as figurative language that translates poorly; scan for it whenever the audience is global or cross-team.
- Deliberate, explicitly bounded analogies remain allowed. The ban targets casual human-verb phrasing in ordinary descriptions, not labeled analogies.

## Durable Claims

These rules extend the empty-praise ban: a claim must survive tomorrow, not just be defensible today.

- Replace product superlatives (best, fastest, simplest, always, never) with measurable, scoped statements. Avoid: "the fastest way to replicate data." Prefer: "replicated a 10 GB dataset in about 4 minutes in our benchmark (link)."
- Write "ensure", "guarantee", or "prevents" only when the outcome is unconditionally true. Otherwise write "helps", "is designed to", or name the mechanism that produces the outcome.
- Phrase security claims so a future incident cannot falsify them: describe what a feature is designed to do, never promise absolute protection.
- Attach a source or link to every performance or cost figure. If none exists, label the claim unverified or remove it.
- Replace bare comparisons against third-party products with the mechanism that produces the advantage plus a pointer to supporting data. Never disparage the other product.
- Run the durability test before delivery: would the claim still be true after a product update, price change, security incident, or competitor release?
- Do not describe unreleased features or roadmap plans; cut "eventually", "in a future release", and "does not yet support". Time-stamped genres such as release notes, blog posts, and announcements are exempt (full timeless-word ban list: docs-style-editor).

## Engagement Without Hype

- Lead with a real problem or decision the reader recognizes.
- Put the main point first in sections and paragraphs; use the rest of the paragraph to explain, qualify, or illustrate it.
- Vary paragraph length, but keep each paragraph about one idea.
- Treat a paragraph past five or six sentences as a signal to split or cut, but never split a single idea; one-sentence paragraphs are fine.
- Shorten sentences and paragraphs together; never merge sentences just to lower the sentence count.
- Vary sentence openers; rewrite runs of consecutive sentences that start with the same phrase.
- Delete register fillers such as "please note that" and "at this time", "let's do X" phrasing, and exclamation marks (canonical list: docs-style-editor word-choice).
- Prefer active verbs and specific nouns.
- Match vocabulary to the audience. For executives and product partners, replace implementation detail with user impact, operational risk, business consequence, or decision context unless the user explicitly asks to keep the technical label. Do not repeat raw implementation phrases from the source when a plain-language explanation would preserve the point.
- For executive summaries, scan for implementation labels such as `backend`, `pooling`, `connection`, `burst load`, `tail latency`, and `retry`. Replace them unless the label is necessary for the decision. If the low-level cause is not decision-relevant, call it "an internal technical change" and spend the detail on user impact.
- When a technical metric or implementation term is essential for a non-implementer, define it in plain language at first use.
- Replace ambiguous pronouns with the noun they refer to when context is unclear.
- Split long sentences that carry multiple ideas.
- Replace "seamless", "robust", "powerful", and similar empty praise with observable behavior.
- End sections with implications, not filler transitions.
- End the whole piece with a concrete next action, decision, or mental model; release narratives should tell readers what to try, monitor, adopt, or understand next.

## Revision Checklist

- The opening makes the reader's reason to care explicit.
- Section openings and paragraphs put the main point first.
- Concept headings are noun phrases that do not begin with an -ing word.
- The core idea can be summarized in one sentence.
- The explanation answers what the reader needs to know, not how the product team happens to organize the system.
- Each new term is defined before use.
- Jargon terms passed the decision tree: written around, replaced, glossed, or defined at first mention; overloaded words are pinned or replaced.
- Vocabulary fits the audience, and non-implementer content avoids unnecessary implementation jargon.
- Executive summaries use plain impact language for causes, risks, and next actions.
- One term is used consistently for each concept, and lists use parallel structure.
- Abstract claims have examples or consequences.
- Confirmed facts, suspected causes, assumptions, and open questions are labeled when the source material is incomplete or uncertain.
- Examples and nonexamples are clearly separated from general explanation.
- Long procedures and reference tables are moved to task or reference topics.
- Idioms, slang, and culture-specific metaphors are removed.
- No component is given human faculties; behavior is described with precise technical verbs.
- Every claim passes the durability test; superlatives, unconditional guarantees, and unsourced figures are removed or scoped.
- No unreleased-feature or roadmap language remains outside time-stamped genres.
- Paragraphs past five or six sentences are split or cut without splitting a single idea, and sentence openers vary.
- Outside-source material is paraphrased in original wording with a link, never copied.
- Caveats and tradeoffs remain accurate.
- The tone is direct, useful, and appropriate for the audience.
- The ending tells the reader what changed, what to do, or how to think about the topic.

## Attribution

Parts of this reference are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified.
