# Writing with verification: focused follow-up, 2026-10-04

The focused candidate reached **74/74 once**, followed by **73/74 on an unchanged fresh repeat** and **15/15 on three new holdouts**. The initial drafts earned the same scores as the reviewed drafts. Every review retained its initial draft, so this configuration showed no measured benefit from review. The repeat also demonstrates that a clean review can miss a contradiction.

This follows the [initial pilot](evaluation-writing-passes-2026-10-04.md), whose paired comparison improved from 64/74 to 71/74. The follow-up changed both the reviewer instructions and the writer/reviewer execution configuration. Its higher scores cannot be attributed to the instruction revision alone.

## Results

| Evaluation | Initial draft | Specialist review | Improved / regressed / unchanged assertions |
| --- | ---: | ---: | ---: |
| Six fixed cases, two fresh samples each | 74/74 | 74/74 | 0 / 0 / 74 |
| Unchanged repeat, two further fresh samples each | 73/74 | 73/74 | 0 / 0 / 74 |
| Three new holdouts, one sample each | 15/15 | 15/15 | 0 / 0 / 15 |

All planned outputs and judgments are present, with no unresolved assertions. The 74 fixed assertions were unchanged throughout. The first two rows contain repeated samples of the same six tasks; assertion counts are not independent document-level observations. No generic-review arm ran in this follow-up.

The repeat's failure was the first sample of `reference-transfer-mixed-config-evidence`. Its table correctly declared `format` an optional string with `json` and `text` as allowed values and `json` as its default. A final source note then stated that constraints were unspecified, without limiting that statement to additional constraints or other settings. The blind judge rejected this contradiction under the existing assertion that declared facts remain accurate. The workflow reviewer had marked the draft clear with limitations. The answer and failing judgment were preserved without a post-score repair.

No additional consequential defects were reported by these judges. That is a bounded review result, not proof that the documents contain no other defects or that the system reliably produces perfect documentation.

## Frozen method and configuration

`technical-docs-reviewer` 1.1.0 added an explicit source-coverage pass, a trace through the draft in actual reading order, and checks of claims in alternatives, table descriptions, and example captions. Structured review asks for checked source evidence before findings. It retains correct drafts and separates ordinary scope limits from evidence gaps that block required verification.

The writer snapshots remained `task-docs-writer` and `reference-docs-writer` 1.2.1 from commit `d73d8185346886745d561e649d75590bc6e7aa3a`. Writing used Codex `gpt-6.1-sol` with low reasoning; workflow review used the same model with medium reasoning. Each draft was shared between the initial and reviewed arms. The reviewer received sources and the draft, but no benchmark assertions. The maximum allowance was two repairs followed by a final review, with a 120-second limit per call. Codex made one invocation per stage; all completed without repair or fallback. The pi-only 8,192-token option was present in the manifest but did not cap Codex output.

Codex CLI 0.160.0 ran in an empty temporary working directory with ambient instructions, skill discovery, memory, shell, browsing, apps, plugins, and delegation disabled. Only task and frozen skill text were inlined as candidate inputs. This isolation is implemented by the separate pilot; `scripts/eval_workflow.py` remains unchanged.

The candidate's plan required an unchanged fresh repeat and frozen holdouts only if the first run reached 74/74. Both were completed. The repeat used the identical manifest and runner, with fresh generation and no reused drafts. No further semantic tuning or candidate search followed its failure.

Fresh-context agents graded anonymous task, answer, and fixed-assertion packets. They received no model identity, condition, review notes, previous verdicts, or target score. Identical task/answer pairs shared a judgment. The join checked full coverage, source/assertion equality, answer text, and hashes. The scores use those separate blind judgments; the configured automatic grading command was not run. The assessment plan initially described that unused grader as pi, but the saved manifest actually configures Codex. This metadata discrepancy did not affect generation or reported grading. Agent judgments are not human expert calibration.

## Holdouts and reviewer regressions

The three new holdouts covered a temporary snapshot whose count must be checked before closing it, an API reference that must distinguish an illustrative response from a declared parameter, and an archive procedure with state-dependent access and one permitted reindex. They were frozen before candidate execution. A separate source audit found one assertion required opening-paragraph placement that its task did not request. Before any holdout outputs existed, that assertion changed from "The opening names" to "The tutorial names"; the outcome requirement remained intact. The original fixture, hash, audit, and correction are retained. None of the fixed 74 assertions changed. These are three related synthetic tasks with one sample each, so their result supports only narrow transfer.

Two focused reviewer fixtures compared the same model with and without the reviewer skill. Blind grading gave **9/10 in each condition**. Both identified a check placed after its required channel was closed, and both accepted a valid bounded reference without demanding uncaptured schema details. The no-skill review omitted the requested repair. The with-skill review proposed the supported reorder but also offered an unsupported reopening alternative. These tests preserve a known reviewer weakness; they do not demonstrate skill lift. The writer must still check proposed repairs against source evidence.

An earlier attempt with the revised instructions and the previous OpenRouter configuration stopped at a provider credit limit. It preserved 14 completed stages, four error stages, three initial drafts, and one reviewed output without semantic grading. The switch to Codex started fresh drafts and changed the execution configuration; it was not a continuation of selected successful outputs. No account limits or credits were changed. Those partial artifacts remain separate from the completed comparisons.

## Recorded effort

| Component | Completed stages | Reported tokens | Sum of recorded call durations |
| --- | ---: | ---: | ---: |
| Initial candidate drafts | 12 | 197,600 | 225.0 seconds |
| Initial candidate reviews | 12 | 192,256 | 256.5 seconds |
| Repeat drafts | 12 | 180,298 | 189.5 seconds |
| Repeat reviews | 12 | 165,243 | 266.8 seconds |
| Holdout drafts | 3 | 32,864 | 49.6 seconds |
| Holdout reviews | 3 | 37,545 | 62.1 seconds |

The 54 stages exclude the abandoned provider attempt, CLI smoke check, reviewer regressions, source audit, blind grading, and repository work. Tokens are executor-reported totals; summed call durations are not campaign wall time or a billing estimate. All 27 reviewed documents remained identical to their initial drafts, despite the added review cost.

## Delivery and verification

The repository adds the configurable reviewer, verification handoffs in the task and reference writers, bounded evaluation tooling, and regression fixtures. Jev remains optional. The evaluation covers the review/repair controller and selected reviewer behavior, not automatic interactive routing or a separate editorial pass.

Repository validation passed for nine skills and 27 eval JSON files; all 56 unit tests passed. The three changed/new skill entrypoints passed the skill creator's validator. No unfinished-work markers or diff whitespace errors remained. These mechanical checks do not override the semantic failures above.

Local source artifacts are in `workspaces/writing-passes-20261004-codex-focused/`, `workspaces/writing-passes-20261004-codex-repeat/`, `workspaces/writing-passes-20261004-codex-holdouts/`, and `workspaces/technical-docs-reviewer/iteration-3/`. Workspaces are ignored by Git. The committed [compact result record](evaluation-writing-passes-focused-2026-10-04.json) preserves configurations, counts, hashes, holdout fixtures, and failed-assertion evidence.
