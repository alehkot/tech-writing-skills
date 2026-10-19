# Accessibility Checklist

## Contents

- [Use When](#use-when)
- [Alt Text Rules](#alt-text-rules)
- [Repeated-Icon Review Cases](#repeated-icon-review-cases)
- [Information Parity](#information-parity)
- [Media Alternatives](#media-alternatives)
- [Media Review Cases](#media-review-cases)
- [Color and Position Independence](#color-and-position-independence)
- [Screen-Reader-Safe Prose](#screen-reader-safe-prose)
- [Verification Passes](#verification-passes)
- [Audit Pointers](#audit-pointers)
- [HTML Outputs Appendix](#html-outputs-appendix)
  - [Menu Path Review Cases](#menu-path-review-cases)
  - [Table Header Review Cases](#table-header-review-cases)
- [Attribution](#attribution)

## Use When

Load this reference before checking alt text, media alternatives, visual-cue independence, or screen-reader-safe prose during an accessibility and inclusion review.

## Alt Text Rules

- Give every informative image alt text: a noun phrase or a full sentence, roughly 155 characters or fewer, with end punctuation so screen readers pause after it.
- Tune alt text to the image's role in the surrounding context, not only to its content. A chart cited for one trend gets alt text about that trend, not an inventory of every series.
- Never start alt text with `Image of`, `Picture of`, or a similar frame, and never write alt text in all caps.
- Give purely decorative or fully text-redundant images empty alt text so assistive technology skips them. For an image inside a link or control, do this only when the supplied context confirms the link or control remains named; do not remove its only text alternative.
- Reuse identical alt text for repeated icons and indicators only when their meaning, function, and context match. For a different supplied action, destination, or meaning, adapt the alternative rather than copying a label based on appearance. Flag an unknown purpose instead of guessing.
- Move explanations longer than the alt-text budget into body text as a figure description. A caption never substitutes for alt text.
- If the source does not say what an image shows, mark the description as unverified instead of narrating plausible content.

Avoid: `IMAGE OF THE DASHBOARD` Prefer: `Dashboard with the ingest queue paused and two workers idle.`

### Repeated-Icon Review Cases

Use these cases to check the review decision against the supplied context. They concern images in documentation, not an application UI audit.

- **Same meaning:** Two standalone status icons both mean `Upload complete.` and neither duplicates nearby text. Keep the same alternative for both.
- **Different destinations:** The same arrow image is the only content of two links, one documented as opening installation instructions and the other as opening upgrade instructions. Use `Installation instructions.` and `Upgrade instructions.` rather than one generic arrow description.
- **Redundant occurrence:** A logo alone links to the documented Acme documentation home page; another occurrence sits inside a link already named `Acme documentation home`. Give the first a destination alternative and the second empty alt text only if the supplied context confirms the link text provides its name. Do not infer redundancy from text outside the link.
- **Additional information:** An icon next to link text indicates a documented PDF format that the text does not mention. Preserve that information in the alternative; accompanying text alone does not make an image redundant.
- **Unknown purpose or name:** If an icon's action or destination is not supplied, flag it for human verification. Do not invent a label or erase an existing alternative merely because the icon repeats elsewhere.

In each case, keep supplied destinations, facts, literal identifiers, and existing UI labels unchanged. These are review examples, not evidence of screen-reader testing or WCAG conformance.

See the [W3C WAI Functional Images tutorial](https://www.w3.org/WAI/tutorials/images/functional/) for the distinction between image-only links and images that supplement an already-named link.

## Information Parity

- Put nothing only in an image: state in body text everything the image conveys, so the image is never the sole carrier of information.
- Never present text, code, configuration, or terminal output as a screenshot; present it as real, selectable, copyable text.
- Select media alternatives by the information channel using the following media pass; a transcript and synchronized captions serve different uses. Keep text alternatives translatable.
- Never use flashing or flickering content, and never rely on an animation as the only way to convey information.

## Media Alternatives

For each asset, establish whether it is audio-only, video without meaningful audio, or video with meaningful audio, and whether it is recorded or live. Use supplied content and alternatives as evidence; an attachment name or a claimed caption track does not establish coverage or accuracy. This is a documentation review, not media-player testing or a WCAG conformance assessment.

- **Recorded audio-only:** Check for a discoverable transcript covering speech, speaker changes where needed, and meaningful sounds. Do not require video captions for an audio-only asset.
- **Recorded video with meaningful audio:** Check for synchronized captions covering speech and meaningful sounds. A separate plain transcript does not replace captions for following the video. Also check the visual information independently: actions, results, or on-screen text absent from the soundtrack need description. Flag gaps in supplied narration/audio description and in any descriptive transcript; captions of speech alone do not establish visual coverage.
- **Video without meaningful audio:** Check for an equivalent description of the meaningful visual sequence, in text or an audio track. Do not request captions for nonexistent audio or background sound that carries no relevant information. Preserve the existing no-image text-parity rule when the sequence carries documentation facts.
- **Already described or redundant content:** Do not demand a separate narration track when the supplied soundtrack already explains all relevant visuals. If media is explicitly labeled as an alternative to equivalent text, record that relationship and verify equivalence before applying an exception. Do not infer equivalence from a nearby summary.
- **Live or unknown:** Flag the need for an appropriate live-media accessibility review; a transcript promised after the event does not provide access during it. If the source or timing is unavailable, report what cannot be checked rather than inventing dialogue, sounds, visual actions, or timestamps.

Check auto-generated captions against supplied evidence, especially negation, quantities, technical terms, and meaningful sounds. Their presence alone is not proof of accuracy. Keep captions, transcripts, and visual descriptions distinct in findings and identify the evidence used.

### Media Review Cases

These original decision cases do not establish media playback behavior or conformance:

- **Transcript is not captions:** A recorded narrated demonstration supplies a correct plain transcript but no synchronized captions. Report the caption gap; do not mark synchronized access complete.
- **Unspoken result:** Captions reproduce `Wait for completion.` while supplied video notes show `Upload failed` without narration. Flag the missing visual result; preserve `Upload failed` exactly.
- **Silent sequence:** A silent setup clip has a complete accompanying text procedure describing every demonstrated action and result. Do not invent a need for speech captions; check the description against the sequence.
- **Audio-only control:** A podcast has an accurate, accessible transcript with speakers and relevant sounds. Do not add a video-caption requirement.
- **Narration control:** A supplied soundtrack already describes every relevant visual. Do not require duplicate audio description merely because no separate track exists.
- **Unchecked automation:** Only a filename `captions.vtt` is supplied. Report caption accuracy and synchronization as unverified; do not claim either passed.
- **Live timing:** A live walkthrough promises a transcript tomorrow. Flag the unresolved live-access need rather than treating the future transcript as current access.

Basis: W3C WAI guidance on [captions](https://www.w3.org/WAI/media/av/captions/), [transcripts](https://www.w3.org/WAI/media/av/transcripts/), and [visual description](https://www.w3.org/WAI/media/av/description/). Use the applicable standard and project requirements for formal assessment.

## Color and Position Independence

- Never rely on color, size, shape, or position as the sole channel for state or meaning; pair every visual cue with a textual one.
- Name the state, not only its rendering. Avoid: `Retry the steps shown in red.` Prefer: `Retry the steps marked Failed, which appear in red.`
- Point within a document with `earlier`, `preceding`, `following`, or a named section — never `above`, `below`, or `the right-hand side` (canonical rules: docs-style-editor word-choice). Avoid: `Use the table above.` Prefer: `Use the preceding table.` or `Use the table in the section named Limits.`
- Do not describe UI locations directionally; refer to controls by their visible label or accessible name (canonical rules: task-docs-writer).

## Screen-Reader-Safe Prose

When the write-simplified-technical-english skill is also active, its stricter sentence and structure rules take precedence over these checks.

- The meaning must survive with all punctuation stripped; read each sentence without punctuation as a check.
- Give each instruction its own list item; never chain unrelated steps inside one paragraph. A documented menu sequence may stay together under the task-docs-writer menu-path exception, with its order explicit in text or a verified accessible house format.
- State abilities positively, and avoid double negatives and exceptions to exceptions (canonical rules: docs-style-editor grammar-and-usage).

Run the following punctuation and casing checks as well, but report each hit against its canonical home instead of re-deciding the rule:

- A semicolon that pushes two clauses into one long spoken sentence. Prefer a period. Outside STE, keep a semicolon only between tightly coupled independent clauses, before a connective such as `therefore` or `that is`, or between series items that contain commas. These exceptions apply here even when docs-style-editor is not installed; report the finding under that canonical punctuation category. STE allows no semicolons.
- An exclamation mark in technical prose (canonical home docs-style-editor word-choice).
- An `&` written for `and` in prose or headings; an ampersand is acceptable only when it mirrors a UI label or sits in a space-constrained table (canonical home docs-style-editor formatting-mechanics).
- An all-caps word or an invented camel-case coinage, which a screen reader may spell out letter by letter; reproduce literal identifiers exactly regardless (canonical home docs-style-editor formatting-mechanics).
- A forced line break inside a sentence or paragraph; start a new paragraph or list item instead (canonical home docs-style-editor formatting-mechanics).

## Verification Passes

Run every pass and record the evidence and outcome: checked with no gap found, gap found, unverified, or not applicable. A document-only review must not imply playback or assistive-technology testing:

- No-image pass: with images ignored, all information is still present in text.
- No-color pass: with color ignored, every state and cue is still distinguishable.
- No-sound pass: check audio information against the appropriate text alternative; for video with meaningful audio, separately verify caption coverage and synchronization when evidence permits.
- No-visuals pass: check meaningful video information against supplied narration/description or descriptive text, preserving the media distinctions above.
- Keyboard-only pass: every documented interaction is described in a way a keyboard-only reader can follow, or the gap is flagged.
- No-punctuation pass: sentences keep their meaning with punctuation stripped.

## Audit Pointers

Run these checks during the review, but report violations against their canonical home, where the full rules live:

- Descriptive link text that makes sense out of context, and disclosure of unexpected link behavior: canonical home docs-style-editor.
- Heading hierarchy without skipped levels, and unique, descriptive, non-empty headings: canonical home docs-style-editor.
- Referring to UI elements by their visible label or accessible name, and flagging icon controls that have neither: canonical home task-docs-writer.
- Introducing each table in the preceding text, preferring simple tables without introducing merged cells, and preserving header-to-data relationships when recommending restructuring: canonical home docs-style-editor.
- The punctuation and casing checks listed under Screen-Reader-Safe Prose: canonical home docs-style-editor.

## HTML Outputs Appendix

Apply this section only when the deliverable's output format is HTML. Skip it for Markdown, plain text, and any other format; the rest of this checklist is format-agnostic.

- Use each element for its semantic purpose: real heading elements for headings, never styled text as a fake heading and never a heading element chosen for its visual size.
- Use `em` only for genuine emphasis and `strong` only for strong importance; use `i` and `b` for italics and bold that carry no emphasis semantics.
- Do not use `br` to fake paragraph spacing; `br` is only for breaks that are part of the content, and spacing belongs to CSS.
- Prefer native interactive elements, and keep the DOM order matching the reading order.
- Give every form input a `label` element.
- Identify table headers by what they label, not by their position or styling. Use `th` for actual row and column headers, including row headers in a later column; use `td` for data. For simple row and column relationships, use the corresponding `scope="row"` or `scope="col"` on the header cells.
- Preserve valid existing header associations. For a supplied complex table, check explicit associations against the supplied relationships: `headers` values refer to document-unique `id` values on header cells in the same table. Do not invent associations from visual placement alone or remove meaningful header markup to satisfy a simple-table preference. Flag unknown relationships or uncheckable rendered behavior.
- Recommend simpler tables under the canonical docs-style-editor table rules when applicable. Restructuring is separate from a mechanical or findings-only review; preserve every cell value, header label, unit, and relationship, and flag any simplification whose equivalence cannot be established.
- Express a documented menu sequence in real text, for example `Select Project, then Settings, then Integrations.`, preserving the supplied labels and their order. A menu path is the task-docs-writer exception to the one-action-per-step rule, whether its separators are words or symbols. Do not rely on a screen reader pronouncing `>` to convey the sequence.
- Do not add `aria-label` or `aria-labelledby` to a generic separator `span` to replace its pronunciation: generic elements prohibit naming. Do not add an unrelated role or make punctuation focusable to force a name. Prefer visible connecting words, or split the sequence into separate steps when needed.
- If a documented, tested house component already supplies equivalent accessible text for a symbolic path, preserve it. If its implementation or rendered behavior is unavailable, flag that verification gap rather than promising how it will be announced. Do not silently rewrite literal HTML examples, command operators, or a `>` that is part of a UI label.

### Menu Path Review Cases

These original cases test editorial decisions against supplied evidence, not browser or screen-reader behavior. They do not establish WCAG conformance.

| Supplied context | Expected review decision | Failure to reject |
| --- | --- | --- |
| HTML prose documents the menu sequence Project, Settings, Integrations using bare `>` separators. | Use visible connecting words, keeping all three supplied labels in order, or separate steps. | Depending on punctuation pronunciation to carry the sequence. |
| A generic `span` around each separator has `aria-label="and then"`. | Flag the prohibited naming and prefer real connecting text in the documentation revision. | Marking it accessible merely because an ARIA attribute exists. |
| A proposed repair gives the separator a button role or a tab stop. | Reject the invented interaction and use ordinary text. | Making punctuation interactive to obtain a spoken name. |
| A supplied, tested house component already exposes equivalent connecting text and preserves each label. | Preserve it; do not duplicate its text or rewrite it solely because the visual separator is `>`. | Requiring a second spoken connector without inspecting the existing alternative. |
| Only the rendered screenshot or component name is supplied. | Flag announcement behavior as unverified; suggest a text sequence without claiming the component failed testing. | Inferring accessible behavior from appearance or a component name. |
| A command contains `output > file`, or the supplied UI label is `Size > 10`. | Preserve the literal operator or full label; the separator rule concerns menu-path prose. | Replacing every greater-than character globally. |
| A Markdown guide contains a menu path, or a code fence quotes the problematic HTML verbatim. | Do not inject HTML/ARIA into Markdown or alter quoted code; propose plain-language prose or flag the example separately. | Applying the HTML appendix outside its scope or silently changing source literals. |

Basis: [W3C ARIA in HTML naming requirements](https://www.w3.org/TR/html-aria/#requirements-for-use-of-aria-attributes-to-name-elements) and [ARIA naming guidance](https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/). This deliberately replaces the generic-span naming pattern in the adapted Google guidance with ordinary text; no particular assistive-technology announcement is guaranteed.

### Table Header Review Cases

These original decision cases check instruction coverage for HTML documentation. They are not browser or screen-reader tests and do not establish WCAG conformance.

| Supplied context | Expected review decision | Failure to reject |
| --- | --- | --- |
| A simple table has column labels in its first row and row labels in its first column. | Keep semantic headers and their matching row/column scope. | Replacing headers with styled data cells. |
| Column one contains ordinal numbers; column two contains the supplied row labels. | Keep the second-column labels as `th` with row scope; leave the ordinal values as data. | Removing header semantics because the labels are outside column one. |
| A first-row cell is a data value, even though it is bold. | Keep it a data cell; identify headers from the supplied meaning. | Making every first-row or bold cell a header. |
| An existing multi-level table supplies valid header IDs and associations; only a copyedit was requested. | Preserve those associations and report any simplification recommendation separately. | Dropping a group label or association to flatten the table during copyediting. |
| A proposed split would lose which unit or group applies to a value. | Flag the unresolved relationship and do not apply the split. | Keeping the numbers but changing what they measure or which group owns them. |
| The source does not establish which header labels a data cell. | Report that association as unverified. | Guessing from proximity or claiming the table passed. |
| The deliverable is Markdown, or HTML appears only as a literal code example. | Skip the HTML appendix for Markdown; preserve literal example code and flag concerns separately. | Injecting HTML into Markdown or silently rewriting a quoted HTML example. |

Basis: W3C WAI guidance on [two-header tables, including offset row headers](https://www.w3.org/WAI/tutorials/tables/two-headers/) and [multi-level header associations and simpler alternatives](https://www.w3.org/WAI/tutorials/tables/multi-level/). Apply the documentation review's existing evidence and literal-preservation boundaries.

## Attribution

Parts of this reference are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified.
