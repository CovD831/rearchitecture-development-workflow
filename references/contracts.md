# Architecture levels and interface contracts

Load this reference when producing an L1, L2 or task-local L3 artifact, or
when reviewing an implementation-facing boundary. L1 means system boundaries,
L2 means stable module/boundary contracts, L3 means task-specific
implementation detail. Map a project's existing labels to these meanings
rather than introducing a second taxonomy.

## Level 1 — system target

L1 defines only system-level facts:

- major subsystems or coordination planes, when needed;
- state/data authorities and sole writers;
- identity families and ownership;
- dependency direction;
- application entrypoint and process/deployment boundary;
- controlled communication forms.

L1 is required and explicit for the in-scope target before implementation
direction. It may omit future modules but may not hide ambiguity in ownership,
dependency direction or deployment. Record every unresolved L1 question with
an owner and decision gate.

Do not put method signatures, transactions or state machines in L1. A diagram
must distinguish ownership, construction order and interaction flow; do not
use one ambiguous arrow for all three.

## Level 2 — stable module/boundary contract

Create one L2 artifact per stable module or cross-module boundary the package
consumes. State:

- responsibility and non-responsibility;
- current classes/contracts inside the boundary;
- provided and required services;
- owned state and writable authority;
- allowed calls and visible data;
- lifecycle and failure containment;
- compatibility and migration notes;
- vocabulary ownership: which side owns each status/enum term and where the
  two sides are normalised;
- decisions deferred to implementation.

Mark significant claims as **established**, **conditional** or **open**. An
open claim must name the bounded experiment, evidence or implementation gate
that will resolve it; do not invent precision for appearance.

Use a small interaction vocabulary. Every cross-boundary interaction
identifies itself as a command, immutable query/view, typed transfer or
receipt/evidence. Do not introduce a generic bus to avoid naming the writer or
authority.

## Boundary vocabulary and legacy records

Two boundary facts that review keeps rediscovering:

- **Vocabulary.** When each side owns its own terms for the same concept, the
  adapter must normalise at the boundary. Passing a value through because it
  "looks like a status" either throws inside the receiver or stores an
  out-of-domain value. Name both vocabularies in the L2 artifact and the single
  place they are translated; a receiver that validates its domain and throws is
  the good outcome, the silent store is the bad one.
- **Legacy records.** A new rule that treats missing metadata as
  "different, therefore hidden" deletes history. State the intended behaviour of
  pre-existing records explicitly, and say which of the two the package does:
  keep them readable under a compatibility default, or carry a backfill. Never
  leave it implicit, because "hide the untagged" is indistinguishable from a
  data-loss change until someone notices their own records are gone.

## Level 3 — task-local implementation contract

Freeze an L3 contract only when implementation is authorized and only for the
selected slice. Cover:

- candidate interfaces and bounded data shapes;
- authorization and scope;
- state transitions and idempotency;
- persistence/checkpoint and external-side-effect behavior;
- cancellation, failure and recovery;
- acceptance matrix and definition of done.

The candidate remains target intent until the implementation task adopts or
records revisions to it. Detailed design normally lives inside the
implementation task, not in the package.

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
| Vocabulary | Do both sides mean the same thing by each status or enum, and where is it normalised? |
| Evidence | Which test or measurement proves the claim? |
