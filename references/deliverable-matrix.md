# Rearchitecture package deliverable matrix

Every multi-document package also requires a `.rearchitecture-package.json`
manifest. The manifest selects the package profile, maps artifact names to
files, records gate state and identifies the next task owner. Use
`references/package-completeness.md` as the schema and hard-stop policy.

Use this matrix to choose the smallest package and workflow layer that makes the
next development decision reviewable. Do not activate a later layer early. A
full package does not require every future module to have an implementation-
detail document.

Architecture rework is delivered incrementally. Every package or migration
increment records what this version delivers, what it explicitly defers, the
next advancement trigger, the evidence required for promotion, and the
stop/rollback rule. Later increments extend verified results; they do not imply
that the first package specifies the whole future system. This delivery-horizon
record is the canonical owner of deferral claims; other documents should link to
it and keep only the local summary needed for orientation.

Level labels are generic routing labels, not mandatory names: Level 1 is system
boundaries and dependency direction, Level 2 is stable module/boundary contracts,
and Level 3 is task-specific implementation detail. A project may use different
names if the same separation is explicit.

| Layer | Stage | Artifact | Minimum content | When required |
|---|---|---|---|
| 0/1 | Intake | scope and authority note | current source hierarchy, baseline revision, in/out scope | always for Layer 1+ |
| 0/1 | Package control | package manifest | profile, artifact map, gate state, next task/owner | always for a package |
| 1 | Positioning | positioning/scope | user, problem, value hypotheses, non-goals, comparison roles | before L1 approval |
| 1 | Level 1 | target architecture | major subsystems, state owners, identities, dependency direction, deployment boundary | before implementation direction |
| 1 | Mapping | current-to-target map | retain/expose/adapt/split/deprecate/remove, hotspots, preserved paths | before migration tasks |
| 1 | Level 2 | relevant boundary contracts | responsibilities, services, state, communication, failure and compatibility | only for consumed boundaries |
| 2 | Level 3 | task contract | exact API/data/auth/lifecycle/persistence/recovery/acceptance | only for selected implementation task |
| 2 | Plan/evidence | migration + fixtures + acceptance | compatibility, rollback, legacy/target and failure evidence | before coding across boundaries |
| 3 | Promotion evidence | compatibility and authority record | executable results, authority merge and removal gate | only after Layer 2 evidence |
| 1 | Decision/review | ADR + independent review + consumption ledger | decision, findings, steelman and consumed changes | before implementation-candidate outcome |
| 1/2 | Experiment | protocol/result | bounded question, frozen controls/oracle, scoped result and limitations | only when tests/invariants cannot settle choice |
| 0/1 | Governance | catalog/maintenance rules | metadata, owners, status, links, promotion and supersession rules | when package has multiple documents |
| 1/2/3 | Handoff | task record | goal, acceptance, invariants, decisions, evidence, next owner and next step | when another person/agent continues |
| optional | Trust | host provenance and external receipt | host event and receipt verification | only when explicitly required |

## Minimum package for a first vertical slice

For a real MVP implementation, the minimum useful set is:

1. approved Level-1 and the relevant Level-2 boundary;
2. current-to-target mapping for the selected call family;
3. task-local Level-3 contract;
4. acceptance/failure matrix with legacy and target fixtures;
5. migration/rollback note;
6. synchronized task handoff and verification commands.

Do not create Level-3 documents for modules that the selected slice does not
consume.

## Increment promotion record

For each version or migration slice, keep a short record containing:

1. deliverables completed in this increment;
2. explicit non-deliverables and unresolved L2 questions;
3. the next slice and its owner;
4. the advancement trigger and required evidence;
5. the stop, rollback or target-revision condition.

The record may live in the project's existing release, migration or task
document. It does not require a new document when an existing canonical owner
already covers the same claims. For a design-only package, record only the
delivered documents, explicit deferrals and next decision or implementation
trigger; add migration, rollback and operational evidence when those concerns
enter scope. Make the record discoverable from the orientation page,
documentation catalog or handoff entrypoint so a later session can resume each
active rearchitecture program without relying on conversation history.
