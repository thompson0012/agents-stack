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
- the action the reviewer performs
- the expected after-state
- the viewport or device class when layout matters
- the selector, label, or visible text that proves the state changed
- loading, empty, error, and retry states when those are in scope

## Guardrails

- Do not make these blocks mandatory for all frontend work.
- Do not replace `.harness/<id>/contract.md` as the canonical sprint contract.
- Do not use this reference to bypass real-browser validation.
- Keep diagrams disposable; regenerate them when the code or contract changes.
- For browser signoff, use `frontend-qa`.
- If the selected work is not frontend, skip this reference.
