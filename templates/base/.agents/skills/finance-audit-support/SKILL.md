---
name: finance-audit-support
description: Use when supporting SOX 404 or internal-control audit work, especially for scoping controls, selecting samples, testing evidence, documenting workpapers, or evaluating deficiencies.
---

# Finance Audit Support

## Overview
Use this skill for practical audit support work around internal controls over financial reporting. It is optimized for walkthroughs, control testing, evidence evaluation, workpaper quality, and deficiency assessment rather than broad accounting analysis.

## When to Use
Use this skill when work involves:
- SOX 404 scoping, risk assessment, or control identification
- Design-effectiveness walkthroughs or operating-effectiveness testing
- Sample selection for recurring or transaction-level controls
- Workpaper preparation, evidence review, or reviewer-ready documentation
- Deficiency classification, aggregation, remediation, or retesting
- Comparing manual, automated, IT-dependent manual, ITGC, or entity-level controls

Do not use this skill for:
- Technical accounting conclusions unrelated to controls
- External audit opinion drafting
- Tax, valuation, or FP&A work

## Quick Reference

### Testing Sequence
1. Scope significant accounts and relevant assertions.
2. Identify the risk and the key control that addresses it.
3. Confirm design effectiveness through walkthroughs.
4. Test operating effectiveness over the full reliance period.
5. Evaluate exceptions, compensating controls, and aggregation.
6. Document conclusion, remediation, and retest plan.

### Common Assertions by Account
| Account area | Assertions to test first |
|---|---|
| Revenue | Occurrence, completeness, accuracy, cut-off |
| Accounts receivable | Existence, valuation, rights |
| Inventory | Existence, valuation, completeness |
| Fixed assets | Existence, valuation, completeness, rights |
| Accounts payable | Completeness, accuracy, existence |
| Accrued liabilities | Completeness, valuation, accuracy |
| Equity | Completeness, accuracy, presentation |
| Financial close/reporting | Presentation, accuracy, completeness |

### Design vs. Operating Effectiveness
| Question | Design effectiveness | Operating effectiveness |
|---|---|---|
| What is being proved? | The control is capable of preventing or detecting the risk | The control actually operated as designed |
| Typical procedures | Walkthrough, inquiry, process tracing | Inspection, observation, reperformance, inquiry |
| Timing | At least annually or after process change | Over the full period of reliance |
| Failure meaning | The control is not fit for purpose | The control was not performed reliably |

## Workflow

### 1. Scope the right controls
A control usually becomes key when it addresses a material risk for a significant account or disclosure.

Prioritize controls when the underlying area has:
- High transaction volume
- Significant estimates or management judgment
- Complex accounting
- Fraud exposure
- Prior errors, audit adjustments, or process changes
- Heavy reliance on one control with little redundancy

### 2. Choose a defensible sample method
| Method | Best use | Watch for |
|---|---|---|
| Random | Default for large homogeneous populations | Requires a complete population |
| Targeted | High-risk items, unusual items, period-end testing | Not representative on its own |
| Haphazard | Small homogeneous populations when random is impractical | Hidden tester bias |
| Systematic | Even coverage across a sequential population | Periodic population patterns |

Use targeted testing to supplement, not disguise, weak population support.

### 3. Set sample size by frequency and risk
| Control frequency | Low risk | Moderate risk | High risk |
|---|---:|---:|---:|
| Annual | 1 | 1 | 1 |
| Quarterly | 2 | 2 | 3 |
| Monthly | 2 | 3 | 4 |
| Weekly | 5 | 8 | 15 |
| Daily | 20 | 30 | 40 |
| Per-transaction, population under 250 | 20 | 30 | 40 |
| Per-transaction, population 250+ | 25 | 40 | 60 |

Increase sample size when:
- Inherent risk is high
- The control is the only control addressing a key risk
- A prior deficiency exists
- The control is new or recently changed
- External auditors will rely on management testing

### 4. Collect evidence that proves the control actually happened
Accept stronger evidence first:
- System logs with performer and timestamp
- Signed or system-recorded approvals
- Screenshots of enforced configurations or workflow blocks
- Reperformed calculations tied to source data
- Observation notes with date, place, and observer

Treat these as weak unless corroborated:
- Verbal confirmation
- Undated documents
- Reports with no provenance or timestamp
- Generic notes such as "per discussion"

### 5. Build reviewer-ready workpapers
Each test workpaper should show:
- Control ID, description, owner, frequency, type, and risk/assertion linkage
- Test objective and step-by-step procedure
- Population definition and sample selection rationale
- Evidence examined for each sample item
- Specific exceptions, not vague pass/fail labels
- Overall conclusion and basis
- Tester and reviewer sign-off

A good workpaper lets another auditor understand exactly what was tested, what evidence was inspected, and why the conclusion is supportable.

## Control-Type Checklist

### Manual controls
Confirm:
- Right person performed the control
- Control was timely
- Review evidence exists
- Reviewer had enough information
- Exceptions were identified and resolved

### Automated controls
Confirm:
- System configuration enforces the intended rule
- Relevant change-management ITGCs are effective
- Any configuration changes during the period trigger retesting

### IT-dependent manual controls
Test both:
- The human review or approval
- Completeness and accuracy of the underlying report or data (IPE)

### IT general controls
Focus on:
- Access provisioning, deprovisioning, privileged access, periodic access review, segregation of duties
- Change approval, testing, environment separation, emergency changes, post-implementation review
- Backups, batch monitoring, incident handling, disaster recovery, system availability

### Entity-level controls
Review:
- Tone at the top and code of conduct
- Audit committee oversight
- Risk assessment and fraud programs
- Monitoring of control effectiveness
- Financial reporting competence and close governance

## Deficiency Evaluation
| Classification | Practical threshold | Common indicators |
|---|---|---|
| Deficiency | Control design or execution failed, but impact is limited or mitigated | Isolated lapse, low likelihood, effective compensating control |
| Significant deficiency | Important enough for governance attention but short of material weakness | More-than-inconsequential exposure, weak key control, meaningful combination of issues |
| Material weakness | Reasonable possibility of material misstatement not being prevented or detected timely | Material misstatement not caught by controls, management fraud, ineffective oversight, pervasive control failure |

When exceptions arise:
1. Define the failure precisely.
2. Assess likelihood and magnitude.
3. Evaluate compensating controls.
4. Aggregate related issues affecting the same process or assertion.
5. Document root cause, remediation owner, target date, and retest plan.

## Common Mistakes
- Testing operation before proving the control is designed well
- Using judgmental samples without documenting why
- Relying on screenshots or reports that do not identify who did what and when
- Calling a control effective despite exceptions with no aggregation analysis
- Treating IT-dependent reports as trustworthy without IPE testing
- Writing workpapers that state conclusions without enough evidence to reproduce them
