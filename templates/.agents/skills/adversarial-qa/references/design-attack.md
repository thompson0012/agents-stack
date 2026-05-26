# Design Attack

Attack architecture decisions. The plan.md defines how the system is built — your job is to find which decisions are wrong, leaky, or fragile under pressure.

## Mindset

Every architecture decision is a tradeoff that looks good on paper and breaks under specific conditions. Find those conditions.

## Attack Patterns

### 1. Abstraction Leakage

For every abstraction boundary, ask: **"What does this abstraction NOT hide?"**

- Does the API expose implementation details (DB schema, internal IDs, framework types)?
- Does the interface require callers to know about internal state (ordering, timing, locking)?
- Does a "simple" method signature hide complex side effects?
- Can callers bypass the abstraction entirely?

### 2. Cascading Failure

For every dependency chain, ask: **"What happens when each link fails?"**

| Dependency | What if it... | Cascade effect |
|---|---|---|
| API A → API B | B is slow | A's connections pool exhausts, all callers of A are blocked |
| Service → Queue | Queue is full | Service blocks on enqueue, backpressure propagates |
| Function → LLM | LLM returns 5x slower | All concurrent requests accumulate, memory grows |
| Job → DB | DB connection pool is saturated | Jobs fail, retry, fail again — retry storm |
| Frontend → API | API returns 502 | Frontend shows loading spinner forever (no timeout) |

### 3. State Distribution

For every piece of state, ask: **"What happens when sources of truth disagree?"**

- Is the same data stored in multiple places (cache + DB, local state + server state)?
- What is the staleness window? Is it bounded?
- What happens when cache is evicted or expires?
- What happens when optimistic UI update fails and must roll back?
- What happens when two sources are updated in different orders?

### 4. Retry and Backpressure

For every retry policy, ask: **"What turns this retry into an amplifier?"**

- Retry without exponential backoff → retry storm
- Retry on dependency that is already failing → thundering herd
- Infinite retry on transient error → if it's not transient, infinite loop
- Retry without idempotency → duplicate side effects
- Retry across service boundaries → cascade amplification

### 5. Configuration and Environment

For every configuration value, ask: **"What if this is wrong?"**

- Hardcoded timeout in code vs configurable — what if the default is too low for production?
- Database connection pool size — calculated for what concurrency?
- Rate limits — what happens when they're hit? Graceful degradation or hard failure?
- Feature flags — what if a flag is toggled mid-operation?
- Environment variables — what if one is missing, empty, or has an unexpected value?

### 6. Security Boundary

For every permission check, ask: **"Who can bypass this?"**

- Is authorization checked at the API layer only? What if someone calls the internal function directly?
- Is tenant isolation enforced at the DB query level? Can a malformed query cross tenants?
- Are rate limits per-user or per-IP? Can one user exhaust the limit for everyone?
- Are secrets checked in at build time or read at runtime? What if the secret store is unreachable?

## Attack Procedure

1. Read plan.md — identify all architecture decisions, dependency chains, state models
2. For each decision, ask: "Under what conditions does this break?"
3. Trace failure cascades through the dependency graph
4. Look for retry amplification and backpressure vulnerabilities
5. Check configuration defaults against production conditions
6. Verify security boundaries are enforced at the right layer
7. Compile findings

## Output

- **F-00X: Cascading failure — [trigger condition] → [cascade path] → [final failure mode]**
- **F-00X: Leaky abstraction — [what the abstraction exposes]**
- **F-00X: Retry amplification — [the retry policy] → [what it amplifies]**
