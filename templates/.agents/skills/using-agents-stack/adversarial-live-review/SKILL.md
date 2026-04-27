---
name: adversarial-live-review
description: Use when after generator execution has produced a handoff and runtime details, and before `state-update` has reconciled the review outcome.
purpose: Run a skeptical QA pass against the actual implementation and contract, then issue a decisive PASS, FAIL, or BLOCKED verdict with corrective or recovery directives.
trigger: After generator execution has produced `.harness/<sprint-id>/handoff.md` and `.harness/<sprint-id>/runtime.md`, and before `state-update` has reconciled the review outcome.
inputs:
  - AGENTS.md
  - docs/reference/architecture.md
  - docs/reference/design.md
  - docs/live/tracked-work.json
  - .harness/<sprint-id>/contract.md
  - .harness/<sprint-id>/handoff.md
  - .harness/<sprint-id>/runtime.md
  - .harness/<sprint-id>/status.json
outputs:
  - .harness/<sprint-id>/qa.md
  - .harness/<sprint-id>/review.md
  - .harness/<sprint-id>/status.json
boundaries:
  - Do not edit implementation files except to capture review artifacts explicitly requested by the harness.
  - Do not soften a failure because the intent was good.
  - Do not pass work that cannot be reproduced.
  - Do not update global project state.
next_skills:
  - state-update
---

# Adversarial Live Review

## Placement
This is a nested child under `using-agents-stack`; its path is `using-agents-stack/adversarial-live-review/`, and the router selects it before standalone use.

You are the skeptical evaluator. Assume the implementation is wrong, incomplete, or misleading until evidence proves otherwise.

Your job is to judge the observable result against the contract, not to admire the effort that produced it.

## Worker Dispatch Contract

- Run live review in a fresh worker context. The orchestrator dispatches a reviewer worker; it does not swap into review mode inline.
- Only the orchestrator may spawn workers. This reviewer must not spawn another worker.
- Tool lane: read, runtime reproduction, browser/QA inspection, and evidence capture only. This reviewer should not have write tools to product code or live state; it returns `qa.md`, `review.md`, and `status.json` payloads for the orchestrator to persist.
- Parallel-safe only for independent acceptance checks that share no mutable environment and write to separate evidence fragments. The orchestrator must assign stable reviewer worker IDs, await every sibling fragment result, record a merged result ledger, and only then synthesize one decisive review record.
- Durable return contract: `.harness/<sprint-id>/qa.md`, `.harness/<sprint-id>/review.md`, and `.harness/<sprint-id>/status.json`, each traceable with stable reviewer `worker_id` / `orchestrator_run_id` when the host provides them. If parallel review fragments were used, the merged result ledger must preserve each fragment's worker id, finding ids, and artifact paths.
- Dispatch framing is non-authoritative. Before reviewing, verify that the dispatched sprint still matches `docs/live/tracked-work.json`, that the claimed review phase still matches the strongest local artifact on disk, and that stronger evidence in the `AGENTS.md` precedence chain beats any dispatch summary, stale resume hint, or copied orchestrator context.
- If those checks disagree with the dispatch frame, stop before writing review artifacts, preserve the existing truthful files, and hand control back to the orchestrator for correct-lane dispatch.

## Preconditions

Review starts only when these files exist:
- `.harness/<sprint-id>/contract.md`
- `.harness/<sprint-id>/handoff.md`
- `.harness/<sprint-id>/runtime.md`

If `handoff.md` says the sprint is blocked, build-failed, awaiting human input, or escalated, do not invent a PASS path. Produce a BLOCKED review only when review truly cannot proceed and route to `state-update`; otherwise the sprint should have bypassed review already.

## Review standard

A sprint passes only when all of the following are true:
1. Every contract acceptance criterion id from `contract.md` is independently checked.
2. The running app or artifact behaves as claimed.
3. The result stays within contract scope.
4. Required commands or tests were executed, or the contract explicitly permits another form of evidence.
5. Another agent could reproduce the result from the recorded runtime notes.
6. Interactive or other stateful criteria prove a real before/action/after transition, not just a plausible final screenshot, static DOM, or one-time final value.
7. `review.md` reports a findings list where every finding names a severity label and an explicit `duplicate_of` value (`none` for canonical findings).
8. Coverage metadata is present and truthful: `areas_reviewed`, `areas_not_reviewed`, `coverage_status`, `criteria_total`, `criteria_checked`, and `all_acceptance_criteria_accounted_for`.
9. `qa.md` and `review.md` both preserve criterion-level coverage keyed by stable `AC-###` ids.
10. Convergence metadata is present and truthful: `convergence_status` and `open_blocking_findings_count`.
11. After deduplicating findings whose `duplicate_of` points at another open finding, there are zero open P0 / P1 / P2 / P3 findings, `coverage_status` is `complete`, and `convergence_status` is `closed`.
12. Advisory findings outside P0 / P1 / P2 / P3 may remain recorded, but they must be clearly labeled non-blocking and must not be smuggled into PASS as unnamed caveats.

Any gap in reproducibility, scope control, acceptance evidence, or review metadata is a review failure. Missing coverage or convergence metadata fails closed.

## Review procedure

### 1. Read the contract first

Extract the following into your own notes before testing:
- observable objective
- required acceptance checks
- allowed and forbidden changes
- explicit non-goals

Do not let the generator redefine success in `handoff.md`.
### Methodology note: domain QA playbooks

After reading the contract, use the narrowest matching playbook(s) or contract recipe(s) to structure the review:

- `frontend-qa` plus `references/frontend-ui-contract-recipe.md` for browser-visible or UI-centric acceptance
- `backend-qa` plus `references/backend-api-contract-recipe.md` for APIs, jobs, queues, webhooks, auth boundaries, data integrity, and observability
- `references/integration-contract-recipe.md` when the contract depends on third-party APIs, callbacks, or other external-system boundaries
- `references/async-worker-contract-recipe.md` when the contract centers on background execution, retries, or queue semantics
- `references/migration-contract-recipe.md` when the contract proves schema/data transitions across time

If a sprint spans multiple surfaces, use the matching combination. These playbooks shape inventory, checks, and evidence capture only. They do not change phase ownership, routing, or the PASS / FAIL / BLOCKED contract, and the worker still produces one harness-owned `qa.md` and one `review.md`.


### 2. Read the execution evidence critically

Use `handoff.md` and `runtime.md` to answer:
- what should I run?
- where should I look?
- what was already verified?
- what could not be verified?
- what assumptions did the generator make?

If instructions are vague, incomplete, or contradictory, record that as a review defect.

### 3. Reproduce the implementation

Prefer the generator's documented commands. If they are missing or unusable, try the minimum repository-derived recovery steps, such as discovering package scripts or the default local URL.

When you must infer missing runtime details:
- write the inference and evidence source into `qa.md`
- keep the inference minimal
- FAIL the sprint if reproducibility still depends on guesswork

### 4. Execute the contract checks

For each acceptance criterion, record it by stable `AC-###` id and capture:
- exact before-state when the criterion is interactive or otherwise stateful
- exact action taken
- exact after-state observed
- reverse or repeat action when the behavior should be reversible
- PASS / FAIL / BLOCKED / NOT_RUN judgment
- proof location or supporting output

For UI work, inspect the live app, not screenshots alone. For non-UI work, use the strongest available observable check: commands, HTTP responses, logs, database effects, queue state, job records, or generated artifacts. Stateful non-UI behavior still needs before/action/after evidence tied to the declared action.

Across the full review, maintain a review-wide coverage inventory for `areas_reviewed` and `areas_not_reviewed`, a contract-check ledger keyed by `AC-###`, and a findings ledger with stable finding ids, severities, statuses, and `duplicate_of` links. If any required area or acceptance criterion cannot be checked, set `coverage_status: incomplete`, mark the missing criterion explicitly, and FAIL closed rather than inferring completion.

### 5. Look for reward hacking and contract violations

FAIL the sprint when you observe any of the following, even if the final screen or output looks correct:
- implementation changed files or behavior outside the approved contract
- reviewer cannot reproduce the environment from recorded notes
- tests or commands required by the contract were skipped without approval
- the generator introduced plausible-looking but unverified claims
- the implementation regressed adjacent behavior the contract implicitly depends on
- an interactive or other stateful criterion passes only because of a hardcoded final state, static mock, canned response, pre-seeded data, or other shortcut that does not exercise the real transition
- a toggle, undo, or reversible behavior reaches the final state once but cannot reverse cleanly when the contract implies reversibility

## Auditability: your review may itself be reviewed

Your review output is subject to independent audit by a subsequent reviewer worker. The orchestrator may dispatch a second specialist to verify your findings, severity labels, evidence paths, and verdict. This means:

- Every finding must reference specific, repeatable evidence — a command output, a URL with observed state, a before/action/after log — not subjective impressions or unverifiable claims.
- Another agent must be able to reproduce your checks from `qa.md` alone, without access to your chat history or intermediate notes.
- Severity labels (P0–P3, ADVISORY) must be justified in the finding description, not asserted without support.
- `duplicate_of` links must name a specific finding ID that the auditor can independently verify is the same root cause.
- `coverage_status`, `convergence_status`, and `open_blocking_findings_count` must match the evidence in `qa.md` — an auditor can recompute them from first principles.
- If a follow-up reviewer disagrees with your verdict or finds that your evidence does not support your conclusion, that disagreement is recorded as a separate audit finding, not suppressed.

Write your output as if a skeptical colleague will read it tomorrow. This protects the verification chain from cascading bias.

## Required outputs
If the host keeps reviewer workers read-only, return exact file payloads for these artifacts and let the orchestrator persist them without altering their substance.

## `.harness/<sprint-id>/qa.md`

This is the detailed evidence log. Use a structure like:

```md
# QA Evidence: <SPRINT-ID>

## Reviewer Trace
- worker_id:
- orchestrator_run_id:

## Environment Used
- Start command:
- URL / entrypoint:
- Test command:

## Coverage Metadata
- areas_reviewed:
  - ...
- areas_not_reviewed:
  - none
- coverage_status: complete | incomplete
- criteria_total: 2
- criteria_checked: 2
- all_acceptance_criteria_accounted_for: true

## Acceptance Checks
### AC-001: <criterion summary>
- Before state:
- Action:
- After state:
- Reverse / repeat check:
- Status: PASS | FAIL | BLOCKED | NOT_RUN
- Evidence:

### AC-002: <criterion summary>
- Before state:
- Action:
- After state:
- Reverse / repeat check:
- Status: PASS | FAIL | BLOCKED | NOT_RUN
- Evidence:

## Findings Ledger
- `RV-001` | severity=P1 | status=OPEN | duplicate_of=none
  - Summary: ...
- `RV-002` | severity=ADVISORY | status=OPEN | duplicate_of=none
  - Summary: ...

## Convergence Summary
- convergence_status: open | closed
- open_blocking_findings_count: 1

## Reproducibility Gaps
- ...

`qa.md` should be factual and granular. It is the raw evidence that supports `review.md`.

## `.harness/<sprint-id>/review.md`

This is the decision memo. Use a structure like:

```md
# Adversarial Review: <SPRINT-ID>

## Status
PASS | FAIL | BLOCKED

## Reviewer Trace
- worker_id:
- orchestrator_run_id:

## Coverage Metadata
- areas_reviewed:
  - ...
- areas_not_reviewed:
  - none
- coverage_status: complete | incomplete
- criteria_total: 2
- criteria_checked: 2
- all_acceptance_criteria_accounted_for: true

## Findings
- `RV-001` | severity=P1 | status=OPEN | duplicate_of=none
  - Summary: ...
- `RV-002` | severity=P1 | status=OPEN | duplicate_of=RV-001
  - Summary: same root cause as RV-001
- `RV-003` | severity=ADVISORY | status=OPEN | duplicate_of=none
  - Summary: ...

## Convergence Summary
- convergence_status: open | closed
- open_blocking_findings_count: 1
- blocking_severities_considered: P0, P1, P2, P3

## Decision Summary
- ...

## Contract Check Results
- `AC-001` | status=PASS | evidence=qa.md#AC-001
- `AC-002` | status=FAIL | evidence=qa.md#AC-002

## Reward-Hacking / Scope Findings
- ...

## Corrective Directives
1. ...
2. ...

Every FAIL or BLOCKED outcome must include recovery directives that are specific enough for the next orchestrator decision or generator retry to act on without reopening the problem framing. Every finding line must carry severity and `duplicate_of`, and `open_blocking_findings_count` counts only open non-duplicate P0 / P1 / P2 / P3 findings.

## `.harness/<sprint-id>/status.json`

At review completion:
- set `phase: "reviewed_pass"`, `"reviewed_fail"`, or `"reviewed_blocked"`
- set `owner_role: "orchestrator"`
- set `resume_from: "review.md"`
- update timestamps and any review artifact pointers the harness uses

The review phase ends by routing to `state-update`, never by editing code.

## Edge-case rules

### Runtime details are missing
If the generator did not provide enough detail to reproduce the app:
- attempt minimal repo-based discovery
- record exactly what you inferred and why
- FAIL the sprint if the result still depends on undocumented knowledge

Missing runtime evidence is itself a review finding.

### Tests cannot be executed
If the contract requires tests and they cannot be run:
- try the exact command documented by the generator
- capture the failure or missing dependency in `qa.md`
- FAIL unless the contract explicitly allows alternative evidence for that check

If tests are optional and live behavior is still verifiable, note the gap but judge based on the contract.

### Implementation exceeded contract scope
If the feature works but the generator touched out-of-contract files or behavior:
- record the exact overreach
- FAIL the sprint unless the contract was formally amended before execution
- direct the next generator either to revert the extra work or to obtain a revised contract

## PASS / FAIL / BLOCKED routing

### PASS
PASS means the implementation is verifiably complete and the review loop is converged. It does not mean “looks good enough.”

On PASS:
- ensure `qa.md` and `review.md` both exist
- ensure every contract criterion id has evidence and a matching `Contract Check Results` entry
- ensure `criteria_total`, `criteria_checked`, and `all_acceptance_criteria_accounted_for` honestly reflect the checked `AC-###` set
- ensure interactive or other stateful criteria include before/action/after proof and reversibility proof when applicable
- ensure `coverage_status: complete`, `convergence_status: closed`, and `open_blocking_findings_count: 0`
- ensure no open non-duplicate P0 / P1 / P2 / P3 finding remains
- ensure `templates/.agents/skills/using-agents-stack/scripts/validate_review_against_contract.py <sprint-id> --repo-root <repo-root>` would return `allow`
- route immediately to `state-update`

### FAIL
FAIL means the sprint stays active and must be corrected. Preserve all evidence. FAIL is mandatory whenever any open non-duplicate P0 / P1 / P2 / P3 finding remains, or when required coverage / convergence metadata is missing or incomplete.

On FAIL:
- keep the sprint artifacts intact
- name the failing criteria and reproduction steps
- preserve finding ids, severities, statuses, and `duplicate_of` links so the next review loop can converge honestly
- issue corrective directives ordered by importance
- instruct the next owner to fix the findings and rerun review
- route immediately to `state-update`

### BLOCKED
BLOCKED means the reviewer could not truthfully reach PASS or FAIL because an environment, dependency, or missing-prerequisite problem prevented judgment. Missing review bookkeeping is not BLOCKED; it is FAIL because the review is incomplete.

On BLOCKED:
- keep the sprint artifacts intact
- name the blocking condition and the exact missing prerequisite or failing command
- issue recovery steps ordered by importance
- route immediately to `state-update`

Never erase evidence to make the next pass look cleaner.
