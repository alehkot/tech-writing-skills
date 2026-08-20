---
name: technical-content-clarifier
description: >-
  Concept clarification for concept topics and audience-aware technical explanations: architecture explanations, engineering blog posts, conceptual documentation, onboarding overviews, release narratives, executive-friendly summaries, developer education, and explanations of systems, algorithms, APIs, incidents, or tradeoffs. Use for clarifying abstractions, choosing examples, tuning tone, and removing knowledge gaps.
  Use when caveats, uncertainty, audience proximity, or source-backed simplification matter.
metadata:
  version: "1.1.0"
  risk_tier: low
---

# Technical Content Clarifier

## Overview

Turn dense technical material into concept topics or explanatory content that a target reader can follow, remember, and use. Optimize for audience fit, concrete examples, accurate simplification, and a clear through-line.

Read [references/clarity-patterns.md](references/clarity-patterns.md) when drafting or revising explainers, content, overviews, or conceptual documentation.

## Workflow

1. Identify the reader: role, technical depth, goal, proximity to the specific system, likely objections, and prior knowledge. If the audience is missing, infer a likely one and state the assumption.
2. Define the point of the content in one sentence: what the reader should understand, believe, or do after reading.
3. Build a through-line: situation, tension or gap, explanation, implications, next action. Put the main point of each section or paragraph first.
4. Head concept sections with descriptive noun phrases that do not begin with an -ing word: "Retention policy design", not "Designing the retention policy".
5. Convert abstractions into concrete examples, scenarios, diagrams-in-words, carefully bounded analogies, or small code/config snippets. Use nonexamples when the boundary matters, and label example boundaries clearly.
6. Define unfamiliar terms at first use. Expand acronyms unless the audience clearly knows them.
7. Write around jargon or substitute a specific plain term; keep a jargon term only when readers search for it or no accurate synonym exists. Gloss a single occurrence inline with the term in parentheses; define a recurring term in parentheses at first mention and use it consistently after. Treat overloaded words such as "solution", "support", and "workload" as undefined until the text pins their meaning or replaces them. Apply the jargon decision tree in [references/clarity-patterns.md](references/clarity-patterns.md).
8. For executives, product partners, or other non-implementers, translate implementation terms into user impact, business risk, cost, speed, reliability, or decision consequences. Avoid raw implementation phrases unless the user explicitly asks to keep them. For example, translate `connection pooling changed under burst load` into "a backend efficiency change made the service handle traffic spikes less smoothly."
9. Use consistent terminology for the same concept throughout the piece. If the source uses competing terms, choose one and mention aliases only when needed.
10. Strip step-by-step procedures and extensive reference tables from concept topics. Link to task or reference topics instead.
11. Separate confirmed facts, suspected causes, examples, assumptions, and open questions before simplifying. Do not let a cleaner narrative turn uncertainty into fact.
12. Remove false precision, jargon that does not help, idioms, slang, sports metaphors, ambiguous pronouns, and references that may not travel across cultures or teams.
13. Describe components with precise technical verbs (specifies, detects, sends, returns, sets, reads). No component "sees", "thinks", "knows", "wants", "decides", or "tells" another what to do. Deliberate, explicitly bounded analogies remain allowed; the ban targets casual human-verb phrasing in ordinary descriptions.
14. Scope every claim so it stays true tomorrow: replace product superlatives (best, fastest, simplest, always, never) with measurable, scoped statements; write "ensure", "guarantee", or "prevents" only for unconditionally true outcomes; attach a source to every performance or cost figure or label it unverified. Apply the durable-claims rules in [references/clarity-patterns.md](references/clarity-patterns.md).
15. Keep simplification honest. Preserve important caveats and tradeoffs instead of smoothing them away.
16. Prefer active voice and short sentences. Split long sentences that carry multiple ideas. Treat a paragraph past five or six sentences as a signal to split or cut, but never split a single idea; one-sentence paragraphs are fine. Shorten sentences and paragraphs together — never merge sentences just to lower the count. Vary sentence openers, and rewrite runs of consecutive sentences that start with the same phrase.
17. For executive summaries, do one final vocabulary pass and replace implementation labels such as `backend`, `pooling`, `connection`, `burst load`, `tail latency`, and `retry` unless the label is required for the decision. If a low-level cause is not needed for the decision, name it only as "an internal technical change" and focus on user impact. Prefer plain phrases such as "during traffic spikes," "the slowest 1% of requests," and "peak-demand delays."
18. End with a concrete next action, decision, or mental model. For release narratives, make the final sentence tell the reader what to try, monitor, adopt, or understand next.

## Completion Criterion

Complete the task only when the piece has a named or stated audience, a one-sentence point, concrete examples or observable consequences for important abstract claims, definitions for unfamiliar terms, visible caveats, source-backed claims or labeled assumptions, and a clear next action or mental model; every applicable self-check item passes.

## Default Explainer Structure

```markdown
# [Topic]

## Why this matters
[Reader-relevant context.]

## The core idea
[Plain explanation.]

## Example
[Concrete scenario or snippet.]

## How it works
[Mechanism, sequence, or model.]

## Tradeoffs
[Limits, risks, and alternatives.]

## What to do next
[Action, decision, or further reading.]
```

## Self-Check

- [ ] The opening answers why the reader should care.
- [ ] Section openings and paragraphs lead with their main point.
- [ ] Concept headings are noun phrases that do not begin with an -ing word.
- [ ] The explanation satisfies the reader's need or curiosity, not just the product's internal structure.
- [ ] The audience analysis accounts for proximity to this system, not only job title.
- [ ] The content defines terms before relying on them.
- [ ] Jargon is written around, replaced, or glossed per the decision tree, and overloaded words are pinned or replaced.
- [ ] Terminology is consistent, and lists use parallel structure.
- [ ] Vocabulary matches the audience; executive-facing content avoids unnecessary implementation jargon.
- [ ] Executive summaries replace implementation labels with plain impact language unless those labels are required for the decision.
- [ ] Procedural steps and dense reference facts are split out or linked rather than embedded.
- [ ] Each abstract claim has an example, scenario, or observable consequence.
- [ ] Examples and nonexamples are clearly labeled or separated from general explanation.
- [ ] Confirmed facts, suspected causes, assumptions, and open questions are not blurred together.
- [ ] The explanation is accurate enough for experts and approachable enough for the target reader.
- [ ] Analogies are bounded so they do not obscure the technical distinction.
- [ ] No component is given human faculties; behavior is described with precise technical verbs.
- [ ] Superlatives, unconditional guarantees, and unsourced figures are removed or scoped per the durable-claims rules.
- [ ] Paragraphs past five or six sentences are split or cut without splitting a single idea, and sentence openers vary.
- [ ] Register fillers such as "please note that", "at this time", "let's do X", and exclamation marks are gone (canonical list: docs-style-editor word-choice).
- [ ] Ambiguous pronouns such as `it`, `this`, `that`, and `they` are replaced when the referent is unclear.
- [ ] Idioms, slang, and culturally specific metaphors have been removed or replaced.
- [ ] Outside-source material is paraphrased and linked, never copied.
- [ ] No unreleased-feature or roadmap language remains outside time-stamped genres.
- [ ] The piece has a clear narrative path, not a loose pile of facts.
- [ ] The ending gives the reader a concrete next action, decision, or mental model.

## Gotchas

- Do not equate "engaging" with hype. Make the material useful, concrete, and well-paced.
- Do not remove caveats that affect decisions.
- Do not use analogies that break under the key technical distinction.
- Do not assume the reader knows the team's acronyms, architecture history, or incident context.
- Do not turn a tidy story into a false certainty.
- Do not copy text, images, code, logos, or transcribed speech from outside sources. Paraphrase in your own words and link to the original; a verbatim quote with a citation is not a substitute for paraphrase in product documentation. The paraphrase must preserve the source's meaning and stay traceable to its source.
- Do not claim a product "is secure" or "prevents" attacks. Describe what a feature is designed to do so a future incident cannot falsify the doc.
- Do not describe unreleased features or roadmap plans; cut "eventually", "in a future release", and "does not yet support". Release notes and blog posts are exempt as time-stamped genres (full timeless-word list: docs-style-editor).

## Attribution

Parts of this skill are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified. This skill is not affiliated with or endorsed by Google.
