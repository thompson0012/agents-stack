---
name: cx-ticket-triage
description: Use when triaging customer support tickets that need categorization, prioritization, duplicate checking, and routing to the right team.
---

# CX Ticket Triage

## Overview
Triage support tickets by identifying root cause, customer impact, urgency, and the team that should own next action. The output should help the next responder move immediately instead of re-reading the entire thread.

## When to Use
Use this skill when a ticket must be:
- categorized into a support taxonomy
- assigned a priority or SLA expectation
- checked for duplicates or known issues
- routed to support, engineering, product, security, or billing
- summarized with internal notes for handoff

Do not use it for deep technical investigation after ownership is already clear.

## Quick Reference

### Categories
| Category | Use for | Common signals |
| --- | --- | --- |
| Bug | Product behaves incorrectly | error, broken, crash, failing, unexpected |
| How-to | Customer needs guidance | how do I, where is, configure, help |
| Feature request | Customer wants missing capability | wish, request, any plans, would be great |
| Billing | Charges, invoices, plans | payment, refund, invoice, upgrade |
| Account | Access, settings, permissions | login, password, SSO, locked out |
| Integration | Third-party connection issues | API, webhook, OAuth, sync |
| Security | Security or compliance concerns | breach, unauthorized, GDPR, vulnerability |
| Data | Import, export, migration, data quality | missing data, duplicates, migration |
| Performance | Speed or availability issues | slow, timeout, latency, down |

### Priority Levels
| Priority | Use for | Response expectation |
| --- | --- | --- |
| P1 | Outage, data loss, security incident, most users blocked | within 1 hour |
| P2 | Major workflow blocked, many users affected, no workaround | within 4 hours |
| P3 | Partial breakage, workaround exists, limited blast radius | within 1 business day |
| P4 | Minor issue, question, cosmetic issue, feature request | within 2 business days |

## Workflow
1. Read the full ticket.
   - Later replies often change severity or clarify root cause.
2. Assign category by root cause.
   - If a login failure is caused by a product defect, treat it as `Bug`, not `Account`.
   - If a ticket contains both a bug and a feature ask, make the bug primary.
3. Set priority by impact.
   - Who is blocked?
   - Is there data loss, security risk, or expanding scope?
   - Is there a usable workaround?
4. Check for duplicates.
   - Search by symptom, customer, product area, and known issues.
   - Merge useful new evidence into the tracked issue.
5. Route to the right owner.
   - Tier 1 for standard guidance and known resolutions.
   - Tier 2 for investigation-heavy support issues.
   - Engineering for confirmed defects or infrastructure failures.
   - Product for validated feature demand or workflow gaps.
   - Security or Billing when domain ownership is explicit.
6. Leave an internal note.
   - State category, priority, routing decision, customer impact, known workaround, and what you already ruled out.

## Routing Guide
| Route to | Typical cases |
| --- | --- |
| Tier 1 support | how-to questions, password resets, documented fixes, basic billing questions |
| Tier 2 support | complex bugs, configuration issues, integration troubleshooting, account investigations |
| Engineering | confirmed code defects, outages, performance degradation, infrastructure failures |
| Product | feature requests with demand signals, design gaps, missing workflow support |
| Security | data exposure concerns, vulnerability reports, compliance issues |
| Billing/Finance | refunds, contract disputes, non-standard billing adjustments |

## Escalation Triggers
Increase urgency when:
- the wait time already exceeds SLA
- multiple customers report the same problem
- a workaround stops working
- the issue spreads to more users, data, or systems
- the customer cites executive or business-critical impact

## Response Patterns
Use concise replies that acknowledge impact and set expectations:
- Bug: confirm investigation, state priority, give workaround if real
- How-to: answer directly or give clear steps
- Feature request: confirm capture and route to product without promising delivery
- Billing: acknowledge urgency and state review timing
- Security: escalate immediately and avoid casual reassurance

## Common Mistakes
- Categorizing from surface symptom instead of root cause
- Under-prioritizing because only one customer reported an actually critical issue
- Skipping duplicate checks and creating fragmented incident tracking
- Routing without stating what was already checked
- Treating feature requests as bugs because the user is frustrated

## Triage Checklist
- [ ] Full thread read
- [ ] Primary category assigned
- [ ] Priority assigned from impact, not tone alone
- [ ] Duplicate and known-issue search completed
- [ ] Correct owner selected
- [ ] Internal handoff note captures context and next action
