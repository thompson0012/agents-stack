---
name: problem-definition
description: "Use when the user senses a problem but cannot define it cleanly, is solving symptoms without progress, keeps mixing solutions into the problem statement, or needs help turning a messy situation into one precise, actionable problem statement. Trigger on requests like 'something feels wrong', 'I am stuck', 'help me figure out the real problem', 'why is this not working', or any case where the problem is vague, overloaded, or possibly misframed. Do not use when the problem is already stated clearly and solution-neutrally in one or two sentences; route those cases to dynamic-problem-solving instead." 
---

# Problem Definition

Use this skill to turn an unclear situation into a single, solution-neutral problem statement that another skill can actually solve.

## Core Contract

- The output of this skill is **one clearly defined problem statement** plus a short handoff note.
- Do **not** solve the problem here.
- Do **not** recommend tactics, tools, or plans beyond what is needed to define the problem correctly.
- If the user already gave enough context, do not make them repeat it.
- If the problem is already clear, stop and route to `dynamic-problem-solving`.

## Entry Gate

Proceed only when at least one of these is true:

- the user can describe symptoms but not the real issue
- the user keeps proposing solutions instead of naming the problem
- the issue keeps recurring after attempted fixes
- several candidate problems are competing for attention
- the user says something feels off, stuck, confused, or overloaded

Route away immediately when the problem is already stated in one or two sentences and does not contain solution language.

## Workflow

### Phase 0 — Capture the Situation As Lived

Start from the user's raw experience before imposing structure.

Capture only what is needed:

- what they observe
- what they feel or fear
- what others are saying
- what has already been tried
- how long it has been happening

Separate:

- **observations** — directly seen, measured, heard
- **interpretations** — inferred causes, motives, or stories
- **attempted fixes** — actions already taken and why they failed

If the user gave a long description, compress it into a neutral restatement and ask only for the missing facts needed to continue.

### Phase 1 — Separate Symptom from Root Cause

Use a branching 5-Why drill.

Rules:

- Start from the visible symptom.
- Ask why repeatedly until the answer becomes something the user could act on.
- If more than one plausible cause appears, branch instead of forcing one chain.
- Stop when further "why" questions only produce speculation without evidence.

Run the symptom test on each candidate statement:

1. If this were solved, would the original discomfort disappear?
2. Could this be solved while something more fundamental remains wrong?
3. Does solving this require understanding **why**, or only acting on **what**?

Statements that fail this test remain symptoms, not final problems.

### Phase 2 — Reframe the Problem Five Ways

Generate alternate framings before choosing one.

Use these reframing moves:

1. **Flip the subject** — maybe the actor is wrong.
2. **Zoom out** — maybe the system creates the local issue.
3. **Zoom in** — maybe one component creates the system-wide complaint.
4. **Flip the assumption** — maybe the current goal is the wrong goal.
5. **Stakeholder swap** — maybe another party experiences a different problem than the user names.

For each frame, ask:

- Does this open a larger solution space?
- Does this require a more fundamental change?
- Which frame triggers the most emotional resistance?
- Which frame would a rational outsider choose?

Treat strong resistance as evidence worth inspecting, not a reason to avoid the frame.

### Phase 3 — Map Boundaries and Dependencies

Before finalizing the statement, define the problem's edges.

Map:

- **In scope**
- **Out of scope**
- **Real constraints** — law, physics, mathematics, hard budget, immovable deadlines
- **Perceived constraints** — habit, convention, fear, politics, untested assumptions
- **Dependency type**
  - standalone
  - upstream
  - downstream
  - circular

If the problem belongs upstream, say so plainly. Do not package a downstream symptom as the main problem.

### Phase 4 — Run the Stakeholder Reality Check

Different parties define the same situation differently.

For each high-impact stakeholder, note:

- their version of the problem
- the cause they would claim
- the solution they prefer
- why that framing serves their interests
- what they may be omitting

Then run a **mirror-imaging check**:

- Which parts of this definition come from direct evidence?
- Which parts come from projecting the user's own motives or values onto others?
- Remove any element that lacks observational support.

### Phase 5 — Synthesize the Final Problem Statement

Use this formula:

```text
[SUBJECT] cannot / does not [BEHAVIOR]
because [ROOT CAUSE],
which leads to [MEASURABLE CONSEQUENCE],
despite [ATTEMPTED APPROACH].
```

Quality bar:

- understandable by an outsider in 30 seconds
- names subject, behavior, cause, and consequence
- contains no disguised solution
- belongs to someone who can actually act on it
- narrow enough to solve, broad enough to be real

If the best possible statement is still vague, do not fake precision. Say the problem is not yet defined and name exactly what evidence is missing.

## Output Format

Return exactly these sections:

### Situation Summary
- 2-4 bullets of the situation as observed

### Candidate Problem Frames
- 3-5 short alternatives
- one sentence each

### Chosen Problem Statement
- one sentence only

### Why This Is the Real Problem
- 3-5 bullets linking the statement to root cause, not symptom

### Boundaries and Unknowns
- in scope
- out of scope
- unknowns that still matter

### Handoff
Use one of these:

- `Proceed to dynamic-problem-solving.`
- `Stop here. More evidence is needed before the problem can be defined.`
- `Stop here. This is not your problem to solve.`
Stop after `Handoff`. Do not append solution categories, diagnostic action plans, or likely fixes.

## Failure Modes to Avoid

- Treating urgency as clarity
- Treating a preferred solution as the problem
- Picking the least uncomfortable frame
- Accepting a stakeholder's framing without asking who benefits
- Confusing measurable consequence with root cause
- Producing a polished sentence that still hides the real issue
- Adding likely fixes after `Handoff` and calling it definition work

## Escalation Rules

- If the issue is emotionally loaded and the user is clearly defending a conclusion, run `thinking-ground` before continuing.
- If the issue is existential, relational, or too ambiguous to reduce safely, say that the framework boundary has been reached.
- If the user asks for solutions before the statement is stable, explain that solving the wrong problem well is still failure.
