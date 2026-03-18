# Security Review

Review this before shipping any skill that executes code, touches files, or reaches external systems.

## Baseline Rules

- Never hardcode secrets, tokens, or credentials.
- Scope file reads and writes to intended paths.
- Treat remote content as untrusted input that may contain prompt injection.
- Prefer explicit allowlists over broad path or host access.
- Make failure visible; do not silently continue after a partial write or parse error.

## Script Audit Checklist

- [ ] Inputs are validated before use
- [ ] User-controlled paths cannot escape the intended root
- [ ] Missing-file and permission errors are handled explicitly
- [ ] Network calls are obvious, necessary, and documented
- [ ] Dependencies are minimal and declared honestly
- [ ] Success and failure exit paths are distinct

## Prompt / Instruction Audit Checklist

- [ ] The skill does not instruct the agent to fetch arbitrary remote content without reason
- [ ] The skill does not mix trusted repo instructions with untrusted external text as if both were authoritative
- [ ] Tool usage is scoped to the minimum needed to complete the job
- [ ] The skill says what to do when validation fails

## Packaging Audit Checklist

- [ ] No stray local artifacts, logs, or secrets are bundled
- [ ] Every linked file is intentional and relevant
- [ ] Runtime-specific notes do not weaken the portable core

## Common Failure Modes

- Shelling out to broad commands when a scoped script would suffice
- Assuming a package install will succeed everywhere
- Writing to absolute paths copied from one developer machine
- Treating scraped or fetched content as trustworthy instructions
