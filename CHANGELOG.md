# Changelog

## [0.31.2] - 2026-09-12

Applied findings from a promotion-closure run (R-004 on Cochpia). The gate was
recorded as 12/12 while two of its cases could no longer pass, and three
documents asserted states that had stopped being true.

### Added

- `references/doc-gates.md`: a **Claim drift** section. Documents rot through
  claims that carry an implicit "still true" — counts, file lists, "remains
  unchanged", "already implemented". Gives the falsification walk to run before
  a handoff, and the correction pattern: keep the history, add a dated banner
  and an explicit update section, never silently rewrite the old text.
- `references/review.md`: three adversarial questions — which claimed
  verifications the project's default regression actually executes; which other
  sites share the shape of a defect just fixed; whether a check makes itself
  pass by widening its own scope.
- `references/contracts.md`: **boundary vocabulary and legacy records**. Name
  both sides' terms for the same concept and the single place they are
  normalised; state explicitly whether pre-existing records stay readable under
  a compatibility default or are backfilled, because "hide the untagged" is
  indistinguishable from a data-loss change until it is too late.

### Changed

- `references/contracts.md`: added a `Vocabulary` row to the interface contract
  checklist, and a vocabulary-ownership bullet to the L2 artifact list.
- `SKILL.md`: two entries in **Do not**.

### Not added

- No new hard gate. "Evidence must be reproducible by someone else" was the
  natural blocker to add, but the checker cannot re-run a project's tests, so by
  this skill's own rule it stays a reviewer question rather than a mechanism.

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
