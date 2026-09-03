# Changelog

## [0.31.1] - 2026-09-04

Applied findings from the first real-repository run (R005 on AutoResearch, the
first package produced by 0.31.0 and compared against a 0.30-era package).

### Added

- SKILL.md step 1 defines `repair` (reconcile existing records with evidence
  that already exists; never new design, code, or rewritten gate state) and a
  read-only rule for legacy packages (pre-0.31 `profile`/`gates` manifests:
  read, link, repair ledgers, never rewrite — drift is backlog).
- review.md names the self-attestation risk: a blocking finding closed only
  by amending package documentation prefers underlying code/test evidence, or
  `"resolution_review": "third-party"` surfaced at handoff.
- The closure-cycle decision (spent/not spent, why) is recorded in the
  increment record.
- Package location guidance: create packages where the project keeps
  rearchitecture records (e.g. `docs/rearchitecture/<package-id>/`).

### Changed

- `check_package.py` detects legacy-schema manifests and skips with an
  explicit message instead of failing with misleading current-schema errors.
- Consumer-anchor matching collapses whitespace, so an anchor may span a
  wrapped line (the R005 run hit this twice).

## [0.31.0] - 2026-09-03

Minimal-closed-loop refactor. The 0.30.x machinery grew one layer per observed
failure (process compliance → manifest and state machine; unconsumed review
findings → review rounds and dispatch provenance; complexity → profiles and
layers). This release keeps one mechanical anchor per root cause and deletes
the rest. The pristine 0.30.0 tree is preserved as the baseline git commit.

### Added

- One seven-step loop (baseline, frame, L1, map/contract, slice, review,
  handoff) replacing phases × layers × profiles.
- One size dial: `orientation`, `design`, `implementation`; promotion folded
  into `implementation`.
- `scripts/check_package.py`: single checker deriving gate state from
  existing artifacts and consumed findings — gate state is derived, never
  declared.
- `fixtures/example-package/`: a complete healthy design package used as a
  checker self-test and worked example.

### Changed

- Manifest reduced from ~25 fields to 10; `gates` object removed (derived by
  the checker).
- Review: one adversarial pass + one steelman per cycle, one closure cycle at
  most; consumption enforced through a single ledger with mechanically
  checked consumer anchors and evidence paths.
- References reduced from 18 to 6: `contracts`, `review`,
  `user-decision-gates`, `delivery`, `doc-gates`, `optional-concerns`.

### Removed

- Workflow state machine, review-round bookkeeping, dispatch receipts,
  host hooks and runtime provenance (independence is a protocol constraint:
  fresh-context reviewer sub-agent, frozen input, read-only reviewer).
- 11 of 13 scripts (~1,200 lines), including the phased validators and the
  Codex-specific hook integration.
- Stale resume fixtures that predated the manifest era.

### Fixed

- "does not close the gate" → gate-opening semantics stated once, correctly,
  in `references/review.md`.
- Consumption-ledger example now matches what the checker enforces (consumer
  anchor and evidence are mandatory).
