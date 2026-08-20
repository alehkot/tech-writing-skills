# Task Documentation Patterns

## Use When

Load this reference for installation docs, setup guides, runbooks, API workflows, CLI instructions, tutorials, and troubleshooting procedures.

## Source Principles

- Task-first structure: users usually come to documentation to complete a job, not to admire feature coverage.
- Progressive disclosure: place prerequisites and concepts where they help, then keep steps focused.
- Concrete writing: examples, expected results, and visible verification points reduce ambiguity.
- Active voice and imperative steps: the reader should know what to do and who acts.
- Evidence discipline: partial notes are not permission to invent missing commands, locations, names, versions, permissions, or success output.

## Procedure Planning Questions

- Who is the reader and what can they already do?
- What environment, permissions, tools, versions, and accounts are required?
- What is the exact end state?
- What can go wrong, and how will the reader notice?
- Which actions are destructive, expensive, slow, or hard to undo?
- Which details are sourced, assumed, unknown, or unsafe to guess?

## Step Rules

- Title tasks by user goal and base-form action verb, such as `Find an address`, not by product UI or an `-ing` phrase, such as `Using the Address window`.
- Use one action per numbered step. The only permitted multi-action step is a menu path joined with `>`: `Click Project > Settings > Integrations`.
- Format a one-step procedure as a single bulleted sentence, never as a numbered list of one.
- Label sub-steps with lowercase letters (a, b, c) and deeper levels with lowercase Roman numerals; end a step that introduces sub-steps with a colon or a period.
- Order the parts of a complex step: the action, then the command, then placeholder definitions, then extra detail, then output, then the result as its own paragraph.
- State the action before its result or justification, in the same paragraph: `Click Deploy. The rollout status appears.`
- Name a dialog or screen as part of the step that produced it: `In the Add credential dialog that opens, click Continue.` Do not make its appearance a stand-alone result step.
- If a procedure grows beyond roughly nine steps, split it into smaller tasks, phases, or subtasks.
- Use `To [goal], [action]` when the reason for an action is not obvious. When that form could read as optional, switch to the colon form: `Rotate the signing key: click Rotate.`
- Start with the condition when a step applies only sometimes.
- Start optional steps with `Optional:`.
- State the location before the action, such as `In the project root, run ...` or `In the console, select ...`.
- Restate the acting context in the first step under each new heading, even when the context has not changed.
- Avoid directional cues such as `above`, `below`, `left`, or `right`; use named UI areas, headings, file paths, or controls instead.
- Put warnings before the action.
- Never put required information in a note: prerequisites and earlier-step reminders go before the step, procedural actions go in the numbered steps, and expected results stay in flow with their step. Never use a note as a cross-reference wrapper. The full notice severity taxonomy is canonical in docs-style-editor.
- Introduce commands by what they accomplish, never with `run the following command`: `Deploy the load generator:`.
- Fold pressing Enter into the step it completes; do not make it its own step.
- Instruct through named UI actions, not keyboard shortcuts: `Paste the connection string into the field`, not `Press Command+V`.
- Document exactly one way to complete a task: the keyboard-accessible, shortest path your audience knows. Put unavoidable alternatives under separate headings or tabs, never inline.
- Link to an already-documented procedure instead of repeating its steps.
- Use bullets only for choices, notes, or examples inside a step.
- Keep bullets and substeps parallel: do not mix commands, explanations, and outcomes at the same level.
- Use one term for each control, file, service, or role; define acronyms and placeholders before use.
- Keep conceptual explanations outside the numbered flow unless they prevent immediate reader error.
- Prefer "Verify that..." steps over vague "Make sure..." language.

## UI Writing

- Bold the exact visible label of every UI element you name. Add code font only when the label is itself a code value; then use both.
- Reproduce label capitalization as shown on screen, except use sentence case when a label is all-caps or labels are inconsistently cased.
- Never use a UI label as a verb or bare noun. Pair the label with an element noun and an action verb: `click Save` and `in the Name field, enter ...`, not `Save the settings` or `Name the account`.
- Use one standard verb per interaction and keep it consistent: click for mouse targets (never `click on`), tap for touch, press for keys, enter for text input, select and clear for checkboxes and options, drag, turn on and turn off. Reserve `type` for characters the reader must literally type, because text can also be pasted or dictated.
- Do not write `hit`. Prefer `select` and `clear` over `check` and `uncheck` for checkboxes and options. Do not write `hover`; write `hold the pointer over`. Do not write `please` in instructions.
- Describe checkbox state as `selected` or `not selected`.
- Name elements with their type word and do not swap these terms within a doc: dialog (not pop-up), page, pane, section, tab, menu, toolbar, list, field or box, toggle.
- Do not use toggle as a verb; state the action and the end position: `click the Backups toggle to the on position`.
- Drop a trailing ellipsis when quoting a button or menu label: `click Browse`, not `click Browse ...`.
- Refer to an icon-only control by its tooltip or accessible name, never as `the icon`. If the source supplies no accessible name, flag it as an open question; never invent one.
- Format keyboard shortcuts as a spelled-out modifier plus an uppercase key, with the macOS variant in parentheses: `Control+S (Command+S on macOS)`. Use press for shortcuts and enter for text input.
- Use `in` with dialogs, fields, lists, menus, panes, and windows; use `on` with pages, tabs, and toolbars.
- Prefer stating the reader's goal over widget-by-widget mechanics when the UI is obvious: `Refresh the page`, not a click sequence.
- Avoid copy-and-paste mechanics; state what to enter in the field, not how to move the text.

## Code and Command Rules

- Use fenced code blocks with language hints.
- Keep syntax characters such as `[ ]`, `{ }`, `|`, and `...` out of any block the reader is meant to copy and run. Give a runnable common-case command, and handle variants in separate blocks, separate task sections, or with an explicit warning to remove the syntax characters before running.
- Break commands longer than 80 characters with a trailing continuation character on every non-final line (backslash for POSIX shells, caret for Windows) and consistent indentation. Verify that the wrapped form runs identically; if you cannot verify it, leave the line long and say so instead of guessing.
- Never break a line inside a URL or a path; keep such literals intact, on their own line if needed.
- In a block with multiple input lines, show the prompt symbol on every input line. Never show a directory in the prompt. Switch to a distinct prompt indicator when the execution context changes, such as local to remote.
- Put command input and command output in separate code blocks; never interleave them.
- Introduce shown output with one fixed lead-in sentence that marks it as illustrative, such as `The output resembles the following:`, and reuse that same lead-in across the doc set. Show output only when the reader copies a value from it or verifies against it.
- Mark omitted output lines with three unspaced dots (`...`) alone on their own line. Mark omitted code with a comment in the sample's own language, such as `# lines omitted`.
- Never present a block that contains an omission as copy-and-run.
- In procedures, document only the arguments the task needs; link to the command reference for the rest.
- Never invent flags, argument values, prompts, or output lines the source does not supply; mark them as open questions.
- Do not mix commands for different operating systems in one block.
- For API examples, show the minimum request and one representative response.
- Introduce any file listing with a sentence that names the file before showing its contents: `In the following build.sh file, ...`.
- Follow a specific filename with the word `file`, and reproduce the filename exactly as it exists in the source, even when it breaks naming conventions.
- Refer to file types by their formal type name, not their extension: `a PNG file`, not `a .png file`.
- Use `extract`, not `unzip`, as the verb for unpacking archives. The full code-font taxonomy is canonical in docs-style-editor.

## Placeholder Rules

- Use exactly one placeholder convention across the doc set. The house form is lowercase `<angle-bracket>` names such as `<cluster-name>`, a deliberate divergence from ALL_CAPS conventions; when the target doc set already uses another convention, follow that convention consistently instead.
- Give every placeholder an informative name; never `x`, `xxx`, or `foo`-style names, except where an x-pattern is the domain's established notation, such as HTTP `Nxx` status classes.
- Do not build possessives such as `my-` or `your-` into placeholder names.
- Keep optionality markers (brackets, braces, ellipses) outside the placeholder token itself.
- Define each placeholder near the command it appears in. After a command with one placeholder, write `Replace <placeholder> with ...`. With several, write `Replace the following:` and list each placeholder in order of appearance with a short description.
- When example output contains values that vary, mark them as placeholders and list them after the output, introduced with a fixed phrase such as `This output includes the following values:`, in order of appearance.
- Describe what each placeholder represents from the source material only. If the source does not state a value's meaning or valid range, mark it as an open question rather than inventing a description.

## Provide the Why

If a fact appears inside a task topic, state its practical impact on the user's task.

- Weak: `The file must be under 10 MB.`
- Better: `To avoid an upload failure, keep the file under 10 MB.`

Avoid background theory in steps; link to a concept topic when the explanation is broader than the immediate task.

## Review Checklist

- Reader and outcome are clear.
- Prerequisites appear before steps.
- The first step can be performed from the stated starting state.
- Steps are chronological.
- Single-step procedures are one bulleted sentence, and multi-action steps appear only as `>` menu paths.
- Optional paths are labeled.
- Important facts explain why they matter to the task.
- Named UI elements are bold, match their visible labels, and use the standard interaction verbs.
- Copyable command blocks are runnable as shown: no syntax characters, no interleaved output, no omission presented as complete.
- Terms and placeholders are defined once and used consistently, under one placeholder convention.
- No prerequisite, required action, or expected result sits inside a note.
- Lists and substeps are parallel.
- The procedure includes a verification section.
- Unknown prerequisites, values, paths, and success signals are labeled as assumptions, open questions, or verification gaps.
- Troubleshooting maps symptoms to likely causes and next actions.
- No unsupported claims, hidden prerequisites, or unexplained acronyms remain.

## Attribution

Parts of this reference are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified.
