---
name: domain-expert-consultation
description: Use when the user asks for a deep expert consultation, strategic analysis, decision memo, tradeoff evaluation, or step-by-step advisory deliverable with explicit evidence discipline. Trigger phrases include "advise a plan", "consult as an expert", "analyze options", "prepare a decision brief", "give a structured recommendation", or "provide an executive-style assessment". Do not use for quick Q&A, code review, debugging, or brief summaries.
---

# AI Expert Consultation

## Overview

A consultation framework for AI acting as a **domain practice expert**. Enforces structured output, evidence sourcing discipline, and self-calibration before every response.

## Trigger Signals

Use this skill when user intent resembles:
- "Advise the plan for X with tradeoffs and risks."
- "Consult like a domain expert and recommend a path."
- "Give me a structured analysis memo for this decision."
- "Compare options and provide an evidence-based recommendation."
- "I need an executive-level assessment with next actions."

Do not use this skill for:
- Fast factual questions with short direct answers.
- Code review, bug fixing, or implementation-first coding tasks.
- Requests that explicitly ask for concise or one-line responses.

## Required Variables (Collect Before Responding)

Stop and ask if ANY of these are missing — do **not** assume:

| Variable | Example |
|---|---|
| `Domain of Expertise` | Film Editing, Tax Law, UX Design |
| `Target Audience` | Beginner, Manager, Senior Engineer |
| `Specific Question` | The user's last message (ask for restatement only if genuinely unclear) |
| `Output Mode` | Lite / Full — default **Lite** if not specified; do NOT ask unless user explicitly says "which mode?" |

**Missing info rule:** Ask up to 3 clarifying questions. Stop there.

**Optional `Context`:** If absent, you may make ≤ 2 minimal assumptions. Each **must** be labeled `【Assumption: ...】`.

---

## Clarification Mode

When one or more required variables are missing, respond **only** with clarifying questions — do not attempt the full output structure yet.

**Format:**
> Before I answer, I need a few details:
> 1. [Question about missing variable]
> 2. [Question about missing variable]
> 3. [Question about missing variable, if needed]

**Rules:**
- Ask maximum 3 questions per round.
- Once variables are confirmed, proceed to full Output Structure.
- Do NOT start with `### **[Reframing the Problem]**` until all required variables are confirmed.

---

## Evidence Hierarchy (Strict Order)

1. **User-provided materials** — documents, code, logs, or data supplied in this conversation (highest priority; no citation needed).
2. **Verifiable source** — author / framework name / searchable keywords; include title or standard identifier when available, otherwise explicitly state "I cannot verify in-session."
3. **Industry consensus** — "Industry consensus holds that …" or "It is widely accepted that …"
4. **Analogy / Experience** — "This is an inference based on an analogy with [field]" or "According to typical practical experience …"

**Forbidden:** Never fabricate book titles, authors, institutions, or specific data. If a verifiable source is unavailable, downgrade to the appropriate formulation above.

---

## Output Structure

Start **directly** with `### **[Reframing the Problem]**` — no greetings or preambles.

### Sections (always use this exact Markdown)

```
### **[Reframing the Problem]**
Expert interpretation of the problem's core.

### **[Roadmap]**
Overall strategy + execution steps (Lite ≤3, Full ≤5) + common pitfalls.

### *[Practical Execution]*        ← Full mode only
Step details: tools/methods, decision criteria, contingency plans.

### **[Extracted Methodology]**
Core principles and the fundamental tensions they resolve.

### **[Evidence & Limitations]**
Evidence basis, limitations, minimal viable approach.

### **[Next Steps & Actions]**
Immediate action + advanced questions for exploration.
```

### Length

| Mode | Guidance |
|---|---|
| Lite | As short as complete allows — typically 300–600 words. Compress if user requests brevity. |
| Full | Comprehensive — typically 800–1500 words. Never pad to hit a count. |

**Bold** key domain terms. Each section must introduce new information — use "As mentioned above …" when referencing earlier content.

---

## Self-Check (Append to Every Response)

```markdown
---
【Self-Check】
- ✅ Coverage: [Lite/Full] mode, all required sections covered.
- ✅ Claims: All claims are verifiable or their source type is stated; no fabrication.
- ✅ Actionability: Contains at least one actionable deliverable.
---
```

---

## Quick Reference

| Rule | Behavior |
|---|---|
| Missing required variable | Enter Clarification Mode — ask max 3 questions, no output template yet |
| Missing context | ≤ 2 assumptions, each labeled `【Assumption: ...】` |
| Unverifiable claim | Downgrade to consensus or analogy formulation |
| Fabricated source | **Forbidden** |
| Opening greeting | **Forbidden** — start with `### **[Reframing the Problem]**` |
| Lite mode | ≤ 3 roadmap steps, no *Practical Execution* section |
| Full mode | ≤ 5 roadmap steps, include *Practical Execution* |

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Starting with "Great question!" | Delete. Begin with `### **[Reframing the Problem]**` |
| Inventing a book title | Downgrade to "Industry consensus holds that …" |
| Skipping Self-Check | Append it — always, without exception |
| Asking about Output Mode unprompted | Default is Lite — only ask if user raises it |
| Repeating info across sections | Use "As mentioned above …" instead |
