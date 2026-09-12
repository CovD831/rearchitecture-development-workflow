# Document coherence and complexity gates

Load this reference when defining the complexity budget, adding architecture
documents, deciding whether an abstraction is justified, or before adding any
mechanism to this workflow itself.

## Complexity budget

Record:

- existing concepts a reader must understand;
- every new noun, boundary, document and runtime mechanism proposed;
- the concrete coupling, duplication or safety problem each addition removes;
- the smallest alternative considered and why it is insufficient;
- the real consumer, owner and acceptance evidence for every new concept.

Defer a concept that has no real consumer, owner or acceptance evidence.
Prefer bounded claims such as "a topology change does not rewrite long-lived
business commitments" over "more modular" or "more scalable".

## Canonical document ownership

Before creating a document, locate the canonical owner for its claim. Add a
focused section or link when that owner remains correct. Create a new document
only when ownership, status, audience or lifecycle is materially different.
For a multi-document package: one short orientation page; one purpose and one
canonical claim owner per document; summaries shorter than their sources;
status, owner and supersession visible; relative links validated before
publication.

## Claim drift

Documents rot in one specific way: a claim that something exists, does not
exist, or is in a certain state stays readable after the change that made it
false. Three instances from one real run (2026-09-12, all three discovered in a
single afternoon):

- a handoff page still said the work was uncommitted after it had been pushed;
- a gate-definition document still listed a route as preserved after the route
  had been deleted;
- a readiness table still said the auth posture was "decided and implemented"
  while the running configuration had that feature switched off.

Before closing a step or a handoff, walk the package and ask of every claim
that asserts a fact about the system, the process or a gate:

- What change would falsify this claim?
- Did this increment make one of those changes?

A claim carrying an implicit "still true" is the one that rots. Counts, file
lists, "remains unchanged", "already implemented" and status words are the usual
carriers — a number in a table is a claim, not decoration.

Correct by preserving the record, not rewriting it: keep the historical text,
add a dated status banner at the top, and add an explicit update section naming
what is no longer true. Silently editing the old text destroys the evidence that
drift happened, which is the part a reader needs to trust the rest. This is the
same principle as never rewriting a historical manifest's gate state.

Never restate a state you have not re-measured in this run. "Should still be
true" is not evidence; when re-measuring is cheap, re-measure.

## Over-design gate

- Does every new abstraction have a real consumer or safety requirement?
- Does it remove a concrete dependency/registration path or enforce an
  invariant?
- Are owner and non-responsibility explicit?
- Is there a smaller reversible alternative?
- Are future features deferred instead of represented by empty modules?
- Can the MVP be implemented and falsified without building the whole
  platform?

## Before adding a hard gate or mechanism

Apply the same discipline to workflow machinery itself (including to this
skill). Admit a new gate, manifest field or validation rule only when all five
are explicit:

1. Which loop step needs it?
2. Which concrete consumer uses it?
3. What unsafe outcome does it prevent?
4. Can a script check it without interpreting prose?
5. Does it duplicate an existing rule or owner?

Otherwise record it as a reviewer question or warning, not a blocker.

## Stopping conditions

If the complexity budget is exceeded, a blocking finding cannot be closed, or
no safe smaller alternative exists, stop and present the remaining options and
trade-offs to the user. Do not silently expand or shrink scope.
