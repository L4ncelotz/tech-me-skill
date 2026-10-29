## Summary

<!-- Provide a brief overview of the motivation and goal of this pull request. -->

## Related Issue

<!-- Link the relevant issue(s) resolved or referenced by this PR (e.g., Closes #123, Fixes #456). -->

## Changes

<!-- Detail the changes introduced in this PR. -->
- 

## Cross-Agent Compatibility Impact

<!-- Explain any impact on different AI agents, models, or tool runtimes. Does this introduce new dependencies or vendor-specific assumptions? -->
- 

## Validation Checklist

Before submitting this PR, please ensure you have completed the following:

- [ ] Ran `python scripts/validate_repo.py` and passed all structural checks.
- [ ] Ran `python -m unittest discover -s tests -v` and all tests passed.
- [ ] Added or updated test scenarios in `evals/scenarios.json` if behavior was modified.
- [ ] Kept `skills/tech-me/SKILL.md` portable and concise; placed extended guides under `references/`.
- [ ] Did not introduce unnecessary frameworks, dependencies, or vendor-specific lock-in.
- [ ] Avoided including credentials, confidential project info, or proprietary data.
