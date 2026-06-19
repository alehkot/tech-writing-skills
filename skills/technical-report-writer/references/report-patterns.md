# Technical Report Patterns

## Use When

Load this reference for recommendation reports, feasibility studies, benchmark reports, tradeoff analyses, postmortems, incident reports, migration assessments, progress reports, and architecture decision reports.

## Source Principles

- Reports support decisions by separating facts, analysis, conclusions, and recommendations.
- Criteria should be stated before options are judged.
- Conclusions explain what the evidence means; recommendations explain what to do next.
- Honest limitations increase credibility.
- Consistent terms, units, and parallel comparisons make the evidence easier to inspect.
- Missing evidence is a finding about confidence, not a blank to fill.

## Report Type Picker

- Recommendation report: use when the reader must choose an action.
- Feasibility study: use when the reader must know whether a plan is practical.
- Benchmark report: use when measured performance, cost, reliability, or quality is central.
- Incident or postmortem report: use when explaining what happened, impact, causes, fixes, and prevention.
- Progress report: use when the reader needs current state, completed work, blockers, and next milestones.

## Criteria Matrix

Use a table when comparing options:

```markdown
| Criterion | Weight | Option A | Option B | Notes |
| --- | ---: | --- | --- | --- |
| Reliability | High |  |  |  |
| Cost | Medium |  |  |  |
| Operational effort | High |  |  |  |
```

When threshold decisions matter, separate mandatory criteria from desirable criteria before scoring options.

## Evidence Chain

For each recommendation, check the chain:

```markdown
Evidence -> Finding -> Conclusion -> Recommendation -> Next action
```

If any link is missing, revise before finalizing.

Use this stricter version when evidence is incomplete:

```markdown
Evidence supplied:
Evidence missing:
Confidence effect:
Allowed conclusion:
Action needed to close the gap:
```

## Comparison Discipline

- Define metrics, units, acronyms, and option names before the reader reaches the findings.
- Use the same term for each option, system, metric, and risk throughout the report.
- Keep criteria rows parallel: same unit, time window, baseline, and level of precision where possible.
- Label estimates, assumptions, and incomplete evidence instead of letting them read like measured facts.

## Executive Summary Pattern

Use four compact parts:

1. Question or decision.
2. Most important evidence.
3. Conclusion.
4. Recommendation or next step.

## Purpose and Order

State the report's purpose with a clear communicating verb:

- `This report recommends...`
- `This report evaluates...`
- `This report explains...`
- `This report summarizes...`

Put the most important decision-relevant information first. Use chronology only when sequence is the point, such as a timeline in an incident report.

For long reports, end the introduction with a short map of the major sections so readers know how the reasoning is organized.

## Modular Audience Pattern

Use modular sections when the report has mixed readers:

- Executive summary: decision, impact, conclusion, recommendation.
- Main body: scope, method, criteria, findings, analysis.
- Appendix: raw data, full benchmark tables, detailed logs, or supporting calculations.
- Next actions: owner, decision point, due date, or follow-up question.

## Review Checklist

- Scope and method are explicit.
- The purpose sentence tells the reader why the report exists.
- Critical findings appear before supporting detail.
- Terms, metrics, units, and option names are defined and consistent.
- Criteria are inspectable and relevant to the decision.
- Mandatory and desirable criteria are separated when that distinction affects the decision.
- Comparison tables and lists use parallel structure.
- Evidence sources are named.
- Missing data is named and reflected in confidence, limitations, or next actions.
- Analysis explains significance rather than repeating data.
- Conclusions do not introduce new evidence.
- Recommendations are actionable and tied to conclusions.
- The report gives a forward-looking action: what the audience should do next.
- Limitations and uncertainty are visible.
- Bad news is stated directly in a topic sentence or other emphatic location, not hidden mid-paragraph.
