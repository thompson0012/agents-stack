# Evaluation and Iteration

Use structured evaluation when any of these are true:

- the skill's discovery wording matters
- the workflow is multi-step or easy to drift from
- you are replacing or upgrading an existing skill
- output quality is hard to judge from one happy-path prompt

## Portable Evaluation Principle

Keep the skill package clean and keep run artifacts elsewhere.

Recommended layout:

```text
skill-name/
├── SKILL.md
├── evals/
│   ├── evals.json
│   └── trigger-evals.json
└── ...

skill-name-evals/
└── iteration-1/
    ├── candidate/
    ├── baseline/
    ├── review.json
    └── benchmark.json
```

Do not ship generated run artifacts as part of the reusable skill package.

## 1. Task Evaluation

Use `evals/evals.json` for prompts that test whether the skill helps complete real work.

Minimum set:

1. direct match
2. ambiguous near miss
3. noisy or adversarial case

Rules:

- use realistic prompts, not toy requests
- keep each eval focused on one main behavior
- describe expected success in plain language
- include file inputs only when they matter to the workflow

## 1A. Temporal Guard Evaluation
Use temporal fixtures when the skill's correctness depends on a state transition, phase gate, or fail-closed decision rather than prompt wording alone.

Examples:
- a guard-like skill allows work only when required artifacts already exist
- a verifier rejects a retry when restore metadata or attempt budget is missing
- a workflow step must prove the exact before/action/after transition, not just the final text output

Guidance:
- capture the required before-state explicitly
- name the guard action or decision point being exercised
- record the expected after-state or routing outcome
- include at least one negative case that must fail closed
- keep these fixtures alongside prompt evals when discovery still matters, but do not let prompt-only evals stand in for temporal correctness

## 2. Baseline Comparison

Compare the same prompts against an honest baseline.

| Situation | Baseline |
| --- | --- |
| New skill | no skill or the default manual workflow |
| Existing skill revision | previous skill version |
| Competing phrasing change | current published description |

Store candidate and baseline outputs separately. If the candidate wins only because the prompts implicitly favor it, the eval set is biased.

## 3. Review Modes

### Objective review

Use when the output can be checked against explicit facts or structure.

Examples:
- required section exists
- produced file type is correct
- listed steps match the expected workflow
- validation command succeeds

### Subjective review

Use when quality depends on clarity, tone, usefulness, or design judgment.

Best practice:
- anonymize candidate and baseline as A and B
- review without revealing which is new
- review the raw artifacts directly; do not include provenance, version names, or a suggested winner in the prompt
- record a short reason for the winner

Use [review-template.md](../assets/review-template.md) to capture that judgment consistently.

## 4. Trigger Evaluation

Use `evals/trigger-evals.json` when the challenge is discovery, not execution.

Write a balanced set of realistic queries:

- should-trigger cases
- should-not-trigger near misses
- ambiguous cases where this skill competes with another

Avoid trivial negatives. A should-not-trigger case is valuable only if it might plausibly fool a naive description.

## 5. Revision Loop

After each round:

1. summarize what the candidate improved
2. identify what still failed or drifted
3. patch the smallest instruction, example, or resource that closes the gap
4. rerun the same eval set before changing the evals themselves

Only change the eval set when it is clearly weak, unrealistic, or non-discriminating.

## 6. Benchmark Notes

When timing, token cost, or human review burden matters, record aggregate comparison in `benchmark.json`.

Recommended measures:

- pass rate or win rate
- time spent
- token or compute cost if the runtime exposes it
- reviewer notes about failure patterns

Do not treat one metric as the whole story. A faster skill that quietly degrades quality is worse.

## 7. Description Optimization Without Overfitting

If discovery is weak:

- inspect failed should-trigger and false-trigger cases
- generalize from intent, not keywords
- keep the description distinctive but concise
- rerun both positive and negative trigger checks after each edit

Do not keep appending every missed phrase into the description. That produces brittle keyword bait instead of durable routing guidance.
