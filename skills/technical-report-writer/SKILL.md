---
name: technical-report-writer
description: >-
  Use this skill when the user needs to write or improve a rigorous technical report for engineering decision-making: recommendation report, feasibility study, benchmark report, incident report, postmortem, progress report, evaluation memo, tradeoff analysis, migration assessment, or architecture decision report. It helps separate evidence, criteria, analysis, conclusions, and recommendations.
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
5. Define unfamiliar terms, acronyms, metrics, units, and option names before using them in findings or recommendations.
6. Define evaluation criteria before comparing options. Use criteria the reader can inspect, such as cost, reliability, security, latency, maintainability, adoption effort, or compliance. Distinguish mandatory criteria from desirable criteria when the decision depends on thresholds.
7. Organize analysis by criteria, not by whatever order the notes arrived in.
8. Keep comparison lists and tables parallel: same criteria, same units, same level of detail.
9. Write conclusions as what the evidence means. Write recommendations as what action to take. Do not merge the two.
10. Structure modularly for mixed audiences: executive summary for decision makers, main findings for implementers, and appendices for detailed evidence when needed. For long reports, map the major sections at the end of the introduction.
11. Add limitations, confidence level, and open questions when evidence is incomplete.
12. End with a forward-looking action: the specific action, owner, decision point, or follow-up the audience should take next.
13. Put the executive summary last in the drafting process, but first in the final report.
14. Run the evidence-to-recommendation check before finalizing.

## Default Recommendation Report Structure

```markdown
# [Report Title]

## Executive Summary
[Decision context, key finding, recommendation.]

## Scope and Method
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

## Next Actions
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
- [ ] Every recommendation traces back to a conclusion, and every conclusion traces back to evidence.
- [ ] Uncertainty and limitations are visible.
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
