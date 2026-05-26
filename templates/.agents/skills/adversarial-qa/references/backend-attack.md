# Backend Attack

Attack running backend services. This domain is about injecting failures, malformed inputs, and adversarial conditions into real execution paths.

This reference extends the **Adversarial Pass** from [backend-qa](../../backend-qa/references/core.md) — that pass defines the framework; this reference defines the attack patterns.

## Mindset

The system works when everything goes right. Your job is to make things go wrong — systematically.

## Attack Patterns

### 1. Input Fuzzing

For every API endpoint, function, or job entry point, inject:

| Attack | What to inject |
|---|---|
| **Malformed JSON** | Missing commas, trailing commas, duplicate keys, nested depth > 100 |
| **Type violation** | String where number expected, array where object expected, null where required |
| **Boundary values** | Empty string, 0, -1, MAX_INT, MAX_INT+1, NaN, Infinity |
| **Encoding attacks** | UTF-8 BOM, null byte injection, Unicode normalization edge cases, emoji in ID fields |
| **Large payloads** | 1KB, 1MB, 10MB, 100MB — at what size does the system break? |
| **Schema violation** | Extra fields, missing required fields, wrong field types, nested objects with wrong structure |

### 2. Concurrent Mutation

For every state-mutating operation, run concurrent requests:

- 2 concurrent writes to the same resource — last write wins or conflict detection?
- 1 read + 1 write simultaneously — read sees partial state?
- 2 concurrent deletes — second one errors or silently succeeds?
- N concurrent creates of the same unique resource — duplicate or rejection?
- 1 write + 1 delete simultaneously — write to deleted resource succeeds?

### 3. Resource Exhaustion

Push each resource type to its limit:

| Resource | Attack |
|---|---|
| **Database connections** | Open N+1 concurrent connections beyond pool limit |
| **Memory** | Request a resource that loads large data (100MB+ JSON, 10K records) |
| **File handles** | Trigger operations that open files without closing them |
| **Threads/workers** | Submit more concurrent jobs than available workers |
| **Network sockets** | Open connections without reading responses |
| **Disk space** | Fill storage with logging or file uploads |

### 4. Dependency Failure

For every external dependency the system calls:

| Dependency | Failure mode | What to observe |
|---|---|---|
| **Database** | Connection refused, connection timeout, query timeout, read-only mode | Does the system degrade gracefully or crash? |
| **Queue** | Enqueue timeout, queue full, broker unreachable | Are messages lost or queued for retry? |
| **LLM API** | Timeout (5s, 30s, 120s), 429 rate limit, 500 error, malformed response, empty response | Does the caller have proper timeout and error handling? |
| **Third-party API** | Slow response (10s, 30s), wrong status codes, unexpected response body, auth token expired | Is there circuit-breaking? Fallback? |
| **Cache (Redis)** | Connection refused, eviction storm, key space full | Does the system fall back to DB correctly? |

### 5. LLM-Specific Attacks

Since LLM calls are a common and uniquely unreliable dependency:

- **Malformed JSON response** — LLM returns `{broken json` instead of valid JSON. How is this handled?
- **Empty string response** — LLM returns `""`. Is this treated as valid?
- **Hallucinated schema** — LLM returns valid JSON but with fields that don't match the expected schema
- **Excessively long response** — LLM returns 100K tokens instead of expected 100. Does the system truncate, error, or OOM?
- **Slow streaming** — LLM streams tokens at 1 per second. Does the caller timeout?
- **Content policy refusal** — LLM returns "I cannot answer this" instead of the expected structured output

### 6. Timeout Cascade

Map every timeout in the system and test the cascade:

```
User → API Gateway (30s timeout)
         → Service A (20s timeout)
              → DB query (5s timeout)
              → LLM call (15s timeout)
         → Service B (10s timeout)
              → External API (8s timeout)
```

What happens when:
- DB query takes 6s (exceeds its 5s timeout, but Service A's 20s hasn't expired)
- LLM call takes 16s (A's upstream 20s still hasn't expired, but LLM's 15s has)
- External API takes 9s (B's 10s hasn't expired, but underlying 8s has)

## Attack Procedure

1. Identify all entry points (API endpoints, job handlers, webhooks, message consumers)
2. For each entry point, apply the fuzzing patterns — record what breaks
3. Identify all state-mutating operations — test concurrent mutations
4. Identify all resource constraints — test exhaustion
5. Map all external dependencies — inject failure into each
6. Map all timeout chains — test every timeout boundary
7. For LLM-reliant systems, run the LLM-specific attack suite
8. Compile findings

## Integration with backend-qa

The backend-qa skill's **Adversarial Pass** (Pass 7 in core.md) defines the methodology for adversarial testing. Use it as your foundation. This reference adds specific attack patterns to execute within that pass.

When attacking a backend, load the backend-qa skill and reference its adversarial pass, then apply these attack patterns.
