# Word Choice

## Contents

- [Use When](#use-when)
- [Scope Notes](#scope-notes)
- [Ambiguous Words](#ambiguous-words)
- [Connectors, Latin Abbreviations, and Chat-isms](#connectors-latin-abbreviations-and-chat-isms)
- [Register and Ease Words](#register-and-ease-words)
  - [Ease-Word Review Cases](#ease-word-review-cases)
- [Redundant Framing](#redundant-framing)
- [Timeless Wording](#timeless-wording)
  - [Resource-State Review Cases](#resource-state-review-cases)
- [Precise Verbs and Nouns](#precise-verbs-and-nouns)
  - [Lifecycle-Verb Review Cases](#lifecycle-verb-review-cases)
  - [Account-Identity Review Cases](#account-identity-review-cases)
- [Compound Spellings](#compound-spellings)
- [Part-of-Speech Splits](#part-of-speech-splits)
- [Sense-Dependent Spellings](#sense-dependent-spellings)
- [Agreement and Article Rulings](#agreement-and-article-rulings)
- [Term Formatting](#term-formatting)
- [Abbreviations](#abbreviations)
- [Spelling and Dictionary Policy](#spelling-and-dictionary-policy)
  - [Dialog Terminology Review Cases](#dialog-terminology-review-cases)
- [Product Names and Trademarks](#product-names-and-trademarks)
- [Document Self-Reference](#document-self-reference)
- [Attribution](#attribution)


## Use When

Load this reference for the word-choice pass: term-by-term rulings, register rules, timeless wording, abbreviations, spelling policy, and product and trademark names.

## Scope Notes

- The register rules in this file — `please`, ease claims, exclamation marks, `let's`, and empty placeholder phrases — are canonical here. Other skills only echo them.
- These rulings govern standard documentation prose. When the write-simplified-technical-english skill is active, its term ledger and controlled vocabulary take precedence.
- Apply the code-literal exception to every ruling: when a disfavored term is a literal command, flag, keyword, field, or UI label, keep the literal exactly as-is in code font, name what it refers to, and use the preferred term in the surrounding prose. Never rewrite an identifier to satisfy a word ruling.
- Rulings that live elsewhere: inclusive terminology, including gendered, ableist, and socially charged terms, in accessibility-inclusion-editor; UI interaction verbs such as `click`, `tap`, `press`, `select`, `clear`, and `enter` in task-docs-writer; modal verbs in [grammar-and-usage.md](grammar-and-usage.md); anthropomorphic verbs and excessive claims in technical-content-clarifier.
- Replace a flagged word with the wording that fits the meaning in that sentence, not with one universal substitute, and keep one term per concept across the doc set.

## Ambiguous Words

| Term | Ruling |
| --- | --- |
| since | Use for elapsed time only; write `because` for cause |
| as | Write `because` for cause, `while` only for simultaneity |
| once | Write `after` when the meaning is sequence |
| while | Write `although` for contrast; keep `while` for simultaneity |
| above, below | Never for position in a document; write `earlier`, `preceding`, `later`, `following` |
| above, below | Prefer `later` or `earlier` for version ranges, preserving the boundary: `2.2 or later` includes `2.2`; `later than 2.2` excludes it. Preserve upper bounds and other constraints; flag ambiguous intent. Never rewrite literal range syntax (canonical home: reference-docs-writer). |
| with | Not for ownership or instrument; write `a node that has 8 vCPUs`, `use the profiler to trace the call` |
| using | Write `by using` when the phrase could attach to the wrong noun |
| possible, impossible | Do not use to mean `you can` or `you cannot` |
| between, among | `between` for two or more distinct things; `among` for members of a group |
| each | Items taken individually; not a synonym for `all` |
| either, neither | Two options with parallel syntax; write `neither A nor B`, never `neither A or B` |
| whether, if | `whether` for alternatives; `if` for a condition |
| comprise | Write `consists of`, `contains`, or `includes` |
| impact | Noun only; the verb is `affects` |
| utilize | Write `use`; keep `utilization` for a measured quantity |
| leverage | Write `use` or `builds on` |
| in order to | Write `to` unless the longer form prevents a misread |
| typically | Means `under normal circumstances`; do not open a sentence with it |
| scale (bare) | State direction and magnitude: `scale out to 12 nodes` |
| performant | Name the quality: `fast`, `low latency`, `accurate` |
| functionality | Write `features` or `capabilities` when that is the meaning |
| actionable | Write `useful` or `that you can act on` |
| best effort | Describe the actual delivery behavior |
| pros, cons | Write `advantages`, `disadvantages` |
| key (adjective) | Do not use for `crucial`; name the reason it matters |
| key (noun) | Say which kind at first mention; write `key-value pair`, and keep `key pair` for two cryptographic keys |
| image | Write `disk image` or `container image` |
| workload, hotspot, nonce, canary | Define at first use and keep the definition; never `hotspotting` or `canarying` |
| limits, quota | Name the specific kind: `usage limit`, `service quota` |
| legacy | Acceptable with a definition, never as a pejorative |
| agnostic | Write `platform-independent` or name the independence |
| traditional | Write `conventional` or the precise contrast |
| exploit | Security sense only; never a synonym for `use` |
| anti-pattern | Avoid, especially in a heading; name the practice to avoid |
| deprecated | Means discouraged but still available; never use it for removed, deleted, or shut down |

## Connectors, Latin Abbreviations, and Chat-isms

| Term | Ruling |
| --- | --- |
| via | Write `through`, `by using`, or `over` |
| and/or | Write `X, Y, or both`; allowed only in a space-constrained table |
| vice versa | State the reciprocal relationship, or write `conversely` |
| e.g. | Write `for example` or `such as` |
| i.e. | Write `that is` |
| etc., and so on | Rewrite with `such as` or `including`; never combine either with `such as` |
| aka | Write `also known as` |
| tl;dr | Write `to summarize` |
| ymmv | Write `your results might vary` |
| RTFM | Write `For more information, see ...` |
| vs. | Write `versus` |
| N/A | Write `N/A`, never `NA`, and spell it out at first reference |
| authN, authZ | Write `authentication`, `authorization` |
| 10x | Write `10 times` |
| approx. | Write `approximately` |

## Register and Ease Words

| Term | Ruling |
| --- | --- |
| please | Only when asking permission or forgiveness; never in an instruction or a cross-reference |
| please note that, at this time | Delete; state the point directly |
| let's | Address the reader: `you`, or an imperative step |
| simply, just, easy, easily, simple, quick, quickly | Remove empty reassurance about effort or speed. Keep or precisely rephrase a source-supported restriction, timing relationship, comparison, or technical term; do not delete by word alone. |
| desire, desired, wish | Write `want` or `need` |
| exclamation mark | None in technical prose except inside a literal |
| obviously, of course, needless to say | Delete |
| internet slang, buzzwords, pop-culture references | Delete; state the technical point |

Avoid: `Simply click Deploy!` Prefer: `Click Deploy.`

Before removing an ease word, check its function in context. For example, `just`
can mean `only`, indicate recency, or express a boundary such as `just before`.
Preserve that meaning without adding precision the source does not supply.
Keep established terms such as `simple random sampling` and exact UI labels.
If `quickly` carries a required timing condition but no usable threshold is
supplied, flag the missing threshold; do not invent seconds or delete the
condition. Do not fill vague wording such as `handles the rest` with guessed
product behavior. Flag the missing behavior instead.

[Microsoft's concise-writing guidance](https://learn.microsoft.com/en-us/style-guide/word-choice/use-simple-words-concise-sentences)
distinguishes unnecessary modifiers from those important to meaning.
[Google's word list](https://developers.google.com/style/word-list#just) makes
removing `just` meaning-dependent; its [tone guidance](https://developers.google.com/style/tone)
discourages unhelpful ease claims in procedures. Apply those preferences within the
source-preservation boundary, rather than as a word blacklist.

### Ease-Word Review Cases

These original editorial cases check instruction consistency and source
preservation. They are not model-behavior evaluations or evidence that a model
produces better writing. Accept equivalent wording that preserves the source.

| Source and context | Acceptable decision | Failure to reject |
| --- | --- | --- |
| `Simply click Deploy!` is empty reassurance in a procedure. | `Click Deploy.` | Keeping empty ease claims because meaningful uses also exist. |
| `Return just the failed records.` The source excludes successful records. | `Return only the failed records.` | Removing the restriction and returning all records. |
| `The request has just completed.` Recency matters to the troubleshooting account. | Retain the recency or rephrase it as `recently completed`. | Changing it to a timeless state or inventing an elapsed duration. |
| `Take the snapshot just before the migration begins.` | Preserve the close timing and before/after relationship. | Dropping the proximity condition or changing the order. |
| `Use simple random sampling.` The source names that statistical method. | Keep the complete technical term. | Replacing it with generic `random sampling` as an ease-word cleanup. |
| `Press the reset button quickly after the indicator changes.` The source requires prompt action but supplies no interval. | Retain the timing condition and flag the unspecified interval. | Inventing a numerical timeout or deleting the timing requirement. |
| The visible control is named `Quick start`. | Preserve the label exactly under the literal exception. | Renaming the control `Start`. |
| `Click Deploy. The pipeline handles the rest.` No later behavior is supplied. | Preserve the source wording and flag the missing behavior as needing a source. | Inventing image-building, rollout, or success guarantees. |

## Redundant Framing

Apply [unslop-guide.md](unslop-guide.md) to conversational padding, ornamental contrast, repeated framing, and decorative jargon. That guide owns the cleanup decisions and evidence boundaries; this reference owns term-by-term rulings.

## Timeless Wording

For product-capability descriptions, describe what the product does now rather than narrating earlier or future capabilities. Apply the table only after checking the word's role: preserve source-defined resource state, reuse versus creation, relative age, and selection rules in procedures or prerequisites. A meaningful distinction can be established elsewhere in the document; it need not appear in the same sentence. If the referent or selection rule is unclear, retain the wording and flag the gap instead of guessing.

| Term | Ruling |
| --- | --- |
| currently, presently, at present, as of this writing | Delete; the document's existence implies them |
| now | Delete, or anchor the change to a release |
| new, newer, latest | For incidental feature-newness claims, delete or use a sourced version/date; preserve a required resource-state or selection distinction |
| old, older | For release comparisons, name the sourced version; preserve source-defined resource-age distinctions |
| soon, eventually, in the future | Delete; do not project a roadmap |
| does not yet | Write `does not support X` |
| existing | Delete only when redundant; retain when it identifies a prerequisite or distinguishes reuse from creation, including across sentences |

- Anchor a genuine newness claim to a fact from the source: `The 4.2 release adds a job history view.`
- Check headings and opening sentences first; `new` and `now` cluster there.
- Exempt time-stamped genres — release notes, blog posts, announcements — and procedural state changes such as `The instance stops responding shortly after you send the shutdown signal.`
- Never invent a version or a date to replace a time-anchored word. Delete only redundant wording; otherwise flag the missing reference point. Do not replace a required moving selector such as `latest successful backup` with a guessed fixed version or date.

[Google's timeless-documentation guidance](https://developers.google.com/style/timeless-documentation) scopes the preference to capability descriptions and allows meaningful procedural state changes. Preserve that boundary rather than applying a word blacklist.

### Resource-State Review Cases

These original manual editorial cases check source preservation and instruction consistency, not measured model behavior or execution of the described operations. Accept equivalent wording that retains the supplied distinctions.

| Source and context | Acceptable decision | Meaning drift to reject |
| --- | --- | --- |
| `Use an existing cluster.` The prerequisite excludes creating a cluster for this task. | Retain `existing` or an equivalent reuse requirement. | `Use a cluster.`, which loses the prerequisite. |
| A rotation guide first says to retain the current key for rollback. A later paragraph says `Select a new signing key.` and requires a replacement key. | Preserve that a distinct replacement key must be selected, even across paragraphs. | Removing the distinction or selecting the retained key instead. |
| `Restore the latest successful backup.` The source defines the selection by successful completion time. | Preserve the success condition and most-recent selection rule. | `Restore a backup.` or inserting an assumed backup date. |
| `Remove the older snapshot.` The source identifies two snapshots by creation time. | Keep the relative-age distinction. | Removing any snapshot or inventing a product version. |
| `The new panel shows request counts.` This is an undated capability description; `new` adds no constraint. | `The panel shows request counts.` | Keeping an unsupported newness claim merely because procedural exceptions exist. |
| `The latest release supports export.` The source supplies no release identifier or intended scope. | Flag which release is meant; do not invent its identifier or broaden support. | `All releases support export.` or substituting a guessed version. |
| The source includes the UI label `New connection` or the literal flag `--existing`. | Preserve the exact literal under the code-literal exception. | Renaming a control or changing command syntax. |
| `Create a new project.` No contrast or resource-selection constraint is supplied; creation establishes newness. | `Create a project.` | Requiring `new` in every creation step. |
| A dated release note announces a new feature. | Retain the appropriate time-stamped genre exception. | Deleting meaningful announcement context mechanically. |

## Precise Verbs and Nouns

| Term | Ruling |
| --- | --- |
| allows you to, enables you to | Write `lets you` |
| enable, turn on | For options and features; pick one verb per document |
| execute | Write `run` when the meaning is the same |
| kill, abort, terminate | Prefer `stop`, `end`, `cancel`, or `exit` only when the source establishes equivalent meaning. Preserve source-defined lifecycle, transaction, and signal distinctions in prose as well as exact literals; if equivalence is unclear, keep the term and flag the gap. |
| surface (verb) | Write `expose` or `make available` |
| persist (verb) | Write `make persistent` or `save` |
| email, interface, ssh, RDP | Never verbs; write `send email`, `interact with`, `connect over SSH` |
| screenshot | Noun only; write `take a screenshot` |
| display | Transitive; write `the panel appears` or `the panel is displayed` |
| ingest | Only for data movement that includes processing; otherwise `import`, `load`, `copy` |
| review | Critical reading only; otherwise `read` |
| fill in, fill out | `fill in` a field, `fill out` a form; a process `populates` |
| extract | The verb for unpacking archives; not `unzip` or `untar`; write `tar file` |
| repo, regex, config, k8s, admin | Write `repository`, `regular expression`, `configuration`, `Kubernetes`, `administrator`, except in literal names |
| the CLI, the UI | Name the specific interface, console, or page |
| account name | Use `username` only when the source establishes that this is a user's username. Preserve distinct account, resource, display-name, ID, and alias concepts; do not infer equivalence from a sign-in context. If the meaning is unclear, keep the term and flag the gap. |
| dialog | The UI window; not `dialog box`, `pop-up`, or `popup`; `dialogue` is human conversation |
| drop-down | Write `list` or `menu`; keep `drop-down` only as a disambiguating modifier |

### Lifecycle-Verb Review Cases

Simpler wording must not change an operation's effects. A stopped resource need
not be terminated, and ending a transaction need not roll it back. Preserve the
source's distinctions, including recoverability, saved changes, and graceful or
forced behavior. Do not infer these effects from a verb alone or add an operation
that the source does not specify. Keep exact command syntax, API names, UI labels,
and quoted output even when surrounding prose can be simplified.

These original manual editorial cases check source preservation, not measured
model behavior or execution of the operations. Each row supplies the evidence
boundary; accept equivalent wording that retains every stated distinction.

| Supplied source and context | Acceptable decision | Meaning drift to reject |
| --- | --- | --- |
| An EC2 guide distinguishes stopping an instance, which can later start, from terminating it, after which it cannot start. | Retain `stop` and `terminate` and the different outcomes in prose. | Replacing `terminate` with `stop`, implying the terminated instance can restart. |
| A PostgreSQL guide says aborting a transaction discards its updates, whereas ending it with `END` commits them. | Retain the rollback/commit distinction; `roll back` can explain `abort` without changing supplied syntax. | Replacing the abort instruction with `end the transaction` or changing `ABORT;` to `END;`. |
| A service guide defines a graceful stop as draining active requests and a forced termination as interrupting them. | Preserve both operations and the stated request-handling difference. | Calling both operations `stop` without preserving which one interrupts requests. |
| The supplied product definition says `terminate the preview` means the same action as `stop the preview`; only ordinary prose is being edited. | Use `stop the preview`. | Requiring the more complex verb despite established equivalence, or inventing data loss. |
| The only supplied sentence is `Abort the job.` No behavior or equivalent operation is defined. | Keep `abort`; flag the missing definition if clarification is needed. | Assuming `cancel`, `stop`, or `exit` has the same effect, or inventing rollback behavior. |
| The source includes the UI label `Terminate instance`, API name `terminate_instances`, command `kill -TERM 1234`, or output `Transaction aborted`. | Preserve each literal exactly; clarify surrounding prose only from supplied facts. | Renaming a control, changing syntax, or treating the word `kill` alone as proof of forced termination. |

The first two cases are grounded in the distinct operations documented by
[AWS EC2 instance state changes](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html)
and PostgreSQL 18's [ABORT](https://www.postgresql.org/docs/18/sql-abort.html)
and [END](https://www.postgresql.org/docs/18/sql-end.html) references (checked
2026-10-27). These are examples of why equivalence needs evidence, not universal
definitions for other products.

### Account-Identity Review Cases

A word-choice preference cannot establish that two identifiers name the same thing.
An account may contain many users, and a sign-in flow may require more than one
identifier. Keep the documented distinction and exact UI labels, field names,
commands, and values. Do not rename a product field or infer that changing one
name changes another.

These original manual editorial cases check source preservation, not measured
model behavior or verification of a real sign-in flow. Each row supplies the
complete evidence boundary; accept equivalent accurate wording.

| Supplied source and context | Acceptable decision | Meaning drift to reject |
| --- | --- | --- |
| A billing guide says the account name identifies the organization on invoices; a separate username identifies an individual user. | Retain both names and their distinct roles. | Renaming the invoice's account name to `username`. |
| A service guide says its account name is the username used to identify the user. No literal field label is being edited. | Use `username` in explanatory prose, preserving the supplied equivalence. | Banning `username` even when the source establishes that meaning. |
| The sign-in instructions require an account ID or account alias, plus an IAM username. | Preserve the alternative account identifiers and the additional username requirement. | Treating the alias as the username or dropping one required identifier. |
| A resource reference defines the storage account name as part of a service endpoint; it is not a user identity. | Keep `storage account name` and its resource role. | Calling the endpoint component a username. |
| The source says a display name is shown to other users and is different from the username. | Preserve both terms and their different purposes. | Replacing the display name with `username` for consistency. |
| The prose only says `Enter your account name.` No product definition is supplied. | Keep the wording and flag what identifier the product expects if needed for the task. | Guessing that the field accepts a username, email address, account ID, or alias. |
| A visible control is labeled `Account name`, or a supplied command has an `--account-name` flag. | Preserve the exact label or flag under the literal exception, even when surrounding prose can be clarified. | Renaming the UI control or command flag to satisfy a prose preference. |
| The source says changing an account's display name leaves its account ID and users unchanged. | Keep the change and the unchanged identities distinct. | Claiming the rename changes user credentials or the account ID. |

This narrows the [Google word-list preference](https://developers.google.com/style/word-list#account-name)
when it would conflate product concepts. The product's authoritative definitions
control meaning: [AWS account naming documentation](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-update-acct-name.html)
describes an account name used in billing and organization views, while
[AWS IAM sign-in documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_sign-in.html)
distinguishes an account ID or alias from the user's name. These are examples of
why equivalence must be established, not universal rules for other products.

## Compound Spellings

| One word | Two words | Hyphenated |
| --- | --- | --- |
| backend, frontend, codebase, filename | data center, data source, data type | multi-cluster, multi-region, multi-tenancy |
| hostname, namespace, endpoint, datastore | file system, name server, key ring | non-key, pre-existing, pre-shared key |
| lifecycle, runbook, timestamp, toolkit | user base, web server, home screen | on-premises (never `on-premise`), read-only |
| walkthrough, whitespace, wildcard, whitepaper | lock screen, status bar, table name | big-endian, little-endian, sub-command |
| email, ecommerce, healthcare, livestream | data cleaning (never `cleansing`) | end-to-end, cost-effective |
| microservices, autoscaling, hardcoded, inline | single most | up-to-date (before a noun) |
| prebuilt, prerecorded, colocate, subtree | | |

## Part-of-Speech Splits

| Noun or adjective | Verb |
| --- | --- |
| setup | set up |
| sign-in, sign-out | sign in, sign out (prefer `sign in` over `log in`; always `sign in to`, never `sign into`) |
| startup | start up |
| timeout | time out |
| failover | fail over |
| backup | back up |
| clickthrough | click through |
| plugin (noun), plug-in (adjective) | plug in |
| third party (noun), third-party (adjective, never `3rd-party`) | — |
| time zone (noun), time-zone (adjective) | — |
| high availability (noun), high-availability (adjective; `HA` after first use) | — |
| load balancing (noun), load-balancing (adjective) | — |

## Sense-Dependent Spellings

| Term | Ruling |
| --- | --- |
| runtime, run time | `runtime` is the execution environment; `run time` is a moment during execution |
| dataflow, data flow | `dataflow` is the stream-processing paradigm; `data flow` is the flow of data |
| plaintext, plain text | `plaintext` in cryptography; `plain text` elsewhere |
| directory, folder | `directory` in command-line contexts, `folder` in GUI contexts; default to `directory` |
| style sheet, stylesheet | Either form, used consistently across the doc set |

## Agreement and Article Rulings

| Term | Ruling |
| --- | --- |
| data | Singular mass noun: `the data is`, `less data` |
| appendixes, indexes, matrixes | Use these plurals; keep `indices` and `matrices` for mathematical or financial contexts |
| emoji | Same form singular and plural |
| a, an | Choose by how the audience pronounces what follows: `a SQL query`, `an SAP system`, `a URL` |
| per | Write rates as `requests per second`, not `requests/second`; do not use `per` for `for each` or `according to` |

## Term Formatting

| Term | Ruling |
| --- | --- |
| ID | Not `id` or `Id`, except inside a literal |
| I/O, PoP, DNSKEY, SHA-1, NoSQL, IoT | Use these exact forms |
| OAuth 2.0, IPsec, UTF-8, HTTPS | Not `OAuth2`, `IPSec`, `UTF8`, or `HTTPs` |
| Unicode, Markdown | Always capitalized; never `UNICODE` |
| internet, web, alpha, beta | Lowercase unless part of an official name |
| curl, lint, trojan | Lowercase; never `cURL` |
| RFC 8446 | `RFC`, a space, then the number |
| v2.4 | Lowercase `v` for a version |
| Unix-like | Use this form for Unix-derived systems |
| boolean, Boolean | Code font for the language keyword, lowercase for the abstract type, capitalized for Boolean logic |
| Mbps, MBps | Use these rate abbreviations, never `Mb/s` or `MB/s` |

## Abbreviations

- Spell out an unfamiliar term at first mention and put the abbreviation in parentheses right after it: `border gateway protocol (BGP)`. Use the abbreviation alone from then on.
- Skip the abbreviation when the term appears only once, unless the short form is better known than the long form.
- When the first mention falls in a heading, use the abbreviation in the heading and expand it in the first paragraph below.
- Do not expand an abbreviation the audience already knows or whose expansion helps nobody: `API`, `URL`, `HTML`, `PDF`, `RAM`, `CPU`, `REST`, `OS`, `US`.
- Do not introduce an abbreviation for a term outside the document's subject; spell such terms out every time.
- Lowercase the expanded form unless it is a proper noun: `data manipulation language (DML)`, not `Data Manipulation Language (DML)`.
- Never use an abbreviation as a verb. Avoid: `SSH into the node.` Prefer: `Connect to the node over SSH.`
- Prefer the full common word to a truncated one, and write acronyms without internal periods.
- Pluralize an abbreviation as a regular word (rulings: [grammar-and-usage.md](grammar-and-usage.md)).
- Never invent an expansion. If the source does not define an abbreviation and it is not universally known, flag it as an open question.

## Spelling and Dictionary Policy

- Default to US English spelling unless the project's locale or documented style guide requires another variant. Report which convention you followed when the source is mixed.
- Use the house forms below, and never mix variants of one word within a document.

| Variant | House form |
| --- | --- |
| canceled, cancelled | `canceled` and `canceling`, but `cancellation` |
| catalog, catalogue | `catalog` |
| dialog, dialogue | `dialog` for the UI element; `dialogue` for human conversation (see [Precise Verbs and Nouns](#precise-verbs-and-nouns)) |
| gray, grey | `gray` |
| toward, towards | `toward`, and the same for `backward` and `forward` |
| acknowledgment, acknowledgement | `acknowledgment`, and `judgment` follows the same pattern |
| email, e-mail | `email`, and `ebook` follows the same pattern |
| website, web site | `website` and `webpage` as one word, `web server` as two |
| life cycle, lifecycle | `lifecycle`, and the same for `timestamp`, `runtime`, and `checkbox` |
| open source, open-source | Two words as a noun, hyphenated before a noun |

- For a variant these tables do not cover, do not settle it from memory. Flag it as an open question, name the dictionary the author should check — Merriam-Webster unless the project names another authority — and leave the draft's form in place until the author answers.
- Spell a technical term absent from the dictionary as the authoritative product or standard documentation spells it. Never invent a spelling; flag the term instead.

### Dialog Terminology Review Cases

Apply the same house form in the word-choice and spelling passes. These original
manual editorial cases check instruction consistency, not measured model behavior
or UI functionality. Project conventions and exact literals still take precedence.

| Supplied source and context | Acceptable decision | Failure to reject |
| --- | --- | --- |
| `The confirmation dialog box appears.` No project-specific terminology is established. | `The confirmation dialog appears.` | Reintroducing `dialog box` during the spelling pass after the word-choice pass removes it. |
| `The confirmation dialog appears.` House defaults apply. | Retain `dialog`. | Adding `box` to satisfy the spelling table. |
| `The transcript records the dialogue between the speakers.` | Retain `dialogue` for human conversation. | Changing conversation to the UI spelling `dialog`. |
| The visible control is labeled `Open dialog box`, or an API identifier is `showDialogBox`. | Preserve each exact literal; apply the house form only to surrounding prose. | Renaming a control or identifier. |
| The project's documented style guide requires `dialog box` in explanatory prose. | Follow the project convention consistently and record the override. | Enforcing the house default despite the higher-precedence project rule. |

[Google's word list](https://developers.google.com/style/word-list#dialog)
distinguishes `dialog` for the UI element from `dialogue` for verbal interaction.
This agrees with the existing house terminology and task-docs-writer examples.

## Product Names and Trademarks

- Write every product, brand, and community-defined term with the capitalization its owner publishes, and match a UI label exactly when you refer to the label.
- Keep an officially lowercase name lowercase even at the start of a sentence, and prefer restructuring the sentence so it does not open with the name.
- Lowercase a feature name unless the owner officially capitalizes it; follow the precedent already set in the product's docs.
- Use the complete official product name. Shorten it only to match a UI label, and make the referent unambiguous when you do.
- After establishing which product you mean, you can discuss the generic concept instead of repeating the brand.
- Do not put `the` before a standalone product name. Do use `the` before a tool or API name, and before a product name that modifies another noun: `the Transcoder API`, `the Transcoder API settings page`.
- Choose `a` or `an` by the sound of the product name when it acts as a modifier.
- Never use a product, feature, or trademark as a verb, and never pluralize, possessivize, or otherwise alter a trademark.
- Use a trademarked term as a modifier of a noun rather than as a bare noun, and follow the owner's published usage and attribution rules.

## Document Self-Reference

- Write `this document`, or the specific genre for that genre: `this tutorial`, `this quickstart`. Do not write `this article`, `this doc`, `this topic`, or `this page` for a document.
- Reserve `page` for a web page or a console sub-page, and never write `chapter` outside a book.
- Spell out `documentation`, except where space is constrained.
- Prefer `Create a project` when the creation verb already establishes newness and no distinction is lost. Retain `new` when the source contrasts the created project with a pre-existing or other project, even outside this sentence or procedure (see [Timeless Wording](#timeless-wording)).
- Write `information about X`, not `information on X`.

## Attribution

Parts of this reference are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified.
