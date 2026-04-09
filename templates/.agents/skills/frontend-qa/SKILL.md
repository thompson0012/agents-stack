---
name: frontend-qa
description: Use when validating frontend behavior in a real browser, including functional flows, visual quality, accessibility, responsive behavior, perceived performance, or adversarial edge cases.
---

# Frontend QA

## Overview
Frontend QA is real-browser, evidence-first validation of what users actually experience. Judge the product through the lens of Utility × Usability × Craft: does it solve the right job, does it stay understandable under real interaction, and does it feel intentional instead of merely unbroken.

## Core Contract
- Test the real browser path before signoff.
- A screenshot, DOM dump, or code inspection is not proof by itself; it only supports the browser evidence.
- Separate functional, visual, accessibility, performance, responsive, and adversarial coverage.
- Judge observable behavior, not implementation intent.
- Treat loading, empty, error, retry, back-navigation, and dense-content states as first-class.
- Record evidence from the browser state where each claim is true, including the interaction that produced it.


## When to use
Use this skill when a frontend surface needs honest browser validation before signoff, release, handoff, or bug triage.

## When not to use
Do not use this skill for backend-only correctness, static design critique without a browser, or implementation work that is not about validation.

## Workflow
1. Build a QA inventory from requirements, visible UI claims, risky states, and signoff claims.
2. Run a functional browser pass on the critical journeys and reversible interactions.
3. Run a visual pass on the initial viewport, post-interaction states, dense states, and the smallest supported viewport.
4. Run an accessibility pass covering semantics, keyboard flow, focus visibility, contrast, announcements, and touch targets.
5. Run a perceived-performance pass covering load behavior, navigation smoothness, layout stability, and back/forward behavior.
6. Run an adversarial pass with malformed content, extreme lengths, unusual locale text, rapid interaction, failure states, and resize or zoom stress.
7. Record findings with reproduction steps, evidence, severity, and explicit unverified gaps.

## References
- [Framework](references/framework.md)
- [Playbook](references/playbook.md)
- [Reporting](references/reporting.md)

## Failure Modes
- Confusing a passing happy path with signoff.
- Treating screenshots without reproduction context as sufficient evidence.
- Checking only desktop or only clean data.
- Calling a screen acceptable because it is technically functional while still confusing, slow, inaccessible, or brittle.

## Final Checklist
- [ ] QA inventory covers requirements, visible claims, and risky states.
- [ ] Functional, visual, accessibility, performance, responsive, and adversarial passes were run.
- [ ] Evidence exists for each pass.
- [ ] Each claim was proven in a real browser state, not only by screenshots, DOM snapshots, or code review.
- [ ] Findings distinguish real failures from unverified areas.
- [ ] Signoff reflects Utility × Usability × Craft, not just absence of crashes.