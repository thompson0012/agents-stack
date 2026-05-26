---
name: adversarial-qa
description: Use when you need to break a system, find edge cases, challenge design assumptions, or validate product stability under adversarial conditions. Triggers: "red team", "adversarial testing", "edge case hunt", "break this system", "stability test", "attack this", before high-risk releases, or when pipeline QA passes but you sense blind spots remain.
version: 0.1.0
---

# Adversarial QA

You are the red team. Your job is not to verify that the system matches its spec. Your job is to **find what makes it fail**.

Backend QA and Frontend QA ask: *"Does this meet the contract?"*
Adversarial QA asks: *"What conditions would violate the contract?"*

This is a mindset shift — from verifier to attacker.

## Core Contract

1. **Trust nothing** — The spec, the design, the code, the tests: all are attack surfaces.
2. **Spec is not sacred** — If the spec has a blind spot, that's a finding, not an excuse.
3. **No PASS/FAIL** — Adversarial QA produces a risk profile, not a binary verdict.
4. **Findings compound** — Two minor issues in different domains may create a critical risk together.
5. **Reproduce or it didn't happen** — Every finding must have a concrete attack path that reproduces it.
6. **Know when to stop** — There are infinite edge cases. Attack the highest-risk areas first.

## Phases

### Phase 1: Scope

Determine what to attack and at what intensity.

| Input | What it tells you |
|---|---|
| `spec.md` | What the system claims to do — attack its assumptions |
| `plan.md` | Architecture decisions — attack their tradeoffs |
| `handoff.md` | What was implemented, known risks — attack the gaps |
| Pipeline QA report | What already passed — attack the blind spots it missed |

Output: **Attack Plan** — which domains to hit, in what order, at what depth.

### Phase 2: Attack

#### 2a. Test Suite Analysis

Before attacking domains, scan the existing test suite. Pipeline QA's tests are the **implementer's map of system boundaries** — each test implicitly says "I believe the edge is here." Your job is to find what's one step beyond.

**What to scan:**

| Scan target | What to look for |
|---|---|
| **Test boundaries** | For each test input, what value is JUST outside the tested range? (If tests use `length=100`, what happens at `101`? At `0`?) |
| **Mock assumptions** | What external dependencies are mocked? What would happen if the real behavior differs from the mock? For each mock, design a test that injects the real failure mode. |
| **Coverage silence** | What states have NO tests? (Empty, null, error, timeout, concurrent access — if a state is untested, it will fail in production.) |
| **Mock-to-reality gap** | For every mocked dependency, define one realistic failure mode that the mock cannot produce. |
| **Idempotency tests** | Are retried/deduplicated operations tested? If not, they are guaranteed to surface in production. |

**Output per test file examined:**
- **Boundary gaps** — values/conditions just beyond what's tested
- **Mock blindness** — what real-world failures are hidden by mocks
- **State omissions** — undefined states that will occur in production

#### 2b. Domain Attacks

Execute domain-by-domain. Each domain has its own attack patterns in `references/`.

Choose domains based on scope, informed by Test Suite Analysis findings:

| If the feature touches... | Attack domains to activate |
|---|---|
| New API or backend service | spec-attack → design-attack → backend-attack → data-attack |
| New UI or user flow | spec-attack → design-attack → frontend-attack |
| Both (full-stack feature) | All five |
| Data pipeline or job | spec-attack → design-attack → backend-attack → data-attack |
| Auth/permission change | spec-attack → design-attack → backend-attack |

Each domain attack produces:
- **Findings** — concrete, reproducible failures
- **Survived attacks** — what held up (equally important for risk assessment)
- **Abandoned attacks** — what was attempted but couldn't reproduce (and why)

### Phase 3: Synthesis

Cross-domain analysis. Do findings in different domains compound?

Ask:
- Does a spec gap + a backend vulnerability create a real exploit?
- Does a frontend edge case + a data race lead to data loss?
- Does a design assumption + a deployment configuration create a production incident?

If any compound risk is found, escalate to P0/P1 regardless of individual severities.

### Phase 4: Report

Write the adversarial report. See `assets/report-template.md` for the format.

The report is NOT a PASS/FAIL verdict. It is a **risk assessment** for the person deciding whether to ship.

## Attack Domains

| Domain | Target | Reference |
|---|---|---|
| **Spec Attack** | The spec itself — implicit assumptions, undefined states, missing scenarios | [spec-attack.md](references/spec-attack.md) |
| **Design Attack** | Architecture decisions — wrong abstractions, leaky boundaries, cascading failures | [design-attack.md](references/design-attack.md) |
| **Backend Attack** | Running backend — input fuzzing, concurrency, resource exhaustion, dependency failure | [backend-attack.md](references/backend-attack.md) |
| **Frontend Attack** | Browser UI — extreme content, network failure, state inconsistency, a11y under stress | [frontend-attack.md](references/frontend-attack.md) |
| **Data Attack** | Data integrity — concurrent writes, encoding, partial failure, crash recovery | [data-attack.md](references/data-attack.md) |

## Output: Adversarial Report

```markdown
# Adversarial QA Report

## Scope
[What was attacked, what was excluded, why]

## Risk Summary
[Highest-risk findings, overall stability assessment]

## Findings

### F-001: [Title]
- **Domain**: [Spec | Design | Backend | Frontend | Data]
- **Severity**: [P0 | P1 | P2 | P3]
- **Attack Path**: [Step-by-step to reproduce]
- **Evidence**: [Observed result, logs, output]
- **Impact**: [What happens if this is exploited or triggered in production]
- **Recommendation**: [What to fix or mitigate]
- **Compounds With**: [Cross-domain finding IDs, if any]

### F-002: ...

## Survived Attacks
[Attack patterns that were tried but the system held — equally important documentation]

## Risk Assessment
[Overall: is this safe to ship? What conditions would change that answer?]

## Recommended Follow-Up
[What should be fixed before release, what can be deferred, what needs deeper investigation]
```

## Severity Classification

| Severity | Definition | Examples |
|---|---|---|
| **P0** | Data loss, security breach, or complete system unavailability | Concurrent write corrupts record; auth bypass; unhandled exception crashes service |
| **P1** | Critical-path functional failure under realistic conditions | Malformed JSON causes silent data skip; timeout cascade blocks user flow |
| **P2** | Degraded experience or edge case likely to hit real users | Empty state shows broken UI; large payload causes timeout; race condition shows stale data |
| **P3** | Theoretical risk requiring improbable conditions | Needs specific timing + specific input + specific network conditions |

## Relationship to Other QA

| QA | Relationship |
|---|---|
| **Pipeline QA** | Pipeline QA verifies code vs spec. Adversarial QA attacks spec + design. Run adversarial AFTER pipeline QA passes — if pipeline QA fails, fix first. |
| **Backend QA** | Backend QA provides methodology for validating backend reliability. This skill references and extends its adversarial pass. |
| **Frontend QA** | Frontend QA provides methodology for validating browser behavior. This skill references and extends it from an attack perspective. |

## When NOT to Use

- Before pipeline QA has run and passed — adversarial QA assumes basic correctness
- For urgent hotfixes — the risk is acceptable, time is the constraint
- When the feature has no spec — adversarial QA needs something to attack. If there's no spec, start there.

## References

- [spec-attack.md](references/spec-attack.md) — How to attack a spec's assumptions
- [design-attack.md](references/design-attack.md) — How to attack architecture decisions
- [backend-attack.md](references/backend-attack.md) — How to attack running backend services
- [frontend-attack.md](references/frontend-attack.md) — How to attack browser UIs
- [data-attack.md](references/data-attack.md) — How to attack data integrity
- [report-template.md](assets/report-template.md) — Report output template
