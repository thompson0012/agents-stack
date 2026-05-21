# agents-stack v3 state machine

Goal-QA-Driven phase model. Orchestrator reads these rules, decides next phase, dispatches worker.

## Core Invariants

1. Files are state. Chat memory is not durable.
2. Exactly one workstream active at a time. Others must be parked.
3. Implementer ≠ Verifier (Generator ≠ Auditor). Implement and QA must be separate workers.
4. Cold start must work. A new agent recovers from files alone.
5. Iteration ≠ Retry. Retry fixes execution within same contract. Iteration changes spec/plan.

## Artifact Precedence

When files disagree, higher-precedence artifact wins:

1. qa-report.md
2. handoff.md
3. tasks.md
4. plan.md
5. spec.md
6. status.json
7. .agents-stack/tracked-work.json

## Phase Table

| Phase | Evidence | Next Step |
|-------|----------|-----------|
| uninitialized | Missing or empty tracked-work.json | Create first workstream |
| spec | spec.md exists | Route to plan |
| plan | plan.md exists | Route to tasks |
| tasks | tasks.md exists | Route to implement |
| implement | handoff.md exists | Route to qa |
| qa | qa-report.md exists | Evaluate verdict |
| release | changelog.md exists + archived | Complete |
| awaiting_human | status.json blocked_reason set | Human decision |
| escalated_to_human | max depth/attempt exceeded | Human decision |
| archived | Evidence in .agents-stack/archive/ | Next workstream |

## Transition Rules

### Forward Pipeline

- No spec.md → route spec
  - spec worker reads CONSTITUTION.md, tracked-work.json, forms spec
- spec.md exists, no plan.md → route plan
  - plan worker reads spec, designs architecture, writes plan.md
- plan.md exists, no tasks.md → route tasks
  - tasks worker reads spec+plan, breaks into tasks with 5D verification, writes tasks.md
- tasks.md exists, no handoff.md → route implement
  - implement worker reads tasks, implements each with TDD, writes handoff.md
  - if build/startup fails: build_failed, orchestrator may retry
- handoff.md exists, no qa-report.md → route qa
  - qa worker independently reproduces and verifies against SPEC
  - verdict: PASS, FAIL, or BLOCKED
  - on FAIL: trace to layer (L1 code, L2 architecture, L3 spec)

### Post-QA

- PASS → route release
- FAIL + Layer 1 (code) + attempt < max_attempts → route implement (retry)
- FAIL + Layer 2 (architecture) → route plan (re-plan)
- FAIL + Layer 3 (spec) → route spec (re-spec)
- FAIL + attempt >= max_attempts → escalated_to_human
- BLOCKED → awaiting_human

### Post-Release

- changelog.md exists → archive workstream
- Update tracked-work.json
- Ready for next workstream

## Three-Layer Rework

| Layer | Scope | Affected Phase | Cost |
|-------|-------|---------------|------|
| L1: Code | Implementation error, missed edge case | implement | Low |
| L2: Architecture | API/DB design insufficient | plan | Medium |
| L3: Spec | Requirement/AC missing or wrong | spec | High |

## Budget Exhaustion

- depth >= max_depth (5) → escalated_to_human
- attempt >= max_attempts (3) → escalated_to_human
