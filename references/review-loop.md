# Independent review loop

The review loop is an optional loop around the Layer 1 design core. It is not
the package state machine and it must not mutate the package directly.

## Stable state

Keep only these records as authoritative:

1. `review_input`: immutable package revision sent to the reviewer;
2. `review_run`: one record per reviewer invocation;
3. `review_report`: the reviewer's structured output for that run;
4. `consumption_record`: the main session's mapping of findings to decisions,
   artifacts and evidence;
5. `review_decision`: the derived outcome (`blocked`, `revise`, `experiment`,
   or `implementation-candidate`).

Do not use `state_history`, `review_rounds`, report fields and ledger fields as
independent sources of truth. They may be projections, but one run record must
own the identity, input revision, parent run and status.

## One normal cycle

```text
freeze input revision
  -> dispatch independent reviewer
  -> persist one immutable report
  -> main session consumes every finding
  -> derive decision
```

The reviewer never edits the package, closes its own findings or changes the
handoff gate. The main session is the only consumer and user-facing narrator.
The initializer may create a reviewer placeholder, but it is not provenance;
the logical reviewer ID and `independent: true` must be recorded after dispatch.

## Closure cycle

A second cycle is permitted only when all conditions hold:

- the previous report contains a blocking finding;
- the main session changed a named artifact or added executable evidence;
- the new input revision differs from the previous review input;
- the new run explicitly points to the parent run and consumed finding IDs.

If these conditions do not hold, do not dispatch another review. Remain
`blocked` or return `revise`.

## Stop conditions

Stop with `implementation-candidate` only when every blocking finding is
resolved or explicitly accepted by an authorized decision record and the
consumption record points to concrete evidence.

Stop with `blocked` when:

- a cycle makes no material progress;
- the input revision is unchanged;
- the same blocking finding is repeated without new evidence; or
- the bounded review budget is exhausted.

The default review budget is one normal cycle plus one closure cycle. A third
cycle requires an explicit user decision record naming the changed scope and
why two cycles were insufficient.

## Provenance separation

Review correctness and dispatch provenance are separate dimensions:

```text
review_status: pending | received | consumed | closed | blocked
provenance_status: unproven | proven
```

An unproven provenance status must not corrupt the review report or consumption
record. It only blocks claims that explicitly require external dispatch proof.

## User-visible projection

The user sees only the main session's checkpoint:

- cycle number and input revision;
- material findings;
- what the main session changed or deferred;
- current decision and next action.

Raw child-agent handoffs remain package evidence and are not automatically
shown to the user.
