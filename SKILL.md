---
name: rearchitecture-development-workflow
description: Build and review an evidence-driven software rearchitecture package before implementation, including current-state mapping, boundary contracts, staged migration, decision records, verification gates, document-coherence controls, and adversarial review. Use for architecture redesign, architecture refactoring, re-architecting, rearchitecture development packages, 架构重构, 重构架构, 架构重设计, or 重新设计架构; do not use for ordinary feature work, a single bug fix, or a code-only refactor.
---

# Rearchitecture Development Workflow

Use this skill to turn an architecture redesign into a development-ready package.
The output is not merely an architecture diagram: it is a bounded contract for
what will be built, how it will migrate, how it will be tested and what claims
remain unsupported. Treat rearchitecture as a continuing migration program:
each package is one reviewable delivery increment, not a promise to specify or
implement the whole future system.

## Operating principles

1. **Separate authority from intention.** Read the repository's current code,
   tests, architecture constitution/manifest and developer instructions first.
   Mark redesign documents as target, plan or evidence. Never let a target
   document silently become current behavior.
2. **Name existing things.** Every proposed module must map to current classes,
   contracts, registries, stores or entrypoints. Do not hide existing content
   behind invented nouns.
3. **Make ownership explicit.** For each boundary state what it owns, what it
   must not own, who writes durable facts, who authorizes mutations and who
   owns failure/recovery.
4. **Earn abstractions from real consumers.** A new abstraction, composition
   mechanism or extension host is admitted only when a real consumer removes a
   named dependency, unifies real registrations or makes cleanup/ownership
   enforceable. A generic abstraction normally needs two real consumers; a
   narrow safety boundary may be admitted for one.
5. **Start with a real vertical slice.** Keep one unchanged legacy fixture and
   add one target-boundary fixture for the same scenario. A synthetic provider
   graph can test mechanics but cannot prove the architecture.
6. **Freeze contracts before replacement.** Define interface form, inputs,
   outputs, authorization, idempotency, errors, persistence, recovery and
   compatibility before removing a concrete dependency.
7. **Treat performance as evidence, not justification.** Preserve authority,
   durable compatibility and recovery first; then measure overhead against the
   current path under equivalent workloads.
8. **Make the document set maintainable.** Give each kind of claim one canonical
   owner, keep current/target/history status visible, provide a short entrypoint
   and validate links/catalog metadata. Do not repeat a policy in many documents
   when a link and a local summary are sufficient.
9. **Plan for successive delivery.** Every package or migration increment states
   its in-scope deliverables, explicit deferrals, next advancement trigger and
   evidence needed to promote the next slice. Later work extends the migration
   from verified results; it does not silently expand the current package.

## Workflow

This workflow uses generic depth labels: Level 1 (L1) for system boundaries,
Level 2 (L2) for stable module/boundary contracts and Level 3 (L3) for
task-specific implementation detail. If the host project uses another naming
scheme, map the labels rather than introducing a second parallel taxonomy.

Right-size first: read the deliverable matrix and select the smallest package
appropriate to the change. The phases below describe the complete path; they are
not a mandatory checklist for every change.

Every package or migration increment must declare a delivery horizon. Use the
schema and design-only reduction in
[`references/deliverable-matrix.md`](references/deliverable-matrix.md); that
record is the canonical owner of deferrals and advancement conditions.

### Phase 0 — Resolve authority and baseline

- Read repository instructions, README, development guidance and architecture
  rules if they exist.
- Search the orientation page, documentation catalog and existing release,
  migration, task and handoff records before concluding that no earlier
  rearchitecture program exists.
- For each active rearchitecture program relevant to the requested scope,
  resume its state before defining new scope: read its latest delivery-horizon/
  increment record, review-ledger decisions and owner gates, unresolved
  deferrals, open L1/L2 claims, ADRs and recorded next task. Verify that the
  previous advancement trigger and promotion evidence are satisfied. If they
  are not satisfied, or a blocking item remains open, present that state and the
  available options to the user before starting new work. If the user explicitly
  authorizes proceeding anyway, record the exception, reason, approver and
  affected scope in the current increment record before proceeding.
- Identify the current source hierarchy and the exact baseline revision.
- Inspect current entrypoints, state/data owners, persistence contracts, tests,
  examples and extension registries when present.
- Record what is implemented, what is target intent and what is unknown.
- Build a reproducible dependency/registration inventory before proposing that
  coupling has been reduced. The minimum evidence is one re-runnable command
  or script, its checked-in output or report, and the same command reused for
  before/after comparison.

If the repository has a task ledger, issue system or handoff convention, follow
that project's format for ownership and acceptance. This workflow does not
require a particular collaboration tool or file layout. Do not use historical
conversation text as architecture authority.

### Phase 1 — Positioning, scope and complexity budget

Write down:

- what the framework/system is and who builds on it;
- the problem caused by current coupling or growth;
- the first-stage deployment boundary;
- non-goals and deferred capabilities, with the delivery horizon/increment
  record as the canonical owner of the detailed deferral list;
- bounded advantages and the primary comparison baseline for each claim.

At the same time, establish a complexity budget:

- list the existing concepts a reader must hold to understand the change;
- list every new noun, boundary, document and runtime mechanism proposed;
- state the concrete coupling, duplication or safety problem each new concept
  removes;
- record the smallest alternative that was considered and why it is insufficient;
- defer any concept that has no real consumer, owner or acceptance evidence.

Prefer claims such as “a topology change does not rewrite long-lived business
commitments” or “an extension cannot mutate domain outcomes” over “more modular”
or “more scalable.”

### User decision gates

Do not infer product intent from code or architecture diagrams. When repository
evidence cannot answer a question and the choice would materially change scope,
ownership, deployment, compatibility, safety, success criteria or migration
order, pause at the relevant decision gate and ask the user. Bundle related
questions into a small set of options with observed facts, trade-offs and a
recommended default. If a choice is not material and is safely reversible, make
the assumption explicit and record it instead of blocking progress. Use
[`references/user-decision-gates.md`](references/user-decision-gates.md) for the
stage-specific question set and where to record each answer.

This decision-gate rule applies to the corresponding gates throughout all
phases, not as a one-time Phase 1.5 questionnaire. If the user explicitly
delegates a material choice (for example, “you decide”), select the stated
recommended default or the best-supported reversible option, record the
delegation and assumptions in the owning artifact, and continue.

### Phase 2 — Level-1 target architecture

Define only system-level facts:

- major subsystems or coordination planes, when the domain needs them;
- state/data authorities and sole writers;
- identity families and ownership;
- dependency direction;
- application entrypoint and process/deployment boundary;
- controlled communication forms.

L1 is required for the in-scope target and must make these decisions explicit
before implementation direction is approved. It need not describe every future
module, but it may not leave ownership, dependency direction or deployment
scope ambiguous. Any unresolved L1 question must be named with an owner and a
decision gate rather than hidden as an omission.

Do not put method signatures, transactions or state machines in L1. Ensure the
diagram distinguishes ownership, construction order and interaction flow; do
not use one ambiguous arrow for all three.

### Phase 3 — Current-to-target mapping

For every current hotspot, classify the first action as retain, expose, adapt,
split, consolidate, deprecate or remove. Record the current owner, target owner,
preserved communication/persistence path and removal gate. Summarize important
deferred subsystems here only as needed to explain the mapping; keep the
delivery horizon/increment record as the canonical owner of the deferral list.

Do not create a new document merely because a topic is interesting. First find
the canonical document for that claim. Add a focused section or link when the
existing owner is still correct; create a new document only when ownership,
status, audience or lifecycle is materially different.

### Phase 4 — Level-2 module contracts

Create one L2 document per stable module or cross-module boundary. Each must
state:

- responsibility and non-responsibility;
- current classes and contracts inside the boundary;
- provided and required services;
- state and writable authority;
- allowed calls and data visibility;
- lifecycle and failure containment;
- compatibility and migration notes;
- decisions deferred to implementation.

L2 does not have to be fully settled in the first package. Mark each significant
claim as established, conditional or open. An open L2 choice must include the
bounded experiment, evidence or implementation gate that will resolve it; do not
invent precision merely to make the document look complete. A later migration
increment may promote an open L2 claim after its evidence is reviewed.

Use a small vocabulary for interfaces. A boundary must identify whether an
interaction is a command, immutable query/view, typed transfer or receipt/
evidence. Do not introduce a generic bus to avoid naming the owner or writer.

Keep the document set navigable:

- provide one short orientation page for the target, current increment and next
  action;
- give each document one purpose and one canonical claim owner;
- use local summaries only to explain why a reader should follow a link;
- maintain a reading route, status labels and last-reviewed metadata;
- validate relative links and the document catalog before publication.

### Phase 5 — MVP and task-local implementation contract

Choose the smallest real closed loop that exercises the intended boundary. A
read/lifecycle-closure slice may precede a first-write-boundary slice when write
responsibilities are not ready. If the project uses local MVP labels, preserve
them, but always pair each label with a descriptive name. State exactly what the
slice proves and what it explicitly does not prove.

Before coding a bounded implementation task, freeze the minimum L3 contract:

- concrete candidate interfaces and data shapes;
- authorization and scope;
- state transitions and idempotency;
- persistence/checkpoint and external-side-effect behavior;
- cancellation, failure and recovery;
- acceptance matrix and definition of done.

Detailed design normally lives in the implementation task. A bounded contract
pack may be prepared immediately before that task when its owner and
adoption/revision rule are explicit. It remains a candidate until the
implementation task adopts or revises it. The same rule applies if the host
project uses a different name than L3. L3 is never a requirement to specify all
modules in the first architecture package: write it only for the concrete task
and boundaries that the selected slice consumes.

### Phase 6 — Adversarial review and bidirectional steelman

Run two passes:

1. **Adversarial pass:** try to break the design using over-design, ambiguous
   ownership, duplicate writers, boundary leakage, unsafe cleanup, unknown
   external outcomes, incompatible versions, migration dead ends and unbounded
   performance claims.
2. **Steelman pass:** state the strongest case for the proposed architecture,
   including why each boundary is useful, what problem it removes and where the
   design is intentionally conservative.

Run the review at three points:

1. after the draft system/boundary package has a concrete vertical slice, before implementation
   approval;
2. after a material design change or experiment result;
3. before publishing or merging a change that alters an authority, contract,
   migration boundary or deployment claim.

Prefer an independent reviewer that did not write the design. If that is not
possible, use a fresh context, disclose the limitation in the ledger and do not
count self-review as independent evidence.

Produce one review ledger with one row per concern:

| Finding | Evidence | Severity | Decision | Consuming action | Owner/gate |
|---|---|---|---|---|---|
|  |  | blocking / non-blocking | accept / reject / defer | document, test, ADR, implementation or issue |  |

Consume the result immediately. Decision and severity have separate meanings:

- **accept** → change the relevant L1/L2/L3 contract, acceptance test or
  implementation task before the next gate;
- **reject** → record the evidence and rationale, without silently dropping it;
- **defer** → create a named future task/ADR with an owner and trigger;

Severity controls the gate independently:

- **blocking** → keep the implementation/publication gate closed until the
  underlying risk is resolved or the finding is explicitly reclassified as
  non-blocking, or accepted as a documented exception, by user confirmation
  or independent reviewer sign-off;
- **non-blocking** → keep the decision visible but do not reopen settled scope.

Rejecting a **blocking** finding does not open the gate by itself. It requires
explicit user confirmation or a signed decision from an independent reviewer;
until that confirmation exists, the implementation/publication gate remains
closed.

A blocking finding cannot be deferred while retaining blocking severity. Merely
recording a rationale or creating a future task/ADR does not close the gate.

The steelman pass is not a vote for the design. It checks whether the design's
strongest value and conservative boundaries are understood before findings are
accepted or rejected.

### Phase 7 — Migration, verification and promotion

Define staged migration with compatibility layers, abort conditions, removal
gates and rollback/restart boundaries. For every stage specify:

- legacy and target fixtures;
- contract and failure tests;
- before/after dependency or registration evidence;
- state/data records, externally visible outcomes, versions and checkpoint
  equivalence where applicable;
- performance measurements and comparison baselines;
- unsupported claims and limitations.

Promote target text into current architecture only after implementation,
compatibility tests and repository authority updates are merged together.

At the end of each migration increment, record one of four outcomes: continue
to the next planned slice, run a named experiment, revise the target/contract,
or stop and preserve the current path. The next increment starts only when its
trigger and promotion evidence are satisfied. A successful first slice proves
that slice; it does not certify unimplemented modules or unresolved L2 choices.

### Phase 8 — Handoff and publication

Before publishing the package:

- validate document metadata, links and catalog entries;
- run architecture conformance and relevant regression/static checks;
- review the complete diff for unrelated files or implementation claims;
- update the project's existing change or handoff record when one exists;
- make the current increment record discoverable from the orientation page,
  documentation catalog or handoff entrypoint;
- state the exact next implementation task and owner.

Do not create a PR or push a branch unless the user authorizes that external
mutation. When authorized, describe the package as documentation/target design
unless runtime behavior actually changed.

## Interface contract checklist

Every implementation-facing boundary answers these questions:

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

## Optional concern modules

Do not assume every architecture needs plugins, versioned providers, multiple
processes, hot reload or dynamic replacement. Activate a concern only when the
requirements and failure model demand it.

If plugin or extension composition is in scope, define multiplicity, ownership,
cleanup, version compatibility, update/removal and isolation boundaries. If it is
not in scope, say so explicitly and keep the core workflow unchanged.

If an optional extension/version concern is activated, do not promise live
replacement, conflicting implementations, or crash/security isolation without
an explicit process and recovery design. Removal must preserve durable domain
facts and must not infer completion or retry an unknown external effect.

If the host is Python and the design requires conflicting versions of a
top-level package in one interpreter or unloading imported code, make the
process boundary and restart/recovery behavior explicit; do not assume that
module reload provides isolation or safe version coexistence.

## Document coherence and over-design gates

Before accepting the package, check both dimensions explicitly.

### Document coherence

- Can a new reader find the target architecture, current increment and next
  action from one entrypoint?
- Does every major claim have one canonical owner?
- Are current behavior, target intent, plans and frozen evidence visibly
  distinguished?
- Are summaries shorter than their canonical sources and linked rather than
  copied?
- Are document status, owner, review date, supersession and inbound links
  consistent?
- Can the package be read in a short orientation path and a deeper review path?

### Over-design resistance

- Does every new abstraction have a named real consumer or safety requirement?
- Does it remove a concrete dependency/registration path or make an invariant
  enforceable?
- Is its owner and non-responsibility explicit?
- Is there a smaller reversible alternative?
- Are future features clearly deferred rather than represented as empty modules?
- Can the MVP be implemented and falsified without building the whole platform?

If either review fails, simplify or split the package before adding more detail.
If the complexity budget is exceeded, a blocking finding cannot be closed, or no
safe smaller alternative is available, stop and present the user with the
remaining options and trade-offs. Do not silently expand or shrink the scope.

## Experiments and ADRs

Use an experiment only for a bounded engineering choice that current invariants,
contracts and a simpler reversible implementation cannot settle. Freeze the
question, hypotheses, baseline, controls, metrics, oracle and safety boundary
before running it. Results are scoped evidence; an ADR and implementation are
required before promotion. Do not reserve experiment or ADR identifiers for a
speculative backlog.

## Deliverable routing

For any change, first use the artifact matrix in
[`references/deliverable-matrix.md`](references/deliverable-matrix.md) to select
the smallest package; the full workflow is not mandatory for a small change.
For the review pass, use
[`references/adversarial-review.md`](references/adversarial-review.md).
For user-direction questions and delegated decisions, use
[`references/user-decision-gates.md`](references/user-decision-gates.md).
Load those references only when producing the corresponding package or review.

## Do not do

- Do not rewrite the whole codebase before proving one real slice.
- Do not turn every file/class into a plugin; only apply plugin/version guidance
  when that concern is actually in scope.
- Do not create duplicate state owners, schedulers, stores, buses or lifecycle
  authorities without an explicit target decision and failure model.
- Do not hide mixed responsibilities behind a renamed pass-through wrapper.
- Do not claim decoupling from a lower dependency count alone.
- Do not use a synthetic demo as the primary MVP exit condition.
- Do not let extension cleanup imply domain completion or destruction of domain
  entities.
- Do not treat task notes, benchmark scores or generated prose as current
  architecture authority.
