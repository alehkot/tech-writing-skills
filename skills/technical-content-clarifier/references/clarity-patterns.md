# Clarity Patterns

## Contents

- [Use When](#use-when)
- [Source Principles](#source-principles)
- [Audience Snapshot](#audience-snapshot)
- [Explanation Moves](#explanation-moves)
- [Jargon Decision Tree](#jargon-decision-tree)
- [Source-to-Impact Checks](#source-to-impact-checks)
- [Audience-Simplification Review Cases](#audience-simplification-review-cases)
- [Anthropomorphism](#anthropomorphism)
  - [Behavior-Preservation Review Cases](#behavior-preservation-review-cases)
- [Durable Claims](#durable-claims)
  - [Claim-Strength Review Cases](#claim-strength-review-cases)
  - [Timeless-Capability Review Cases](#timeless-capability-review-cases)
- [Engagement Without Hype](#engagement-without-hype)
- [Revision Checklist](#revision-checklist)
- [Attribution](#attribution)


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

## Source-to-Impact Checks

Changing the vocabulary does not supply missing evidence. Before replacing a mechanism with an impact statement:

- Identify the observed change, its conditions and affected scope, and any supported consequence. Keep observations separate from suspected explanations.
- Preserve the direction of the result: a change alone establishes neither improvement nor harm. "After" does not establish "because of."
- State a missing impact as unknown, not as "no impact." Keep a necessary technical term and explain it when a shorter impact-only sentence would lose the distinction needed for the decision.
- Preserve the measured quantity when explaining a technical metric. Do not substitute an average for a percentile, select an unstated percentile, or turn an internal measurement into a customer outcome.
- Carry these limits into the executive summary, even if the detailed explanation remains elsewhere. Do not invent a customer, revenue, cost, or reliability consequence to make an internal measurement sound relevant.

These checks apply the skill's source-preservation contract to audience adaptation. [Google's audience guidance](https://developers.google.com/tech-writing/one/audience) supports explaining unfamiliar terms for the reader; [Microsoft's concise-writing guidance](https://learn.microsoft.com/en-us/style-guide/word-choice/use-simple-words-concise-sentences) pairs simple words with precise meaning. Neither substitutes for evidence about the documented system.

## Audience-Simplification Review Cases

These original cases are manual editorial checks, not model-performance evaluations. The supplied context is the entire evidence boundary for each case; accept equivalent accurate wording.

| Supplied source and context | Acceptable decision | Meaning drift to reject |
| --- | --- | --- |
| `Connection pooling changed under burst load.` No outcome is supplied. | Explain connection reuse and traffic spikes; flag that user impact is unspecified. | Claiming the service became slower, smoother, cheaper, or less reliable. |
| `After the deployment, checkout errors increased. The cause is under investigation.` | Keep the increase, checkout scope, timing, and unresolved cause in plain language. | Saying the deployment caused the errors. |
| `In the load test, the cache reduced database reads by 20%; customer latency was not measured.` | Retain the measured reduction and test scope; say customer response-time impact was not measured. | Claiming customers received 20% faster responses. |
| `The change reduced checkout failures during traffic spikes.` The source establishes this causal result. | `The change caused fewer checkout failures during traffic spikes.` | Removing the condition or weakening a confirmed cause to mere coincidence. |
| `We have no user-impact measurements for the queue change.` | Say no user-impact measurements are available in the supplied evidence. | `Users were unaffected.` |
| `Tail latency increased.` No percentile is specified. | Preserve the increase in high-end response times and flag the unspecified statistic if needed. | Stating that average latency or the slowest 1% increased. |
| The decision is whether to reuse connections or increase connection capacity. | Retain and explain the two mechanisms so the alternatives remain distinct. | Replacing both alternatives with an indistinguishable "internal technical change." |

## Anthropomorphism

- Do not give software or hardware human faculties: no component "sees", "thinks", "knows", "wants", "decides", or "tells" another component what to do.
- Replace human verbs with source-supported technical verbs such as specifies, detects, sends, returns, sets, and reads. For "the scheduler decides which node it likes best," write "the scheduler selects a node" and flag the unspecified selection criteria when needed for the explanation. Write "the node with the most free memory" only when the source establishes that policy.
- Preserve the actor, action, conditions, and evidence status. Do not turn an unknown mechanism into a plausible algorithm, a request into completed work, or a suspected result into a confirmed result. Keep supplied technical detail rather than reducing a known mechanism to a vague verb. Preserve exact identifiers and quoted strings; the wording pass changes explanatory prose, not literal names.
- Treat anthropomorphism as figurative language that translates poorly; scan for it whenever the audience is global or cross-team.
- Deliberate, explicitly bounded analogies remain allowed. The ban targets casual human-verb phrasing in ordinary descriptions, not labeled analogies.

### Behavior-Preservation Review Cases

These original manual editorial cases check instruction consistency, not measured
model behavior. Each case supplies its own hypothetical evidence boundary; accept
equivalent wording that preserves those facts.

| Supplied source and context | Acceptable decision | Meaning drift to reject |
| --- | --- | --- |
| `The scheduler decides which node it likes best.` No policy is supplied. | Say the scheduler selects a node; flag the missing selection criteria when the explanation needs them. | Inventing most-free-memory, least-loaded, random, or round-robin selection. |
| The source says the scheduler selects the eligible node with the most free memory. | Retain eligibility and the stated memory criterion while simplifying the prose. | Dropping the policy or adding an unsupported tie-break rule. |
| `The monitor sees a failure.` No detection mechanism is supplied. | Say the monitor detects a failure; leave the detection mechanism unspecified. | Claiming it polls every five seconds or receives a particular event. |
| `The controller tells the worker to restart.` The source establishes a restart request, not its outcome. | Say the controller requests a worker restart; keep completion unconfirmed. | Saying the controller restarts the worker or that the restart succeeded. |
| `The client thinks the connection is down.` The source says the client inferred this after a timeout; the actual connection state is unknown. | Describe the client's inference after the timeout and retain the uncertainty about the connection. | Replacing the inference with confirmed detection of a failed connection. |
| The source names an API method `knowsLeader()` and explains that it returns a cached leader identifier. | Keep the literal method name and its cached-return behavior. | Renaming the API or claiming it discovers the current leader. |
| A labeled dispatcher analogy compares a scheduler to a receptionist, with the analogy's limits stated. | Keep the bounded analogy when it helps the reader; keep actual selection behavior separate. | Treating the analogy as evidence for an unstated scheduling policy or banning all analogies. |

[Google's anthropomorphism guidance](https://developers.google.com/style/anthropomorphism)
supports replacing figurative human actions with direct technical wording. The
checks here apply that style rule without supplying missing product behavior.

## Durable Claims

These rules extend the empty-praise ban: a claim must survive tomorrow, not just be defensible today.

- Replace product superlatives (best, fastest, simplest, always, never) with measurable, scoped statements. Avoid: "the fastest way to replicate data." Prefer: "replicated a 10 GB dataset in about 4 minutes in our benchmark (link)."
- Match claim strength to the sources. Use "ensure", "guarantee", or "prevents" only when supported within the stated version, scope, and conditions. A condition limits where a claim applies; it does not by itself make the outcome uncertain. Preserve an established outcome and its limits, or describe its supported mechanism directly. Do not mechanically replace it with "helps" or "is designed to", which express weaker claims.
- Keep design intentions, best-effort behavior, observations, and established guarantees distinct. Preserve tentative language when the evidence is tentative. When support is missing or conflicting, flag that gap instead of inventing either a guarantee or a reassuring design intention.
- Avoid blanket security assurances. Describe the supported mechanism, scope or threat model, and limitations; a narrowly established behavior does not prove that the product is secure against every attack. Use design-intent wording only when that is what the source establishes.
- Attach a source or link to every performance or cost figure. If none exists, label the claim unverified or remove it.
- Replace bare comparisons against third-party products with the mechanism that produces the advantage plus a pointer to supporting data. Never disparage the other product.
- Run the durability test before delivery: would the claim still be true after a product update, price change, security incident, or competitor release?
- In ordinary product explanations, remove roadmap implications while retaining current capability facts. Rewrite `does not yet support attachments` as `does not support attachments`, not by deleting the limitation. Keep the affected feature, version, scope, conditions, and uncertainty; do not turn planned support into available support. Preserve exact literals and flag consequential uncertainty instead of guessing. Time-stamped genres such as release notes, blog posts, and announcements retain their temporal context; this exception does not license inventing or upgrading plans.

### Claim-Strength Review Cases

These original cases check editorial source fidelity and instruction consistency,
not measured model behavior or the correctness of any real product. Each row
supplies its complete hypothetical evidence boundary; accept equivalent accurate
wording. The rule rejects unsupported assurances without weakening supported facts.

| Supplied source and context | Acceptable treatment | Meaning drift to reject |
| --- | --- | --- |
| A supplied protocol specification establishes: `While the lease is valid, only its holder can commit a write.` | Preserve the valid-lease condition and exclusive-write rule. A direct statement of the behavior is sufficient. | `The lease helps limit writes to its holder`, or a guarantee that applies after the lease expires. |
| The source establishes that a gateway with signature validation enabled rejects requests with an invalid signature; unsigned health probes are exempt. | Preserve the enabled setting, invalid-signature rejection, and explicit exemption. | Calling validation merely a design goal, deleting the exemption, or claiming the gateway prevents all unauthorized access. |
| The source says a proposed retry mechanism `is designed to reduce transient failures`; its effect has not been verified. | Preserve the proposal, intent, and unverified effect. | Claiming it guarantees successful requests or prevents every failure. |
| The supplied copy says `Our product prevents account takeovers`, but provides no evidence or stated protection scope. | Flag the unsupported assurance and request evidence or remove the claim. | Inventing a verified protection mechanism, or assuming `is designed to prevent` is supported merely because it sounds weaker. |
| A benchmark reports no duplicate records in 100 test runs with one specified configuration. | State the observation and configuration; leave guarantees unestablished. | Claiming that duplicates can never occur, or dropping the successful observation altogether. |
| `If configured correctly, this guarantees recovery.` Neither the configuration nor a recovery guarantee is established by the supplied evidence. | Flag the missing configuration and support; a conditional clause alone does not validate the claim. | Treating `if configured correctly` as evidence of a guarantee or inventing the required configuration. |
| A quoted diagnostic contains `guaranteed delivery disabled`; the source does not establish its implementation. | Preserve the exact diagnostic and keep implementation details unspecified. | Editing the literal for style, or treating the name as proof of a delivery guarantee. |

[Google's excessive-claims guidance](https://developers.google.com/style/excessive-claims)
calls for verifiable, appropriately bounded claims. These cases apply the
source-preservation contract in both directions: do not strengthen an uncertain
claim or weaken a supported one.

### Timeless-Capability Review Cases

These original cases are manual editorial checks, not measured model behavior.
Each supplied statement is the evidence boundary; accept equivalent wording.

| Supplied source and context | Acceptable decision | Meaning drift to reject |
| --- | --- | --- |
| `The export API does not yet support attachments.` Ordinary product explanation. | Say the export API does not support attachments. | Deleting the limitation or saying attachments are supported. |
| `Version 2 does not yet support attachments on shared workspaces.` | Preserve version 2, attachments, and shared-workspace scope while removing `yet`. | Extending the restriction to all versions or all workspaces. |
| `The source does not establish whether attachments are supported.` | Retain the unknown capability status. | Converting missing evidence into either support or lack of support. |
| `Attachment support is planned for a future release.` No current capability is established. | Do not present the plan as a current feature; flag the missing current-capability evidence if needed. | Inventing present support or asserting non-support from the plan alone. |
| A dated release announcement says attachment support is planned, not committed. | Keep the dated context and tentative status when relevant to that genre. | Changing the plan into a guarantee or released capability. |
| Quoted diagnostic output contains `does not yet support attachments`. | Preserve the exact output; clarify capability separately only from supplied evidence. | Editing the diagnostic literal during prose cleanup. |
| `The export API supports attachments.` | Retain the positive capability statement. | Adding a limitation or future qualification. |

[Google's timeless-documentation guidance](https://developers.google.com/style/timeless-documentation)
removes temporal implications while retaining unsupported-feature information.
These checks apply that distinction without supplying missing product facts.

## Engagement Without Hype

- Lead with a real problem or decision the reader recognizes.
- Put the main point first in sections and paragraphs; use the rest of the paragraph to explain, qualify, or illustrate it.
- Vary paragraph length, but keep each paragraph about one idea.
- Treat a paragraph past five or six sentences as a signal to split or cut, but never split a single idea; one-sentence paragraphs are fine.
- Shorten sentences and paragraphs together; never merge sentences just to lower the sentence count.
- Vary sentence openers; rewrite runs of consecutive sentences that start with the same phrase.
- Delete register fillers such as "please note that" and "at this time", "let's do X" phrasing, and exclamation marks (canonical list: docs-style-editor word-choice).
- Prefer active verbs and specific nouns.
- Match vocabulary to the audience. For executives and product partners, explain implementation detail through source-supported impact or decision context; when impact is missing, explain the mechanism and flag the gap. Do not repeat raw implementation phrases from the source when a plain-language explanation would preserve the point.
- For executive summaries, scan for implementation labels such as `backend`, `pooling`, `connection`, `burst load`, `tail latency`, and `retry`. Replace them unless the label is necessary for the decision. If the low-level cause is not decision-relevant, summarize it as "an internal technical change" only when accurate and spend the detail on documented impact. Apply the source-to-impact checks; do not turn missing impact into either a benefit or an assurance of no harm.
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
- Executive summaries use plain language while preserving source-supported impact, causality, scope, and unknowns.
- One term is used consistently for each concept, and lists use parallel structure.
- Abstract claims have examples or consequences.
- Confirmed facts, suspected causes, assumptions, and open questions are labeled when the source material is incomplete or uncertain.
- Examples and nonexamples are clearly separated from general explanation.
- Long procedures and reference tables are moved to task or reference topics.
- Idioms, slang, and culture-specific metaphors are removed.
- No component is given human faculties; behavior is described with precise technical verbs.
- Every claim passes the durability test; unsupported or overbroad assurances, superlatives, and unsourced figures are removed or scoped without weakening supported behavior or dropping its conditions.
- Timeless cleanup retains current capability limitations, scope, conditions, uncertainty, and exact literals while removing roadmap implications outside time-stamped genres.
- Paragraphs past five or six sentences are split or cut without splitting a single idea, and sentence openers vary.
- Outside-source material is paraphrased in original wording with a link, never copied.
- Caveats and tradeoffs remain accurate.
- The tone is direct, useful, and appropriate for the audience.
- The ending tells the reader what changed, what to do, or how to think about the topic.

## Attribution

Parts of this reference are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified.
