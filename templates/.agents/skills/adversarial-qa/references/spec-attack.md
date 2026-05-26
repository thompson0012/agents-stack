# Spec Attack

Attack the spec itself. The spec defines what the system claims to do — your job is to find what it doesn't say, what it assumes, and what it gets wrong.

## Mindset

Every spec is an incomplete model of reality. Your job is to find the gaps.

## Attack Patterns

### 1. Implicit Assumptions

For every "Given" precondition in the spec, ask: **"What if this precondition is false?"**

| Pattern | Example |
|---|---|
| Assumes user exists | What if user was deleted between authorization and action? |
| Assumes data is valid | What if the data was written by a previous version that allowed different values? |
| Assumes system state | What if another request already modified this state? |
| Assumes external service is available | What if the LLM/DB/payment gateway is down? |
| Assumes time is linear | What if a request arrives with a timestamp from the future? From 5 years ago? |

### 2. Undefined States

For every state transition in the spec, ask: **"What states are NOT defined?"**

- What is the system's state before first use?
- What is the state after a partial operation (halfway through a transaction)?
- What is the state after a failure and retry?
- What is the state when two conflicting operations happen simultaneously?
- What is the state after data migration?
- What is the state when a dependency returns an unexpected response?

### 3. Missing Scenarios

For every AC in the spec, ask: **"What scenario is NOT covered?"**

- Happy path is defined — what about all the ways it can fail?
- Single-user flow is defined — what about concurrent users on the same resource?
- Success response is defined — what about every error response code?
- Common input is defined — what about empty, null, maximum, minimum, and malformed input?
- Fresh state is defined — what about after 1000 operations?

### 4. Conflicting Requirements

Look for ACs that cannot simultaneously be true:

- "Must respond in < 50ms" vs "Must validate against external API"
- "Must never lose data" vs "Must accept fire-and-forget requests"
- "Must be eventually consistent" vs "Must return immediately after write"

### 5. Terminology Ambiguity

Flag every term that could mean different things to different readers:

- "Active user" — logged in? used in last 24h? has a session?
- "Save" — committed to DB? acknowledged? durable?
- "Delete" — soft delete? hard delete? reversible?
- "Processed" — received? validated? stored? acted upon?

## Attack Procedure

1. Read the spec once for understanding
2. Read it again, line by line, asking: "What is this NOT saying?"
3. For each AC, write down the implicit assumptions it makes
4. For each assumption, ask: "What breaks if this assumption is wrong?"
5. For each undefined state, construct a concrete scenario that exercises it
6. Check for conflicting requirements and ambiguous terminology
7. Compile findings into the adversarial report

## Output

- **F-00X: Spec gap — [what's missing]**
  Severity P2/P3 (spec gaps are rarely production blockers alone, but they compound with other domain findings)
- **F-00X: Assumption failure — [what assumption, what breaks]**
  Severity P1/P2 depending on how likely the assumption is violated in production
- **F-00X: Conflicting requirements — [which ACs, why they conflict]**
  Severity P1 — this indicates the spec cannot be fully satisfied
