---
name: frontend-evaluator
description: Use when browser-facing work already exists and the main need is an independent acceptance gate: re-check the experience in a browser, record evidence, and return `pass`, `fail`, or `blocked` without implementing fixes.
---

# Frontend Evaluator

Use this skill to judge shipped browser-facing work from a fresh evaluator stance.

The evaluator is not the builder. Treat generator claims, prior screenshots, and "works for me" statements as untrusted until re-verified.

## Boundary

Use this skill when:
- browser-facing work already exists and needs an independent acceptance decision
- the main question is whether the delivered experience satisfies the contract, not how to implement it
- the team needs defects, evidence, and retry guidance written clearly enough for another owner to act

Do not use this skill for:
- building or fixing the frontend
- builder-side browser QA during implementation — use `website-building`
- pre-implementation product or design review — use the relevant planning or review skill instead
- general repo implementation work with no browser acceptance gate

## Core Contract

- Re-run the evaluation from a fresh stance. Do not trust generator assertions, prior signoff, or screenshots without independent verification.
- Use the shared **Interactive Browser QA** methodology at `website-building/shared/12-playwright-interactive.md` as the canonical workflow. Follow it by reference; do not replace it with a shorter private checklist.
- Treat `docs/live/qa.md` as the canonical evidence artifact. The evaluation is not complete until that file tells the truth.
- Return exactly one verdict: `pass`, `fail`, or `blocked`.
- This skill judges and records evidence. It does not implement fixes.

## Verdict Rules

### `pass`
Use `pass` only when all of the following are true:
- the shared Interactive Browser QA workflow was completed in full
- every required user-visible claim was independently verified with evidence tied to the observed state where it matters
- `docs/live/qa.md` contains the required sections and enough detail for another person to audit the conclusion
- no unresolved functional, visual, accessibility, or viewport-fit defect remains within the evaluation scope
- main-flow accessibility basics were independently checked and recorded in `docs/live/qa.md`

### `fail`
Use `fail` for any product defect or evaluation-integrity defect.

Automatic `fail` conditions include:
- partial execution of the shared QA workflow
- unsupported claims in the final verdict or evidence artifact
- missing, ambiguous, or stale evidence records in `docs/live/qa.md`
- screenshots presented as proof without independent verification of the underlying behavior or state
- skipping exploratory coverage that the shared workflow requires
- discovering defects that violate the acceptance contract, even if the generator reported success
- visible clipping, weak contrast, broken layering, or missing key states dismissed as minor polish rather than classified and recorded as defects

### `blocked`
Use `blocked` only when environment or setup conditions prevent honest evaluation.

Examples:
- the app or preview cannot be started from the expected setup
- required credentials, fixtures, services, or network access are unavailable
- the browser automation environment itself is broken

`blocked` is not a soft failure. Do not use it for product bugs, partial workflow execution, or missing evidence. If evaluation could have happened and the record is weak or the product is wrong, the verdict is `fail`.

## Evidence Artifact

Write the evaluation to `docs/live/qa.md` in markdown.

At minimum, include these sections:
1. `## Evidence Matrix`
2. `## Defects by Severity`
3. `## Retry Contract`
4. `## Final Verdict`

Keep the artifact audit-friendly.

### Evidence Matrix
For each requirement, user-visible claim, or acceptance gate, record:
- what was checked
- how it was checked
- what evidence was captured
- whether it passed, failed, or could not be evaluated

### Defects by Severity
Group defects by severity so the next owner can triage accurately. Include the observable symptom, the reproduction path, and the evidence pointer.

### Retry Contract
State what the next owner must do before another evaluation is credible. Tie each retry instruction to the relevant defect or blocker. If the issue is environmental, say what external setup change is required.

### Final Verdict
End with exactly one of:
- `pass`
- `fail`
- `blocked`

Then give a brief justification grounded in the evidence matrix and defect list.

## Evaluation Workflow

1. Reconstruct the acceptance scope from the user request, planner contract, and delivered browser-facing behavior.
2. Read and apply the shared **Interactive Browser QA** methodology at `website-building/shared/12-playwright-interactive.md`.
3. Build explicit coverage for every requirement, visible claim, and critical flow that the final verdict will mention.
4. Execute the browser evaluation from a fresh evaluator posture using real interactions and observed states.
5. Record the evidence in `docs/live/qa.md` as the work happens. Do not defer the record until memory gets fuzzy.
6. Classify the outcome as `pass`, `fail`, or `blocked` using the rules above.
7. Stop after reporting the verdict, defects, and retry instructions. Do not implement fixes inside this skill.

## Failure Modes to Avoid

- turning generator confidence into evaluator evidence
- summarizing the shared QA methodology instead of actually running it
- calling the work `blocked` when the real result is a failed product or failed evaluation process
- treating screenshots alone as sufficient proof of correctness
- omitting retry guidance and forcing the next owner to reverse-engineer what to do
- letting the evaluator drift into implementation or design changes instead of holding the acceptance gate
