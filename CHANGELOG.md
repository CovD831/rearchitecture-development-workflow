# Changelog

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
