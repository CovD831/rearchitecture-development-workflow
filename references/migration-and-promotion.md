# Migration, experiments and promotion

Load this reference when the target architecture is entering an experiment,
implementation increment, compatibility migration or promotion decision.

## Migration stage evidence

For every stage specify:

- legacy and target fixtures for the same scenario;
- contract and failure tests;
- before/after dependency or registration evidence;
- state/data records, externally visible outcomes, versions and checkpoint
  equivalence where applicable;
- performance measurements against equivalent workloads and a named baseline;
- unsupported claims and limitations;
- compatibility layer, abort condition, removal gate and rollback/restart
  boundary.

A dependency-count decrease is supporting evidence, not proof of decoupling.
Compare public outcomes, durable facts, receipts, revisions and checkpoints when
those are part of the contract.

## Increment outcome and promotion

At the end of an increment choose exactly one outcome:

1. continue to the next planned slice;
2. run a named bounded experiment;
3. revise the target or contract;
4. stop and preserve the current path.

The next increment starts only when its recorded trigger and promotion evidence
are satisfied. A successful first slice proves only that slice; it does not
certify unimplemented modules or unresolved L2 claims.

Promote target text into current architecture only after implementation,
compatibility evidence and repository authority updates are merged together.
Keep the legacy path executable until its removal gate is satisfied.

## Experiments and ADRs

Use an experiment only for a bounded engineering choice that invariants,
contracts and a simpler reversible implementation cannot settle. Freeze the
question, hypotheses, baseline, controls, metrics, oracle and safety boundary
before execution.

Results are scoped evidence, not decisions. Record limitations, then use an ADR
and implementation evidence before promotion. Do not reserve experiment or ADR
identifiers for a speculative backlog.

