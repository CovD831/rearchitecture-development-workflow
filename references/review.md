# Independent review: adversarial pass, steelman, and consumption

Load this reference when running loop step 6, or after a material design
change. The phase is a two-agent workflow: the main session is the package
author and the sole consumer of findings; a separate sub-agent is the
reviewer. Never perform the review as a single uninterrupted authoring pass —
unreviewed self-review is what this step exists to prevent.

## Protocol

1. Freeze the review input: package path and revision, scope, review
   questions, and which artifacts may change afterwards.
2. Dispatch one independent reviewer sub-agent with a fresh context and a
   review-only prompt. The reviewer may not edit the package and may not set
   or clear gates.
3. Persist the reviewer's structured report as `review_report` (JSON).
4. Consume every finding into `review_ledger` (JSON): each finding gets a
   decision, a consumer artifact with an anchor, an owner, and evidence.
5. Update the L1/L2/ADR/migration/test artifacts the decisions point to, then
   re-run the checker.

One cycle = one adversarial pass plus one steelman, run together. Budget: one
cycle by default; one closure cycle is allowed only when blocking findings
were actually fixed and the input revision changed; anything more requires an
explicit user approval recorded in the increment record. If no independent
reviewer can be dispatched at all, leave `review.status: pending`, do not
self-review in place of the reviewer, and say so at the handoff.

A blocking finding keeps the handoff gate closed until the underlying risk is
resolved with evidence, or the user or an independent reviewer explicitly
accepts it as a recorded exception (approver named in the ledger). Rejecting
or deferring a blocking finding alone never opens the gate.

## Adversarial questions

### Scope and complexity

- Does the package solve a real coupling problem or only rename constructors?
- Can any proposed abstraction be deleted without losing a named safety or
  dependency benefit?
- Are future extension, live-update or distributed claims accidentally
  implied by the first-stage design?

### Authority and boundaries

- Is every durable fact assigned one writer?
- Does any view expose owner tokens, mutable records or arbitrary traversal?
- Can one subsystem mutate another's truth without an explicit command,
  authorization and receipt?
- Did a new bus, scheduler, database, cache or lifecycle authority appear?

### Lifecycle, failure and recovery

- What happens before and after durable admission?
- What happens if shutdown, observer cleanup or provider close fails?
- Does timeout, dependency loss or module removal destroy a domain entity
  without an explicit policy?
- Can an unknown external write be replayed or silently marked successful?
- Is the restart/rollback boundary explicit?

### Compatibility and evidence

- Is the legacy path still executable as a parity fixture?
- Are public results, durable facts, receipts and checkpoints compared rather
  than only "it runs"?
- Does a lower dependency count actually remove concrete coupling?
- Are performance claims tied to equivalent workloads and a stated baseline?

## Steelman prompts

- What important change becomes safer or easier because of this boundary?
- Which current authority is preserved instead of duplicated?
- Which developer or extension surface becomes smaller or clearer?
- Why is the selected MVP the smallest slice that can falsify the design?
- Which conservative exclusions prevent the project from becoming overbuilt?

## Report format (`review_report`)

The report must contain at least one finding; a review that finds nothing to
say has not looked.

```json
{
  "package_id": "R-001",
  "input_revision": "<frozen revision>",
  "reviewer": "<sub-agent id>",
  "findings": [
    {"id": "AR-001", "statement": "<claim>", "severity": "blocking | non-blocking",
     "evidence_refs": [], "recommendation": "<action>"}
  ],
  "steelman": {"strongest_support": "", "strongest_opposition": "",
               "decision_refs": ["05-adr.md"]},
  "overall": "pass | blocked"
}
```

`overall` is the reviewer's verdict on the frozen input: `blocked` when it
contained unresolved blocking findings. The handoff gate is never read from
the report — it is derived from the ledger after consumption.

## Ledger format (`review_ledger`)

```json
[
  {"finding_id": "AR-001", "severity": "blocking", "decision": "accepted",
   "consumer": {"path": "04-l2-contracts.md", "anchor": "write boundary"},
   "owner": "<owner>", "evidence": "tests/test_parity.py::test_parity",
   "status": "closed"}
]
```

- `decision`: `accepted`, `rejected`, `deferred` or `exception`.
- `consumer`: the artifact that absorbs the finding; `anchor` must be text
  that actually appears in that file, on a single line (the checker does a
  plain substring match). A finding with no consumer artifact is not
  consumed.
- `evidence`: a repository path (optionally `::symbol` or `#anchor`) that
  exists; required for `accepted` blocking findings.
- `exception` requires an `approver` field naming the user or independent
  reviewer who accepted the risk.
- `status`: `open` or `closed`. Blocking findings must be `closed` before
  handoff; non-blocking findings may stay `open` only with an owner and a
  named trigger.

The checker verifies mechanically: report and ledger finding IDs match
exactly, every entry is complete, anchors and evidence paths exist, and no
blocking finding is left open. If the report's findings would oscillate or the
budget is exhausted, stop with `review.status: blocked` and surface the
remaining options to the user.
