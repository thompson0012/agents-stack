# Sprint Contract: [FEATURE-###] [short title]

<!--
  Template: .agents/skills/using-agents-stack/references/templates/.harness/contract.md
  Owner: evaluator-contract-review
  Copy into .harness/<WORKSTREAM-ID>/contract.md after proposal approval.
  This is the approved execution boundary. Execution must not exceed it.
  Delete this comment block before use.
-->

## Approved Scope

[Derived from sprint_proposal.md, refined by contract review. Exact file list and boundaries.]

### Allowed Files

- `path/to/file.ts`

### Forbidden Areas

- [explicitly out of bounds]

## Contract Acceptance Criteria

Each criterion must be independently verifiable as a state transition. Hardcoded end-state checks that pass without exercising the feature are invalid.

- **AC-001**: [before-state] → [action] → [expected after-state]
- **AC-002**: [before-state] → [action] → [expected after-state]

## Build / Startup Triage

[Minimum check to prove the sprint is reviewable: build command, test command, or smoke test.]

## Review Instructions

[How a reviewer reproduces the result. Commands, environment, expected observable behavior.]

## Risk Acknowledgement

[Risks accepted at contract time. Reviewer will check these.]
