# Word Choice

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
| above, below | Never for version ranges; write `2.2 or later`, `2.2 or earlier`, never `2.2+` |
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
| simply, just, easy, easily, simple, quick, quickly | Delete; `just` survives only when it marks the simpler of two alternatives |
| desire, desired, wish | Write `want` or `need` |
| exclamation mark | None in technical prose except inside a literal |
| obviously, of course, needless to say | Delete |
| internet slang, buzzwords, pop-culture references | Delete; state the technical point |

Avoid: `Simply click Deploy, and the pipeline will just handle the rest!` Prefer: `Click Deploy. The pipeline builds the image and starts the rollout.`

## Timeless Wording

Describe what the product does now. Do not narrate how it differs from earlier versions or how it might change.

| Term | Ruling |
| --- | --- |
| currently, presently, at present, as of this writing | Delete; the document's existence implies them |
| now | Delete, or anchor the change to a release |
| new, newer, latest | Delete, or anchor to a version number or a release date |
| old, older | Name the version instead |
| soon, eventually, in the future | Delete; do not project a roadmap |
| does not yet | Write `does not support X` |
| existing | Delete unless it distinguishes two things present in the same sentence |

- Anchor a genuine newness claim to a fact from the source: `The 4.2 release adds a job history view.`
- Check headings and opening sentences first; `new` and `now` cluster there.
- Exempt time-stamped genres — release notes, blog posts, announcements — and procedural state changes such as `The instance stops responding shortly after you send the shutdown signal.`
- Never invent a version or a date to replace a time-anchored word. If the source does not supply one, delete the word or flag the claim.

## Precise Verbs and Nouns

| Term | Ruling |
| --- | --- |
| allows you to, enables you to | Write `lets you` |
| enable, turn on | For options and features; pick one verb per document |
| execute | Write `run` when the meaning is the same |
| kill, abort, terminate | Write `stop`, `end`, `cancel`, or `exit`; keep the original as literal command syntax |
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
| account name | Write `username` |
| dialog | The UI window; not `dialog box`, `pop-up`, or `popup`; `dialogue` is human conversation |
| drop-down | Write `list` or `menu`; keep `drop-down` only as a disambiguating modifier |

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
| dialog, dialogue | `dialog box` for the UI element |
| gray, grey | `gray` |
| toward, towards | `toward`, and the same for `backward` and `forward` |
| acknowledgment, acknowledgement | `acknowledgment`, and `judgment` follows the same pattern |
| email, e-mail | `email`, and `ebook` follows the same pattern |
| website, web site | `website` and `webpage` as one word, `web server` as two |
| life cycle, lifecycle | `lifecycle`, and the same for `timestamp`, `runtime`, and `checkbox` |
| open source, open-source | Two words as a noun, hyphenated before a noun |

- For a variant these tables do not cover, do not settle it from memory. Flag it as an open question, name the dictionary the author should check — Merriam-Webster unless the project names another authority — and leave the draft's form in place until the author answers.
- Spell a technical term absent from the dictionary as the authoritative product or standard documentation spells it. Never invent a spelling; flag the term instead.

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
- Write `Create a project`, not `Create a new project`, unless you are distinguishing it from another project created in the same procedure.
- Write `information about X`, not `information on X`.

## Attribution

Parts of this reference are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified.
