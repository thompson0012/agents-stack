---
name: __SKILL_NAME__
description: Use when __TRIGGER__.
---

# __SKILL_TITLE__

## Overview
__OVERVIEW__

## Core Contract
- State the non-negotiable rule this skill enforces.
- Keep the scope narrow enough that another agent can tell when to load it.

## Workflow
1. Capture the minimum required inputs.
2. Execute the workflow in the smallest reliable sequence.
3. Validate the output before calling the task done.

## References
- Add `references/...` links only for detail that does not belong inline.

## Evaluation
- Add at least 3 realistic prompts to `evals/evals.json`.
- Add `evals/trigger-evals.json` if discovery precision matters.
- Compare the candidate against an honest baseline when behavior changed.

## Final Checklist
- [ ] Trigger conditions are clear in `description`
- [ ] Body explains execution, not discovery
- [ ] Linked local files exist
- [ ] Validation and evaluation are complete
