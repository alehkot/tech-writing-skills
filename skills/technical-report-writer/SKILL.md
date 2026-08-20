---
name: technical-report-writer
description: >-
  Technical report writing for rigorous engineering decision documents: recommendation reports, feasibility studies, benchmark reports, incident reports, postmortems, progress reports, evaluation memos, tradeoff analyses, migration assessments, and architecture decision reports. Use for separating evidence, criteria, analysis, conclusions, and recommendations.
  Use when evidence traceability, limitations, missing data, or decision criteria must be explicit.
metadata:
  version: "1.1.0"
  risk_tier: low
---

# Technical Report Writer

## Overview

Build reports that let a technical or management reader understand what was studied, how it was evaluated, what the evidence means, and what action should follow.

Read [references/report-patterns.md](references/report-patterns.md) when the task involves analysis, comparison, recommendations, incidents, benchmarks, or status reporting.

## Workflow

1. Identify the report type, audience groups, decision to support, scope, deadline, and required level of detail.
2. State the document's purpose with a clear communicating verb, such as `This report recommends...`, `This report evaluates...`, or `This report explains...`.
3. Put the most important information first. Do not organize by chronology or suspense when readers need a decision.
4. Separate facts from interpretation. Capture raw evidence, data sources, assumptions, and uncertainty before drafting conclusions.
5. Write in active voice with the actor as the subject. Allow passive voice only to emphasize the object, to de-emphasize the actor and avoid blame in incident or postmortem prose (`247 writes were rejected during the failover`), or when the actor is irrelevant. Recast passives that name their actor with `by` as active sentences.
6. Define unfamiliar terms, acronyms, metrics, units, and option names before using them in findings or recommendations.
7. Define evaluation criteria before comparing options. Use criteria the reader can inspect, such as cost, reliability, security, latency, maintainability, adoption effort, or compliance. Distinguish mandatory criteria from desirable criteria when the decision depends on thresholds.
8. Organize analysis by criteria, not by whatever order the notes arrived in.
9. Keep comparison lists and tables parallel: same criteria, same units, same level of detail.
10. Write conclusions as what the evidence means. Write recommendations as what action to take. Do not merge the two.
11. Structure modularly for mixed audiences: executive summary for decision makers, main findings for implementers, and appendices for detailed evidence when needed. For long reports, map the major sections at the end of the introduction.
12. Add limitations, confidence level, and open questions when evidence is incomplete.
13. Audit every major claim through this chain: evidence, finding, conclusion, recommendation, next action. If a link is missing, revise, downgrade confidence, or list the gap.
14. End with a forward-looking action: the specific action, owner, decision point, or follow-up the audience should take next.
15. Put the executive summary last in the drafting process, but first in the final report.

## Completion Criterion

Complete the task only when every recommendation traces through evidence, finding, conclusion, recommendation, and next action; criteria are inspectable before comparisons, limitations and missing data are visible, and every applicable self-check item passes.

## Default Recommendation Report Structure

```markdown
# [Report title]

## Executive summary
[Decision context, key finding, recommendation.]

## Scope and method
[What was evaluated and how.]

## Criteria
[How options are judged.]

## Findings
[Evidence organized by criterion.]

## Analysis
[What the evidence means.]

## Conclusions
[Supported interpretations.]

## Recommendations
[Specific actions and next steps.]

## Limitations
[Uncertainty, missing data, assumptions.]

## Next actions
[Owners, decision points, or follow-up work.]
```

## Self-Check

- [ ] The report states the decision or question it supports.
- [ ] The introduction uses a clear communicating verb to explain why the report exists.
- [ ] The most important information appears first.
- [ ] Terms, acronyms, metrics, units, and option names are defined and used consistently.
- [ ] The criteria appear before the option-by-option analysis.
- [ ] Mandatory criteria and desirable criteria are separated when threshold decisions matter.
- [ ] Comparison lists and tables use parallel structure and comparable units.
- [ ] Claims pass the durability check: no superlatives or unconditional guarantees (canonical rules in technical-content-clarifier's claims guidance).
- [ ] Comparison tables use consistent digit grouping and unambiguous date formats (canonical rules in docs-style-editor's numbers-dates-units reference).
- [ ] Every recommendation traces back to a conclusion, and every conclusion traces back to evidence.
- [ ] Uncertainty and limitations are visible.
- [ ] Missing data is labeled and does not silently become a confident finding.
- [ ] Tables are used where they help comparison; prose explains significance rather than repeating table cells.
- [ ] The executive summary can stand alone for a busy reader.
- [ ] Detailed evidence moves to appendices when it would overload decision makers.
- [ ] Material bad news appears in an emphatic location, not buried mid-paragraph.
- [ ] The ending gives a clear forward-looking action, not just a recap.

## Gotchas

- Do not start with a recommendation and retrofit evidence around it.
- Do not use "best" without criteria.
- Do not bury bad news. State material risks and negative findings clearly.
- Do not treat status reports, incident reports, and recommendation reports as the same artifact; choose the template that matches the decision need.
- Do not rank options conclusively when the supplied evidence cannot support the ranking.

## Attribution

Parts of this skill are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified. This skill is not affiliated with or endorsed by Google.
