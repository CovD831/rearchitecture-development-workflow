# Independent review-agent protocol

The adversarial review and bidirectional steelman phase is a two-agent
workflow. The main session is the package author and consumer; a separate
sub-agent is the reviewer. Do not perform this phase as a single uninterrupted
authoring pass.

## Visibility boundary

Reviewer-to-main-session messages and reviewer reports are internal workflow
artifacts. They are not user-facing by default. The main session is the sole
user-facing narrator: it consumes the report, decides what is relevant to
surface, and presents a concise status, material findings, decisions, open
risks and handoff state. Do not forward raw sub-agent messages unless the user
explicitly asks to inspect them.

## Required sequence

1. The main session freezes the review input: package path/revision, scope,
   review questions, and the artifacts that may be changed after review.
2. The main session starts one independent sub-agent with a review-only prompt.
   The reviewer must not edit the package or mark gates.
3. The reviewer returns a structured report containing reviewer identity,
   baseline, findings, steelman, and evidence requests.
4. The main session writes the report to the canonical review artifact without
   silently rewriting findings.
5. The main session creates or updates the finding-consumption ledger. Every
   finding gets an ID, decision, consumer, owner, gate and evidence.
6. The main session presents the user-facing review checkpoint (round, status,
   finding counts, blocking risks and next action), then updates the relevant
   L1/L2/ADR/migration/test artifacts,
   then sends the consumed result back to the reviewer for confirmation when a
   blocking finding was resolved or reclassified.
7. Only after consumption is recorded may the main session run the package
   checker and request handoff.

## Review rounds

The default is not an unconditional single pass. Use rounds driven by material
change:

1. **Round 1 — discovery:** independent adversarial review and bidirectional
   steelman against the frozen package revision.
2. **Round 2 — closure:** required when Round 1 has any blocking finding, when
   the main session changes an authority/boundary/ADR/migration rule, or when
   the reviewer requests evidence. The reviewer checks the consumed ledger and
   the new evidence against the changed revision.
3. **Round 3 — exception review:** only when Round 2 still has a disputed
   blocking finding or a material revision. It requires explicit user or
   independent-reviewer disposition; it is not an automatic retry.

Stop with `review_resolved` when the latest round finds no unresolved blocking
finding, every finding has a consumer/owner/gate/evidence entry, steelman
decision impact is referenced by an ADR/L1/L2/migration artifact, and the
reviewer confirms the current revision. Stop with `blocked` when the reviewer
fails or times out, the revision drifts, a blocking finding remains after
Round 3, findings oscillate between decisions, or the review budget is
exceeded. Non-blocking findings may remain deferred only with an owner and
advancement trigger; deferral never opens a blocked gate.

Record `round`, `review_run_id`, `parent_review_run_id`, `input_revision`,
`post_consumption_revision`, `trigger`, and
`closure_confirmation` for every report. A new material finding starts another
round; cosmetic edits do not.

The review state is monotonic and may not skip a state:

```text
draft → review_requested → review_received → consumption_pending
      → review_resolved | blocked → handoff_allowed
```

`handoff_allowed` is a derived state, never a value the author may set to
override an earlier state.

At minimum, the main session should present checkpoints before review, after a
review report is received, after finding consumption, and before handoff. The
checkpoint is a derived summary; the canonical report and ledger remain in the
package.

## Reviewer report minimum

Use JSON for machine-consumed reports. Markdown may mirror the report for
readability, but the JSON report is authoritative and immutable.

```json
{
  "package_id": "R-001",
  "round": 1,
  "review_run_id": "AR-2026-09-03-01",
  "reviewer": {"agent_id": "<sub-agent id>", "independent": true, "input_revision": "<revision>"},
  "findings": [{"id": "AR-001", "statement": "<claim>", "severity": "blocking", "evidence_refs": [], "recommendation": "<action>"}],
  "steelman": {"strongest_support": "", "strongest_opposition": "", "fact_checks": [], "retained_decisions": [], "removed_decisions": [], "changed_boundaries": [], "deferred_gates": [], "final_decision": "", "decision_refs": []},
  "overall": "blocked",
  "closure_confirmation": false
}
```

`overall: pass` means only that the reviewer found no unresolved blocking issue
in the frozen input. It does not authorize handoff and cannot replace the
main-session consumption step.

## Consumption ledger minimum

```json
[{"finding_id": "AR-001", "severity": "blocking", "decision": "accept", "consumer_refs": [{"kind": "path", "ref": "04-l2-contracts.md"}], "task_ref": "S1", "test_or_evidence_refs": [{"kind": "path", "ref": "tests/test_parity.py::test_legacy_target_parity"}], "owner": "<owner>", "gate": "S1 promotion", "status": "pending", "resolution_ref": null}]
```

No review gate can pass while a finding lacks a consumer, owner, gate or
evidence. A blocking finding requires `resolved` evidence or an explicit,
durable exception approved by the user or an independent reviewer.
