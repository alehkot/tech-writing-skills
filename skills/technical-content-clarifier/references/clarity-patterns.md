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

## Engagement Without Hype

- Lead with a real problem or decision the reader recognizes.
- Put the main point first in sections and paragraphs; use the rest of the paragraph to explain, qualify, or illustrate it.
- Vary paragraph length, but keep each paragraph about one idea.
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
- The core idea can be summarized in one sentence.
- The explanation answers what the reader needs to know, not how the product team happens to organize the system.
- Each new term is defined before use.
- Vocabulary fits the audience, and non-implementer content avoids unnecessary implementation jargon.
- Executive summaries use plain impact language for causes, risks, and next actions.
- One term is used consistently for each concept, and lists use parallel structure.
- Abstract claims have examples or consequences.
- Confirmed facts, suspected causes, assumptions, and open questions are labeled when the source material is incomplete or uncertain.
- Examples and nonexamples are clearly separated from general explanation.
- Long procedures and reference tables are moved to task or reference topics.
- Idioms, slang, and culture-specific metaphors are removed.
- Caveats and tradeoffs remain accurate.
- The tone is direct, useful, and appropriate for the audience.
- The ending tells the reader what changed, what to do, or how to think about the topic.
