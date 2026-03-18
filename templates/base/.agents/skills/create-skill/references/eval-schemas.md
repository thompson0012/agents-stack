# Evaluation Schemas

These structures are intentionally portable. They describe the data you capture during evaluation without assuming one specific runtime or benchmark harness.

## `evals/evals.json`

Task-level eval prompts for candidate vs baseline comparison.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": "direct-match",
      "prompt": "Realistic user request",
      "expected_output": "What success looks like",
      "files": [],
      "notes": "Optional setup or review note"
    }
  ]
}
```

### Fields
- `skill_name`: must match the skill frontmatter name
- `evals[].id`: stable identifier, unique within the file
- `evals[].prompt`: realistic user prompt
- `evals[].expected_output`: short success description
- `evals[].files`: optional input file paths or references
- `evals[].notes`: optional reviewer note

## `evals/trigger-evals.json`

Discovery checks for whether the skill should trigger.

```json
[
  {
    "id": "should-trigger-1",
    "query": "Realistic user query",
    "should_trigger": true,
    "why": "Why the skill should or should not trigger"
  }
]
```

### Fields
- `id`: stable identifier, unique within the file
- `query`: realistic user query
- `should_trigger`: expected routing outcome
- `why`: optional rationale for reviewers

## `review.json`

Human or agent review notes comparing candidate and baseline.

```json
{
  "eval_id": "direct-match",
  "winner": "candidate",
  "decision_type": "blind",
  "summary": "Candidate was clearer and more complete.",
  "findings": [
    {
      "label": "clarity",
      "winner": "candidate",
      "evidence": "Used a tighter checklist and fewer ambiguous steps."
    }
  ]
}
```

### Fields
- `eval_id`: links the review back to the task eval
- `winner`: `candidate`, `baseline`, or `tie`
- `decision_type`: `objective`, `subjective`, or `blind`
- `summary`: short explanation of the outcome
- `findings[]`: optional criterion-level notes

## `benchmark.json`

Aggregate summary for one evaluation round.

```json
{
  "skill_name": "example-skill",
  "iteration": 1,
  "summary": {
    "candidate_pass_rate": 0.67,
    "baseline_pass_rate": 0.33,
    "winner": "candidate"
  },
  "metrics": {
    "candidate_time_seconds": 42.5,
    "baseline_time_seconds": 51.2,
    "candidate_tokens": 3800,
    "baseline_tokens": 4200
  },
  "notes": [
    "Candidate improved clarity but still missed one near-miss case."
  ]
}
```

### Fields
- `skill_name`: skill being evaluated
- `iteration`: evaluation round number
- `summary`: top-line result
- `metrics`: optional time or cost comparison
- `notes`: qualitative observations that numbers alone miss

## Schema Rules of Thumb

- Prefer explicit names over positional meaning.
- Keep identifiers stable across iterations.
- Store generated outputs outside the skill package; schemas describe the records, not where every runtime must save them.
- Add fields only when they change a review decision, not because more telemetry feels impressive.
