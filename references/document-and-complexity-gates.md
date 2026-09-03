# Document coherence and complexity gates

Load this reference when defining the complexity budget, adding architecture
documents or deciding whether a proposed abstraction is justified.

## Complexity budget

Record:

- existing concepts a reader must understand;
- every new noun, boundary, document and runtime mechanism proposed;
- the concrete coupling, duplication or safety problem each addition removes;
- the smallest alternative considered and why it is insufficient;
- the real consumer, owner and acceptance evidence for every new concept.

Defer a concept that has no real consumer, owner or acceptance evidence. Prefer
bounded claims such as “a topology change does not rewrite long-lived business
commitments” over “more modular” or “more scalable.”

## Canonical document ownership

Before creating a document, locate the canonical owner for its claim. Add a
focused section or link when that owner remains correct. Create a new document
only when ownership, status, audience or lifecycle is materially different.

For a multi-document package:

- provide one short orientation page for the target, current increment and next
  action;
- give each document one purpose and one canonical claim owner;
- keep summaries shorter than their sources and link rather than copy;
- maintain a reading route, status, owner, review date and supersession data;
- validate relative links and the document catalog before publication.

The delivery-horizon/increment record is the canonical owner of detailed
deferrals and advancement conditions. Other documents keep only the local
summary needed for orientation.

## Document coherence gate

- Can a new reader find the target, current increment and next action from one
  entrypoint?
- Does every major claim have one canonical owner?
- Are current behavior, target intent, plans and frozen evidence visibly
  distinguished?
- Are status, owner, review date, supersession and inbound links consistent?
- Can the package be read through both a short route and a deeper review route?

## Over-design gate

- Does every new abstraction have a real consumer or safety requirement?
- Does it remove a concrete dependency/registration path or enforce an
  invariant?
- Are owner and non-responsibility explicit?
- Is there a smaller reversible alternative?
- Are future features deferred instead of represented by empty modules?
- Can the MVP be implemented and falsified without building the whole platform?

If either gate fails, simplify or split the package before adding detail. If the
complexity budget is exceeded, a blocking finding cannot be closed or no safe
smaller alternative exists, stop and present the remaining options and
trade-offs. Do not silently expand or shrink scope.

