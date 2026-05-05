# Runtime Log: [FEATURE-###] [short title]

<!--
  Template: .agents/skills/using-agents-stack/references/templates/.harness/runtime.md
  Owner: generator-execution
  Copy into .harness/<WORKSTREAM-ID>/runtime.md at execution start.
  Append throughout execution. This is the canonical record of what happened.
  Delete this comment block before use.
-->

## Environment

- **Branch/commit**: [ref]
- **Runtime**: [node 22, python 3.12, etc.]
- **Key dependencies**: [versions if relevant]

## Build / Startup Triage

[Run the contract's triage command. Record output. If it fails, record build_failed and stop.]

```
$ [command]
[output]
```

**Triage result**: [PASS / FAIL]

## Execution Log

### [timestamp] — [checkpoint description]

[What was done, what files changed, what was verified.]

```
$ [verification command]
[output]
```

## Known Issues

- [issue]: [impact, mitigation, or acceptance]

## Resume Checkpoint

[If interrupted, the next execution worker starts here.]

- **Last verified step**: [description]
- **Next step**: [description]
- **Files in modified state**: [list]
