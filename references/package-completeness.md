# Package completeness and phase gates

Load this reference at intake and before handoff. A multi-document
rearchitecture effort is not complete because the documents exist or because
the prose mentions the missing work. The package must declare its profile and
machine-checkable gate state in `.rearchitecture-package.json`.

## Package profiles

Profiles select the package shape; layers select how much of that shape is
activated. Do not interpret a `design` profile as permission to require
implementation or promotion evidence. The minimum design closed loop may end
in `blocked`, `revise`, `experiment` or `implementation-candidate`.

Choose exactly one profile in the manifest:

| Profile | Purpose | Handoff allowed when |
|---|---|---|
| `orientation` | Short summary or decision intake | No implementation handoff; next gate is explicit |
| `design` | Target package before coding | L1, mapping, relevant L2, ADRs and review consumption are coherent; implementation evidence is not required |
| `implementation` | One vertical-slice task | Design gates plus frozen L3, fixtures, migration/rollback and acceptance evidence pass |
| `promotion` | Move verified target behavior into current authority | Implementation, compatibility evidence and authority update are all merged |

For `implementation`, the manifest must additionally map `l3`, `fixtures`,
`acceptance` and `rollback`. `promotion` must also map `authority_merge`.

The `design` profile must use `review_reports` even when there is only one
report. Add a new report file for each later round; do not overwrite an earlier
report. Every report must declare its `package_id` and `round`.

`orientation` is an entrypoint, never a substitute for a `design` or
`implementation` package. If the requested outcome is ambiguous, default to
`design` and stop at the first unresolved material user decision.

## Required manifest shape

```json
{
  "package_id": "R-001",
  "profile": "design",
  "status": "draft",
  "baseline_revision": "<exact revision or documented working tree>",
  "current_revision": "<latest consumed package revision>",
  "documents": {
    "scope": "00-scope-and-authority.md",
    "positioning": "01-positioning-and-complexity.md",
    "l1": "02-l1-target-architecture.md",
    "mapping": "03-current-to-target-map.md",
    "l2": ["04-l2-contracts.md"],
    "migration": "05-s1-migration-and-evidence.md",
    "adr": ["06-adr-r001.md"],
    "review": "07-adversarial-and-steelman.md",
    "review_reports": ["review-report.json", "review-round2-report.json"],
    "review_request": "review-request.json",
    "review_ledger": "review-ledger.json",
    "evidence_registry": "evidence-registry.json",
    "maintenance": "08-maintenance-and-catalog.md",
    "handoff": "<existing task or increment record>"
  },
  "gates": {
    "authority": "pass",
    "user_decisions": "pass",
    "l1": "pass",
    "mapping": "pass",
    "l2": "pass",
    "review": "pass",
    "evidence": "pending",
    "promotion": "pending"
  },
  "reviewer": {
    "id": "<sub-agent id>",
    "independent": true,
    "report_status": "pending"
  },
  "dispatch_receipt": {
    "request_id": "<review_run_id>",
    "source_thread": "<main session>",
    "reviewer_thread": "<independent sub-agent>",
    "started_at": "<timestamp>",
    "completed_at": "<timestamp>",
    "report_ref": "review-report.json"
  },
  "dispatch_receipt_ref": "../../.rearchitecture/dispatch-log/R-001-review-01.json",
  "review_state": "review_requested",
  "review_round": 1,
  "max_review_rounds": 3,
  "review_rounds": [],
  "state_history": [],
  "advancement_trigger": "<observable condition>",
  "promotion_evidence": ["<command or artifact>"],
  "stop_rule": "<abort, rollback or target-revision condition>",
  "next_task": {"id": "<task>", "owner": "<owner>"}
}
```

The manifest is the package's machine-readable index and gate state. Markdown
remains the canonical owner of rationale and evidence. Do not mark a gate
`pass` when it is only described as future work. `status: ready` is allowed
only when the validator reports no missing required artifact, broken link,
unresolved blocking finding or unanswered material decision.

## Layered hard-stop rules

- Layer 0 stops on missing scope, authority or next action.
- Layer 1 stops on incoherent target boundaries, unresolved material decisions
  or unconsumed blocking findings once review has been requested.
- Layer 2 stops on missing task-local contract, fixtures, acceptance or
  rollback evidence.
- Layer 3 stops on missing compatibility evidence or authority merge.
- The optional trust layer stops only claims that require externally proven
  reviewer provenance; it must not retroactively invalidate an earlier design
  package that made no such claim.

## Hard-stop rules

- Missing manifest, missing required artifact or broken link: stop.
- `design`/`implementation` handoff without adversarial review and steelman:
  stop.
- Any blocking review finding not resolved or explicitly accepted by the user
  or independent reviewer: stop.
- Missing next task, owner, advancement trigger or promotion evidence: stop.
- A summary document claiming to be the complete package: stop and relabel it
  as `orientation`.

Run `scripts/check_package_completeness.py <package-dir>` before publication or
handoff. The checker is a gate, not a documentation suggestion.
