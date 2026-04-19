---
name: design-compounder
description: Use after state-update has reconciled a design sprint outcome and queued the feature id in compound_pending_feature_ids.
purpose: Distill durable design learnings — token decisions, component patterns, visual vocabulary choices, failure modes — into docs/live/memory.md and optionally into docs/reference/design.md when the lesson is stable current truth.
trigger: After `state-update` has queued the feature id in `docs/live/tracked-work.json` under `compound_pending_feature_ids`.
inputs:
  - AGENTS.md
  - docs/live/tracked-work.json
  - docs/live/memory.md
  - docs/reference/design.md
  - .harness/<sprint-id>/* or docs/archive/<sprint-id>_<timestamp>/* (decisive sprint evidence)
  - .harness/<sprint-id>/context.md
  - .harness/<sprint-id>/review.md
  - .harness/<sprint-id>/handoff.md
outputs:
  - updated docs/live/memory.md (when durable learning survives with artifact-linked provenance)
  - optional precise update to docs/reference/design.md (when the lesson is stable current truth)
  - optional scoped docs/records/* page (when durable but non-reference residue should persist)
  - updated docs/live/tracked-work.json (feature id removed from compound_pending_feature_ids)
boundaries:
  - Do not reopen proposal, execution, or review.
  - Do not claim or change runnable_active_sprint_id.
  - Do not persist chat-only conclusions or paraphrased conversation logs.
  - Do not invent lessons from a single artifact without decisive sprint evidence.
  - Do not let docs/records/* become a second contract or hidden registry.
  - Do not update docs/reference/design.md unless the lesson is genuinely stable current truth, not sprint-local observation.
next_skills:
  - design-context-scout (next sprint)
  - generator-brainstorm
  - generator-proposal
---

# Design Compounder

You are the learning phase of the design harness. Your job is to decide what, if anything, from the just-concluded sprint should become durable cross-sprint knowledge.

Compounding is explicit and non-runnable. It does not reopen any phase. It does not claim the runnable sprint slot. It extracts only what has artifact-linked provenance — not what seemed good in the conversation.

## Worker Dispatch Contract

- Run in a fresh worker context after `state-update`. Do not fold compounding into state reconciliation.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: read sprint evidence, write `docs/live/memory.md` only when durable residue survives with provenance, optionally patch `docs/reference/design.md` and scoped `docs/records/*`, and clear the queue entry in `docs/live/tracked-work.json`. No product-code edits, no `.harness/*/status.json` rewrites, no archive moves.
- Not parallel-safe against another worker touching `docs/live/memory.md` or `docs/reference/design.md`. Process one queued feature at a time.
- Dispatch framing is non-authoritative. Verify the queued feature against `docs/live/tracked-work.json` before writing.

## Required Reads

Before writing anything:
1. `AGENTS.md`
2. `docs/live/tracked-work.json` — confirm the feature is in `compound_pending_feature_ids`
3. `docs/live/memory.md` — current durable learning baseline
4. `docs/reference/design.md` — current stable reference
5. Sprint decisive evidence: `review.md`, `handoff.md`, `context.md`, `contract.md`

## What Qualifies as Durable Learning

Extract only lessons that meet all three criteria:

1. **Decisive** — drawn from `review.md` verdict, accepted `contract.md` criteria, or confirmed `handoff.md` evidence, not from the conversation or from plausible inferences.
2. **Artifact-linked** — can cite the exact sprint file and path that proves the lesson.
3. **Cross-sprint valuable** — benefits a future sprint, not just a record of what this sprint did.

### Design-specific durable lessons worth capturing

| Category | Example worth capturing |
|---|---|
| Token decisions | "Project uses `#1A1A2E` as the primary dark surface; oklch derivations for accents work better than inventing new colors." |
| Font choices | "Libre Baskerville at 600 weight reads well at 32px+ for slide headings; below 24px it becomes too heavy." |
| Component patterns | "Card hover state: `transform: translateY(-2px)` + shadow lift proved more legible than color-fill transitions at the project's density." |
| Scaffold insight | "Deck projects at 1920×1080 with `scale()` wrapper lose crisp text below 0.6x zoom; prefer SVG for diagrams." |
| Anti-pattern confirmed | "Left-border accent card was proposed in sprint DESIGN-002 and flagged by review as AI slop — reject it in all future sprints." |
| Accessibility discovery | "Project's semantic primary blue (#2563EB on white) only achieves 4.4:1 — use the +10% darker variant (#1D4ED8) for body text." |
| Variation strategy finding | "Color treatment and layout variations got the most human attention; typography-only variations were consistently ignored." |
| Review failure pattern | "React `const styles = {}` naming collision broke the Tweaks panel in DESIGN-001 and DESIGN-002; always use component-prefixed names." |

### What is not durable learning

- "The artifact looked good." — no provenance, no future value
- "We used Tailwind." — architecture fact, not a lesson
- Routine implementation steps that apply to every sprint
- Observations that contradict `review.md` evidence
- Chat-only conclusions with no artifact path

## Decision: Extract or Skip

Before writing `memory.md`, decide explicitly:

**Extract** when: at least one lesson qualifies under all three criteria above.

**Skip deliberately** when: the sprint produced no lessons that survive the criteria, or all apparent lessons lack decisive artifact provenance. Record the skip decision in `memory.md` as a one-line dated note: `[SPRINT-ID] Deliberately skipped — no durable design residue with artifact provenance found.`

Skipping is not a failure. Silently inventing lessons is.

## memory.md Entry Format

Append to `docs/live/memory.md`. Do not overwrite existing entries.

```md
## [SPRINT-ID] <short lesson title> — <ISO date>
- **Category**: token | typography | component | scaffold | anti-pattern | accessibility | variation-strategy | process
- **Lesson**: [one clear sentence stating the durable learning]
- **Evidence**: `.harness/<sprint-id>/review.md` — [exact finding id or section name]
- **Applies to**: all future sprints | sprints using [specific output type] | projects using [specific design system]
- **Provenance**: [link to decisive artifact: review.md#RV-001, contract.md#AC-002, etc.]
```

Multiple distinct lessons from one sprint each get their own entry.

## docs/reference/design.md Update

Update `docs/reference/design.md` only when the lesson is **stable current truth** — meaning it describes how the project works now, not an observation from one sprint.

Examples that justify a reference update:
- A token value was confirmed as the canonical choice and should be documented for all future builders
- A component pattern was ratified and should be the default going forward
- A known constraint (contrast issue, font limitation) applies to the whole project

Examples that do not justify a reference update:
- A lesson that only applies to slide decks in this one sprint
- A finding that may change when the design system evolves
- An advisory observation that hasn't been ratified

When updating `docs/reference/design.md`, make a precise addition or edit — do not rewrite the whole file. Note the sprint id and evidence path in a comment or footnote.

## docs/records/* Scoped Page

Create a scoped record page only when:
- Durable discussion residue is too detailed for a `memory.md` entry
- The content is not stable enough for `docs/reference/design.md`
- The feature already exists in `docs/live/tracked-work.json` with a `record_paths` field

Register the path in the feature's `record_paths` in `tracked-work.json`. Do not create a record as a substitute for `memory.md` or as a second archive.

## Queue Clearance

After writing (or deliberately skipping), remove the feature id from `compound_pending_feature_ids` in `docs/live/tracked-work.json`. This is the only mandatory write — even a skip requires it.

## Done Definition

This phase is complete when:
- The queue entry is cleared from `compound_pending_feature_ids`
- `docs/live/memory.md` either has new entries with artifact-linked provenance, or records a dated deliberate-skip note
- Any `docs/reference/design.md` update is a precise, stable-truth addition
- No phase is reopened, no runnable sprint slot is claimed
