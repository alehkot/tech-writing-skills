# Reader-comprehension pass

## Contents

- [Read without supplying the missing context](#read-without-supplying-the-missing-context)
- [Report a supported finding, not a preference](#report-a-supported-finding-not-a-preference)
- [Calibration cases](#calibration-cases)
  - [1. Decision summary with its request displaced](#1-decision-summary-with-its-request-displaced)
  - [2. Team-local abbreviation](#2-team-local-abbreviation)
  - [3. Polished but empty takeaway](#3-polished-but-empty-takeaway)
  - [4. Informational update without an ask](#4-informational-update-without-an-ask)
  - [5. Lookup reference](#5-lookup-reference)
  - [6. Uncertainty is useful information](#6-uncertainty-is-useful-information)
  - [7. Missing evidence is not a license to guess](#7-missing-evidence-is-not-a-license-to-guess)
  - [8. Known audience vocabulary](#8-known-audience-vocabulary)
- [Sources and scope](#sources-and-scope)

Use this pass when reviewing whether a technical draft serves its stated reader.
It supplements source verification; a clear explanation can still be wrong.
For a short, clear message, a brief check is enough. Do not demand a new section,
summary, question, or rewrite merely to make the review visible.

## Read without supplying the missing context

1. Identify the audience, purpose, genre, and relevant prior knowledge from the
   request. If these are uncertain, state the assumption or limit the finding;
   do not assume every reader is a novice or a specialist.
2. Read in the draft's actual order. From its text and the stated reader background,
   state the takeaway and locate its support. For a lookup reference, this can be
   the answer to the requested lookup rather than an overarching argument.
3. For a requested decision or action, locate what is needed, from whom, and any
   supplied conditions or timing. Flag ambiguity that prevents the stated job;
   do not invent an owner or deadline. An informative update, reference, or concept
   explanation need not ask the reader to act.
4. Note where a reader must guess: unexplained team-local terms, unclear referents,
   missing context, or a decision hidden behind detail when the requested format
   is a quick decision summary. Necessary technical vocabulary and a deliberately
   chronological narrative are not defects by themselves.
5. Compare that reading with the request and sources. A fact present only in the
   source does not make the draft self-explanatory. Conversely, known prerequisites,
   accessible links appropriate to the document, and explicitly excluded topics
   do not all need to be repeated. Do not claim to have tested a link or a reader
   unless that verification actually happened.

## Report a supported finding, not a preference

For each comprehension finding, name the passage, the reader's job, the information
or connection they cannot recover, and its consequence. Suggest the smallest
repair supported by the sources. A missing definition may need a question to the
owner, not a guessed expansion. An uncertain audience warrants a conditional
concern, not a confirmed defect. Keep uncertainty visible.

Check proposed cuts against the purpose and evidence. Repetition that obscures a
required decision may merit a cut; length alone does not. Preserve caveats,
conditions, alternatives, warnings, attribution, and decision-relevant detail.
If the draft works, return a scoped clean result and leave it intact.

This pass is a reviewer simulation. Do not claim that readers understood the
artifact, that writing quality improved, or that a usability study passed.
When actual reader feedback is requested, offer a focused question such as asking
where the reader lost the connection to the stated task. Do not contact readers
or share the draft without authorization.

## Calibration cases

These original miniature cases illustrate the contract, not measured model
performance. Review each draft before reading its expected treatment.

### 1. Decision summary with its request displaced

Request: a two-sentence opening for a release approver who needs the decision and
deadline immediately. Source: the approver must choose a launch date by Friday;
the test suite passed, but capacity testing is still pending.
Draft: "The team made progress this week. The test suite passed, but capacity
testing is still pending." A later appendix says "Choose a launch date by Friday."

Expected treatment: a comprehension finding at the opening: the requested decision
and deadline are absent from the required summary, although present later. Move
that existing request into the opening without dropping the capacity caveat. Do
not assert that the release is ready or that the test suite failed.

### 2. Team-local abbreviation

Request: an onboarding note for an engineer new to this team. Source defines
"RBG" as "release-blocking gate".
Draft: "Before the launch review, check whether the RBG is open."

Expected treatment: identify the undefined team-local abbreviation and suggest the
source-backed expansion. Do not invent how the gate opens or a command to check it.

### 3. Polished but empty takeaway

Request: summarize the incident's known customer effect for support engineers.
Source: requests timed out for 12 minutes; the cause is still under investigation.
Draft: "Our systems encountered a challenging event. The team responded with
commitment and continues its pursuit of operational excellence."

Expected treatment: identify the absent effect/duration as coverage and comprehension
problems, not merely disliked vocabulary. Preserve the unknown cause; do not invent
lost data, recovery steps, or a root cause.

### 4. Informational update without an ask

Request: an FYI to service owners. Source and draft: "The maintenance window moved
to Tuesday at 10:00 UTC. No action is required."

Expected treatment: scoped clean result. Do not add a decision, owner, or deadline.

### 5. Lookup reference

Request: review the entry for an optional integer retry-count field in an API
reference. Source and draft: "max_retries: optional integer; default 3. A value of
0 disables retries."

Expected treatment: scoped clean result for that entry. No essay introduction,
next action, analogy, or expansion of API is required for this stated audience.

### 6. Uncertainty is useful information

Request: explain test results to the engineering lead. Source and draft: "In the
staging test, p95 latency fell from 240 ms to 180 ms. We have not measured production
traffic; these results do not establish a production improvement."

Expected treatment: retain the qualification. Do not recommend deleting it for
brevity or replace p95 with average latency.

### 7. Missing evidence is not a license to guess

Request: review a draft for a new cross-team reader. Source does not define RBG.
Draft: "The RBG is open, so proceed."

Expected treatment: flag the undefined abbreviation and unclear action for this reader,
with the precise evidence gap. Request a definition and intended action rather
than assert an acronym expansion or supply executable steps.

### 8. Known audience vocabulary

Request: review a brief note for maintainers who are explicitly familiar with the
release-blocking gate (RBG). Source and draft: "The RBG remains closed until the
capacity test passes."

Expected treatment: scoped clean result. Do not demand an expansion solely because
case 2 needed one for a different audience.

## Sources and scope

- Gergely Orosz, [Becoming a Better Writer](https://newsletter.pragmaticengineer.com/p/becoming-a-better-writer)
  (2022; made public in 2026), recommends recipient-perspective editing and focused
  feedback. This is practitioner advice, not a controlled evaluation.
- Google's [Audience](https://developers.google.com/tech-writing/one/audience)
  guidance explains how prior knowledge and proximity to a subject affect what a
  reader needs explained.

The review procedure and calibration cases above are original applications of
those ideas. They do not impose an author's stylistic preferences or claim an
experimentally established quality gain.
