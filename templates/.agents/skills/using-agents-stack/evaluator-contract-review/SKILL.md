---
name: evaluator-contract-review
description: Use when `.harness/<workstream-id>/sprint_proposal.md` exists and no trustworthy approved contract is present.
purpose: Adversarially review a sprint proposal and either approve it as a contract or force a revision with specific, actionable feedback.
trigger: Use when `.harness/<workstream-id>/sprint_proposal.md` exists and no trustworthy approved contract is present.
inputs:
  - AGENTS.md
  - docs/live/tracked-work.json
  - docs/live/current-focus.md
  - docs/live/roadmap.md
  - docs/live/progress.md
  - docs/live/memory.md
  - docs/reference/*
  - .harness/<workstream-id>/sprint_proposal.md
  - .harness/<workstream-id>/status.json
  - affected code areas named by the proposal
outputs:
  - .harness/<workstream-id>/contract.md on approval
  - updated .harness/<workstream-id>/status.json
  - specific revision feedback recorded back into `.harness/<workstream-id>/sprint_proposal.md` or adjacent sprint-local notes when rejected
boundaries:
  - Do not implement the feature.
  - Do not soften requirements to make approval easier.
  - Do not approve unverifiable or overbroad work.
  - Do not change global backlog priority unless required to reflect an explicit stop condition.
next_skills:
  - generator-execution
  - generator-proposal
---

# Evaluator Contract Review

## Placement
This is a nested child under `using-agents-stack`; its path is `using-agents-stack/evaluator-contract-review/`, and the router selects it before standalone use.

## Mission
Stress-test the sprint proposal as if the implementation will fail in every ambiguous corner.

Your job is to reject weak proposals early. Approval means the scope, boundaries, and verification plan are strong enough that execution can be judged without debate.

## Worker Dispatch Contract

- Run contract review in a fresh worker context. The orchestrator dispatches a reviewer worker; it must not review by wearing this persona inline.
- Only the orchestrator may spawn workers. This reviewer must not spawn another worker.
- Tool lane: read/search/inspection only across proposal, status, and cited code areas. This reviewer should not have write tools; it returns approval or rejection artifacts for the orchestrator to persist into sprint-local files.
- Copy `.harness/<workstream-id>/contract.md` from the canonical template at `references/templates/.harness/contract.md`. Fill placeholders; delete template comment blocks. Do not construct this file from memory.
- Durable return contract: approved `contract.md` content or precise proposal-revision feedback, plus the corresponding `status.json` update payload. Include reviewer `worker_id` / `orchestrator_run_id` in the returned status metadata when the host provides them.
- Dispatch framing is non-authoritative. Before deciding, verify that the dispatched feature still matches `docs/live/tracked-work.json`, that the claimed phase still matches the strongest local/live artifact on disk, and that stronger evidence in the `AGENTS.md` precedence chain beats any dispatch summary, stale resume hint, or copied orchestrator context.
- If those checks disagree with the dispatch frame, stop before writing review artifacts, preserve the existing truthful files, and hand control back to the orchestrator for correct-lane dispatch.

## Required Reads
Read all of the following before deciding:

1. `AGENTS.md`
2. `docs/live/tracked-work.json`
3. `docs/live/current-focus.md` and `docs/live/roadmap.md`
4. `docs/live/progress.md` and `docs/live/memory.md`
5. Relevant `docs/reference/*`
6. `.harness/<workstream-id>/sprint_proposal.md`
7. `.harness/<workstream-id>/status.json`
8. The real code and tests in the areas the proposal claims it will touch

Do not review only the prose. Verify that the claimed file boundaries and acceptance steps match the actual repo.

## Expected Outputs
If the host keeps reviewer workers read-only, return exact file payloads for these artifacts and let the orchestrator persist them without altering their substance.

### Approval path: `.harness/<workstream-id>/contract.md`
Write an approved contract only when the proposal is execution-ready.
The contract must include:
- sprint id and objective
- exact allowed files or narrowly bounded allowed directories
- explicit forbidden files or forbidden subsystems
- a `## Acceptance Criteria` section whose entries use stable `AC-###` ids and the canonical shape below
```md
- `AC-001` | stateful=no | reversible=no
  - Requirement: ...
  - Evidence: ...
- `AC-002` | stateful=yes | reversible=yes
  - Requirement: ...
  - Evidence: ...
  - Before state: ...
  - Action: ...
  - After state: ...
  - Reverse check: ...
```
- concrete verification script or commands
- open assumptions, ambiguous states, and reward-hack surfaces execution may rely on
- clear non-goals and deferred work
- enough structural fidelity that `templates/.agents/skills/using-agents-stack/scripts/validate_contract.py <workstream-id> --repo-root <repo-root>` would return `allow` before approval
- a `## Task Decomposition` section whose structured JSON matches the canonical schema below (carried forward from the proposal, refined if needed during contract review):
```json
{
  "tasks": [
    {
      "id": "<kebab-case-id>",
      "symbols": [
        {"name": "<SymbolName>", "kind": "function|method|type|interface",
         "signature": "<full signature>", "file_hint": "<subdirectory>/"}
      ],
      "depends_on": ["<other-task-id>"],
      "acceptance": ["<verifiable condition>"]
    }
  ]
}
```
- verification that the task decomposition is parseable JSON, contains at least one task, has no circular dependencies, and every `depends_on` reference resolves to a declared task id
- the contract must include this decomposition so `scripts/check_contract_symbols.py` can mechanically verify symbol existence after execution
- for stateful or reversible behavior, the contract must require before/action/after evidence and reversal proof instead of static end-state prose

Also update `status.json` so the sprint resumes from `contract.md` and the next owner is the orchestrator, which can dispatch a fresh `generator-execution` worker.

### Rejection path: revision feedback
If the proposal is not execution-ready, do not write `contract.md`.
Instead record precise revision feedback in sprint-local state, preferably by replacing or appending a clearly labeled review section in `sprint_proposal.md`, and update `status.json` to show revision is required.

Feedback must be actionable, for example:
- acceptance criterion `AC-003` is not observable because no selector or command is specified
- proposal claims `src/app/**` is allowed, which is too broad for a one-sprint change
- architecture introduces a new persistence layer but the scope hides migration work
- the task decomposition contains a circular dependency (task B depends on task C, which depends on task B) or references unknown task ids
- the task decomposition has symbol signatures that do not match the target language
- the toggle requirement can be reward-hacked by rendering a hardcoded final state because the proposal never requires a before/action/after check
- the proposal assumes seeded data already exists but never names that dependency or how review will detect the wrong starting state
- the proposed contract shape would fail `validate_contract.py` because it omits stable acceptance IDs or criterion evidence fields

## Review Workflow

### 1. Verify the active sprint truth
- Confirm there is only one runnable sprint.
- Confirm the proposal matches the selected backlog item.
- Confirm the proposal reflects the current repo, not an imagined future structure.
- Confirm the proposal aligns with the durable source-goal and authorized initiative slice in `docs/live/roadmap.md` and `docs/live/current-focus.md`.
- If the roadmap files and proposal disagree about what this sprint is for, reject and send the work back for proposal repair before any contract is approved.

### 2. Attack assumptions and reward-hack surfaces
Reject if the proposal:
- relies on hidden environment, data, caller, or repo-state assumptions that are not written down
- leaves wording loose enough that contradictory states could both appear to satisfy the contract
- never asks how the implementation could fake a pass or shortcut the required transition
- skips plausible alternative directions when that choice changes the contract shape or the honest file boundary


### 2b. Force global thinking check

Before approving, the reviewer must answer the following system-level questions for the contract's task decomposition and record the answers in the contract's `## Assumptions` section:

- **Upstream failure**: For each task with upstream dependencies, what happens if upstream module X returns nil, an error, or unexpected input? The answer must name the specific fallback behavior (graceful degradation, explicit error propagation, default value with documented rationale), not "handle it" or "fail gracefully".
- **Downstream consumption**: For each task, which downstream modules consume its outputs? Name the specific task ids and the symbol names they depend on.
- **Failure blast radius**: If this module fails, which downstream modules are affected? Name the specific task ids that cannot proceed and describe the observable impact.
- **Upstream assumptions**: What assumptions is each task making about upstream behavior — types, invariants, error modes, ordering? What breaks if those assumptions change?

If the proposal or contract cannot answer these questions, it is not execution-ready. Reject and require the proposer to add a `## Assumptions` section with explicit answers before re-submission.

These answers become part of the contract's `## Assumptions` section so that `generator-execution` can reference them during implementation.

### 3. Attack the scope
Reject if any of these are true:
- more than one meaningful product increment is bundled together
- the proposal quietly narrows the user's stated initiative into a different smaller project
- the change spans unrelated subsystems without justification
- the proposal's deferred-work section hides core parts of the same initiative instead of naming later roadmap slices
- the proposal leaves follow-on sprints implicit instead of making them explicit in the roadmap
- the proposal requires follow-on work before its own acceptance can be tested
- "nice to have" items are mixed into required scope


### 3b. Attack the task decomposition
Reject if the task decomposition:
- is missing entirely from the proposal
- is not parseable JSON (malformed, truncated, or embedded in prose without a fenced block)
- contains zero tasks
- contains tasks without any declared symbols (every task must produce at least one observable symbol)
- has circular dependencies (A depends on B, B depends on A)
- references task ids in `depends_on` that do not exist in the decomposition
- has symbols without signatures, or signatures that do not match the target language (e.g., Python `def` syntax in a Go project)
- has tasks whose symbols span unrelated subsystems without justification
- cannot be verified because `file_hint` paths do not exist in the repo

A valid task decomposition is the prerequisite for mechanical symbol verification. If it fails these structural checks, the contract cannot be approved.

### 4. Attack the observability

Reject if acceptance cannot be verified from outside the author's head.

Common failures:
- vague UX language with no interaction or visual checks
- internal implementation claims substituted for user-visible outcomes
- no stable `AC-###` id per acceptance criterion
- no concrete command, page, selector, endpoint, fixture, viewport, or data shape to inspect
- missing negative cases where failure modes matter
- interactive or other stateful behavior defined only as a final static state instead of a before/action/after transition
- a criterion that could pass via hardcoded mocks, static DOM, canned output, pre-seeded data, or a screenshot without exercising the real path
- a criterion whose `stateful` / `reversible` flags contradict the evidence the reviewer would need

For browser-visible work, require acceptance criteria that name:
- the starting state the reviewer must see before acting
- the route, page, or component
- the action the reviewer performs
- the expected after-state
- the viewport or input mode when layout or accessibility matters
- the selector or visible text that proves the state changed

Consult the narrowest matching contract recipe before approval:
- `references/frontend-ui-contract-recipe.md` for browser-visible UI work
- `references/backend-api-contract-recipe.md` for API routes, auth boundaries, and backend-visible behavior
- `references/integration-contract-recipe.md` for third-party APIs, callbacks, and other cross-system boundaries
- `references/async-worker-contract-recipe.md` for jobs, queues, schedulers, and other background execution
- `references/migration-contract-recipe.md` for schema or data transitions that must be proved across time

If those details are missing, reject or send the proposal back for revision; do not infer them yourself.


### 5. Attack the boundary honesty
Reject if the proposal:
- omits allowed-file boundaries
- omits forbidden-file boundaries
- hides architecture, dependency, schema, routing, or new roadmap-authorization work inside general wording
- relies on touching generated, vendor, or unrelated files without justification
- discovers late scope that belongs to a different roadmap slice but still tries to keep the current sprint runnable instead of pausing for re-authorization

### 6. Attack resumability and retry honesty
Reject if a future agent would be unable to continue from sprint-local files alone.
The contract or revision feedback must make the next action obvious without chat history.

If the proposal discusses retries, ensure it names a clean restore boundary such as a disposable worktree, VCS snapshot, or equivalent restore reference. Do not require unconditional destructive reset as the default recovery path.

### 7. Write the outcome decisively
- If approved, write `contract.md` as the canonical sprint boundary and update `status.json` to `phase: "contracted"` with `resume_from: "contract.md"`.
- If rejected, leave no ambiguous maybe-state. Record the exact revision required and update `status.json` to a revision-needed phase that routes back to proposal work.

## File Write Expectations
- Approval writes `contract.md` and updates `status.json`.
- Rejection updates existing sprint-local planning state; it does not create a fake approval artifact.
- Do not write `handoff.md`, `review.md`, or archive artifacts in this phase.
- Do not edit implementation files.

## Mandatory Rejection Conditions
You must reject the proposal when any of the following is true:
- acceptance criteria are unverifiable
- acceptance criteria can be reward-hacked by hardcoded static outcomes rather than real state transitions
- hidden assumptions, contradictory states, or reward-hack surfaces remain implicit
- file boundaries are missing, too broad, or dishonest
- the sprint hides architecture changes, migrations, or dependency churn
- scope exceeds one bounded sprint for the current contract
- the task decomposition is missing, unparseable, has circular dependencies, or contains symbols without signatures
- the proposal hides multi-sprint initiative scope or a required roadmap re-authorization boundary
- required repo context is missing and the proposal papers over the gap
- the proposal conflicts with `AGENTS.md`, `docs/live/current-focus.md`, `docs/live/roadmap.md`, global state, or reference docs

## Quality Bar
A good contract review:
- is adversarial, not collaborative wishful thinking
- attacks assumptions, ambiguity, and reward-hack paths before code exists
- makes approval meaningful and rejection specific
- protects the repo from scope creep before code exists
- preserves a clean state transition: proposed -> contracted or proposed -> revision required
- leaves the next responsible role obvious from files alone

## Done Definition
This skill is done when execution can begin against a real approved contract, or the proposal has been sent back with precise revision demands and no false appearance of approval.
