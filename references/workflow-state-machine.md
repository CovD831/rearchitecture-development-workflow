# Workflow state machine

The package lifecycle is a state machine. The main session may request a
transition, but it may not skip a state or set a derived approval state by
editing prose.

```text
draft → review_requested → review_received → consumption_pending
      → review_resolved → handoff_allowed
                 ↑                 ↓
                 └── next review round
Any failure, timeout, revision drift or unresolved blocking finding → blocked
```

State authority is split deliberately: the main session requests review and
records consumption; reviewer receipt and resolution are derived from
structured artifacts; `handoff_allowed` is derived only by the checker.

The manifest should record state history with `state`, `actor`, `timestamp`,
`input_revision` and `evidence_ref`. A revision mismatch invalidates the review.
The manifest should also record `review_round` and `max_review_rounds` (default
`3`). `review_resolved` is valid only after the round-specific stop conditions
in the review-agent protocol are satisfied.
