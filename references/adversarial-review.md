# Adversarial review and bidirectional steelman worksheet

Use this after the package has a concrete vertical slice and before publication
or implementation handoff. Prefer a reviewer who did not write the design; if
that is not possible, use a fresh context and record the limitation.

## When to run

Run the review:

1. after the draft system/boundary package has a concrete vertical slice and
   before implementation approval;
2. after a material design change or experiment result;
3. before publishing or merging a change that alters an authority, contract,
   migration boundary or deployment claim.

## Adversarial questions

### Scope and complexity

- Does the package solve a real coupling problem or only rename constructors?
- Can any proposed abstraction be deleted without losing a named safety or
  dependency benefit?
- Are future extension, live-update, process-host or distributed claims
  accidentally implied by the first-stage design?

### Authority and boundaries

- Is every durable fact assigned one writer?
- Does any view expose owner tokens, mutable records or arbitrary traversal?
- Can one subsystem mutate another subsystem's truth without an explicit
  command, authorization and receipt?
- Did a new bus, scheduler, database, cache or lifecycle authority appear?

### Lifecycle, failure and recovery

- What happens before and after durable admission?
- What happens if shutdown, observer cleanup or provider close fails?
- Does timeout, heartbeat, dependency loss or module removal destroy or release
  a domain entity without an explicit policy?
- Can an unknown external write be replayed or silently marked successful?
- Is the restart/rollback boundary explicit?

### Compatibility and evidence

- Is the legacy path still executable as a parity fixture?
- Are public results, durable facts, receipts, revisions and checkpoints
  compared rather than only “it runs”?
- Does a lower dependency count actually remove concrete coupling?
- Are benchmark claims tied to equivalent workloads and a stated baseline?

## Steelman prompts

- What important change becomes safer or easier because of this boundary?
- Which current authority is preserved instead of duplicated?
- Which developer or extension surface becomes smaller or clearer?
- Why is the selected MVP the smallest slice that can falsify the design?
- Which conservative exclusions prevent the project from becoming overbuilt?

## Reconciliation record

For each concern, record:

| Finding | Evidence | Severity | Decision | Consuming action | Owner/gate |
|---|---|---|---|---|---|
|  |  | blocking / non-blocking | accept / reject / defer | document, test, ADR, implementation or issue |  |

Decision and severity are separate axes. Accept findings by updating the
relevant architecture/contract/test/task before the next gate. Reject findings
only with recorded evidence and rationale. Defer findings through a named
future task or decision record with an owner and trigger. A blocking finding
keeps the gate closed until the underlying risk is resolved or the finding is
explicitly reclassified as non-blocking, or accepted as a documented exception,
by user confirmation or independent reviewer sign-off. Rejecting a blocking
finding requires the same explicit confirmation; rationale alone does not open
the gate. A blocking finding cannot be deferred while retaining blocking
severity, and merely creating a future task/ADR does not close the gate. Block
publication when a concern violates an
invariant, creates duplicate authority, makes recovery undefined, or makes the
vertical slice unverifiable. Keep readability improvements and future
opportunities explicitly non-blocking so they do not reopen a settled
architecture.
