---
name: frontend-design
description: Use when a design deliverable must be produced as a durable HTML artifact — prototypes, slide decks, animations, wireframes, or UI mockups — and the work must follow a file-first, adversarially reviewed, harness-compatible workflow.
---

# Frontend Design

Use this router when the hard problem is producing a high-quality design artifact — an HTML prototype, slide deck, animation, or wireframe — with explicit scope, a design-context checkpoint, adversarial quality review, and durable learning capture.

Do not perform child phase work here. Dispatch one fresh worker per phase. Merge returned artifacts, then decide the next dispatch. If delegation is warranted for evidence gathering, prefer fresh workers; if the sprint state already makes the route clear, keep the dispatch direct.

## Core Contract

- Route to exactly one child, or say no family child fits.
- Files beat chat memory. If the sprint workspace and the conversation disagree, the workspace wins.
- One runnable design sprint at a time. Do not open a second sprint while one is active.
- Design context must exist before any artifact is built. If `context.md` is absent or untrusted, route to `design-context-scout` first.
- Human approval gates proposals before execution. `sprint_proposal.md` with `phase: "awaiting_human"` means the builder must not start until the human clears it.
- The builder does not self-approve. Only `design-reviewer` may issue a verdict.
- The reviewer is adversarial. A beautiful artifact is not evidence of a correct one.
- Retry after FAIL requires a named `clean_restore_ref` in `status.json`.
- Attempt budgets are finite. When `attempt_count >= max_attempts`, park at `escalated_to_human`.
- Compound pending work drains before a new sprint is opened.

## Decision Order

1. Check whether this family applies: the work is to produce or revise a durable design artifact (HTML prototype, deck, animation, wireframe, UI mockup).
2. Read `docs/live/tracked-work.json` to determine whether any runnable design sprint is active, parked, or queued for compounding.
3. If `compound_pending_feature_ids` is non-empty, route `design-compounder` before opening or resuming any sprint.
4. If a runnable active sprint exists, route from the strongest local artifact in `.harness/<sprint-id>/`.
5. Phase routing from strongest local artifact — in order:
   - `review.md` exists and is unreconciled → route to `state-update` (harness) before next step
   - `handoff.md` with `READY_FOR_REVIEW` and no `review.md` → `design-reviewer`
   - `contract.md` approved and `phase: "contracted"` or `"building"` → `design-builder`
   - `sprint_proposal.md` exists and `phase: "awaiting_human"` → surface to human; do not auto-dispatch
   - `context.md` exists but no `sprint_proposal.md` → `design-proposer`
   - `.harness/<sprint-id>/` folder exists with only `status.json` and no `context.md` → `design-context-scout`
6. If no runnable sprint and no active harness folder exists:
   - First read `docs/live/tracked-work.json` for a pending design feature; if found, route `design-context-scout` to begin scouting for it.
   - If no tracked feature exists yet, a `project-initializer` pass may be needed first.
7. `review_failed` with valid `clean_restore_ref` and remaining budget → `design-builder` retry.
8. `build_failed` or `review_failed` without `clean_restore_ref`, or budget exhausted → `state-update` → `escalated_to_human`.
9. `review.md` PASS → `state-update` (harness), then queue compound, then `design-compounder`.

## Phase Model

| Phase | Artifact | Owner |
|---|---|---|
| `context_needed` | nothing yet | `design-context-scout` |
| `context_ready` | `context.md` | `design-proposer` |
| `awaiting_human` | `sprint_proposal.md` | human |
| `contracted` | `contract.md` | `design-builder` |
| `building` | in-progress HTML, `runtime.md` | `design-builder` |
| `awaiting_review` | `handoff.md` | `design-reviewer` |
| `reviewed_pass` | `review.md` PASS | `state-update` → `design-compounder` |
| `reviewed_fail` | `review.md` FAIL | `design-builder` retry |
| `build_failed` | `runtime.md` with failure | `state-update` |
| `escalated_to_human` | `status.json` | human |

## Family Workflow Boundary

This router owns:
- design context scouting
- design sprint proposal and contract
- HTML artifact implementation
- adversarial design quality review
- design learning compound capture

This router does not own general harness lifecycle management. After `review.md` is written, route through `state-update` (from `using-agents-stack`) for archive, live-state reconciliation, and progress ledger updates. This family's state machine is a domain layer on top of the harness, not a replacement for it.

## Router Output

Return one of these forms, then dispatch the selected child as a fresh worker:

- `Route to frontend-design/design-context-scout.`
- `Route to frontend-design/design-proposer.`
- `Parked at awaiting_human. Surface sprint_proposal.md to human for approval.`
- `Route to frontend-design/design-builder.`
- `Route to frontend-design/design-reviewer.`
- `Route to frontend-design/design-compounder.`
- `Route to using-agents-stack/state-update.` (after review verdict or build failure)
- `Escalated to human. No family child fits without human action.`
- `No family child fits.` (if the work is not a design artifact task)
