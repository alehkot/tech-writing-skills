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
- Use one action per numbered step.
- If a procedure grows beyond roughly nine steps, split it into smaller tasks, phases, or subtasks.
- Use `To [goal], [action]` when the reason for an action is not obvious.
- Start with the condition when a step applies only sometimes.
- Start optional steps with `Optional:`.
- State the location before the action, such as `In the project root, run ...` or `In the console, select ...`.
- Avoid directional cues such as `above`, `below`, `left`, or `right`; use named UI areas, headings, file paths, or controls instead.
- Put warnings before the action.
- Use bullets only for choices, notes, or examples inside a step.
- Keep bullets and substeps parallel: do not mix commands, explanations, and outcomes at the same level.
- Use one term for each control, file, service, or role; define acronyms and placeholders before use.
- Keep conceptual explanations outside the numbered flow unless they prevent immediate reader error.
- Prefer "Verify that..." steps over vague "Make sure..." language.

## Code and Command Rules

- Use fenced code blocks with language hints.
- Use clear placeholders such as `<cluster-name>` and define them near the command.
- Include expected output when output is short and diagnostic.
- Do not mix commands for different operating systems in one block.
- For API examples, show the minimum request and one representative response.

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
- Optional paths are labeled.
- Important facts explain why they matter to the task.
- Terms and placeholders are defined once and used consistently.
- Lists and substeps are parallel.
- The procedure includes a verification section.
- Unknown prerequisites, values, paths, and success signals are labeled as assumptions, open questions, or verification gaps.
- Troubleshooting maps symptoms to likely causes and next actions.
- No unsupported claims, hidden prerequisites, or unexplained acronyms remain.
