---
name: backend-qa
description: Use when validating backend behavior in real execution paths, including APIs, jobs, queues, webhooks, auth boundaries, data integrity, failure handling, observability, performance, or adversarial backend conditions.
---

# Backend QA

## Overview

Backend QA validates what downstream consumers and operators actually get from a service.
Signoff lens: **Utility × Reliability × Contract** — does it produce the needed outcome,
stay honest under failure and concurrency, and tell the truth in its schemas, permissions, and errors.

Shared QA methodology is defined in [core.md](references/core.md). Read it first.
This file defines only backend-specific extensions.

## Domain-Specific Passes

In addition to the 7 core passes defined in core.md:

- **State & data emphasis** — retries, deduplication, transactions, concurrent mutation, compensating paths
- **Resilience emphasis** — poison-message handling, queue replay, partial outage recovery
- **Contract emphasis** — status code accuracy, idempotency rules, ordering guarantees, error taxonomy

## Signoff Criteria

- Missing **Utility**: the endpoint returns valid output that doesn't solve the consumer's job → FAIL
- Missing **Reliability**: concurrent or duplicate requests corrupt state, recovery depends on luck → FAIL
- Missing **Contract**: callers cannot distinguish auth failure from validation failure from dependency failure → FAIL

## References

- [core.md](references/core.md) — Shared QA methodology
- [Framework](references/framework.md) — Utility × Reliability × Contract in detail
- [Playbook](references/playbook.md) — Pass execution playbook
- [Reporting](references/reporting.md) — Findings format and severity classification
