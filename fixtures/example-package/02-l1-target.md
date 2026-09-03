# L1 target architecture (target, not current behavior)

- Subsystems: **Scheduler** (ordering and admission), **Job Store** (sole
  writer of job state), **Job Runtime** (execution workers).
- State authority: the Job Store is the only writer of durable job records.
  The Scheduler holds no durable state; it derives views through the store's
  query form.
- Identity: `job_id` is minted by the Job Store; `run_id` by the Job Runtime.
  The two are correlated by a store-owned receipt and never conflated.
- Dependency direction: Runtime → Store ← Scheduler. No subsystem calls
  another subsystem's internals.
- Entrypoint and deployment: one process, one HTTP entrypoint; the boundary
  in this package is a module boundary.
- Unresolved L1 questions: none open; retry-policy ownership is deferred with
  the delivery horizon.
