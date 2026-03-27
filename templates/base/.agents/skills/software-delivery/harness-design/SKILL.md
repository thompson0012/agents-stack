---
name: harness-design
description: Use when the real problem is cross-session delivery control: deciding whether work should stay in one session, resume through `context-compaction`, or run through a planner/generator/evaluator loop with explicit handoffs, artifacts, and return paths.
---

# Harness Design

Use this skill to define the control model for work that will span resets, handoffs, or independent verification.

This skill does not implement the product work itself. It defines how the work will be controlled so the next skills can execute honestly.

## Boundary

Use this skill when:
- the team must choose between one uninterrupted session, a resumed continuation, or a planner/generator/evaluator loop
- work will cross session boundaries and needs explicit baton passing instead of implicit memory
- independent evaluation must be separated from generation so pass/fail decisions stay credible
- the main uncertainty is orchestration, handoff truthfulness, or retry ownership rather than product scope or implementation details

Do not use this skill when:
- the router can already choose the next ordinary stage without more control design
- the main need is a PRD, plan review, implementation, or browser QA rather than the control model around that work
- the request only says "be more organized" or "track status better" without a concrete cross-session or role-separation problem

## Core Contract

- Choose exactly one execution mode: `single-session`, `compacted-continuation`, or `planner-generator-evaluator`.
- Make the choice from observable conditions such as session-boundary risk, context volume, independent-verification needs, and defect-routing needs.
- Name `context-compaction` as the canonical mechanism for `compacted-continuation`. Do not describe compaction as an ad hoc summary.
- Keep planner, generator, and evaluator as separate owners. Planner and evaluator must not collapse into the same role.
- Define the handoff artifacts, pass/fail gates, and return paths before any implementation begins.
- When live docs are part of the workflow, require honest updates before each baton pass so the next role reads current truth rather than stale intent.
- Preserve goal lineage: the source goal, plan goal, and current phase goal must remain linked until the user explicitly retires or replaces the work.
- Rehydrate from stored truth before phase 1 and after every compaction; do not continue from chat memory alone.
- Stay portable. Do not assume a vendor-specific runtime, daemon, background supervisor, or always-on agent framework.

## Mode Selection

Choose the mode by the dominant control risk.

### `single-session`
Use this mode when all of the following are true:
- one agent can complete the next meaningful slice without crossing a session reset
- the work fits in a single bounded attempt without context pressure
- no independent evaluator is needed before the next decision
- failures can be handled directly by the same agent without ambiguous ownership

Choose `single-session` because the work is small and bounded, not because no one has thought about alternatives.

### `compacted-continuation`
Use this mode when:
- the same role should continue the work, but the session will likely reset or exceed comfortable context size
- continuity depends on preserving current state, decisions, touched files, and next action across sessions
- the main problem is state transfer, not role separation or independent acceptance

For this mode, `context-compaction` is the canonical mechanism. Use it to produce the continuation snapshot and keep the same role responsible after the reset.

Do not choose `compacted-continuation` when the real need is skeptical verification, explicit retry routing between roles, or multi-role control.

### `planner-generator-evaluator`
Use this mode when any of these are true:
- the work is large enough that planning, building, and judging should not happen inside one role
- browser-facing, risky, or high-cost changes require independent pass/fail evaluation
- repeated retries are plausible and must route to the correct owner instead of looping vaguely
- the team needs explicit contracts for what the planner decides, what the generator may change, and what the evaluator may reject

Choose this mode only when role separation buys real control. Do not use it as ceremony for routine work.

## Role Ownership

### Planner
Owns:
- choosing the execution mode
- defining scope, contracts, acceptance gates, and handoff artifacts
- deciding what the generator is allowed to change
- deciding whether a reported defect is actually a scope, contract, or orchestration problem

Does not own:
- implementing the code or content changes
- grading its own plan as the final evaluator

### Generator
Owns:
- executing the plan inside the permitted boundary
- updating the agreed handoff artifacts with what actually changed, what was verified, and what remains true or blocked
- returning implementation defects with concrete evidence when the plan was followed but the output failed

Does not own:
- expanding scope silently
- redefining acceptance criteria during implementation
- self-certifying independent acceptance when an evaluator lane exists

### Evaluator
Owns:
- checking the delivered work against the planner's contract and the observable acceptance gate
- reporting pass, fail, and defect evidence clearly enough that the next owner knows what must change
- preserving independence from generation so the evaluation is not a self-justification loop

Does not own:
- writing the implementation fix
- rewriting the plan unless the failure proves the plan itself is wrong

## Handoff Artifacts

For any non-trivial control model, define these artifacts explicitly:
- `docs/live/current-focus.md` — current objective and active boundary
- `docs/live/roadmap.md` — source goal, plan goal, phase ledger, goal changes, and resume rules for phased work
- `docs/live/runtime.md` — current execution mode, baton owner, and transition rules
- `docs/live/progress.md` — progress record with touched files and verification evidence
- `docs/live/qa.md` — evaluation record when an evaluator exists
- next-owner instruction stating who acts next and why (written into `docs/live/current-focus.md`)

When live docs are in use, update them before handoff with the current truth. At minimum, the receiving role must be able to recover:
- what mode is active
- what was changed
- what was verified
- what failed
- who owns the next action
- what the original source goal is
- what phase goal is active now
- whether the user changed direction and retired the old goal

## Return Paths

Every failure must route to one owner.

- **Implementation defect** -> return to the generator. The plan was still valid, but the produced work did not satisfy it.
- **Scope, contract, or orchestration defect** -> return to the planner. The control model, boundary, or acceptance logic was wrong or incomplete.
- **Environment or setup blocker** -> mark the work as `blocked`. Do not pretend planning or implementation can proceed until the external blocker is removed.
- **Goal-lineage drift** -> return to the planner. If the current phase can no longer be reconciled with the source goal or roadmap, the control artifact is stale and must be rewritten before more implementation continues.

If a failure could fit more than one bucket, choose the earliest broken contract. Do not send generator work back to the planner just because the failure was discovered late.

## Output Shape

Return a compact control artifact with these sections:
1. **Chosen mode** — exactly one of `single-session`, `compacted-continuation`, `planner-generator-evaluator`
2. **Why this mode** — the observable conditions that made the other modes wrong
3. **Role ownership** — planner, generator, evaluator boundaries
4. **Handoff artifacts** — what must exist before baton passing
5. **Return paths** — implementation defect, scope/contract/orchestration defect, environment blocker
6. **Next route** — the next skill or work lane that should execute under this control model

## Failure Modes to Avoid

- Treating ordinary stage selection as harness design.
- Calling a vague summary "compaction" instead of using `context-compaction`.
- Letting planner and evaluator collapse into one role and then calling the result independent.
- Using planner/generator/evaluator loops as a prestige pattern for routine work.
- Writing handoffs that say what was intended instead of what is currently true.
- Hiding environment blockers inside implementation retries.
- Describing a runtime-specific agent service, daemon, or orchestrator as if it were required by this skill.
