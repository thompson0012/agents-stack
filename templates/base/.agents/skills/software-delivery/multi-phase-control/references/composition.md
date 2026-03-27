# Composition

How `multi-phase-control` composes with other skills.

## Composition Model

`multi-phase-control` is a **workflow orchestrator**. It sets up structure and delegates specialized work to other skills.

```
multi-phase-control (orchestrator)
├── harness-design (control model selection)
├── context-compaction (state transfer)
├── feature-spec (requirements per phase)
├── verification-before-completion (phase completion)
└── docs/live/ structure (shared convention)
```

## When to Invoke Each Skill

### harness-design

**When:** Control model unclear at start of multi-phase work

**Why:** Need to decide between `single-session`, `compacted-continuation`, or `planner-generator-evaluator`

**Integration:**
- Called by `multi-phase-control` Phase 2
- Records chosen mode in the consuming project's `docs/live/runtime.md`
- Provides role ownership boundaries
- Supplies the runtime contract that `multi-phase-control` uses for phase execution

### context-compaction

**When:** Context approaching limits, session ending, or before phase transition

**Why:** Preserve state for continuation without loss

**Integration:**
- Scheduled by `multi-phase-control` Phase 3 (compaction checkpoint)
- Reads from `current-focus.md` and `progress.md`
- Produces continuation snapshot that references these files
- Uses the consuming project's `docs/live/` root, not the template repo's live-doc skeletons

### feature-spec

**When:** A phase needs detailed requirements beyond the roadmap

**Why:** Phase 1 of a larger roadmap may need its own spec

**Integration:**
- Can be invoked per-phase
- Spec should reference parent `current-focus.md`
- Phase completion updates `progress.md`

### verification-before-completion

**When:** About to claim phase complete

**Why:** Ensure exit criteria verified before transition

**Integration:**
- Checks against exit criteria in `current-focus.md`
- Updates verification status in `progress.md`
- Provides evidence for gate passage

### QA evidence handoff

**When:** Out-of-scope findings or explicit independent acceptance exist

**Why:** Keep current verdicts honest while preserving separate follow-up items

**Integration:**
- Use `qa.md` for in-scope verdicts and separate out-of-scope findings
- Keep retry ownership distinct from scope follow-ups

## Shared Conventions

### Live Docs Structure

The templates in this skill package seed the consuming project's `docs/live/` files. Do not treat `templates/base/docs/live/` as actual session state.

Multiple skills read/write to the consuming project's `docs/live/`:

| File | Owner | Skills That Read |
|------|-------|------------------|
| `current-focus.md` | multi-phase-control | context-compaction, feature-spec, verification |
| `progress.md` | multi-phase-control | context-compaction, verification |
| `runtime.md` | harness-design | multi-phase-control, context-compaction |
| `qa.md` | evaluator (if exists) | verification |

### Read Order

All skills should follow:

```
AGENTS.md → docs/live/current-focus.md → docs/live/progress.md
```

Then read additional docs as needed.

### State Consistency

Before any handoff:
- `current-focus.md` reflects original objective and current focus
- `progress.md` reflects actual state, not aspirational state
- Drift log is up to date

## Composition Patterns

### Pattern 1: Simple Multi-Phase

```
User: "Build X in 3 phases, preserve across sessions"

multi-phase-control
├── Create current-focus.md + progress.md
├── Phase gates defined
├── harness-design → compacted-continuation
└── context-compaction at checkpoints
```

No evaluator needed — same role continues.

### Pattern 2: Multi-Phase with Verification

```
User: "Build X in 3 phases, I want independent review each phase"

multi-phase-control
├── Create current-focus.md + progress.md
├── harness-design → planner-generator-evaluator
├── Phase 1: planner defines, generator builds, evaluator checks
├── Phase 2: planner updates, generator builds, evaluator checks
└── etc.
```

Role separation enabled by `harness-design` output.

### Pattern 3: Recovery After Drift

```
Agent detects drift (current focus ≠ original objective, no drift log)

multi-phase-control
├── Read current-focus.md → detect drift log gap
├── Stop implementation
├── Add to drift log with explanation
├── Confirm with user OR rollback
└── Resume with clear current focus
```

## What `multi-phase-control` Does NOT Do

| Responsibility | Owned By |
|-----------------|----------|
| Implement phases | generator / implementer |
| Verify phases | verifier / evaluator |
| Choose single vs multi-session | harness-design |
| Produce continuation snapshot | context-compaction |
| Write feature spec | feature-spec |

`multi-phase-control` sets up, tracks, and delegates.
