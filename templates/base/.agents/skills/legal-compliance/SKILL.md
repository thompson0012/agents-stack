---
name: legal-compliance
description: Use when in-house legal work involves privacy compliance obligations such as DPA review, data subject requests, breach timelines, international transfers, or regulatory monitoring.
---

# Legal Compliance

## Overview
Use this skill for operational privacy and compliance support inside an in-house legal function. It focuses on recurring workflows: privacy-law issue spotting, DPA review, data subject request handling, cross-border transfer checks, and regulatory monitoring.

## When to Use
Use this skill when work involves:
- GDPR, UK GDPR, CCPA/CPRA, or similar privacy-law obligations
- Reviewing vendor or customer DPAs and transfer terms
- Handling data subject or consumer rights requests
- Assessing breach-notification timing and escalation needs
- Tracking new privacy rules, regulator guidance, or enforcement developments
- Advising teams on privacy-by-design or records-of-processing obligations

Do not use this skill for:
- Bespoke litigation strategy
- Product counseling unrelated to data, privacy, or regulatory obligations
- Jurisdiction-specific legal advice that requires local counsel beyond issue spotting

## Quick Reference

### Core Response Timelines
| Regulation | Acknowledge | Substantive response | Extension |
|---|---|---|---|
| GDPR / UK GDPR | Promptly as best practice | 30 days | +60 days for complex requests with notice |
| CCPA / CPRA | 10 business days | 45 calendar days | +45 days with notice |
| LGPD | Not specified | 15 days | Limited |

### High-Importance Privacy Deadlines
| Event | Deadline or expectation |
|---|---|
| GDPR supervisory authority breach notice | Within 72 hours of awareness |
| Processor notice to controller | Without undue delay; aim for 24-48 hours contractually |
| GDPR data subject rights response | Within 30 days unless validly extended |
| CCPA/CPRA request acknowledgment | Within 10 business days |

### Regulation Triggers to Spot Early
| Topic | What to check |
|---|---|
| GDPR / UK GDPR | Lawful basis, Article 30 records, DPIA need, transfers, DPO requirement |
| CCPA / CPRA | Notice at collection, rights workflow, opt-out or sharing mechanics, service-provider terms |
| Cross-border transfers | Adequacy, SCCs, UK addendum, transfer impact assessment, supplementary measures |
| Breach response | Awareness date, affected jurisdictions, risk level, regulator and individual notice triggers |

## Workflow

### 1. Identify the governing regime
At intake, confirm:
- Where the individuals are located
- Which group entity is processing the data
- Whether the company is acting as controller/business or processor/service provider
- Whether sensitive, special-category, employee, children’s, or cross-border data is involved

This determines both the deadline and the contract posture.

### 2. Review DPAs against required clauses
A usable DPA review should confirm:
- Subject matter, duration, nature, and purpose of processing
- Types of personal data and categories of data subjects
- Processing only on documented instructions
- Personnel confidentiality commitments
- Appropriate security measures
- Sub-processor approval and flow-down obligations
- Assistance with data subject rights, security incidents, DPIAs, and regulator consultation
- Deletion or return of data at termination
- Audit rights or an acceptable audit-report substitute
- Breach notification language that supports regulatory deadlines

### 3. Check transfer mechanics separately
Do not assume the services agreement solves transfer risk. Confirm:
- The transfer mechanism is explicitly identified
- Current EU SCCs are used where required
- The correct SCC module is selected
- UK addendum is included if UK data is in scope
- A transfer impact assessment exists for non-adequate countries
- Supplementary technical or contractual measures match the risk

## DPA Negotiation Positions
| Issue | Why it matters | Default position |
|---|---|---|
| Blanket sub-processor authorization | Loss of visibility and control | Require notice and right to object |
| Breach notice over 72 hours | Controller may miss regulator deadline | Push for 24-48 hours |
| No audit rights | Hard to verify compliance | Accept SOC 2 Type II plus for-cause audit right |
| No deletion timeline | Data may linger indefinitely | Require deletion or return within 30-90 days |
| No processing locations | Hidden transfer or localization risk | Require disclosure of locations |
| Outdated SCCs | Transfer mechanism may be invalid | Require current SCC package |

## Data Subject Request Handling

### Intake checklist
Log at minimum:
- Date received
- Request type
- Requester identity and verification status
- Applicable law
- Response deadline
- Assigned owner

### Request types to classify correctly
- Access / right to know
- Rectification / correction
- Erasure / deletion
- Restriction
- Portability
- Objection
- Opt-out of sale or sharing
- Limit use of sensitive personal information

### Response sequence
1. Verify identity proportionately.
2. Freeze deletion if a litigation hold or legal retention obligation applies.
3. Locate the requester’s data across systems.
4. Apply exemptions and document the legal basis.
5. Prepare the response or denial with jurisdiction-specific language.
6. Record what was produced, withheld, deleted, or escalated.

### Common exemptions to check
- Legal claims or defense
- Statutory or regulatory retention obligations
- Rights of third parties
- Public-interest, research, or archival grounds where available
- Internal litigation hold or investigation needs

## Breach and Escalation Triggers
Escalate immediately when:
- A personal-data breach may trigger a 72-hour deadline
- Special-category or sensitive data is involved
- Cross-border transfer mechanisms may be invalid or challenged
- A regulator inquiry, audit, or complaint arrives
- A new law or enforcement trend affects core business activities
- A compliance deadline requires product, contract, or process changes

For any suspected breach, record:
- Awareness time
- Systems and data categories affected
- Jurisdictions and estimated number of individuals involved
- Containment status
- Notification recommendation and approval path

## Regulatory Monitoring
Maintain a lightweight but repeatable process:
- Subscribe to key regulator updates and official announcements
- Track enforcement actions in the company’s sector
- Maintain a calendar of effective dates and implementation deadlines
- Summarize only changes that affect products, contracts, notices, or operational controls
- Escalate changes that require legal, engineering, security, or commercial action

Priority authorities and sources commonly include:
- EU supervisory authorities and the EDPB
- UK ICO
- California Privacy Protection Agency and California AG
- FTC and relevant state AGs
- Major overseas regulators where the business operates

## Common Mistakes
- Starting a DPA review without first deciding the company’s role and applicable law
- Treating transfer language as boilerplate instead of a separate risk area
- Accepting processor breach notice windows that make the 72-hour GDPR deadline unrealistic
- Fulfilling deletion requests without checking for litigation hold or legal retention duties
- Tracking regulatory news without turning it into operational actions, owners, and dates
- Logging rights requests inconsistently, making deadline compliance hard to prove
