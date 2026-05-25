---
name: meta-methodology-extraction
description: Use when extracting the implicit methodology from a deep-dive conversation — reverse-engineering the analytical path and operational principles into a reusable Framework + Workflow + SOP. Triggers include "extract the methodology", "derive a framework from this conversation", "what method did we use here", "turn this into a repeatable process", "提煉出方法論". Do NOT use for summarizing content; this extracts the method, not the subject.
version: 0.2.0
---

# Meta-Methodology Extraction

Extract the implicit methodology from a deep-dive conversation. Output three files under `.agents-stack/methodology-extraction/<id>/`: `framework.md`, `workflow.md`, `sop.md`, `validation-report.md`.

**This is not a fill-in-the-blank template.** The methodology must be discovered from the conversation, not projected onto it. The steps below describe what to observe, not what to produce.

## What to Observe

When reading the source conversation, look for:

### 1. Layer Progression

How did the analysis move from start to finish? Identify the natural stages — do NOT force a predefined layer model. Common patterns include:

- Broad taxonomy → pick one problem → deep-dive mechanism → root cause → solutions → vision
- Phenomenon → symptom → cause → fix → production norms
- Current state → why broken → what's being done → what should be done → how to do it

**Key question**: If you had to teach someone to analyze a similar problem, what stages would you tell them to go through, in what order?

### 2. Principles

What operational rules governed the analysis? These are not domain facts ("LLMs are probabilistic") but analytical rules ("if a symptom can't be measured, it can't be diagnosed"). Look for:

- Heuristics the analyst applied (e.g., "always ask for evidence before accepting a claim")
- Boundary rules (e.g., "stop drilling when you hit a structural invariant")
- Quality criteria (e.g., "a symptom must be observable, not interpretive")

### 3. Cognitive Moves

What structural devices did the analysis use repeatedly?

- Comparisons (A vs B tables)
- Level separation (training layer / inference layer / engineering layer)
- Time horizons (now / 3-5 years / ultimate)
- Model mapping (applying known frameworks to new domains)
- Priority ordering (what to build first and why)

**Key question**: If you removed these devices, would the analysis still hold its structure?

---

## Extraction Process

### Step 1: Read for Path

Read the conversation end-to-end. Do not take notes. Just absorb the arc.

Then answer: **"This conversation moved from ____ to ____ to ____ to ____."** This is your analytical path — the backbone of the methodology.

### Step 2: Extract the Framework

From the path, derive:

- **Mental models**: The core ways of seeing that made the analysis possible. 3-5, each with a plain-language explanation and source in the conversation.
- **Taxonomies**: If the conversation created classification systems, extract them. Do NOT invent taxonomies that weren't in the conversation.
- **Principles**: The operational rules behind each stage of the path. Every principle must answer "why this stage matters."
- **Structural patterns**: The devices used to organize knowledge. Catalog them.

For every element: is it **universal** (would work on a different domain) or **domain-specific** (tied to the conversation's topic)?

### Step 3: Build the Workflow

Translate the path into executable steps. Each step needs:

- **What**: the action
- **Why**: the principle behind it (from Framework)
- **Input**: what must be available before starting
- **Output**: what must be produced before moving on

**The workflow must be executable by someone who never read the source conversation.**

### Step 4: Derive SOP

From the Workflow, extract operational norms:

- Rules: when to start, when to stop, when to redo a step
- Quality gates: objective completion criteria per step
- Metrics: how to tell if the process is healthy
- Anomaly responses: what to do when a step fails or stalls

### Step 5: Validate

Back-test everything against the source conversation:

- Coverage: does the Framework capture every significant pattern?
- Gaps: what was in the conversation but NOT in the extraction? Why?
- Over-extraction: are any one-time observations being mistaken for universal rules?
- Boundary: which parts are universal, which are domain-specific, which are provisional?

---

## Output Structure

```
.agents-stack/methodology-extraction/<id>/
├── framework.md              # Path, mental models, taxonomies, principles, structural patterns
├── workflow.md               # Executable steps: what, why, input, output
├── sop.md                    # Rules, quality gates, metrics, anomaly responses
└── validation-report.md      # Coverage, gaps, over-extraction flags, boundary statement
```

---

## Output Format (Consolidated Response)

After extraction is complete, report:

- **Depth verdict**: sufficient / insufficient
- **Analytical path**: "This conversation moved from ____ to ____ to ____ to ____."
- **Framework summary**: key mental models, principle count
- **Workflow summary**: step count
- **Validation**: coverage gaps, over-extraction flags, boundary classification

---

## Critical Rules

- Never force a predefined structure onto the conversation. The methodology must emerge.
- Never confuse domain content (what was discussed) with methodology (how it was discussed).
- Every extracted element must be traceable to the source conversation.
- The workflow must be standalone — executable without reading the source.
- If the conversation is too shallow to extract methodology, say so and stop. Do not fabricate.
