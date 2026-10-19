# Task Documentation Patterns

## Contents

- [Use When](#use-when)
- [Source Principles](#source-principles)
- [Procedure Planning Questions](#procedure-planning-questions)
- [Tutorials and How-To Guides](#tutorials-and-how-to-guides)
- [Step Rules](#step-rules)
- [Action-Timing Review Cases](#action-timing-review-cases)
- [UI Writing](#ui-writing)
- [Code and Command Rules](#code-and-command-rules)
- [Placeholder Rules](#placeholder-rules)
- [Provide the Why](#provide-the-why)
- [Copyable Example Review Cases](#copyable-example-review-cases)
  - [Line-Wrapping Review Cases](#line-wrapping-review-cases)
- [Review Checklist](#review-checklist)
- [Attribution](#attribution)


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

## Tutorials and How-To Guides

Keep both forms within task documentation, but plan them for different reader needs:

- For a tutorial, name the small working result the learner will create. Choose a supported exercise path, resolve incidental choices from the source, and place an observable checkpoint early and after later milestones. Keep only the explanation needed to perform the next action; link broader background separately. Mark missing setup or checkpoint evidence instead of inventing it.
- For a how-to guide, state the practical end state and assume the stated prerequisites. Keep conditions that change the required action, such as renewing an expired credential before deployment. Give each branch a decision criterion before its action. Separate alternative methods, and omit practice exercises or background lessons that do not help finish the job.
- When the request leaves the form unclear, use the reader's goal and experience to choose it and state the assumption. Split a request for both forms into separately named topics.

## Step Rules

- Title tasks by user goal and base-form action verb, such as `Find an address`, not by product UI or an `-ing` phrase, such as `Using the Address window`.
- Use one primary action per numbered step. Preserve source-required overlap: keep tightly coupled simultaneous actions together with explicit wording such as `while holding`. For state that must persist across several steps, separate the primary actions while explicitly carrying that state through each dependent step (for example, `keep ... active until ...`). Preserve supplied start, stop, and release conditions; do not invent durations, release points, or a sequential substitute. If timing is unclear, retain the source wording and flag the gap.
- A documented menu sequence may share a step, for example: Select **Project**, then **Settings**, then **Integrations**. Keep supplied labels and order. Use connecting words or a verified accessible house menu-path format rather than relying on how `>` is pronounced. Along with Enter completing an input below, these are bounded grouping rules, not permission to combine unrelated setup, execution, or verification actions.
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
- Prefer named UI actions over optional keyboard shortcuts: `Paste the connection string into the field`, not `Press Command+V`. Preserve a source-required key, button hold, or chord when it defines the action; do not replace it with an unsupported UI method or drop the required overlap.
- Choose one recommended, keyboard-accessible method that fits the reader. Preserve necessary conditional actions within that method; put competing methods under separate headings or tabs.
- Link to an already-documented procedure instead of repeating its steps.
- Use bullets only for choices, notes, or examples inside a step.
- Keep bullets and substeps parallel: do not mix commands, explanations, and outcomes at the same level.
- Use one term for each control, file, service, or role; define acronyms and placeholders before use.
- Keep conceptual explanations outside the numbered flow unless they prevent immediate reader error.
- Prefer "Verify that..." steps over vague "Make sure..." language.

## Action-Timing Review Cases

These original editorial cases check instruction consistency and source preservation,
not measured model performance or execution in a real product. Each row supplies
its own task facts; do not infer the same behavior for another application.

| Supplied source and context | Expected decision | Rewrite to reject |
| --- | --- | --- |
| In the file list, select the first file, then hold Shift while selecting the last file. | Keep the initial selection before the sustained Shift-and-selection action; state that Shift stays held during the last selection. | Press Shift, release it, then select the last file; or omit Shift. |
| In the canvas, hold the constraint key throughout the drag and release it after releasing the pointer button. | Keep the hold active through the drag and preserve the supplied release order. | Split into isolated press/drag steps that lose the hold, or release the key before the pointer button. |
| Press the two named buttons at the same time; no duration is supplied. | Keep simultaneity explicit without inventing a hold duration. | Press one button and then the other, or hold them for five seconds. |
| Keep the preview running while changing the setting; stop it after the new value appears. | Preserve the running state through the change and the supplied stop condition. | Stop the preview before changing the setting. |
| Keep the preview running while configuring access, starting the job, and checking its output; stop it after the check. | Separate the distinct actions while explicitly keeping the preview active through each; preserve the supplied stop point. | Force every action into one oversized step, or stop the preview between dependent steps. |
| Select Project, then Settings, then Integrations. | A single documented menu sequence remains allowed, with textual order and exact labels. | Reorder the selections or mark the sequence simultaneous. |
| Enter the supplied search text and press Enter to submit it. | Keep Enter with the input it completes, without adding unsupported navigation. | Forbid this grouping under a menu-only exception or invent an extra confirmation click. |
| Create the workspace, configure access, then run validation; no overlap is specified. | Keep the distinct actions in order as separate steps. | Combine them merely to shorten the procedure, or invent concurrent execution. |
| The notes say to hold a key and select an item but do not establish whether the hold must continue during selection. | Preserve the wording and flag the timing question. | Invent either a release point or a required overlap. |

[Google's procedure guidance](https://developers.google.com/style/procedures)
provides the one-action default and the menu-sequence and input-completion
patterns. The source-preservation rule here also keeps necessary overlap explicit;
formatting must not change how a documented interaction works.
[Microsoft's procedure checklist](https://learn.microsoft.com/en-us/style-guide/checklists/procedures-and-instructions-checklist)
uses a modifier held during a click, and [Apple's selection documentation](https://support.apple.com/guide/mac-help/select-items-mchlp1378/mac)
documents held modifiers for selecting items. These are examples of timing that
must survive a writing or accessibility pass, not universal key mappings.

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
- Separate command-synopsis notation from executable syntax. Optional-argument markers (`[--verbose]`), choice groups (`{--json|--yaml}`), and repetition markers (`<file>...`) belong in a labeled syntax block, not a copy-and-run example. Select a source-supported invocation for the task or show alternatives separately; do not tell readers to delete punctuation indiscriminately. Preserve characters that are part of the actual language or data, including shell pipes, test brackets, variable-expansion braces, JSON objects and arrays, and literal strings containing `...`.
- Aim for command lines of 80 characters or fewer only when wrapping preserves behavior. Identify the actual shell and version from the source; an operating-system label such as Windows does not identify the shell. If the shell or safe wrapping is unverified, keep the original line and flag the verification gap.
- Use that shell's syntax at valid break points, not a continuation character on every non-final line. Bash supports backslash-newline outside single-quoted strings; PowerShell supports natural syntax breaks and backtick continuation, not the caret used by cmd.exe. Prefer natural breaks where supported. Keep explicit continuation characters immediately before the newline, with no trailing spaces. Preserve quoting, argument boundaries, literal data, and existing meaningful newlines; verify the wrapped form behaves identically before presenting it as copyable. See the [shell comparison](https://learn.microsoft.com/en-us/cli/azure/get-started-tutorial-2-environment-syntax?view=azure-cli-latest#be-aware-of-line-continuation-characters), [Bash escaping rules](https://www.gnu.org/s/bash/manual/html_node/Escape-Character.html) and [PowerShell parsing guidance](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_parsing?view=powershell-7.5#line-continuation).
- Never break a line inside a URL or a path; keep such literals intact, on their own line if needed.
- Omit prompt prefixes from copyable command blocks, including multi-command blocks. State the shell, working directory, and local or remote context in prose before the block. If prompts are needed to illustrate an interactive session, label it as a transcript rather than a copy-and-run block, or verify that the rendered copy action excludes every prompt. Do not strip meaningful `$` characters from variables or other executable syntax.
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

## Copyable Example Review Cases

Use these cases to check the distinction when reviewing a draft. They are editorial
checks, not evidence that a model followed the skill or that an example was run.
Only claim execution when the relevant command was actually tested.

| Supplied example and context | Expected decision |
| --- | --- |
| POSIX shell command: `printf '%s\n' ready \| tr a-z A-Z` | Preserve the pipe; it connects two commands and is not a choice marker. |
| JSON body: `{"labels":["docs"],"message":"Waiting..."}` | Preserve the braces, brackets, and dots; they are data syntax and string content. |
| POSIX shell command: `[ -n "${HOME}" ]` | Preserve test brackets, variable expansion, and quoting. |
| Declared synopsis: `acme list [--verbose] {--json\|--yaml} <file>...` | Keep it labeled as syntax. Give a separate sourced invocation for copying; do not guess an option or filename. |
| Two input commands prefixed with `$ ` | Remove only the prompt prefixes in the copyable version; preserve commands and line boundaries. Label a retained prompt-bearing version as a transcript. |
| A command containing `<project-id>` | Define the placeholder and require replacement before execution. Do not claim it runs unchanged or invent a real project identifier. |
| A sample containing an omitted-code comment | Keep it labeled as abbreviated; do not fabricate the missing code or present it as complete. |

### Line-Wrapping Review Cases

Apply the same editorial-check limitation above; these cases do not establish execution or model behavior.

| Supplied example and context | Expected decision |
| --- | --- |
| A long command labeled only `Windows` | Preserve it and flag the missing shell; do not infer cmd.exe or insert carets. |
| A long PowerShell command on Windows or Linux | Use verified PowerShell break points or backtick continuation; never select caret or backslash from the operating system. |
| A long Bash command running on Windows | Use verified Bash syntax; the operating system does not change the shell's continuation rules. |
| A quoted argument contains a long URL or literal text | Keep the value and quoting intact; do not insert a newline inside it to reach 80 columns. |
| A supplied multi-line command already uses valid natural breaks | Preserve them; do not append continuation characters mechanically to every line. |
| The target shell or a safe equivalence check is unavailable | Leave the original long line and state the verification gap; do not claim a wrapped form was tested. |

## Review Checklist

- Reader and outcome are clear.
- Prerequisites appear before steps.
- The first step can be performed from the stated starting state.
- Steps are chronological.
- Single-step procedures are one bulleted sentence. Grouped actions preserve required overlap or sustained state, explicit menu order, or Enter completing its input; unrelated actions stay separate.
- Optional paths are labeled.
- Important facts explain why they matter to the task.
- Named UI elements are bold, match their visible labels, and use the standard interaction verbs.
- Copyable command blocks preserve executable syntax and separate any required placeholder replacements from claims of running unchanged; no unresolved synopsis notation, copied prompt prefixes, interleaved output, or omission is presented as a complete command.
- Line wrapping follows the documented shell, preserves arguments and literals, and is verified or left unchanged with a gap noted.
- Terms and placeholders are defined once and used consistently, under one placeholder convention.
- No prerequisite, required action, or expected result sits inside a note.
- Lists and substeps are parallel.
- The procedure includes a verification section.
- Unknown prerequisites, values, paths, and success signals are labeled as assumptions, open questions, or verification gaps.
- Troubleshooting maps symptoms to likely causes and next actions.
- No unsupported claims, hidden prerequisites, or unexplained acronyms remain.

## Attribution

Parts of this reference are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified.
