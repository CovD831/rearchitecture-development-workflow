# Delivery horizon, migration evidence, and promotion

Load this reference at step 2 (framing), before implementation, and at each
increment end. It owns the delivery-horizon schema, the per-size artifact
minimums, and migration/promotion evidence rules.

## Artifact minimums by loop step

| Loop step | Artifact | Minimum content |
|---|---|---|
| 1 Baseline | scope note | source hierarchy, baseline revision, in/out scope |
| 2 Frame | positioning + delivery horizon | user, problem, non-goals, deliver/defer split, advancement trigger and evidence, stop rule |
| 3 L1 | target architecture | subsystems, state owners, identities, dependency direction, deployment boundary |
| 4 Map | current-to-target map | retain/expose/adapt/split/consolidate/deprecate/remove per hotspot, owners, preserved paths |
| 4 L2 | boundary contracts | responsibilities, services, state, failure, compatibility; claims marked established/conditional/open |
| 5 L3 | task contract | exact API/data/auth/lifecycle/persistence/recovery/acceptance for the selected slice |
| 5 Evidence | fixtures + acceptance | one legacy and one target fixture per scenario, contract/failure tests, dependency inventory |
| 6 Review | report + ledger | per `references/review.md` |
| 7 Handoff | increment record | outcome, next task and owner, trigger, evidence links |

The delivery horizon in the increment record is the canonical owner of
deferrals and advancement conditions; other documents link to it and keep
only a local summary.

## Minimum package for a first vertical slice

1. approved L1 and the consumed L2 boundary;
2. current-to-target mapping for the selected call family;
3. task-local L3 contract;
4. acceptance/failure matrix with legacy and target fixtures;
5. migration/rollback note;
6. synchronized handoff and verification commands.

## Migration evidence

For every implementation stage specify:

- legacy and target fixtures for the same scenario, plus contract and failure
  tests;
- before/after dependency or registration evidence, produced by one
  rerunnable command reused for both measurements;
- state records, externally visible outcomes and checkpoint equivalence where
  applicable;
- performance measured against equivalent workloads and a named baseline;
- the compatibility layer, abort condition, removal gate and
  rollback/restart boundary;
- explicitly unsupported claims and limitations.

A dependency-count decrease is supporting evidence, never proof of
decoupling by itself.

## Increment end and promotion

At each increment end choose exactly one outcome: continue to the next
planned slice, run a named bounded experiment, revise the target or contract,
or stop and preserve the current path. A successful slice proves only that
slice.

Promote target text into current architecture only after implementation,
compatibility evidence and the repository authority update merge together.
Keep the legacy path executable until its removal gate is satisfied.

Use an experiment only for a bounded choice that contracts and a simpler
reversible implementation cannot settle; freeze question, baseline, controls
and oracle before executing. Experiment results are scoped evidence, not
decisions — promote through an ADR plus implementation evidence. Record one
ADR per material approved choice: decision, alternatives, consequences,
status.
