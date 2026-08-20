# Inclusive Terms

## Use When

Load this reference before scanning a draft for non-inclusive terminology or replacing flagged terms during an accessibility and inclusion review.

## Replacement Principles

- Replace a flagged term with the precise wording for the meaning intended in that sentence, not with one universal substitute. `crazy` can mean `unexpected`, `complicated`, or `strange` depending on the sentence.
- Prefer rewriting the sentence over coining a one-for-one substitute verb. Avoid: `You can allowlist the sender's domain.` Prefer: `You can add the sender's domain to the allowlist.`
- When an industry term has a precise technical meaning with no accurate synonym, keep the precise term: `terminate` a TCP connection, `execute` permission on a file.
- Keep one term for one concept across the doc set; do not alternate between a replacement and its synonyms.
- Apply figurative-language replacements only to figurative uses. A literal use stays: `a blind spot in the camera's coverage` describes optics, not a person.
- When the write-simplified-technical-english skill is active, its controlled-vocabulary rules take precedence; STE prose avoids pronouns entirely, so the singular-they ruling applies only to non-STE text.

## Gendered Language

- Use singular they, with a plural verb, for a person of unknown or irrelevant gender; or rewrite to second person. Avoid: `Each reviewer submits his comments before he approves the change.` Prefer: `Each reviewer submits their comments before they approve the change.`
- Never write generic `he`, `she`, `he/she`, `s/he`, or `(s)he`, and never alternate genders as a fairness device.
- Write `pronouns`, not `preferred pronouns`.

| Avoid | Prefer |
| --- | --- |
| man-hours, man-days | person-hours, person-days |
| manned | staffed, crewed, operated |
| mankind | humanity, people |
| manmade | artificial, synthetic |
| man-in-the-middle attack | on-path attack, person-in-the-middle attack |
| male adapter / female adapter | plug / socket |
| guys (for a group) | everyone, folks, the team |
| businessman, salesman | businessperson, salesperson |

## Ableist Terms

Replace the term with the precise meaning intended; never use these words about people or systems figuratively.

| Avoid | Prefer |
| --- | --- |
| sanity check | confidence check, completeness check, quick check |
| dummy value, dummy variable | placeholder, sample value |
| hangs, hung | stops responding, stopped responding |
| crazy, insane, bonkers (inanimate subjects only) | unexpected, complicated, strange |
| cripples (a system) | severely degrades, slows |
| blind to | ignores, unaware of |
| blind write | write without a read |
| dumb (a component) | name the actual limitation, such as `has no local cache` |

Avoid: `A crazy config value can cripple the scheduler.` Prefer: `An unexpected config value can severely degrade the scheduler.`

## Violent and Figurative Terms

Remove metaphorical, graphic, or violent phrasing whenever a literal term exists. If an entrenched term must appear so readers can connect it to other material, mention it once, de-emphasized, in parentheses, and use the literal term everywhere else.

| Avoid | Prefer |
| --- | --- |
| STONITH | fence failed nodes |
| blast radius | affected area |
| war room | incident-management team, situation room |
| nuke | remove, delete |
| hit (a key or button) | press, click |
| single pane of glass | unified interface |
| spin up | create, start |
| housekeeping | maintenance, cleanup |
| bleeding edge | newest available, experimental |

- Process verbs such as `kill`, `abort`, and `terminate` have their canonical ruling in docs-style-editor word-choice; when one appears as literal command syntax, the code-literal exception in this reference applies.
- Introduction pattern for an entrenched term: `Isolate the failed node from shared storage (a step some cluster tools call fencing or STONITH).`

## Socially Charged Terms

| Avoid | Prefer |
| --- | --- |
| whitelist | allowlist, trustlist, safelist |
| blacklist | blocklist, denylist, excludelist |
| graylist | provisional list |
| master/slave (paired) | primary/replica, controller/worker, leader/follower, publisher/subscriber |
| master (alone) | primary, main, parent, controller — pick the domain-accurate term |
| native (a feature) | built-in |
| first-class citizen | describe the actual capability |
| grandfathered | legacy, exempt, made an exception |
| tribal knowledge | undocumented team knowledge, knowledge held by the group |
| ninja, guru, wizard, sherpa (a person) | expert, specialist, guide |
| brown bag (session) | learning session |
| black hat / white hat | rule-violating, malicious / ethical, compliant |
| black-box / white-box testing | opaque-box / clear-box testing |

- Use list replacements as nouns only, never as verbs; rewrite the action instead: `add the address to the blocklist`, not `blocklist the address`.
- Never call a person a `native` anything; describe the relevant experience instead.

## Disability Language

- Use the terms a community prefers: person-first by default (`a person who is blind`, `a person with epilepsy`), identity-first where a community's documented preference is identity-first (`an autistic person`, `the Deaf community`).
- Never use `normal` or `healthy` as the contrast class; write `nondisabled`, `sighted`, `hearing`, or `neurotypical` as the context requires.
- Reserve `abnormal`, `deficient`, and similar words for systems and measurements, never for people.
- `see` is acceptable for cross-references; do not contort sentences to avoid it.

| Avoid | Prefer |
| --- | --- |
| suffering from, afflicted with, victim of | living with, has |
| wheelchair-bound, confined to a wheelchair | uses a wheelchair |
| differently abled, special, handi-capable, physically challenged | name the disability plainly, in the community's preferred terms |

- If you do not know which terms a community prefers, flag the passage for human verification. Never fabricate a preference.

## Older Adults

| Avoid | Prefer |
| --- | --- |
| the elderly, seniors, senior citizens | older adults |
| the aging, age-themed wordplay such as `90 years young` | older adults, the aging population |

## Example Names and Personas

- Give example people globally diverse fictional given names drawn from many cultures, and default every example person to singular they.
- Never build an example on a gender binary, such as one imagined user of each gender, and never assign stereotyped roles, such as a gendered executive or an ethnically typed engineer.
- Avoid holidays, sports, and cultural references specific to one country; pick scenarios that translate everywhere, such as calendars, inventories, or sensor readings.
- Do not classify readers divisively, such as splitting them into native and non-native English speakers; describe the relevant skill or context instead.
- Reserved fictitious values for domains, IP addresses, and phone numbers have their canonical table in docs-style-editor safe-example-values; this reference governs only the people and personas in examples.

## Legacy-Term Introduction Pattern

When readers need a legacy term to recognize a concept or to search other material, use this pattern exactly once per document:

1. At first use, give the preferred term with the legacy term in parentheses: `an allowlist (called a whitelist in some older tools)`.
2. After that, use only the preferred term.
3. Do not repeat the parenthetical, add the legacy term to headings, or use it as a verb.

If readers do not need the legacy term, omit it entirely.

## Code-Literal Exception

This exception protects the anti-fabrication guarantee: literal identifiers are facts, not wording choices.

- A flagged term that is a literal command, flag, keyword, branch name, field, or other identifier is reproduced exactly, in code font, and refers only to that code item. A `--whitelist` flag stays `--whitelist` in every command; a branch literally named `master` stays `master` in commands and code font.
- Never rewrite, rename, or sanitize the identifier, and never invent a cleaned-up alias for it.
- Use the preferred term in the surrounding prose. At first mention, tie the prose term to the literal once, then drop the pairing. Avoid: `Deploy from master.` Prefer: Deploy from the primary branch, which this repository names `master`.
- After the first mention, use the preferred term in prose and return to the code-font literal only when naming the code item itself.
- Never use the non-inclusive term outside code font.
- Record each kept literal in the review output's `Code literals kept as-is` list, with a suggested prose alternative, so maintainers can decide whether to rename the identifier upstream.

## Attribution

Parts of this reference are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified.
