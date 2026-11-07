---
name: technical-content-clarifier
description: >-
  Concept clarification for concept topics and audience-aware technical explanations: architecture explanations, engineering blog posts, conceptual documentation, onboarding overviews, release narratives, executive-friendly summaries, developer education, and explanations of systems, algorithms, APIs, incidents, or tradeoffs. Use for clarifying abstractions, choosing examples, tuning tone, and removing knowledge gaps.
  Use when caveats, uncertainty, audience proximity, or source-backed simplification matter.
metadata:
  version: "1.1.5"
  risk_tier: low
---

# Technical Content Clarifier

## Overview

Turn dense technical material into concept topics or explanatory content that a target reader can follow, remember, and use. Optimize for audience fit, concrete examples, accurate simplification, and a clear through-line.

Read [references/clarity-patterns.md](references/clarity-patterns.md) when drafting or revising explainers, content, overviews, or conceptual documentation.

Choose the explanatory sequence, examples, and analogies to fit the reader. Treat the default structure as an adaptable scaffold; preserve supplied facts, qualifications, exact literals, and the user's required format.

## Workflow

1. Identify the reader: role, technical depth, goal, proximity to the specific system, likely objections, and prior knowledge. If the audience is missing, infer a likely one and state the assumption.
2. Define the point of the content in one sentence: what the reader should understand, believe, or do after reading.
3. Build a through-line: situation, tension or gap, explanation, implications, next action. Put the main point of each section or paragraph first.
4. Head concept sections with descriptive noun phrases that do not begin with an -ing word: "Retention policy design", not "Designing the retention policy".
5. Convert abstractions into concrete examples, scenarios, diagrams-in-words, carefully bounded analogies, or small code/config snippets. Use nonexamples when the boundary matters, and label example boundaries clearly.
6. Define unfamiliar terms at first use. Expand acronyms unless the audience clearly knows them.
7. Write around jargon or substitute a specific plain term; keep a jargon term only when readers search for it or no accurate synonym exists. Gloss a single occurrence inline with the term in parentheses; define a recurring term in parentheses at first mention and use it consistently after. Treat overloaded words such as "solution", "support", and "workload" as undefined until the text pins their meaning or replaces them. Apply the jargon decision tree in [references/clarity-patterns.md](references/clarity-patterns.md).
8. For executives, product partners, or other non-implementers, explain implementation terms in plain language and lead with source-supported user impact or decision consequences. Do not infer a benefit, regression, cause, cost, or affected population from a technical change alone. For example, `connection pooling changed under burst load` can become "Connection reuse changed during traffic spikes; the source does not specify the effect on users." If the mechanism matters to the decision, retain and explain it. See the source-to-impact checks in [references/clarity-patterns.md](references/clarity-patterns.md).
9. Use consistent terminology for the same concept throughout the piece. If the source uses competing terms, choose one and mention aliases only when needed.
10. Strip step-by-step procedures and extensive reference tables from concept topics. Link to task or reference topics instead.
11. Separate confirmed facts, suspected causes, examples, assumptions, and open questions before simplifying. Do not let a cleaner narrative turn uncertainty into fact.
12. Remove false precision, jargon that does not help, idioms, slang, sports metaphors, ambiguous pronouns, and references that may not travel across cultures or teams.
13. Describe components with source-supported technical verbs (specifies, detects, sends, returns, sets, reads). Changing a human verb does not supply a missing algorithm, trigger, actor, or successful result; preserve known behavior and flag necessary unknown details rather than inventing them. No component "sees", "thinks", "knows", "wants", "decides", or "tells" another what to do. Deliberate, explicitly bounded analogies remain allowed; the ban targets casual human-verb phrasing in ordinary descriptions.
14. Scope every claim so it stays true tomorrow: replace product superlatives (best, fastest, simplest, always, never) with measurable, scoped statements; use "ensure", "guarantee", or "prevents" only when the sources support that strength within the stated scope and conditions; preserve established behavior rather than weakening it to design intent; attach a source to every performance or cost figure or label it unverified. Apply the durable-claims rules in [references/clarity-patterns.md](references/clarity-patterns.md).
15. Keep simplification honest. Preserve important caveats and tradeoffs instead of smoothing them away.
16. Prefer active voice and short sentences. Split long sentences that carry multiple ideas. Treat a paragraph past five or six sentences as a signal to split or cut, but never split a single idea; one-sentence paragraphs are fine. Shorten sentences and paragraphs together — never merge sentences just to lower the count. Vary sentence openers, and rewrite runs of consecutive sentences that start with the same phrase.
17. For executive summaries, do one final vocabulary pass and replace implementation labels such as `backend`, `pooling`, `connection`, `burst load`, `tail latency`, and `retry` unless the label is required for the decision. If a low-level cause is not needed for the decision, summarize it as "an internal technical change" only when that preserves the source, and focus on documented impact. If impact is unknown, state that gap instead of inventing a consequence. Choose plain phrases that preserve the specified metric and conditions; do not turn unspecified `tail latency` into an invented percentile or average.
18. End with a concrete next action, decision, or mental model. For release narratives, make the final sentence tell the reader what to try, monitor, adopt, or understand next.

## Verify and Correct

Use the existing self-check internally. Check the complete explanation, including examples and analogies, against the sources and reader's question. Correct confirmed in-scope gaps once, then recheck the final explanation for meaning, caveats, and literals. In review-only work, verify findings without editing the source. Report remaining gaps; a caller's explicit review budget takes precedence.

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
- [ ] Executive summaries simplify vocabulary without inventing impact or causality; direction, scope, conditions, and decision-relevant mechanisms stay source-supported.
- [ ] Procedural steps and dense reference facts are split out or linked rather than embedded.
- [ ] Each abstract claim has an example, scenario, or observable consequence.
- [ ] Examples and nonexamples are clearly labeled or separated from general explanation.
- [ ] Confirmed facts, suspected causes, assumptions, and open questions are not blurred together.
- [ ] The explanation is accurate enough for experts and approachable enough for the target reader.
- [ ] Analogies are bounded so they do not obscure the technical distinction.
- [ ] No component is given human faculties; technical verb replacements preserve sourced behavior without inventing an algorithm, trigger, actor, or successful result.
- [ ] Unsupported or overbroad assurances, superlatives, and unsourced figures are removed or scoped; source-supported behavior keeps its strength, conditions, and limits under the durable-claims rules.
- [ ] Paragraphs past five or six sentences are split or cut without splitting a single idea, and sentence openers vary.
- [ ] Register fillers such as "please note that", "at this time", "let's do X", and exclamation marks are gone (canonical list: docs-style-editor word-choice).
- [ ] Ambiguous pronouns such as `it`, `this`, `that`, and `they` are replaced when the referent is unclear.
- [ ] Idioms, slang, and culturally specific metaphors have been removed or replaced.
- [ ] Outside-source material is paraphrased and linked, never copied.
- [ ] Timeless cleanup removes roadmap implications without deleting current capability limitations, their scope or conditions; time-stamped genres and exact literals retain their appropriate context.
- [ ] The piece has a clear narrative path, not a loose pile of facts.
- [ ] The ending gives the reader a concrete next action, decision, or mental model.

## Gotchas

- Do not equate "engaging" with hype. Make the material useful, concrete, and well-paced.
- Do not remove caveats that affect decisions.
- Do not use analogies that break under the key technical distinction.
- Do not assume the reader knows the team's acronyms, architecture history, or incident context.
- Do not turn a tidy story into a false certainty.
- Do not copy text, images, code, logos, or transcribed speech from outside sources. Paraphrase in your own words and link to the original; a verbatim quote with a citation is not a substitute for paraphrase in product documentation. The paraphrase must preserve the source's meaning and stay traceable to its source.
- Do not turn a security feature into a blanket promise that a product "is secure" or prevents all attacks. Distinguish a design goal from source-established behavior within a named scope or threat model. Preserve documented conditions, exceptions, and uncertainty; neither invent protection nor weaken a supported mechanism into mere intent.
- In ordinary product explanations, remove roadmap implications, not current capability facts. For example, change `does not yet support attachments` to `does not support attachments`, retaining the affected feature, version, scope, and conditions. Do not delete the limitation or turn planned support into available support. Preserve exact literals; flag consequential uncertainty rather than guessing. Release notes and blog posts retain their time-stamped context (see the timeless-capability checks in the reference).

## Attribution

Parts of this skill are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified. This skill is not affiliated with or endorsed by Google.
