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
