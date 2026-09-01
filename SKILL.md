---
name: rearchitecture-development-workflow
description: Build and review an evidence-driven software rearchitecture package before implementation, including current-state mapping, boundary contracts, staged migration, decision records, verification gates, document-coherence controls, and adversarial review. Use for architecture redesign, architecture refactoring, re-architecting, rearchitecture development packages, 架构重构, 重构架构, 架构重设计, or 重新设计架构; do not use for ordinary feature work, a single bug fix, or a code-only refactor.
---

# Rearchitecture Development Workflow

Use this skill to turn an architecture redesign into a development-ready package.
The output is not merely a diagram: it is a bounded contract for what will be
built, how it will migrate, how it will be tested and what remains unsupported.
Treat rearchitecture as a continuing migration program. Each package is one
reviewable delivery increment, not a promise to specify or implement the whole
future system.

## Operating principles

1. **Separate authority from intention.** Read current code, tests, architecture
   authority and repository instructions first. Mark redesign documents as
   target, plan or evidence; never present them as current behavior.
2. **Name existing things.** Map every proposed module to current classes,
   contracts, registries, stores or entrypoints. Do not hide existing content
   behind invented nouns.
3. **Make ownership explicit.** State what each boundary owns and must not own,
   who writes durable facts, who authorizes mutations and who owns recovery.
4. **Earn abstractions from real consumers.** Admit a new abstraction only when
   a real consumer removes a named dependency, unifies real registration or
   makes an invariant enforceable. A generic abstraction normally needs two
   consumers; a narrow safety boundary may be admitted for one.
5. **Start with a real vertical slice.** Preserve one legacy fixture and add one
   target-boundary fixture for the same scenario. A synthetic graph can test
   mechanics but cannot prove the architecture.
6. **Freeze contracts before replacement.** Define inputs, outputs,
   authorization, identity, idempotency, failure, persistence, recovery and
   compatibility before removing a concrete dependency.
7. **Treat performance as evidence, not justification.** Preserve authority,
   durable compatibility and recovery first; then measure equivalent workloads
   against the current path.
8. **Keep documents maintainable.** Give each claim one canonical owner, keep
   current/target/history status visible and link to policy instead of copying
   it across documents.
9. **Plan for successive delivery.** Every increment states deliverables,
   deferrals, its next advancement trigger and required promotion evidence.

## Workflow and module loading

Level 1 (L1) means system boundaries, Level 2 (L2) means stable module/boundary
contracts and Level 3 (L3) means task-specific implementation detail. Map a
project's existing labels to these meanings rather than introducing a second
taxonomy.

Right-size first. Read
[`references/deliverable-matrix.md`](references/deliverable-matrix.md) and select
the smallest package that makes the next decision reviewable. The phases below
are the complete path, not a mandatory checklist for every request. Load the
other references only when their corresponding phase or concern is active.

Every package or migration increment must declare a delivery horizon. The
deliverable matrix owns the schema, design-only reduction, deferrals and
advancement conditions.

### Phase 0 — Resolve authority and baseline

- Read repository instructions, README, development guidance and architecture
  authority if they exist.
- Search orientation, documentation, release, migration, task and handoff
  records before concluding that no earlier rearchitecture program exists.
- For each active program relevant to the request, read its latest increment
  record, review decisions, unresolved deferrals, open L1/L2 claims, ADRs and
  recorded next task before defining new scope.
- Verify the previous advancement trigger and promotion evidence. If either is
  unmet, or a blocking finding remains open, present the state and options to
  the user before continuing. If the user authorizes an exception, record the
  reason, approver and affected scope in the current increment record.
- Identify the source hierarchy and exact baseline revision. Inspect current
  entrypoints, state/data owners, persistence, tests, examples and extension
  registries when present.
- Record what is implemented, what is target intent and what is unknown.
- Before claiming reduced coupling, create a reproducible dependency or
  registration inventory: one rerunnable command/script, checked-in output or
  report, and the same method reused for before/after comparison.

Follow the repository's existing task ledger, issue system and handoff format.
Do not require a particular collaboration tool, and do not use conversation
history as architecture authority.

### Phase 1 — Positioning and scope

Record:

- what the system is and who builds on it;
- the problem caused by current coupling or growth;
- the first-stage deployment boundary;
- non-goals and deferred capabilities;
- bounded advantages and the comparison baseline for each claim.

At the same time, establish a complexity budget. Load
[`references/document-and-complexity-gates.md`](references/document-and-complexity-gates.md)
for the budget, document ownership rules and stopping conditions. Prefer bounded
claims over words such as “more modular” or “more scalable.”

### User decision gates

Do not infer product intent from code or diagrams. When repository evidence
cannot answer a material question about scope, ownership, deployment,
compatibility, safety, success criteria or migration order, pause and ask the
user. Bundle related choices, show observed facts and trade-offs, and recommend
a conservative default when justified.

Use [`references/user-decision-gates.md`](references/user-decision-gates.md) for
the stage-specific questions and durable recording locations. If the user
explicitly delegates a material choice, select the recommended or best-supported
reversible option, record the delegation and assumptions, and continue. Make
non-material reversible assumptions explicit instead of blocking progress.

### Phase 2 — Level-1 target architecture

Define major subsystems or coordination planes, state/data authorities and sole
writers, identity ownership, dependency direction, application entrypoint,
process/deployment boundary and controlled communication forms.

L1 is required and explicit for the in-scope target before implementation
direction. It need not describe every future module, but it may not leave
ownership, dependency direction or deployment scope ambiguous. Name unresolved
L1 questions with an owner and decision gate.

Load [`references/architecture-contracts.md`](references/architecture-contracts.md)
for L1 diagram rules and the L2/L3/interface schemas used in later phases.

### Phase 3 — Current-to-target mapping

For every current hotspot, classify the first action as retain, expose, adapt,
split, consolidate, deprecate or remove. Record current owner, target owner,
preserved communication/persistence path and removal gate. Keep the delivery
horizon as the canonical owner of detailed deferrals.

Do not create a document merely because a topic is interesting. Find the
canonical owner first; create a new document only when ownership, status,
audience or lifecycle is materially different.

### Phase 4 — Level-2 module contracts

Create one L2 contract per stable module or cross-module boundary. Cover
responsibility and non-responsibility, current components, provided/required
services, writable authority, allowed calls/data visibility, lifecycle/failure,
compatibility and decisions deferred to implementation.

L2 may remain incomplete in the first package. Mark significant claims as
established, conditional or open. Every open choice needs a bounded experiment,
evidence threshold or implementation gate that can resolve it; do not invent
precision for appearance.

Use the L2 and interaction-form rules in
[`references/architecture-contracts.md`](references/architecture-contracts.md).
Use the navigation and canonical-owner checks in
[`references/document-and-complexity-gates.md`](references/document-and-complexity-gates.md)
when the package contains multiple documents.

### Phase 5 — MVP and task-local contract

Choose the smallest real closed loop that exercises the intended boundary. A
read/lifecycle-closure slice may precede a first-write-boundary slice. Preserve
local MVP labels only when paired with a descriptive name, and state exactly
what the slice proves and does not prove.

Before coding a bounded implementation task, freeze only the L3 contract
consumed by that task. It remains a candidate until the implementation task
adopts or records revisions to it. Do not create L3 documents for unselected
modules. Use the L3 and interface checklist in
[`references/architecture-contracts.md`](references/architecture-contracts.md).

### Phase 6 — Adversarial review and bidirectional steelman

Run an adversarial pass that tries to break ownership, recovery, compatibility,
migration and evidence claims, followed by a steelman that states the strongest
value and deliberately conservative boundaries. Prefer an independent reviewer
who did not write the package; otherwise use a fresh context and disclose the
limitation.

Use [`references/adversarial-review.md`](references/adversarial-review.md) for
review timing, questions and the single reconciliation ledger. Consume every
finding immediately. A blocking finding keeps the gate closed until the risk is
resolved or explicitly downgraded/accepted as an exception by the user or an
independent reviewer; rejecting or deferring it alone does not open the gate.

### Phase 7 — Migration, verification and promotion

Define staged migration with compatibility layers, abort conditions, removal
gates, rollback/restart boundaries, legacy/target fixtures and equivalent
evidence. Promote target text into current architecture only after the
implementation, compatibility evidence and repository authority updates merge
together.

At each increment end, choose one outcome: continue, run a named experiment,
revise the target/contract, or stop and preserve the current path. The next
increment starts only when its trigger and promotion evidence are satisfied.
Load [`references/migration-and-promotion.md`](references/migration-and-promotion.md)
for detailed evidence, experiments and ADR rules.

### Phase 8 — Handoff and publication

Before publication:

- validate metadata, links, catalogs and relevant conformance/regression checks;
- inspect the full diff for unrelated files or unsupported implementation claims;
- update the project's existing change/handoff record;
- make the increment record discoverable from an orientation or catalog entry;
- state the exact next task and owner.

Do not create a PR or push a branch unless the user authorizes that external
mutation. When authorized, describe the package as target design/documentation
unless runtime behavior actually changed.

## Optional concerns

Plugins, version coexistence, process isolation, hot replacement and dynamic
unloading are not default architecture requirements. Load
[`references/optional-concerns.md`](references/optional-concerns.md) only when
the requested design actually activates one of those concerns.

## Module routing

| Need | Load |
|---|---|
| Select the smallest artifact set and delivery horizon | [`deliverable-matrix.md`](references/deliverable-matrix.md) |
| Ask for or record a material user decision | [`user-decision-gates.md`](references/user-decision-gates.md) |
| Define L1/L2/L3 or an implementation-facing interface | [`architecture-contracts.md`](references/architecture-contracts.md) |
| Control document growth, complexity or over-design | [`document-and-complexity-gates.md`](references/document-and-complexity-gates.md) |
| Run adversarial review and steelman | [`adversarial-review.md`](references/adversarial-review.md) |
| Plan migration, experiments, ADRs or promotion | [`migration-and-promotion.md`](references/migration-and-promotion.md) |
| Design plugins, isolation or version coexistence | [`optional-concerns.md`](references/optional-concerns.md) |

Do not load every module by default. The active phase and requested deliverable
determine which references are needed.

## Do not do

- Do not rewrite the whole codebase before proving one real slice.
- Do not turn every file/class into a plugin.
- Do not create duplicate state owners, schedulers, stores, buses or lifecycle
  authorities without an explicit target decision and failure model.
- Do not hide mixed responsibilities behind a renamed pass-through wrapper.
- Do not claim decoupling from a lower dependency count alone.
- Do not use a synthetic demo as the primary MVP exit condition.
- Do not let extension cleanup imply domain completion or destruction.
- Do not treat task notes, benchmark scores or generated prose as current
  architecture authority.
