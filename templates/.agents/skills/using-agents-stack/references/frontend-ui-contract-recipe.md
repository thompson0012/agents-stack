# Frontend UI Contract Recipe

This reference helps agents-stack proposal and review workers make frontend UI work observable without inventing a second contract.
It is guidance, not a harness contract. If it conflicts with `AGENTS.md`, `.harness/<id>/contract.md`, or the state-machine rules, those sources win.

## When to consult

Use this reference when the selected work is frontend UI or browser-visible interaction and the prompt or proposal would otherwise be too generic.
It is especially useful when the surface needs layout, interaction flow, and data-shape clarity before code exists.

## Prompt-side structure

When a UI contract recipe is useful, prefer the lightest structure that still answers the risk:

- `Mermaid_Logic` for state, branching, and failure flow
- `ASCII_Layout` for spatial hierarchy and composition
- `Data_Schema` only when typed renderer payloads or data binding are part of the risk
- `contract_check` as a private preflight rubric, not a canonical wire format

## What the proposal or review should make observable

For browser-visible UI work, the contract or proposal should usually name:

- the route, page, or component
- the starting state the reviewer must see before acting
- the action the reviewer performs
- the expected after-state
- the reverse or repeated action when the behavior should be reversible or toggleable
- the viewport or device class when layout matters
- the selector, label, or visible text that proves the state changed because of the action, not just because a final state was already rendered
- loading, empty, error, and retry states when those are in scope

## Guardrails

- Do not make these blocks mandatory for all frontend work.
- Do not replace `.harness/<id>/contract.md` as the canonical sprint contract.
- Do not use this reference to bypass real-browser validation.
- Proposal and review workers should tighten the slice or fail it when the signoff could be reward-hacked by a hardcoded final DOM, static screenshot, canned response, or other fake green path that never proves the transition.
- For toggles, undo flows, and other reversible interactions, require proof of the forward transition and the reversal instead of accepting a one-way final state.
- If the browser-visible proof cannot distinguish a real interaction from a seeded end state, the sprint is not review-ready yet.
- Keep diagrams disposable; regenerate them when the code or contract changes.
- For browser signoff, use `frontend-qa`.
- If the selected work is not frontend, skip this reference.
