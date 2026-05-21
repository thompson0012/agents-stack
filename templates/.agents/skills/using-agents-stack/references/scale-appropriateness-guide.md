# Scale Appropriateness Guide

> **Supplementary reference.** The primary complexity audit framework is `references/complexity-signals.md` — a catalog of universal over-engineering patterns. This guide provides scale-specific severity modifiers and floor expectations. Use it alongside complexity-signals, not instead of them.

This reference helps workers calibrate what "just right" means at different project scales.

## The Floor Concept

The floor is not about minimalism. It's about **necessary surface**: the code, structure, and patterns without which the product cannot do its job. Cut below the floor and the product breaks. Add above the floor without evidence and you're carrying dead weight.

| What | Floor or not? |
|------|---------------|
| The product can't function without it | **Floor** — keep |
| The product functions but maintenance/debugging is painful | **Above floor** — investigate alternatives |
| No one can name the concrete problem it solves | **Above floor** — cut |
| "Best practice" or "we might need it later" | **Above floor** — cut unless evidence exists |
| Enables a stated requirement (testing, auth, data integrity) | **Floor** — keep |

## The Three Scales

Scale determines where the floor sits. The same product concept at different scales has different floors.

| Scale | Team | Users | Life span | Floor posture |
|-------|------|-------|-----------|---------------|
| **internal_tool** | 1-3 | Internal only | Months–2yr | Lowest floor. Single-file patterns often sufficient. |
| **team_service** | 3-15 | Internal org or early adopters | 2–5yr | Moderate floor. Structure for team collaboration. |
| **distributed_product** | 15+ or external | External, paying customers | 5yr+ | Higher floor. Structure for scale, compliance, multiple teams. |

## Floor Per Concern

These are defaults, not absolutes. Deviate with evidence.

| Concern | `internal_tool` floor | `team_service` floor | `distributed_product` floor |
|---------|----------------------|---------------------|---------------------------|
| **Modular decomposition** | One file per distinct responsibility. Split when >300 lines or 2+ clear domains. | One file/package per bounded context. Shared conventions documented. | Full module boundaries with explicit contracts. |
| **Interfaces/abstractions** | None unless 2+ concrete implementations exist today, OR the abstraction is required for testing a non-trivial dependency. | Interfaces at module boundaries where test doubles are needed for non-trivial deps. | Interfaces at every external boundary. |
| **Dependency wiring** | Direct imports or a single wiring function. | Single wiring file/module per entrypoint. | DI container or explicit wiring layer with configuration. |
| **Error handling** | Handle errors at call sites. `try/except` or `Result<T,E>`. | Consistent error wrapping with context. | Error taxonomy with recovery strategies, observability hooks. |
| **Configuration** | `.env` or single config object. | Config module with schema validation. | Config hierarchy with environment-specific overrides, secrets management. |
| **Testing** | Tests that prove correctness for critical paths. | Tests at module boundaries + integration tests for key flows. | Comprehensive unit + integration + contract + e2e. |
| **Async/queues/workers** | Synchronous unless async is a stated requirement. | Queues for actual async operations (notifications, long jobs). | Event-driven where scale requires it. |
| **Observability** | `print()` / `console.log` at key decision points. | Structured logging with request IDs. | Full tracing, metrics, alerting. |

## Judging "Above Floor" Additions

For anything above the floor, ask:

1. **What concrete problem does this solve?** — "Separation of concerns" is not concrete. "When Alice and Bob edit this file simultaneously, they merge-conflict on the routing table" is concrete.
2. **What's the evidence this problem exists or will exist?** — Past incidents, user complaints, team friction, stated requirements.
3. **What's the simplest solution to JUST this problem?** — Not the elegant general solution. The point solution that makes the pain go away.
4. **What does keeping it cost?** — Files, layers, lines, onboarding time, refactoring resistance.

If you can't answer #1 and #2, the addition is above-floor without evidence. Default to cut.

## Scale Misalignment Signals

These patterns suggest the architecture is calibrated for a higher scale than the project actually is:

| Signal | What it means |
|--------|---------------|
| >3 layers to trace one operation | Layers exist for architectural purity, not concrete problems. |
| Interface with 1 implementation and no test double need | The interface is indirection, not abstraction. |
| DI framework for a single-entrypoint project | Manual wiring would be shorter than the framework config. |
| Multi-provider abstraction with 1 provider | "Future-proofing" without a concrete trigger. |
| Repository/DAO layer with simple CRUD | The ORM/driver IS the repository for this scale. |
| Event bus / message queue for synchronous flows | Async complexity without async requirements. |
| Pattern vocabulary in code (Factory, Strategy, Observer) without the problem those patterns solve | Pattern application, not problem solving. |

None of these signals mean "always wrong." They mean "justify or cut."

## Quick Triage

Before reviewing a design or implementation, answer:

1. **Scale**: `internal_tool` / `team_service` / `distributed_product`?
2. **Floor check**: What's the minimum necessary surface for this sprint's behavior?
3. **Above-floor audit**: Is everything above the floor backed by concrete evidence?
4. **Misalignment check**: Any scale-misalignment signals from the table above?

If #3 finds additions without evidence, or #4 finds signals without justification → the design has unnecessary complexity.

## Usage

- `spec` phase: classify the project scale and scope requirements against the floor table.
- `plan` phase: use this guide as the judgment framework for overspecification.
- `prune-review`: use the floor concept as the primary lens — everything above-floor gets challenged.
