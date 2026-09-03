---
name: rearchitecture-development-workflow
description: Build and review an evidence-driven software rearchitecture package before implementation, including current-state mapping, boundary contracts, staged migration, decision records, verification gates, document-coherence controls, and adversarial review. Use for architecture redesign, architecture refactoring, re-architecting, rearchitecture development packages, 架构重构, 重构架构, 架构重设计, or 重新设计架构; do not use for ordinary feature work, a single bug fix, or a code-only refactor.
---

# Rearchitecture Development Workflow

Turn an architecture redesign into a development-ready package: a bounded
contract for what will be built, how it will migrate, how it will be verified
and what remains unsupported. Treat rearchitecture as a continuing migration
program. Each package is one reviewable increment, never a promise to specify
the whole future system.

## The loop

One workflow, seven steps. Pick a package size (table below) and run the loop
only as far as that size requires. Every step writes files in a package
directory; chat prose is not the record.

1. **Baseline.** Read repository instructions and architecture authority.
   Search for an earlier rearchitecture program; if one exists, read its
   manifest and latest increment record before defining new scope. If the
   recorded advancement trigger is unmet or a blocking finding is open,
   present the state and options to the user instead of starting the next
   increment. Record the exact baseline revision and what is implemented,
   target intent, or unknown.
2. **Frame.** Record the user and the problem caused by current coupling, the
   first deployment boundary, non-goals, and a delivery horizon: what this
   increment delivers, what it explicitly defers, and the trigger and
   evidence required to advance. Load
   [`references/delivery.md`](references/delivery.md).
3. **L1 target.** Define major subsystems, state/data authorities and sole
   writers, identity ownership, dependency direction, entrypoint and
   deployment boundary. Resolve every open L1 question or name it with an
   owner and a decision gate. Load
   [`references/contracts.md`](references/contracts.md).
4. **Map and contract.** For each current hotspot classify retain / expose /
   adapt / split / consolidate / deprecate / remove, with current owner,
   target owner and removal gate. Create one L2 contract per stable boundary
   the package actually consumes; mark claims established, conditional or
   open. Do not create L2 or L3 material for modules the slice does not
   consume.
5. **Slice.** Choose the smallest real vertical slice — one legacy fixture
   plus one target fixture for the same scenario — and state exactly what it
   proves. Freeze a task-local L3 contract only when implementation is
   authorized and only for the interfaces the slice consumes.
6. **Review.** Dispatch one independent reviewer sub-agent for one
   adversarial pass plus one steelman in the same cycle. Persist the report
   and consume every finding into the ledger. Load
   [`references/review.md`](references/review.md).
7. **Hand off.** Run `scripts/check_package.py <package-dir>` and fix every
   reported failure. Record the outcome (continue / run a named experiment /
   revise the target / stop and preserve), the exact next task and owner, and
   make the increment record discoverable from the project's orientation or
   catalog page. Never push or open a PR without explicit user authorization.

## Package sizes

| Size | Runs the loop through | Checker requires |
|---|---|---|
| `orientation` | step 2 | scope, next task, trigger |
| `design` | step 6 | scope, positioning, L1, mapping, L2, ADR, handoff, consumed review |
| `implementation` | steps 5–7 | design set plus L3, fixtures, acceptance, rollback |

A `design` package ends in a recommendation — implementation-candidate,
experiment, revise, or blocked — never in implementation authorization.
Promotion is not a separate size: merging verified target behavior into
current authority is the closed-out end state of an `implementation` package.
If the request is ambiguous, default to `design` and stop at the first
material user decision.

## Manifest

Initialize the package with
`scripts/init_package.py <dir> <size> <package-id> <baseline-revision>` and
keep `.rearchitecture-package.json` current:

```json
{
  "package_id": "R-001",
  "size": "design",
  "baseline_revision": "<revision>",
  "documents": {
    "scope": "00-scope.md",
    "positioning": "01-positioning.md",
    "l1": "02-l1-target.md",
    "mapping": "03-current-to-target-map.md",
    "l2": ["04-l2-contracts.md"],
    "adr": ["05-adr.md"],
    "handoff": "06-handoff.md",
    "review_report": "review-report.json",
    "review_ledger": "review-ledger.json"
  },
  "review": {"status": "pending", "reviewer": ""},
  "next_task": {"id": "S1", "owner": ""},
  "advancement_trigger": "<observable condition>",
  "stop_rule": "<abort / rollback / revise condition>"
}
```

Gate state is derived, not declared: the checker infers it from which files
exist and whether every finding is consumed. Never hand-edit a status to make
a gate look passed; the checker does not read prose claims.

## Hard gates

- No handoff while the manifest, any mapped artifact or any referenced
  evidence path is missing.
- No implementation without an authorized slice, a frozen L3 contract and
  legacy/target fixtures.
- No implementation while a blocking review finding is open or a material
  user decision is unanswered.
- Evidence must exist before it is claimed: an evidence reference is a
  repository path (optionally `::symbol` or `#anchor`) or a command plus a
  result artifact that actually exists.

## Working rules

- Ask the user only material questions, bundled, with a recommended default;
  record answers in the owning artifact. Load
  [`references/user-decision-gates.md`](references/user-decision-gates.md).
- Keep documents lean: one canonical owner per claim; link instead of copy.
  Before adding any document, abstraction or hard gate, apply
  [`references/doc-gates.md`](references/doc-gates.md).
- Plugins, process isolation, hot replacement and version coexistence are not
  default requirements. Load
  [`references/optional-concerns.md`](references/optional-concerns.md) only
  when the request activates one.

## Do not

- rewrite the whole codebase before proving one real slice;
- turn every file/class into a plugin or create duplicate state owners,
  schedulers, stores or buses without an explicit target decision;
- hide mixed responsibilities behind a renamed pass-through wrapper;
- claim decoupling from a lower dependency count alone;
- use a synthetic demo as the primary MVP exit condition;
- treat task notes, benchmark scores or generated prose as architecture
  authority.
