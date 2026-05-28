---
name: frontend-design
description: Use when a design deliverable must be produced as a durable HTML artifact — prototypes, slide decks, animations, wireframes, or UI mockups — and the work must follow a file-first, adversarially reviewed, harness-compatible workflow.
---

# Frontend Design

Use this router when the hard problem is producing a high-quality design artifact — an HTML prototype, slide deck, animation, or wireframe — with explicit scope, a design-context checkpoint, adversarial quality review, and durable learning capture.

Do not perform child phase work here. Dispatch one fresh worker per phase. Merge returned artifacts, then decide the next dispatch. If delegation is warranted for evidence gathering, prefer fresh workers; if the sprint state already makes the route clear, keep the dispatch direct.
Each child lives under `frontend-design/<child-name>/`, and child SKILL.md files should say they are nested design-family workers.

## Core Contract

- Route to exactly one child, or say no family child fits.
- Files beat chat memory. If the sprint workspace and the conversation disagree, the workspace wins.
- One runnable design sprint at a time. Do not open a second sprint while one is active.
- Design spec must exist before any artifact is built. If `design.md` is absent or its phase is `design_needed`, route to `design-context-scout` first.
- Human approval gates proposals before execution. `design.md` with `phase: "awaiting_human"` means the builder must not start until the human clears it.
- The builder does not self-approve. Only `design-reviewer` may issue a verdict.
- The reviewer is adversarial. A beautiful artifact is not evidence of a correct one.
- Retry after FAIL requires a named `clean_restore_ref` in `status.json`.
- Attempt budgets are finite. When `attempt_count >= max_attempts`, park at `escalated_to_human`.
- Compound pending work drains before a new sprint is opened.

## Decision Order

1. Check whether this family applies: the work is to produce or revise a durable design artifact (HTML prototype, deck, animation, wireframe, UI mockup).
2. Read `.agents-stack/tracked-work.json` to determine whether any runnable design sprint is active, parked, or queued for compounding.
3. If `compound_pending_feature_ids` is non-empty, route `design-compounder` before opening or resuming any sprint.
4. If a runnable active sprint exists, route from the strongest local artifact in `.agents-stack/<sprint-id>/`.
5. Phase routing from strongest local artifact — in order:
   - `design-qa.md` exists and is unreconciled → route to `orchestrator` (harness) before next step
   - `design-handoff.md` with `READY_FOR_REVIEW` and no `design-qa.md` → `design-reviewer`
    - `design.md` with `phase: "design_contracted"` → `design-builder` (prototype validation is now an optional pre-build step within builder)
   - `design.md` exists and `phase: "approved"` (human-approved, contract not yet finalized) → `design-proposer` to formalize the contract
   - `design.md` exists and `phase: "awaiting_human"` → surface to human; do not auto-dispatch
   - `design.md` exists with `no_design_system_found: true` and `phase: "awaiting_human"` → surface to human; do not advance to proposer until human provides design reference
   - `design.md` exists with `phase: "design_spec"` (scout completed, no proposal yet) → `design-proposer`
   - `.agents-stack/<sprint-id>/` folder exists with only `status.json` and no `design.md` → `design-context-scout`
6. If no runnable sprint and no active harness folder exists:
   - First read `.agents-stack/tracked-work.json` for a pending design feature; if found, route `design-context-scout` to begin scouting for it.
   - If no tracked feature exists yet, a `project-initializer` pass may be needed first.
7. `qa_fail` with valid `clean_restore_ref` and remaining budget → `design-builder` retry.
8. `qa_blocked` → route to `orchestrator` (harness) to record the blocker, then surface to human. Do not auto-retry a BLOCKED verdict.
9. `build_error` or `qa_fail` without `clean_restore_ref`, or budget exhausted → `orchestrator` → `escalated_to_human`.
10. `design-qa.md` PASS → route to `orchestrator` (harness) to reconcile verdict and queue compound.
11. After `orchestrator` confirms `compound_pending_feature_ids` is non-empty → route to `design-compounder`.
12. After `design-compounder` clears the queue → sprint is complete; open next sprint if pending.

## Phase Model

| Phase | Artifact | Owner |
|---|---|---|
| `design_needed` | nothing yet | `design-context-scout` |
| `design_spec` | `design.md` | `design-proposer` |
| `awaiting_human` | `design.md` | human |
| `design_contracted` | `design.md` | `design-builder` |
| `building` | in-progress HTML, `design-handoff.md` | `design-builder` |
| `awaiting_review` | `design-handoff.md` | `design-reviewer` |
| `qa_pass` | `design-qa.md` PASS | `orchestrator` → `design-compounder` |
| `qa_fail` | `design-qa.md` FAIL | `design-builder` retry |
| `qa_blocked` | `design-qa.md` BLOCKED | `orchestrator` → human |
| `build_error` | `design-handoff.md` with failure | `orchestrator` |
| `escalated_to_human` | `status.json` | human |

## Family Workflow Boundary

This router owns:
- design context scouting
- design sprint proposal and contract
- HTML artifact implementation
- adversarial design quality review
- design learning compound capture

This router does not own general harness lifecycle management. After `design-qa.md` is written, route through `orchestrator` (from `using-agents-stack`) for archive, live-state reconciliation, and progress ledger updates. This family's state machine is a domain layer on top of the harness, not a replacement for it.

## Router Output

Return one of these forms, then dispatch the selected child as a fresh worker:

- `Route to frontend-design/design-context-scout.`
- `Route to frontend-design/design-proposer.`
- `Parked at awaiting_human. Surface design.md to human for approval.`
- `Route to frontend-design/design-builder.`
- `Route to frontend-design/design-reviewer.`
- `Route to frontend-design/design-compounder.`
- `Route to using-agents-stack (root orchestrator).` (after review verdict or build failure)
- `Escalated to human. No family child fits without human action.`
- `No family child fits.` (if the work is not a design artifact task)

## References

- [design-quality-contract-recipe](references/design-quality-contract-recipe.md)

## Final Checklist

- [ ] Only one routing target selected per session
- [ ] `compound_pending_feature_ids` checked before opening a new sprint
- [ ] `design.md` verified present before routing to `design-proposer`
- [ ] `awaiting_human` phase not auto-dispatched — surfaced to human
- [ ] `orchestrator` invoked after every review verdict (PASS, FAIL, or BLOCKED)
- [ ] `qa_blocked` routes to `orchestrator` + human, not to builder retry
- [ ] `qa_pass` sequence: `orchestrator` → confirm compound queued → `design-compounder`
- [ ] Children inventory in `references/children.json` is current
