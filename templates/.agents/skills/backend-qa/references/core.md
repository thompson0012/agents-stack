# QA Core — Shared Methodology

This reference defines the shared QA methodology used by `backend-qa` and `frontend-qa`.
Each domain skill references this core and adds only domain-specific passes and signoff criteria.

## QA Inventory

Build a QA inventory before any pass execution. The inventory covers:
- Consumer jobs or user workflows
- Service contracts, schemas, or visible UI claims
- State transitions or interaction states
- Risky failure modes
- Signoff claims

## Pass Structure

Every QA execution follows this sequence:

1. **Functional pass** — Core success paths
2. **Contract pass** — Status codes, schemas, permissions, idempotency, error semantics
3. **State & data pass** — Writes, reads, retries, deduplication, before/after invariants
4. **Resilience pass** — Dependency failure, timeouts, partial outage, restart, recovery
5. **Observability pass** — Logs, traces, metrics, load signals
6. **Security / abuse pass** — Auth boundaries, malformed inputs, concurrency, unusual payloads
7. **Adversarial pass** — Edge cases, extreme inputs, rapid interaction, failure states

(Each domain skill may add domain-specific passes beyond these 7 core passes.)

## Evidence Rules

- Test the real path before signoff when available. A screenshot, DOM dump, or code inspection alone is not proof.
- Record evidence from the state where each claim is true.
- Include the interaction or request that produced the evidence.
- Separate confirmed defects, contract gaps, environment issues, and product tradeoffs.

## Output Contract

Every QA execution produces:

1. **QA Inventory** — What was tested against
2. **Evidence Ledger** — Per-pass findings with reproduction steps
3. **Findings** — Labeled by severity, classification, and evidence basis
4. **Signoff Statement** — Reflects the domain lens, not just absence of crashes
5. **Unverified Gaps** — Explicitly listed; never silently omitted

## Core Failure Modes

| Failure | Why it fails |
|---------|-------------|
| Confusing one successful path with signoff | Most failures live in non-happy-path states |
| Declaring behavior correct because the code looks reasonable | Behavior is in the runtime, not the source |
| Ignoring retries, duplicates, or concurrency because they're harder to stage | These are first-class states, not edge cases |
| Treating missing observability as a docs issue | Missing logs/traces/metrics is a QA finding |
