# Layered rearchitecture workflow

The workflow is progressive. Start with the smallest layer that answers the
next decision, then add a layer only when its evidence has a named consumer.
New manifests created by `init_package_manifest.py` use `validation_mode:
layered`; older manifests remain on the compatibility strict validator until
they explicitly opt in.

## Layer 0 — orientation (optional)

Produce only a bounded entrypoint: current authority, baseline, scope, next
decision, owner and trigger. It never authorizes implementation and does not
require review, L3 contracts, fixtures, provenance or promotion evidence.

## Layer 1 — minimum design closed loop

This is the minimum useful rearchitecture package:

```text
manifest -> authority/scope -> positioning -> L1 target
  -> current-to-target map -> relevant L2 -> ADR
  -> independent review/steelman -> finding consumption
  -> explicit outcome + next task
```

It proves that the direction is bounded and reviewable; it does not prove that
the target is implementable. Valid outcomes are `blocked`, `revise`,
`experiment` and `implementation-candidate`. The last is a recommendation for
the next package, not implementation authorization.

Use `scripts/check_package_completeness.py --phase design-core <package-dir>`
for this layer. The default checker remains the strict handoff validator.

When review is explicitly requested, use
`scripts/check_package_completeness.py --phase review-loop <package-dir>`.

When a selected vertical slice enters implementation, use
`scripts/check_package_completeness.py --phase implementation-evidence
<package-dir>`.

Use `scripts/check_package_completeness.py --phase provenance <package-dir>`
only when the package claims externally proven reviewer dispatch. Without
`provenance_required: true`, the result is explicitly `unproven`, not a core
package failure.

## Layer 2 — implementation slice

Activate only after a named vertical slice exists. Add only its task-local L3
contract, legacy/target fixtures, acceptance/failure matrix, migration,
compatibility and rollback evidence. Do not create L3 material for unselected
modules.

## Layer 3 — promotion

Activate only after Layer 2 evidence exists. Add compatibility/parity results,
recovery/replay and failure-injection results where applicable, authority merge
and the removal gate. Only this layer may move target behavior into current
authority.

## Optional trust layer — runtime provenance

Host hooks, external dispatch receipts and runtime identity are an optional
trust enhancement around independent review. Require them only when external
reviewer-dispatch proof is explicitly claimed or repository policy mandates it.
They must not make a Layer 1 design package require implementation evidence.

## Escalation rule

At the end of each layer record exactly one next action: revise, run a named
experiment, advance, or stop/preserve. Adding a document or field is not an
escalation reason by itself; the new layer needs a named consumer, owner and
evidence threshold.

## Gate ownership

- Layer 0: main session.
- Layer 1: independent reviewer plus main-session consumption.
- Layer 2: implementation task owner.
- Layer 3: promotion owner and repository authority owner.
- Trust layer: host runtime/operator; the checker only verifies receipts.
