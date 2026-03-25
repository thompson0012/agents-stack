---
name: plan-design-review
description: Use when a feature plan includes user-facing UI or UX changes and needs pre-implementation design challenge for hierarchy, states, responsiveness, accessibility, trust, and anti-slop decisions before coding starts.
---

# Plan Design Review

Use this skill to challenge a product plan's design decisions before implementation begins.

The job is to make the plan specific enough that the shipped experience feels intentional, trustworthy, and usable across real states. This is not a live UI audit, browser QA pass, or implementation skill.

## Boundary

Use this skill when:
- a feature plan includes screens, flows, dashboards, forms, settings, onboarding, messaging, or any other user-facing interaction
- the plan sounds plausible but still hides design choices behind phrases like "clean UI", "simple flow", or "standard responsive layout"
- the team needs to catch hierarchy, state, accessibility, or trust gaps before build work starts

Do not use this skill for:
- feature discovery before the core problem is clear — use `software-delivery/feature-discovery`
- PRD drafting or scope negotiation — use `feature-spec`
- visual system or token generation in isolation — use `using-design/design-foundations` or `using-design/generating-design-tokens` as needed
- implementing or QA'ing a built website or app — use `website-building`
- live browser review, screenshot critique, or component polish after code exists

## Core Contract

- Review the plan as a user experience, not a list of screens.
- Specificity beats taste words. Replace vague design adjectives with concrete decisions.
- Empty, loading, error, permission, and first-run states are part of the feature.
- Responsive and accessible behavior must be designed, not assumed.
- Trust is a design requirement whenever the interface asks for time, money, data, or irreversible action.
- Reject generic AI-slop patterns when the plan has not earned them.

## What Good Output Looks Like

Return a strengthened design plan with these sections:
1. **User and context** — who is using this, under what conditions, and what they are trying to accomplish
2. **Journey and hierarchy** — what the user sees first, second, and third across the critical path
3. **State coverage** — the designed behavior for empty, loading, error, success, edge, and permission states
4. **Interaction risks** — where confusion, distrust, overload, or accidental action could occur
5. **Required plan edits** — concrete UX decisions the plan must add before coding
6. **Handoff** — either `Ready for website-building or coding-and-data.` or `Not ready for implementation.` with the missing design decisions

## Review Workflow

### Phase 1 — Rebuild the User Situation

Extract the real context:
- primary user type and their level of familiarity
- device and environment constraints
- what they are trying to achieve now, not eventually
- what they fear losing, misunderstanding, or doing wrong
- what trust signals they need before acting

If the plan cannot say who the interface serves in this moment, stop and tighten the plan first.

### Phase 2 — Check Journey and Hierarchy

For each key screen or step, identify:
- the primary action
- the supporting context
- the secondary actions or exits
- what should visually dominate and what should recede
- what the user should understand within the first few seconds

If everything appears equally important, the plan has no hierarchy yet.

### Phase 3 — Design the States

Review the full state model, not just the happy path:
- first-use and returning-user differences
- empty, sparse, and overloaded data states
- loading and delayed work
- validation, inline errors, hard failures, and recovery paths
- destructive or irreversible actions
- permission, role, plan-tier, and feature-flag states
- success confirmation and next-step guidance

Empty states must teach, reassure, or move the user forward. Error states must tell the truth and offer a next action.

### Phase 4 — Pressure-Test Real-World Use

Challenge the plan for:
- mobile and narrow viewport behavior beyond simple stacking
- keyboard flow, focus order, touch targets, and screen-reader meaning
- long names, translated copy, dense data, and unusual but valid inputs
- interruptions, tab switching, session expiry, and offline or degraded conditions
- trust-sensitive moments like checkout, deletion, publishing, approvals, or data sharing

If the plan depends on perfect attention, perfect network, or perfect copy length, it is not ready.

### Phase 5 — Run the Anti-Slop Pass

Flag and replace generic patterns that usually signal under-designed work:
- unexplained card grids
- default dashboard layouts with no task hierarchy
- decorative hero sections in utility workflows
- placeholder empty states and vague microcopy
- component-library defaults treated as final design
- visual noise added to compensate for unclear structure

Ask what is unique about this user's task, stakes, and decision speed. The plan should look shaped by that answer.

### Phase 6 — Tighten the Plan

Turn the critique into concrete plan edits:
- specify the critical screens or steps
- name the hierarchy and primary actions
- define the missing states and recovery behavior
- call out accessibility requirements that must be true at ship time
- mark trust, copy, or interaction decisions that still need explicit resolution

End with a clear recommendation: ready now, ready after design edits, or not ready.

## Quick Checklist

- Does each step have a clear primary action?
- Is the visual and information hierarchy explicit?
- Are empty, loading, error, success, and permission states designed?
- Is mobile behavior intentional rather than merely compressed?
- Can keyboard and assistive-technology users complete the core task?
- Does the interface build trust at the moments where users feel risk?
- Would this experience still feel specific if all branding were stripped away?

## Failure Modes to Avoid

- Mistaking component selection for interaction design
- Calling a plan "clean" or "intuitive" without specifying why
- Treating accessibility as a compliance add-on instead of a design constraint
- Designing only for ideal data density, copy length, and network conditions
- Using generic AI-generated layouts that ignore user stakes and task sequence
- Deferring empty, error, and recovery states until implementation
- Letting this skill replace live implementation QA that belongs to `website-building`
