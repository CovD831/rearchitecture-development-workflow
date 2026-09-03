# ADR-1: Job Store becomes the sole writer of job state

- Decision: route all durable job-row writes through a Job Store module with
  command/receipt forms; direct writes are removed behind a parity fixture.
- Alternatives: (a) keep direct writes and add lint rules (rejected: no
  enforceable invariant); (b) extract a job-state service process (deferred:
  module boundary is the smallest reversible step).
- Consequences: four call sites change; receipt correlation adds one durable
  column; scheduler loses direct row access.
- Status: approved for the first implementation slice; promotion re-review
  required after parity evidence.
