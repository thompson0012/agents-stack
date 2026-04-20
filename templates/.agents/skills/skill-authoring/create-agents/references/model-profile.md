# Model Profile

Agent manifests should name the preferred model, a fallback model, and a no-preference option.

## Required shape

```yaml
model_profile:
  preferred: gpt-5.4-mini
  fallback: gpt-4.1
  no_preference: allowed
```

## Rules

- Prefer the smallest model that can honestly do the job.
- Use the fallback when the preferred model is unavailable or a different balance is better.
- Keep `no_preference` explicit for model-agnostic agents or runtimes that pick the default.
- Do not bury model choice in body prose.
