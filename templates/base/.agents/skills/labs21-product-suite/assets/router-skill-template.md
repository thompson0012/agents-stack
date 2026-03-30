---
name: router-name
description: Use when requests need to be routed across a related skill family and the agent must pick one child path explicitly.
---

# Router Name

## Overview
Describe the family boundary this router owns and what kinds of requests should enter here before a leaf skill is chosen.

## Core Contract
- Route to exactly one child or say no child fits.
- Use `references/children.json` as the source of truth for child selection, install hints, and fallbacks.
- Do not solve the child skill's full job inside the router.
- Do not silently degrade when the best child is missing. Install it or disclose the fallback.

## Decision Order
1. Check whether the request belongs in this family at all.
2. Apply the ordered selection logic from `references/children.json`.
3. Pick the narrowest child that honestly fits.
4. If the child is missing, install it when allowed or disclose the fallback.
5. Hand off to the selected child.

## Router Output
Return one of these forms and then invoke the selected child if needed:
- `Route to <child-path>.`
- `Install <child-path>, then route to <child-path>.`
- `Fallback to <fallback-path>.`
- `No family child fits; answer directly.`

Add one sentence explaining why the selected child is the narrowest correct fit.

## References
- `references/children.json`
- Add any family-specific reference files needed for boundary or edge-case detail.

## Final Checklist
- [ ] Router stays focused on selection and handoff
- [ ] Child inventory is current in `references/children.json`
- [ ] Missing/install/fallback behavior is explicit
- [ ] Validation completed
