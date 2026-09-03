# User decision gates

Use this reference when repository evidence does not determine a material
architecture or delivery choice. Do not ask questions merely because a detail
is missing; first decide whether the answer changes scope, ownership,
deployment, compatibility, safety, success measure or migration order.

## How to ask

- State the observed facts and the unresolved choice.
- Offer a small set of materially different options, including a conservative
  recommendation when one is justified.
- Explain the consequence of each option and what becomes deferred.
- Ask only the questions needed to pass the current step; do not front-load
  task-level implementation details.
- Record the answer in the owning artifact named below. Conversation text is
  not the durable decision record.

## Gates and question sets

| Gate | Ask the user when evidence is insufficient | Record the answer in |
|---|---|---|
| Positioning and scope | What problem must this rearchitecture solve? Who is affected? What is explicitly out of scope? What constraints, compatibility promises and comparison baseline matter? | positioning / delivery horizon |
| L1 approval | Which system boundary, authority, deployment boundary or communication rule is preferred when the repository supports more than one materially different option? | L1 target architecture; material alternatives also get an ADR |
| L2 stabilization | Which trade-off should an experiment resolve (correctness, latency, operability, cost)? What risk or evidence threshold is acceptable? | L2 contract as conditional/open, then ADR |
| First slice | Which real vertical slice should be delivered first? What must it prove, and what must it not claim? | increment record and orientation page |
| Implementation handoff | Which task owner, acceptance threshold, compatibility window or rollback boundary is required when the project has not specified it? | L3 task contract or the project's existing task record |
| Review disposition | Does the user confirm rejecting, downgrading or accepting as an exception a blocking finding? | review ledger (exception approver) and increment record |
| Resume | Should the previous unmet gate be repaired first, or does the user explicitly authorize an exception? | increment record, including reason, approver and affected scope |

## Decision rules

- If the user has already answered a question in a current canonical artifact,
  do not ask it again; cite the artifact and continue.
- If no answer is available and the choice is material, stop at that gate
  rather than silently selecting a target architecture.
- If the user explicitly delegates the choice, choose the recommended default
  or the best-supported reversible option, record the delegation, the
  assumption and its reversal condition in the owning artifact, and continue.
- Make non-material reversible assumptions explicit instead of blocking
  progress.
