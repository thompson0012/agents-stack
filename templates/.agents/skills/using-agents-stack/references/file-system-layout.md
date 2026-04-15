# canonical file-system layout

This reference describes the canonical agents-stack starter topology. The router and child skills should treat these paths as the harness model for a repository using this family. The orchestrator chooses a phase, dispatches a fresh worker for that phase, and relies on these files as the durable return path.

## Top-level layout

```text
AGENTS.md
.agents/skills/using-agents-stack/
.harness/<workstream-id>/
docs/live/
docs/archive/<workstream-id>_<timestamp>/
docs/records/
docs/reference/
docs/scripts/
```

## `AGENTS.md`

Purpose:

- repository operating contract
- lifecycle, role boundaries, and review standard
- state precedence and handoff protocol
- rules for one runnable active sprint plus explicitly parked non-terminal sprints

Every worker should read this file before acting.

## `.agents/skills/using-agents-stack/`

Purpose:

- root router skill plus child skill packages for each harness role
- references that explain routing, state transitions, file semantics, and worker delegation rules
- eval guidance for verifying the package itself

Expected router children:

- `project-initializer`
- `generator-brainstorm`
- `generator-proposal`
- `evaluator-contract-review`
- `generator-execution`
- `adversarial-live-review`
- `state-update`
- `compound-capture`

The router stays thin. It chooses one child and dispatches that child as a fresh worker instead of doing the phase inline. Brainstorm and Compound are explicit non-runnable phases in the same family.

## `docs/live/`

These files are durable project-wide state. They survive across many sprints.

### `docs/live/tracked-work.json`

Purpose:

- canonical backlog and feature registry
- priority, dependencies, runnable-active vs parked state, archived history, and per-feature traceability pointers
- the first place the router checks for initialization, dependency-aware scheduling, active sprint selection, and durable links to ideas, records, references, and evidence

Rules:

- empty or missing means the repo is not initialized yet
- `idea_backlog_path` should point at `docs/live/ideas.md` for durable pre-proposal exploration
- `compound_pending_feature_ids` is a non-runnable queue that drains before runnable sprint resume or new backlog selection
- more than one runnable active feature is invalid
- parked `awaiting_human` and `escalated_to_human` features may remain listed, but they must not also be marked as the runnable active sprint
- a feature marked runnable-active should have a matching `.harness/<workstream-id>/` folder unless the proposal has not been created yet
- a selected planning item may also keep `.harness/<workstream-id>/status.json` as its canonical local checkpoint while `runnable_active_sprint_id` remains null
- `tracked-work.json` remains the only tracked-work registry; fields such as `idea_ref`, `evidence_path`, `record_paths`, and `reference_paths` belong here rather than in a second registry
- each feature should have exactly one canonical `evidence_path` at a time: `.harness/<workstream-id>/` while selected locally, active, or parked, then `docs/archive/<workstream-id>_<timestamp>/` after PASS archive cutover
- when no runnable active sprint exists, routing chooses the highest-priority dependency-ready `needs_brainstorm` item before ordinary `pending` proposal work
- `docs/live/roadmap.md` may explain initiative continuation, but `tracked-work.json` still selects runnable truth and backlog order

### `docs/live/ideas.md`

Purpose:

- durable pre-proposal exploration backlog
- refinement notes for tracked `needs_brainstorm` work
- rejected directions and open questions that should survive chat-context loss

Rules:

- it is not the runnable sprint selector
- it may justify creating or refining one backlog item in `docs/live/tracked-work.json`, but it must not claim `runnable_active_sprint_id`
- it should stay at the idea, problem, and tradeoff level rather than becoming a hidden sprint proposal

### `docs/live/current-focus.md`

Purpose:

- live current objective, goal lineage, and next-owner resume anchor
- points a cold-start agent at the active sprint, parked blocker, or next backlog lane plus the strongest artifact to read next

Rules:

- it complements `docs/live/tracked-work.json`, `docs/live/roadmap.md`, `docs/live/progress.md`, and `docs/live/memory.md`; it does not replace any of them
- when an active or parked sprint exists, it must point back to `.harness/<workstream-id>/contract.md` for slice truth instead of becoming a second contract
- keep it concise and refresh it when decisive state changes so resume routing does not depend on chat memory


### `docs/live/roadmap.md`

Purpose:

- durable initiative ledger for source goals, remaining slices, and re-authorization boundaries
- explains what work remains beyond the current runnable sprint and when automation may continue versus when a human must explicitly re-scope or re-authorize

Rules:

- it complements `docs/live/tracked-work.json` and `docs/live/current-focus.md`; it does not replace runnable selection or sprint-local execution truth
- it must not claim `runnable_active_sprint_id` or overrule `.harness/<workstream-id>/contract.md` for an active sprint
- refresh it whenever planning or state reconciliation changes which slice comes next, what still remains, or where the next human authorization boundary lives


### `docs/live/progress.md`

Purpose:

- append-only-ish project ledger of visible outcomes
- links sprint IDs to archive artifacts, retries, human gates, compound publication, record lifecycle events, and next recommended action

Use it to understand the latest archived, failed, parked, or freshly reconciled sprint without reading chat logs. It records record creation, promotion, supersession, expiry, and archive cutover events without becoming a second registry.

### `docs/live/memory.md`

Purpose:

- durable lessons, known pitfalls, environment notes, and recovery context
- the place to preserve facts that matter beyond one sprint after explicit compounding

This is not scratch space. It should store information the next agent actually needs, and it should usually be written by `compound-capture` rather than by routine state reconciliation. Memory entries must keep artifact-linked provenance to decisive sprint evidence; a direct inline artifact-path citation is sufficient, so a separate records page is not required for every note.

## `.harness/<workstream-id>/`

This folder contains selected-workstream durable state. One folder may be the runnable active sprint. A selected planning workstream may also live here with `status.json.phase = needs_brainstorm` or `pending`, and additional non-terminal folders are otherwise allowed only when they are explicitly parked in `awaiting_human` or `escalated_to_human`.

Fresh workers come and go, but the workstream folder stays stable. Planning passes, retries, review cycles, human pauses, and resume attempts write back into the same local evidence set.

### Canonical sprint-local artifact layout

```text
.harness/<workstream-id>/
├── sprint_proposal.md
├── contract.md
├── runtime.md
├── handoff.md
├── qa.md
├── review.md
└── status.json
```

### Canonical sprint-local files and meanings

#### `sprint_proposal.md`

- proposed objective, scope, allowed files, risks, and test intent
- created by a `generator-proposal` worker
- consumed by an `evaluator-contract-review` worker

#### `contract.md`

- approved sprint contract
- source of truth for boundaries and acceptance criteria during execution
- should describe observable checks as state transitions where possible, not just final static assertions
- consumed by `generator-execution` and `adversarial-live-review` workers

#### `runtime.md`

- execution-time notes about commands, environment, running processes, and build/startup triage
- the canonical place to capture why execution entered `build_failed`, `paused_by_timeout`, or a resumable runtime checkpoint
- created and updated by `generator-execution`

#### `handoff.md`

- execution checkpoint proving what changed, how to verify it, what remains risky, and how to resume
- the human-readable pause boundary when a sprint enters `awaiting_human`
- should name the exact files or decisions a human must touch before resume
- created by a `generator-execution` worker
- existence means execution claims review readiness unless contradicted by stronger evidence

#### `qa.md`

- detailed review evidence log with exact checks, observations, and reproduction notes behind `review.md`
- created by an `adversarial-live-review` worker
- consumed by `state-update`, humans, and retry/resume audits when review evidence must be re-read
- optional until review runs; once present, archive it with the rest of the sprint evidence

#### `review.md`

- adversarial PASS/FAIL/BLOCKED decision with evidence and corrective or recovery directives
- created by an `adversarial-live-review` worker
- existence means routing should go to `state-update`

#### `status.json`

- machine-readable sprint phase, owner, heartbeat, blockers, retry budget, restore boundary, and `resume_from`
- useful for timeout/recovery and for exposing explicit `build_failed`, `review_failed`, `awaiting_human`, or `escalated_to_human` states
- lower routing precedence than later-phase artifacts
- good place to record worker traceability when the runtime exposes it

Recommended fields:

- `sprint_id`
- `phase`
- `owner_role`
- `last_updated_at`
- `resume_from`
- `attempt_count`
- `max_attempts`
- `clean_restore_ref`
- `active_pids`
- `worker_id` for the currently assigned worker, such as `exec-002`
- `worker_kind` for the host runtime primitive, such as `sub-agent`, `Task agent`, or `parallel agent`
- `expected_outputs` for the artifacts the worker must return
- `blocked_on` when a blocker is active
- `human_action_required` when the sprint is paused for edits or approval
- `pause_reason` or `escalation_reason` when the sprint is parked
- `parked_at` when the sprint left the runnable lane

The trace and pause fields are optional only when they do not apply. When a sprint is retried or parked, these fields are part of the durable contract, not convenience notes.

## `docs/archive/<workstream-id>_<timestamp>/`

Purpose:

- immutable-ish sprint archive after review PASS and state update
- preserves proposal, contract, runtime, handoff, review, and status snapshot for audit and recovery, plus `qa.md` when that artifact was generated

In the starter pack, `docs/archive/WORKSTREAM-000_timestamp/` is the archived example. It should read as a finished sprint, not an active one.

Archive rules:

- archive only after review PASS and state update
- PASS archive cutover should prefer move or verified rename; if copying is required, update the feature's canonical `evidence_path` to the archive and explicitly de-canonicalize the source `.harness/<workstream-id>/` workspace after verification
- never reuse the active `.harness/<workstream-id>/` folder as the archive itself
- archive naming should include the workstream ID and a timestamp or equivalent unique suffix
- preserve the final `status.json` snapshot so worker IDs, attempt counters, restore boundaries, and parked history remain visible in historical evidence when those fields were recorded
- archive never overrides active live or local sprint truth

## `docs/records/`

Purpose:

- durable, traceable, scoped records from discussion or sprint work
- a home for artifacts that should outlive chat but are not the active contract, immutable archive evidence, or universally current reference truth

Rules:

- records are optional; do not imply that every sprint must create one
- record pages must carry page-local provenance and validity metadata such as `scope`, `status`, `superseded_by`, and the sprint or archive contributions they summarize
- records may be superseded, expired, or promoted later; keep those lifecycle facts on the page and log them in `docs/live/progress.md`
- feature-linked records should be referenced from `docs/live/tracked-work.json` via `record_paths`, not through a second registry

## `docs/reference/`

Purpose:

- stable architecture, design, and domain references shared across sprints
- current truth that proposals, contracts, execution, and review must respect

Starter-pack examples:

- `architecture.md`
- `design.md`

These files are current reference material, not sprint-local notes. Promote content here only when it is the stable present truth; otherwise keep it in `docs/records/` with explicit provenance.

## `docs/scripts/`

Purpose:

- automation helpers for the harness, such as timeout recovery or watchdog scripts
- operational support, not the source of truth for project state

Starter-pack example:

- `orchestrator.py`

Scripts may inspect or update state, but the durable truth still lives in the state files they read and write. If a script dispatches workers, it should record the outcome back into sprint-local or live-state files instead of hiding evidence in process memory.

## State ownership summary

| Path | Scope | Typical writer | Typical reader |
| --- | --- | --- | --- |
| `AGENTS.md` | repository-wide | human maintainers | every worker |
| `docs/live/tracked-work.json` | global | initializer, brainstorm, state-update, and compound-capture workers | router, brainstorm, proposal, state-update, and compound-capture workers |
| `docs/live/ideas.md` | global | generator-brainstorm worker | router, brainstorm, and proposal workers |
| `docs/live/current-focus.md` | global | initializer, proposal, and state-update workers | router, humans, and any worker resuming from durable state |
| `docs/live/roadmap.md` | global | initializer, proposal, and state-update workers | router, proposal, state-update, and human planners |
| `docs/live/progress.md` | global | state-update worker | router, proposal workers, humans |
| `docs/live/memory.md` | global | initializer and compound-capture workers | router, proposal, execution, and review workers |
| `docs/records/*` | scoped durable | generator-brainstorm, generator-proposal, state-update, and compound-capture workers, plus human maintainer promotion/supersession edits | router, proposal, state-update, compound-capture, humans |
| `.harness/<workstream-id>/sprint_proposal.md` | sprint-local | generator-proposal worker | contract-review worker |
| `.harness/<workstream-id>/contract.md` | sprint-local | evaluator-contract-review worker | execution and review workers |
| `.harness/<workstream-id>/runtime.md` | sprint-local | generator-execution worker | execution, review, and resume logic |
| `.harness/<workstream-id>/handoff.md` | sprint-local | generator-execution worker | review, humans, and resume logic |
| `.harness/<workstream-id>/qa.md` | sprint-local | adversarial-live-review worker | state-update, humans, and resume logic |
| `.harness/<workstream-id>/review.md` | sprint-local | adversarial-live-review worker | state-update and resume logic |
| `.harness/<workstream-id>/status.json` | sprint-local | current phase worker | router, resume logic, audits |
| `docs/archive/<workstream-id>_<timestamp>/` | historical | state-update worker | humans, audits, future planning |

## Routing implications

- `docs/live/tracked-work.json` is the runnable/backlog selector, live traceability index, and home of each feature's canonical `evidence_path`; `docs/live/current-focus.md` is the live resume anchor, and `docs/live/roadmap.md` is the initiative ledger for what remains and where re-authorization is required.
- `docs/records/*` may inform planning and state reconciliation, but records stay linked through `tracked-work.json` and never replace it as the tracked-work registry.
- Missing or empty live state means initialize.
- Non-empty `compound_pending_feature_ids` means compound before any runnable sprint resume or new backlog selection.
- No runnable active sprint but dependency-ready `needs_brainstorm` work means brainstorm.
- No runnable active sprint, no compound queue, and dependency-ready `pending` work means propose.
- Proposal without contract means contract review.
- Contract without handoff means execution.
- `build_failed` and reconciled `review_failed` still belong to execution when retry budget and restore metadata allow a safe retry.
- Handoff without review means live review.
- Review present or contradictory state means state update.
- Parked `awaiting_human` and `escalated_to_human` sprints remain visible in `.harness/`, but they do not auto-dispatch execution.
- Child work always returns through durable files in this layout; the orchestrator should not rely on inline persona state as the only record.
