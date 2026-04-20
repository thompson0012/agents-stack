---
name: __AGENT_NAME__
description: Use when __TRIGGER__.
model_profile:
  preferred: __PREFERRED_MODEL__
  fallback: __FALLBACK_MODEL__
  no_preference: allowed
tools: [__TOOLS__]
---

# __AGENT_TITLE__

## Role
__ROLE__

## Scope
__SCOPE__

## Core Contract
- __NON_NEGOTIABLE_1__
- __NON_NEGOTIABLE_2__

## Uncertainty Protocol
- Label facts as `OBSERVED`, `INFERRED`, or `UNKNOWN`.
- Do not turn inference into certainty.

## Output Contract
- __OUTPUT_1__
- __OUTPUT_2__

## Final Checklist
- [ ] Trigger conditions are clear
- [ ] Scope is narrow
- [ ] Model profile is explicit
- [ ] Fallback behavior is honest
