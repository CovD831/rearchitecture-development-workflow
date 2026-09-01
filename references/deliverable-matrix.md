# Rearchitecture package deliverable matrix

Use this matrix to choose the smallest package that makes the next development
decision reviewable. A full package does not require every future module to have
an implementation-detail document.

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

| Stage | Artifact | Minimum content | When required |
|---|---|---|---|
| Intake | scope and authority note | current source hierarchy, baseline revision, in/out scope | always |
| Positioning | positioning/scope | user, problem, value hypotheses, non-goals, comparison roles | before Level-1 approval |
| Level 1 | target architecture | major subsystems, state owners, identities, dependency direction, deployment boundary | required and explicit for the in-scope target before implementation direction |
| Mapping | current-to-target map | retain/expose/adapt/split/deprecate/remove, hotspots, preserved paths | before migration tasks |
| Level 2 | module/boundary contracts | responsibilities, services, state, communication, failure and compatibility; mark claims established, conditional or open | when a boundary is stable; unresolved choices must name an experiment or decision gate |
| Level 3 | task contract | exact candidate API, data, auth, lifecycle, persistence, recovery and acceptance for the selected task | only immediately before or inside the implementation task, and only for consumed boundaries |
| Plan | migration/implementation plan | phases, PR boundaries, compatibility, abort/removal gates, rollback/restart | before coding across boundaries |
| Evidence | test/benchmark plan | fixtures, contract/failure tests, dependency evidence, performance baseline | before claiming improvement |
| Decision | ADR | one decision, alternatives, consequences, promotion status | when a material choice is approved |
| Experiment | protocol/result | bounded question, frozen controls/oracle, scoped result and limitations | only when tests/invariants cannot settle choice |
| Governance | catalog/maintenance rules | metadata, owners, status, links, promotion and supersession rules | when package has multiple documents |
| Handoff | task record | goal, acceptance, invariants, decisions, evidence, next owner and next step | when another person/agent continues |

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
