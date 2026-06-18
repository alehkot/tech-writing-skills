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
  --skill technical-report-writer
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

## Topic-Type Coverage

The core documentation triad is covered by separate skills so agents do not mix information types:

- **Task topics** answer "How do I do this?" Use `task-docs-writer`.
- **Concept topics** answer "What is this and why does it matter?" Use `technical-content-clarifier`.
- **Reference topics** answer "What are the exact facts, syntax, values, fields, messages, or limits?" Use `reference-docs-writer`.

`proposal-argument-crafter` and `technical-report-writer` are document-genre skills. They can link to or draw from task, concept, and reference topics, but they should not replace the topic-type skills.

For broad requests such as "document this system," split the output into discrete topic types instead of one mixed article: a concept overview, task procedures, and reference facts.

## Writing Principle Coverage

The shared human-facing writing principles are mapped at [docs/writing-principles.md](docs/writing-principles.md). The main cross-skill checks are: know the reader, choose the right topic type, put the main point first, define terms, keep terminology consistent, make lists parallel, provide concrete examples, stay concise, use active voice, avoid culture-bound wording, and preserve objective evidence and uncertainty.

## Source Basis and Attribution

This repository is an original Agent Skills bundle. The skills draw on general technical-writing concepts, methods, and factual ideas from the following works and resources, transformed into concise agent workflows for software-engineering contexts:

- Mike Markel and Stuart A. Selber, *Technical Communication*, 14th ed., Bedford/St. Martin's/Macmillan Learning, 2025. ISBN 978-1-319-41425-2.
- Michael Alley, *The Craft of Scientific Writing*, 4th ed., Springer, 2018. DOI: 10.1007/978-1-4419-8288-9.
- Gretchen Hargis, Michelle Carey, Ann Kilty Hernandez, Polly Hughes, Deirdre Longo, Shannon Rouiller, and Elizabeth Wilde, *Developing Quality Technical Information: A Handbook for Writers and Editors*, 2nd ed., IBM Press, 2004. ISBN 978-0-13-147749-0.
- Google for Developers, "Technical Writing Courses for Engineers" and related public developer documentation resources, https://developers.google.com/tech-writing.

The skills do not reproduce source text, examples, exercises, figures, tables, templates, or other expressive presentation from those works. They paraphrase and operationalize noncopyrightable ideas such as audience analysis, topic-type separation, task-focused procedures, evidence-based reports, objective claims, and concise reference structures. This project is not affiliated with, sponsored by, or endorsed by the listed authors, publishers, or Google.

## License

This project's original files are licensed under the MIT License. Reuse is allowed with preservation of the copyright and permission notice.

The cited books, publishers, and Google resources retain their own copyrights and license terms. Google Developers documentation is generally licensed under Creative Commons Attribution 4.0, with code samples under Apache 2.0 unless otherwise noted; see Google's site policies at https://developers.google.com/terms/site-policies.

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

## Evaluation Fixtures

Each skill includes three eval files:

- `evals/evals.json`: realistic writing tasks with expected outputs and observable assertions.
- `evals/train_queries.json`: should-trigger and should-not-trigger prompts for improving frontmatter descriptions.
- `evals/validation_queries.json`: held-out trigger prompts for checking that description improvements generalize.

Each skill keeps 20 trigger queries total: 12 train, 8 validation, 10 should-trigger, and 10 should-not-trigger. The should-not-trigger queries include near-misses that share writing vocabulary but belong to another skill.

Use these fixtures to evaluate skill changes with isolated runs:

```bash
uv run python scripts/eval_workflow.py init --skill task-docs-writer
```

1. Run each eval once with the skill and once without it, or against the previous skill version.
2. Save outputs in the generated ignored workspace, for example `workspaces/task-docs-writer/iteration-1/...`.
3. Grade assertions with concrete evidence from the output.
4. Review the outputs manually for qualities that are hard to assert mechanically.
5. Capture token and duration data in each `timing.json`.
6. Optional: run and grade scaffolded prompts with Codex CLI:

```bash
uv run python scripts/eval_workflow.py run-codex --skill task-docs-writer --iteration 1
uv run python scripts/eval_workflow.py grade-codex --skill task-docs-writer --iteration 1
```

7. Aggregate graded results:

```bash
uv run python scripts/eval_workflow.py aggregate --skill task-docs-writer --iteration 1
```

8. Review `benchmark.json` and `feedback.json`.
9. Revise the skill only when the failure pattern generalizes beyond one prompt.

Run all skills by omitting `--skill`, or pass `--runs with_skill old_skill` when comparing against a previous skill snapshot.

This follows the official Agent Skills evaluation pattern at https://agentskills.io/skill-creation/evaluating-skills: compare with-skill and baseline runs, record timing, grade assertions with evidence, aggregate results, and review the actual outputs with a human.

## Validation

Validate a skill after changes:

```bash
uv run python scripts/validate.py
```

Also scan for pending-work markers before publishing:

```bash
rg "T(O)DO|\\[T(O)DO" .
```
