# Pipeline: v4

```
                    ┌───────────────────────────────────────────┐
                    │           ITERATION  ROUTING              │
                    │                                           │
                    │  L1 ──→ re-execute same scope             │
                    │  L2 ──→ revise plan, re-task, re-code     │
                    │  L3 ──→ revise spec, re-everything        │
                    └─────────────────┬─────────────────────────┘
                                      │ feeds into
                                      ▼
┌──────┐   ┌──────┐   ┌───────┐   ┌──────────┐   ┌──────────┐   ┌──────┐   ┌───────┐
│ spec │──→│ plan │──→│ tasks │──→│ analyze  │──→│implement │──→│  qa  │──→│ audit │
└──┬───┘   └──┬───┘   └───┬───┘   └────┬─────┘   └────┬─────┘   └──┬───┘   └───┬───┘
   │          │          │            │             │          │          │
   │          │          │            ├── L1 ───────┤          │          │
   │          │          │            │   (fix tasks)           │          │
   │          │          │            │                          │          │
   │          │          ├── L2 ──────┤                          │          │
   │          │          │   (revise plan → re-task)             │          │
   │          │          │                                        │          │
   │          ├── L3 ────┴────────────┤                          │          │
   │          │   (revise spec → re-plan → re-task)              │          │
   │          │                                                    │          │
   ├── L3 ────┴──────────────────────┴──────────────┤             │          │
   │   (revise spec → everything)                                  │          │
   │                                                              │          │
   │                                          ┌── L1 ─────────────┤          │
   │                                          │   (re-code task)              │
   │                                          │                              │
   │                                          ├── L2 ────────────┴──────────┤
   │                                          │   (revise plan → everything) │
   │                                          │                              │
   │                                          ├── L3 ───────────┴───────────┤
   │                                          │   (revise spec → everything) │
   │                                          │                              │
   │                                          │                    ┌── L1 ──┤
   │                                          │                    │  (advisory — no reroute)
   │                                          │                    │
   │                                          │                    ├── L2 ──┤
   │                                          │                    │  (advisory — next workstream)
   │                                          │                    │
   │                                          │                    └── L3 ──┤
   │                                          │                       (advisory — reframe spec)
```

## Layer Definitions

| Layer | What changes | Scope |
|-------|-------------|-------|
| **L1 — Code** | Implementation only. Same contract, same plan. | Single task or code block |
| **L2 — Plan** | Architecture, API, schema revised. Tasks regenerated. | Full workstream |
| **L3 — Spec** | Requirements, ACs, scope redefined. Everything re-executes. | Full workstream |

## Phase Responsibilities

| Phase | Input | Output | Entry Gate | Exit Gate |
|-------|-------|--------|------------|-----------|
| **spec** | Human intent | `spec.md` | Active workstream | ACs verifiable without reading code |
| **plan** | `spec.md` | `plan.md` | spec.md exists | Impact analysis names real files |
| **tasks** | `spec.md`, `plan.md` | `tasks.md` | plan.md exists | 5-dimension complete, DAG valid |
| **analyze** | `spec.md`, `plan.md`, `tasks.md` | Pass/fail + layer | tasks.md exists | No L1/L2/L3 gaps, or routed back |
| **implement** | `tasks.md` | Code + `handoff.md` | analyze pass | RED→GREEN→REGRESS per task, review pass |
| **qa** | `handoff.md` | `qa-report.md` | handoff exists | Reproduce gate passed, ACs verified on live system |
| **audit** | All artifacts | `changelog.md`, `learnings/` | qa PASS | Archive complete |

## Feedback Destinations by Trigger Point

| Trigger | L1 routes to | L2 routes to | L3 routes to |
|---------|-------------|-------------|-------------|
| **analyze** gap | tasks | plan | spec |
| **implement** blocker | same task redo | plan | spec |
| **qa** FAIL | implement | plan | spec |
| **audit** note | advisory | advisory (next workstream) | advisory (next workstream) |
