# Portability Checklist

Use this file when a skill must travel across different agent runtimes.

## Portable Core Principle

Assume the lowest common denominator first:

- local files may exist, but access may be restricted
- shell or code execution may be absent
- package installation may be blocked
- network access may be disabled or policy-gated
- sharing or packaging may differ by runtime

Design the core skill so it still makes sense if every optional capability disappears.

## Capability Matrix

Fill this out before adding runtime-specific instructions.

| Capability | Questions to answer |
| --- | --- |
| Filesystem | Can the agent read and write local files? Any directory restrictions? |
| Shell / code execution | Can it run Python, shell, or notebooks? |
| Network | Can it reach the public web, internal APIs, or nothing at all? |
| Package install | Are extra dependencies allowed, preinstalled only, or forbidden? |
| Archives / uploads | Does the runtime expect a folder, zip, inline text, or API object? |
| Sharing model | Is the skill personal, repo-scoped, workspace-scoped, or uploaded artifact-based? |
| Tool inventory | Which tools are guaranteed vs optional? |

## Recommended Defaults

- Prefer standard-library scripts.
- Use relative paths, not machine-specific absolute paths.
- Keep frontmatter minimal unless the target runtime requires more fields.
- Avoid hard-coding vendor brand names into the core instructions.
- Put runtime overlays into a dedicated section or reference note.

## Common Runtime Profiles

### Local CLI agent
- Usually has the richest file and shell access.
- Still avoid assuming global packages or privileged directories.

### Managed workspace agent
- Often has files and tools, but installs and network may be policy-gated.
- Keep dependencies explicit and optional.

### API-injected agent
- Commonly has the tightest constraints.
- Expect preinstalled dependencies only and limited or no network.

## Packaging Rule

Do not let packaging requirements define the skill's core structure. First build a coherent folder. Then document the outer packaging shape the target runtime needs.

## When to Add Runtime-Specific Metadata

Add extra metadata only when all of these are true:

- the target runtime requires it
- the field changes behavior or validation
- the field does not confuse other runtimes reading the same package

Otherwise, leave it out.
