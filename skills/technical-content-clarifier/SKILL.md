---
name: technical-content-clarifier
description: >-
  Concept clarification for concept topics and audience-aware technical explanations: architecture explanations, engineering blog posts, conceptual documentation, onboarding overviews, release narratives, executive-friendly summaries, developer education, and explanations of systems, algorithms, APIs, incidents, or tradeoffs. Use for clarifying abstractions, choosing examples, tuning tone, and removing knowledge gaps.
metadata:
  version: "1.0.0"
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
4. Convert abstractions into concrete examples, scenarios, diagrams-in-words, carefully bounded analogies, or small code/config snippets. Use nonexamples when the boundary matters, and label example boundaries clearly.
5. Define unfamiliar terms at first use. Expand acronyms unless the audience clearly knows them.
6. For executives, product partners, or other non-implementers, translate implementation terms into user impact, business risk, cost, speed, reliability, or decision consequences. Avoid raw implementation phrases unless the user explicitly asks to keep them. For example, translate `connection pooling changed under burst load` into "a backend efficiency change made the service handle traffic spikes less smoothly."
7. Use consistent terminology for the same concept throughout the piece. If the source uses competing terms, choose one and mention aliases only when needed.
8. Strip step-by-step procedures and extensive reference tables from concept topics. Link to task or reference topics instead.
9. Remove false precision, jargon that does not help, idioms, slang, sports metaphors, ambiguous pronouns, and references that may not travel across cultures or teams.
10. Keep simplification honest. Preserve important caveats and tradeoffs instead of smoothing them away.
11. Prefer active voice and short sentences. Split long sentences that carry multiple ideas.
12. For executive summaries, do one final vocabulary pass and replace implementation labels such as `backend`, `pooling`, `connection`, `burst load`, `tail latency`, and `retry` unless the label is required for the decision. If a low-level cause is not needed for the decision, name it only as "an internal technical change" and focus on user impact. Prefer plain phrases such as "during traffic spikes," "the slowest 1% of requests," and "peak-demand delays."
13. End with a concrete next action, decision, or mental model. For release narratives, make the final sentence tell the reader what to try, monitor, adopt, or understand next.

## Completion Criterion

Complete the task only when the piece has a named or stated audience, a one-sentence point, concrete examples or observable consequences for important abstract claims, definitions for unfamiliar terms, visible caveats, and a clear next action or mental model; every applicable self-check item passes.

## Default Explainer Structure

```markdown
# [Topic]

## Why This Matters
[Reader-relevant context.]

## The Core Idea
[Plain explanation.]

## Example
[Concrete scenario or snippet.]

## How It Works
[Mechanism, sequence, or model.]

## Tradeoffs
[Limits, risks, and alternatives.]

## What To Do Next
[Action, decision, or further reading.]
```

## Self-Check

- [ ] The opening answers why the reader should care.
- [ ] Section openings and paragraphs lead with their main point.
- [ ] The explanation satisfies the reader's need or curiosity, not just the product's internal structure.
- [ ] The audience analysis accounts for proximity to this system, not only job title.
- [ ] The content defines terms before relying on them.
- [ ] Terminology is consistent, and lists use parallel structure.
- [ ] Vocabulary matches the audience; executive-facing content avoids unnecessary implementation jargon.
- [ ] Executive summaries replace implementation labels with plain impact language unless those labels are required for the decision.
- [ ] Procedural steps and dense reference facts are split out or linked rather than embedded.
- [ ] Each abstract claim has an example, scenario, or observable consequence.
- [ ] Examples and nonexamples are clearly labeled or separated from general explanation.
- [ ] The explanation is accurate enough for experts and approachable enough for the target reader.
- [ ] Analogies are bounded so they do not obscure the technical distinction.
- [ ] Ambiguous pronouns such as `it`, `this`, `that`, and `they` are replaced when the referent is unclear.
- [ ] Idioms, slang, and culturally specific metaphors have been removed or replaced.
- [ ] The piece has a clear narrative path, not a loose pile of facts.
- [ ] The ending gives the reader a concrete next action, decision, or mental model.

## Gotchas

- Do not equate "engaging" with hype. Make the material useful, concrete, and well-paced.
- Do not remove caveats that affect decisions.
- Do not use analogies that break under the key technical distinction.
- Do not assume the reader knows the team's acronyms, architecture history, or incident context.
