# Changelog

All notable changes to this Skill are recorded here.

## [0.9.2] - 2026-09-02

### Changed

- Clarified resume fixture output as fixture-integrity validation, not Skill
  behavior validation.
- Extended portability checks to cover checked-in resume fixtures.
- Added an explicit beta test for on-demand L2 reference loading.

## [0.9.1] - 2026-09-01

### Changed

- Reduced `SKILL.md` from 429 to 246 lines while preserving one external Skill
  entrypoint and the existing workflow semantics.
- Added explicit on-demand routing for architecture contracts, document and
  complexity gates, migration/promotion and optional extension concerns.
- Moved detailed L1/L2/L3 schemas and the interface checklist into
  `references/architecture-contracts.md`.
- Moved document coherence and over-design checks into
  `references/document-and-complexity-gates.md`.
- Moved migration evidence, experiments and ADR promotion rules into
  `references/migration-and-promotion.md`.
- Moved plugin, version coexistence and Python isolation guidance into
  `references/optional-concerns.md`.

### Compatibility

- Skill name, triggers, authorization boundaries, artifact meanings and
  resume/review gate behavior remain unchanged.

## [0.9.0] - 2026-09-01

### Added

- Evidence-driven architecture intake, current-to-target mapping and staged
  migration workflow.
- Explicit Level-1, evidence-bounded Level-2 and task-local Level-3 delivery
  rules.
- Delivery-horizon records for successive increments and cross-session resume.
- User decision gates, including delegated-choice and documented-exception
  behavior.
- Adversarial review and bidirectional-steelman ledger with closed blocking-gate
  semantics.
- Document-coherence and over-design gates.
- Healthy and blocked resume regression fixtures.
- Public-beta packaging, validation, evaluation and contribution guidance.
- MIT License for personal, team and public reuse.

### Validation

- Package structure and reference validation passed.
- Independent cold-start and real-repository design-package evaluation passed.
- Runtime implementation behavior remains outside the evidence claimed by this
  release.
