---
name: evaluator-contract-review
purpose: Adversarially review a sprint proposal and either approve it as a contract or force a revision with specific, actionable feedback.
trigger: Use when `.harness/<feature-id>/sprint_proposal.md` exists and no trustworthy approved contract is present.
inputs:
  - AGENTS.md
  - docs/live/tracked-work.json
  - docs/live/current-focus.md
  - docs/live/roadmap.md
  - docs/live/progress.md
  - docs/live/memory.md
  - docs/reference/*
  - .harness/<feature-id>/sprint_proposal.md
  - .harness/<feature-id>/status.json
  - affected code areas named by the proposal
outputs:
  - .harness/<feature-id>/contract.md on approval
  - updated .harness/<feature-id>/status.json
  - specific revision feedback recorded back into `.harness/<feature-id>/sprint_proposal.md` or adjacent sprint-local notes when rejected
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

## Mission
Stress-test the sprint proposal as if the implementation will fail in every ambiguous corner.

Your job is to reject weak proposals early. Approval means the scope, boundaries, and verification plan are strong enough that execution can be judged without debate.

## Worker Dispatch Contract

- Run contract review in a fresh worker context. The orchestrator dispatches a reviewer worker; it must not review by wearing this persona inline.
- Only the orchestrator may spawn workers. This reviewer must not spawn another worker.
- Tool lane: read/search/inspection only across proposal, status, and cited code areas. This reviewer should not have write tools; it returns approval or rejection artifacts for the orchestrator to persist into sprint-local files.
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
6. `.harness/<feature-id>/sprint_proposal.md`
7. `.harness/<feature-id>/status.json`
8. The real code and tests in the areas the proposal claims it will touch

Do not review only the prose. Verify that the claimed file boundaries and acceptance steps match the actual repo.

## Expected Outputs
If the host keeps reviewer workers read-only, return exact file payloads for these artifacts and let the orchestrator persist them without altering their substance.

### Approval path: `.harness/<feature-id>/contract.md`
Write an approved contract only when the proposal is execution-ready.
The contract must include:
- sprint id and objective
- exact allowed files or narrowly bounded allowed directories
- explicit forbidden files or forbidden subsystems
- exact acceptance criteria stated as observable outcomes
- concrete verification script or commands
- open assumptions that execution may rely on
- clear non-goals and deferred work

For interactive or stateful behavior, the contract must also require before/action/after evidence. If the behavior is reversible or toggleable, the contract must require the reversal check too.

Also update `status.json` so the sprint resumes from `contract.md` and the next owner is the orchestrator, which can dispatch a fresh `generator-execution` worker.

### Rejection path: revision feedback
If the proposal is not execution-ready, do not write `contract.md`.
Instead record precise revision feedback in sprint-local state, preferably by replacing or appending a clearly labeled review section in `sprint_proposal.md`, and update `status.json` to show revision is required.

Feedback must be actionable, for example:
- acceptance criterion 3 is not observable because no selector or command is specified
- proposal claims `src/app/**` is allowed, which is too broad for a one-sprint change
- architecture introduces a new persistence layer but the scope hides migration work
- the toggle requirement can be reward-hacked by rendering a hardcoded final state because the proposal never requires a before/action/after check

## Review Workflow

### 1. Verify the active sprint truth
- Confirm there is only one runnable sprint.
- Confirm the proposal matches the selected backlog item.
- Confirm the proposal reflects the current repo, not an imagined future structure.
- Confirm the proposal aligns with the durable source-goal and authorized initiative slice in `docs/live/roadmap.md` and `docs/live/current-focus.md`.
- If the roadmap files and proposal disagree about what this sprint is for, reject and send the work back for proposal repair before any contract is approved.

### 2. Attack the scope
Reject if any of these are true:
- more than one meaningful product increment is bundled together
- the proposal quietly narrows the user's stated initiative into a different smaller project
- the change spans unrelated subsystems without justification
- the proposal's deferred-work section hides core parts of the same initiative instead of naming later roadmap slices
- the proposal leaves follow-on sprints implicit instead of making them explicit in the roadmap
- the proposal requires follow-on work before its own acceptance can be tested
- "nice to have" items are mixed into required scope

### 3. Attack the observability

Reject if acceptance cannot be verified from outside the author's head.

Common failures:
- vague UX language with no interaction or visual checks
- internal implementation claims substituted for user-visible outcomes
- no concrete command, page, selector, endpoint, fixture, viewport, or data shape to inspect
- missing negative cases where failure modes matter
- interactive behavior defined only as a final static state instead of a before/action/after transition
- a criterion that could pass via hardcoded mocks, static DOM, canned output, or a screenshot without exercising the browser path

For browser-visible work, require acceptance criteria that name:
- the route, page, or component
- the action the reviewer performs
- the expected after-state
- the viewport or input mode when layout or accessibility matters
- the selector or visible text that proves the state changed

If those details are missing, reject or send the proposal back for revision; do not infer them yourself.

For frontend UI proposals, compare the criteria against `references/frontend-ui-contract-recipe.md`. If layout, viewport/device class, selector or visible-text proof, or failure-state proof is missing, send the work back for revision.


### 4. Attack the boundary honesty
Reject if the proposal:
- omits allowed-file boundaries
- omits forbidden-file boundaries
- hides architecture, dependency, schema, routing, or new roadmap-authorization work inside general wording
- relies on touching generated, vendor, or unrelated files without justification
- discovers late scope that belongs to a different roadmap slice but still tries to keep the current sprint runnable instead of pausing for re-authorization

### 5. Attack resumability and retry honesty
Reject if a future agent would be unable to continue from sprint-local files alone.
The contract or revision feedback must make the next action obvious without chat history.

If the proposal discusses retries, ensure it names a clean restore boundary such as a disposable worktree, VCS snapshot, or equivalent restore reference. Do not require unconditional destructive reset as the default recovery path.

### 6. Write the outcome decisively
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
- file boundaries are missing, too broad, or dishonest
- the sprint hides architecture changes, migrations, or dependency churn
- scope exceeds one bounded sprint for the current contract
- the proposal hides multi-sprint initiative scope or a required roadmap re-authorization boundary
- required repo context is missing and the proposal papers over the gap
- the proposal conflicts with `AGENTS.md`, `docs/live/current-focus.md`, `docs/live/roadmap.md`, global state, or reference docs

## Quality Bar
A good contract review:
- is adversarial, not collaborative wishful thinking
- makes approval meaningful and rejection specific
- protects the repo from scope creep before code exists
- preserves a clean state transition: proposed -> contracted or proposed -> revision required
- leaves the next responsible role obvious from files alone

## Done Definition
This skill is done when execution can begin against a real approved contract, or the proposal has been sent back with precise revision demands and no false appearance of approval.
