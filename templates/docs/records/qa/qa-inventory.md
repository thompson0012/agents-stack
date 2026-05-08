# QA Inventory

Use this file before any validation pass to build a checklist that covers what must be proven, not just what is easy to test.

## What it is

A QA inventory is a written list of claims that must be verified before signoff. It is built from requirements, visible promises, contracts, risky states, and edge cases—not from the tester's convenience.

Every signoff claim must map to at least one explicit check. If a claim has no check, the inventory is incomplete.

---

## Universal Sections

Use these for any surface, frontend or backend.

### 1. Requirements Mapping

List the specific requirements or user stories this surface is supposed to satisfy.

| Requirement | How to verify | Evidence needed |
|-------------|-------------|-----------------|
|             |             |                 |

### 2. Visible Claims

List every promise the surface makes to its consumer.

- What outcomes are guaranteed?
- What states are communicated explicitly?
- What actions are available and what do they do?

### 3. Risky States and Transitions

List the states most likely to hide defects.

- Loading, empty, error, retry, partial data
- State transitions that involve persistence or async work
- Navigation away and return
- Concurrent or repeated actions

### 4. Signoff Claims

List the specific statements you will make at signoff, and the evidence that supports each.

| Signoff claim | Evidence | Verified |
|---------------|----------|----------|
|               |          | [ ]      |

### 5. Unverified Gaps

Explicitly list what you did not check, and why.

| Gap | Reason | Risk level |
|-----|--------|------------|
|     |        |            |

---

## Frontend-Specific Additions

Use these when validating a browser surface.

### Viewports and Devices

- Supported viewport ranges
- Touch vs. mouse input classes
- Theme or mode variations (light, dark, high-contrast, reduced-motion)

### Interaction Surfaces

- Core user journeys from entry to completion
- Reversible interactions (cancel, back, undo)
- Keyboard, focus, and assistive-technology paths
- Touch target size and mobile ergonomics

### Visual States to Inspect

- Initial viewport
- Post-interaction states
- Dense or maximum-content states
- Smallest supported viewport
- Loading, empty, success, error states

### Adversarial Front-End Stress

- Empty, null, partial, and maximum data
- Long strings, unusual Unicode, RTL, mixed-direction text
- Rapid repeated actions and double submit
- Slow, partial, or failed network
- Resize, zoom, font scaling, reduced-motion
- Overlapping UI states (modals, toasts, dropdowns, validation)

---

## Backend-Specific Additions

Use these when validating a service, API, job, queue, or webhook.

### Consumer Jobs and Contracts

- Endpoints, events, jobs, webhooks, queue messages
- Auth boundaries and permission checks
- Idempotency, ordering, and pagination guarantees
- Expected vs. actual status codes, schemas, error semantics

### State and Data Touch Points

- Authoritative stores touched by the workflow
- State transitions and invariants
- Duplicate prevention and at-most-once / at-least-once behavior
- Transactional boundaries and rollback paths

### Resilience and Failure Paths

- Slow or failing dependencies
- Timeout and cancellation behavior
- Partial outage (one dependency fails while others succeed)
- Worker restart, process crash, redelivery during in-flight work
- Poison messages, dead-letter handling, retry exhaustion
- Degraded mode or fail-closed behavior

### Observability Sources

- Logs, traces, metrics available for this flow
- Correlation identifiers joining request → downstream call → final outcome
- Queue depth, lag, saturation, throughput, latency signals

### Adversarial Backend Stress

- Malformed, partial, null, duplicate, or schema-adjacent payloads
- Rapid repeated requests, duplicate webhook deliveries, concurrent writes
- Large payloads, deep nesting, long strings, unusual Unicode, boundary numerics
- Delayed dependencies, reordered events, stale retries, replay after recovery
- Mismatched auth context, expired tokens, revoked permissions, cross-tenant references

---

## Minimum State Coverage Checklist

Before signoff, verify you have touched the states the surface meaningfully supports.

### Frontend

- [ ] default / initial
- [ ] loading
- [ ] empty
- [ ] populated
- [ ] success
- [ ] error
- [ ] partial data
- [ ] dense or maximum data
- [ ] disabled or read-only
- [ ] unauthorized or redirected

### Backend

- [ ] success
- [ ] validation failure
- [ ] unauthorized or forbidden
- [ ] not found
- [ ] conflict or duplicate
- [ ] accepted and pending async work
- [ ] retry and replay
- [ ] partial dependency failure
- [ ] timeout or cancellation
- [ ] concurrent mutation
- [ ] maximum or unusual input
- [ ] recovery after restart or redelivery

---

## Evidence Rules

- Record the exact state, request, or input that triggered the behavior.
- Capture reproduction steps, not just outcomes.
- Quote exact text when reporting copy, labels, errors, or contract fields.
- Use screenshots or recordings when they clarify a visual or motion claim.
- Record before and after data state when persistence or integrity is involved.
- Keep notes on what remains unverified so the report does not overclaim.
