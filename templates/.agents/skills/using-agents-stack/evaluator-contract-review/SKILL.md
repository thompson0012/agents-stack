---
name: evaluator-contract-review
description: Adversarially review a sprint proposal before any code is written.
purpose: Find gaps that would make the implementation wrong regardless of implementation quality.
trigger: `.harness/<workstream-id>/sprint_proposal.md` exists and no trustworthy approved contract is present.
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
  - .harness/<workstream-id>/review_feedback.md on rejection
  - .harness/<workstream-id>/review_trace.md (always — the gap report)
  - updated .harness/<workstream-id>/status.json
boundaries:
  - Do not implement. Do not soften requirements. Do not approve unverifiable work.
---

# Evaluator Contract Review

## Mission

Find **gaps** — things that must be true for the change to work that the proposal has not established.

A gap is not a "maybe." A gap is: "the proposal says X but doesn't say what happens when Y, and Y will happen." Your output is a gap report. If the report is empty, the proposal is approved. If it contains any gap, the proposal goes back for revision.

**You have one job: answer 10 questions. No severity labels. No classification tiers. No "caveats." Just gaps.**

---

## The 10 Questions

For each question, read the proposal. If you find a gap, describe it concretely. If you find none, write "no gap." Do not speculate. Do not invent gaps to prove you're thorough. A gap exists or it doesn't.

### Q1: What assumptions does this proposal make that aren't stated?

Scan for things the proposal takes for granted: "the database has seed data," "the service is configured," "the caller is authenticated," "the file already exists."

For each unstated assumption: what breaks if it's wrong?

A proposal with zero unstated assumptions is rare. That's fine — what matters is that the critical ones are surfaced. An assumption about the Go runtime existing is trivial. An assumption about a specific env var being set in production is not.

### Q2: What operations have no described failure handling?

For every operation the proposal describes (function calls, API requests, database queries, file I/O, network calls): does the proposal say what happens when it fails?

List every operation. For each: is the failure behavior described? If not, what's the most likely failure mode?

A proposal that says "errors are handled appropriately" has not described failure handling. "Handled" is not a specification.

### Q3: What external dependencies are called without describing the failure case?

Special case of Q2, isolated because external failures are the most destructive and most often missed. External = databases, APIs, message queues, object storage, auth services, payment gateways — anything outside the changed component.

For each external call: what happens when it's unreachable? When it times out? When it returns unexpected data? When it returns data in an unexpected format?

### Q4: What data access paths are described without specifying authorization?

For any path that reads or writes data that is not public: who is authorized? How is identity verified? What happens when identity is missing, expired, or unauthorized?

A proposal that says "auth middleware handles it" without specifying which middleware, which scopes, and which error responses has a gap.

### Q5: Are there any cross-module exchanges where the two sides disagree on format, semantics, or protocol?

For every boundary crossing between modules, services, or languages: does the producer's output format match the consumer's expected input format? If one side encrypts, does the other side use the same algorithm? If one side serializes, does the other side use the same schema?

This is the AES/XOR problem: each side is internally correct, they are mutually wrong.

### Q6: Do any two statements in the proposal contradict each other?

Scan for pairs of claims that cannot simultaneously be true. "Always returns a User struct" + "Returns null when user not found" (if User is not nullable). "Idempotent" + "Increments a counter." "No migration needed" + "Adds a NOT NULL column."

### Q7: Can each acceptance criterion be verified from outside the author's head?

For each AC: is there a concrete command, page, endpoint, selector, or data shape to inspect? Can a reviewer determine — without asking the author — whether the criterion is met?

"Better UX" is not verifiable. "After deployment, `GET /users/123` returns 200 with `last_active` present and non-null" is verifiable.

### Q8: What existing defense layers does this change pass through or bypass?

Beyond authorization (Q4): rate limiting, audit logging, input sanitization, PII scanning, circuit breakers, timeouts, retry budgets. Does the change pass through these layers? Does it create a path that bypasses them? Does it assume they exist without verifying?

A proposal that adds a new data access path without mentioning any defense layer has a gap — even if authorization is specified.

### Q9: If multiple operations compose into one action, what happens when some succeed and some fail?

When the proposal describes "do A, then B, then C" — are A, B, C atomic? If A succeeds and B fails, is the system in a consistent state? What cleans up A's effects?

A proposal that describes a multi-step action without addressing partial failure has a gap.

### Q10: Does the proposal align with the active roadmap and current focus?

Does the proposal target the correct backlog item? Does it match the authorized initiative slice in `docs/live/roadmap.md`? Is there only one runnable sprint active?

A proposal that solves a different problem than what the roadmap authorizes has a gap — regardless of how well-designed it is internally.

---

## Gap Report (review_trace.md)

Output a gap report with this structure:

```markdown
## Review Trace — <sprint-id>
Date: <date>

### Q1 — Unstated Assumptions
- **GAP**: The proposal assumes the `organizations` table already has a row for every user's `org_id`. What breaks: if an org is missing, the FK constraint rejects the insert. The proposal should either (a) add a NOT NULL check with a clear error, or (b) explicitly state this assumption and its risk.
- **GAP**: The proposal assumes the `AUTH_SERVICE_URL` env var is configured. What breaks: the service won't start or will crash on first request.

### Q2 — Missing Failure Handling
- no gap

### Q3 — External Dependency Failures
- **GAP**: Calls `POST /payment/charge`. No failure handling described. Most likely failures: timeout (payment provider down), insufficient funds, invalid card. The proposal should specify what the caller receives in each case.

...
```

Every gap entry must include: (1) what the gap is, (2) what breaks if unaddressed.

If a question has no gaps, write "no gap." Do not leave it blank — blank is ambiguous.

---

## Verdict

| Condition | Verdict |
|-----------|---------|
| Gap report is empty (all 10 questions → "no gap") | **APPROVE** → write `contract.md` |
| Gap report has any gap | **REQUEST REVISION** → write `review_feedback.md` with the gap report, update `status.json` to `phase: "proposal_revision_required"` |

That's it. Two verdicts. No caveats, no partial approvals, no severity tiers. A proposal with gaps goes back. A proposal without gaps goes forward.

---

## Rules

### All Gaps in One Pass
List every gap you find. Do not hold gaps back for a second round. The revision loop exists for the proposer to fix gaps, not for you to discover them incrementally.

### Gap, Not Opinion
A gap is "the proposal doesn't say what happens when X fails." An opinion is "I would design this differently." Do not report opinions as gaps. If the proposal specifies a design you disagree with but the design is complete (all 10 questions answered), there is no gap.

### Unknown Is a Gap
If the proposal is too vague to determine whether a gap exists — that IS a gap. "The proposal doesn't describe the error path clearly enough to assess" is a valid gap entry for Q2.

### One Pass, Not Two
You have one pass. Answer all 10 questions. Your output is the gap report. Do not iterate on your own review. If the proposal is revised and re-submitted, a fresh evaluator worker will review it.

### Existing Code Is Evidence
When answering Q3, Q4, Q5, Q8 — read the actual code the proposal claims to touch. Do not trust the proposal's description of existing behavior. Verify against the repo.

---

## Quick Reference

| Q | Question | What It Catches |
|---|----------|----------------|
| 1 | Unstated assumptions? | Implicit prerequisites that break if wrong |
| 2 | Missing failure handling? | Happy-path-only proposals |
| 3 | External dependency failures? | "Calls X" without "what if X is down" |
| 4 | Authorization gaps? | New data paths with no access control |
| 5 | Cross-module inconsistency? | AES/XOR, format mismatches |
| 6 | Internal contradictions? | Claims that cancel each other |
| 7 | Unverifiable ACs? | "Better UX" — no measurable outcome |
| 8 | Defense layer gaps? | Missing rate limiting, audit, sanitization |
| 9 | Partial failure? | Multi-step actions without atomicity |
| 10 | Scope alignment? | Wrong backlog item, wrong initiative slice |
