# canonical file-system layout

This reference describes the canonical agents-stack starter topology. The router and child skills should treat these paths as the harness model for a repository using this family. The orchestrator chooses a phase, dispatches a fresh worker for that phase, and relies on these files as the durable return path.

## Top-level layout

```text
AGENTS.md
.agents/skills/using-agents-stack/
.harness/<feature-id>/
docs/live/
docs/archive/<feature-id>_<timestamp>/
docs/reference/
docs/scripts/
```

## `AGENTS.md`

Purpose:

- repository operating contract
- lifecycle, role boundaries, and review standard
- state precedence and handoff protocol
- rules for single active sprint execution

Every worker should read this file before acting.

## `.agents/skills/using-agents-stack/`

Purpose:

- root router skill plus child skill packages for each harness role
- references that explain routing, state transitions, file semantics, and worker delegation rules
- eval guidance for verifying the package itself

Expected router children:

- `project-initializer`
- `generator-proposal`
- `evaluator-contract-review`
- `generator-execution`
- `adversarial-live-review`
- `state-update`

The router stays thin. It chooses one child and dispatches that child as a fresh worker instead of doing the phase inline.

## `docs/live/`

These files are durable project-wide state. They survive across many sprints.

### `docs/live/features.json`

Purpose:

- canonical backlog and feature registry
- priority, dependencies, and active/pending/completed state
- the first place the router checks for initialization and active sprint selection

Rules:

- empty or missing means the repo is not initialized yet
- more than one active feature is invalid
- a feature marked active should have a matching `.harness/<feature-id>/` folder unless the proposal has not been created yet

### `docs/live/progress.md`

Purpose:

- append-only-ish project ledger of visible outcomes
- links sprint IDs to archive artifacts, merge points, and next recommended action

Use it to understand the latest completed or failed sprint without reading chat logs.

### `docs/live/memory.md`

Purpose:

- durable lessons, known pitfalls, environment notes, and recovery context
- the place to preserve facts that matter beyond one sprint

This is not scratch space. It should store information the next agent actually needs.

## `.harness/<feature-id>/`

This folder contains the single active sprint. It is the local working state for one feature. In the starter pack, `.harness/FEAT-001/` is the in-flight example.

Fresh workers come and go, but the sprint folder stays stable. Retries, review cycles, and resume attempts write back into the same sprint-local evidence set.

### Required files and meanings

#### `sprint_proposal.md`

- proposed objective, scope, allowed files, risks, and test intent
- created by a `generator-proposal` worker
- consumed by an `evaluator-contract-review` worker

#### `contract.md`

- approved sprint contract
- source of truth for boundaries and acceptance criteria during execution
- consumed by `generator-execution` and `adversarial-live-review` workers

#### `handoff.md`

- execution checkpoint proving what changed, how to verify it, what remains risky, and how to resume
- created by a `generator-execution` worker
- existence means execution claims review readiness unless contradicted by stronger evidence

#### `review.md`

- adversarial PASS/FAIL/BLOCKED decision with evidence and corrective or recovery directives
- created by an `adversarial-live-review` worker
- existence means routing should go to `state-update`

#### `status.json`

- machine-readable sprint phase, owner, heartbeat, blockers, and `resume_from`
- useful for timeout/recovery and for exposing explicit blocked or `review_failed` states
- lower routing precedence than later-phase artifacts
- good place to record worker traceability when the runtime exposes it

Recommended fields:

- `sprint_id`
- `phase`
- `owner_role`
- `last_updated_at`
- `resume_from`
- `active_pids`
- `worker_id` for the currently assigned worker, such as `exec-002`
- `worker_kind` for the host runtime primitive, such as `sub-agent`, `Task agent`, or `parallel agent`
- `expected_outputs` for the artifacts the worker must return
- blocker metadata when blocked

The trace fields are optional, but they help preserve who did what across retries without creating a second source of truth outside the sprint folder.

## `docs/archive/<feature-id>_<timestamp>/`

Purpose:

- immutable-ish sprint archive after review PASS and state update
- preserves proposal, contract, handoff, review, and status snapshot for audit and recovery, plus `runtime.md` and `qa.md` when those artifacts were generated

In the starter pack, `docs/archive/FEAT-000_timestamp/` is the completed example. It should read as a finished sprint, not an active one.

Archive rules:

- archive only after review PASS and state update
- never reuse the active `.harness/<feature-id>/` folder as the archive itself
- archive naming should include the feature ID and a timestamp or equivalent unique suffix
- preserve the final `status.json` snapshot so worker IDs, phase, and return paths remain visible in historical evidence when those fields were recorded

## `docs/reference/`

Purpose:

- stable architecture, design, and domain references shared across sprints
- context that proposals, contracts, execution, and review must respect

Starter-pack examples:

- `architecture.md`
- `design.md`

These files are reference material, not sprint-local notes.

## `docs/scripts/`

Purpose:

- automation helpers for the harness, such as timeout recovery or watchdog scripts
- operational support, not the source of truth for project state

Starter-pack example:

- `orchestrator.py`

Scripts may update state, but the durable truth still lives in the state files they read and write. If a script dispatches workers, it should record the outcome back into sprint-local or live-state files instead of hiding evidence in process memory.

## State ownership summary

| Path | Scope | Typical writer | Typical reader |
| --- | --- | --- | --- |
| `AGENTS.md` | repository-wide | human maintainers | every worker |
| `docs/live/features.json` | global | initializer, state-update workers | router, proposal, state-update workers |
| `docs/live/progress.md` | global | state-update worker | router, proposal workers, humans |
| `docs/live/memory.md` | global | initializer, execution, state-update workers | router, proposal, execution workers |
| `.harness/<feature-id>/sprint_proposal.md` | sprint-local | generator-proposal worker | contract-review worker |
| `.harness/<feature-id>/contract.md` | sprint-local | evaluator-contract-review worker | execution and review workers |
| `.harness/<feature-id>/handoff.md` | sprint-local | generator-execution worker | review and resume logic |
| `.harness/<feature-id>/review.md` | sprint-local | adversarial-live-review worker | state-update and resume logic |
| `.harness/<feature-id>/status.json` | sprint-local | current phase worker | router, resume logic, audits |
| `docs/archive/<feature-id>_<timestamp>/` | historical | state-update worker | humans, audits, future planning |

## Routing implications

- Missing or empty live state means initialize.
- No active sprint but pending work means propose.
- Proposal without contract means contract review.
- Contract without handoff means execution.
- Handoff without review means live review.
- Review present means state update.
- Contradictions are resolved by artifact precedence, then reconciled through state update.
- Child work always returns through durable files in this layout; the orchestrator should not rely on inline persona state as the only record.
