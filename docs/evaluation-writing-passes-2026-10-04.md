# Writing with verification: 2026-10-04 pilot

Review and repair improved the same starting drafts, but the requested 74/74 result was not established in this initial pilot. Its last completed comparison scored **71/74 after review versus 64/74 before review**: seven assertion-level improvements, no measured regressions, and 67 unchanged results. Three newly frozen holdouts improved from **14/15 to 15/15**. These small comparisons support retaining a source-based review step; they do not establish reliable convergence to perfect documentation.

A later [focused follow-up](evaluation-writing-passes-focused-2026-10-04.md) reached 74/74 with a different writer configuration, then 73/74 on an unchanged repeat. Both scores were identical before and after review. The original results and limitations below remain unchanged.

## Results and interpretation

| Campaign | Initial draft | Generic review | Specialist review |
| --- | --- | --- | --- |
| Initial pilot: six cases, two samples | 67 pass, 4 fail, 3 unresolved | 69 pass, 4 fail, 1 unresolved | 73 pass, 1 fail |
| Revised controller and reviewer: same six cases, two new initial drafts each | 64 pass, 10 fail | Not completed | 71 pass, 3 fail |
| Three new holdouts, one sample each | 14 pass, 1 fail | Not run | 15 pass, 0 fail |

The six fixed cases contain 37 assertions per sample. Their prompts and assertions remained unchanged across campaigns. The initial drafts differ between the first and second comparisons, so 73/74 followed by 71/74 is not a controlled measurement of the reviewer-model change. The revised comparison reused all 12 recorded drafts from an interrupted campaign, preserving their hashes and provenance; it is a paired continuation, not a fresh confirmation run. No best-of-many answer selection was used.

The initial pilot compared the same draft across single-pass, generic-review, and specialist-review arms. It had a controller defect: ordinary source limitations triggered repairs even when the reviewer found no defect. All 12 initial specialist reviews reported no findings, yet rewriting still occurred. Its 73/74 therefore cannot establish that the specialist's criticism caused the improvement. The repaired controller retains a draft when no finding exists and distinguishes scope limitations from blocking evidence gaps.

In that initial campaign, generic review produced two improvements, one regression, 68 unchanged judgments, and three unresolved pairs. Specialist review produced four improvements, no regressions, 67 unchanged judgments, and three unresolved pairs. These are assertion-level counts, not independent document-level observations.

## Remaining defects

The revised specialist arm missed three fixed assertions:

- **Local-service tutorial, sample 2:** the browser check appeared only in a final checklist after the server had already been stopped. It also offered an unsupported HTTP-request alternative. This failed both checkpoint placement and supported-action requirements.
- **UI tutorial, sample 2:** the introduction described creating and previewing a report but did not name the saved `Trial` report as the outcome required by the assertion.

Blind review also found defects outside those assertions: inferred configuration purposes, an unsupported browser prerequisite, and a promise that a listing returns *all* jobs. A perfect fixed score would not cover these findings. In the revised run, ten workflow results were marked clear with limitations, one remained unresolved, and one used an explicit replacement reviewer. A clear workflow label is not a correctness guarantee.

The unresolved review demanded the underlying registry export to verify illustrative example values. The supplied source summary was sufficient for the bounded reference task, but the reviewer treated that limitation as blocking. This illustrates the opposite failure from missing a defect: requiring evidence beyond the task's stated scope.

## Method and configuration

The writer snapshots came from commit `d73d8185346886745d561e649d75590bc6e7aa3a` (`task-docs-writer` and `reference-docs-writer` 1.2.1). All writing and repairs used pi through OpenRouter with `~google/gemini-flash-latest`, low reasoning. The specialist review received the original request, complete draft, and `technical-docs-reviewer`; generic review instead received the writing instructions. Neither saw the benchmark assertions. Repair prompts treated reviewer findings as fallible and required checking them against the original source.

The initial reviewer used the same Gemini model and a one-repair allowance. The revised comparison used `openai/gpt-5.4`, medium reasoning, up to two repairs followed by a final review, a 120-second call timeout, and two provider/schema attempts per stage. The completed continuation imposed an 8,192-token output cap through each pi call's isolated configuration. The evaluated reviewer was version 1.0.1; version 1.0.2 additionally tells an already assigned reviewer not to launch another reviewer. The pilot did not separately measure that routing clarification.

An earlier uncapped attempt encountered a provider credit-reservation error. The local output cap allowed the continuation without changing global provider settings. One review still failed the required JSON schema in four attempts across two preserved stage invocations. Its invalid feedback was not passed to the writer. A fresh agent then reviewed that case from sources only, the configured writer made one repair, and the agent checked the complete revision. That fallback is included in the final 71/74 result; the result is not an unattended success by the configured model alone.

Before final grading, three new cases were frozen: a UI procedure with three access states, an error reference with conditional header availability and unknown units, and a migration preview that must not be presented as application. They used the same revised review configuration. Their 15/15 result covers one sample of three closely related tasks, not broad generalization.

Fresh agents independently graded anonymous source/answer packets. They saw the fixed assertions but no generation condition, review notes, or previous verdicts. Identical task/answer pairs shared a single judgment. The reported revised scores use those blind judgments, not the configured automatic grader. This is independent model review, not human expert calibration.

The initial automatic grader (`openai/gpt-5.4-mini`, low reasoning) was unreliable against the blind labels: five false passes among nine known failing assertion instances, and 13 false rejections among 209 known valid instances; four instances remained unresolved. These counts include repeated identical outputs across arms. Original judgments were retained rather than overwritten.

## Recorded effort

| Completed comparison component | Provider stages | Reported tokens | Sum of recorded call durations |
| --- | ---: | ---: | ---: |
| Twelve reused initial drafts | 12 | 77,139 | 66.8 seconds |
| Revised review and repair, including failed schema stages and fallback writer repair | 34 | 189,267 | 667.4 seconds |
| Three new holdout drafts | 3 | 19,254 | 16.6 seconds |
| Holdout review and repair | 9 | 43,063 | 124.6 seconds |

Durations are summed provider-call time, not elapsed campaign time. Tokens are the totals reported by the executor. This table excludes the interrupted campaign's unused reviews, the initial pilot, agent-based review and grading, and repository work. It is not a complete billing or latency estimate. The additional review cost must be weighed against the limited measured gains.

## Repository changes and checks

- Added `technical-docs-reviewer` with source-to-draft coverage checks, claim-to-source verification, fallible-review handling, and a bounded repair handoff. The user or project can choose the reviewer or grader; Jev is optional.
- Added verification handoffs to the task and reference writers. Editorial changes require a final meaning check. The pilot measured the review/repair core, not a separate editorial stage or an interactive agent's routing behavior.
- Added `scripts/eval_writing_passes.py` with frozen configurations, shared initial drafts, separate workflow review and final grading, immutable saved answers, explicit missing/unresolved denominators, and bounded model calls. The shared `scripts/eval_workflow.py` remains unchanged.
- Added disputed-review fixtures and a reviewer regression for correctly documented unknowns. The focused unknowns case retained the valid draft with and without the skill; it is a useful regression check, not evidence of skill lift. A new task-repair assertion was clarified to permit checking the supplied receipt; none of the 74 pilot assertions changed.
- Validation passed for nine skills and 27 eval JSON files; all 55 unit tests passed. The three changed/new skill entrypoints passed the skill creator's validator. No unfinished-work markers or diff whitespace errors remained.

The next evidence needed is better detection of execution-order and unsupported-behavior defects without manufacturing problems in valid drafts, followed by another frozen comparison on fresh cases. Merely changing the reviewer model did not establish a reliable perfect result.

Preserved local evidence is under `workspaces/writing-passes-20261004/`, `workspaces/writing-passes-20261004-round2/`, `workspaces/writing-passes-20261004-round3/`, and `workspaces/writing-passes-20261004-holdouts/`. The revised campaign's `blind-final-results.json` contains every joined verdict, answer hash, workflow status, paired count, and additional finding. Workspaces are ignored by Git; the compact [result record](evaluation-writing-passes-2026-10-04.json) preserves the counts and failed-assertion evidence with this report.
