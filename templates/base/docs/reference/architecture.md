# Architecture Reference

Read when system shape, boundaries, or invariants matter. Keep this focused on stable structure.

## System Boundaries

- Inside scope: the template harness under `templates/base/`, including live-doc templates that downstream projects copy into their own `docs/live/` for active objective, runtime control state, continuity, and QA evidence.
- Outside scope: product-specific implementation details, vendor-specific runtimes, and mandatory process for trivial one-shot tasks.
- Boundary note: `templates/base/docs/live/` are template skeletons; actual live docs live in consuming projects. `docs/live/runtime.md` and `docs/live/qa.md` extend the live-doc surface when explicit delivery control or independent evaluation is needed; they are not required for every trivial task.

## Invariants

- Invariant: when harness control is in use, exactly one mode is active: `single-session`, `compacted-continuation`, or `planner-generator-evaluator`.
- Why it must hold: baton ownership, reset handling, and return paths become ambiguous if modes mix.
- Failure signal: `docs/live/runtime.md` leaves the active mode or baton owner unclear.

- Invariant: `context-compaction` is the reset mechanism for `compacted-continuation`; a loose summary is not a substitute.
- Why it must hold: continuation must preserve honest state for the same role across session boundaries.
- Failure signal: work resets under `compacted-continuation` without a real compaction artifact.

- Invariant: `harness-design` owns the execution-mode contract and live-doc integrity rules, including retry budgets, baton ownership, and `doc_state` handoff semantics.
- Why it must hold: control state becomes ambiguous if mode, retries, or live-doc write state are implied instead of declared.
- Failure signal: live docs or runtime mode are updated without a declared state transition or a clear owner.

- Invariant: independent acceptance records evidence and exactly one verdict in `docs/live/qa.md`: `pass`, `fail`, or `blocked`.
- Why it must hold: evaluation only works if another role can audit what was checked and why the verdict stands.
- Failure signal: QA conclusions live only in chat, omit evidence, or avoid a verdict.

## Major Components

- Component: `docs/live/current-focus.md`
- Responsibility: in consuming projects, states the active objective, scope, constraints, success criteria, and next-owner instruction.
- Key dependency: planner or current baton owner keeping the boundary current.

- Component: `docs/live/runtime.md`
- Responsibility: records the active mode, current baton owner, entry criteria, reset-vs-compaction rule, artifact pointers, and stop/escalation conditions.
- Key dependency: harness-control decisions and honest updates before each baton pass.

- Component: `docs/live/qa.md`
- Responsibility: stores evaluator evidence, verdicts, and separate out-of-scope findings when evaluation exists.
- Key dependency: an independent evaluator or acceptance role writing the record clearly.

- Component: `docs/live/todo.md`
- Responsibility: sequences the queued work so the active baton owner and next owner can see what remains and what is already done.
- Key dependency: the current role keeping task ordering current when priorities or execution state change.

- Component: `docs/live/progress.md`
- Responsibility: records what changed, what was verified, blockers, and the next recommended action.
- Key dependency: the working role updating continuity after meaningful work.

- Component: `docs/live/qa.md`
- Responsibility: stores evaluator evidence, defect severity, final verdict, and retry contract when an independent acceptance lane exists.
- Key dependency: an independent evaluator or explicit acceptance pass writing the record as it verifies.

- Component: `.agents/skills/software-delivery/`
- Responsibility: routes non-trivial software work between feature discovery, multi-phase control, harness control, plan reviews, and independent frontend evaluation.
- Key dependency: the request being classified by the dominant delivery need rather than by convenience.

- Component: `.agents/skills/software-delivery/multi-phase-control/`
- Responsibility: preserves roadmap intent across phases with explicit phase gates, drift tracking, compaction checkpoints, and live-doc persistence.
- Key dependency: the control model and baton ownership rules staying aligned with `harness-design` and `context-compaction`.
