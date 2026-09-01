# Contributing and beta feedback

This project is in public beta. The most useful contributions are observed
behavior from real repositories, especially cases where the Skill asks too many
questions, creates excessive documents, over-designs the target, misses an
existing authority or continues past an unmet gate.

## Report a test

Open an issue with:

- Skill version;
- repository language, approximate size and documentation maturity;
- the exact user request;
- whether the run was a fresh session or a resume;
- artifacts created or changed;
- decisions/questions asked of the user;
- what the Skill did well;
- unexpected behavior;
- whether the problem is document disorder, over-design, authority confusion,
  scope expansion, missed evidence, excessive ceremony or another category;
- the smallest correction you believe would help.

Remove credentials, customer data, proprietary source and local absolute paths
before sharing a report.

## Change policy

- Prefer fixes supported by a reproduced failure or real evaluation result.
- Do not turn one repository's terminology or architecture preference into a
  universal rule.
- Keep project-specific invariants in the consuming repository.
- Preserve the distinction between severity and review decision.
- Preserve the rule that a target document is not current runtime authority.
- Add detail to a reference rather than expanding `SKILL.md` when the guidance
  is conditional.
- Update [EVALUATION.md](EVALUATION.md) when a behavior claim gains or loses
  evidence.
- Add an entry to [CHANGELOG.md](CHANGELOG.md) for user-visible changes.

## Validate a contribution

```bash
python3 scripts/validate_package.py
git diff --check
```

For material workflow changes, also run at least one independent fresh-context
test. Give the evaluator the Skill, a realistic request and a safe isolated
repository, but do not provide the expected answer or suspected bug.

