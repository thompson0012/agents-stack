---
name: backend-qa
description: Use when validating backend behavior in real execution paths, including APIs, jobs, queues, webhooks, auth boundaries, data integrity, failure handling, observability, performance, or adversarial backend conditions.
---

# Backend QA

## Overview
Backend QA is evidence-first validation of what downstream consumers and operators actually get from a service. Judge the system through the lens of Utility × Reliability × Contract: does it produce the needed outcome, does it stay honest under failure and concurrency, and do its schemas, permissions, and errors tell the truth.

## Core Contract
- Test real execution paths before signoff whenever the live path is available.
- Separate functional, contract, state-and-data, resilience, observability, security-abuse, and adversarial coverage.
- Judge observable service behavior, not implementation intent.
- Treat retries, duplicates, concurrency, partial failure, and recovery as first-class states.
- Record evidence from the request, job, queue, trace, log, metric, or data state where each claim is true.

## When to use
Use this skill when a backend service, API, worker, queue, webhook flow, or auth boundary needs honest validation before signoff, release, handoff, incident triage, or risk review.

## When not to use
Do not use this skill for backend implementation, pure architecture or design work, mock-only speculation when a real path is available, or non-validation tasks such as prompt writing.

## Workflow
1. Build a QA inventory from consumer jobs, service contracts, state transitions, risky failure modes, and signoff claims.
2. Run a functional pass on the core success paths across APIs, jobs, queues, or webhooks.
3. Run a contract pass on status codes, schemas, permissions, idempotency, ordering, and error semantics.
4. Run a state-and-data pass on writes, reads, retries, deduplication, transactions, and before or after invariants.
5. Run a resilience pass covering dependency failure, timeouts, partial outage, restart, retry, poison-message, and recovery behavior.
6. Run observability, performance, security-abuse, and adversarial passes on traces, metrics, logs, load signals, auth boundaries, malformed inputs, duplicates, concurrency, and large or unusual payloads.
7. Record findings with evidence, severity, classification, and explicit unverified gaps.

## References
- [Framework](references/framework.md)
- [Playbook](references/playbook.md)
- [Reporting](references/reporting.md)
- [QA Inventory Template](../../../docs/reference/qa-inventory.md)

## Failure Modes
- Mistaking one successful request for backend signoff.
- Declaring behavior correct because the code path looks reasonable.
- Ignoring retries, duplicate delivery, or concurrent mutation because they are harder to stage.
- Treating missing logs, traces, or metrics as a documentation issue instead of a QA finding.

## Final Checklist
- [ ] QA inventory covers consumer jobs, contracts, data transitions, and risky failure modes.
- [ ] Functional, contract, state-data, resilience, observability, security-abuse, and adversarial passes were run.
- [ ] Evidence exists for each pass.
- [ ] Findings distinguish confirmed defects, contract gaps, environment issues, and product tradeoffs.
- [ ] Signoff reflects Utility × Reliability × Contract, not just absence of crashes.
