---
name: proposal-argument-crafter
description: >-
  Use this skill when the user needs to write or improve a persuasive technical proposal: internal engineering pitch, architecture investment request, project proposal, vendor proposal, RFP response, grant-style technical plan, budget request, or implementation proposal. It helps parse constraints, build a problem-solution argument, prove feasibility, and make the proposal compliant, credible, and decision-ready.
---

# Proposal Argument Crafter

## Overview

Create proposals that persuade technical and business reviewers by connecting a real problem, a feasible plan, supporting evidence, qualifications, cost, schedule, risks, and requested decision.

Read [references/proposal-patterns.md](references/proposal-patterns.md) when drafting a new proposal, responding to an RFP, or reviewing a proposal for compliance and persuasiveness.

## Workflow

1. Extract the decision context: reviewer, requested decision, audience attitude, stakes, constraints, deadline, required sections, exact heading names, page limits, formatting rules, evaluation criteria, and disallowed claims.
2. State the problem in the reviewer's terms. Show consequence, urgency, and why the status quo is insufficient.
3. If reviewers are skeptical or hostile, establish the practical benefits and evidence before asking them to accept the recommendation.
4. Use a problem-plan-evidence-decision spine: problem or opportunity, proposed plan, evidence of fit, and decision requested.
5. Present the proposed solution as a plan, not just an idea: scope, deliverables, milestones, owners, dependencies, and success metrics.
6. Add proof: prior work, benchmarks, prototypes, customer evidence, named personnel qualifications, comparable projects, available resources, management structure, or measured constraints.
7. Define unfamiliar terms and acronyms, then use terminology consistently across problem, solution, evidence, budget, and risks.
8. Make the main assertions visible through assertion headings, lead sentences, or pull-quote style callouts when allowed by the proposal format.
9. Make cost and schedule reviewable. Use a table for budget and a milestone list or timeline for schedule; for complex delivery plans, use or describe a Gantt chart, network diagram, or dependency-aware timeline.
10. Describe quality-control or evaluation methods when the proposal promises delivery, implementation, or measurable outcomes.
11. Address risks honestly. Pair each material risk with mitigation, fallback, or decision point.
12. End with the explicit ask: approval, budget, staffing, decision, pilot, or next meeting.
13. Run the compliance and persuasion checks before finalizing.

## Default Proposal Structure

```markdown
# [Proposal Title]

## Summary
[Problem, proposal, value, ask.]

## Problem
[Current state, impact, constraints.]

## Proposed Approach
[Plan, deliverables, milestones.]

## Evidence and Qualifications
[Why this plan and team can succeed.]

## Budget and Schedule
[Cost, timeline, staffing.]

## Risks and Mitigations
[Honest risks with controls.]

## Decision Needed
[Specific approval or next action.]
```

## Self-Check

- [ ] The proposal follows all supplied instructions before optimizing style.
- [ ] The first page makes the problem, solution, value, and ask unmistakable.
- [ ] The argument follows a problem-plan-evidence-decision spine.
- [ ] Claims are backed by evidence or labeled as assumptions.
- [ ] Terms and acronyms are defined once and used consistently.
- [ ] Benefits are tied to reviewer goals, not just engineering elegance.
- [ ] Anticipated reviewer objections are answered directly and objectively.
- [ ] Key personnel or team qualifications are included when credibility depends on execution capacity.
- [ ] Delivery proposals explain how quality, success, or acceptance will be evaluated.
- [ ] Main assertions are easy to find while skimming.
- [ ] Risks are visible and credible.
- [ ] The budget and timeline can be evaluated independently.
- [ ] Lists and tables use parallel wording so reviewers can compare items quickly.
- [ ] The document does not overpromise, hide uncertainty, or imply unsupported guarantees.

## Gotchas

- In formal RFP-style contexts, compliance comes before cleverness. Preserve required section order and labels unless the user says otherwise.
- Do not confuse enthusiasm with persuasion. Persuasion comes from fit, evidence, feasibility, and reviewer relevance.
- Do not hide the ask. The reviewer should know exactly what decision is needed.
