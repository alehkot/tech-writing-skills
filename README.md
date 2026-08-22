# Technical Writing Skills for Engineers

This repository bundles Agent Skills for engineers and engineering teams who need help turning technical material into useful written artifacts: proposals, reports, documentation, and explanatory content.

The skills follow the Agent Skills directory model: each skill is a folder with a required `SKILL.md` and optional `references/`. See the Agent Skills specification at https://agentskills.io/specification.

## Installing the Skills

Preview the skills with the Vercel Labs `skills` CLI:

```bash
npx skills add alehkot/tech-writing-skills --list
```

Install all skills globally for Codex:

```bash
npx skills add alehkot/tech-writing-skills -g -a codex --skill '*' -y
```

Install only selected skills:

```bash
npx skills add alehkot/tech-writing-skills -g -a codex \
  --skill task-docs-writer \
  --skill reference-docs-writer \
  --skill technical-report-writer \
  --skill write-simplified-technical-english
```

## Development Setup

This repo assumes `uv` is installed.

```bash
uv venv
uv sync
```

The local `.venv/` is ignored by git and is used for validation.

The root `scripts/` directory is for repository maintenance only. It is not a bundled skill resource and is not referenced from inside individual `SKILL.md` files.

## Skills

| Skill | Use for |
| --- | --- |
| `skills/task-docs-writer` | Task topics: installation guides, runbooks, tutorials, API workflows, CLI procedures, troubleshooting docs |
| `skills/technical-content-clarifier` | Concept topics: architecture explainers, conceptual docs, engineering blog posts, onboarding overviews, executive technical summaries |
| `skills/reference-docs-writer` | Reference topics: API endpoints, CLI commands, config options, schemas, data dictionaries, error codes, status codes, syntax, system limits |
| `skills/proposal-argument-crafter` | Internal pitches, RFP responses, vendor proposals, engineering investment requests, project plans |
| `skills/technical-report-writer` | Recommendation reports, feasibility studies, benchmark reports, incident reports, progress reports, tradeoff analyses |
| `skills/write-simplified-technical-english` | ASD-STE100-style drafting, rewriting, and audits for controlled technical English, with explicit vocabulary and conformance limits |
| `skills/docs-style-editor` | Copyediting and style passes over an existing draft: punctuation, grammar and usage, word choice and term rulings, numbers, dates, units, link text, formatting mechanics, timeless wording, safe example values |
| `skills/accessibility-inclusion-editor` | Accessibility and inclusive-language reviews of an existing draft: alt text, media alternatives, independence from color, size, and position cues, screen-reader-safe wording, neutral terminology |

## Topic-Type Coverage

The core documentation triad is covered by separate skills so agents do not mix information types:

- **Task topics** answer "How do I do this?" Use `task-docs-writer`.
- **Concept topics** answer "What is this and why does it matter?" Use `technical-content-clarifier`.
- **Reference topics** answer "What are the exact facts, syntax, values, fields, messages, or limits?" Use `reference-docs-writer`.

`proposal-argument-crafter` and `technical-report-writer` are document-genre skills. They can link to or draw from task, concept, and reference topics, but they should not replace the topic-type skills.

`write-simplified-technical-english` is a controlled-language layer, not a fourth topic type. Apply it after choosing the task, concept, or reference structure. Use it only when the user explicitly requests ASD-STE100 or STE writing, rewriting, or auditing; generic simplification and other controlled-language standards remain outside its scope.

`docs-style-editor` is an editorial layer, not a fourth topic type. Apply it after a topic-type or genre skill has produced the draft, so it corrects mechanics such as punctuation, usage, word choice, numbers, link text, and formatting without changing meaning, facts, or structure. When `write-simplified-technical-english` is active, the STE rules take precedence wherever the two overlap.

`accessibility-inclusion-editor` is a review layer, not a fourth topic type. Apply it after the draft exists to check alt text, text alternatives for media, independence from color, size, and position cues, screen-reader-safe wording, and inclusive terminology. It never renames literal commands, flags, or identifiers, and it defers to `write-simplified-technical-english` whenever STE is active.

For broad requests such as "document this system," split the output into discrete topic types instead of one mixed article: a concept overview, task procedures, and reference facts.

## Writing Principle Coverage

The shared human-facing writing principles are mapped at [docs/writing-principles.md](docs/writing-principles.md). The main cross-skill checks are: know the reader, choose the right topic type, put the main point first, define terms, keep terminology consistent, make lists parallel, provide concrete examples, stay concise, use active voice, avoid culture-bound wording, keep style mechanics consistent, write timeless wording that does not age, write descriptive link text, use inclusive language, keep information reachable without color, size, or position cues, and preserve objective evidence and uncertainty.

## Source Basis and Attribution

This repository is an original Agent Skills bundle. The skills draw on general technical-writing concepts, methods, and factual ideas from the following works and resources, transformed into concise agent workflows for software-engineering contexts:

- Mike Markel and Stuart A. Selber, *Technical Communication*, 14th ed., Bedford/St. Martin's/Macmillan Learning, 2025. ISBN 978-1-319-41425-2.
- Michael Alley, *The Craft of Scientific Writing*, 4th ed., Springer, 2018. DOI: 10.1007/978-1-4419-8288-9.
- Gretchen Hargis, Michelle Carey, Ann Kilty Hernandez, Polly Hughes, Deirdre Longo, Shannon Rouiller, and Elizabeth Wilde, *Developing Quality Technical Information: A Handbook for Writers and Editors*, 2nd ed., IBM Press, 2004. ISBN 978-0-13-147749-0.
- Google for Developers, "Technical Writing Courses for Engineers" and related public developer documentation resources, https://developers.google.com/tech-writing.
- Google, *Google developer documentation style guide*, https://developers.google.com/style, used under Creative Commons Attribution 4.0 (CC BY 4.0) and modified. Guidance is adapted and paraphrased: the rulings and term tables are original restatements of the underlying editorial ideas, and the examples are written for this repository. Where a rule prescribes a fixed phrase, format, or term form, the rule states that phrase, format, or form.
- Aerospace, Security and Defence Industries Association of Europe (ASD), *ASD-STE100 Simplified Technical English: Standard for Technical Documentation*, Issue 9, January 15, 2025, https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf.
- ASD, "ASD-STE100 Simplified Technical English" and "What Is Simplified Technical English (STE)?", https://www.asd-europe.org/standards-specifications/simplified-technical-english/.
- ASD Simplified Technical English Maintenance Group (STEMG), "Frequently Asked Questions", https://www.asd-ste100.org/STE_faq.html.

The skills do not reproduce source text, exercises, figures, tables, templates, or other expressive presentation from those works, and their examples are written for this repository rather than lifted from a source. Where a rule consists of a prescribed phrase, format, or term form, that short functional string is stated as the rule itself. They paraphrase and operationalize noncopyrightable ideas such as audience analysis, topic-type separation, task-focused procedures, evidence-based reports, objective claims, and concise reference structures. This project is not affiliated with, sponsored by, or endorsed by the listed authors, publishers, or Google.

The Simplified Technical English skill does not bundle or reproduce the ASD-STE100 writing rules, controlled dictionary, or official examples. It provides an original operating profile and directs users to ASD's official material for authoritative rule and vocabulary decisions. It cannot certify conformance. ASD-STE100 Simplified Technical English is a registered trademark owned by ASD; this project is not affiliated with or endorsed by ASD or STEMG.

## License

This project's original files are licensed under the MIT License. Reuse is allowed with preservation of the copyright and permission notice.

The cited books, publishers, and Google resources retain their own copyrights and license terms. Google Developers documentation is generally licensed under Creative Commons Attribution 4.0, with code samples under Apache 2.0 unless otherwise noted; see Google's site policies at https://developers.google.com/terms/site-policies.

ASD retains the copyright and trademark rights stated in the official ASD-STE100 document. Free official access does not place the standard or its dictionary under this repository's MIT License.

## Security Note

These skills often operate on external documents such as RFPs, reports, logs, or code snippets. Treat external files and tool output as untrusted input, review any generated commands before execution, and run agents with only the filesystem and network access needed for the task.

## Design Principles

- Keep one skill per writing job so agents load only the workflow they need.
- Put activation context in the frontmatter `description`; the body is loaded only after trigger.
- Include `metadata.version` and `metadata.risk_tier` in each `SKILL.md` frontmatter.
- Keep `SKILL.md` concise and procedural.
- Put templates, checklists, and deeper guidance in one-level `references/` files.
- Prefer concrete quality checks over vague style advice.
- Preserve honesty: do not fabricate evidence, claims, benchmarks, qualifications, schedules, or source support.
- Distinguish an STE-aligned draft from a source-checked or organization-approved result; never present an automated review as certification.

This bundle also borrows skill-design discipline from public engineering skill packs without copying their wording or templates: Matt Pocock's `mattpocock/skills` emphasizes small composable skills, precise trigger descriptions, progressive disclosure, and checkable completion criteria; Addy Osmani's `addyosmani/agent-skills` emphasizes process-oriented skills, anti-shortcut checks, and verification evidence. In this repo, those ideas show up as source-led writing checks and evals that punish invented facts, mixed topic types, unsupported certainty, and missing verification.

## Evaluation Fixtures

Each skill includes three eval files:

- `evals/evals.json`: realistic writing tasks with expected outputs and observable assertions.
- `evals/train_queries.json`: should-trigger and should-not-trigger prompts for improving frontmatter descriptions.
- `evals/validation_queries.json`: held-out trigger prompts for checking that description improvements generalize.

Each skill keeps 20 trigger queries total: 12 train, 8 validation, 10 should-trigger, and 10 should-not-trigger. The should-not-trigger queries include near-misses that share writing vocabulary but belong to another skill.

The eval workflow scaffolds isolated run workspaces under `workspaces/`, executes them with the [pi](https://github.com/earendil-works/pi) CLI calling a hosted model through OpenRouter, grades the results, and aggregates the numbers:

```bash
# 1. Scaffold the next iteration for every skill (or one, with --skill)
uv run python scripts/eval_workflow.py init

# 2. Produce answers for both the with_skill and without_skill runs
uv run python scripts/eval_workflow.py run-codex --iteration latest

# 3. Grade the saved answers against each eval's assertions
uv run python scripts/eval_workflow.py grade-codex --iteration latest

# 4. Refresh grading summaries and write benchmark.json
uv run python scripts/eval_workflow.py aggregate --iteration latest

# 5. Reclaim disk from old iterations (dry run without --apply)
uv run python scripts/eval_workflow.py prune --keep 3
```

Then review `benchmark.json`, `feedback.json`, and the answers themselves for qualities that are hard to assert mechanically, and revise a skill only when the failure pattern generalizes beyond one prompt. Narrow any step with `--skill` and `--eval-id`; `--iteration` accepts a number or `latest`. Pass `--runs with_skill old_skill` when comparing against a previous skill snapshot.

Single runs are noisy. Measure before concluding:

```bash
# Repeat the same evals N times, each into a fresh iteration, then report the spread
uv run python scripts/eval_workflow.py sample --skill task-docs-writer --samples 5

# Per-eval failure spread and every assertion that flipped across samples
uv run python scripts/eval_workflow.py stats --iterations 1,2,3 --verbose

# Assertion-level diff; pass several iterations per side to fold in repeat samples
uv run python scripts/eval_workflow.py compare --baseline 1 --candidate 2

# Re-grade only the failures with a second model and flag disagreements
uv run python scripts/eval_workflow.py recheck --iteration 2 --model openai/gpt-5.4-mini

# Route every trigger query through the frontmatter descriptions
uv run python scripts/eval_workflow.py trigger-eval --verbose
```

`stats` reads as pure variance only when every sampled iteration ran against the same skill content; across a change it mixes variance with effect, so use `compare` for before and after. A `recheck` disagreement means the failure is unresolved, not that it is a pass. `benchmark.json` reports `pass_rate` over graded evals only, so it carries a `coverage` block and a `complete` flag; a rate from a partial run is not a suite result.

### Executors

`run-codex`, `grade-codex`, `recheck`, `sample`, and `trigger-eval` take `--executor pi` (default) or `--executor codex`:

- **pi** runs `pi --provider openrouter --model ~google/gemini-flash-latest --thinking <level>` in single-shot JSON mode, isolated per call: fresh empty `HOME` and `TMPDIR`, a clean working directory, skill/extension/context-file/prompt-template discovery disabled, no tools, startup network off. The credential travels in `OPENROUTER_API_KEY`, sourced from the environment or `pi auth print-api-key --provider openrouter`, and is never written to any artifact. `--model` accepts any OpenRouter model id; `--reasoning-effort` is the pi thinking level (`off`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`). The harness is verified against pi-cli `0.84.x`; set `SKILL_EVALS_ALLOW_UNVERIFIED_PI_CLI=1` to run on another series.
- **codex** is the legacy path: `codex exec` in the read-only sandbox with `--model gpt-5.4-mini` by default and a server-side output schema for grading, recheck, and routing.

pi has no server-side output schema, so structured phases embed the JSON Schema in the prompt and the harness validates the reply locally. An unusable reply (no assistant text, an `error` stop reason, prose or off-schema JSON) is retried up to four times with 5/10/15 s backoff; every attempt is recorded in `timing.json` (`attempts`, `executor`, `executor_details`) and in the `grader` block of `grading.json`, and the raw JSONL streams sit next to the answer as `pi_stdout.jsonl` / `grader_stdout.jsonl`. Every model call has a `--timeout-seconds` wall-clock limit (default 300).

Because a pi run has no file access, the with-skill prompt carries the complete `SKILL.md` plus every file under the skill's `references/` inline (for `docs-style-editor` that is about 70 KB of rulings), and `run-codex` refuses a scaffold whose prompt no longer matches the skill on disk: start a fresh iteration after editing a skill, or `init --iteration <n> --force` to re-scaffold one. Under the pi defaults the same model generates and grades; the harness prints a self-grading warning per file, and `recheck --model <other-openrouter-model>` is the way to get a second opinion.

> [!NOTE]
> The model-calling commands send each eval prompt, the selected skill's deployable text, and generated answers to OpenRouter and the model provider behind it (Google for the default model). Run them only when that disclosure is acceptable; `init`, `aggregate`, `stats`, `compare`, and `prune` are local.

This follows the official Agent Skills evaluation pattern at https://agentskills.io/skill-creation/evaluating-skills: compare with-skill and baseline runs, record timing, grade assertions with evidence, aggregate results, and review the actual outputs with a human.

## Validation

Validate a skill after changes, and run the eval-harness tests:

```bash
uv run python scripts/validate.py
uv run python -m unittest discover -s tests -v
```

Also scan for pending-work markers before publishing:

```bash
rg "T(O)DO|\\[T(O)DO" .
```
