# Architecture levels and interface contracts

Load this reference when producing an L1, L2 or task-local L3 artifact, or when
reviewing an implementation-facing boundary.

## Level 1 — system target

L1 defines only system-level facts:

- major subsystems or coordination planes, when needed;
- state/data authorities and sole writers;
- identity families and ownership;
- dependency direction;
- application entrypoint and process/deployment boundary;
- controlled communication forms.

L1 is required for the in-scope target. It may omit future modules but may not
hide ambiguity in ownership, dependency direction or deployment. Record every
unresolved L1 question with an owner and decision gate.

Do not put method signatures, transactions or state machines in L1. A diagram
must distinguish ownership, construction order and interaction flow; do not use
one ambiguous arrow for all three.

## Level 2 — stable module/boundary contract

Create one L2 artifact per stable module or cross-module boundary. State:

- responsibility and non-responsibility;
- current classes/contracts inside the boundary;
- provided and required services;
- owned state and writable authority;
- allowed calls and visible data;
- lifecycle and failure containment;
- compatibility and migration notes;
- decisions deferred to implementation.

Mark significant claims as **established**, **conditional** or **open**. An open
claim must name the bounded experiment, evidence or implementation gate that
will resolve it. Later increments may promote a claim only after that evidence
is reviewed.

Use a small interaction vocabulary. Every cross-boundary interaction identifies
itself as a command, immutable query/view, typed transfer or receipt/evidence.
Do not introduce a generic bus to avoid naming the writer or authority.

## Level 3 — task-local implementation contract

Before coding a selected task, freeze the minimum contract consumed by that
task:

- candidate interfaces and bounded data shapes;
- authorization and scope;
- state transitions and idempotency;
- persistence/checkpoint and external-side-effect behavior;
- cancellation, failure and recovery;
- acceptance matrix and definition of done.

Detailed design normally lives inside the implementation task. A candidate may
be frozen immediately beforehand when its owner and adoption/revision rule are
explicit. It remains target intent until the implementation task adopts or
revises it. Never require L3 documents for modules the selected slice does not
consume.

## Interface contract checklist

| Contract field | Required question |
|---|---|
| Owner | Which module is the sole writer or authority? |
| Form | Command, query/view, transfer or receipt/evidence? |
| Input/output | What is the bounded request, view or receipt shape? |
| Authorization | Who may call it, under which scope or capability? |
| Identity | Which IDs remain distinct and how are they correlated? |
| Idempotency | What does exact replay or conflicting replay do? |
| Failure | Which owner reports and contains each failure? |
| Persistence | Which durable records, transactions or checkpoints change? |
| Recovery | What happens after restart or unknown external outcome? |
| Version | Which contract/config/durable versions must match? |
| Compatibility | What legacy path remains and when may it be removed? |
| Evidence | Which test or measurement proves the claim? |

