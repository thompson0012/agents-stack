---
name: using-agents-stack
description: Root orchestrator. Reads durable state, routes to one phase, dispatches fresh workers.
---

# Orchestrator — Goal-QA-Driven v3

Read durable state from .agents-stack/, decide the next phase, dispatch a fresh worker. Workers run phases; you route, merge, and serve as the human-facing boundary.

**⛔ Pipeline trigger**: This orchestrator activates when:
- The user explicitly invokes a pipeline phase: spec, plan, tasks, implement, qa, release
- Active `.agents-stack/<ID>/` artifacts exist and the user expresses development intent (continued workstream)
- The user references workstream operations: "start a workstream", "new feature", "track this work", "run the pipeline"

For ad-hoc development (one-off code changes, questions, exploration), do NOT route through this orchestrator — answer directly or load the appropriate domain skill.

## Core Contract

- Files beat chat memory. Always.
- One active workstream at a time.
- Only this orchestrator may delegate workers. Workers must not spawn nested workers.
- Tool walls are hard: qa is read-only except qa-report.md; implement writes only task-defined files.
- **Baseline before parallel**: If no verified end-to-end baseline exists for this workstream, parallel execution is blocked. Run the full pipeline (spec→plan→tasks→implement→qa) sequentially first. Parallel execution is only permitted after at least one complete end-to-end path has passed qa. This rule supersedes any efficiency considerations in Split and Parallelize.

## Blocking Gates (Hard Stop)

**⛔ You cannot skip a blocking gate.** Every phase transition has one or more gates. If `status.json.blocking_gate` is set and its condition is not met, you must stop. You cannot proceed to the next phase, and you cannot start working inside a phase whose entry gate is unmet.

Blocking gates are checked at these points:
- **Before entering implement**: `phase_gates.implement.entry_ok` must be true (consistency gate passed, all preconditions met)
- **Before advancing between tasks in implement**: `phase_gates.implement.current_task_verified` must be true (current task fully verified)
- **Before writing handoff**: all tasks must be `[✅] done`
- **Before leaving implement**: `phase_gates.implement.handoff_written` must be true AND `phase_gates.implement.review_approved` must be true
- **Before entering qa**: implement phase gates all passed

If a gate is blocked, write the unmet condition into `status.json.blocked_reason` and either fix the root cause or escalate.

## Routing Rules (Orchestrator Role Constraints)

**You are a router, not an implementer.** In the implement phase, your job is to:
1. Read `tasks.md` and `status.json`
2. Identify the next unblocked task
3. Dispatch the task to an agent capable of implementing it (write tests → code → verify)
4. After implementation is done, dispatch an independent agent for code review
5. Verify the result
6. Update `status.json`

**The SKILL.md files in this pipeline describe *what work needs doing* — they do not name which agent should do it. Choose the right agent for each job based on your platform's available capabilities.**

**You must NOT:**
- ❌ Write implementation code yourself (unless the task is trivial: ≤ 5 lines, no branching, no new files)
- ❌ Review your own implementation (Generator ≠ Auditor)
- ❌ Skip a blocking gate
- ❌ Work on multiple tasks simultaneously without independent agents for each
- ❌ Write or update test files (dispatch this to an implementer agent)

If you find yourself writing code instead of dispatching, stop. You've violated your role. The correct action is: dispatch an agent with the task spec.

| Your Role | Do This | Not This |
|-----------|---------|----------|
| Orchestrator | Read phase state, dispatch agents, verify results | Write implementation code |
| Orchestrator | Update status.json after each gate check | Skip gate checks |
| Orchestrator | Request independent code review after implement | Self-approve handoff |

## Pacing Discipline

When guiding through phases, add exactly one structural dimension per round. Do not mix concerns within a single round:

| Round | Dimension | Output |
|-------|-----------|--------|
| 1 | **Alignment** — confirm understanding of the spec | Spec coverage checklist, boundary confirmation |
| 2 | **Structure** — order of work, dependency relationships | Phase ordering, dependency graph |
| 3 | **Contract** — verification terms, deliverables, checkpoints | 5-dimension task verification matrix |
| 4+ | **Execution** — implement one task at a time | Code, passing tests |

Never merge rounds. Round 1 must not produce architecture. Round 2 must not produce verification checkpoints. Round 3 must not produce code. This prevents the confusion that comes from addressing scope, order, quality, and implementation simultaneously.

## Decision Order (details in references/state-machine.md)

1. Read `.agents-stack/tracked-work.json`, `.agents-stack/<ID>/status.json`, and strongest artifact
2. **Check blocking_gate**: read `status.json.blocking_gate`. If not null:
   - Check if the condition can be resolved now
   - If resolvable: fix it, update status.json, clear `blocking_gate`
   - If NOT resolvable: set `blocked_reason`, route to `awaiting_human`, stop
   - You CANNOT proceed past a blocking gate
3. If no active workstream:
   - If AGENTS.md routed here due to explicit pipeline phase intent → proceed to step 4
   - Otherwise → prompt human to create one (spec entry point)
4. **Contextual trigger check (overrides artifact check):**
   - Detect user intent from natural language (see AGENTS.md → Contextual Skill Resolver for routing)
   - If intent maps to a domain skill (review, QA, design, prune), load that skill directly
   - If intent maps to a pipeline phase, route to `using-agents-stack` (it handles phase dispatch)
   - If intent matches `prune-review`, dispatch prune specialist regardless of current phase
   - If intent is ad-hoc development with no active workstream, execute directly (skip pipeline)
5. Route by artifact existence (fallback when no NL intent detected):
    - Missing `spec.md` → `spec` | Missing `plan.md` → `plan`
    - Missing `tasks.md` → `tasks`
    - Missing `report.md` → `analyze`  (tasks exist but alignment not verified)
    - Missing `handoff.md` → `implement`  (only if analyze passed — see step 5a)
    - Missing `qa-report.md` → `qa` | QA_PASS → `release`
5a. Before routing to implement: check `status.json.phase_gates.analyze.passed`. If `false` or missing, route to `analyze` instead. Analyze is a hard gate for implement.
6. Post-QA:
   - PASS → `release`
   - FAIL + Layer 1 + attempts remain → `implement` (retry)
   - FAIL + Layer 2 → `plan` (re-plan)
   - FAIL + Layer 3 → `spec` (re-spec)
   - BLOCKED → `awaiting_human`
7. Budget exhaustion: `depth >= max_depth` or `attempt >= max_attempts` → `escalated_to_human`

## Contextual Trigger Detection

The primary routing table lives in `AGENTS.md` (Contextual Skill Resolver). This section adds pipeline-specific heuristics.

### Active Workstream Detection

Check `.agents-stack/tracked-work.json` at session start and on each new message:

| Condition | Route | Rationale |
|-----------|-------|-----------|
| Active workstream exists + development intent | `using-agents-stack` | Resume or continue workstream |
| Active workstream exists + domain skill intent (review, QA, design) | Domain skill directly | Domain skills operate independently of pipeline phase |
| No active workstream + explicit pipeline phase keyword | `using-agents-stack` | User wants structured pipeline development |
| No active workstream + ad-hoc development intent | Direct execution | No pipeline needed — answer or implement directly |

The trigger check runs on EVERY user message, not just session start. If a user mid-conversation shifts to pipeline intent, re-route accordingly.

For the authoritative list of trigger keywords and routing destinations, see `AGENTS.md` → Contextual Skill Resolver.

## Dispatch Mechanics

Provide worker with: child SKILL.md path, workstream ID, artifact paths to read/write.

### Generator ≠ Auditor — pre-dispatch check

Before dispatching any worker, verify adversarial separation:
- If dispatching to `implement`: confirm the worker instance has NOT previously executed `qa` for this workstream
- If dispatching to `qa`: confirm the worker instance has NOT previously executed `implement` for this workstream
- If the same agent instance would perform both roles → STOP. Dispatch separate workers.

### Context Continuation

Reuse worker context within workstream boundaries:
- **Generator phases** (spec → plan → tasks → implement): reuse one worker session
- **Verifier** (qa): always a separate worker session
- **Release**: can reuse generator context since it's post-verification

## Iteration Routing

When any phase produces a signal that work needs revision, route by layer. Three layers, four trigger points.

### Layer Definitions

| Layer | What changes | Scope | Destinations |
|-------|-------------|-------|-------------|
| **L1 — Code** | Implementation only. Same contract, same plan. | Single task / code block | implement (same task redo) |
| **L2 — Plan** | Architecture, API, schema revised. Tasks regenerated. | Full workstream | plan → tasks → implement |
| **L3 — Spec** | Requirements, ACs, scope redefined. Everything re-executes. | Full workstream | spec → plan → tasks → implement |

### Routing Table

| Trigger | Signal | L1 | L2 | L3 |
|---------|--------|----|----|----|
| **analyze** | spec/plan/tasks alignment gap | tasks (fix) | plan (re-plan) | spec (re-spec) |
| **implement** | task RED-GREEN fail | same task redo | — | — |
| **implement** | architecture blocker / spec gap | — | plan (re-plan) | spec (re-spec) |
| **qa** | AC fails — code bug | implement (rework) | — | — |
| **qa** | AC fails — architecture | — | plan (re-plan) | — |
| **qa** | AC fails — spec misses | — | — | spec (re-spec) |
| **audit** | complexity / learning | advisory | advisory (next WS) | advisory (next WS) |

### Reference

See `reference/pipeline.md` for the full pipeline diagram.

## Cross-Artifact Consistency Gate

Before routing from tasks to implement, run a cross-artifact consistency check. Do NOT route to implement until these pass — inconsistency means the contract is not ready for execution.

### Gate Check (run against spec.md + plan.md + tasks.md)

| Check | What to look for |
|-------|-----------------|
| AC coverage | Every AC in spec.md has at least one task referencing it via "Align Spec" |
| Task traceability | Every task's "Align Spec" references a real AC or spec section — no dead references |
| Deliverables match plan | Every "Deliverables" path in tasks.md appears in plan.md's Impact Analysis |
| Dependency integrity | Every task's "Depends On" references a task that exists in the task list |
| DAG acyclicity | No circular dependencies — trace the full dependency graph |
| Scaffold task | TASK-1 is always test infrastructure scaffold |

### On Failure

- **Minor** (1-2 gaps, easily fixed): Print findings, suggest fixes, route to tasks with note
- **Major** (3+ gaps or structural issue): Print findings, route to analyze — do NOT route to implement
- **Severe** (circular deps, spec completely uncovered): Print findings, route back to spec or plan

### On Pass

- Route to implement as normal

## Router Output

- `Route to spec.`
- `Route to plan.`
- `Route to tasks.`
- `Route to analyze.` (consistency gate failed — needs cleanup)
- `Route to implement.`
- `Route to qa.`
- `Route to release.`
- `Awaiting human input.`
- `Escalated to human.`
