---
name: task-docs-writer
description: >-
  Task documentation writing for task topics and task-oriented engineering documentation where readers must complete an action: installation guides, setup docs, runbooks, tutorials, operational procedures, API workflows, CLI instructions, and troubleshooting steps. Use for transforming feature descriptions or messy notes into clear prerequisites, ordered steps, checks, and recovery guidance.
  Use when missing prerequisites, commands, permissions, versions, or success signals must be labeled rather than invented.
metadata:
  version: "1.3.1"
  risk_tier: low
---

# Task Docs Writer

## Overview

Turn technical workflows into task topics that let a reader complete a task with minimal interruption. Optimize for task-first structure, concrete steps, reader context, and verifiable outcomes.

Read [references/task-docs-patterns.md](references/task-docs-patterns.md) when drafting a full procedure, revising a messy guide, or checking a document before handoff.

## Plan From Evidence

Before drafting, extract the supplied or independently verified actions and pair each with its documented result. Keep unsupported actions and outcomes in a gap list instead of the procedure. Do not add a conventional next step or alternative method merely because it usually accompanies this kind of task.

For each check with named states, map every supplied state to its next action, recheck, or stop condition. Include the ordinary continuation state explicitly; documenting only the exception leaves the reader to infer when to proceed. Draft from this map, keeping the working notes out of the delivered procedure unless requested.

## Workflow

1. Identify the reader, task, starting state, target outcome, and environment. Distinguish a tutorial that builds experience through a guided exercise from a how-to guide that helps a practiced reader finish a job; apply the matching pattern in [references/task-docs-patterns.md](references/task-docs-patterns.md). If the source lacks required versions, permissions, credentials, or platform assumptions, mark them as assumptions or questions instead of inventing them.
2. Title and frame the task around the user's goal, not the product surface or internal feature name. Prefer a base-form action verb such as `Create`, `Configure`, or `Verify`; avoid `-ing` task titles such as `Creating`. Keep articles in titles and headings: `Create a VM instance`, never `Create VM instance`.
3. Separate task content from conceptual background. Keep long explanations before or after the procedure, not inside the steps.
4. Create the procedure in this order: purpose, prerequisites, before-you-start checks, steps, expected result, verification, rollback or troubleshooting. Choose one recommended, keyboard-accessible path that fits the audience. Keep tutorials on a supported exercise path; retain necessary condition-based branches in how-to guides and say how to choose. Put alternative methods under separate headings or tabs, and link to already-documented procedures instead of repeating their steps.
5. Start each action step with an imperative verb. Use one primary action per step; the only multi-action step is a menu path joined with `>`. Format a one-step procedure as a single bulleted sentence, never a numbered list of one. Put conditions first: `If you use Kubernetes, set ...`.
6. Provide the why when it changes user behavior. Use `To [goal], [action]` when a step's purpose is not obvious; switch to the colon form (`Rotate the signing key: click Rotate.`) when the `To ...` form could read as optional.
7. State location before action when the reader must act in a specific UI, file, directory, console, or service. Restate the acting context in the first step under each new heading, even when it is unchanged. Use named locations instead of directional cues such as `above`, `below`, or `right`.
8. When a step names a UI element, bold its exact visible label and use the standard interaction verbs: click, tap, press, enter (reserve type for characters the reader must literally type), select and clear, drag, turn on or turn off. Refer to an icon-only control by its tooltip or accessible name; if the source supplies none, flag it as an open question instead of inventing one. Apply the UI writing rules in [references/task-docs-patterns.md](references/task-docs-patterns.md).
9. Label optional work at the start of the sentence: `Optional: ...`.
10. Use one term consistently for each UI element, command, file, role, or system component. Define unfamiliar terms, acronyms, and placeholders before relying on them.
11. Make command examples copyable and adaptable. Introduce each command by what it accomplishes, never with `run the following command`. Use one placeholder convention across the doc set: the house form is lowercase `<angle-bracket>` names, and a target doc set's existing convention wins when one exists. Give placeholders informative names and define each near its command with `Replace <placeholder> with ...` or a `Replace the following:` list.
12. Keep lists and substeps parallel: same grammar, same level of detail, and no mixed choices/actions in one list.
13. Split procedures that grow beyond roughly nine steps into smaller tasks, phases, or subtasks.
14. Audit every action against a source ledger: supplied facts, assumptions, open questions, and omitted details that would affect execution. Include troubleshooting advice, recovery actions, escalation routes, and responsible roles in this audit. Preserve sourced stop conditions. Remove unsupported executable advice and flag the gap as an open question; a plausible diagnosis or an unknown error message does not justify an invented recovery action.
15. Add verification points where the reader can tell whether the step worked. State the action before its result, in the same paragraph: `Click Deploy. The rollout status appears.` Prefer observable signals: command output, status code, UI state, log line, or file path. If the source does not provide an exact signal, label the verification gap.

## Verification Handoff

Keep a complete draft separate from its review. Give the original request,
sources, and draft to the user- or project-specified reviewer or grader. Use
`technical-docs-reviewer` when available; no particular provider is required.
Prefer a fresh read-only reviewer when available and authorized. Otherwise run
the self-check explicitly and identify it as self-review if reporting the mode.
Do not claim that an unavailable requested grader ran.

Check each finding against the sources before repairing it. Preserve supported
actions and facts even if a reviewer proposes removing them. By default, allow
one repair and a final review of the complete revision; a caller's explicit
review budget takes precedence. Keep remaining material gaps visible. After a
style or unslop edit, recheck the final meaning, conditions, sequence, and literals.
Deliver the procedure and consequential gaps; include internal review records
only when requested.

## Completion Criterion

Complete the task only when the output gives the reader a usable procedure: every prerequisite, action, decision point, verification signal, and recovery path from the source is represented, labeled as an assumption, or called out as an open question; no command, UI path, permission, version, success output, or recovery action is invented; every applicable self-check item passes.

## Output Shape

Use this default structure unless the user or repo has an established template. Include troubleshooting actions only when the source supplies them; otherwise replace that section with the relevant open questions or verification gaps.

```markdown
# [Task name]

Use this procedure to [outcome].

## Prerequisites
- [Requirement]

## Steps
1. [Imperative action.]
2. [Imperative action.]

## Verify
- [Observable success signal]

## Troubleshoot
- If [symptom], [sourced diagnosis or recovery action; otherwise flag the gap].
```

## Self-Check

- [ ] The document names its intended reader and outcome.
- [ ] Tutorials name a concrete exercise outcome and provide early and subsequent checkpoints; how-to guides preserve necessary decisions without adding teaching detours.
- [ ] The title and opening are framed around the user's goal rather than the product surface, task headings use base-form action verbs, and headings keep their articles and use sentence case (canonical rules: docs-style-editor formatting-mechanics).
- [ ] Prerequisites are visible before the first step.
- [ ] Steps are chronological and do not hide decisions in paragraphs.
- [ ] The procedure uses `you` and active voice to describe what the reader does.
- [ ] Steps or facts that need rationale explain the practical why.
- [ ] Each step begins with an action verb or a clear condition.
- [ ] Single-step procedures are one bulleted sentence, and the only multi-action steps are `>` menu paths.
- [ ] Each step states the action before its result, and a dialog is named in the step that produced it.
- [ ] UI or file-location steps name the location before the action, and the first step under each heading restates the acting context.
- [ ] Named UI elements are bold, match their visible labels, and use the standard interaction verbs (click, tap, press, enter, select, clear).
- [ ] The guide avoids directional location cues that depend on page layout or visual position.
- [ ] Optional steps are explicitly labeled.
- [ ] Terms, acronyms, and placeholders are defined once and used consistently.
- [ ] Placeholders follow one convention across the doc set, and each is defined near its command or listed after the output it appears in.
- [ ] Commands are introduced by what they accomplish; copyable blocks contain no syntax characters, and input and output sit in separate blocks.
- [ ] No prerequisite, required action, or expected result hides in a note, and no note wraps a cross-reference.
- [ ] Steps contain no `please`, `simply`, `just`, or `easily` (canonical list: docs-style-editor word-choice).
- [ ] Example values use documentation-reserved data such as `example.com`, RFC 5737 IP ranges, and 800-555-01xx phone numbers (canonical table: docs-style-editor safe-example-values).
- [ ] Long procedures are split into manageable tasks, phases, or subtasks.
- [ ] Lists, choices, and substeps are parallel and concise.
- [ ] Code samples include language or shell fences, placeholders, and expected results where useful.
- [ ] The guide includes at least one verification path.
- [ ] Missing execution details are captured as assumptions, open questions, or verification gaps.
- [ ] Warnings and destructive actions appear before the relevant step, not after it.

## Gotchas

- Do not turn a procedure into a feature tour. Readers came to complete a job.
- Do not bury prerequisites in prose.
- Do not combine setup, execution, and verification in one long step.
- Do not use passive voice when it hides the actor. Tell the reader what to do.
- Do not fill gaps with plausible commands, console paths, file names, or output strings.
- Do not interleave competing ways to do the same task; separate alternative methods while keeping conditions that determine the required action.

## Attribution

Parts of this skill are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified. This skill is not affiliated with or endorsed by Google.
