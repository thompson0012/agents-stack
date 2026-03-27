---
name: multi-phase-control
description: Use when a vision and multi-phase roadmap must preserve original intent across phases or sessions, especially when phase gates, drift tracking, or compaction checkpoints are needed.
---

# Multi-Phase Control

## Overview

Orchestrate multi-phase work to preserve original intent across context resets, session boundaries, and phased execution. This skill sets up the persistence structure and phase gates that prevent drift from the original vision.

Use this **before** starting phase 1 when:
- A vision and multi-phase roadmap has been stated
- Work will span multiple sessions or context cycles
- Original intent must survive across phases
- The risk of drift is explicit or implied by scope

This skill does **not** implement the work itself. It sets up:
- Persistence structure (`current-focus.md`, `progress.md`)
- Phase gates with entry/exit criteria
- Compaction checkpoints
- Drift tracking

## Core Contract

- Set up persistence structure before phase 1 begins
- Track original objective AND current focus separately — drift must be explicit
- Define entry/exit criteria for each phase
- Schedule compaction checkpoints before context exhaustion
- Compose with existing skills: `harness-design` for control model, `context-compaction` for state transfer

## When This Skill Applies

| Situation | Trigger |
|-----------|---------|
| Vision + phased roadmap stated | User presents a multi-phase plan and asks to begin phase 1 |
| Cross-session continuity needed | Work will span multiple sessions or context resets |
| Drift risk explicit | User mentions "preserve", "maintain", "don't lose", "original intent" |
| Handoff between agents | Need to transfer state to another session/agent |

Do NOT use when:
- Single-session work with no phases
- Implementation details only — no control structure needed
- Request just asks for a plan without execution

## Workflow

### Phase 1 — Capture Vision and Roadmap

Before any implementation work:

0. **Do not write real session state into `templates/base/docs/live/`** — those files are template skeletons for downstream projects.

1. **Read source of truth** — Where is the vision/roadmap documented? If only in conversation, persist it.
2. **Create or update the consuming project's `docs/live/current-focus.md`** using `assets/current-focus-template.md` as the starter shape:
   ```markdown
   # Current Focus
   
   ## Original Objective
   [Verbatim from source — what the session was originally opened to do]
   
   ## Current Focus  
   [What is actively being worked on right now — starts same as original]
   
   ## Scope
   ### In Scope
   - [Item 1]
   - [Item 2]
   
   ### Explicitly Out of Scope
   - [Item 1]
   - [Item 2]
   
   ## Success Criteria
   - [ ] [Criterion 1]
   - [ ] [Criterion 2]
   
   ## Phase Breakdown
   | Phase | Objective | Entry Criteria | Exit Criteria |
   |-------|-----------|---------------|---------------|
   | 1 | [objective] | [what must exist before starting] | [what must be verified before next phase] |
   | 2 | [objective] | [depends on phase 1 exit] | [what must be verified before next phase] |
   
   ## Drift Log
   | Date | Original | Current | Reason |
   |------|----------|---------|--------|
   | [initial] | [original objective] | [same as original] | Initial state |
   ```

3. **Create or update the consuming project's `docs/live/progress.md`** using `assets/progress-template.md` as the starter shape:
   ```markdown
   # Progress
   
   ## State
   - Phase: [current phase number]
   - Status: planning / in-progress / blocked / complete
   - Last Action: [what was just done]
   - Next Action: [what must happen first on resume]
   
   ## Completed
   - [x] [Milestone 1]: [result/output]
   
   ## In Progress
   - [ ] [Current task]
   
   ## Blocked
   - [ ] [Blocker]: [reason]
   
   ## Touched Files
   | File | Status | Notes |
   |------|--------|-------|
   | [path] | modified/created/pending | [brief note] |
   
   ## Verification Status
   | Check | Status | Evidence |
   |-------|--------|----------|
   | [check name] | passed/failed/pending | [link or summary] |
   ```

### Phase 2 — Choose Control Model

Invoke `harness-design` to select the appropriate execution mode:

| Mode | When to Use |
|------|-------------|
| `single-session` | All phases fit in one session — no control structure needed |
| `compacted-continuation` | Same role continues across sessions — context compaction required |
| `planner-generator-evaluator` | Phases require independent verification — role separation needed |

Record the chosen mode in the consuming project's `docs/live/runtime.md` when runtime control is needed:
```markdown
# Runtime

## Execution Mode
[compacted-continuation | planner-generator-evaluator]

## Baton Owner
[planner | generator | evaluator — who owns the next action]

## Role Boundaries
- Planner owns: [scope, contracts, acceptance gates]
- Generator owns: [implementation inside boundary]
- Evaluator owns: [independent verification]
```

### Phase 3 — Define Phase Gates

For each phase in the roadmap:

1. **Entry Criteria** — What must exist before starting?
   - Previous phase exit criteria met?
   - Dependencies resolved?
   - Clear acceptance gate defined?

2. **Exit Criteria** — What must be verified before moving on?
   - Concrete deliverables produced?
   - Tests passing?
   - Documentation updated?
   - `progress.md` reflects current truth?

3. **Compaction Checkpoint** — When to checkpoint before context exhaustion?
   - Before phase transition
   - After significant decisions
   - When context approaches limits

### Phase 4 — Enable Recovery After Reset

Before context exhaustion or session end:

1. **Invoke `context-compaction`** to produce continuation snapshot
2. **Update `progress.md`** with:
   - Current phase and status
   - What was just done
   - What must happen next
   - Touched files
   - Verification status

3. **Track drift explicitly** — If original objective ≠ current focus:
    - Add entry to Drift Log in `current-focus.md`
    - Explain why focus changed
    - Confirm user acceptance if scope changed

### Phase 5 — Bind to Existing Skills

Compose with existing skills as needed:

| Skill | When to Invoke |
|-------|----------------|
| `harness-design` | Control model is unclear or needs explicit selection |
| `context-compaction` | At checkpoints or before context exhaustion |
| `feature-spec` | Phase needs requirements document |
| `verification-before-completion` | Before claiming phase complete |

## References

- [phase-gates.md](references/phase-gates.md) — Detailed gate patterns and anti-patterns
- [drift-detection.md](references/drift-detection.md) — How to detect drift early
- [composition.md](references/composition.md) — How this skill composes with others

## Assets

- [current-focus-template.md](assets/current-focus-template.md) — Starter template for `docs/live/current-focus.md`
- [progress-template.md](assets/progress-template.md) — Starter template for `docs/live/progress.md`
- [runtime-template.md](assets/runtime-template.md) — Starter template for `docs/live/runtime.md`

## How to Resume

When resuming multi-phase work:

1. Read the consuming project's `AGENTS.md` → `docs/live/current-focus.md` → `docs/live/progress.md`
2. Check drift log — has objective changed?
3. Check phase status — which phase, entry/exit criteria
4. Continue from "Next Action" in progress

## Evaluation

Realistic prompts in `evals/evals.json`:
1. Direct match — user presents multi-phase roadmap and asks to start phase 1
2. Ambiguous case — user mentions "phases" but unclear if persistence structure needed
3. Adversarial — context is long, user asks to "just continue" without resetting

## Final Checklist

- [ ] `current-focus.md` created with original objective and phase breakdown
- [ ] `progress.md` created with state tracking
- [ ] Live docs were written in the consuming project, not in `templates/base/docs/live/`
- [ ] Control model chosen (single-session, compacted-continuation, or planner-generator-evaluator)
- [ ] Entry/exit criteria defined for each phase
- [ ] Compaction checkpoint scheduled if needed
- [ ] Drift tracking structure in place
- [ ] User can resume by reading `current-focus.md` → `progress.md`
