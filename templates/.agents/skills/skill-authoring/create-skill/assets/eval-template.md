# Skill Evaluation Scenario

## Scenario Name
- [Short label]

## Why This Scenario Exists
- [What discovery or execution behavior this tests]

## Prompt
```text
[prompt under test]
```

## Should The Skill Trigger?
- yes / no
- Why:

## Expected Behavior
- [What the agent should do if the skill triggers]
- [What the agent should avoid]

## Temporal Fixture Variant
- Use this section when the skill behaves like a guard or gate and correctness depends on state transitions rather than prompt wording alone.
- Phase or artifact gate:
- Before state:
- Guard action or decision point:
- Expected after state or routing outcome:
- Negative / fail-closed case:

## Observed Result
- Triggered:
- Outcome:
- Failure or drift:

## Fix Applied
- [Minimal change made to close the gap]

## Re-test Result
- pass / fail
- Notes:
