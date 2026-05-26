# Data Attack

Attack data integrity. This domain is about finding what causes data loss, corruption, inconsistency, or silent correctness failures.

## Mindset

The system probably handles the happy data path correctly. Your job is to find the operations, concurrency patterns, and edge cases that silently corrupt or lose data.

## Attack Patterns

### 1. Concurrent Write Conflicts

For every write operation, test concurrent access:

| Pattern | What to test |
|---|---|
| **Two concurrent updates** | Both read old state, both compute new state, both write — last write wins, losing one update |
| **Concurrent update + delete** | Update reads a record, delete removes it, update writes to a now-deleted record |
| **Concurrent create** | Two requests create a record with the same unique key — duplicate or error? |
| **Concurrent insert + read** | One request inserts, another reads — does the read see the insert? (read-after-write consistency) |
| **Batch + concurrent update** | A batch operation reads a set, an individual update modifies one record, batch writes stale data |

### 2. Partial Failure in Batch Operations

For every operation that affects multiple records:

- Does a 10-record batch succeed even if record 5 fails?
- Is the system in a consistent state after partial batch failure?
- Are already-processed records rolled back, or is the batch partially committed?
- Can the caller distinguish "all succeeded", "partial success", and "all failed"?

### 3. Large Payload and Encoding

| Attack | What to test |
|---|---|
| **Maximum field size** | What happens when a string field exceeds the DB column size? Truncation? Error? Silent write? |
| **Deep nesting** | JSONB/document fields with 10, 50, 100 levels of nesting |
| **Unicode edge cases** | 4-byte UTF-8 (emojis, rare CJK), zero-width characters, BOM, null byte (\u0000) |
| **Very long identifiers** | 255-char username, 512-char email, 1000-char title |
| **Encoding mismatch** | Write UTF-8, read as latin-1 (or vice versa) — does the application layer handle this? |

### 4. Crash Recovery

| Scenario | What to observe |
|---|---|
| **Crash mid-write** | Kill the process while writing a record. After restart, is the record complete, absent, or corrupted? |
| **Crash mid-batch** | Kill during a batch operation. Is the state between "before" and "after" consistent? |
| **Crash mid-migration** | Kill during a DB migration. After restart, is migration rolled back or partially applied? |
| **Double restart** | Start, crash immediately, restart, crash again — does recovery handle this? |

### 5. Idempotency Violations

For every operation that claims to be idempotent:

- Send the same request twice — is the state identical after 1 and 2 requests?
- Send the same request with the same idempotency key but different body — which is accepted?
- Send the same request with the same idempotency key after the first completes — is the first response replayed?
- Send a request, get a timeout (but it actually succeeded on the server), send again — duplicate?

### 6. Retention and Cleanup

| Attack | What to test |
|---|---|
| **Data retention expiry** | What happens exactly at the retention boundary? Is data deleted atomically? |
| **Soft delete cascade** | Soft-delete a parent record. Do child records reference the deleted parent? |
| **Cleanup job failure** | A scheduled cleanup job fails halfway. Is the next run idempotent? |
| **Orphan records** | Delete a user/workspace/project — are all related records deleted, or are there orphans? |
| **Aggregation inconsistency** | A counter that tracks "number of items" — is it consistent after concurrent add/remove? |

### 7. Race Between Consistency Models

| Pattern | What to test |
|---|---|
| **Write → cache → read** | Write to DB, write to cache, read from cache — what if cache write fails? |
| **Optimistic locking** | Two concurrent reads get version=1. Both write with version=1. Second write should fail — does it? |
| **Read after write consistency** | Write, immediately read from a different replica/node — do you see the write? |
| **Eventual consistency window** | How long after a write can a read return stale data? Is this bounded? |

## Attack Procedure

1. Identify all CRUD operations and their data models
2. For each write operation: test concurrent access patterns
3. For each batch operation: test partial failure, verify rollback
4. For each field: test maximum size, encoding, and boundary values
5. For each claimed idempotency guarantee: attempt to violate it
6. For each retention/cleanup policy: test boundary conditions
7. For each caching layer: test consistency after write failures
8. Compile findings

## Output

- **F-00X: Data loss — [what operation, what condition]** → P0
- **F-00X: Data corruption — [what scenario, what state]** → P0/P1
- **F-00X: Idempotency violation — [what operation]** → P1
- **F-00X: Race condition — [what reads/writes conflict]** → P1/P2
- **F-00X: Encoding/truncation — [what field, what value]** → P2
